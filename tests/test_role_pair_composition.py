import sys
from pathlib import Path
import unittest
import pandas as pd

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from draft_meta import DraftMetaSnapshot,MetaPolicy


def tables():
    matches=[];players=[]
    for i in range(20):
        for side in ['Blue','Red']:
            champs=['T','J1' if i<10 else 'J2','M1' if i<10 else 'M2','A','S1' if i<16 else 'S2'] if side=='Blue' else ['OppT','OppJ','OppM','OppA','OppS']
            date='2026-11-01' if i<19 else '2026-11-02'
            matches.append(dict(gameid=f'g{i}',date=date,patch=16.2,league='WLDs',side=side,
                                teamname=side,firstPick=int(side=='Blue'),**{f'pick{n+1}':c for n,c in enumerate(champs)}))
            for role,c in zip(['top','jng','mid','bot','sup'],champs):
                players.append(dict(gameid=f'g{i}',date=date,side=side,teamname=side,position=role,
                                    champion=c,playername=role+side,result=int(side=='Blue')))
    return None,pd.DataFrame(matches),pd.DataFrame(players)


class RolePairTests(unittest.TestCase):
    def snapshot(self,t=None,**kwargs):return DraftMetaSnapshot(region='WLDS',policy=MetaPolicy(as_of=kwargs.get('as_of','2026-11-02')),tables=t or tables())

    def test_all_ten_role_pairs_and_same_team_only(self):
        s=self.snapshot()
        self.assertEqual(len(s.pair_totals),20) # ten undirected role pairs, both query directions
        self.assertEqual(s.pair_evidence('sup','S1','bot','A')['games'],16)
        self.assertEqual(s.pair_evidence('sup','OppS','bot','A')['games'],0)
        self.assertEqual(s.pair_evidence('mid','M1','jng','J1')['games'],10)
        self.assertEqual(s.pair_evidence('mid','M1','sup','J1')['games'],0)
        self.assertEqual(s.pair_evidence('top','T','jng','J2')['games'],10)

    def test_observed_association_beats_absent_pair_without_name_rules(self):
        s=self.snapshot()
        known=s.pair_evidence('sup','S1','bot','A')
        absent=s.pair_evidence('sup','OppS','bot','A')
        self.assertGreater(known['smoothed_lift'],1)
        self.assertLess(known['effective_lift'],known['smoothed_lift'])
        self.assertGreater(known['effective_lift'],1)
        self.assertLess(absent['smoothed_lift'],1)
        self.assertGreater(absent['effective_lift'],absent['smoothed_lift'])
        self.assertLess(absent['effective_lift'],1)
        self.assertEqual(absent['status'],'unobserved_pair')
        self.assertEqual(known['anchor_games'],20)
        self.assertEqual(known['co_pick_share'],.8)
        self.assertIsNone(known['causal_uplift'])
        self.assertLessEqual(known['co_pick_share_ci95_wilson'][0],.8)
        self.assertGreaterEqual(known['co_pick_share_ci95_wilson'][1],.8)

    def test_renaming_champions_does_not_change_pair_score(self):
        t=tables();s=self.snapshot(t)
        renamed=(None,t[1].replace({'A':'ExampleADC','S1':'ExampleSupport'}),t[2].replace({'A':'ExampleADC','S1':'ExampleSupport'}))
        b=self.snapshot(renamed)
        self.assertEqual(s.pair_evidence('sup','S1','bot','A')['smoothed_lift'],b.pair_evidence('sup','ExampleSupport','bot','ExampleADC')['smoothed_lift'])

    def test_enemy_evidence_uses_all_roles_and_never_counts_allies(self):
        s=self.snapshot()
        ev=s.enemy_evidence('mid','M1','top','OppT')
        self.assertEqual(ev['games'],10)
        self.assertEqual(ev['wins'],10)
        self.assertEqual(s.enemy_evidence('mid','M1','top','T')['games'],0)
        self.assertEqual(s.enemy_evidence('mid','M1','jng','OppJ')['games'],10)
        self.assertIsNone(ev['causal_uplift'])

    def test_sparse_unknown_and_time_cutoff_keep_distinct_evidence(self):
        s=self.snapshot()
        self.assertEqual(s.pair_evidence('sup','S2','bot','A')['status'],'sparse_pair')
        unknown=s.pair_evidence('sup','S1','bot','NeverSeen')
        self.assertEqual(unknown['status'],'insufficient_anchor_history')
        self.assertEqual(unknown['anchor_games'],0)
        early=self.snapshot(as_of='2026-11-01')
        self.assertEqual(early.pair_evidence('sup','S2','bot','A')['games'],3)
        self.assertEqual(early.pair_evidence('sup','S2','bot','A')['anchor_games'],19)


if __name__=='__main__':unittest.main()
