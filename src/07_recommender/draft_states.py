"""Observed pre-action draft states with conservative reconstructed series groups.

Labels/final results/roles are never included in state_features(). Unknown series
prefixes or invalid Fearless histories are rejected, not silently filled in.
"""
from collections import defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import sys
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from analysis_data import load_clean_tables
from draft_meta import patch_code


def action_order(first):
    second='Red' if first=='Blue' else 'Blue'
    a,b=first,second
    return ([(s,'ban') for s in [a,b]*3]+[(s,'pick') for s in [a,b,b,a,a,b]]+
            [(s,'ban') for s in [b,a,b,a]]+[(s,'pick') for s in [b,a,a,b]])


def state_features(state):
    """Explicit allowlist: no label, outcome, final roles, IDs or future roster."""
    features={k:str(state[k]) for k in ['action','slot','actor_team','opponent_team','league','patch']}
    features.update(turn=float(state['turn']),game_number=float(state['game_number']))
    for key in ['own_picks','enemy_picks','own_bans','enemy_bans','used_champions']:
        values=state.get(key,[])
        features[f'{key}_count']=float(len(values))
        features.update({f'{key}={c}':1. for c in values})
    return features


def game_states(rows,used,series_id):
    if len(rows)!=2 or set(rows.side)!={'Blue','Red'}:raise ValueError('not_two_sides')
    first_flags=pd.to_numeric(rows.firstPick,errors='coerce')
    if sorted(first_flags.tolist())!=[0,1]:raise ValueError('invalid_firstPick')
    if pd.to_datetime(rows.date,utc=True).nunique()!=1:raise ValueError('inconsistent_team_dates')
    first=rows.loc[first_flags.eq(1),'side'].iloc[0]
    teams={r.side:r for r in rows.itertuples(index=False)}
    picks={s:[] for s in teams};bans={s:[] for s in teams};records=[]
    for turn,(side,action) in enumerate(action_order(first),1):
        enemy='Red' if side=='Blue' else 'Blue'
        number=len(picks[side] if action=='pick' else bans[side])+1
        champion=getattr(teams[side],f'{action}{number}',None)
        if pd.isna(champion) or not str(champion).strip() or str(champion).lower() in ['none','noban','null']:
            raise ValueError('missing_or_skipped_action')
        champion=str(champion)
        unavailable=set(used)|set(sum(picks.values(),[]))|set(sum(bans.values(),[]))
        if champion in unavailable:raise ValueError('duplicate_or_Fearless_locked_action')
        row=teams[side]
        records.append({'gameid':str(row.gameid),'series_id':series_id,
             'series_provenance':'reconstructed_team_pair_game_number_contiguous_not_official_id',
             'date':pd.to_datetime(row.date,utc=True).isoformat(),'league':str(row.league).upper(),
             'patch':patch_code(row.patch),'game_number':int(row.game),'turn':turn,
             'actor_side':side,'actor_team':row.teamname,'opponent_team':teams[enemy].teamname,
             'first_pick_side':first,'action':action,'slot':('F' if side==first else 'S')+f'_{action}{number}',
             'own_picks':list(picks[side]),'enemy_picks':list(picks[enemy]),
             'own_bans':list(bans[side]),'enemy_bans':list(bans[enemy]),
             'used_champions':list(used),'unavailable':sorted(unavailable),'target_champion':champion})
        (picks if action=='pick' else bans)[side].append(champion)
    return records,list(used)+sum(picks.values(),[])


def build_states(matches=None,region='WLDS'):
    if matches is None:_,matches,_=load_clean_tables()
    region=region.upper()
    m=matches[matches.league.str.upper().eq(region)].copy()
    games=[];rejected=[]
    for game,g in m.groupby('gameid',sort=False):
        try:
            numbers=pd.to_numeric(g.game,errors='raise')
            if len(g)!=2 or numbers.nunique()!=1 or not float(numbers.iloc[0]).is_integer():raise ValueError('game_number_or_team_rows')
            number=int(numbers.iloc[0])
            if number not in range(1,6):raise ValueError('unsupported_game_number')
            date=pd.to_datetime(g.date,utc=True).min()
            key=(str(g.league.iloc[0]).upper(),str(g.year.iloc[0]),str(g.split.iloc[0]),tuple(sorted(g.teamname)))
            games.append((date,str(game),number,key,g))
        except (ValueError,TypeError) as exc:rejected.append({'gameid':str(game),'reason':str(exc)})
    # Group only known prefixes beginning at game 1. Reset on gaps/long intervals.
    active={};series=defaultdict(list)
    for date,game,number,key,g in sorted(games,key=lambda x:(x[0],x[1])):
        previous=active.get(key)
        if number==1:
            sid=f'{region}:{game}';active[key]=(number,date,sid)
        elif previous and previous[0]+1==number and pd.Timedelta(0)<=date-previous[1]<=pd.Timedelta(hours=24):
            sid=previous[2];active[key]=(number,date,sid)
        else:
            active.pop(key,None);rejected.append({'gameid':game,'reason':'incomplete_or_ambiguous_series_prefix'});continue
        series[sid].append(g)
    records=[];accepted_series=0
    for sid,groups in series.items():
        temporary=[];used=[]
        try:
            for g in groups:
                states,used=game_states(g,used,sid);temporary.extend(states)
        except ValueError as exc:
            rejected.extend({'gameid':str(g.gameid.iloc[0]),'reason':f'rejected_series:{exc}'} for g in groups)
            continue
        records.extend(temporary);accepted_series+=1
    records.sort(key=lambda s:(s['date'],s['gameid'],s['turn']))
    payload='\n'.join(json.dumps(r,sort_keys=True,ensure_ascii=False) for r in records)
    manifest={'region':region,'games':len({r['gameid'] for r in records}),'series':accepted_series,
              'states':len(records),'rejected_games':rejected,'sha256':hashlib.sha256(payload.encode()).hexdigest(),
              'series_policy':'same league/year/split/unordered team pair, game1 then consecutive game numbers within24h; reject bad series',
              'limitations':['Series IDs are reconstructed, not verified official event IDs.',
                             'Observed roles/outcomes/future picks are excluded from features.',
                             'This builder assumes hard Fearless for the requested event; validate event rules before other regions.',
                             'Unknown prefixes, skipped bans and invalid Fearless series are excluded.']}
    return records,manifest


def export_states(region='WLDS'):
    records,manifest=build_states(region=region)
    path=ROOT/f'data/processed/{region.lower()}_draft_states.jsonl'
    path.write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in records),encoding='utf-8')
    (ROOT/f'reports/{region.lower()}_draft_states_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='rejected_games'},ensure_ascii=False,indent=2))
    print('Rejected games:',len(manifest['rejected_games']))
    return records,manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',default='WLDS')
    export_states(parser.parse_args().region)
