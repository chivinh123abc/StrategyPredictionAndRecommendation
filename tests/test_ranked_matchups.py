"""Synthetic fixtures test invariants; never used as real matchup evidence."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src/01_data_pipeline'))
from ranked_matchups import (extract_match, load_rank, summarize, RiotClient,
                            RiotError, ROLES, pro_observations)


def fixture():
    participants = []
    frames = {}
    for i in range(1, 11):
        participants.append({'participantId': i, 'teamId': 100 if i <= 5 else 200,
                             'teamPosition': list(ROLES)[(i - 1) % 5],
                             'championName': f'champ{i}', 'win': i <= 5})
        frames[str(i)] = {'totalGold': i * 100, 'xp': i * 20,
                          'minionsKilled': i * 2, 'jungleMinionsKilled': i}
    meta = {'matchId': 'KR_123'}
    detail = {'metadata': meta, 'info': {'queueId': 420, 'mapId': 11,
              'gameDuration': 1200, 'gameStartTimestamp': 1780000000000,
              'gameVersion': '16.20.123.4', 'participants': participants}}
    timeline = {'metadata': meta, 'info': {'frames': [
        {'timestamp': t, 'participantFrames': copy.deepcopy(frames)}
        for t in [0, 599900, 600001, 900000]]}}
    return detail, timeline


class RankedMatchupsTests(unittest.TestCase):
    def test_signed_mirrors_ids_and_no_future_frame(self):
        d, t = fixture()
        # Participant order is irrelevant; team IDs and participant IDs are authoritative.
        d['info']['participants'].reverse()
        rows = extract_match(d, t)
        self.assertEqual(len(rows), 10)
        a = next(r for r in rows if r['team_id'] == 100 and r['role'] == 'top')
        b = next(r for r in rows if r['team_id'] == 200 and r['role'] == 'top')
        self.assertEqual(a['gold_diff_10'], -500)
        self.assertEqual(a['cs_diff_10'], -15)
        self.assertEqual(b['gold_diff_10'], 500)
        self.assertEqual(a['frame_ms_10'], 599900)
        self.assertEqual(a['patch'], '16.20')
        self.assertFalse(any('puuid' in r for r in rows))

    def test_missing_measurements_never_zero_or_future(self):
        d, t = fixture()
        del t['info']['frames'][1]['participantFrames']['1']['xp']
        rows = extract_match(d, t)
        self.assertIsNone(rows[0]['xp_diff_10'])
        self.assertEqual(rows[0]['gold_diff_10'], -500)
        t['info']['frames'] = [t['info']['frames'][0], t['info']['frames'][2]]
        rows = extract_match(d, t)
        self.assertIsNone(rows[0]['gold_diff_10'])
        self.assertIsNone(rows[0]['frame_ms_10'])

    def test_short_game_no_15_backfill(self):
        d, t = fixture()
        d['info']['gameDuration'] = 800
        self.assertIsNone(extract_match(d, t)[0]['gold_diff_15'])
        d['info']['gameDuration'] = 599
        with self.assertRaisesRegex(ValueError, 'shorter'):
            extract_match(d, t)

    def test_frame_tolerance_and_descriptive_only_nearest(self):
        d, t = fixture()
        t['info']['frames'] = [t['info']['frames'][1], t['info']['frames'][2]]
        t['info']['frames'][0]['timestamp'] = 540200
        self.assertIsNone(extract_match(d, t)[0]['gold_diff_10'])
        nearest = extract_match(d, t, 'nearest')[0]
        self.assertEqual(nearest['frame_ms_10'], 600001)
        self.assertEqual(nearest['gold_diff_10'], -500)
        t['info']['frames'][1]['timestamp'] = 601001
        self.assertIsNone(extract_match(d, t, 'nearest')[0]['gold_diff_10'])

    def test_ambiguous_roles_rejected(self):
        for invalid in ('', 'TOP'):
            d, t = fixture()
            d['info']['participants'][1]['teamPosition'] = invalid
            with self.assertRaises(ValueError):
                extract_match(d, t)

    def test_identity_queue_result_guards(self):
        for part, key, value in [('timeline', 'matchId', 'KR_999'),
                                  ('detail', 'queueId', 440), ('detail', 'mapId', 12)]:
            d, t = fixture()
            if part == 'timeline':
                t['metadata'] = {key: value}
            else:
                d['info'][key] = value
            with self.assertRaises(ValueError):
                extract_match(d, t)
        d, t = fixture()
        d['info']['participants'][0]['win'] = False
        with self.assertRaisesRegex(ValueError, 'result'):
            extract_match(d, t)

    def test_cache_dedup_rejection_and_summary(self):
        d, t = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            for name, obj in [('KR_123.match.json', d), ('KR_123.timeline.json', t),
                              ('bad.match.json', d)]:
                (p / name).write_text(json.dumps(obj), encoding='utf-8')
            rows, rejected = load_rank(p)
        self.assertEqual(len(rows), 10)
        self.assertEqual(len(rejected), 1)
        stats = summarize(rows, ['platform', 'queue'])
        self.assertEqual(len(stats), 10)
        self.assertTrue(stats.games.eq(1).all())
        self.assertTrue(stats.ci95_high.gt(stats.ci95_low).all())
        self.assertTrue(stats.gold_diff_10_n.eq(1).all())
        self.assertTrue(stats.gold_diff_10_sd.isna().all())
        # Patch/role groups cannot be silently pooled.
        other = rows.assign(patch='16.21', match_id='KR_124')
        self.assertEqual(len(summarize(pd.concat([rows, other]), ['platform', 'queue'])), 20)

    def test_pro_strict_roles_and_actual_measurements(self):
        d, t = fixture()
        rows = []
        for p in d['info']['participants']:
            rows.append(dict(gameid='pro1', side='Blue' if p['teamId'] == 100 else 'Red',
                             position=ROLES[p['teamPosition']], champion=p['championName'],
                             result=int(p['win']), date='2026-10-01', league='WLDS', patch=16.2,
                             gamelength=1200, datacompleteness='complete',
                             goldat10=p['participantId'] * 100, xpat10=None, csat10=None))
        players = pd.DataFrame(rows)
        out = pro_observations(players)
        self.assertEqual(len(out), 10)
        self.assertEqual(out.iloc[0].gold_diff_10, -500)
        self.assertTrue(out.gold_diff_15.isna().all())
        self.assertTrue(out.patch.eq('16.20').all())
        players.loc[1, 'position'] = 'top'
        self.assertTrue(pro_observations(players).empty)

    def test_client_auth_no_retry_and_no_leak(self):
        session = Mock()
        session.get.return_value.status_code = 403
        client = RiotClient('dummy-test-secret', session=session)
        with self.assertRaises(RiotError) as context:
            client.get('kr', '/test')
        self.assertNotIn('dummy-test-secret', str(context.exception))
        self.assertEqual(session.get.call_count, 1)
        self.assertFalse(session.get.call_args.kwargs['allow_redirects'])

    def test_client_rate_limit_and_bounded_retry(self):
        session, sleep = Mock(), Mock()
        limited = Mock(status_code=429, headers={'Retry-After': '2'})
        success = Mock(status_code=200)
        success.json.return_value = {'ok': True}
        session.get.side_effect = [limited, success]
        self.assertEqual(RiotClient('dummy', session, sleep).get('kr', '/test'), {'ok': True})
        sleep.assert_called_once_with(2)
        session.get.side_effect = None
        session.get.return_value = Mock(status_code=429, headers={'Retry-After': '120'})
        sleep.reset_mock()
        with self.assertRaises(RiotError):
            RiotClient('dummy', session, sleep).get('kr', '/test')
        sleep.assert_not_called()
        session.get.side_effect = requests.ConnectionError('dummy-secret')
        session.get.reset_mock()
        with self.assertRaises(RiotError) as context:
            RiotClient('dummy', session, sleep).get('kr', '/test')
        self.assertEqual(session.get.call_count, 3)
        self.assertNotIn('dummy-secret', str(context.exception))


if __name__ == '__main__':
    unittest.main()
