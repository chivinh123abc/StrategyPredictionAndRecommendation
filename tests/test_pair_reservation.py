from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from pair_reservation import reserve_pairs,enemy_bans_before_next_pick
from simulate_draft_match import DraftState,needs_tactical_review
from simulate_fearless_series import first_selection_order


class Snapshot:
    def pair_evidence(self,role,champ,ally_role,ally,minimum):
        n=8 if champ in ['PartnerA','PartnerB'] or ally in ['PartnerA','PartnerB'] else 1
        return {'games':n,'winrate':.5,'ci95_wilson':[.2,.8],'effective_lift':1.2 if n==8 else .7}


class Advisor:
    policy=SimpleNamespace(min_games=5)
    def context(self,region):return Snapshot(),None,None


def setup(first='blue',own_role='sup',turn=11):
    s=DraftState(first_side=first);side=first;enemy='red' if side=='blue' else 'blue'
    s.history=[{} for _ in range(turn-1)]
    s.picks[side]={'mid':'AllyMid',own_role:'Anchor'}
    s.picks[enemy]={'bot':'EnemyBot','sup':'EnemySupport'}
    missing='bot' if own_role=='sup' else 'sup'
    rows=[{'champion':'Solo','role':'top','score':.9,'reasons':['original']},
          {'champion':'PartnerA','role':missing,'score':.7,'reasons':['original']},
          {'champion':'PartnerB','role':missing,'score':.6,'reasons':['original']},
          {'champion':'Sparse','role':missing,'score':.95,'reasons':['original']}]
    return s,side,rows


class PairReservationTests(unittest.TestCase):
    def test_two_bans_two_partners_secure_pair_without_changing_scores(self):
        s,side,rows=setup();before=deepcopy(rows)
        result=reserve_pairs(rows,Advisor(),s,side,'WLDS')
        chosen=next(r for r in result if r['champion']=='PartnerA')
        solo=next(r for r in result if r['champion']=='Solo')
        self.assertEqual(chosen['pair_reservation']['priority_tier'],0)
        self.assertEqual(solo['pair_reservation']['supported_partner_count'],2)
        self.assertEqual(solo['pair_reservation']['worst_case_partners_remaining'],0)
        self.assertEqual(chosen['score'],.7);self.assertEqual(rows,before)

    def test_consecutive_pick_means_no_urgent_promotion(self):
        s,side,rows=setup(turn=10)
        self.assertEqual(enemy_bans_before_next_pick(s,side),0)
        result=reserve_pairs(rows,Advisor(),s,side,'WLDS')
        self.assertFalse(any(r['pair_reservation']['priority_tier']==0 for r in result))

    def test_red_first_and_blue_first_have_same_risk_and_priority(self):
        outputs=[]
        for first in ['blue','red']:
            s,side,rows=setup(first)
            outputs.append([(r['champion'],r['pair_reservation']) for r in reserve_pairs(rows,Advisor(),s,side,'WLDS')])
        self.assertEqual(outputs[0],outputs[1])

    def test_symmetric_partner_role_and_locked_partner_excluded(self):
        s,side,rows=setup(own_role='bot');s.used_champions=['PartnerA']
        result=reserve_pairs(rows,Advisor(),s,side,'WLDS')
        info=next(r for r in result if r['champion']=='Solo')['pair_reservation']
        self.assertEqual(info['missing_role'],'sup')
        self.assertEqual([p['champion'] for p in info['supported_partners']],['PartnerB'])

    def test_enemy_bot_not_revealed_does_not_trigger_this_policy(self):
        s,side,rows=setup();enemy='red' if side=='blue' else 'blue';s.picks[enemy].pop('sup')
        self.assertEqual(reserve_pairs(rows,Advisor(),s,side,'WLDS'),rows)

    def test_sparse_completed_pair_requires_review_even_before_enemy_five(self):
        s,side,rows=setup();result=reserve_pairs(rows,Advisor(),s,side,'WLDS')
        chosen=next(r for r in result if r['champion']=='Sparse')
        self.assertTrue(needs_tactical_review(chosen,{'bot':'A','sup':'B'}))
        self.assertFalse(needs_tactical_review(chosen,{'bot':'A','sup':'B'},True))
        self.assertEqual(chosen['pair_reservation']['status'],'completed_insufficient_support')

    def test_first_selection_can_repeat_and_is_validated(self):
        order=['red','red','blue','blue','red']
        self.assertEqual(first_selection_order(5,order),order)
        for invalid in [['green'],['blue','red']]:
            with self.assertRaises(ValueError):first_selection_order(1,invalid)


if __name__=='__main__':unittest.main()
