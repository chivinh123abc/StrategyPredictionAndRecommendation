"""Temporal held-out draft-slot retrieval benchmark, not a winrate-uplift test."""
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'06_machine_learning'))
from draft_model import load_pivoted_draft_data,POSITIONS
from validation import split_groups,fingerprint
from historical_recommender import HistoricalRecommender


def retrieval_metrics(rows):
    return {'queries':len(rows),'recall_at_5':float(np.mean([r['rank']<=5 for r in rows])),
            'mrr_at_5':float(np.mean([1/r['rank'] if r['rank']<=5 else 0 for r in rows])),
            'candidate_coverage':float(np.mean([r['covered'] for r in rows]))}


def evaluate():
    df=load_pivoted_draft_data();parts,_=split_groups(df)
    test=parts['test']
    # Freeze all historical counts strictly before the held-out test period.
    cutoff=pd.to_datetime(test.date,utc=True).min()
    engine=HistoricalRecommender(before=cutoff)
    base,_,_,_=engine.stats('ALL')
    rows=[];baseline=[]
    for row in test.itertuples(index=False):
        for side,opposite in [('blue','red'),('red','blue')]:
            own={r:getattr(row,f'{side}_{r}') for r in POSITIONS}
            enemy={r:getattr(row,f'{opposite}_{r}') for r in POSITIONS}
            for role in POSITIONS:
                truth=own[role];allies={r:c for r,c in own.items() if r!=role}
                picks=engine.recommend(role,allies,enemy,top_k=10000)
                names=[p['champion'] for p in picks]
                rank=names.index(truth)+1 if truth in names else float('inf')
                common={'gameid':row.gameid,'covered':truth in names}
                rows.append({**common,'rank':rank})
                popularity=sorted(names,key=lambda c:(-base[(role,c)][1],c))
                baseline.append({**common,'rank':popularity.index(truth)+1 if truth in popularity else float('inf')})
    rng=np.random.default_rng(42)
    ids=sorted(test.gameid.unique())
    lookup={g:[i for i,r in enumerate(rows) if r['gameid']==g] for g in ids}
    boot={k:[] for k in ['recall_at_5','mrr_at_5','candidate_coverage']}
    for _ in range(300):
        sampled=[rows[i] for g in rng.choice(ids,len(ids),replace=True) for i in lookup[g]]
        for k,v in retrieval_metrics(sampled).items():
            if k in boot:boot[k].append(v)
    result={'protocol':'retrospective_final_draft_slot_retrieval',
            'data_fingerprint':fingerprint(df),'historical_cutoff_exclusive':cutoff.isoformat(),
            'historical_games':int(engine.players.gameid.nunique()),'test_games':len(ids),
            'historical_ranker':retrieval_metrics(rows),'popularity_baseline':retrieval_metrics(baseline),
            'ci95_group_bootstrap':{k:np.quantile(v,[.025,.975]).tolist() for k,v in boot.items()},
            'limitations':['Reconstructs a final draft slot with other nine picks visible; not an actual pick-order replay.',
                           'Observed pick is a retrieval label, not the optimal choice.',
                           'No causal winrate improvement is measured. Wilson and bootstrap intervals ignore repeated teams/players.',
                           'Benchmark context excludes bans because this dataset pivot does not retain ban order.']}
    root=Path(__file__).resolve().parents[2]
    path=root/'reports/recommender_evaluation.json'
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return result


if __name__=='__main__':evaluate()
