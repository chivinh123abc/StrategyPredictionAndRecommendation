"""Temporal and draft evidence safeguards, independent of champion tier opinions."""
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys
import unittest
import pandas as pd

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from draft_meta import DraftMetaSnapshot,MetaPolicy,patch_code
from draft_advisor import DraftAdvisor
from simulate_draft_match import DraftState,run_pro_tournament_draft_simulation


def frames():
    matches=[];players=[]
    for game,date,patch in [('old','2025-08-20',15.16),('earlier','2026-08-10',16.15),
                             ('target','2026-08-31',16.16),('future','2026-09-15',16.18)]:
        for side in range(2):
            champs=[f'{r}{side}' for r in ['top','jng','mid','bot','sup']]
            matches.append(dict(gameid=game,date=date,patch=patch,league='LCK',teamname=f'Team{side}',
                                firstPick=1-side,**{f'pick{i+1}':c for i,c in enumerate(champs)},
                                **{f'ban{i}':'OldOnly' if game=='earlier' else f'Ban{i}' for i in range(1,6)}))
            for role,c in zip(['top','jng','mid','bot','sup'],champs):
                players.append(dict(gameid=game,date=date,position=role,champion=c,
                                    teamname=f'Team{side}',playername=f'{game}_{role}',result=1-side))
    return None,pd.DataFrame(matches),pd.DataFrame(players)


class SnapshotTests(unittest.TestCase):
    def snapshot(self,**kwargs):return DraftMetaSnapshot(region='LCK',policy=MetaPolicy(**kwargs),tables=frames())

    def test_cutoff_window_season_and_roster_do_not_see_future(self):
        s=self.snapshot(as_of='2026-08-31')
        self.assertEqual(set(s.matches.gameid),{'earlier','target'})
        self.assertEqual(s.target_patch,'16.16')
        self.assertEqual(s.roster('Team0')['gameid'],'target')
        self.assertFalse(s.players.playername.str.startswith('future').any())
        narrow=self.snapshot(as_of='2026-08-31',lookback_days=10)
        self.assertEqual(set(narrow.matches.gameid),{'target'})

    def test_explicit_patch_missing_is_rejected_not_synthesized(self):
        with self.assertRaises(ValueError):self.snapshot(as_of='2026-08-31',patch='26.23')
        s=self.snapshot(as_of='2026-09-30',patch='16.15')
        self.assertEqual(set(s.matches.gameid),{'earlier'})

    def test_decay_presence_counts_once_per_game_and_patch_activity(self):
        s=self.snapshot(as_of='2026-08-31')
        self.assertAlmostEqual(s.game_weights['earlier'],.5)
        self.assertAlmostEqual(s.presence['OldOnly'],1/3)
        self.assertEqual(s.patch_role_counts[('mid','mid0')],1)
        self.assertAlmostEqual(s.presence['mid0'],1)
        self.assertFalse(s.eligible('mid','OldOnly',1))

    def test_observed_first_selection_is_independent_of_color(self):
        s=self.snapshot(as_of='2026-08-31')
        self.assertGreater(s.slot_priority('F1','top','top0'),s.slot_priority('S1','top','top0'))
        self.assertEqual(patch_code(16.2),'16.20')
        self.assertEqual(patch_code(16.02),'16.02')

    def test_flex_inference_ignores_provisional_enemy_role_keys(self):
        class Snapshot:
            def role_probabilities(self,champ):
                return {'top':.5,'mid':.5} if champ=='Flex' else {'mid':1.}
        advisor=object.__new__(DraftAdvisor)
        a=advisor.infer_enemy_roles({'jng':'Flex','sup':'Mage'},Snapshot())
        b=advisor.infer_enemy_roles({'top':'Flex','mid':'Mage'},Snapshot())
        self.assertEqual(a,b)
        self.assertEqual(a['top'],{'Flex':1.})
        self.assertEqual(a['mid'],{'Mage':1.})

    def test_previous_game_champions_are_unavailable(self):
        s=DraftState(used_champions=['Used'])
        with self.assertRaises(ValueError):s.apply('blue','ban','Used')
        self.assertEqual(s.history,[])

    def test_live_freshness_guard_refuses_stale_snapshot(self):
        with redirect_stdout(io.StringIO()),self.assertRaisesRegex(ValueError,'cũ'):
            run_pro_tournament_draft_simulation(region='LCK',interactive=False,
                                               meta_policy=MetaPolicy(as_of='2026-11-23'),max_data_age_days=14)


if __name__=='__main__':unittest.main()
