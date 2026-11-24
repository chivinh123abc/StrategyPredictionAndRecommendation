from pathlib import Path
import sys
import unittest

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from simulate_draft_match import needs_tactical_review


class TacticalReviewTests(unittest.TestCase):
    def test_unsupported_response_to_full_enemy_team_is_not_auto_finalized(self):
        enemies=dict(zip(['top','jng','mid','bot','sup'],['A','B','C','D','E']))
        for name in ['Candidate1','Candidate2','Trundle']:
            self.assertTrue(needs_tactical_review({'champion':name,'review_required':True},enemies))

    def test_blind_pick_and_supported_response_are_not_blocked(self):
        self.assertFalse(needs_tactical_review({'review_required':True},{'mid':'Enemy'}))
        self.assertFalse(needs_tactical_review({'review_required':False},dict(zip(range(5),range(5)))))

    def test_explicit_statistical_demo_override_is_separate_from_counter_evidence(self):
        choice={'review_required':True,'mechanical_counter_status':'not_evaluated'}
        self.assertFalse(needs_tactical_review(choice,dict(zip(range(5),range(5))),allow_statistical_auto=True))
        self.assertEqual(choice['mechanical_counter_status'],'not_evaluated')
