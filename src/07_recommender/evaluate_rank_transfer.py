"""Exploratory chronological Rank/Pro matchup ablation; never enables live scoring.

Only the matchup component differs. Pick retrieval is not tactical optimality.
Existing Worlds data has been used in prior project audits: not a fresh final test.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'src/01_data_pipeline')]
from analysis_data import load_clean_tables, DB_PATH
from rank_data_contract import ChampionCatalog, normalize_observations
from ranked_matchups import load_rank, write_json, METRICS
from historical_recommender import HistoricalRecommender, evidence
from draft_advisor import DraftAdvisor
from draft_meta import MetaPolicy
from draft_states import build_states
from evaluate_draft_policy import assign_observed


def normalize_tables(matches, players, catalog):
    matches, players = matches.copy(), players.copy()
    audit = []
    for frame, cols in [(players, ['champion']),
                         (matches, [f'{a}{i}' for a in ('pick', 'ban') for i in range(1, 6)])]:
        for col in cols:
            mapping = {}
            for value in frame[col].dropna().unique():
                if str(value).lower() in ('', 'none', 'noban', 'null'):
                    mapping[value] = value
                    continue
                mapping[value] = catalog.name(value)
                audit.append({'column': col, 'raw': value, 'canonical': mapping[value]})
            frame[col] = frame[col].map(mapping)
    return matches, players, audit


def split_series(states, patch):
    picks = [s for s in states if s['action'] == 'pick' and s['patch'] == patch]
    groups = {}
    for s in picks:
        groups.setdefault(s['series_id'], []).append(s)
    ordered = sorted(groups, key=lambda k: min(x['date'] for x in groups[k]))
    if len(ordered) < 10:
        raise ValueError('Need >=10 complete reconstructed series for chronological partitions')
    a, b = int(len(ordered) * .6), int(len(ordered) * .8)
    partitions = {'history': ordered[:a], 'validation': ordered[a:b], 'test': ordered[b:]}
    result = {name: sorted([s for sid in ids for s in groups[sid]],
                           key=lambda s: (s['date'], s['gameid'], s['turn']))
              for name, ids in partitions.items()}
    for earlier, later in [('history', 'validation'), ('validation', 'test')]:
        if max(s['date'] for s in result[earlier]) >= min(s['date'] for s in result[later]):
            raise ValueError('Overlapping series dates across chronological partitions')
    return result, partitions


class RankEvidence:
    def __init__(self, rows, cutoff, patch, platform='KR', days=60):
        dates = pd.to_datetime(rows.played_at, utc=True, errors='coerce')
        ends = pd.to_datetime(rows.ended_at, utc=True, errors='coerce')
        cut = pd.to_datetime(cutoff, utc=True)
        mask = dates.le(cut) & dates.ge(cut - pd.Timedelta(days=days))
        mask &= ends.notna() & ends.le(cut)
        mask &= rows.patch.eq(patch) & rows.platform.str.upper().eq(platform.upper())
        self.rows = rows[mask].drop_duplicates(['match_id', 'team_id', 'role']).copy()
        self.excluded_future_rows = int((dates.gt(cut) | ends.gt(cut)).sum())
        self.counts, self.wins = Counter(), Counter()
        for _, game in self.rows.groupby('match_id'):
            if len(game) != 10 or game.groupby('team_id').role.nunique().tolist() != [5, 5]:
                raise ValueError('RankEvidence requires complete ten-row matches')
            for a in game.itertuples():
                for b in game.itertuples():
                    if a.team_id == b.team_id:
                        continue
                    key = (a.role, a.champion, b.role, b.champion)
                    self.counts[key] += 1
                    self.wins[key] += int(a.win)

    def evaluate(self, role, champ, masses, baseline, enemy_count, min_games, prior):
        residual, covered, rows = 0., 0., []
        for enemy_role, choices in masses.items():
            for opponent, prob in choices.items():
                key = (role, champ, enemy_role, opponent)
                n, wins = self.counts[key], self.wins[key]
                ev = {**evidence(wins, n), 'enemy_role': enemy_role, 'opponent': opponent,
                      'role_probability': prob, 'domain': 'rank',
                      'status': 'observed_context' if n >= min_games else 'insufficient_context'}
                rows.append(ev)
                if n >= min_games:
                    # Same Pro baseline/threshold/prior as control: change only source of matchup counts.
                    residual += prob * (wins / n - baseline) * n / (n + prior)
                    covered += prob
        return float(np.clip(.5 + residual / max(1, enemy_count), 0, 1)), rows, covered / max(1, enemy_count)


class TransferAdvisor(DraftAdvisor):
    def __init__(self, *args, rank_evidence, **kwargs):
        super().__init__(*args, **kwargs)
        self.rank_evidence = rank_evidence
        self.mode = 'pro_only'
        self.rank_coverage = {}

    def evaluate_enemy_context(self, role, champ, role_masses, snapshot, baseline, enemy_count):
        pro = super().evaluate_enemy_context(role, champ, role_masses, snapshot, baseline, enemy_count)
        rank = self.rank_evidence.evaluate(role, champ, role_masses, baseline, enemy_count,
                                           self.policy.min_games, self.meta_policy.prior_games)
        self.rank_coverage[(role, champ)] = rank[2]
        if self.mode == 'pro_only':
            return pro
        if self.mode == 'rank_only':
            return rank
        if self.mode == 'hybrid':
            # Mix only supported Rank pairs; otherwise preserve the Pro control.
            # This avoids attributing shrinkage toward .5 to non-existent Rank data.
            lookup = {(e['enemy_role'], e['opponent']): e for e in pro[1]}
            correction, coverage = 0., 0.
            for ev in rank[1]:
                prev = lookup.get((ev['enemy_role'], ev['opponent']))
                n = ev['games']
                pn = prev['games'] if prev else 0
                if max(n, pn) >= self.policy.min_games:
                    coverage += ev['role_probability']
                if n < self.policy.min_games:
                    continue
                rr = (ev['winrate'] - baseline) * n / (n + self.meta_policy.prior_games)
                pr = (prev['winrate'] - baseline) * pn / (pn + self.meta_policy.prior_games) if pn >= self.policy.min_games else 0
                correction += .5 * ev['role_probability'] * (rr - pr)
            score = float(np.clip(pro[0] + correction / max(1, enemy_count), 0, 1))
            return score, pro[1] + rank[1], coverage / max(1, enemy_count)
        raise ValueError('unknown_transfer_mode')


def metrics(rows):
    if not rows:
        return {'queries': 0, 'recall_at_1': None, 'recall_at_5': None, 'mrr_at_5': None}
    return {'queries': len(rows), 'recall_at_1': float(np.mean([r['rank'] == 1 for r in rows])),
            'recall_at_5': float(np.mean([r['rank'] is not None and r['rank'] <= 5 for r in rows])),
            'mrr_at_5': float(np.mean([1 / r['rank'] if r['rank'] and r['rank'] <= 5 else 0 for r in rows])),
            'candidate_coverage': float(np.mean([r['rank'] is not None for r in rows])),
            'queries_with_supported_rank_candidate': sum(r['rank_supported_candidates'] > 0 for r in rows),
            'queries_with_revealed_enemy': sum(r['enemy_count'] > 0 for r in rows)}


def paired_interval(rows, mode, seed=42):
    control = [r for r in rows if r['mode'] == 'pro_only']
    variant = [r for r in rows if r['mode'] == mode]
    assert [(r['gameid'], r['turn']) for r in control] == [(r['gameid'], r['turn']) for r in variant]
    groups = {}
    for a, b in zip(control, variant):
        hit = lambda r: int(r['rank'] is not None and r['rank'] <= 5)
        groups.setdefault(a['series_id'], []).append(hit(b) - hit(a))
    if not groups:
        return {'series': 0, 'delta': None, 'ci95': None}
    values = list(groups.values())
    rng = np.random.default_rng(seed)
    samples = [float(np.mean([x for i in rng.integers(len(values), size=len(values)) for x in values[i]])) for _ in range(1000)]
    return {'series': len(values), 'delta': float(np.mean([x for xs in values for x in xs])),
            'ci95': np.quantile(samples, [.025, .975]).tolist(),
            'kind': 'paired_reconstructed_series_bootstrap_1000_seed42'}


def replay(states, advisor, region):
    rows = []
    snapshot, _, _ = advisor.context(region)
    for index, state in enumerate(states):
        if index % 50 == 0:
            print(f'  replay {index}/{len(states)}', flush=True)
        own = assign_observed(state['own_picks'], snapshot)
        enemy = assign_observed(state['enemy_picks'], snapshot)
        roster = snapshot.roster(state['actor_team'])
        roster = roster['players'] if roster else {}
        pools = {}
        for mode in ('pro_only', 'rank_only', 'hybrid'):
            advisor.mode = mode
            advisor.rank_coverage = {}
            candidates = {}
            for role in ('top', 'jng', 'mid', 'bot', 'sup'):
                if role in own:
                    continue
                picks = advisor.recommend_picks(role, own, enemy, state['unavailable'], roster.get(role),
                    top_k=10000, region=region, draft_slot=state['slot'].replace('_pick', ''))
                for p in picks:
                    champ = p['champion']
                    if champ not in candidates or p['score'] > candidates[champ]['score']:
                        candidates[champ] = p
            ordered = sorted(candidates, key=lambda c: (candidates[c]['evidence_status'] == 'sparse_candidate',
                             -candidates[c]['score'], -candidates[c]['games'], c))
            if set(ordered) & set(state['unavailable']):
                raise AssertionError('Illegal candidate in replay')
            pools[mode] = set(ordered)
            truth = state['target_champion']
            rank = ordered.index(truth) + 1 if truth in candidates else None
            supported = sum(any(advisor.rank_coverage.get((r, c), 0) > 0
                                for r in ('top', 'jng', 'mid', 'bot', 'sup')) for c in ordered)
            rows.append({'gameid': state['gameid'], 'series_id': state['series_id'], 'date': state['date'],
                         'turn': state['turn'], 'mode': mode, 'observed_pick': truth, 'rank': rank,
                         'top5': ordered[:5], 'enemy_count': len(state['enemy_picks']),
                         'rank_supported_candidates': supported})
        if not pools['pro_only'] == pools['rank_only'] == pools['hybrid']:
            raise AssertionError('Variant changed legal candidate pool')
    return rows


def audit_contract(rank, players, cache, catalog):
    raw_names, player_ids = {}, set()
    for path in sorted(cache.glob('*.match.json')):
        for p in json.loads(path.read_text(encoding='utf-8'))['info']['participants']:
            raw_names[(p['championName'], p['championId'])] = catalog.name(p['championName'], p['championId'])
            if p.get('puuid'):
                player_ids.add(p['puuid'])
    differences = {}
    for minute in (10, 15):
        for m, field in [('gold', 'gold'), ('xp', 'xp'), ('cs', 'cs')]:
            a = pd.to_numeric(players.get(f'{field}at{minute}'), errors='coerce')
            b = pd.to_numeric(players.get(f'opp_{field}at{minute}'), errors='coerce')
            stored = pd.to_numeric(players.get(f'{field}diffat{minute}'), errors='coerce')
            if stored is None:
                continue
            valid = a.notna() & b.notna() & stored.notna()
            differences[f'{m}_{minute}'] = {'available': int(valid.sum()),
                'mismatch': int(((a - b - stored).abs().gt(1e-6) & valid).sum())}
    total = pd.to_numeric(players.total_cs, errors='coerce')
    lane = pd.to_numeric(players.minionkills, errors='coerce')
    jungle = pd.to_numeric(players.monsterkills, errors='coerce')
    valid = total.notna() & lane.notna() & jungle.notna()
    return {'official_catalog_version': catalog.version,
            'rank_distinct_participants': len(player_ids),
            'rank_name_mapping': [{'raw': k[0], 'champion_id': k[1], 'canonical': v} for k, v in raw_names.items()],
            'pro_stored_diff_checks': differences,
            'pro_total_cs_check': {'available': int(valid.sum()), 'mismatch': int(((total - lane - jungle).abs().gt(1e-6) & valid).sum())},
            'rank_frame_offsets_ms': {str(m): sorted((rank[f'frame_ms_{m}'].dropna() - m * 60000).unique().tolist()) for m in (10, 15)},
            'cs_definition_source': 'https://lol.timsevenhuysen.com/matchdata/match-data-dictionary/',
            'role_semantics': 'postgame reported/inferred role, not observed lane occupancy or draft intent',
            'timestamp_semantics': 'UTC start; nearest +/-1000ms is descriptive only; Pro exact frame timestamps unavailable'}


def evaluate(args):
    catalog = ChampionCatalog.read(args.catalog)
    rank, rejected = load_rank(args.cache, 'nearest', catalog)
    _, matches, players = load_clean_tables()
    matches, players, names = normalize_tables(matches, players, catalog)
    states, state_manifest = build_states(matches, args.region)
    partitions, ids = split_series(states, args.patch)
    cutoff = (pd.to_datetime(partitions['validation'][0]['date'], utc=True) - pd.Timedelta(nanoseconds=1)).isoformat()
    cohort_status = 'seed_selected_unverified_research'
    if not args.allow_seed_only_research:
        from rank_eligibility import audit as audit_rank_cohort
        summary, cohort = audit_rank_cohort(args.cache, args.cohort_policy,
            args.output / 'cohort_audit', args.rank_evidence, cutoff)
        allowed = {r['match_id'] for r in cohort if r['pro_high_rank_data_admissible']}
        if not allowed:
            raise ValueError('Không có trận đủ bằng chứng Rank cao lịch sử. Xem cohort_audit; chỉ tái lập nghiên cứu seed-only cũ bằng --allow-seed-only-research.')
        rank = rank[rank.match_id.isin(allowed)].copy()
        cohort_status = 'all_ten_historical_high_documented_not_independently_authenticated'
    rank_ev = RankEvidence(rank, cutoff, args.patch, args.platform)
    # No training result from a match that started before but ended after freeze.
    ends = pd.to_datetime(matches.date, utc=True) + pd.to_timedelta(matches.gamelength, unit='s')
    past_matches = matches[ends.le(pd.to_datetime(cutoff, utc=True))].copy()
    past_players = players[players.gameid.isin(past_matches.gameid)].copy()
    history = HistoricalRecommender.from_frames(past_matches, past_players)
    advisor = TransferAdvisor(historical=history, meta_policy=MetaPolicy(as_of=cutoff, patch=args.patch), rank_evidence=rank_ev)
    advisor.context(args.region)
    args.output.mkdir(parents=True, exist_ok=True)
    contract = audit_contract(rank, players, args.cache, catalog)
    write_json(args.output / 'data_contract.json', contract)
    write_json(args.output / 'name_normalization.json', names)
    write_json(args.output / 'splits.json', {'series_ids': ids, 'cutoff': cutoff,
        'states_manifest': state_manifest, 'policy': 'chronological series 60/20/20; frozen history at validation start; no tuning'})
    outputs = {}
    for part in ('validation', 'test'):
        print(f'Replaying {part}: {len(partitions[part])} picks', flush=True)
        rows = replay(partitions[part], advisor, args.region)
        write_json(args.output / f'{part}_queries.json', rows)
        control = [r for r in rows if r['mode'] == 'pro_only']
        outputs[part] = {'metrics': {m: metrics([r for r in rows if r['mode'] == m])
                                    for m in ('pro_only', 'rank_only', 'hybrid')},
                         'recall5_delta_vs_pro': {m: paired_interval(rows, m) for m in ('rank_only', 'hybrid')},
                         'ordered_top5_changed_vs_pro': {m: sum(a['top5'] != b['top5'] for a, b in zip(control,
                             [r for r in rows if r['mode'] == m])) for m in ('rank_only', 'hybrid')}}
    report = {'protocol': 'exploratory_matchup_source_ablation_v1', 'patch': args.patch,
        'rank_cohort_status': cohort_status,
        'rank_platform': args.platform, 'history_cutoff': cutoff,
        'rank_games_cached': int(rank.match_id.nunique()), 'rank_games_eligible': int(rank_ev.rows.match_id.nunique()),
        'rank_future_rows_excluded': rank_ev.excluded_future_rows, 'rank_rejected': rejected,
        'rank_eligible_patches': sorted(rank_ev.rows.patch.unique()),
        'partitions': {p: {'series': len(ids[p]), 'games': len({s['gameid'] for s in partitions[p]}),
                          'picks': len(partitions[p])} for p in partitions},
        'results': outputs, 'hybrid_weight': .5, 'min_matchup_games': advisor.policy.min_games,
        'only_component_changed': 'matchup; same Pro base_wr/prior/threshold/candidate_pool/other_components',
        'integration_enabled': False,
        'decision': 'Do not integrate: exploratory/reused Pro data requires fresh independent evidence; inspect coverage and CI.',
        'limitations': ['Retrieval of observed picks is not proof of strategic quality/counter/win uplift.',
          'Existing Worlds games used in previous project audits: chronological holdout is not a fresh final test.',
          'Rank seed selection uses present-day Challenger status, subject to survivor/selection bias; historical ranks unknown.',
          'Hard Fearless series IDs reconstructed, not officially verified; exclusions in splits.json.',
          'Rank-only means only matchup counts from Rank; other components remain Pro, not an entirely Rank-trained system.',
          'Hybrid averages residuals 50/50 only for Rank pairs with n>=5, otherwise preserves Pro; not pooled counts/probabilities.',
          'Pro snapshot retains its existing earlier-patch backfill; Rank requires exact target patch/platform and pre-cutoff event time.',
          'Gold/XP/CS are descriptive exports, excluded from draft inputs to avoid post-draft leakage.',
          'A degenerate bootstrap CI [0,0] from identical hit patterns is not proof of equivalence or zero population uncertainty.',
          'Scores are heuristic priorities, not calibrated probabilities; this experiment cannot assess probability calibration.',
          'No observed-pick retrieval benchmark validates ban decisions or BO5 optimality.'],
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'db_sha256': hashlib.sha256(DB_PATH.read_bytes()).hexdigest(),
        'catalog_sha256': hashlib.sha256(args.catalog.read_bytes()).hexdigest(),
        'raw_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.cache.glob('*.match.json'))}}
    write_json(args.output / 'evaluation.json', report)
    lines = ['# Thử nghiệm nguồn đối đầu Rank / Pro', '',
        f"Patch {args.patch}, cutoff {cutoff}. Rank hợp lệ: {report['rank_games_eligible']}/{report['rank_games_cached']} trận cache.",
        'Đánh giá thăm dò trên dữ liệu giải cũ, không phải final test mới. Chưa bật tích hợp contextual.', '',
        '| Tập | Cấu hình | Queries | Recall@5 | MRR@5 | Queries có ứng viên đủ mẫu Rank |',
        '|---|---|---:|---:|---:|---:|']
    for part, result in outputs.items():
        for mode, met in result['metrics'].items():
            lines.append(f"| {part} | {mode} | {met['queries']} | {met['recall_at_5']:.4f} | {met['mrr_at_5']:.4f} | {met['queries_with_supported_rank_candidate']} |")
    lines += ['', 'Chênh Recall@5 so Pro và CI95 bootstrap theo series:']
    for part, result in outputs.items():
        for mode, delta in result['recall5_delta_vs_pro'].items():
            lines.append(f"- {part}/{mode}: {delta['delta']:.4f}, CI95 {delta['ci95']}; {delta['series']} series.")
    lines += ['', 'Chỉ thay thành phần matchup; cùng pool hợp lệ, role chỉ suy từ lịch sử đã đóng băng và tướng đã lộ. Hybrid cố định50/50, không tune từ test.', '',
              'CI [0,0] ở metric có cùng hit/miss không chứng minh hai phương pháp tương đương trong tổng thể. Đọc cùng coverage và số series nhỏ.', '',
              '## Giới hạn', ''] + [f'- {x}' for x in report['limitations']]
    (args.output / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'eligible_rank_games': report['rank_games_eligible'], 'results': outputs}, ensure_ascii=False), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=ROOT / 'data/raw/riot_matchups_study')
    parser.add_argument('--catalog', type=Path, default=ROOT / 'data/raw/riot_matchups_study/champion_16.20.1.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'reports/rank_transfer_evaluation')
    parser.add_argument('--region', default='WLDS')
    parser.add_argument('--platform', default='KR')
    parser.add_argument('--patch', default='16.20')
    parser.add_argument('--cohort-policy', type=Path, default=ROOT / 'src/config/draft_modes.json')
    parser.add_argument('--rank-evidence', type=Path, help='Private historical rank evidence records.')
    parser.add_argument('--allow-seed-only-research', action='store_true',
                        help='Reproduce the old unverified-seed experiment; never label it verified high rank.')
    args = parser.parse_args()
    try:
        evaluate(args)
    except ValueError as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
