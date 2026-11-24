"""Collect ten-player Solo/Duo tier snapshots, not historical rank or MMR.

Private raw/evidence per run; public reports contain counts, match IDs and tiers
only. Acceptance requires all ten >= floor and declared recency/spread limits.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import pandas as pd

from ranked_matchups import RiotClient, RiotError, write_json, extract_match, COLUMNS, ROOT
from rank_eligibility import read_policy, assess_match, utc, TIERS


def now_utc():
    return datetime.now(timezone.utc)


def parse_snapshot(payload, puuid, platform, observed_at, source_ref):
    record = {'puuid': puuid, 'platform': platform.upper(), 'queue': 'RANKED_SOLO_5x5',
              'kind': 'snapshot', 'observed_at': observed_at, 'source_ref': source_ref,
              'tier': None, 'division': None, 'league_points': None}
    if not isinstance(payload, list) or any(not isinstance(x, dict) for x in payload):
        return {**record, 'status': 'invalid_response_shape'}
    entries = [x for x in payload if x.get('queueType') == record['queue']]
    if len(entries) != 1:
        return {**record, 'status': 'no_solo_rank_entry' if not entries else 'ambiguous_solo_rank_entry'}
    entry = entries[0]
    if entry.get('puuid') not in (None, puuid):
        return {**record, 'status': 'response_identity_mismatch'}
    if entry.get('tier') not in TIERS:
        return {**record, 'status': 'unrecognized_tier'}
    return {**record, 'status': 'ok', 'tier': entry['tier'], 'division': entry.get('rank'),
            'league_points': entry.get('leaguePoints')}


def classify_match(detail, snapshots, policy, checked_at, max_age_hours=24, max_spread_minutes=15):
    # Structural admission reused; historical evidence stays unknown for snapshots.
    base = assess_match(detail, [], policy, checked_at)
    info = detail.get('info', {})
    rows, reasons = [], []
    floor = TIERS.index(policy['pro']['rank_tier_floor'])
    high = low = missing = 0
    times = []
    platform = base['platform']
    for p in info.get('participants', []):
        snap = snapshots.get((platform, p.get('puuid')))
        reason = None
        if not snap or snap.get('status') != 'ok':
            reason = snap.get('status', 'not_fetched') if snap else 'not_fetched'
        elif (snap.get('platform') != platform or snap.get('queue') != 'RANKED_SOLO_5x5'
              or snap.get('puuid') != p.get('puuid') or snap.get('kind') != 'snapshot'
              or snap.get('tier') not in TIERS or not snap.get('source_ref')):
            reason = 'snapshot_scope_mismatch'
        else:
            try:
                observed = utc(snap['observed_at'])
                if observed > checked_at:
                    raise ValueError('future_observation')
                times.append(observed)
            except (KeyError, ValueError, TypeError):
                reason = 'invalid_snapshot_time'
        if reason:
            missing += 1
            reasons.append(reason)
        elif TIERS.index(snap['tier']) >= floor:
            high += 1
        else:
            low += 1
        rows.append({'team_id': p.get('teamId'), 'participant_id': p.get('participantId'),
                     'role': p.get('teamPosition'), 'tier': snap.get('tier') if snap else None,
                     'observed_at': snap.get('observed_at') if snap else None,
                     'status': reason or 'ok'})
    age = spread = None
    try:
        ended = max(info['gameStartTimestamp'] / 1000 + info['gameDuration'],
                    (info.get('gameEndTimestamp') or 0) / 1000)
        end = datetime.fromtimestamp(ended, timezone.utc)
        if times:
            age = (max(times) - end).total_seconds() / 3600
            spread = (max(times) - min(times)).total_seconds() / 60
            if min(times) < end:
                reasons.append('snapshot_precedes_match_end')
            if age > max_age_hours:
                reasons.append('match_too_old_for_near_match_proxy')
            if spread > max_spread_minutes:
                reasons.append('snapshot_spread_exceeded')
    except (ValueError, KeyError, TypeError, OSError, OverflowError):
        reasons.append('invalid_match_end_time')
    if low:
        reasons.append('participant_below_tier_floor')
    if missing or len(rows) != 10:
        reasons.append('not_all_ten_rank_snapshots_available')
    invalid = [x for x in base['reasons'] if x != 'not_all_ten_documented_high_at_match']
    reasons += invalid
    temporal = any(x in reasons for x in ('snapshot_precedes_match_end', 'match_too_old_for_near_match_proxy',
                                         'snapshot_spread_exceeded', 'invalid_match_end_time'))
    status = 'rejected' if invalid or low or temporal else 'missing' if missing or len(rows) != 10 else 'accepted'
    return {'match_id': base['match_id'], 'platform': platform, 'game_version': info.get('gameVersion'),
            'queue': 420, 'status': status, 'high_participants': high, 'below_floor_participants': low,
            'missing_participants': missing, 'all_ten_high_at_observation': high == 10 and not invalid,
            'snapshot_delay_hours': age, 'snapshot_spread_minutes': spread,
            'historical_rank_verified': False, 'reasons': sorted(set(reasons)), 'participants': rows}


def collect_run(args, client, clock=now_utc):
    policy = read_policy(args.policy)
    started = clock()
    run_id = started.strftime('%Y%m%dT%H%M%S%fZ')
    private = args.cache / run_id
    output = args.output / run_id
    private.mkdir(parents=True, exist_ok=False)
    output.mkdir(parents=True, exist_ok=False)
    ids = list(dict.fromkeys(args.match_id or []))
    snapshots, details, timelines = {}, {}, {}
    requests = Counter()
    issues, seed_counts = [], []
    seed_selection = []
    excluded_ids = set(getattr(args, 'exclude_match_ids', set()))
    ids = [mid for mid in ids if mid not in excluded_ids]
    seed_offset = getattr(args, 'seed_offset', 0)
    registry = getattr(args, 'seed_registry', set())
    stopped = False

    def get(host, path, kind, params=None):
        requests[kind] += 1
        return client.get(host, path, params)

    def handle_error(exc, stage):
        nonlocal stopped
        # Never persist arbitrary exception/request text or PUUIDs in public logs.
        issues.append({'stage': stage, 'http_status': exc.status_code, 'error': exc.reason_code})
        if exc.status_code != 404:
            stopped = True

    try:
        if not ids and not args.match_id:
            league = get(args.platform, '/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5', 'seed_league')
            for index, entry in enumerate(league.get('entries', [])[seed_offset:seed_offset + args.seed_players], seed_offset + 1):
                if not entry.get('puuid'):
                    continue
                if entry['puuid'] in registry:
                    continue
                registry.add(entry['puuid'])
                seed_selection.append({'seed_index': index, 'puuid': entry['puuid'], 'tier_at_selection': 'CHALLENGER'})
                batch = get(args.routing, f'/lol/match/v5/matches/by-puuid/{entry["puuid"]}/ids', 'match_list',
                    {'queue': 420, 'type': 'ranked', 'start': 0, 'count': args.matches_per_seed})
                seed_counts.append({'seed_index': index, 'returned_ids': len(batch)})
                ids = list(dict.fromkeys(ids + [mid for mid in batch if mid not in excluded_ids]))
                if len(ids) >= args.limit:
                    break
    except RiotError as exc:
        handle_error(exc, 'discovery')
    ids = ids[:args.limit]
    for index, mid in enumerate(ids, 1):
        if not re.fullmatch(r'[A-Z0-9]+_\d+', mid) or mid.split('_')[0].lower() != args.platform:
            raise ValueError('Match ID is invalid or belongs to another platform')
        if stopped:
            break
        try:
            detail = get(args.routing, f'/lol/match/v5/matches/{mid}', 'match_detail')
            if detail.get('metadata', {}).get('matchId') != mid:
                issues.append({'stage': 'match_detail', 'error': 'response_match_id_mismatch'})
                continue
            details[mid] = detail
            write_json(private / f'{mid}.match.json', detail)
            write_json(private / f'{mid}.match.provenance.json', {'fetched_at': clock().isoformat(), 'routing': args.routing})
        except RiotError as exc:
            handle_error(exc, 'match_detail')
            continue
        for p in detail.get('info', {}).get('participants', []):
            puuid = p.get('puuid')
            key = (args.platform.upper(), puuid)
            if not puuid or key in snapshots or stopped:
                continue
            slug = hashlib.sha256(puuid.encode()).hexdigest()
            source = f'riot_rank_snapshots/{run_id}/snapshots/{slug}.json'
            try:
                payload = get(args.platform, f'/lol/league/v4/entries/by-puuid/{puuid}', 'participant_rank')
                observed = clock().isoformat()
                write_json(private / 'snapshots' / f'{slug}.json',
                           {'observed_at': observed, 'platform': args.platform.upper(), 'response': payload})
                snapshots[key] = parse_snapshot(payload, puuid, args.platform, observed, source)
            except RiotError as exc:
                snapshots[key] = {'puuid': puuid, 'platform': args.platform.upper(), 'queue': 'RANKED_SOLO_5x5',
                    'kind': 'snapshot', 'observed_at': clock().isoformat(), 'source_ref': source,
                    'tier': None, 'status': 'api_error', 'http_status': exc.status_code}
                handle_error(exc, 'participant_rank')
            # Persist progress, including partial auth/rate/network failures.
            write_json(private / 'rank_snapshots.json', list(snapshots.values()))
        if not stopped:
            try:
                timeline = get(args.routing, f'/lol/match/v5/matches/{mid}/timeline', 'timeline')
                if timeline.get('metadata', {}).get('matchId') == mid:
                    timelines[mid] = timeline
                    write_json(private / f'{mid}.timeline.json', timeline)
            except RiotError as exc:
                handle_error(exc, 'timeline')
        print(f'Checked candidate {index}/{len(ids)}; unique participant snapshots {len(snapshots)}', flush=True)
    finished = clock()
    matches, observations = [], []
    for mid in ids:
        if mid not in details:
            matches.append({'match_id': mid, 'status': 'missing', 'reasons': ['match_detail_unavailable'],
                            'high_participants': 0, 'below_floor_participants': 0, 'missing_participants': 10,
                            'all_ten_high_at_observation': False, 'historical_rank_verified': False, 'participants': []})
            continue
        row = classify_match(details[mid], snapshots, policy, finished, args.max_match_age_hours, args.max_snapshot_spread_minutes)
        if mid not in timelines:
            row['reasons'].append('timeline_unavailable')
        matches.append(row)
        if row['status'] == 'accepted' and mid in timelines:
            try:
                data = extract_match(details[mid], timelines[mid], 'nearest')
                for r in data:
                    participant = next(p for p in details[mid]['info']['participants']
                        if p['teamId'] == r['team_id'] and p['teamPosition'] in ('TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY')
                        and {'TOP':'top','JUNGLE':'jng','MIDDLE':'mid','BOTTOM':'bot','UTILITY':'sup'}[p['teamPosition']] == r['role'])
                    snap = snapshots[(args.platform.upper(), participant['puuid'])]
                    r.update(tier_at_observation=snap['tier'], rank_observed_at=snap['observed_at'],
                             cohort='all_ten_high_snapshot_near_match_proxy', historical_rank_verified=False)
                observations.extend(data)
            except (ValueError, KeyError, TypeError):
                row['reasons'].append('timeline_extraction_failed')
    counts = Counter(r['status'] for r in matches)
    summary = {'schema': 'ten-player-rank-snapshots-v1', 'run_id': run_id,
        'started_at': started.isoformat(), 'finished_at': finished.isoformat(),
        'collection_status': 'api_stopped' if stopped else 'complete',
        'platform': args.platform.upper(), 'routing': args.routing, 'queue': 'RANKED_SOLO_5x5',
        'tier_floor': policy['pro']['rank_tier_floor'], 'max_match_age_hours': args.max_match_age_hours,
        'max_snapshot_spread_minutes': args.max_snapshot_spread_minutes,
        'seed_counts': seed_counts, 'candidate_games': len(matches),
        'seed_offset': seed_offset, 'excluded_seen_match_ids_count': len(excluded_ids),
        'accepted_games': counts['accepted'], 'rejected_games': counts['rejected'], 'missing_games': counts['missing'],
        'all_ten_high_at_observation_games': sum(r['all_ten_high_at_observation'] for r in matches),
        'games_with_missing_participants': sum(r['missing_participants'] > 0 for r in matches),
        'unique_participants_checked': len(snapshots), 'snapshot_status_counts': dict(Counter(s['status'] for s in snapshots.values())),
        'request_calls': dict(requests), 'issues': issues, 'accepted_observations': len(observations),
        'reason_counts': dict(Counter(x for r in matches for x in set(r['reasons']))),
        'historical_rank_verified': False, 'pro_rank_signal_enabled': False,
        'interpretation': 'All ten ranks observed serially during collection; near-match proxy, not rank at match time.',
        'private_manifest_sha256': hashlib.sha256(json.dumps(list(snapshots.values()), sort_keys=True).encode()).hexdigest()}
    write_json(private / 'rank_snapshots.json', list(snapshots.values()))
    write_json(private / 'seed_selection.json', seed_selection)
    write_json(private / 'manifest.json', summary)
    write_json(output / 'summary.json', summary)
    write_json(output / 'matches.json', matches)
    write_json(output / 'accepted_match_ids.json', [r['match_id'] for r in matches if r['status'] == 'accepted'])
    columns = COLUMNS + ['tier_at_observation', 'rank_observed_at', 'cohort', 'historical_rank_verified']
    pd.DataFrame(observations, columns=columns).to_csv(output / 'accepted_observations.csv', index=False, encoding='utf-8-sig')
    lines = ['# Thu thập snapshot rank đủ10người', '',
        f"Server {summary['platform']}, Solo/Duo; ngưỡng {summary['tier_floor']}+ tại lúc kiểm tra.",
        f"Tổng {len(matches)} trận: nhận {counts['accepted']}, loại {counts['rejected']}, thiếu {counts['missing']}.",
        f"Đã kiểm {len(snapshots)} participant duy nhất; đủ10người đạt ngưỡng tại snapshot: {summary['all_ten_high_at_observation_games']} trận.",
        f"Trạng thái collection: {summary['collection_status']}. Xem summary.json/guard issues nếu API dừng.", '',
        f'Chỉ nhận nhóm gần trận nếu snapshot sau kết thúc trận tối đa{args.max_match_age_hours}giờ và10snapshot trải trong tối đa{args.max_snapshot_spread_minutes}phút. Đây là ngưỡng kỹ thuật tự thiết kế, chỉnh được, chưa tối ưu.',
        'Snapshot được chụp nối tiếp, không đồng thời; không xác nhận rank lịch sử lúc trận. Không tự chuyển thành historical_interval hoặc bật tín hiệu cho Giải.',
        'Không có Solo/Duo entry/lỗi API là thiếu thông tin, không suy thành tier thấp. Trận đã biết có người dưới ngưỡng được loại; có thể đồng thời còn thiếu participant khác.',
        'Chỉ cohort snapshot đủ điều kiện được xuất accepted_observations nếu có timeline; gold/XP/CS gần10/15phút chỉ mô tả. Match acceptance và coverage timeline là hai điều kiện riêng.', '',
        '| Match | Kết quả | Đạt tier | Dưới tier | Thiếu | Lý do |', '|---|---|---:|---:|---:|---|']
    lines += [f"| {r['match_id']} | {r['status']} | {r['high_participants']} | {r['below_floor_participants']} | {r['missing_participants']} | {', '.join(r['reasons']) or 'đủ điều kiện snapshot proxy'} |" for r in matches]
    (output / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    write_json(args.output / 'latest.json', {'run_id': run_id, 'report_dir': run_id})
    print(json.dumps({k: summary[k] for k in ('run_id', 'collection_status', 'candidate_games', 'accepted_games', 'rejected_games', 'missing_games', 'unique_participants_checked')}, ensure_ascii=False), flush=True)
    return summary, matches


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--platform', choices=['kr', 'vn2', 'tw2', 'na1', 'euw1'], default='kr')
    p.add_argument('--routing', choices=['asia', 'sea', 'americas', 'europe'])
    p.add_argument('--limit', type=int, default=5)
    p.add_argument('--seed-players', type=int, default=5)
    p.add_argument('--seed-offset', type=int, default=0)
    p.add_argument('--max-requests', type=int, default=300)
    p.add_argument('--matches-per-seed', type=int, default=1)
    p.add_argument('--match-id', action='append')
    p.add_argument('--max-match-age-hours', type=float)
    p.add_argument('--max-snapshot-spread-minutes', type=float)
    p.add_argument('--policy', type=Path, default=ROOT / 'src/config/draft_modes.json')
    p.add_argument('--cache', type=Path, default=ROOT / 'data/raw/riot_rank_snapshots')
    p.add_argument('--output', type=Path, default=ROOT / 'reports/rank_snapshot_collection')
    args = p.parse_args()
    defaults = read_policy(args.policy)['snapshot_collection']
    if args.max_match_age_hours is None:
        args.max_match_age_hours = defaults['max_match_age_hours']
    if args.max_snapshot_spread_minutes is None:
        args.max_snapshot_spread_minutes = defaults['max_snapshot_spread_minutes']
    if not (1 <= args.limit <= 20 and 1 <= args.seed_players <= 20 and 1 <= args.matches_per_seed <= 20
            and 0 <= args.seed_offset <= 299 and 1 <= args.max_requests <= 1000):
        p.error('limit/seed-players/matches-per-seed must be1..20')
    if not (0 < args.max_match_age_hours <= 168 and 0 < args.max_snapshot_spread_minutes <= 60):
        p.error('Age must be0..168h; snapshot spread0..60min')
    from config.settings import RIOT_API_KEY, SERVER_METADATA
    args.routing = args.routing or SERVER_METADATA[args.platform]['region']
    try:
        summary, _ = collect_run(args, RiotClient(RIOT_API_KEY, min_interval=1.3, max_requests=args.max_requests))
        return 2 if summary['collection_status'] == 'api_stopped' else 0
    except (ValueError, RiotError) as exc:
        p.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
