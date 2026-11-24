from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/07_recommender'))
from content_based import ContentBasedRecommender, FEATURES


def sample_players():
    rows=[]
    # Item names intentionally do not occur in any expert champion dictionary.
    for champ,vector in [('Alpha',[1,4,1,2,.2]),('Beta',[2,3,2,1,.3]),('Gamma',[4,1,4,4,.4])]:
        for i in range(6):
            rows.append({'gameid':f'{champ}{i}','date':f'2026-01-{i+1:02d}',
                         'league':'LCK','position':'mid','champion':champ,
                         'playername':'User' if champ=='Alpha' else 'Other',
                         **dict(zip(FEATURES,vector))})
    return pd.DataFrame(rows)


class ContentBasedTests(unittest.TestCase):
    def setUp(self):
        self.players=sample_players()
        self.engine=ContentBasedRecommender(players=self.players)

    def test_cosine_matches_direct_calculation_and_excludes_seed_bans(self):
        catalog=self.engine.catalog('mid')
        a=catalog['vectors'].loc['Alpha'].to_numpy()
        result=self.engine.recommend_similar('Alpha','mid',already_banned={'Gamma'})
        self.assertEqual([r['champion'] for r in result['recommendations']],['Beta'])
        b=catalog['vectors'].loc['Beta'].to_numpy()
        self.assertAlmostEqual(result['recommendations'][0]['cosine_similarity'],np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))
        self.assertIsNone(result['probability'])
        self.assertIsNone(result['causal_uplift'])

    def test_player_profile_is_pick_weighted_mean(self):
        result=self.engine.recommend_for_player('User','mid')
        vector=self.engine.catalog('mid')['vectors'].loc['Alpha']
        np.testing.assert_allclose(list(result['normalized_query_profile'].values()),vector)
        self.assertEqual(result['profile']['item_weights'],{'Alpha':6})
        self.assertAlmostEqual(result['recommendations'][0]['cosine_similarity'],1)

    def test_future_outlier_does_not_change_past_profile_or_scaling(self):
        future=self.players.iloc[[0]].copy()
        future['gameid']='future';future['date']='2027-01-01'
        future[FEATURES]=999999.0
        a=ContentBasedRecommender(players=self.players,before='2026-02-01').catalog('mid')
        b=ContentBasedRecommender(players=pd.concat([self.players,future]),before='2026-02-01').catalog('mid')
        pd.testing.assert_frame_equal(a['vectors'],b['vectors'])
        self.assertEqual(a['scaling_max'],b['scaling_max'])

    def test_cold_start_missing_values_and_constant_catalog_abstain(self):
        self.assertEqual(self.engine.recommend_for_player('Unknown','mid')['status'],'insufficient_profile')
        self.assertEqual(self.engine.recommend_similar('Unknown','mid')['recommendations'],[])
        bad=self.players.copy();bad.loc[bad.champion.eq('Beta'),'dpm']=np.nan
        self.assertNotIn('Beta',ContentBasedRecommender(players=bad).catalog('mid')['raw'].index)
        constant=self.players.copy();constant[FEATURES]=1.0
        self.assertEqual(ContentBasedRecommender(players=constant).recommend_for_player('User','mid')['recommendations'],[])

    def test_region_role_and_exclude_seen(self):
        self.assertEqual(self.engine.recommend_similar('Alpha','mid',region='LPL')['recommendations'],[])
        self.assertEqual(self.engine.recommend_similar('Alpha','top')['recommendations'],[])
        result=self.engine.recommend_for_player('User','mid',exclude_seen=True)
        self.assertNotIn('Alpha',[r['champion'] for r in result['recommendations']])
        with self.assertRaises(ValueError):self.engine.catalog('invalid')


if __name__=='__main__':unittest.main()
