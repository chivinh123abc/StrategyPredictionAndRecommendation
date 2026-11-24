"""Regression tests for signed data, leakage boundaries and honest outputs."""
from pathlib import Path
import importlib.util
import sys
import unittest
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/06_machine_learning'),str(ROOT/'src/07_recommender')]
from analysis_data import load_clean_tables,clean_ranked,complete_10min
from validation import split_groups,calibrate,fingerprint,check_gpu
from snowball_model import load_integrated_10min_dataset,SnowballFeaturePipeline,LolSnowballPredictionSystem
from draft_model import DraftFeatureEngineering,historical_training_features,load_pivoted_draft_data,LolDraftPredictionSystem
from historical_recommender import HistoricalRecommender,wilson


class IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rank,cls.matches,cls.players=load_clean_tables()
        cls.snow=load_integrated_10min_dataset()
        cls.draft=load_pivoted_draft_data()

    def test_signed_differences_and_exports(self):
        self.assertGreater(int((self.rank.blueGoldDiff<0).sum()),0)
        np.testing.assert_array_equal(self.rank.blueGoldDiff,self.rank.blueTotalGold-self.rank.redTotalGold)
        np.testing.assert_array_equal(self.rank.redGoldDiff,-self.rank.blueGoldDiff)
        csv=pd.read_csv(ROOT/'data/processed/clean_ranked_10min.csv')
        np.testing.assert_array_equal(csv.blueGoldDiff,csv.blueTotalGold-csv.redTotalGold)
        self.assertEqual(set(csv.gameId),set(self.rank.gameId))

    def test_no_synthetic_or_future_features(self):
        f=SnowballFeaturePipeline().engineer_features(self.snow)
        self.assertTrue(np.isfinite(f.to_numpy()).all())
        for col in ['firstdragon','firsttower','void_grubs','top_golddiff','carry_gold_lead']:
            self.assertNotIn(col,f)
        rank=self.snow[self.snow.is_pro_play.eq(0)]
        b=rank[rank.side.eq('Blue')].set_index('gameid')
        r=rank[rank.side.eq('Red')].set_index('gameid')
        np.testing.assert_array_equal(b.golddiffat10,-r.golddiffat10)
        self.assertEqual(int(complete_10min(self.matches).isna()[['golddiffat10','killsat10']].sum().sum()),0)

    def test_group_and_time_boundaries(self):
        for df in [self.snow,self.draft]:
            parts,_=split_groups(df)
            names=list(parts)
            for i,a in enumerate(names):
                for b in names[i+1:]:
                    self.assertFalse(set(parts[a].gameid)&set(parts[b].gameid))
                pro=parts[a] if 'is_pro_play' not in df else parts[a][parts[a].is_pro_play.eq(1)]
                if i<len(names)-1:
                    nxt=parts[names[i+1]]
                    if 'is_pro_play' in df:nxt=nxt[nxt.is_pro_play.eq(1)]
                    self.assertLess(pd.to_datetime(pro.date,utc=True).max(),pd.to_datetime(nxt.date,utc=True).min())

    def test_draft_encoding_cannot_see_own_block_labels(self):
        # Flipping labels in the first block cannot alter its own encoded features.
        small=self.draft.head(90).copy()
        a=historical_training_features(DraftFeatureEngineering(),small)
        dates=pd.to_datetime(small.date,utc=True)
        block=np.array_split(sorted(dates.unique()),6)[0]
        mask=dates.isin(block)
        other=small.copy();other.loc[mask,'blue_win']=1-other.loc[mask,'blue_win']
        b=historical_training_features(DraftFeatureEngineering(),other)
        np.testing.assert_allclose(a[mask],b[mask])

    def test_calibration_bounds(self):
        p=calibrate(np.array([0,.5,1]),{'alpha':.5,'prior':.6})
        np.testing.assert_allclose(p,[.3,.55,.8])

    def test_equal_timestamps_stay_in_one_partition(self):
        rows=[]
        for i in range(40):
            for side in ['Blue','Red']:
                rows.append({'gameid':f'g{i}','side':side,'date':f'2026-01-{1+i//2:02d}',
                             'is_pro_play':1,'result':int(side=='Blue')})
        parts,_=split_groups(pd.DataFrame(rows).sample(frac=1,random_state=3))
        seen={}
        for name,frame in parts.items():
            for date in frame.date.unique():
                self.assertNotIn(date,seen)
                seen[date]=name

    def test_recommender_handles_champion_outside_expert_dictionary(self):
        engine=HistoricalRecommender.__new__(HistoricalRecommender)
        engine.min_games=5;engine._regions={}
        engine.players=pd.DataFrame([{'gameid':f'g{i}','position':'mid','side':'Blue',
                                     'champion':'NewUncataloguedChampion','playername':'P',
                                     'league':'LCK','result':i%2} for i in range(8)])
        result=engine.recommend('mid',[],[],region='LCK')
        self.assertEqual(result[0]['champion'],'NewUncataloguedChampion')
        self.assertEqual(result[0]['historical']['games'],8)
        self.assertEqual(engine.recommend('top',[],[],region='LCK'),[])

    def test_models_manifest_and_gpu(self):
        for system,df in [(LolDraftPredictionSystem.load_model(),self.draft),
                          (LolSnowballPredictionSystem.load_model(),self.snow)]:
            self.assertEqual(system.evaluation['data_fingerprint'],fingerprint(df))
            check_gpu(system.best_model)
            self.assertIn('test_ci95_group_bootstrap',system.evaluation)

    def test_recommender_evidence_and_exclusions(self):
        engine=HistoricalRecommender()
        picks=engine.recommend('mid',{'jng':'Vi'},{'mid':'Azir'},already_banned={'Ahri'},top_k=10)
        self.assertTrue(picks)
        for p in picks:
            self.assertNotIn(p['champion'],['Vi','Azir','Ahri'])
            self.assertIsNone(p['probability']);self.assertIsNone(p['expected_winrate_delta'])
            ev=p['historical'];lo,hi=ev['ci95_wilson']
            self.assertLessEqual(lo,ev['winrate']);self.assertGreaterEqual(hi,ev['winrate'])
            self.assertEqual(ev['wins']/ev['games'],ev['winrate'])
        unassigned=engine.recommend('mid',[],['Azir'],top_k=2)
        self.assertTrue(all(p['matchup'] is None for p in unassigned))
        self.assertEqual(engine.recommend('mid',[],[],region='NO_SUCH_LEAGUE'),[])

    def test_unknown_expert_input_does_not_invent_uplift(self):
        from recommender_engine import PunisherEngine
        r=PunisherEngine().detect_flaws_and_punishers(['Renekton','Lee Sin','Yasuo','Jinx','Thresh'])
        self.assertIsNone(r['expected_winrate_delta'])
        self.assertEqual(r['punishers'],[])
        self.assertTrue(all(f['winrate_impact'] is None for f in r['flaws']))

    def test_dataset_change_invalidates_test_manifest(self):
        from evaluate_models import verified_test
        system=LolDraftPredictionSystem.load_model()
        changed=self.draft.copy()
        changed.loc[changed.index[0],'blue_win']=1-changed.loc[changed.index[0],'blue_win']
        with self.assertRaisesRegex(ValueError,'Dataset changed'):
            verified_test(system,changed,'blue_win')


if __name__=='__main__':unittest.main()
