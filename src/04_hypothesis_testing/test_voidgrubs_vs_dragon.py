"""Minute-10 objectives: rank observations only until pro timelines exist."""
import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'07_recommender'))
from analysis_data import load_clean_tables,DB_PATH
from historical_recommender import evidence


class ObjectiveHypothesisTester:
    def __init__(self,db_path=DB_PATH,alpha=.05):
        self.db_path=Path(db_path);self.alpha=alpha

    def load_data(self):
        rank,_,_=load_clean_tables(self.db_path)
        # One fixed side per independent match. No mirror observations in tests.
        out=pd.DataFrame({'gameid':rank.gameId,'side':'Blue','result':rank.blueWins,
                          'has_first_dragon':(rank.blueDragons>0).astype(int),
                          'has_3_grubs':(rank.blueVoidgrubs>=3).astype(int),
                          'void_grubs':rank.blueVoidgrubs,'dragons':rank.blueDragons})
        return out.iloc[:0].copy(),out

    @staticmethod
    def compute_contingency_stats(df,feature_col,target_col='result'):
        if df.empty:return {'status':'unavailable','reason':'No verified pro objective timestamps at minute 10'}
        ct=pd.crosstab(df[feature_col],df[target_col]).reindex(index=[1,0],columns=[1,0],fill_value=0)
        a,b,c,d=ct.to_numpy().ravel()
        table=[[int(a),int(b)],[int(c),int(d)]]
        odds,p=stats.fisher_exact(table)
        return {'status':'descriptive_association','table':table,'n_games':len(df),
                'has_objective':evidence(a,a+b),'no_objective':evidence(c,c+d),
                'odds_ratio':float(odds) if np.isfinite(odds) else None,'p_value':float(p),
                'method':'Fisher exact; Blue side only; two objectives use Bonferroni alpha/2',
                'causal_uplift':None}

    def compute_scenario_matrix(self,df):
        rows=[]
        for (dragon,grubs),g in df.groupby(['has_first_dragon','has_3_grubs']):
            rows.append({'dragon_before10':int(dragon),'at_least_3_grubs_before10':int(grubs),
                         **evidence(int(g.result.sum()),len(g))})
        return pd.DataFrame(rows)

    def run_tests(self):
        pro,rank=self.load_data()
        result={}
        for source,df in [('pro',pro),('rank',rank)]:
            for name,col in [('grubs','has_3_grubs'),('dragon','has_first_dragon')]:
                r=self.compute_contingency_stats(df,col)
                if 'p_value' in r:r['reject_bonferroni']=r['p_value']<self.alpha/2
                result[source+'_'+name]=r
            result[source+'_scenarios']=self.compute_scenario_matrix(df)
        return result

    def display_report(self,export=True):
        import json
        result=self.run_tests()
        print('Pro Play: unavailable at minute 10; full-match objective totals are excluded.')
        for k,v in result.items():
            if not isinstance(v,pd.DataFrame):print(k,json.dumps(v,ensure_ascii=False))
        print('Rank: presence of a dragon before minute 10, NOT necessarily the first dragon.')
        print('Association only; repeated players/teams and patch confounding remain.')
        if export:
            result['rank_scenarios'].to_csv(Path(__file__).resolve().parents[2]/'data/processed/hypothesis_test_3_objectives.csv',index=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,default=DB_PATH)
    p.add_argument('--no-export',action='store_true');args=p.parse_args()
    ObjectiveHypothesisTester(args.db).display_report(export=not args.no_export)
