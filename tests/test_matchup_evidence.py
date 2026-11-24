import copy
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/07_recommender'),str(ROOT/'src/01_data_pipeline')]
from matchup_evidence import pro_observations,SourceView,compare_sources,available_before,read_rank_snapshot,normalize_rank,MatchupExplanations,format_evidence
from rank_data_contract import ChampionCatalog
from evaluate_contextual_evidence import LaneRankEvidence,prospective_partitions,freeze_records
from draft_advisor import DraftAdvisor
from draft_meta import MetaPolicy
from historical_recommender import HistoricalRecommender


def fixture():
    roles=['top','jng','mid','bot','sup'];matches=[];players=[];entries={}
    for i in range(5):
        for side,offset in [('Blue',0),('Red',5)]:
            champs=[f'C{offset+j+1}' for j in range(5)]
            matches.append(dict(gameid=f'g{i}',side=side,date=f'2026-11-{i+1:02}T00:00:00Z',
                gamelength=1200,patch=16.2,league='WLDs',teamname=side,firstPick=int(side=='Blue'),
                **{f'pick{k+1}':c for k,c in enumerate(champs)},**{f'ban{k}':f'ban{k}{side}' for k in range(1,6)}))
            for j,role in enumerate(roles):
                c=champs[j];entries[c]={'id':c,'name':c,'key':str(offset+j+1)}
                players.append(dict(gameid=f'g{i}',side=side,position=role,champion=c,result=int(side=='Blue'),
                    teamname=side,playername=role+side,date=f'2026-11-{i+1:02}T00:00:00Z',gamelength=1200,
                    league='WLDs',dpm=500+offset,cspm=5+offset/10,wpm=.5,damagetakenperminute=400,earnedgoldshare=.2,
                    goldat10=1000+offset*200,goldat15=2000+offset*200,xpat10=1000+offset*100,
                    xpat15=2000+offset*100,csat10=100+offset*4,csat15=150+offset*4))
    return pd.DataFrame(matches),pd.DataFrame(players),ChampionCatalog({'version':'test','data':entries})


class MatchupEvidenceTests(unittest.TestCase):
    def test_frozen_missing_measurements_remain_null_not_zero(self):
        rows=pd.DataFrame([dict(gold_diff_15=float('nan'),gold_diff_10=-100)])
        records=freeze_records(rows)
        json.dumps(records,allow_nan=False)
        self.assertIsNone(records[0]['gold_diff_15'])
        self.assertEqual(records[0]['gold_diff_10'],-100)

    def test_pro_signed_join_mirrors_and_metric_missing(self):
        m,p,c=fixture();rows=pro_observations(m,p,c)
        self.assertEqual(len(rows),50)
        self.assertEqual(set(rows.champion_id),set(range(1,11)))
        a=rows[(rows.role=='top')&(rows.team_id=='Blue')]
        self.assertTrue(a.gold_diff_15.eq(-1000).all())
        self.assertTrue(rows.groupby(['match_id','role']).gold_diff_15.sum().eq(0).all())
        p.loc[(p.gameid=='g0')&(p.side=='Red')&(p.position=='top'),'goldat15']=None
        measured=pro_observations(m,p,c)
        lane=measured[(measured.match_id=='g0')&(measured.role=='top')]
        self.assertTrue(lane.gold_diff_15.isna().all())
        self.assertTrue(lane.xp_diff_15.notna().all())

    def test_15_minute_fields_are_not_used_for_short_matches(self):
        m,p,c=fixture();m.loc[m.gameid=='g0','gamelength']=700
        rows=pro_observations(m,p,c)
        self.assertTrue(rows[rows.match_id=='g0'].gold_diff_15.isna().all())
        self.assertTrue(rows[rows.match_id=='g0'].gold_diff_10.notna().all())

    def test_duplicate_role_rejected_incomplete_game_not_invented(self):
        m,p,c=fixture()
        with self.assertRaises(ValueError):pro_observations(m,pd.concat([p,p.iloc[:1]]),c)
        rows=pro_observations(m,p.drop(index=0),c)
        self.assertNotIn('g0',set(rows.match_id))

    def test_conflicts_ci_and_zero_support_are_separate(self):
        m,p,c=fixture();rows=pro_observations(m,p,c)
        a=SourceView(rows).lookup('top','C1','C6')
        b=copy.deepcopy(a);b['gold_diff_15_mean']=1000;b['gold_diff_15_mean_ci95_low']=900;b['gold_diff_15_mean_ci95_high']=1100;b['winrate']=0
        conflict=compare_sources(a,b)
        self.assertEqual(conflict['gd15_comparison'],'opposite_supported_intervals')
        self.assertTrue(conflict['winrate_direction_conflict'])
        b['gold_diff_15_mean_ci95_low']=-2000
        self.assertEqual(compare_sources(a,b)['gd15_comparison'],'opposite_means_uncertain')
        missing=SourceView(pd.DataFrame()).lookup('top','C1','C6')
        self.assertIsNone(missing['winrate'])
        self.assertEqual(compare_sources(a,missing)['sample_status'],'insufficient_samples')
        self.assertEqual(a['games'],5)

    def test_rank_availability_uses_ingestion_as_well_as_event_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'r.db'
            c=sqlite3.connect(path)
            c.executescript('CREATE TABLE jobs(match_id TEXT,status TEXT,updated_at REAL); CREATE TABLE observations(match_id TEXT,team_id INT,role TEXT,row_json TEXT);')
            row=dict(match_id='g',ended_at='2026-11-01T00:00:00Z',available_at='2026-11-02T00:00:00Z')
            c.execute('INSERT INTO jobs VALUES(?,?,?)',('g','accepted',pd.Timestamp('2026-11-24T00:00:00Z').timestamp()))
            c.execute('INSERT INTO observations VALUES(?,?,?,?)',('g',100,'top',json.dumps(row)));c.commit();c.close()
            rows=read_rank_snapshot(path)
            self.assertTrue(available_before(rows,'2026-11-23T00:00:00Z').empty)
            self.assertEqual(len(available_before(rows,'2026-11-25T00:00:00Z')),1)

    def test_unknown_rank_id_excludes_whole_game_not_fuzzy_matching(self):
        _,_,c=fixture()
        rows=pd.DataFrame([dict(match_id='a',champion='C1',champion_id=1,opponent='C6',opponent_id=999),
            dict(match_id='a',champion='C2',champion_id=2,opponent='C7',opponent_id=7)])
        result,unknown=normalize_rank(rows,c)
        self.assertTrue(result.empty);self.assertEqual(unknown,1)

    def test_rank_experiment_is_same_role_and_unsupported_is_neutral(self):
        m,p,c=fixture();rows=pro_observations(m,p,c)
        ev=LaneRankEvidence(rows)
        score,trace,coverage=ev.evaluate('top','C1',{'mid':{'C6':1}},.5,1,5,10)
        self.assertEqual((score,trace,coverage),(.5,[],0))
        score,trace,coverage=ev.evaluate('top','C1',{'top':{'C6':.5}},.5,1,5,10)
        self.assertGreater(score,.5);self.assertEqual(coverage,.5)
        self.assertEqual(ev.evaluate('top','C1',{'top':{'C6':1}},.5,1,6,10)[0],.5)

    def test_prospective_series_excludes_series_started_before_freeze(self):
        states=[dict(action='pick',series_id=f's{i}',gameid=f'g{i}',turn=7,date=f'2026-11-{i+1:02}T00:00:00Z') for i in range(15)]
        parts,ids,ready=prospective_partitions(states,'2026-11-05T00:00:00Z')
        self.assertTrue(ready);self.assertEqual([len(ids[p]) for p in ['validation','test']],[5,5])
        self.assertFalse(set(ids['validation'])&set(ids['test']))
        states.append(dict(states[10],date='2026-11-01T00:00:00Z'))
        self.assertFalse(prospective_partitions(states,'2026-11-05T00:00:00Z')[2])

    def test_explanations_do_not_change_order_or_scores(self):
        m,p,c=fixture();history=HistoricalRecommender.from_frames(m,p)
        base=DraftAdvisor(historical=history,meta_policy=MetaPolicy(as_of='2026-11-06'),explain_matchups=False)
        provider=SimpleNamespace(explain=lambda *a:[{'sentinel':'explanation_only'}])
        shown=DraftAdvisor(historical=history,meta_policy=MetaPolicy(as_of='2026-11-06'),matchup_explanations=provider)
        args=('top',{}, {'top':'C6'})
        a=base.recommend_picks(*args,region='WLDS');b=shown.recommend_picks(*args,region='WLDS')
        self.assertTrue(a)
        self.assertEqual([(r['champion'],r['score']) for r in a],[(r['champion'],r['score']) for r in b])
        self.assertEqual(b[0]['matchup_source_comparison'][0]['sentinel'],'explanation_only')

    def test_prospective_overlapping_series_are_not_ready(self):
        states=[dict(action='pick',series_id=f's{i}',gameid=f'g{i}',turn=7,date=f'2026-11-{i+1:02}T00:00:00Z') for i in range(15)]
        states.append(dict(states[8],gameid='late',date='2026-11-15T12:00:00Z'))
        self.assertFalse(prospective_partitions(states,'2026-11-05T00:00:00Z')[2])

    def test_console_displays_both_sources_with_uncertainty(self):
        from simulate_draft_match import explain
        m,p,c=fixture();pro=SourceView(pro_observations(m,p,c)).lookup('top','C1','C6')
        rank=SourceView(pd.DataFrame()).lookup('top','C1','C6')
        comparison=dict(champion='C1',opponent='C6',role='top',enemy_role_probability=.7,
            pro=pro,rank=rank,comparison=compare_sources(pro,rank))
        text=StringIO()
        with redirect_stdout(text):explain({'matchup_source_comparison':[comparison]})
        output=text.getvalue()
        for expected in ['PRO: n=5','RANK: n=0','Wilson95','GD10=-1000','GD15 mean CI95','insufficient_samples']:
            self.assertIn(expected,output)


if __name__=='__main__':unittest.main()
