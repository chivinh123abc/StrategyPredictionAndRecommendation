import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src/01_data_pipeline'))
from ranked_matchups import RiotClient, RiotError
from rank_coverage import load_cohort, observations, coverage_tables, chronological_plan, build, SCOPE
from rank_eligibility import read_policy
from collect_rank_snapshots import collect_run
from collect_rank_batches import campaign
from test_ranked_matchups import fixture


class RankCoverageTests(unittest.TestCase):
    def make_run(self, base, shift=0, exclude=None):
        d, t = fixture()
        for p in d['info']['participants']:
            p['puuid'] = f'private-{p["participantId"]}'
            p['championId'] = p['participantId']
        now = datetime.fromtimestamp(d['info']['gameStartTimestamp']/1000 + 3600 + shift, timezone.utc)
        def get(host, path, params=None):
            if '/entries/by-puuid/' in path:
                return [{'queueType': 'RANKED_SOLO_5x5', 'tier': 'MASTER'}]
            return t if path.endswith('/timeline') else d
        client = Mock(); client.get.side_effect = get
        a = SimpleNamespace(policy=ROOT/'src/config/draft_modes.json', cache=base/'private', output=base/'public',
            match_id=['KR_123'], limit=5, platform='kr', routing='asia', seed_players=5, matches_per_seed=1,
            max_match_age_hours=24, max_snapshot_spread_minutes=15, exclude_match_ids=exclude or set())
        summary, matches = collect_run(a, client, lambda: now)
        return a, client, summary

    def test_http_budget_counts_retry_and_stops_before_next_request(self):
        session = Mock(); session.get.return_value = Mock(status_code=503)
        client = RiotClient('dummy', session=session, sleep=Mock(), max_requests=1)
        with self.assertRaises(RiotError) as err:
            client.get('kr', '/fixture')
        self.assertEqual(err.exception.reason_code, 'request_budget_exhausted')
        self.assertEqual(session.get.call_count, 1)
        self.assertEqual(client.request_attempts, 1)

    def test_seen_explicit_id_is_not_refetched_or_replaced_by_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, client, summary = self.make_run(Path(tmp), exclude={'KR_123'})
            self.assertEqual(summary['candidate_games'], 0)
            client.get.assert_not_called()

    def test_duplicate_runs_count_same_game_and_players_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            self.make_run(base); self.make_run(base, shift=60)
            policy = read_policy(ROOT/'src/config/draft_modes.json')
            selected, universe, runs, hashes = load_cohort(base/'public', base/'private', policy)
            rows, games = observations(selected)
            self.assertEqual(len(runs), 2)
            self.assertEqual(len(games), 1)
            self.assertEqual(len(rows), 10)
            self.assertEqual(rows._puuid.nunique(), 10)
            self.assertEqual(games.selected_run_id.iloc[0], runs[0]['run_id'])

    def test_unobserved_candidate_names_have_zero_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); self.make_run(base)
            selected, universe, _, _ = load_cohort(base/'public', base/'private', read_policy(ROOT/'src/config/draft_modes.json'))
            rows, _ = observations(selected)
            universe.add(('KR', 420, '16.20', 'MASTER', 'top', 99, 'not-in-accepted'))
            champs, lanes = coverage_tables(rows, universe)
            zero = champs[champs.champion_id.eq(99)].iloc[0]
            self.assertEqual(zero.games, 0)
            self.assertEqual(zero.games_needed, 5)
            self.assertEqual(zero.players_needed, 3)
            self.assertTrue(lanes[lanes.champion_id.eq(99)].games.eq(0).all())

    def plan_data(self):
        scope = dict(platform='KR', queue=420, patch='16.23', tier_floor='MASTER')
        games = pd.DataFrame([{**scope, 'match_id': f'g{i}', 'played_at': f'2026-01-{i:02}T00:00:00Z',
            'ended_at': f'2026-01-{i:02}T00:30:00Z', 'available_at': f'2026-01-{i:02}T01:00:00Z'} for i in range(1,11)])
        champs = pd.DataFrame([{**scope, 'role': role, 'champion_id': c, 'supported': True}
                              for role in ['top','jng','mid','bot','sup'] for c in [1,2]])
        return games, champs

    def test_chronological_split_preserves_games_and_requires_available_evidence(self):
        games, champs = self.plan_data()
        result = chronological_plan(games, champs)
        self.assertTrue(result['ready'])
        self.assertEqual([result['partitions'][p]['games'] for p in ('history','validation','test')], [6,2,2])
        games['available_at'] = '2026-02-01T00:00:00Z'
        result = chronological_plan(games, champs)
        self.assertFalse(result['ready'])
        self.assertEqual(result['partitions']['history']['available_before_validation_games'], 0)
        self.assertIn('insufficient_history_with_snapshot_evidence_available_before_validation', result['blockers'])

    def test_tied_start_times_stay_in_one_partition(self):
        games, champs = self.plan_data()
        games = pd.concat([games, games.iloc[[6]].assign(match_id='same-time-as-g7')])
        result = chronological_plan(games, champs)
        membership = {g: p for p, data in result['partitions'].items() for g in data['match_ids']}
        self.assertEqual(membership['g7'], membership['same-time-as-g7'])

    def test_empty_collection_exports_headers_and_blocks_readiness(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            result = build(SimpleNamespace(collection=base/'public', private=base/'private',
                policy=ROOT/'src/config/draft_modes.json', output=base/'out'))
            self.assertEqual(result['accepted_unique_games'], 0)
            self.assertFalse(result['readiness'])
            self.assertTrue(pd.read_csv(base/'out/champion_role_coverage.csv').empty)

    def test_build_exports_counts_without_private_ids_and_json_scalar_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); self.make_run(base)
            result = build(SimpleNamespace(collection=base/'public', private=base/'private',
                policy=ROOT/'src/config/draft_modes.json', output=base/'out'))
            self.assertEqual(result['accepted_unique_games'], 1)
            self.assertEqual(result['unique_players'], 10)
            ready = json.loads((base/'out/readiness.json').read_text(encoding='utf-8'))
            self.assertEqual(ready['target_scope']['queue'], 420)
            text = (base/'out/observations.csv').read_text(encoding='utf-8-sig')
            self.assertNotIn('private-', text)
            self.assertNotIn('_puuid', text)

    def test_campaign_stops_on_partial_batch_and_advances_seed_slice(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            args = SimpleNamespace(policy=ROOT/'src/config/draft_modes.json', output=base/'public', cache=base/'private',
                batches=3, seed_offset=5, seeds_per_batch=5, matches_per_batch=5, platform='kr', routing='asia')
            client = Mock(request_attempts=3, max_requests=200)
            summaries = [({'collection_status':'complete','accepted_games':1}, [{'match_id':'KR_123','status':'accepted'}]),
                         ({'collection_status':'api_stopped','accepted_games':0}, [])]
            with patch('collect_rank_batches.collect_run', side_effect=summaries) as mocked:
                runs = campaign(args, client)
            self.assertEqual(len(runs), 2)
            self.assertEqual([c.args[0].seed_offset for c in mocked.call_args_list], [5,10])
            self.assertIn('KR_123', mocked.call_args_list[1].args[0].exclude_match_ids)


if __name__ == '__main__':
    unittest.main()
