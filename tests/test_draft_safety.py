from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from draft_safety import role_preferences,infer_free_role,annotate_lane_support,lane_support_priority
from simulate_draft_match import needs_tactical_review


class Snapshot:
    role_counts={('mid','Flex'):100,('top','Flex'):40,('sup','Flex'):10,('jng','Flex'):0}
    def enemy_evidence(self,role,champ,enemy_role,opponent):
        n=7 if champ=='Observed' else 0
        return {'games':n,'wins':4 if n else 0,'winrate':4/7 if n else None,
                'ci95_wilson':[.25,.85] if n else [None,None]}


class DraftSafetyTests(unittest.TestCase):
    def test_sparse_lane_intervals_do_not_override_original_scores(self):
        rows=[{'score':.1483,'lane_review':{'opponent':'Enemy','requires_review':True,'games':1,'ranking_confidence_bound':.206}},
              {'score':.1784,'lane_review':{'opponent':'Enemy','requires_review':True,'games':2,'ranking_confidence_bound':.095}},
              {'score':.2203,'lane_review':{'opponent':'Enemy','requires_review':True,'games':4,'ranking_confidence_bound':.046}},
              {'score':.1361,'lane_review':{'opponent':'Enemy','requires_review':True,'games':0,'ranking_confidence_bound':None}}]
        ranked=sorted(rows,key=lambda r:(lane_support_priority(r,True),-r['score']))
        self.assertEqual([r['score'] for r in ranked],[.2203,.1784,.1483,.1361])

    def test_adequate_lane_support_keeps_review_gate_without_ranking_winrate(self):
        supported={'score':.2,'lane_review':{'opponent':'Enemy','requires_review':False,'ranking_confidence_bound':.1}}
        unknown={'score':.8,'lane_review':{'opponent':'Enemy','requires_review':True,'ranking_confidence_bound':.5}}
        self.assertEqual(sorted([unknown,supported],key=lambda r:(lane_support_priority(r,True),-r['score'])),[supported,unknown])
        self.assertTrue(needs_tactical_review(unknown,{'top':'Enemy'}))

    def test_disabled_lane_comparison_and_blind_lane_do_not_create_priority(self):
        self.assertFalse(lane_support_priority({'lane_review':{'opponent':'Enemy','requires_review':True}},False))
        self.assertFalse(lane_support_priority({'lane_review':{'opponent':None,'requires_review':False}},True))
    def test_manual_placement_uses_highest_observed_free_role(self):
        snapshot=Snapshot()
        self.assertEqual(infer_free_role(snapshot,'Flex',{}),'mid')
        self.assertEqual(infer_free_role(snapshot,'Flex',{'mid':'Taken'}),'top')
        self.assertEqual(infer_free_role(snapshot,'Flex',{'mid':'Taken','top':'Other'}),'sup')
        self.assertEqual([r['games'] for r in role_preferences(snapshot)['Flex']],[100,40,10])

    def test_no_observed_free_position_does_not_invent_an_assignment(self):
        for champ,occupied in [('Unknown',{}),('Flex',{'mid':'A','top':'B','sup':'C'})]:
            with self.assertRaises(ValueError):infer_free_role(Snapshot(),champ,occupied)

    def test_exposed_lane_blocks_auto_without_waiting_for_five_opponents(self):
        rows=annotate_lane_support([{'champion':'Unknown','role':'top','score':.9}],Snapshot(),{'top':'Enemy'},5)
        self.assertTrue(needs_tactical_review(rows[0],{'top':'Enemy'}))
        self.assertEqual(rows[0]['lane_review']['games'],0)
        self.assertEqual(rows[0]['score'],.9)
        self.assertFalse(needs_tactical_review(rows[0],{'top':'Enemy'},True))

    def test_observed_and_blind_lane_do_not_claim_a_counter(self):
        rows=[{'champion':'Observed','role':'top','score':.6}]
        supported=annotate_lane_support(rows,Snapshot(),{'top':'Enemy'},5)[0]
        blind=annotate_lane_support(rows,Snapshot(),{'mid':'Other'},5)[0]
        self.assertFalse(needs_tactical_review(supported,{'top':'Enemy'}))
        self.assertFalse(needs_tactical_review(blind,{'mid':'Other'}))
        self.assertIsNone(blind['lane_review']['games'])
        self.assertNotIn('lane_review',rows[0])

    def test_both_sides_can_have_first_selection_every_game_without_alternation(self):
        from simulate_fearless_series import first_selection_order
        for side in ['blue','red']:
            self.assertEqual(first_selection_order(5,[side]*5),[side]*5)
        with self.assertRaises(ValueError):first_selection_order(5)


if __name__=='__main__':unittest.main()
