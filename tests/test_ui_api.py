from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient

api=importlib.import_module('src.api.app')
ROOT=Path(__file__).resolve().parents[1]


class DraftApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client=TestClient(api.app)
        cls.names=[row['name'] for row in api.registry()['champions']]
        cls.db=ROOT/'data/database/lol_live_data.db'
        cls.before=hashlib.sha256(cls.db.read_bytes()).hexdigest()

    @classmethod
    def tearDownClass(cls):
        cls.client.close()
        assert hashlib.sha256(cls.db.read_bytes()).hexdigest()==cls.before

    def session(self):return api.Session().model_dump()

    def game(self,start=0,first='blue',turns=20):
        moves=[];picks={'blue':0,'red':0}
        for i,(side,kind) in enumerate(api.draft_schedule(first)[:turns]):
            role=api.ROLES[picks[side]] if kind=='pick' else None
            if kind=='pick':picks[side]+=1
            moves.append({'side':side,'action':kind,'champion':self.names[start+i],'role':role})
        return {'first_side':first,'history':moves,'swaps':[]}

    def test_catalog_health_and_static_ui_do_not_expose_project_files(self):
        self.assertEqual(self.client.get('/api/health').json()['pick_scoring'],'current')
        result=self.client.get('/api/catalog');self.assertEqual(result.status_code,200)
        self.assertGreater(len(result.json()['champions']),100)
        self.assertNotIn('RIOT_API_KEY',result.text)
        self.assertEqual(self.client.get('/.env').status_code,404)
        self.assertEqual(self.client.get('/data/database/lol_live_data.db').status_code,404)

    def test_view_uses_real_engine_and_only_public_advice(self):
        result=self.client.post('/api/draft/view',json={'session':self.session()})
        self.assertEqual(result.status_code,200,result.text)
        data=result.json()
        self.assertEqual((data['turn']['side'],data['turn']['action'],data['turn']['number']),('blue','ban',1))
        self.assertEqual(len(data['recommendations']),5)
        self.assertGreater(data['scope']['history_games'],0)
        self.assertNotIn('_puuid',result.text)
        self.assertNotIn('contextual_trace',result.text)
        self.assertTrue(all(row.get('reason') or row.get('reasons') for row in data['recommendations']))

    def test_snapshot_is_pinned_and_replays_identically(self):
        first=self.client.post('/api/draft/view',json={'session':self.session()}).json()
        self.assertIsNotNone(first['session']['settings']['as_of'])
        self.assertEqual(first['configuration']['contextual_version'],'fixed_capacity_v2')
        second=self.client.post('/api/draft/view',json={'session':first['session']}).json()
        self.assertEqual(first['recommendations'],second['recommendations'])
        self.assertEqual(first['session']['snapshot_id'],second['session']['snapshot_id'])
        first['session']['settings']['allow_statistical_auto']=True
        self.assertEqual(self.client.post('/api/draft/view',json={'session':first['session']}).status_code,200)

    def test_changed_snapshot_or_configuration_requires_new_session(self):
        first=self.client.post('/api/draft/view',json={'session':self.session()}).json()
        invalid=deepcopy(first['session']);invalid['snapshot_id']='0'*64
        self.assertEqual(self.client.post('/api/draft/view',json={'session':invalid}).status_code,409)
        first['session']['settings']['ban_strategy']='legacy'
        self.assertEqual(self.client.post('/api/draft/view',json={'session':first['session']}).status_code,409)

    def test_changed_source_cannot_reuse_stale_advisor_cache(self):
        with patch.object(api,'source_fingerprint',return_value='0'*64):
            result=self.client.post('/api/draft/view',json={'session':self.session()})
        self.assertEqual(result.status_code,409)
        self.assertIn('khởi động lại API',result.json()['detail'])

    def test_duplicate_wrong_turn_and_forged_board_are_rejected(self):
        session=self.session();session['current']=self.game(turns=1)
        result=self.client.post('/api/draft/action',json={'session':session,'champion':self.names[0]})
        self.assertEqual(result.status_code,400)
        invalid=deepcopy(session);invalid['current']['history'].append({'side':'blue','action':'ban','champion':self.names[1],'role':None})
        self.assertEqual(self.client.post('/api/draft/view',json={'session':invalid}).status_code,400)
        invalid=deepcopy(session);invalid['current']['picks']={'blue':{'top':'invented'}}
        self.assertEqual(self.client.post('/api/draft/view',json={'session':invalid}).status_code,422)
        session['settings']['pick_scoring']='simple'
        self.assertEqual(self.client.post('/api/draft/view',json={'session':session}).status_code,422)

    def test_manual_pick_swap_and_replay_keep_flex_role(self):
        session=self.session();session['current']=self.game(turns=6)
        result=self.client.post('/api/draft/action',json={'session':session,'champion':self.names[15],'role':'mid'})
        self.assertEqual(result.status_code,200,result.text)
        session=result.json()['session']
        result=self.client.post('/api/draft/swap',json={'session':session,'side':'blue','champion':self.names[15],'target_role':'top'})
        self.assertEqual(result.status_code,200,result.text)
        data=result.json();self.assertEqual(data['games'][-1]['picks']['blue'],{'top':self.names[15]})
        replay=self.client.post('/api/draft/view',json={'session':data['session']})
        self.assertEqual(replay.json()['games'][-1]['picks']['blue'],{'top':self.names[15]})

    def test_auto_missing_evidence_requires_explicit_test_flag(self):
        session=self.session();session['current']=self.game(turns=19)
        row={'champion':self.names[30],'role':'sup','review_required':True}
        with patch.object(api,'recommend',side_effect=lambda state,*a,**kw:[] if state.complete else [row]):
            result=self.client.post('/api/draft/action',json={'session':session,'auto':True})
            self.assertEqual(result.status_code,409)
            self.assertEqual(len(session['current']['history']),19)
            session['settings']['allow_statistical_auto']=True
            result=self.client.post('/api/draft/action',json={'session':session,'auto':True})
            self.assertEqual(result.status_code,200,result.text)
            self.assertTrue(result.json()['games'][-1]['complete'])

    def test_five_game_replay_derives_fearless_locks_and_rejects_reuse(self):
        session=self.session();games=[self.game(start=i*20,first='blue' if i%2==0 else 'red') for i in range(5)]
        session['completed']=games[:4];session['current']=games[4]
        result=self.client.post('/api/draft/view',json={'session':session})
        self.assertEqual(result.status_code,200,result.text)
        data=result.json();self.assertTrue(data['series_complete'])
        self.assertEqual([len(g['used_champions']) for g in data['games']],[0,10,20,30,40])
        session['current']['history'][0]['champion']=games[0]['history'][6]['champion']
        self.assertEqual(self.client.post('/api/draft/view',json={'session':session}).status_code,400)
        session=self.session();session['completed']=[self.game(turns=2)]
        self.assertEqual(self.client.post('/api/draft/view',json={'session':session}).status_code,400)

    def test_history_explanation_does_not_invent_score_for_manual_unknown_role(self):
        selected=next(c['name'] for c in api.registry()['champions'] if c['roles'] and 'jng' not in c['roles'])
        bans=[name for name in self.names if name!=selected][:6]
        session=self.session();session['current']=self.game(turns=6)
        for move,name in zip(session['current']['history'],bans):move['champion']=name
        session['current']['history'].append({'side':'blue','action':'pick','champion':selected,'role':'jng'})
        result=self.client.post('/api/draft/explain',json={'session':session,'game_index':0,'turn':7})
        self.assertEqual(result.status_code,200,result.text)
        self.assertIsNone(result.json()['advice']);self.assertTrue(result.json()['notice'])

    def test_nonfinite_measurements_are_null_in_json(self):
        data=api.clean({'games':np.int64(3),'missing':np.nan,'value':np.float64(-120)})
        json.dumps(data,allow_nan=False)
        self.assertIsNone(data['missing']);self.assertEqual(data['value'],-120)

    def bot_window_session(self,mirror=False):
        session=self.session();session['settings']['as_of']='2026-11-24'
        turns=[('blue','ban','Qiyana',None),('red','ban','Nocturne',None),
            ('blue','ban','Olaf',None),('red','ban','Vi',None),('blue','ban','Ezreal',None),
            ('red','ban','Lee Sin',None),('blue','pick','Cassiopeia','mid'),
            ('red','pick','Renata Glasc','sup'),('red','pick','Kalista','bot'),
            ('blue','pick','Nautilus','sup')]
        if mirror:
            session['settings'].update(blue_team='Gen.G',red_team='T1')
            session['current']['first_side']='red'
        session['current']['history']=[{'side':('red' if side=='blue' else 'blue') if mirror else side,
            'action':kind,'champion':champ,'role':role} for side,kind,champ,role in turns]
        return session

    def test_real_pair_window_secures_supported_adc_before_bans(self):
        session=self.bot_window_session()
        result=self.client.post('/api/draft/view',json={'session':session})
        self.assertEqual(result.status_code,200,result.text)
        row=result.json()['recommendations'][0]
        self.assertEqual(row['role'],'bot')
        self.assertEqual(row['pair_reservation']['status'],'secure_now')
        self.assertEqual(row['pair_reservation']['enemy_bans_before_next_own_pick'],2)
        self.assertGreaterEqual(row['pair_reservation']['pair_evidence']['games'],5)

    def test_real_pair_window_mirrors_with_red_first_selection(self):
        output=[]
        for mirror in [False,True]:
            result=self.client.post('/api/draft/view',json={'session':self.bot_window_session(mirror)})
            self.assertEqual(result.status_code,200,result.text)
            output.append([(r['champion'],r.get('role'),r.get('pair_reservation')) for r in result.json()['recommendations']])
        self.assertEqual(output[0],output[1])

    def test_role_filter_warns_instead_of_returning_adc_for_top(self):
        result=self.client.post('/api/draft/view',json={'session':self.bot_window_session(),'only_role':'top'})
        self.assertEqual(result.status_code,200,result.text)
        self.assertTrue(all(r['role']=='top' for r in result.json()['recommendations']))
        self.assertEqual(result.json()['recommendations'][0]['pair_reservation']['status'],'at_risk')

    def test_same_team_can_have_first_selection_two_games_in_a_row(self):
        session=self.session();session['completed']=[self.game(first='red')]
        session['current']['first_side']='red'
        result=self.client.post('/api/draft/view',json={'session':session})
        self.assertEqual(result.status_code,200,result.text)
        self.assertEqual(result.json()['turn']['side'],'red')
        self.assertEqual(len(result.json()['games'][-1]['used_champions']),10)

    def late_top_session(self):
        session=self.bot_window_session()
        tail=[('blue','pick','Jhin','bot'),('red','pick','Orianna','mid'),
            ('red','ban','Jayce',None),('blue','ban','Jarvan IV',None),
            ('red','ban','Rumble',None),('blue','ban','Pantheon',None),
            ('red','pick','Ambessa','top'),('blue','pick','Wukong','jng')]
        session['current']['history'] += [{'side':s,'action':a,'champion':c,'role':r} for s,a,c,r in tail]
        return session

    def test_manual_pick_without_role_uses_next_popular_free_position(self):
        session=self.bot_window_session();session['current']['history']=session['current']['history'][:9]
        view=self.client.post('/api/draft/view',json={'session':session}).json()
        occupied=view['games'][-1]['picks']['blue']
        expected=next(p['role'] for p in view['role_preferences']['Galio'] if p['role'] not in occupied)
        self.assertEqual(view['role_preferences']['Galio'][0]['role'],'mid')
        result=self.client.post('/api/draft/action',json={'session':view['session'],'champion':'Galio'})
        self.assertEqual(result.status_code,200,result.text)
        self.assertEqual(result.json()['session']['current']['history'][-1]['role'],expected)
        self.assertEqual(result.json()['games'][-1]['picks']['blue']['mid'],'Cassiopeia')

    def test_known_top_opponent_does_not_wait_for_all_five_enemy_picks(self):
        session=self.late_top_session()
        view=self.client.post('/api/draft/view',json={'session':session}).json()
        self.assertEqual(len(view['games'][-1]['picks']['red']),4)
        self.assertEqual(view['recommendations'][0]['champion'],'Gnar')
        self.assertEqual(view['recommendations'][0]['lane_review']['games'],6)
        galio=next(r for r in view['recommendations'] if r['champion']=='Galio')
        self.assertEqual(galio['lane_review']['games'],0)
        self.assertTrue(api.needs_tactical_review(galio,view['games'][-1]['picks']['red']))
        # Force the candidate only to exercise the HTTP auto-finalization guard.
        with patch.object(api,'recommend',return_value=[galio]):
            result=self.client.post('/api/draft/action',json={'session':view['session'],'auto':True})
        self.assertEqual(result.status_code,409)

    def test_high_raw_matchup_winrate_does_not_hide_two_game_sample(self):
        view=self.client.post('/api/draft/view',json={'session':self.late_top_session()}).json()
        renekton=next(r for r in view['recommendations'] if r['champion']=='Renekton')
        self.assertEqual(renekton['lane_review']['games'],2)
        self.assertEqual(renekton['lane_review']['winrate'],1.)
        self.assertTrue(renekton['lane_review']['requires_review'])
        order=[r['champion'] for r in view['recommendations']]
        self.assertLess(order.index('Gnar'),order.index('Renekton'))
        insufficient=[r for r in view['recommendations'] if r['lane_review']['requires_review']]
        self.assertEqual([r['ranking_score'] for r in insufficient],sorted([r['ranking_score'] for r in insufficient],reverse=True))


if __name__=='__main__':unittest.main()
