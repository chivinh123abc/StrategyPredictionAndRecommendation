import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src/01_data_pipeline'))
from rank_eligibility import assess_match, participant_evidence, read_policy, audit, utc
from test_ranked_matchups import fixture


class RankEligibilityTests(unittest.TestCase):
    def setUp(self):
        self.policy = read_policy(ROOT / 'src/config/draft_modes.json')
        self.detail, _ = fixture()
        for p in self.detail['info']['participants']:
            p['puuid'] = f'private-test-{p["participantId"]}'
        self.started = datetime.fromtimestamp(self.detail['info']['gameStartTimestamp'] / 1000, timezone.utc)
        self.cutoff = self.started + timedelta(days=1)

    def records(self, kind='historical_interval', tier='MASTER'):
        return [{'puuid': p['puuid'], 'platform': 'KR', 'queue': 'RANKED_SOLO_5x5',
                 'tier': tier, 'kind': kind, 'source_ref': 'fixture://documented-interval-not-real-data',
                 'observed_at': (self.started - timedelta(minutes=1)).isoformat(),
                 'valid_from': (self.started - timedelta(hours=1)).isoformat(),
                 'valid_until': (self.started + timedelta(hours=1)).isoformat()}
                 for p in self.detail['info']['participants']]

    def assess(self, records, seed=False):
        return assess_match(self.detail, records, self.policy, self.cutoff, seed)

    def test_seed_only_is_unknown_not_low(self):
        r = self.assess([], True)
        self.assertEqual(r['rank_cohort_status'], 'challenger_seed_only')
        self.assertEqual(r['historical_participant_counts'], {'unknown': 10})
        self.assertTrue(r['rank_mode_data_admissible'])
        self.assertFalse(r['pro_high_rank_data_admissible'])

    def test_all_ten_documented_high_required(self):
        self.assertTrue(self.assess(self.records())['pro_high_rank_data_admissible'])
        self.assertFalse(self.assess(self.records()[:9])['pro_high_rank_data_admissible'])

    def test_snapshots_never_become_historical_rank(self):
        r = self.assess(self.records(kind='snapshot', tier='CHALLENGER'))
        self.assertEqual(r['rank_cohort_status'], 'all_ten_high_at_observation_only')
        self.assertFalse(r['pro_high_rank_data_admissible'])

    def test_lower_tier_is_distinct_from_unknown(self):
        data = self.records(); data[0]['tier'] = 'DIAMOND'
        r = self.assess(data)
        self.assertEqual(r['rank_cohort_status'], 'known_below_floor_present')
        self.assertFalse(r['pro_high_rank_data_admissible'])

    def test_wrong_queue_server_future_observation_rejected(self):
        for key, value in [('queue', 'RANKED_FLEX_SR'), ('platform', 'VN2'),
                           ('observed_at', (self.cutoff + timedelta(seconds=1)).isoformat())]:
            data = self.records()
            data[0][key] = value
            self.assertFalse(self.assess(data)['pro_high_rank_data_admissible'])

    def test_missing_source_invalid_interval_or_naive_time_rejected(self):
        for key, value in [('source_ref', ''), ('valid_until', self.started.isoformat()),
                           ('observed_at', '2026-01-01T00:00:00')]:
            data = self.records(); data[0][key] = value
            self.assertFalse(self.assess(data)['pro_high_rank_data_admissible'])

    def test_conflicting_historical_intervals_rejected(self):
        data = self.records(); other = dict(data[0]); other['tier'] = 'CHALLENGER'
        r = self.assess(data + [other])
        self.assertEqual(r['rank_cohort_status'], 'rank_evidence_conflict')
        self.assertFalse(r['pro_high_rank_data_admissible'])

    def test_malformed_match_not_admitted_in_either_mode(self):
        original = copy.deepcopy(self.detail)
        for key, value in [('puuid', 'private-test-1'), ('participantId', 99), ('teamPosition', 'TOP')]:
            self.detail = copy.deepcopy(original)
            self.detail['info']['participants'][1][key] = value
            r = self.assess(self.records())
            self.assertFalse(r['rank_mode_data_admissible'])
            self.assertFalse(r['pro_high_rank_data_admissible'])

    def test_policy_refuses_unsafe_assumptions(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'policy.json'
            policy = copy.deepcopy(self.policy)
            policy['pro']['current_snapshot_is_historical_rank'] = True
            p.write_text(json.dumps(policy), encoding='utf-8')
            with self.assertRaises(ValueError): read_policy(p)
        with self.assertRaises(ValueError): utc('2026-01-01T00:00:00')

    def test_audit_dedup_private_export_and_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); cache = base / 'cache'; cache.mkdir()
            p = cache / 'KR_123.match.json'
            p.write_text(json.dumps(self.detail), encoding='utf-8')
            before = p.read_bytes()
            summary, rows = audit(cache, ROOT / 'src/config/draft_modes.json', base / 'output', cutoff=self.cutoff.isoformat())
            self.assertEqual(summary['pro_high_rank_data_admissible_games'], 0)
            self.assertEqual(before, p.read_bytes())
            text = (base / 'output/matches.json').read_text(encoding='utf-8')
            self.assertNotIn('private-test', text)
            duplicate = cache / 'duplicate.match.json'; duplicate.write_bytes(before)
            with self.assertRaisesRegex(ValueError, 'Duplicate'): audit(cache, ROOT / 'src/config/draft_modes.json', base / 'second')


if __name__ == '__main__':
    unittest.main()
