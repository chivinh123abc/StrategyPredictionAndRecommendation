from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/07_recommender'))
from draft_advisor import DraftAdvisor, AdvisorPolicy, ROLES
from simulate_draft_match import DraftState, draft_schedule, run_pro_tournament_draft_simulation, TEAM_PRESETS
from recommender_engine import RecommenderEngine


class DraftStateTests(unittest.TestCase):
    def test_order_depends_on_first_pick_and_has_twenty_actions(self):
        for first,second in [('blue','red'),('red','blue')]:
            order=draft_schedule(first)
            self.assertEqual(len(order),20)
            self.assertEqual(order[:6],[(s,'ban') for s in [first,second]*3])
            self.assertEqual(order[12:16],[(s,'ban') for s in [second,first,second,first]])
            self.assertEqual(order[16:],[(s,'pick') for s in [second,first,first,second]])
            for side in ['blue','red']:
                self.assertEqual(order.count((side,'pick')),5)
                self.assertEqual(order.count((side,'ban')),5)

    def test_invalid_turn_duplicates_and_occupied_roles_do_not_mutate(self):
        state=DraftState()
        with self.assertRaises(ValueError):state.apply('red','ban','A')
        self.assertEqual(state.history,[])
        state.apply('blue','ban','A')
        with self.assertRaises(ValueError):state.apply('red','ban','A')
        for i,(side,kind) in enumerate(state.schedule[1:6]):state.apply(side,kind,f'Ban{i}')
        state.apply('blue','pick','C','mid')
        state.apply('red','pick','D','mid')
        n=len(state.history)
        with self.assertRaises(ValueError):state.apply('red','pick','E','mid')
        self.assertEqual(len(state.history),n)
        state.swap('red','D','top')
        self.assertEqual(state.picks['red'],{'top':'D'})
        state.apply('red','pick','E','mid')
        state.swap('red','D','mid')
        self.assertEqual(state.picks['red'],{'top':'E','mid':'D'})


class DraftAdvisorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine=RecommenderEngine.load()
        cls.advisor=DraftAdvisor(db_path=cls.engine.pick_recommender.db_path)

    def test_context_evidence_components_and_exclusions(self):
        rows=self.advisor.recommend_picks('mid',{'jng':'Vi'},{'mid':'Azir'},
                                          {'Ahri'},'Faker',top_k=8,region='LCK')
        self.assertTrue(rows)
        for r in rows:
            self.assertNotIn(r['champion'],['Vi','Azir','Ahri'])
            self.assertIsNone(r['probability'])
            self.assertIn('content',r['score_components'])
            self.assertIn('matchup',r['score_components'])
            parts=r['score_components']
            base=[p for k,p in parts.items() if k!='composition']
            priority=sum(p['weight']*p['value'] for p in base)/sum(p['weight'] for p in base)
            factor=r['composition_lift']**parts.get('composition',{}).get('weight',0)
            expected=priority*factor/(1-priority+priority*factor)
            self.assertAlmostEqual(r['score'],expected)
        blind=self.advisor.recommend_picks('mid',{}, {},player_name='__unknown__',region='LCK')
        self.assertTrue(all('matchup' not in r['score_components'] and 'content' not in r['score_components'] for r in blind))

    def test_bans_use_only_unfilled_enemy_roles_and_legal_champions(self):
        rows=self.advisor.recommend_bans(TEAM_PRESETS['T1'],{'mid':'Azir'},
                                        {'jng':'Vi'},banned={'Ahri'},region='LCK',protected={'Jinx'})
        self.assertTrue(rows)
        for row in rows:
            self.assertNotIn(row['champion'],['Azir','Vi','Ahri','Jinx'])
            self.assertNotIn('mid',row['target_roles'])
            self.assertGreaterEqual(row['denial_loss'],0)
            self.assertIsNone(row['probability'])
        self.assertEqual(self.advisor.recommend_bans({},dict(zip(ROLES,['A','B','C','D','E'])),{}),[])

    def test_blue_interactive_filters_explanations_and_complete_draft(self):
        commands=iter(['why 1','999','mid','all','']+['']*20)
        with redirect_stdout(io.StringIO()) as capture:
            result=run_pro_tournament_draft_simulation('T1','GEN.G',region='LCK',
                   input_fn=lambda _:next(commands),engine=self.engine,advisor=self.advisor,allow_statistical_auto=True)
        self.assertTrue(result['complete'])
        self.assertIn('Số gợi ý không hợp lệ',capture.getvalue())
        self.assertEqual(len(result['history']),20)
        self.assertEqual(len(set(result['bans']['blue']+result['bans']['red']+
                                 list(result['picks']['blue'].values())+list(result['picks']['red'].values()))),20)
        self.assertTrue(any('content' in h['advice'].get('score_components',{}) for h in result['history']))

    def test_red_first_pick_interactive_and_session_persistence(self):
        with tempfile.TemporaryDirectory() as directory,redirect_stdout(io.StringIO()):
            path=Path(directory)/'draft.json'
            result=run_pro_tournament_draft_simulation('T1','GEN.G',region='LCK',user_side='red',
                       first_side='red',input_fn=lambda _:'',save_session=path,engine=self.engine,advisor=self.advisor,allow_statistical_auto=True)
            saved=json.loads(path.read_text(encoding='utf-8'))
        self.assertTrue(result['complete'])
        self.assertEqual(saved['history'],result['history'])
        self.assertEqual(result['history'][0]['side'],'red')
        self.assertEqual(set(result['picks']['blue']),set(ROLES))
        self.assertEqual(set(result['picks']['red']),set(ROLES))

    def test_eof_aborts_without_inventing_user_choice(self):
        def eof(_):raise EOFError
        with redirect_stdout(io.StringIO()):
            result=run_pro_tournament_draft_simulation(region='LCK',input_fn=eof,engine=self.engine,advisor=self.advisor)
        self.assertFalse(result['complete'])
        self.assertEqual(result['history'],[])

    def test_public_engine_wrapper_and_invalid_policy(self):
        self.assertTrue(self.engine.recommend_draft_picks('mid',{}, {},player_name='Faker',region='LCK'))
        with self.assertRaises(ValueError):AdvisorPolicy(weights={'meta':1})


if __name__=='__main__':unittest.main()
