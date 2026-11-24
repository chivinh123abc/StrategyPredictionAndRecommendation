from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src/01_data_pipeline'))
from collect_rank_snapshots import parse_snapshot, classify_match, collect_run
from ranked_matchups import RiotError
from rank_eligibility import read_policy
from test_ranked_matchups import fixture


class RankSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.policy = read_policy(ROOT / 'src/config/draft_modes.json')
        self.d, self.t = fixture()
        for p in self.d['info']['participants']:
            p['puuid'] = f'private-{p["participantId"]}'
        self.now = datetime.fromtimestamp(self.d['info']['gameStartTimestamp'] / 1000 + 3600, timezone.utc)

    def entry(self, tier='MASTER', queue='RANKED_SOLO_5x5'):
        return {'tier': tier, 'queueType': queue, 'rank': 'I', 'leaguePoints': 0}

    def snapshots(self):
        return {('KR', p['puuid']): parse_snapshot([self.entry()], p['puuid'], 'kr', self.now.isoformat(), 'private-fixture')
                for p in self.d['info']['participants']}

    def classify(self, snapshots):
        return classify_match(self.d, snapshots, self.policy, self.now)

    def test_accepts_ten_current_master_but_never_historical(self):
        r = self.classify(self.snapshots())
        self.assertEqual(r['status'], 'accepted')
        self.assertEqual(r['high_participants'], 10)
        self.assertFalse(r['historical_rank_verified'])
        self.assertNotIn('puuid', json.dumps(r))

    def test_one_below_floor_rejected(self):
        s = self.snapshots(); s[('KR', 'private-1')]['tier'] = 'DIAMOND'
        r = self.classify(s)
        self.assertEqual(r['status'], 'rejected')
        self.assertEqual(r['below_floor_participants'], 1)

    def test_absent_rank_is_missing_not_low(self):
        s = self.snapshots(); s.pop(('KR', 'private-1'))
        r = self.classify(s)
        self.assertEqual(r['status'], 'missing')
        self.assertEqual(r['missing_participants'], 1)
        self.assertEqual(r['below_floor_participants'], 0)

    def test_flex_unranked_duplicate_and_bad_payload_not_valid_solo(self):
        cases = [([], 'no_solo_rank_entry'), ([self.entry(queue='RANKED_FLEX_SR')], 'no_solo_rank_entry'),
                 ([self.entry(), self.entry()], 'ambiguous_solo_rank_entry'), ({}, 'invalid_response_shape'),
                 ([self.entry('INVENTED')], 'unrecognized_tier'),
                 ([{**self.entry(), 'puuid': 'someone-else'}], 'response_identity_mismatch')]
        for payload, expected in cases:
            r = parse_snapshot(payload, 'p', 'KR', self.now.isoformat(), 'fixture')
            self.assertEqual(r['status'], expected)
            self.assertIsNone(r['tier'])

    def test_zero_lp_is_preserved(self):
        r = parse_snapshot([self.entry()], 'p', 'KR', self.now.isoformat(), 'fixture')
        self.assertEqual(r['league_points'], 0)

    def test_old_match_rejected_even_with_ten_high_snapshots(self):
        self.d['info']['gameStartTimestamp'] -= 48 * 3600 * 1000
        r = self.classify(self.snapshots())
        self.assertEqual(r['status'], 'rejected')
        self.assertTrue(r['all_ten_high_at_observation'])
        self.assertIn('match_too_old_for_near_match_proxy', r['reasons'])

    def test_spread_future_and_wrong_scope_rejected(self):
        s = self.snapshots(); s[('KR', 'private-1')]['observed_at'] = (self.now - timedelta(minutes=20)).isoformat()
        self.assertIn('snapshot_spread_exceeded', self.classify(s)['reasons'])
        s = self.snapshots(); s[('KR', 'private-1')]['observed_at'] = (self.now + timedelta(seconds=1)).isoformat()
        self.assertEqual(self.classify(s)['missing_participants'], 1)
        s = self.snapshots(); s[('KR', 'private-1')]['platform'] = 'VN2'
        self.assertEqual(self.classify(s)['missing_participants'], 1)

    def test_snapshot_before_match_end_rejected(self):
        s = self.snapshots()
        for value in s.values():
            value['observed_at'] = datetime.fromtimestamp(self.d['info']['gameStartTimestamp'] / 1000, timezone.utc).isoformat()
        self.assertIn('snapshot_precedes_match_end', self.classify(s)['reasons'])

    def run_fixture(self, fatal=None):
        requests = []
        def get(host, path, params=None):
            requests.append(path)
            if '/entries/by-puuid/' in path:
                if fatal:
                    raise fatal
                return [self.entry()]
            if path.endswith('/timeline'):
                return self.t
            return self.d
        client = Mock(); client.get.side_effect = get
        temp = tempfile.TemporaryDirectory(); base = Path(temp.name)
        args = SimpleNamespace(policy=ROOT / 'src/config/draft_modes.json', cache=base / 'private',
            output=base / 'reports', match_id=['KR_123', 'KR_123'], limit=5, platform='kr', routing='asia',
            seed_players=5, matches_per_seed=1, max_match_age_hours=24, max_snapshot_spread_minutes=15)
        summary, matches = collect_run(args, client, clock=lambda: self.now)
        return temp, base, summary, matches, requests

    def test_run_persists_all_ten_and_exports_no_identity(self):
        tmp, base, summary, matches, requests = self.run_fixture()
        try:
            self.assertEqual(summary['accepted_games'], 1)
            self.assertEqual(summary['unique_participants_checked'], 10)
            self.assertEqual(summary['accepted_observations'], 10)
            self.assertEqual(sum('/entries/by-puuid/' in p for p in requests), 10)
            run = summary['run_id']
            private = json.loads((base / 'private' / run / 'rank_snapshots.json').read_text(encoding='utf-8'))
            self.assertEqual(len(private), 10)
            public = (base / 'reports' / run / 'matches.json').read_text(encoding='utf-8')
            self.assertNotIn('private-', public)
            self.assertNotIn('puuid', public)
            self.assertTrue((base / 'reports' / run / 'accepted_observations.csv').exists())
        finally:
            tmp.cleanup()

    def test_auth_failure_stops_after_first_rank_request_and_reports_missing(self):
        tmp, base, summary, matches, requests = self.run_fixture(RiotError('sanitized', 403))
        try:
            self.assertEqual(summary['collection_status'], 'api_stopped')
            self.assertEqual(summary['missing_games'], 1)
            self.assertEqual(summary['accepted_games'], 0)
            self.assertEqual(sum('/entries/by-puuid/' in p for p in requests), 1)
        finally:
            tmp.cleanup()

    def test_404_is_missing_and_checks_remaining_participants(self):
        tmp, base, summary, matches, requests = self.run_fixture(RiotError('sanitized', 404))
        try:
            self.assertEqual(summary['collection_status'], 'complete')
            self.assertEqual(summary['missing_games'], 1)
            self.assertEqual(summary['unique_participants_checked'], 10)
            self.assertEqual(sum('/entries/by-puuid/' in p for p in requests), 10)
        finally:
            tmp.cleanup()


if __name__ == '__main__':
    unittest.main()
