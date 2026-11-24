"""Resumable, rate-limited evidence updater. No lifetime target number of matches."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

from ranked_matchups import ROOT, RiotClient, RiotError, write_json, extract_match, METRICS
from rank_eligibility import read_policy, utc, TIERS
from collect_rank_snapshots import parse_snapshot, classify_match
from rank_coverage import ROLE_MAP
from rank_lake import RankLake, exclusive_writer, import_snapshot_runs


def now(): return datetime.now(timezone.utc)


def fetch_snapshot(lake, client, platform, participant, ended, raw, ttl_minutes=15):
    puuid = participant['puuid']
    record = lake.snapshot(platform,puuid)
    if record and record.get('status') == 'ok':
        age = (now()-utc(record['observed_at'])).total_seconds()
        if 0 <= age <= ttl_minutes*60 and utc(record['observed_at']).timestamp() >= ended:
            return record, False
    payload = client.get(platform,f'/lol/league/v4/entries/by-puuid/{puuid}')
    observed = now().isoformat()
    slug = hashlib.sha256(puuid.encode()).hexdigest()
    path = raw/'snapshots'/slug/(now().strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    write_json(path,{'platform':platform.upper(),'observed_at':observed,'response':payload})
    record = parse_snapshot(payload,puuid,platform,observed,str(path.relative_to(raw)))
    lake.cache_snapshot(record)
    return record, True


def process_job(lake, client, job, policy, raw):
    mid, platform, routing = job['match_id'],job['platform'],job['routing']
    detail_path = Path(job['detail_path']) if job['detail_path'] else raw/'matches'/f'{mid}.match.json'
    fetched_at = job['detail_fetched_at']
    if detail_path.exists():
        detail = json.loads(detail_path.read_text(encoding='utf-8'))
        if not fetched_at:
            # File may have survived a crash before the SQL checkpoint; do not invent an earlier availability.
            fetched_at=now().isoformat()
            with lake.db: lake.db.execute('UPDATE jobs SET detail_path=?,detail_fetched_at=? WHERE match_id=?',(str(detail_path),fetched_at,mid))
    else:
        detail = client.get(routing,f'/lol/match/v5/matches/{mid}')
        if detail.get('metadata',{}).get('matchId') != mid:
            raise ValueError('Match detail identity mismatch')
        fetched_at = now().isoformat()
        write_json(detail_path,detail)
        with lake.db:
            lake.db.execute('UPDATE jobs SET detail_path=?,detail_fetched_at=? WHERE match_id=?',(str(detail_path),fetched_at,mid))
    info = detail['info']
    ended = max(info['gameStartTimestamp']/1000+info['gameDuration'],(info.get('gameEndTimestamp') or 0)/1000)
    defaults = policy['snapshot_collection']
    # Preserve an already qualified cohort when resuming a delayed timeline download.
    saved = json.loads(job['evidence_json']) if job['evidence_json'] else None
    if saved:
        snaps={(r['platform'],r['puuid']):r for r in saved['snapshots']}
        classification=saved['classification']; available=saved['available_at']; fresh=0
    else:
        classification,snaps,available,fresh = qualify(lake,client,detail,platform,policy,raw,ended,fetched_at)
        if classification['status']!='accepted':
            lake.persist_result(mid,classification,available,[])
            return classification['status'],fresh
        with lake.db:
            lake.db.execute('UPDATE jobs SET evidence_json=? WHERE match_id=?',
                (json.dumps({'snapshots':list(snaps.values()),'classification':classification,'available_at':available}),mid))
        lake.persist_result(mid,classification,available,[])
    timeline_path = Path(job['timeline_path']) if job['timeline_path'] else raw/'matches'/f'{mid}.timeline.json'
    if timeline_path.exists():
        timeline = json.loads(timeline_path.read_text(encoding='utf-8'))
        with lake.db: lake.db.execute('UPDATE jobs SET timeline_path=? WHERE match_id=?',(str(timeline_path),mid))
    else:
        timeline = client.get(routing,f'/lol/match/v5/matches/{mid}/timeline')
        if timeline.get('metadata',{}).get('matchId') != mid:
            raise ValueError('Timeline identity mismatch')
        write_json(timeline_path,timeline)
        with lake.db: lake.db.execute('UPDATE jobs SET timeline_path=? WHERE match_id=?',(str(timeline_path),mid))
    measured = extract_match(detail,timeline,'nearest')
    data = []
    for r in measured:
        p = next(p for p in info['participants'] if p['teamId']==r['team_id'] and ROLE_MAP[p['teamPosition']]==r['role'])
        enemy = next(e for e in info['participants'] if e['teamId']!=p['teamId'] and e['teamPosition']==p['teamPosition'])
        snap = snaps[(platform.upper(),p['puuid'])]
        r.update(tier_floor=policy['pro']['rank_tier_floor'],champion_id=p['championId'],opponent_id=enemy['championId'],
                 _puuid=p['puuid'],_enemy_puuid=enemy['puuid'],available_at=available,
                 tier_at_observation=snap['tier'],rank_observed_at=snap['observed_at'],historical_rank_verified=False)
        data.append(r)
    lake.persist_result(mid,classification,available,data)
    return 'accepted',fresh


def qualify(lake,client,detail,platform,policy,raw,ended,fetched_at):
    info=detail['info']; defaults=policy['snapshot_collection']; mid=detail['metadata']['matchId']
    # Reject out-of-window/invalid games before spending ten tier requests.
    from rank_eligibility import assess_match
    structural = assess_match(detail,[],policy,now())
    invalid = [r for r in structural['reasons'] if r!='not_all_ten_documented_high_at_match']
    if (now().timestamp()-ended)/3600 > defaults['max_match_age_hours']:
        invalid.append('match_too_old_for_near_match_proxy')
    if invalid:
        return {'status':'rejected','match_id':mid,'reasons':invalid},{},now().isoformat(),0
    snaps, fresh = {}, 0
    for p in info['participants']:
        try:
            record, fetched = fetch_snapshot(lake,client,platform,p,ended,raw)
            fresh += int(fetched)
        except RiotError as exc:
            if exc.status_code != 404:
                raise
            record = {'puuid':p['puuid'],'platform':platform.upper(),'queue':'RANKED_SOLO_5x5',
                      'kind':'snapshot','observed_at':now().isoformat(),'tier':None,'status':'api_error'}
        snaps[(platform.upper(),p['puuid'])] = record
        if record.get('status')=='ok' and TIERS.index(record['tier']) >= TIERS.index(policy['pro']['rank_tier_floor']):
            lake.add_seed(platform,p['puuid'],record['tier'],'observed_participant',record['observed_at'])
    classification = classify_match(detail,snaps,policy,now(),defaults['max_match_age_hours'],defaults['max_snapshot_spread_minutes'])
    available = max([utc(fetched_at)] + [utc(r['observed_at']) for r in snaps.values()]).isoformat()
    return classification,snaps,available,fresh


def discover_seed(lake, client, routing_by_platform, policy):
    placeholders=','.join('?' for _ in routing_by_platform)
    seed = lake.db.execute(f'''SELECT * FROM seeds WHERE last_polled<? AND platform IN ({placeholders})
      ORDER BY CASE tier WHEN 'CHALLENGER' THEN 0 WHEN 'GRANDMASTER' THEN 1 ELSE 2 END,last_polled,platform,puuid LIMIT 1''',
      (time.time()-600,*routing_by_platform)).fetchone()
    if seed is None:
        return False
    platform = seed['platform']
    params = {'queue':420,'type':'ranked','start':seed['page_start'],'count':100,
              'startTime':int(time.time()-policy['snapshot_collection']['max_match_age_hours']*3600)}
    try:
        ids = client.get(routing_by_platform[platform],f'/lol/match/v5/matches/by-puuid/{seed["puuid"]}/ids',params)
    except RiotError as exc:
        if exc.status_code!=404: raise
        with lake.db: lake.db.execute('UPDATE seeds SET last_polled=? WHERE platform=? AND puuid=?',(time.time(),platform,seed['puuid']))
        return True
    if not isinstance(ids,list): raise ValueError('Invalid match-list response')
    import re
    for mid in ids:
        if not re.fullmatch(r'[A-Z0-9]+_\d+',mid) or mid.split('_')[0].lower()!=platform:
            continue
        lake.enqueue(mid,platform,routing_by_platform[platform])
    with lake.db:
        lake.db.execute('UPDATE seeds SET last_polled=?,page_start=? WHERE platform=? AND puuid=?',
            (0 if len(ids)==100 else time.time(),seed['page_start']+100 if len(ids)==100 else 0,platform,seed['puuid']))
    return True


def bootstrap(lake,client,platforms,raw=None):
    raw=Path(raw) if raw is not None else ROOT/'data/raw/rank_lake'
    for platform in platforms:
        for tier,endpoint in [('CHALLENGER','challengerleagues'),('GRANDMASTER','grandmasterleagues'),('MASTER','masterleagues')]:
            # Membership is an actual current-rank response, not a seed-only inference.
            key=f'bootstrap_rank_lists:{platform}:{tier}'
            if float(lake.meta(key) or 0) > time.time()-900:
                continue
            payload = client.get(platform,f'/lol/league/v4/{endpoint}/by-queue/RANKED_SOLO_5x5')
            if not isinstance(payload,dict) or not isinstance(payload.get('entries'),list):
                raise RiotError('Invalid ranked league-list response',reason_code='invalid_league_list')
            if payload.get('tier') != tier or payload.get('queue') != 'RANKED_SOLO_5x5':
                raise RiotError('League-list tier/queue mismatch',reason_code='invalid_league_list')
            observed=now().isoformat()
            path=raw/'league_lists'/platform/tier/(now().strftime('%Y%m%dT%H%M%S%fZ')+'.json')
            write_json(path,{'platform':platform.upper(),'observed_at':observed,
                'endpoint':f'/lol/league/v4/{endpoint}/by-queue/RANKED_SOLO_5x5','response':payload})
            seeds=[];snapshots=[]
            for entry in payload.get('entries',[]):
                if isinstance(entry,dict) and isinstance(entry.get('puuid'),str) and entry['puuid']:
                    puuid=entry['puuid']
                    record=parse_snapshot([{'queueType':payload['queue'],'tier':payload['tier'],
                        'rank':entry.get('rank'),'leaguePoints':entry.get('leaguePoints')}],
                        puuid,platform,observed,str(path.relative_to(raw)))
                    record['source_kind']='league_list_membership'
                    seeds.append((platform.lower(),puuid,tier,'league_list',observed))
                    snapshots.append((platform.lower(),puuid,observed,json.dumps(record)))
            with lake.db:
                lake.db.executemany('''INSERT INTO seeds(platform,puuid,tier,source,observed_at) VALUES(?,?,?,?,?)
                    ON CONFLICT(platform,puuid) DO UPDATE SET tier=excluded.tier,source=excluded.source,observed_at=excluded.observed_at''',seeds)
                lake.db.executemany('INSERT OR REPLACE INTO snapshots VALUES(?,?,?,?)',snapshots)
            lake.set_meta(key,str(time.time()))


def next_job(lake,client,routes,policy):
    """Persist round-robin platform order, including discovery amid a backlog."""
    platforms=list(routes)
    previous=lake.meta('scheduler:last_platform')
    if previous in platforms:
        offset=platforms.index(previous)+1
        platforms=platforms[offset:]+platforms[:offset]
    for platform in platforms:
        def pending():
            return lake.db.execute('''SELECT * FROM jobs WHERE next_attempt<=? AND platform=? AND
                (status IN ('pending','missing') OR (status='accepted' AND NOT EXISTS
                (SELECT 1 FROM observations o WHERE o.match_id=jobs.match_id))) ORDER BY rowid LIMIT 1''',
                (time.time(),platform)).fetchone()
        job=pending()
        if job is None:
            discover_seed(lake,client,{platform:routes[platform]},policy)
            job=pending()
        if job is not None:
            lake.set_meta('scheduler:last_platform',platform)
            return job
    return None


def session(args):
    from config.settings import RIOT_API_KEY, SERVER_METADATA
    from rank_matchup_tables import export_tables
    policy = read_policy(args.policy)
    routes = {p:SERVER_METADATA[p]['region'] for p in args.platforms}
    sid = now().strftime('%Y%m%dT%H%M%S%fZ')
    client = RiotClient(RIOT_API_KEY,min_interval=1.3,max_requests=args.max_requests,deadline=time.monotonic()+args.max_minutes*60)
    with exclusive_writer(args.db):
        lake = RankLake(args.db,policy)
        started = now().isoformat(); processed=0; fresh=0; stop='idle'; last_export=time.monotonic()
        with lake.db: lake.db.execute('INSERT INTO sessions(session_id,started_at,status) VALUES(?,?,?)',(sid,started,'running'))
        try:
            import_snapshot_runs(lake,args.old_reports,args.old_private,policy)
            export_tables(lake,args.output,args.min_games,args.target_games_per_matchup)
            bootstrap(lake,client,args.platforms,args.raw)
            while True:
                if client.request_attempts>=args.max_requests:
                    stop='request_budget_exhausted'; break
                if time.monotonic()>=client.deadline:
                    stop='session_time_limit'; break
                job=next_job(lake,client,routes,policy)
                if job is None: break
                try:
                    _, n = process_job(lake,client,job,policy,args.raw)
                    fresh+=n; processed+=1
                except RiotError as exc:
                    if exc.status_code != 404: raise
                    lake.persist_result(job['match_id'],{'status':'missing','reasons':['api_404']},now().isoformat(),[])
                except (ValueError,KeyError,TypeError,StopIteration):
                    lake.persist_result(job['match_id'],{'status':'rejected','reasons':['invalid_match_or_timeline_payload']},now().isoformat(),[])
                    processed+=1
                if processed and (processed%5==0 or time.monotonic()-last_export>=60):
                    export_tables(lake,args.output,args.min_games,args.target_games_per_matchup)
                    last_export=time.monotonic()
                    print(json.dumps({'processed_this_session':processed,'http_attempts':client.request_attempts,**lake.counts()}),flush=True)
        except RiotError as exc:
            stop=exc.reason_code if exc.status_code is None else f'http_{exc.status_code}'
        except KeyboardInterrupt:
            stop='interrupted'
        finally:
            detail={'session_id':sid,'stop_reason':stop,'processed_this_session':processed,'fresh_snapshots':fresh,
                    'http_attempts':client.request_attempts,'request_budget':args.max_requests,'counts':lake.counts()}
            with lake.db: lake.db.execute('UPDATE sessions SET finished_at=?,status=?,http_attempts=?,detail_json=? WHERE session_id=?',
                (now().isoformat(),stop,client.request_attempts,json.dumps(detail),sid))
            export_tables(lake,args.output,args.min_games,args.target_games_per_matchup)
            write_json(args.output/'sessions'/f'{sid}.json',detail)
            lake.close()
        print(json.dumps(detail),flush=True)
        return stop


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,default=ROOT/'data/database/ranked_evidence.db')
    p.add_argument('--raw',type=Path,default=ROOT/'data/raw/rank_lake')
    p.add_argument('--output',type=Path,default=ROOT/'reports/rank_matchups_live')
    p.add_argument('--policy',type=Path,default=ROOT/'src/config/draft_modes.json')
    p.add_argument('--old-reports',type=Path,default=ROOT/'reports/rank_snapshot_collection')
    p.add_argument('--old-private',type=Path,default=ROOT/'data/raw/riot_rank_snapshots')
    p.add_argument('--platforms',default='kr')
    p.add_argument('--max-requests',type=int,default=600)
    p.add_argument('--max-minutes',type=float,default=15)
    p.add_argument('--min-games',type=int,default=5)
    p.add_argument('--target-games-per-matchup',type=int,default=None,help='Optional legacy manual progress target; no fixed quota by default, never claims U.GG parity.')
    p.add_argument('--watch',action='store_true',help='Repeat bounded sessions until stopped or auth/service failure; no lifetime match cap.')
    p.add_argument('--pause-seconds',type=float,default=60)
    p.add_argument('--export-only',action='store_true')
    a=p.parse_args(); a.platforms=list(dict.fromkeys(a.platforms.lower().split(',')))
    if not set(a.platforms)<= {'kr','vn2','tw2','na1','euw1'} or not(1<=a.max_requests<=10000 and 0<a.max_minutes<=240 and a.min_games>=1 and a.pause_seconds>=1 and (a.target_games_per_matchup is None or a.target_games_per_matchup>=1)):
        p.error('Invalid platform/session limits')
    if a.export_only:
        from rank_matchup_tables import export_tables
        with exclusive_writer(a.db):
            lake=RankLake(a.db,read_policy(a.policy))
            try: export_tables(lake,a.output,a.min_games,a.target_games_per_matchup)
            finally: lake.close()
        return 0
    while True:
        reason=session(a)
        if not a.watch or reason not in ('request_budget_exhausted','session_time_limit','idle'):
            return 0 if reason in ('request_budget_exhausted','session_time_limit','idle','interrupted') else 2
        try: time.sleep(a.pause_seconds)
        except KeyboardInterrupt: return 0


if __name__=='__main__':
    raise SystemExit(main())
