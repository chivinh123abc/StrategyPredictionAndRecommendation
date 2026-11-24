from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import math

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/07_recommender')]
from draft_advisor import DraftAdvisor,AdvisorPolicy
from historical_recommender import HistoricalRecommender,evidence
from draft_meta import MetaPolicy
from compare_pick_scoring import collapse
from test_matchup_evidence import fixture


class SimplePickScoringTests(unittest.TestCase):
    def advisor(self):
        obj=DraftAdvisor.__new__(DraftAdvisor);obj.policy=AdvisorPolicy(scoring='simple')
        return obj

    def rows(self):
        return [{'champion':'A','games':10,'historical':evidence(6,10)},
                {'champion':'B','games':5,'historical':evidence(2,5)}]

    def snapshot(self):
        return SimpleNamespace(role_counts={('mid','A'):10,('mid','B'):5},metadata=lambda:{'scope':'fixture'})

    def test_default_is_unchanged_and_variant_uses_three_equal_signals(self):
        self.assertEqual(AdvisorPolicy().scoring,'current')
        self.assertEqual(AdvisorPolicy(scoring='simple').effective_weights,{'pick_frequency':1.,'content':1.,'matchup':1.})
        with self.assertRaises(ValueError):AdvisorPolicy(scoring='invented')

    def test_exact_mean_supported_matchup_and_missing_profile(self):
        rows=self.advisor()._simple_rows(self.rows(),'mid',{'mid':'Enemy'},self.snapshot(),
            {'Enemy':1.},{'A':.6},'fixture',{('mid','A','Enemy'):(4,5)},'F1')
        self.assertEqual(rows[0]['champion'],'A');self.assertAlmostEqual(rows[0]['score'],.8)
        self.assertAlmostEqual(rows[1]['score'],.45)
        self.assertNotIn('content',rows[1]['score_components'])
        self.assertEqual(rows[1]['score_components']['matchup']['source'],'historical_role_winrate_fallback')
        self.assertTrue(rows[1]['review_required'])
        self.assertEqual(rows[1]['mechanical_counter_status'],'not_evaluated')

    def test_no_enemy_does_not_invent_matchup(self):
        rows=self.advisor()._simple_rows(self.rows(),'mid',{},self.snapshot(),{}, {},'fixture',{},None)
        self.assertEqual(rows[0]['score'],1.)
        self.assertEqual(set(rows[0]['score_components']),{'pick_frequency'})
        self.assertEqual(rows[0]['enemy_context_evidence'],[])
        self.assertFalse(rows[0]['review_required'])

    def test_flex_uses_only_supported_mass_and_does_not_claim_full_team(self):
        rows=self.advisor()._simple_rows(self.rows(),'mid',{'top':'Flex','mid':'Enemy'},self.snapshot(),
            {'Enemy':.75,'Flex':.25},{},'fixture',{('mid','A','Enemy'):(4,5),('mid','A','Flex'):(1,1)},None)
        self.assertAlmostEqual(rows[0]['score_components']['matchup']['value'],.8)
        self.assertAlmostEqual(rows[0]['enemy_context_coverage'],.375)
        self.assertEqual(rows[0]['matchup_scope'],'same_role_only')
        self.assertEqual(rows[0]['mechanical_counter_status'],'not_evaluated')

    def test_candidate_pools_and_exclusions_match_current(self):
        m,p,_=fixture();history=HistoricalRecommender.from_frames(m,p)
        args=dict(historical=history,meta_policy=MetaPolicy(as_of='2026-11-06'),explain_matchups=False)
        current=DraftAdvisor(**args);simple=DraftAdvisor(**args,policy=AdvisorPolicy(scoring='simple'))
        query=('top',{}, {'top':'C6'})
        a=current.recommend_picks(*query,region='WLDS');b=simple.recommend_picks(*query,region='WLDS')
        self.assertTrue(a);self.assertEqual({r['champion'] for r in a},{r['champion'] for r in b})
        self.assertFalse(simple.recommend_picks(*query,already_banned=['C1'],region='WLDS'))
        for row in b:self.assertTrue(math.isfinite(row['score']) and 0<=row['score']<=1)

    def test_simple_does_not_call_pair_lift_scoring(self):
        m,p,_=fixture();simple=DraftAdvisor(historical=HistoricalRecommender.from_frames(m,p),
            meta_policy=MetaPolicy(as_of='2026-11-06'),policy=AdvisorPolicy(scoring='simple'),explain_matchups=False)
        snapshot,_,_=simple.context('WLDS')
        with patch.object(snapshot,'pair_evidence',side_effect=AssertionError('Lift used by simple scorer')):
            rows=simple.recommend_picks('top',{'mid':'C3'},{'top':'C6'},region='WLDS')
        self.assertTrue(rows)
        self.assertEqual(rows[0]['composition_lift'],1.)
        self.assertEqual(rows[0]['composition_evidence'],[])

    def test_collapse_preserves_supported_tier_and_best_role(self):
        rows=[dict(champion='A',lane='mid',games=1,score=.99,evidence_status='sparse_candidate'),
            dict(champion='A',lane='top',games=5,score=.5,evidence_status='observed_candidate'),
            dict(champion='B',lane='mid',games=5,score=.6,evidence_status='observed_candidate')]
        self.assertEqual(collapse(rows),['B','A'])


if __name__=='__main__':unittest.main()
