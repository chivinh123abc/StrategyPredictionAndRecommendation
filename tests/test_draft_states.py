import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from draft_states import game_states,build_states,state_features
from opponent_model import split_series,feasible_roles,OpponentModel,public_simulation_state
from simulate_draft_match import DraftState
from draft_advisor import DraftAdvisor,AdvisorPolicy
from draft_meta import MetaPolicy


def rows(number=1):
    return pd.DataFrame([dict(gameid=f'g{number}',date=f'2026-11-{number:02}T10:00:00Z',game=number,
        side=side,firstPick=int(side=='Blue'),teamname=side,league='WLDS',year=2026,split='',patch=16.2,
        **{f'pick{i}':f'Game{number}_{side}_Pick{i}'for i in range(1,6)},
        **{f'ban{i}':f'{side}_Ban{i}'for i in range(1,6)}) for side in ['Blue','Red']])


class DraftStateDatasetTests(unittest.TestCase):
    def test_pre_action_history_and_mask_contain_no_future_choice(self):
        states,used=game_states(rows(),[],'series1')
        self.assertEqual(len(states),20);self.assertEqual(len(used),10)
        for i,s in enumerate(states):
            self.assertEqual(len(s['own_picks']+s['enemy_picks']+s['own_bans']+s['enemy_bans']),i)
            self.assertNotIn(s['target_champion'],s['unavailable'])
            self.assertNotIn('target_champion',state_features(s))
        a=state_features(states[7]);changed={**states[7],'target_champion':'FakeFuture','result':1,'final_roles':{'top':'FakeFuture'}}
        self.assertEqual(a,state_features(changed))

    def test_fearless_carries_picks_but_does_not_carry_bans(self):
        _,used=game_states(rows(),[],'s')
        second,_=game_states(rows(2),used,'s')
        self.assertEqual(len(second[0]['used_champions']),10)
        self.assertNotIn('Blue_Ban1',second[0]['unavailable'])
        self.assertNotIn(second[0]['target_champion'],second[0]['unavailable'])

    def test_rejects_ambiguous_prefix_or_any_repeated_fearless_action(self):
        data,manifest=build_states(rows(2))
        self.assertEqual(data,[]);self.assertTrue(manifest['rejected_games'])
        a=rows();b=rows(2);b.loc[b.side.eq('Blue'),'pick1']=a.loc[a.side.eq('Red'),'pick1'].iloc[0]
        data,manifest=build_states(pd.concat([a,b],ignore_index=True))
        self.assertEqual(data,[]);self.assertEqual(len(manifest['rejected_games']),2)

    def test_series_split_is_disjoint_and_chronological(self):
        states=[]
        for i in range(20):
            states.append({'series_id':f's{i//2}','gameid':f'g{i}','date':f'2026-01-{i+1:02}T00:00:00Z'})
        parts=split_series(states)
        for a,b in [('train','validation'),('train','test'),('validation','test')]:
            self.assertFalse({s['series_id']for s in parts[a]}&{s['series_id']for s in parts[b]})
            self.assertFalse({s['gameid']for s in parts[a]}&{s['gameid']for s in parts[b]})
        self.assertLess(max(s['date']for s in parts['train']),min(s['date']for s in parts['validation']))

    def test_observed_role_feasibility_does_not_know_final_roles(self):
        roles={'Support':{'sup'},'OtherSupport':{'sup'},'Carry':{'bot'},'Flex':{'mid','sup'}}
        self.assertFalse(feasible_roles(['Support','OtherSupport'],roles))
        self.assertTrue(feasible_roles(['Support','Flex','Carry'],roles))
        self.assertTrue(feasible_roles(['Support','Unknown'],roles))

    def test_model_mask_rejects_prior_picks_bans_and_filled_roles(self):
        m=OpponentModel();m.classes=np.array(['Support','OtherSupport','Carry','Locked','Banned'])
        m.role_catalog={'Support':{'sup'},'OtherSupport':{'sup'},'Carry':{'bot'}}
        m.action_classes={'pick':set(m.classes)}
        s={'action':'pick','own_picks':['Support'],'enemy_picks':[],'used_champions':['Locked'],
           'own_bans':['Banned'],'enemy_bans':[]}
        self.assertEqual(m.allowed(s).tolist(),[False,False,True,False,False])
        ranked=m.rank(s,np.array([.9,.08,.01,.005,.005]))
        self.assertEqual([r['champion']for r in ranked],['Carry'])
        self.assertAlmostEqual(ranked[0]['next_action_probability'],1.)

    def test_live_forecast_state_does_not_include_action_not_yet_taken(self):
        s=DraftState()
        for i,(side,action) in enumerate(s.schedule[:6]):s.apply(side,action,f'Ban{i}')
        forecast=public_simulation_state(s,{'blue':'A','red':'B'},
                    {'requested_as_of':'2026-11-13','dataset_patch':'16.20'},'WLDS')
        s.apply('blue','pick','FutureChoice','mid')
        self.assertEqual(forecast['own_picks'],[])
        self.assertNotIn('FutureChoice',forecast['unavailable'])
        self.assertEqual(forecast['slot'],'F_pick1')

    def test_replay_before_training_cutoff_is_refused(self):
        model=OpponentModel();model.train_through='2026-10-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'cutoff'):
            model.rank({'date':'2026-09-01T00:00:00Z'})

    def test_other_enemy_roles_change_context_without_champion_specific_rules(self):
        class Snapshot:
            def enemy_evidence(self,role,champ,enemy_role,enemy):
                return {'games':20,'winrate':.8 if enemy=='Positive' else .2}
        advisor=object.__new__(DraftAdvisor);advisor.policy=AdvisorPolicy();advisor.meta_policy=MetaPolicy()
        positive=advisor.evaluate_enemy_context('jng','Candidate',{'mid':{'Positive':1.}},Snapshot(),.5,1)
        negative=advisor.evaluate_enemy_context('jng','Candidate',{'mid':{'Negative':1.}},Snapshot(),.5,1)
        self.assertGreater(positive[0],.5);self.assertLess(negative[0],.5)
        self.assertEqual(positive[2],1.)

