from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from ban_planner import BanPlanner,ContextualBanPolicy
from simulate_draft_match import DraftState
from draft_advisor import ROLES


class Snapshot:
    def metadata(self):return {'region':'WLDS','dataset_patch':'16.20','requested_as_of':'2026-11-13'}


class Advisor:
    def context(self,region):return Snapshot(),None,None

    def recommend_picks(self,role,own,enemy,player_name=None,**kwargs):
        occupied=set(own.values())|set(enemy.values())
        return [{'champion':f'{role}_{i}','score':(12-i)/20,'games':12,'evidence_status':'observed_candidate'}
                for i in range(12) if f'{role}_{i}' not in occupied]


def planner(**kwargs):
    return BanPlanner(Advisor(),{'blue':{r:'P'for r in ROLES},'red':{r:'Q'for r in ROLES}},
                      {'blue':'A','red':'B'},'WLDS',**kwargs)


class BanPlannerTests(unittest.TestCase):
    def test_removing_a_backup_cannot_increase_short_pool_value(self):
        p=planner()
        rows=[{'score':.9},{'score':.6}]
        self.assertAlmostEqual(p.pool_value(rows),.5)
        self.assertAlmostEqual(p.pool_value(rows[:1]),.3)
        self.assertGreater(p.pool_value(rows),p.pool_value(rows[:1]))
        self.assertEqual(p.pool_value([]),0.)

    def test_fixed_capacity_monotone_for_every_removed_option(self):
        p=planner()
        for count in range(1,13):
            rows=[{'score':1-i/20} for i in range(count)]
            before=p.pool_value(rows)
            for index in range(count):
                self.assertLessEqual(p.pool_value(rows[:index]+rows[index+1:]),before+1e-12)
        self.assertAlmostEqual(p.pool_value([{'score':.9},{'score':.6},{'score':.3}]),.6)

    def test_side_selection_and_pool_cost_change_context_without_name_rules(self):
        p=planner();first=DraftState(first_side='blue')
        second=DraftState(first_side='red');second.apply('red','ban','OutsideCatalog')
        a=p.contextual(first,'blue')[0];b=p.contextual(second,'blue')[0]
        self.assertTrue(a['own_next_pick_before_enemy'])
        self.assertFalse(b['own_next_pick_before_enemy'])
        self.assertGreater(a['own_access_cost'],b['own_access_cost'])
        self.assertLess(a['contextual_score'],b['contextual_score'])

    def test_fearless_and_protected_champions_are_excluded_and_scarcity_changes(self):
        p=planner();s=DraftState(used_champions=['top_0','top_1','jng_0'])
        rows=p.contextual(s,'blue',protected=['mid_0'])
        self.assertFalse({r['champion']for r in rows}&{'top_0','top_1','jng_0','mid_0'})
        candidate=next(r for r in rows if r['champion']=='top_2')
        self.assertEqual(candidate['pool_impact']['enemy:top']['before_options'],10)
        self.assertEqual(candidate['fearless_locked_count'],3)

    def test_contextual_is_deterministic_serializable_and_not_live_state(self):
        p=planner();state=DraftState();before=deepcopy(state.as_dict())
        result=p.recommend(state,'blue');again=p.recommend(state,'blue')
        self.assertEqual(state.as_dict(),before)
        self.assertEqual([(r['champion'],r['ban_priority'])for r in result],[(r['champion'],r['ban_priority'])for r in again])
        json.dumps(result,allow_nan=False)
        state.apply('blue','ban','ChangedLater')
        self.assertEqual(result[0]['contextual_trace']['state']['history'],[])
        self.assertNotIn('search_trace',result[0])
        self.assertNotIn('branches',result[0])

    def test_unsupported_mode_and_wrong_turn_are_rejected(self):
        with self.assertRaises(ValueError):planner().recommend(DraftState(),'blue',mode='lookahead')
        with self.assertRaises(ValueError):planner().recommend(DraftState(),'red')
        with self.assertRaises(ValueError):ContextualBanPolicy(pool_top_k=0)
        with self.assertRaises(ValueError):ContextualBanPolicy(own_cost_weight=float('nan'))

    def test_filled_roles_are_not_ban_targets_and_target_role_is_respected(self):
        p=planner();s=DraftState();s.picks['red']['mid']='mid_0'
        rows=p.contextual(s,'blue',target_role='sup')
        self.assertTrue(rows)
        self.assertTrue(all(r['champion'].startswith('sup_')for r in rows))
        self.assertFalse(p.contextual(s,'blue',target_role='mid'))

    def test_score_matches_documented_one_step_pool_loss_and_trace_all_candidates(self):
        p=planner();rows=p.recommend(DraftState(),'blue')
        self.assertTrue(rows)
        for r in rows:
            self.assertAlmostEqual(r['ban_priority'],r['enemy_pool_loss']-r['own_access_cost'])
            self.assertIsNone(r['probability'])
            self.assertGreaterEqual(r['contextual_trace']['legal_candidates'],len(rows))
            self.assertEqual(r['contextual_trace']['mode'],'contextual')
