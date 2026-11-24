import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/01_data_pipeline'))
from rank_lake import RankLake, exclusive_writer
from rank_eligibility import read_policy
from ranked_matchups import RiotClient,RiotError
from update_rank_evidence import process_job,fetch_snapshot,discover_seed,next_job,bootstrap
from rank_matchup_tables import aggregate,export_tables
from test_ranked_matchups import fixture


class RankLakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.policy=read_policy(ROOT/'src/config/draft_modes.json')
        self.lake=RankLake(self.base/'evidence.db',self.policy)
        self.d,self.t=fixture()
        self.at=datetime.now(timezone.utc)
        self.d['info']['gameStartTimestamp']=int((self.at-timedelta(hours=1)).timestamp()*1000)
        for p in self.d['info']['participants']:
            p['puuid']=f'private-{p["participantId"]}';p['championId']=p['participantId']
        self.raw=self.base/'raw'

    def tearDown(self):
        self.lake.close();self.tmp.cleanup()

    def job(self):
        self.lake.enqueue('KR_123','kr','asia')
        return self.lake.db.execute('SELECT * FROM jobs WHERE match_id=?',('KR_123',)).fetchone()

    def client(self,interrupt_timeline=False):
        client=Mock()
        def get(host,path,params=None):
            if '/entries/by-puuid/' in path:
                return [{'queueType':'RANKED_SOLO_5x5','tier':'MASTER','rank':'I','leaguePoints':0}]
            if path.endswith('/timeline'):
                if interrupt_timeline: raise RiotError('budget',reason_code='request_budget_exhausted')
                return self.t
            return self.d
        client.get.side_effect=get
        return client

    def test_canonical_database_destination_refused(self):
        with self.assertRaisesRegex(ValueError,'canonical'):
            RankLake(ROOT/'data/database/lol_live_data.db',self.policy)

    def test_queue_identity_and_atomic_ingestion(self):
        job=self.job()
        self.assertEqual(self.lake.enqueue('KR_123','kr','asia'),0)
        with self.assertRaises(ValueError):
            self.lake.persist_result('KR_123',{'status':'accepted'},self.at.isoformat(),[{}]*9)
        self.assertEqual(self.lake.counts()['pending'],1)
        self.assertEqual(self.lake.counts()['accepted_observations'],0)

    def test_policy_mixing_refused(self):
        other=copy.deepcopy(self.policy);other['snapshot_collection']['max_match_age_hours']=48
        with self.assertRaisesRegex(ValueError,'policy changed'):
            RankLake(self.base/'evidence.db',other)

    def test_exclusive_writer_lock_and_release(self):
        lock=self.base/'other.db'
        with exclusive_writer(lock):
            with self.assertRaises(RuntimeError):
                with exclusive_writer(lock): pass
        with exclusive_writer(lock): pass

    def test_tier_cache_preserves_actual_observation_timestamp(self):
        c=self.client();p=self.d['info']['participants'][0]
        with patch('update_rank_evidence.now',return_value=self.at):
            one,fresh=fetch_snapshot(self.lake,c,'kr',p,self.at.timestamp()-100,self.raw)
        with patch('update_rank_evidence.now',return_value=self.at+timedelta(seconds=30)):
            two,fresh2=fetch_snapshot(self.lake,c,'kr',p,self.at.timestamp()-100,self.raw)
        self.assertTrue(fresh);self.assertFalse(fresh2)
        self.assertEqual(one['observed_at'],two['observed_at'])
        self.assertEqual(c.get.call_count,1)

    def test_cache_refetches_for_newer_match_end(self):
        c=self.client();p=self.d['info']['participants'][0]
        with patch('update_rank_evidence.now',return_value=self.at):
            fetch_snapshot(self.lake,c,'kr',p,self.at.timestamp()-100,self.raw)
        with patch('update_rank_evidence.now',return_value=self.at+timedelta(seconds=30)):
            _,fresh=fetch_snapshot(self.lake,c,'kr',p,self.at.timestamp()+10,self.raw)
        self.assertTrue(fresh);self.assertEqual(c.get.call_count,2)

    def test_timeline_interruption_resumes_even_after_recency_window(self):
        c=self.client(True)
        with patch('update_rank_evidence.now',return_value=self.at):
            with self.assertRaises(RiotError): process_job(self.lake,c,self.job(),self.policy,self.raw)
        job=self.job()
        self.assertEqual(job['status'],'accepted')
        self.assertIsNotNone(job['evidence_json'])
        self.assertEqual(self.lake.counts()['accepted_observations'],0)
        later=Mock();later.get.return_value=self.t
        with patch('update_rank_evidence.now',return_value=self.at+timedelta(days=2)):
            status,fresh=process_job(self.lake,later,job,self.policy,self.raw)
        self.assertEqual(status,'accepted');self.assertEqual(fresh,0)
        self.assertEqual(later.get.call_count,1)
        self.assertTrue(later.get.call_args.args[1].endswith('/timeline'))
        self.assertEqual(self.lake.counts()['accepted_observations'],10)

    def test_repeated_processing_cannot_duplicate_observations(self):
        c=self.client()
        with patch('update_rank_evidence.now',return_value=self.at):
            process_job(self.lake,c,self.job(),self.policy,self.raw)
            process_job(self.lake,c,self.job(),self.policy,self.raw)
        self.assertEqual(self.lake.counts()['accepted_observations'],10)

    def test_seed_pagination_and_duplicate_ids(self):
        self.lake.add_seed('kr','seed','CHALLENGER','fixture',self.at.isoformat())
        self.lake.add_seed('euw1','other','CHALLENGER','fixture',self.at.isoformat())
        c=Mock();c.get.return_value=[f'KR_{i}' for i in range(100)]
        self.assertTrue(discover_seed(self.lake,c,{'kr':'asia'},self.policy))
        self.assertEqual(c.get.call_args.args[0],'asia')
        self.assertEqual(c.get.call_args.args[2]['count'],100)
        self.assertIn('startTime',c.get.call_args.args[2])
        self.assertEqual(self.lake.counts()['pending'],100)
        seed=self.lake.db.execute("SELECT page_start FROM seeds WHERE platform='kr'").fetchone()[0]
        self.assertEqual(seed,100)
        c.get.return_value=[]
        discover_seed(self.lake,c,{'kr':'asia'},self.policy)
        self.assertEqual(self.lake.counts()['pending'],100)

    def test_session_deadline_checked_before_http(self):
        transport=Mock()
        c=RiotClient('dummy',session=transport,deadline=time.monotonic()-1)
        with self.assertRaises(RiotError) as err: c.get('kr','/fixture')
        self.assertEqual(err.exception.reason_code,'session_time_limit')
        transport.get.assert_not_called()

    def test_raw_detail_survives_crash_before_sql_checkpoint(self):
        path=self.raw/'matches/KR_123.match.json';path.parent.mkdir(parents=True)
        path.write_text(json.dumps(self.d),encoding='utf-8')
        c=self.client()
        with patch('update_rank_evidence.now',return_value=self.at):
            process_job(self.lake,c,self.job(),self.policy,self.raw)
        self.assertEqual(self.lake.counts()['accepted_observations'],10)
        self.assertFalse(any(call.args[1].endswith('/KR_123') for call in c.get.call_args_list))
        self.assertEqual(self.job()['detail_fetched_at'],self.at.isoformat())

    def test_empty_export_has_readable_headers(self):
        out=self.base/'empty'
        summary=export_tables(self.lake,out)
        self.assertEqual(summary['games_with_observations'],0)
        self.assertTrue(pd.read_csv(out/'observations.csv').empty)

    def test_export_keeps_sparse_rows_without_private_ids(self):
        with patch('update_rank_evidence.now',return_value=self.at):
            process_job(self.lake,self.client(),self.job(),self.policy,self.raw)
        out=self.base/'report';s=export_tables(self.lake,out)
        self.assertEqual(s['games_with_observations'],1)
        self.assertEqual(s['matchup_rows'],10)
        self.assertEqual(s['supported_matchups'],0)
        table=pd.read_csv(out/'all_matchups.csv')
        self.assertTrue(table.gold_diff_15_mean_ci95_low.isna().all())
        text='\n'.join(p.read_text(encoding='utf-8-sig') for p in out.iterdir())
        self.assertNotIn('private-',text)
        self.assertNotIn('_puuid',text)

    def test_winrate_and_gold_rankings_are_separate(self):
        rows=[]
        for cid,win,gold in [(1,1,-1000),(2,0,1000)]:
            for i in range(5):
                rows.append(dict(platform='KR',queue=420,patch='16.23',tier_floor='MASTER',role='jng',
                    champion_id=cid,opponent_id=99,champion=f'c{cid}',opponent='enemy',
                    match_id=f'{cid}-{i}',team_id=100,win=win,_puuid=f'a{i}',_enemy_puuid=f'b{i}',gold_diff_15=gold))
        table=aggregate(pd.DataFrame(rows))
        self.assertEqual(table.sort_values('winrate',ascending=False).iloc[0].champion_id,1)
        self.assertEqual(table.sort_values('gold_diff_15_mean',ascending=False).iloc[0].champion_id,2)
        self.assertEqual(table[table.champion_id.eq(1)].iloc[0].early_status,'observed_early_disadvantage')
        self.assertTrue(table.win_ci95_high.gt(table.win_ci95_low).all())


    def test_pooled_reversal_and_duplicate_counts(self):
        rows=[]
        for patch_name,platform,gold in [('16.22','KR',300),('16.23','EUW1',-100)]:
            for i in range(5):
                rows.append(dict(platform=platform,queue=420,patch=patch_name,tier_floor='MASTER',role='mid',
                    champion_id=1,opponent_id=2,champion='A',opponent='B',match_id=f'{platform}_{i}',
                    team_id=100,win=i%2,_puuid=f'p{i}',_enemy_puuid=f'e{i}',gold_diff_15=gold))
        frame=pd.DataFrame(rows+rows)
        self.assertEqual(len(aggregate(frame)),2)
        pooled=aggregate(frame,pooled=True,target_games=9).iloc[0]
        self.assertEqual(pooled.games,10)
        self.assertEqual(pooled.gold_diff_15_mean,100)
        self.assertEqual(pooled.patch_count,2)
        self.assertEqual(pooled.platform_count,2)
        self.assertEqual(pooled.gd15_patch_direction,'mixed_directions')
        self.assertTrue(pooled.target_reached)
        self.assertEqual(pooled.games_remaining,0)
        other=pd.DataFrame([dict(rows[0],match_id='other',tier_floor='DIAMOND')])
        self.assertEqual(len(aggregate(pd.concat([frame,other]),pooled=True)),2)

    def test_pooled_single_patch_does_not_claim_stability(self):
        with patch('update_rank_evidence.now',return_value=self.at):
            process_job(self.lake,self.client(),self.job(),self.policy,self.raw)
        out=self.base/'pooled'
        summary=export_tables(self.lake,out,target_games=2000)
        p=pd.read_csv(out/'pooled_all_matchups.csv')
        self.assertTrue(p.gd15_patch_direction.eq('insufficient_patch_evidence').all())
        self.assertTrue(p.games_remaining.eq(1999).all())
        self.assertEqual(summary['pooled_matchups_at_target'],0)
        self.assertNotIn('_puuid',(out/'pooled_all_matchups.csv').read_text(encoding='utf-8-sig'))
        self.assertEqual(len(pd.read_csv(out/'matchup_collection_progress.csv')),10)

    def test_platform_rotation_discovers_other_region_before_draining_backlog(self):
        self.lake.enqueue('KR_1','kr','asia')
        self.lake.enqueue('KR_2','kr','asia')
        self.lake.add_seed('euw1','europe-seed','CHALLENGER','fixture',self.at.isoformat())
        client=Mock();client.get.return_value=['EUW1_1']
        routes={'kr':'asia','euw1':'europe'}
        first=next_job(self.lake,client,routes,self.policy)
        self.assertEqual(first['platform'],'kr')
        second=next_job(self.lake,client,routes,self.policy)
        self.assertEqual(second['platform'],'euw1')
        self.assertEqual(client.get.call_args.args[0],'europe')
        self.assertEqual(self.lake.meta('scheduler:last_platform'),'euw1')
        third=next_job(self.lake,client,routes,self.policy)
        self.assertEqual(third['platform'],'kr')

    def test_default_export_has_no_fixed_quota_or_invented_ugg_parity(self):
        with patch('update_rank_evidence.now',return_value=self.at):
            process_job(self.lake,self.client(),self.job(),self.policy,self.raw)
        out=self.base/'no_quota';summary=export_tables(self.lake,out)
        self.assertIsNone(summary['target_games_per_matchup'])
        self.assertIsNone(summary['pooled_matchups_at_target'])
        self.assertFalse(summary['ugg_coverage_parity_verified'])
        progress=pd.read_csv(out/'matchup_collection_progress.csv')
        self.assertTrue(progress[['target_games','games_remaining','target_reached']].isna().all().all())
        self.assertTrue(progress.reference_status.eq('not_loaded').all())
        self.assertEqual(int(progress.games.sum()),10)

    def test_league_list_membership_is_archived_and_reused_with_original_time(self):
        client=Mock()
        def get(host,path,params=None):
            tier=('GRANDMASTER' if '/grandmasterleagues/' in path else 'CHALLENGER' if '/challengerleagues/' in path else 'MASTER')
            return {'tier':tier,'queue':'RANKED_SOLO_5x5','entries':[{'puuid':f'private-{tier}','rank':'I','leaguePoints':42}]}
        client.get.side_effect=get
        with patch('update_rank_evidence.now',return_value=self.at):
            bootstrap(self.lake,client,['kr'],self.raw)
        self.assertEqual(client.get.call_count,3)
        s=self.lake.snapshot('kr','private-MASTER')
        self.assertEqual(s['tier'],'MASTER')
        self.assertEqual(s['source_kind'],'league_list_membership')
        archive=json.loads(next((self.raw/'league_lists/kr/MASTER').glob('*.json')).read_text(encoding='utf-8'))
        self.assertEqual(archive['observed_at'],s['observed_at'])
        self.assertEqual(archive['response']['entries'][0]['puuid'],s['puuid'])
        no_calls=Mock();no_calls.get.side_effect=AssertionError('Unexpected individual call')
        with patch('update_rank_evidence.now',return_value=self.at+timedelta(seconds=10)):
            record,fresh=fetch_snapshot(self.lake,no_calls,'kr',{'puuid':'private-MASTER'},self.at.timestamp()-1,self.raw)
        self.assertFalse(fresh)
        self.assertEqual(record['observed_at'],s['observed_at'])
        bootstrap(self.lake,client,['kr'],self.raw)
        self.assertEqual(client.get.call_count,3)

    def test_wrong_league_queue_is_not_rank_evidence(self):
        client=Mock();client.get.return_value={'tier':'CHALLENGER','queue':'RANKED_FLEX_SR','entries':[{'puuid':'wrong'}]}
        with self.assertRaises(RiotError): bootstrap(self.lake,client,['kr'],self.raw)
        self.assertIsNone(self.lake.snapshot('kr','wrong'))

    def test_league_cache_before_new_match_end_still_fetches_individual_rank(self):
        client=Mock()
        client.get.side_effect=lambda host,path,params=None: {'tier':'GRANDMASTER' if 'grandmasterleagues' in path else 'CHALLENGER' if 'challengerleagues' in path else 'MASTER','queue':'RANKED_SOLO_5x5','entries':[{'puuid':'member'}]}
        with patch('update_rank_evidence.now',return_value=self.at):
            bootstrap(self.lake,client,['kr'],self.raw)
        individual=Mock();individual.get.return_value=[{'queueType':'RANKED_SOLO_5x5','tier':'MASTER','rank':'I','leaguePoints':0}]
        with patch('update_rank_evidence.now',return_value=self.at+timedelta(seconds=20)):
            _,fresh=fetch_snapshot(self.lake,individual,'kr',{'puuid':'member'},self.at.timestamp()+10,self.raw)
        self.assertTrue(fresh)
        self.assertEqual(individual.get.call_count,1)


if __name__=='__main__': unittest.main()
