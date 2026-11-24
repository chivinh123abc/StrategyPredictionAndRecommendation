"""CUDA-trained next-action prediction from public, pre-action draft states.

This predicts observed coach behavior, not the best strategy or game winner.
"""
import argparse
from collections import Counter,defaultdict
import json
from pathlib import Path
import pickle
import sys
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/06_machine_learning'),str(Path(__file__).resolve().parent)]
from validation import gpu_candidates,check_gpu
from draft_states import export_states,state_features
from analysis_data import load_clean_tables

MODEL_PATH=ROOT/'models/opponent_model.pkl'


def feasible_roles(champions,catalog):
    """One champion per role, using only training-era observed roles; no final labels."""
    choices=[set(catalog.get(c,{'top','jng','mid','bot','sup'})) for c in champions]
    choices.sort(key=len)
    def assign(index,occupied):
        if index==len(choices):return True
        return any(assign(index+1,occupied|{r}) for r in choices[index]-occupied)
    return assign(0,set())


def split_series(states):
    groups=defaultdict(list)
    for s in states:groups[s['series_id']].append(s)
    ordered=sorted(groups,key=lambda k:(min(s['date'] for s in groups[k]),k))
    if len(ordered)<10:raise ValueError('Need at least10 reconstructed series')
    n=len(ordered);cuts=[0,int(n*.7),int(n*.85),n]
    parts={name:[s for key in ordered[cuts[i]:cuts[i+1]] for s in groups[key]]
           for i,name in enumerate(['train','validation','test'])}
    for a,b in [('train','validation'),('validation','test')]:
        if pd.to_datetime(max(s['date'] for s in parts[a]))>=pd.to_datetime(min(s['date'] for s in parts[b])):
            raise ValueError('Series/time blocks overlap: cannot claim chronological split')
    return parts


class OpponentModel:
    def allowed(self,state):
        excluded=set(state.get('unavailable',[]))|set(state.get('used_champions',[]))
        for k in ['own_picks','enemy_picks','own_bans','enemy_bans']:excluded.update(state.get(k,[]))
        seen=self.action_classes.get(state['action'],set())
        return np.array([c in seen and c not in excluded and
                         (state['action']!='pick' or feasible_roles(state.get('own_picks',[])+[c],self.role_catalog))
                         for c in self.classes],dtype=bool)

    def baseline(self,state,name):
        counts=self.action_counts[state['action']]
        prior=np.array([counts.get(c,0) for c in self.classes],dtype=float)
        prior=(prior+1/len(self.classes))/(prior.sum()+1)
        if name=='action_popularity':return prior
        key=(state['action'],state['slot']) if name=='slot_frequency' else (state['action'],state['actor_team'])
        group=(self.slot_counts if name=='slot_frequency' else self.team_counts).get(key,{})
        return (np.array([group.get(c,0) for c in self.classes])+10*prior)/(sum(group.values())+10)

    def rank(self,state,raw=None,top_k=5):
        if raw is None:
            if pd.to_datetime(state['date'],utc=True)<=pd.to_datetime(self.train_through,utc=True):
                raise ValueError('State is not after training data cutoff; refusing historical lookahead')
            raw=self.model.predict_proba(self.vectorizer.transform([state_features(state)]))[0]
        allowed=self.allowed(state)
        p=np.asarray(raw,dtype=float)*allowed
        if p.sum()<=0:return []
        p=p/p.sum()
        indices=sorted(np.flatnonzero(allowed),key=lambda i:(-p[i],str(self.classes[i])))[:top_k]
        return [{'champion':str(self.classes[i]),'next_action_probability':float(p[i]),
                 'probability_kind':'uncalibrated_masked_action_probability_not_winrate'} for i in indices]

    @classmethod
    def load(cls,path=MODEL_PATH):
        with Path(path).open('rb') as f:payload=pickle.load(f)
        if not isinstance(payload,dict) or payload.get('schema_version')!=1:raise ValueError('Unsupported opponent model schema')
        result=cls.__new__(cls);result.__dict__.update(payload['state'])
        return result


def evaluate(model,states,raw):
    methods=['xgboost_context','action_popularity','slot_frequency','team_frequency']
    rows={name:[] for name in methods}
    for s,prediction in zip(states,raw):
        for name in methods:
            probability=prediction if name=='xgboost_context' else model.baseline(s,name)
            ranked=model.rank(s,probability,top_k=len(model.classes))
            names=[r['champion'] for r in ranked]
            rank=names.index(s['target_champion'])+1 if s['target_champion'] in names else None
            prob=ranked[rank-1]['next_action_probability'] if rank else 1e-12
            rows[name].append({'series_id':s['series_id'],'action':s['action'],'covered':rank is not None,
                               'recall1':int(rank==1),'recall5':int(rank is not None and rank<=5),
                               'mrr5':1/rank if rank is not None and rank<=5 else 0,'nll':float(-np.log(max(prob,1e-12)))})
    def summarize(items):
        return {'queries':len(items),'recall_at_1':float(np.mean([r['recall1'] for r in items])),
                'recall_at_5':float(np.mean([r['recall5'] for r in items])),
                'mrr_at_5':float(np.mean([r['mrr5'] for r in items])),
                'log_loss_including_unseen_targets':float(np.mean([r['nll'] for r in items])),
                'target_coverage':float(np.mean([r['covered'] for r in items]))}
    result={name:{'all':summarize(items),**{a:summarize([r for r in items if r['action']==a]) for a in ['pick','ban']}}for name,items in rows.items()}
    return result,rows


def train(region='WLDS',path=MODEL_PATH):
    states,dataset_manifest=export_states(region)
    parts=split_series(states);train_states=parts['train']
    system=OpponentModel();system.classes=np.array(sorted({s['target_champion'] for s in train_states}))
    encoding={c:i for i,c in enumerate(system.classes)}
    system.vectorizer=DictVectorizer(dtype=np.float32)
    X=system.vectorizer.fit_transform([state_features(s) for s in train_states])
    y=np.array([encoding[s['target_champion']] for s in train_states])
    system.train_through=max(s['date'] for s in train_states)
    _,_,players=load_clean_tables()
    historical=players[players.gameid.isin({s['gameid'] for s in train_states})]
    system.role_catalog={c:set(g.position) for c,g in historical.groupby('champion')}
    system.action_counts=defaultdict(Counter);system.slot_counts=defaultdict(Counter);system.team_counts=defaultdict(Counter)
    system.action_classes=defaultdict(set)
    for s in train_states:
        c=s['target_champion'];a=s['action']
        system.action_counts[a][c]+=1;system.slot_counts[(a,s['slot'])][c]+=1
        system.team_counts[(a,s['actor_team'])][c]+=1;system.action_classes[a].add(c)
    Xval=system.vectorizer.transform([state_features(s) for s in parts['validation']])
    candidates=gpu_candidates();trials=[];models={}
    for name,model in candidates.items():
        model.set_params(n_estimators=40,objective='multi:softprob',num_class=len(system.classes),eval_metric='mlogloss')
        model.fit(X,y);check_gpu(model)
        training_device=json.loads(model.get_booster().save_config())['learner']['generic_param']['device']
        model.set_params(device='cpu') # Inference on CSR is allowed; training was verified CUDA.
        metric,_=evaluate(system,parts['validation'],model.predict_proba(Xval))
        trials.append({'model':name,'training_device':training_device,'validation':metric['xgboost_context']['all']})
        models[name]=model
    best=min(trials,key=lambda t:t['validation']['log_loss_including_unseen_targets'])
    system.model=models[best['model']]
    test_states=parts['test'];Xtest=system.vectorizer.transform([state_features(s) for s in test_states])
    test_metrics,rows=evaluate(system,test_states,system.model.predict_proba(Xtest))
    rng=np.random.default_rng(42);ids=sorted({s['series_id'] for s in test_states})
    per_series={sid:[i for i,s in enumerate(test_states) if s['series_id']==sid] for sid in ids}
    delta=[]
    for _ in range(300):
        ix=[i for sid in rng.choice(ids,len(ids),replace=True) for i in per_series[sid]]
        delta.append(np.mean([rows['xgboost_context'][i]['recall5']-rows['slot_frequency'][i]['recall5'] for i in ix]))
    report={'region':region,'dataset':dataset_manifest,'feature_policy':'explicit_pre_action_allowlist_no_labels_outcomes_final_roles',
            'split_policy':'70/15/15_chronological_reconstructed_series_no_shared_game_or_series',
            'evaluation_use':'development_holdout_previously_inspected_source_not_fresh_final_test',
            'partitions':{k:{'states':len(v),'games':len({s['gameid'] for s in v}),
                              'series':len({s['series_id'] for s in v}),'first':min(s['date'] for s in v),
                              'last':max(s['date'] for s in v),'gameids':sorted({s['gameid'] for s in v}),
                              'series_ids':sorted({s['series_id'] for s in v})}for k,v in parts.items()},
            'validation_candidates':trials,'selected_model':best['model'],'training_device':best['training_device'],
            'inference_device':'cpu','classes':len(system.classes),'features':len(system.vectorizer.feature_names_),
            'metrics':test_metrics,'recall5_delta_vs_slot_ci95_series_bootstrap':np.quantile(delta,[.025,.975]).tolist(),
            'limitations':['This imitates observed choices, not mechanical counters or optimal picks.',
                          'Probabilities are masked/renormalized and uncalibrated; not game win probabilities.',
                          'Champions not observed in training cannot be predicted; coverage is reported.',
                          'Series grouping reconstructed from team pairs/game numbers; not official series IDs.',
                          'Pick role-feasibility mask uses training-era observed roles and may miss novel flex roles.',
                          'No claim of independent fresh test, causal uplift or BO5 optimality.']}
    system.evaluation=report
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with Path(path).open('wb') as f:pickle.dump({'schema_version':1,'state':system.__dict__},f)
    Path(path).with_suffix('.evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'reports/opponent_model_evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['dataset','partitions']},ensure_ascii=False,indent=2))
    return system


def public_simulation_state(draft,names,scope,region):
    side,action=draft.schedule[len(draft.history)]
    other='red' if side=='blue' else 'blue'
    picks={s:list(values.values()) for s,values in draft.picks.items()}
    n=len(picks[side] if action=='pick' else draft.bans[side])+1
    return {'date':scope['requested_as_of'],'league':region,'patch':scope['dataset_patch'],
            'game_number':len(draft.used_champions)//10+1,'turn':len(draft.history)+1,
            'action':action,'slot':('F' if side==draft.first_side else 'S')+f'_{action}{n}',
            'actor_team':names[side],'opponent_team':names[other],
            'own_picks':picks[side],'enemy_picks':picks[other],
            'own_bans':list(draft.bans[side]),'enemy_bans':list(draft.bans[other]),
            'used_champions':list(draft.used_champions),'unavailable':sorted(draft.unavailable)}


def predict_session(path,turn=1,output=ROOT/'reports/opponent_prediction.json'):
    session=json.loads(Path(path).read_text(encoding='utf-8'))
    if turn not in range(1,len(session['history'])+1):raise ValueError('Turn not available in session')
    current=session['history'][turn-1];side=current['side'];other='red' if side=='blue' else 'blue'
    picks={'blue':[],'red':[]};bans={'blue':[],'red':[]}
    for h in session['history'][:turn-1]:(picks if h['action']=='pick' else bans)[h['side']].append(h['champion'])
    action=current['action'];n=len((picks if action=='pick' else bans)[side])+1
    used=session.get('used_champions',[])
    state={'date':session['meta_scope']['requested_as_of'],'league':session['region'],
           'patch':session['meta_scope']['dataset_patch'],'game_number':len(used)//10+1,'turn':turn,
           'action':action,'slot':('F' if side==session['first_pick_side'] else 'S')+f'_{action}{n}',
           'actor_team':session['teams'][side],'opponent_team':session['teams'][other],
           'own_picks':picks[side],'enemy_picks':picks[other],'own_bans':bans[side],'enemy_bans':bans[other],
           'used_champions':used,'unavailable':sorted(set(used+sum(picks.values(),[])+sum(bans.values(),[])))}
    model=OpponentModel.load();predictions=model.rank(state)
    report={'state':state,'predictions':predictions,'trained_through':model.train_through,
            'reference_action_in_saved_session':current['champion'],
            'reference_kind':'saved_simulation_choice_not_real_coach_label',
            'limitations':model.evaluation['limitations']}
    Path(output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--train',action='store_true');parser.add_argument('--region',default='WLDS')
    parser.add_argument('--predict-session',type=Path);parser.add_argument('--turn',type=int,default=1)
    args=parser.parse_args()
    if args.train:train(args.region)
    elif args.predict_session:predict_session(args.predict_session,args.turn)
    else:parser.error('Use --train or --predict-session PATH --turn N')
