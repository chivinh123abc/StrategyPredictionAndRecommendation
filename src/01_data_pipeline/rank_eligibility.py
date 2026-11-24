"""Audit ranked cohort provenance; no assumption that missing tier means low tier.

Historical intervals are supplied evidence, structurally checked, not independently
authenticated by this tool. Current League-v4 snapshots cannot fill historical rank.
This is an admission audit, not a ranked draft recommender or a live advisor change.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIERS = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD',
         'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
POSITIONS = {'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY'}


def utc(value):
    result = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timestamp_must_include_timezone')
    return result.astimezone(timezone.utc)


def read_policy(path):
    policy = json.loads(Path(path).read_text(encoding='utf-8'))
    pro = policy['pro']
    if pro['rank_tier_floor'] not in TIERS:
        raise ValueError('invalid_tier_floor')
    if pro['rank_queue'] != 'RANKED_SOLO_5x5':
        raise ValueError('This policy audits Solo/Duo only; Flex needs its own contract')
    if not all(pro[k] is True for k in ('all_ten_participants_required', 'require_documented_rank_at_match')):
        raise ValueError('This audit requires the strict historical all-ten policy')
    if pro['rank_signal_enabled'] or pro['current_snapshot_is_historical_rank'] or pro['challenger_seed_is_all_participants_high']:
        raise ValueError('Unsafe cohort assumptions or runtime activation in admission policy')
    return policy


def participant_evidence(puuid, platform, started, records, policy, knowledge_cutoff):
    floor = TIERS.index(policy['pro']['rank_tier_floor'])
    historical, snapshots = [], []
    invalid = 0
    for record in records:
        if record.get('puuid') != puuid:
            continue
        if str(record.get('platform', '')).upper() != platform.upper() or record.get('queue') != policy['pro']['rank_queue']:
            continue
        try:
            tier = record['tier']
            observed = utc(record['observed_at'])
            if tier not in TIERS or not str(record.get('source_ref', '')).strip():
                raise ValueError('missing_tier_or_source')
            if observed > knowledge_cutoff:
                continue
            if record.get('kind') == 'snapshot':
                snapshots.append((observed, tier))
            elif record.get('kind') == 'historical_interval':
                a, b = utc(record['valid_from']), utc(record['valid_until'])
                if a >= b:
                    raise ValueError('invalid_interval')
                if a <= started < b:
                    historical.append(tier)
            else:
                raise ValueError('unknown_evidence_kind')
        except (ValueError, TypeError, KeyError):
            invalid += 1
    if len(set(historical)) > 1:
        return {'historical': 'conflicting_evidence', 'snapshot': 'unknown', 'invalid_records': invalid}
    hist = ('documented_high' if TIERS.index(historical[0]) >= floor else 'documented_below_floor') if historical else 'unknown'
    snapshot = 'unknown'
    if snapshots:
        last = max(t for t, _ in snapshots)
        tiers = {tier for t, tier in snapshots if t == last}
        snapshot = ('high_at_observation' if TIERS.index(next(iter(tiers))) >= floor else 'below_floor_at_observation') if len(tiers) == 1 else 'conflicting_evidence'
    return {'historical': hist, 'snapshot': snapshot, 'invalid_records': invalid}


def assess_match(detail, records, policy, knowledge_cutoff, seed_selected=False):
    info = detail.get('info', {})
    mid = detail.get('metadata', {}).get('matchId', '')
    platform = mid.split('_')[0]
    players = info.get('participants', [])
    reasons = []
    if info.get('queueId') != 420 or info.get('mapId') != 11:
        reasons.append('not_solo_ranked_summoners_rift')
    if len(players) != 10 or len({p.get('puuid') for p in players if p.get('puuid')}) != 10:
        reasons.append('missing_or_duplicate_participant_identity')
    if (len({p.get('participantId') for p in players}) != 10
            or any(p.get('participantId') not in range(1, 11) or p.get('teamId') not in (100, 200) for p in players)):
        reasons.append('invalid_participant_or_team_ids')
    for team in (100, 200):
        team_players = [p for p in players if p.get('teamId') == team]
        if len(team_players) != 5 or {p.get('teamPosition') for p in team_players} != POSITIONS:
            reasons.append('ambiguous_role_assignment')
    try:
        started = datetime.fromtimestamp(info['gameStartTimestamp'] / 1000, timezone.utc)
    except (KeyError, ValueError, TypeError, OSError, OverflowError):
        started = None
        reasons.append('missing_start_time')
    if info.get('gameDuration', 0) < 600:
        reasons.append('short_match')
    evaluations = [participant_evidence(p.get('puuid'), platform, started, records, policy, knowledge_cutoff)
                   for p in players] if started else []
    hist = Counter(e['historical'] for e in evaluations)
    snapshot = Counter(e['snapshot'] for e in evaluations)
    eligible = not reasons and hist['documented_high'] == 10
    status = ('documented_high_all_ten' if eligible else 'rank_evidence_conflict' if hist['conflicting_evidence']
              else 'known_below_floor_present' if hist['documented_below_floor']
              else 'all_ten_high_at_observation_only' if snapshot['high_at_observation'] == 10
              else 'challenger_seed_only' if seed_selected else 'historical_rank_unknown')
    if not eligible:
        reasons.append('not_all_ten_documented_high_at_match')
    return {'match_id': mid, 'platform': platform, 'rank_cohort_status': status,
            'rank_mode_data_admissible': not any(x != 'not_all_ten_documented_high_at_match' for x in reasons),
            'pro_high_rank_data_admissible': eligible, 'historical_participant_counts': dict(hist),
            'snapshot_participant_counts': dict(snapshot), 'seed_selection_confirmed': seed_selected,
            'invalid_evidence_records': sum(e['invalid_records'] for e in evaluations),
            'reasons': sorted(set(reasons))}


def audit(cache, policy_path, output, evidence_path=None, cutoff=None):
    policy = read_policy(policy_path)
    records = json.loads(evidence_path.read_text(encoding='utf-8')) if evidence_path else []
    if not isinstance(records, list):
        raise ValueError('Evidence input must be a list of records')
    knowledge_cutoff = utc(cutoff) if cutoff else datetime.now(timezone.utc)
    manifest_path = cache / 'collection_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    seed_ids = set(manifest.get('matches', [])) if manifest.get('seed_method') == 'challenger_list_at_fetch' else set()
    rows = []
    hashes = {}
    seen = set()
    for path in sorted(cache.glob('*.match.json')):
        detail = json.loads(path.read_text(encoding='utf-8'))
        mid = detail.get('metadata', {}).get('matchId')
        if mid in seen:
            raise ValueError('Duplicate payload match ID in audit input')
        seen.add(mid)
        rows.append(assess_match(detail, records, policy, knowledge_cutoff, mid in seed_ids))
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary = {'policy_version': policy['version'], 'tier_floor': policy['pro']['rank_tier_floor'],
               'tier_floor_status': policy['pro']['rank_tier_floor_status'],
               'knowledge_cutoff': knowledge_cutoff.isoformat(), 'games': len(rows),
               'cohort_status_counts': dict(Counter(r['rank_cohort_status'] for r in rows)),
               'rank_mode_data_admissible_games': sum(r['rank_mode_data_admissible'] for r in rows),
               'pro_high_rank_data_admissible_games': sum(r['pro_high_rank_data_admissible'] for r in rows),
               'rank_mode_runtime': policy['rank']['runtime_status'], 'pro_rank_signal_enabled': False,
               'note': 'Unknown historical tier is not low rank. Supplied historical intervals are not independently authenticated.',
               'raw_sha256': hashes, 'policy_sha256': hashlib.sha256(policy_path.read_bytes()).hexdigest()}
    output.mkdir(parents=True, exist_ok=True)
    for name, obj in [('summary.json', summary), ('matches.json', rows)]:
        (output / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Kiểm tra nguồn Rank cao cho hai chế độ', '',
             f"Ngưỡng làm việc: {summary['tier_floor']}+ (cấu hình được, chưa tối ưu). Tổng: {len(rows)} trận.",
             f"Dữ liệu có thể tiếp nhận cho Rank: {summary['rank_mode_data_admissible_games']} trận; đủ điều kiện Rank cao lịch sử cho Giải: {summary['pro_high_rank_data_admissible_games']} trận.", '',
             'Không biết rank lịch sử không đồng nghĩa rank thấp. Seed Thách Đấu chỉ xác nhận cách chọn mẫu tại lúc fetch, không xác nhận cả10người lúc trận diễn ra.',
             'Snapshot hiện tại không được đổi thành lịch sử. Interval lịch sử cần nguồn/chứng cứ bên ngoài; công cụ chỉ kiểm hợp đồng dữ liệu, không xác thực độc lập tài liệu đó.',
             'Đây là audit dữ liệu và thiết kế chế độ: runtime Rank chưa triển khai; runtime Giải vẫn legacy/contextual dùng Pro, chưa bật tín hiệu Rank.', '',
             '| Nhãn | Số trận |', '|---|---:|']
    lines += [f'| {status} | {count} |' for status, count in summary['cohort_status_counts'].items()]
    (output / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('raw_sha256',)}, ensure_ascii=False))
    return summary, rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, default=ROOT / 'data/raw/riot_matchups_study')
    p.add_argument('--policy', type=Path, default=ROOT / 'src/config/draft_modes.json')
    p.add_argument('--output', type=Path, default=ROOT / 'reports/rank_cohort_audit')
    p.add_argument('--evidence', type=Path, help='Private rank evidence records, not player names.')
    p.add_argument('--knowledge-cutoff', help='Timezone-aware cutoff for available rank evidence.')
    a = p.parse_args()
    audit(a.cache, a.policy, a.output, a.evidence, a.knowledge_cutoff)


if __name__ == '__main__':
    main()
