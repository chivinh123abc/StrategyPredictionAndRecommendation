"""Chronological professional draft replay with only already revealed picks.

This measures retrieval of observed picks, NOT strategic optimality/win uplift.
All methods share the same recent, legal candidate pool.
"""
import json
from itertools import permutations
from pathlib import Path
import re
import sys
import argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from draft_advisor import DraftAdvisor, ROLES
from draft_meta import MetaPolicy


def assign_observed(champions,snapshot):
    if not champions:return {}
    def mass(roles):return np.prod([snapshot.role_probabilities(c).get(r,0) for c,r in zip(champions,roles)])
    chosen=max(permutations(ROLES,len(champions)),key=mass)
    return dict(zip(chosen,champions))


def metric(rows):
    if not rows:return {'queries':0}
    return {'queries':len(rows),'recall_at_1':float(np.mean([r['rank']==1 for r in rows])),
            'recall_at_5':float(np.mean([r['rank']<=5 for r in rows])),
            'mrr_at_5':float(np.mean([1/r['rank'] if r['rank']<=5 else 0 for r in rows])),
            'candidate_coverage':float(np.mean([r['covered'] for r in rows]))}


def evaluate(region='LCK',holdout_games=20):
    baseline_advisor=DraftAdvisor()
    matches=baseline_advisor.history.matches
    region=region.upper()
    sub=matches[matches.league.str.upper().eq(region)].copy()
    order=sub.groupby('gameid').date.first().sort_values()
    if len(order)<=holdout_games:raise ValueError('Insufficient historical games for replay')
    chosen=order.tail(holdout_games)
    cutoff=pd.to_datetime(chosen.min(),utc=True)-pd.Timedelta(nanoseconds=1)
    advisor=DraftAdvisor(meta_policy=MetaPolicy(as_of=cutoff.isoformat()))
    snapshot,_,_=advisor.context(region)
    past=sub[pd.to_datetime(sub.date,utc=True)<=cutoff]
    # A whole-history presence baseline, with no lookahead into holdout.
    all_presence={}
    for game,g in past.groupby('gameid'):
        p=advisor.history.players[advisor.history.players.gameid.eq(game)]
        names=set(p.champion)
        for col in ['ban1','ban2','ban3','ban4','ban5']:
            if col in g:names.update(g[col].dropna())
        for c in names:all_presence[c]=all_presence.get(c,0)+1
    rows={k:[] for k in ['long_history_presence','recent_presence','patch_context_priority']}
    slot_order=[('F',1),('S',1),('S',2),('F',2),('F',3),('S',3),('S',4),('F',4),('F',5),('S',5)]
    rejected=[];example=[]
    for game in chosen.index:
        g=sub[sub.gameid.eq(game)]
        if len(g)!=2 or int(g.firstPick.sum())!=1:
            rejected.append({'gameid':game,'reason':'missing/unreliable firstPick'});continue
        first=g[g.firstPick.eq(1)].iloc[0];second=g[g.firstPick.eq(0)].iloc[0]
        teams={'F':first,'S':second}
        choices={prefix:[row[f'pick{i}'] for i in range(1,6)] for prefix,row in teams.items()}
        allpicks=choices['F']+choices['S']
        if len(set(allpicks))!=10 or any(pd.isna(c) or not c for c in allpicks):
            rejected.append({'gameid':game,'reason':'invalid pick order records'});continue
        banned={v for row in teams.values() for c in ['ban1','ban2','ban3']
                if pd.notna(v:=row[c]) and str(v).lower() not in ['','none','noban','null']}
        picked={'F':[],'S':[]}
        for index,(prefix,n) in enumerate(slot_order):
            if index==6:
                banned.update(v for row in teams.values() for c in ['ban4','ban5']
                              if pd.notna(v:=row[c]) and str(v).lower() not in ['','none','noban','null'])
            other='S' if prefix=='F' else 'F'
            own=assign_observed(picked[prefix],snapshot)
            enemy=assign_observed(picked[other],snapshot)
            roster=snapshot.roster(teams[prefix].teamname)
            roster=roster['players'] if roster else {}
            unavailable=banned|set(picked['F']+picked['S'])
            candidates={}
            for role in ROLES:
                if role in own:continue
                ranked=advisor.recommend_picks(role,own,enemy,unavailable,roster.get(role),top_k=10000,
                                               region=region,draft_slot=f'{prefix}{n}')
                for r in ranked:
                    if r['champion'] not in candidates or r['score']>candidates[r['champion']]['score']:
                        candidates[r['champion']]=r
            names=list(candidates)
            priorities={
                'long_history_presence':sorted(names,key=lambda c:(-all_presence.get(c,0),c)),
                'recent_presence':sorted(names,key=lambda c:(-snapshot.presence.get(c,0),c)),
                'patch_context_priority':sorted(names,key=lambda c:(-candidates[c]['score'],c))}
            truth=choices[prefix][n-1]
            if len(example)<10:
                example.append({'gameid':str(game),'slot':f'{prefix}{n}','observed_pick':truth,
                                'suggested_top5':priorities['patch_context_priority'][:5]})
            for name,items in priorities.items():
                rows[name].append({'gameid':str(game),'slot':f'{prefix}{n}',
                                   'covered':truth in names,'rank':items.index(truth)+1 if truth in names else float('inf')})
            picked[prefix].append(truth)
    report={'protocol':'frozen_history_chronological_actual_pick_order_replay',
            'region':region,'historical_cutoff_exclusive':pd.to_datetime(chosen.min(),utc=True).isoformat(),
            'meta_scope':snapshot.metadata(),'requested_holdout_games':holdout_games,
            'accepted_games':len(chosen)-len(rejected),'rejected_games':rejected,'example_replay':example,
            'metrics':{k:metric(v) for k,v in rows.items()},
            'limitations':['Only previously revealed picks and phase-available bans are supplied.',
                           'Own/enemy role assignments inferred from frozen historical frequencies, not heldout final role labels.',
                           'All compared methods share the same recent-patch eligible candidate pool.',
                           'Pick retrieval is imitation evidence; no causal strategy/winrate benefit is measured.',
                           'A fixed historical snapshot is not updated with holdout game outcomes.',
                           'Prior-game Fearless restrictions are not reconstructed in this benchmark.',
                           'Small development audit, not an independent final test or a validation-tuned policy.']}
    # Paired per-game bootstrap for difference in retrieval, not a claim of uplift.
    rng=np.random.default_rng(42)
    ids=sorted({r['gameid'] for r in rows['recent_presence']})
    if not ids:raise ValueError('No reliable pick-order games available for replay')
    indices={g:[i for i,r in enumerate(rows['recent_presence']) if r['gameid']==g] for g in ids}
    deltas=[]
    for _ in range(300):
        ix=[i for g in rng.choice(ids,len(ids),replace=True) for i in indices[g]]
        a=np.mean([rows['patch_context_priority'][i]['rank']<=5 for i in ix])
        b=np.mean([rows['recent_presence'][i]['rank']<=5 for i in ix])
        deltas.append(a-b)
    report['recall5_difference_vs_recent_presence_ci95']=np.quantile(deltas,[.025,.975]).tolist()
    root=Path(__file__).resolve().parents[2]
    (root/f'reports/{region.lower()}_draft_policy_evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region',default='LCK',choices=['LCK','WLDS','LPL'])
    parser.add_argument('--holdout-games',type=int,default=20)
    args=parser.parse_args()
    evaluate(args.region,args.holdout_games)
