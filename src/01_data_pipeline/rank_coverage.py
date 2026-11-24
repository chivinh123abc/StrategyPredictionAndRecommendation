"""Deduplicated snapshot-cohort coverage and chronological readiness, no ranker/UI.

Private PUUIDs are used in memory for distinct counts only. Rejected candidates
define an observed-name audit universe, never add evidence to accepted counts.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

import pandas as pd

from ranked_matchups import ROOT, write_json, extract_match, METRICS
from rank_eligibility import read_policy, utc
from collect_rank_snapshots import classify_match

ROLE_MAP = {'TOP': 'top', 'JUNGLE': 'jng', 'MIDDLE': 'mid', 'BOTTOM': 'bot', 'UTILITY': 'sup'}
SCOPE = ['platform', 'queue', 'patch', 'tier_floor']


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def patch(version):
    m = re.match(r'^(\d+)\.(\d+)\.', str(version))
    if not m:
        raise ValueError('Missing raw major.minor patch')
    return f'{int(m[1])}.{int(m[2]):02d}'


def load_cohort(public_root, private_root, policy):
    accepted, universe, audit, source_hashes = {}, set(), [], {}
    defaults = policy['snapshot_collection']
    for summary_path in sorted(public_root.glob('*/summary.json')):
        summary = read_json(summary_path)
        if summary.get('schema') != 'ten-player-rank-snapshots-v1':
            continue
        run = summary['run_id']
        if (summary['tier_floor'] != policy['pro']['rank_tier_floor']
            or summary['max_match_age_hours'] != defaults['max_match_age_hours']
            or summary['max_snapshot_spread_minutes'] != defaults['max_snapshot_spread_minutes']):
            audit.append({'run_id': run, 'status': 'excluded_policy_mismatch'})
            continue
        private = private_root / run
        source_hashes[f'{run}/public_summary.json'] = hashlib.sha256(summary_path.read_bytes()).hexdigest()
        snapshots = read_json(private / 'rank_snapshots.json')
        by_person = {(r['platform'], r['puuid']): r for r in snapshots}
        source_hashes[f'{run}/rank_snapshots.json'] = hashlib.sha256((private / 'rank_snapshots.json').read_bytes()).hexdigest()
        for saved in read_json(summary_path.parent / 'matches.json'):
            mid = saved['match_id']
            path = private / f'{mid}.match.json'
            if not path.exists():
                continue
            detail = read_json(path)
            info = detail['info']
            actual = classify_match(detail, by_person, policy, utc(summary['finished_at']),
                summary['max_match_age_hours'], summary['max_snapshot_spread_minutes'])
            if actual['status'] != saved['status']:
                raise ValueError('Classification no longer matches saved cohort; do not silently ingest')
            scope = (actual['platform'], 420, patch(info['gameVersion']), summary['tier_floor'])
            for p in info['participants'] if info.get('queueId') == 420 and info.get('mapId') == 11 else []:
                if p.get('teamPosition') in ROLE_MAP and p.get('championId') is not None:
                    universe.add(scope + (ROLE_MAP[p['teamPosition']], int(p['championId']), p['championName']))
            source_hashes[f'{run}/{mid}.match.json'] = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual['status'] != 'accepted':
                continue
            provenance = private / f'{mid}.match.provenance.json'
            detail_known_at = read_json(provenance).get('fetched_at') if provenance.exists() else summary['finished_at']
            available_at = max([utc(p['observed_at']) for p in actual['participants']] + [utc(detail_known_at)]).isoformat()
            if provenance.exists():
                source_hashes[f'{run}/{mid}.match.provenance.json'] = hashlib.sha256(provenance.read_bytes()).hexdigest()
            timeline_path = private / f'{mid}.timeline.json'
            if timeline_path.exists():
                source_hashes[f'{run}/{mid}.timeline.json'] = hashlib.sha256(timeline_path.read_bytes()).hexdigest()
            candidate = {'run_id': run, 'scope': scope, 'detail': detail, 'snapshots': by_person,
                         'available_at': available_at, 'private': private}
            old = accepted.get(mid)
            if old and old['detail'] != detail:
                raise ValueError('Conflicting details for repeated accepted match ID')
            # First qualifying observation avoids counting one replayed match as new evidence.
            if old is None or available_at < old['available_at']:
                accepted[mid] = candidate
        audit.append({'run_id': run, 'status': summary['collection_status'],
                      'candidates': summary['candidate_games'], 'accepted_in_run': summary['accepted_games']})
    return accepted, universe, audit, source_hashes


def observations(accepted):
    rows, games = [], []
    for mid, item in sorted(accepted.items()):
        info = item['detail']['info']
        scope = dict(zip(SCOPE, item['scope']))
        measurements = {}
        path = item['private'] / f'{mid}.timeline.json'
        if path.exists():
            try:
                measurements = {(r['team_id'], r['role']): r for r in extract_match(item['detail'], read_json(path), 'nearest')}
            except (ValueError, KeyError, TypeError):
                measurements = {}
        started = pd.to_datetime(info['gameStartTimestamp'], unit='ms', utc=True)
        ended = max(info['gameStartTimestamp'] + info['gameDuration'] * 1000, info.get('gameEndTimestamp') or 0)
        games.append({**scope, 'match_id': mid, 'played_at': started.isoformat(),
                      'ended_at': pd.to_datetime(ended, unit='ms', utc=True).isoformat(),
                      'available_at': item['available_at'], 'selected_run_id': item['run_id']})
        for p in info['participants']:
            role = ROLE_MAP[p['teamPosition']]
            enemy = next(x for x in info['participants'] if x['teamId'] != p['teamId'] and x['teamPosition'] == p['teamPosition'])
            snap = item['snapshots'][(scope['platform'], p['puuid'])]
            row = {**scope, 'match_id': mid, 'played_at': started.isoformat(), 'available_at': item['available_at'],
                   'role': role, 'team_id': p['teamId'], 'champion_id': int(p['championId']), 'champion': p['championName'],
                   'opponent_id': int(enemy['championId']), 'opponent': enemy['championName'],
                   '_puuid': p['puuid'], '_enemy_puuid': enemy['puuid'], 'win': int(p['win']),
                   'tier_at_observation': snap['tier'], 'rank_observed_at': snap['observed_at'],
                   'historical_rank_verified': False}
            row.update({k: v for k, v in measurements.get((p['teamId'], role), {}).items()
                        if '_diff_' in k or k.startswith('frame_ms_')})
            for k in METRICS + ['frame_ms_10','frame_ms_15']:
                row.setdefault(k, None)
            rows.append(row)
    return pd.DataFrame(rows, columns=None if rows else SCOPE + ['match_id','role','champion_id','champion','_puuid','_enemy_puuid']), pd.DataFrame(games, columns=SCOPE + ['match_id','played_at','ended_at','available_at','selected_run_id'])


def coverage_tables(rows, universe, min_games=5, min_players=3):
    champions, lanes = [], []
    # ID is identity; display labels are provenance from Riot, not manually maintained aliases.
    targets = defaultdict(dict)
    for item in sorted(universe):
        scope, role, cid, name = item[:4], item[4], item[5], item[6]
        targets[(scope, role)][cid] = name
    for (scope, role), names in sorted(targets.items()):
        mask = rows.role.eq(role)
        for col, value in zip(SCOPE, scope):
            mask &= rows[col].eq(value)
        group = rows[mask]
        for cid, name in sorted(names.items()):
            sample = group[group.champion_id.eq(cid)]
            n, people = sample.match_id.nunique(), sample._puuid.nunique()
            champions.append({**dict(zip(SCOPE, scope)), 'role': role, 'champion_id': cid, 'champion': name,
                'games': n, 'unique_players': people, 'games_needed': max(0, min_games - n),
                'players_needed': max(0, min_players - people), 'supported': n >= min_games and people >= min_players})
            for oid, opponent in sorted(names.items()):
                if oid == cid:
                    continue
                pair = sample[sample.opponent_id.eq(oid)] if len(sample) else sample
                n, a, b = pair.match_id.nunique(), pair._puuid.nunique(), pair._enemy_puuid.nunique()
                lanes.append({**dict(zip(SCOPE, scope)), 'role': role, 'champion_id': cid, 'champion': name,
                    'opponent_id': oid, 'opponent': opponent, 'games': n, 'champion_players': a, 'opponent_players': b,
                    'unique_players': len(set(pair._puuid) | set(pair._enemy_puuid)),
                    'games_needed': max(0, min_games - n), 'champion_players_needed': max(0, min_players - a),
                    'opponent_players_needed': max(0, min_players - b),
                    'supported': n >= min_games and min(a, b) >= min_players})
    champion_columns = SCOPE + ['role','champion_id','champion','games','unique_players','games_needed','players_needed','supported']
    lane_columns = SCOPE + ['role','champion_id','champion','opponent_id','opponent','games','champion_players',
                           'opponent_players','unique_players','games_needed','champion_players_needed','opponent_players_needed','supported']
    return pd.DataFrame(champions, columns=champion_columns), pd.DataFrame(lanes, columns=lane_columns)


def chronological_plan(games, champions, min_games=5):
    partitions, blockers = {}, []
    if games.empty:
        return {'ready': False, 'blockers': ['no_accepted_games'], 'partitions': {}}
    # Time ties stay together. Never split a match or use a snapshot before it was available.
    times = sorted(games.played_at.unique())
    if len(times) < 3:
        blockers.append('fewer_than_three_distinct_game_start_times')
    a, b = int(len(times) * .6), int(len(times) * .8)
    buckets = {'history': times[:a], 'validation': times[a:b], 'test': times[b:]}
    ids = {}
    for name, values in buckets.items():
        part = games[games.played_at.isin(values)]
        ids[name] = sorted(part.match_id)
        partitions[name] = {'games': len(part), 'match_ids': ids[name]}
    for name, threshold in [('history', 5), ('validation', 2), ('test', 2)]:
        if partitions[name]['games'] < threshold:
            blockers.append(f'{name}_too_few_games_minimum_{threshold}')
    if buckets['validation']:
        cutoff = pd.to_datetime(min(buckets['validation']), utc=True)
        history = games[games.match_id.isin(ids['history'])]
        eligible = history[pd.to_datetime(history.available_at, utc=True).lt(cutoff)
                           & pd.to_datetime(history.ended_at, utc=True).lt(cutoff)]
        partitions['history']['available_before_validation_games'] = len(eligible)
        partitions['history']['available_before_validation_match_ids'] = sorted(eligible.match_id)
        if len(eligible) < 5:
            blockers.append('insufficient_history_with_snapshot_evidence_available_before_validation')
    for scope, group in champions.groupby(SCOPE) if len(champions) else []:
        for role in ROLE_MAP.values():
            if group[group.role.eq(role) & group.supported].champion_id.nunique() < 2:
                blockers.append(f'{"/".join(map(str,scope))}/{role}:fewer_than_two_supported_champions')
    return {'ready': not blockers, 'blockers': blockers, 'partitions': partitions,
        'criteria_kind': 'engineering_readiness_policy_not_statistical_power_analysis',
        'criteria': {'champion_games': min_games, 'champion_unique_players': 3,
                     'supported_champions_per_role': 2, 'history_games': 5, 'validation_games': 2, 'test_games': 2},
        'split_semantics': '60/20/20 distinct game-start times; history evidence AND result available before validation start',
        'rank_recommender_implemented': False, 'evaluation_status': 'not_run', 'metrics': None,
        'planned_baselines': ['same_role_popularity_from_frozen_history', 'same_role_historical_result_with_Wilson'],
        'limitation': 'Match-v5 has no full ranked pick-order log. Do not fabricate draft turns from participant order.'}


def build(args):
    policy = read_policy(args.policy)
    accepted, universe, runs, hashes = load_cohort(args.collection, args.private, policy)
    rows, games = observations(accepted)
    champions, lanes = coverage_tables(rows, universe)
    args.output.mkdir(parents=True, exist_ok=True)
    public_rows = rows.drop(columns=[c for c in rows if c.startswith('_')])
    public_rows.to_csv(args.output / 'observations.csv', index=False, encoding='utf-8-sig')
    games.to_csv(args.output / 'games.csv', index=False, encoding='utf-8-sig')
    champions.to_csv(args.output / 'champion_role_coverage.csv', index=False, encoding='utf-8-sig')
    lanes.to_csv(args.output / 'lane_matchup_coverage.csv', index=False, encoding='utf-8-sig')
    if len(rows):
        role_cov = rows.groupby(SCOPE + ['role']).agg(games=('match_id','nunique'), unique_players=('_puuid','nunique')).reset_index()
        patch_cov = rows.groupby(SCOPE).agg(games=('match_id','nunique'), unique_players=('_puuid','nunique')).reset_index()
    else:
        role_cov = pd.DataFrame(columns=SCOPE + ['role','games','unique_players'])
        patch_cov = pd.DataFrame(columns=SCOPE + ['games','unique_players'])
    if universe:
        role_keys = pd.DataFrame(sorted({x[:5] for x in universe}), columns=SCOPE + ['role'])
        patch_keys = pd.DataFrame(sorted({x[:4] for x in universe}), columns=SCOPE)
        role_cov = role_keys.merge(role_cov, on=SCOPE + ['role'], how='outer')
        patch_cov = patch_keys.merge(patch_cov, on=SCOPE, how='outer')
        for frame in (role_cov, patch_cov):
            frame[['games','unique_players']] = frame[['games','unique_players']].fillna(0).astype(int)
    role_cov.to_csv(args.output / 'role_coverage.csv', index=False, encoding='utf-8-sig')
    patch_cov.to_csv(args.output / 'patch_coverage.csv', index=False, encoding='utf-8-sig')
    target_games, target_champions = games, champions
    target_scope = None
    if len(games):
        latest = games.sort_values(['played_at','match_id']).iloc[-1]
        target_scope = {k: int(latest[k]) if k == 'queue' else str(latest[k]) for k in SCOPE}
        for k, v in target_scope.items():
            target_games = target_games[target_games[k].eq(v)]
            target_champions = target_champions[target_champions[k].eq(v)]
    readiness = chronological_plan(target_games, target_champions)
    readiness['target_scope'] = target_scope
    write_json(args.output / 'readiness.json', readiness)
    summary = {'schema': 'rank-snapshot-coverage-v1', 'runs': runs, 'accepted_unique_games': len(games),
        'participant_observations': len(rows), 'unique_players': int(rows._puuid.nunique()) if len(rows) else 0,
        'duplicate_accepted_games_removed': sum(r.get('accepted_in_run',0) for r in runs)-len(games),
        'observed_target_champion_roles': len(champions), 'supported_champion_roles': int(champions.supported.sum()) if len(champions) else 0,
        'observed_universe_directed_lane_pairs': len(lanes), 'supported_lane_pairs': int(lanes.supported.sum()) if len(lanes) else 0,
        'zero_evidence_champion_roles': int(champions.games.eq(0).sum()) if len(champions) else 0,
        'zero_evidence_lane_pairs': int(lanes.games.eq(0).sum()) if len(lanes) else 0,
        'readiness': readiness['ready'], 'historical_rank_verified': False, 'pro_rank_signal_enabled': False,
        'source_sha256': hashes,
        'universe_semantics': 'Champions observed at that role in fetched candidate matches; rejected candidates add names only, no sample counts. Not all valid game champions.'}
    write_json(args.output / 'summary.json', summary)
    lines = ['# Độ phủ dữ liệu Rank snapshot', '',
        f"Khử trùng: {len(games)} trận accepted / {len(rows)} dòng participant / {summary['unique_players']} người duy nhất.",
        f"Champion-role đủ n5 và3người: {summary['supported_champion_roles']}/{len(champions)}; kèo cùng đường đủ mẫu/độ đa dạng: {summary['supported_lane_pairs']}/{len(lanes)}.",
        'Counts chỉ lấy accepted; rejected/missing không được cộng bằng chứng. Một trận ở nhiều run chỉ giữ lần accepted sớm nhất. Server/queue/patch/floor giữ riêng.',
        'Các hàng0 là thiếu mẫu trong universe tướng/role đã thấy ở các trận ứng viên, không khẳng định toàn bộ tướng/role khả thi của game.', '',
        '| Server/patch | Role | Trận | Người | Tướng đủ mẫu | Số trận cao nhất của1tướng |',
        '|---|---|---:|---:|---:|---:|']
    for row in role_cov.to_dict('records'):
        group = champions[champions.role.eq(row['role'])]
        for col in SCOPE:
            group = group[group[col].eq(row[col])]
        lines.append(f"| {row['platform']}/{row['patch']} | {row['role']} | {row['games']} | {row['unique_players']} | {int(group.supported.sum())} | {int(group.games.max()) if len(group) else 0} |")
    lines += ['',
        '## Chưa đủ điều kiện triển khai/đánh giá recommender' if not readiness['ready'] else '## Cổng dữ liệu đạt điều kiện kỹ thuật tối thiểu', '']
    lines += [f'- {x}' for x in readiness['blockers']]
    lines += ['', 'Readiness là policy kỹ thuật tự thiết kế, không chứng minh đủ statistical power. Không hạ n5/3người hoặc bỏ cutoff để ép pass.',
        'Snapshot phải có trước thời điểm đánh giá, không chỉ ngày trận trước cutoff. Nhiều batch trong cùng ngày không tự thành kiểm chứng tương lai.',
        'Recommender Rank và phép đánh giá/baseline chưa được chạy trong bước này nếu chưa đủ điều kiện; không có metric giả. Runtime Giải không đổi.', '',
        'CSV: patch_coverage/role_coverage/champion_role_coverage/lane_matchup_coverage ghi số trận/người và số còn thiếu; games/observations là accepted dataset không PUUID.',
        'Rank hiện chỉ là cohort Master+ gần lúc quan sát, không exact rank lịch sử; không đo MMR, counter nhân quả hoặc tối ưu draft/BO5.']
    (args.output / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('source_sha256','runs')}, ensure_ascii=False))
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--collection', type=Path, default=ROOT / 'reports/rank_snapshot_collection')
    p.add_argument('--private', type=Path, default=ROOT / 'data/raw/riot_rank_snapshots')
    p.add_argument('--policy', type=Path, default=ROOT / 'src/config/draft_modes.json')
    p.add_argument('--output', type=Path, default=ROOT / 'reports/rank_coverage')
    build(p.parse_args())


if __name__ == '__main__':
    main()
