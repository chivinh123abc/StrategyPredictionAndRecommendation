"""Minute-10 prediction using measured macro features common to both sources."""
import argparse
from datetime import datetime
from pathlib import Path
import pickle
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analysis_data import load_clean_tables, complete_10min, DB_PATH
from validation import evaluate_training, calibrate, SCHEMA_VERSION

MODEL_PATH = PROJECT_ROOT / 'models/snowball_model.pkl'
MACRO_COLUMNS = ['golddiffat10','xpdiffat10','csdiffat10','killsat10','deathsat10']


def load_integrated_10min_dataset(db_path=DB_PATH):
    rank, matches, _ = load_clean_tables(db_path)
    pro = complete_10min(matches)[['gameid','side','date','result']+MACRO_COLUMNS].copy()
    pro['is_pro_play'] = 1
    ranks = []
    for side, sign in [('Blue',1),('Red',-1)]:
        r = pd.DataFrame({'gameid': rank.gameId, 'side': side,
                          'date': pd.NaT,
                          'result': rank.blueWins if sign==1 else 1-rank.blueWins,
                          'golddiffat10': sign*rank.blueGoldDiff,
                          'xpdiffat10': sign*rank.blueExperienceDiff,
                          'csdiffat10': sign*(rank.blueTotalMinionsKilled+rank.blueTotalJungleMinionsKilled-rank.redTotalMinionsKilled-rank.redTotalJungleMinionsKilled),
                          'killsat10': rank.blueKills if sign==1 else rank.redKills,
                          'deathsat10': rank.blueDeaths if sign==1 else rank.redDeaths,
                          'is_pro_play': 0})
        ranks.append(r)
    return pd.concat([pro,*ranks],ignore_index=True).sort_values(['gameid','side']).reset_index(drop=True)


class SnowballFeaturePipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []

    def engineer_features(self, df):
        X = df[MACRO_COLUMNS].astype(float).copy()
        if not np.isfinite(X.to_numpy()).all(): raise ValueError('Missing/non-finite minute-10 measurements')
        X['kill_diff'] = X.killsat10-X.deathsat10
        X['kda_ratio'] = (X.killsat10+1)/(X.deathsat10+1)
        X['is_blue_side'] = df.side.eq('Blue').astype(float)
        X['is_pro_play'] = df.is_pro_play.astype(float)
        self.feature_names = X.columns.tolist()
        return X

    def fit_transform(self, df): return self.scaler.fit_transform(self.engineer_features(df))
    def transform(self, df): return self.scaler.transform(self.engineer_features(df))


class LolSnowballPredictionSystem:
    def __init__(self):
        self.fe = SnowballFeaturePipeline()
        self.best_model = None
        self.best_model_name = ''
        self.feature_importances_ = {}

    def train_and_evaluate(self, test_size=.20):
        return evaluate_training(self,load_integrated_10min_dataset(),'result',MODEL_PATH,test_size)

    def save_model(self,path=MODEL_PATH):
        payload = {'model':self.best_model,'model_name':self.best_model_name,
                   'feature_engineering':self.fe,'calibration':self.calibration,
                   'evaluation':self.evaluation,'schema_version':SCHEMA_VERSION,
                   'trained_at':datetime.now().isoformat(),'target':'result'}
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        with open(path,'wb') as f: pickle.dump(payload,f)

    @classmethod
    def load_model(cls,path=MODEL_PATH):
        class U(pickle.Unpickler):
            def find_class(self,module,name):
                if name=='SnowballFeaturePipeline': return SnowballFeaturePipeline
                return super().find_class(module,name)
        with open(path,'rb') as f: payload=U(f).load()
        if payload.get('schema_version')!=SCHEMA_VERSION:
            raise ValueError('Legacy model uses unsafe features; run snowball_model.py --train')
        system=cls()
        system.best_model,system.best_model_name=payload['model'],payload['model_name']
        system.fe,system.calibration,system.evaluation=payload['feature_engineering'],payload['calibration'],payload['evaluation']
        return system

    def predict_snowball(self,gold_diff,xp_diff,cs_diff,kills,deaths,side='Blue',is_pro_play=1):
        if side not in ['Blue','Red'] or is_pro_play not in [0,1]: raise ValueError('Invalid side/source')
        if min(kills,deaths)<0: raise ValueError('Kills/deaths cannot be negative')
        row=pd.DataFrame([dict(zip(MACRO_COLUMNS,[gold_diff,xp_diff,cs_diff,kills,deaths]),side=side,is_pro_play=is_pro_play)])
        p=float(calibrate(self.best_model.predict_proba(self.fe.transform(row))[:,1],self.calibration)[0])
        return {'win_probability_pct':round(p*100,2),'lose_probability_pct':round((1-p)*100,2),
                'gold_lead':float(gold_diff),'model_used':self.best_model_name,
                'probability_kind':'calibrated_model_estimate','causal_uplift':None,
                'features_used':self.fe.feature_names}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--train',action='store_true')
    p.add_argument('--predict',action='store_true')
    for flag in ['gold-diff','xp-diff','cs-diff','kills','deaths']: p.add_argument('--'+flag,type=float)
    p.add_argument('--side',choices=['Blue','Red'],default='Blue')
    p.add_argument('--source',choices=['pro','rank'],default='pro')
    args=p.parse_args()
    if args.predict:
        fields=['gold_diff','xp_diff','cs_diff','kills','deaths']
        if any(getattr(args,f) is None for f in fields): p.error('All five minute-10 measurements are required')
        print(LolSnowballPredictionSystem.load_model().predict_snowball(**{f:getattr(args,f) for f in fields},side=args.side,is_pro_play=int(args.source=='pro')))
    elif args.train: LolSnowballPredictionSystem().train_and_evaluate()
    else: p.print_help()
