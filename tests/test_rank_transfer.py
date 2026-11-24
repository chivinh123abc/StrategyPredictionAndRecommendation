import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
import tempfile
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'src/01_data_pipeline'), str(ROOT / 'src/07_recommender')]
from rank_data_contract import ChampionCatalog, normalize_observations
from ranked_matchups import extract_match, collect
from evaluate_rank_transfer import RankEvidence, split_series, TransferAdvisor, paired_interval, metrics
from draft_advisor import AdvisorPolicy
from draft_meta import MetaPolicy
from historical_recommender import evidence
from test_ranked_matchups import fixture


class RankTransferTests(unittest.TestCase):
    def test_collection_limits_each_seed_and_passes_historical_range(self):
        def get(host, path, params=None):
            if 'challengerleagues' in path:
                return {'entries': [{'puuid': f'seed{i}'} for i in range(3)]}
            if 'by-puuid' in path:
                self.assertEqual(params['count'], 1)
                self.assertLess(params['startTime'], params['endTime'])
                return [f'KR_{path.split("/")[-2][-1]}']
            mid = path.removesuffix('/timeline').split('/')[-1]
            d, t = fixture()
            result = t if path.endswith('/timeline') else d
            result['metadata'] = {'matchId': mid}
            return result
        client = Mock(); client.get.side_effect = get
        with tempfile.TemporaryDirectory() as tmp:
            args = SimpleNamespace(platform='kr', routing='asia', match_id=None, limit=3,
                seed_players=3, matches_per_seed=1, start_time='2026-10-01T00:00:00Z',
                end_time='2026-10-14T23:59:59Z', cache=Path(tmp))
            with patch('ranked_matchups.RiotClient', return_value=client):
                collect(args)
            manifest = json.loads((Path(tmp) / 'collection_manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['seed_players_used'], 3)
            self.assertEqual(len(manifest['matches']), 3)
            self.assertTrue(all(s['returned_ids'] == 1 for s in manifest['seed_counts']))

    def test_official_aliases_ids_and_unknown_rejection(self):
        c = ChampionCatalog({'version': 'test', 'data': {
            'MonkeyKing': {'id': 'MonkeyKing', 'name': 'Wukong', 'key': '62'},
            'AurelionSol': {'id': 'AurelionSol', 'name': 'Aurelion Sol', 'key': '136'}}})
        self.assertEqual(c.name('MonkeyKing'), 'Wukong')
        self.assertEqual(c.name('aurelion-sol'), 'Aurelion Sol')
        self.assertEqual(c.name('irrelevant', 62), 'Wukong')
        with self.assertRaises(ValueError): c.name('invented champion')
        with self.assertRaises(ValueError): c.name('Wukong', 9999)
        rows, audit = normalize_observations(pd.DataFrame([{'champion': 'MonkeyKing', 'opponent': 'AurelionSol'}]), c)
        self.assertEqual(rows.iloc[0].opponent, 'Aurelion Sol')
        self.assertTrue(all(r['changed'] for r in audit))

    def test_official_alias_collision_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            ChampionCatalog({'data': {'A': {'id': 'a-b', 'name': 'A', 'key': '1'},
                                       'B': {'id': 'ab', 'name': 'B', 'key': '2'}}})

    def test_temporal_scope_uses_end_time_patch_platform(self):
        d, t = fixture()
        rows = pd.DataFrame(extract_match(d, t))
        cut = pd.Timestamp(rows.ended_at.iloc[0]) + pd.Timedelta(seconds=1)
        future = rows.assign(match_id='KR_future', ended_at=(cut + pd.Timedelta(seconds=1)).isoformat())
        wrong_patch = rows.assign(match_id='KR_wrong_patch', patch='16.21')
        wrong_server = rows.assign(match_id='VN2_wrong_server', platform='VN2')
        ev = RankEvidence(pd.concat([rows, future, wrong_patch, wrong_server]), cut, '16.20')
        self.assertEqual(ev.rows.match_id.nunique(), 1)
        self.assertEqual(ev.excluded_future_rows, 10)
        self.assertEqual(ev.counts[('top', 'champ1', 'jng', 'champ7')], 1)
        self.assertEqual(ev.counts[('top', 'champ1', 'jng', 'champ2')], 0)

    def test_rank_residual_requires_samples_and_has_correct_sign(self):
        d, t = fixture()
        rows = pd.DataFrame(extract_match(d, t))
        many = pd.concat([rows.assign(match_id=f'KR_{i}') for i in range(5)])
        cut = pd.Timestamp(rows.ended_at.iloc[0]) + pd.Timedelta(seconds=1)
        ev = RankEvidence(many, cut, '16.20')
        score, trace, coverage = ev.evaluate('top', 'champ1', {'top': {'champ6': 1}}, .5, 1, 5, 10)
        self.assertAlmostEqual(score, .5 + .5 * 5 / 15)
        self.assertEqual(coverage, 1)
        self.assertEqual(trace[0]['games'], 5)
        self.assertEqual(ev.evaluate('top', 'champ1', {'top': {'champ6': 1}}, .5, 1, 6, 10)[0], .5)

    def test_series_disjoint_chronology_and_overlap_rejection(self):
        states = [{'action': 'pick', 'patch': '16.20', 'series_id': f's{i}',
                   'date': f'2026-10-{i+1:02}T00:00:00+00:00', 'gameid': f'g{i}', 'turn': 7}
                   for i in range(10)]
        parts, ids = split_series(states, '16.20')
        self.assertEqual([len(parts[x]) for x in ('history', 'validation', 'test')], [6, 2, 2])
        self.assertFalse(set(ids['history']) & set(ids['test']))
        bad = copy.deepcopy(states)
        bad.append({**states[0], 'date': '2026-10-08T12:00:00+00:00'})
        with self.assertRaisesRegex(ValueError, 'Overlapping'): split_series(bad, '16.20')

    def make_advisor(self, rank_n):
        a = TransferAdvisor.__new__(TransferAdvisor)
        a.policy = AdvisorPolicy()
        a.meta_policy = MetaPolicy()
        a.rank_coverage = {}
        a.rank_evidence = Mock()
        ev = {**evidence(rank_n, rank_n), 'enemy_role': 'top', 'opponent': 'enemy', 'role_probability': 1}
        a.rank_evidence.evaluate.return_value = (.5 if rank_n < 5 else .5 + .5 * rank_n / (rank_n + 10), [ev], int(rank_n >= 5))
        snapshot = Mock()
        snapshot.enemy_evidence.return_value = {**evidence(0, 10), 'enemy_role': 'top', 'opponent': 'enemy'}
        return a, snapshot

    def test_hybrid_missing_rank_preserves_control_exactly(self):
        a, snapshot = self.make_advisor(1)
        args = ('top', 'own', {'top': {'enemy': 1}}, snapshot, .5, 1)
        a.mode = 'pro_only'; pro = a.evaluate_enemy_context(*args)
        a.mode = 'hybrid'; hybrid = a.evaluate_enemy_context(*args)
        self.assertEqual(pro[0], hybrid[0])
        self.assertEqual(pro[2], hybrid[2])
        a.mode = 'rank_only'; rank = a.evaluate_enemy_context(*args)
        self.assertEqual(rank[0], .5)
        self.assertEqual(rank[2], 0)

    def test_hybrid_averages_supported_pair_residuals(self):
        a, snapshot = self.make_advisor(10)
        args = ('top', 'own', {'top': {'enemy': 1}}, snapshot, .5, 1)
        a.mode = 'pro_only'; pro = a.evaluate_enemy_context(*args)
        a.mode = 'rank_only'; rank = a.evaluate_enemy_context(*args)
        a.mode = 'hybrid'; hybrid = a.evaluate_enemy_context(*args)
        self.assertAlmostEqual(hybrid[0], (pro[0] + rank[0]) / 2)

    def test_metrics_and_bootstrap_pair_identity(self):
        rows = [{'gameid': 'g', 'turn': 7, 'series_id': 's', 'mode': m, 'rank': r,
                 'rank_supported_candidates': 0, 'enemy_count': 1}
                for m, r in [('pro_only', None), ('rank_only', 1)]]
        delta = paired_interval(rows, 'rank_only')
        self.assertEqual(delta['delta'], 1)
        self.assertEqual(delta['ci95'], [1, 1])
        self.assertEqual(metrics(rows)['recall_at_5'], .5)
        rows[1]['turn'] = 8
        with self.assertRaises(AssertionError): paired_interval(rows, 'rank_only')


if __name__ == '__main__':
    unittest.main()
