"""Same-pool comparison of the current and a simple descriptive pick formula."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/01_data_pipeline')]
from analysis_data import load_clean_tables,DB_PATH
from draft_advisor import DraftAdvisor,AdvisorPolicy,ROLES
from draft_meta import MetaPolicy
from historical_recommender import HistoricalRecommender
from draft_states import build_states
from evaluate_draft_policy import assign_observed
from evaluate_rank_transfer import split_series,metrics,paired_interval
from audit_draft_choices import diagnostic_score
from ranked_matchups import write_json

COMPONENTS=['meta','draft_order','historical','matchup','synergy','composition','mastery','content']


def collapse(rows,score=lambda row:row['score']):
    """Best eligible role for each champion; sparse tier shared by every formula."""
    chosen={}
    for row in rows:
        key=(row['evidence_status']=='sparse_candidate',-float(score(row)),-row['games'],row['champion'])
        if row['champion'] not in chosen or key<chosen[row['champion']][0]:chosen[row['champion']]=(key,row)
    return sorted(chosen,key=lambda champion:chosen[champion][0])


def replay_pair(states,current,simple,region):
    snapshot,_,_=current.context(region)
    simple._contexts=current._contexts;simple._content_cache=current._content_cache
    results=[];audit=Counter();examples=[]
    for index,state in enumerate(states):
        if index%50==0:print(f'replay {index}/{len(states)}',flush=True)
        own=assign_observed(state['own_picks'],snapshot);enemy=assign_observed(state['enemy_picks'],snapshot)
        roster=snapshot.roster(state['actor_team']);roster=roster['players'] if roster else {}
        candidates={mode:[] for mode in ['current','simple']}
        for role in ROLES:
            if role in own:continue
            for mode,advisor in [('current',current),('simple',simple)]:
                ranked=advisor.recommend_picks(role,own,enemy,state['unavailable'],roster.get(role),top_k=10000,
                    region=region,draft_slot=state['slot'].replace('_pick',''))
                if set(r['champion'] for r in ranked)&set(state['unavailable']):raise AssertionError('Illegal candidate')
                candidates[mode].extend(ranked)
        pools={mode:{(r['lane'],r['champion']) for r in rows} for mode,rows in candidates.items()}
        if pools['current']!=pools['simple']:raise AssertionError('Candidate role pools differ')
        pool_digest=hashlib.sha256(json.dumps(sorted(pools['current'])).encode()).hexdigest()
        ordered={mode:collapse(rows) for mode,rows in candidates.items()}
        popularity={r['champion']:snapshot.presence.get(r['champion'],0) for r in candidates['current']}
        ordered['recent_presence']=sorted(ordered['current'],key=lambda c:(-popularity[c],c))
        truth=state['target_champion']
        for mode,items in ordered.items():
            results.append({'mode':'pro_only' if mode=='current' else mode,'formula':mode,
                'gameid':state['gameid'],'series_id':state['series_id'],'date':state['date'],'turn':state['turn'],
                'observed_pick':truth,'rank':items.index(truth)+1 if truth in items else None,
                'top5':items[:5],'candidate_count':len(items),'enemy_count':len(enemy),
                'candidate_role_pool_sha256':pool_digest,
                'rank_supported_candidates':0})
        for component in COMPONENTS:
            removed=collapse(candidates['current'],lambda r:diagnostic_score(r,component))
            audit[(component,'active_queries')]+=int(any(component in r['score_components'] for r in candidates['current']))
            audit[(component,'top1_changes')]+=int(bool(removed and ordered['current'] and removed[0]!=ordered['current'][0]))
            audit[(component,'recall5_hit_changes')]+=int((truth in removed[:5])!=(truth in ordered['current'][:5]))
            audit[(component,'net_hit5_gain_current')]+=int(truth in ordered['current'][:5])-int(truth in removed[:5])
        if len(examples)<5:
            examples.append({'gameid':state['gameid'],'turn':state['turn'],
                'current_top5':ordered['current'][:5],'simple_top5':ordered['simple'][:5]})
    return results,audit,examples


def evaluate(region='WLDS',patch='16.20',output=ROOT/'reports/pick_scoring_comparison',limit=0):
    _,matches,players=load_clean_tables();states,manifest=build_states(matches,region)
    parts,ids=split_series(states,patch)
    cutoff=(pd.Timestamp(parts['validation'][0]['date'])-pd.Timedelta(nanoseconds=1)).isoformat()
    ends=pd.to_datetime(matches.date,utc=True)+pd.to_timedelta(matches.gamelength,unit='s')
    past=matches[ends.le(pd.Timestamp(cutoff))]
    history=HistoricalRecommender.from_frames(past,players[players.gameid.isin(past.gameid)])
    kwargs=dict(historical=history,meta_policy=MetaPolicy(as_of=cutoff,patch=patch),explain_matchups=False)
    current=DraftAdvisor(**kwargs);simple=DraftAdvisor(**kwargs,policy=AdvisorPolicy(scoring='simple'))
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    report={'protocol':'same_pool_frozen_series_pick_formula_comparison_v1','region':region,'patch':patch,
        'cutoff':cutoff,'series_ids':ids,'states_manifest':manifest,'query_limit_per_split':limit,
        'history_games':int(history.matches.gameid.nunique()),'meta_scope':current.context(region)[0].metadata(),
        'default_before':'current','default_after':'current','automatic_promotion':False,
        'simple_formula':'mean(available frequency, cosine, same-role WR); explicit overall-WR fallback',
        'results':{},'limitations':['Reused Pro audit data: development comparison, not a fresh independent final test.',
            'Recall/MRR retrieve observed picks, not tactical quality/counter/win improvement.',
            'No weight tuning or test-driven formula changes; no Rank or postgame query resources used.',
            'Different missing-profile patterns change the count of averaged signals in simple.',
            'Simple scores same-role matchups only; synergy/team interactions remain descriptive.',
            'Reconstructed series IDs and existing flexible-role inference remain shared extensions.',
            'Bootstrap CI is conditional on this small sample; [0,0] does not prove equivalence.']}
    all_rows=[];component_rows=[]
    for part in ['validation','test']:
        selected=parts[part][:limit] if limit else parts[part]
        print(f'{part}: {len(selected)} queries',flush=True)
        rows,audit,examples=replay_pair(selected,current,simple,region)
        all_rows.extend(dict(r,partition=part) for r in rows)
        report['results'][part]={'metrics':{mode:metrics([r for r in rows if r['formula']==mode]) for mode in ['current','simple','recent_presence']},
            'delta_recall5_simple_minus_current':paired_interval(rows,'simple'),
            'top5_changes':sum(a['top5']!=b['top5'] for a,b in zip([r for r in rows if r['formula']=='current'],[r for r in rows if r['formula']=='simple'])),
            'same_candidate_role_pools_verified':True,'examples':examples}
        component_rows.extend({'partition':part,'component':c,**{k:audit[c,k] for k in ['active_queries','top1_changes','recall5_hit_changes','net_hit5_gain_current']}} for c in COMPONENTS)
    test=report['results']['test'];a=test['metrics']['current'];b=test['metrics']['simple']
    report['observed_test_decline']=b['recall_at_5']<a['recall_at_5'] or b['mrr_at_5']<a['mrr_at_5']
    report['decision']='Keep current default; simple is an explicit demo/comparison option. Independent tactical-quality evidence is unavailable.'
    report['db_sha256']=hashlib.sha256(DB_PATH.read_bytes()).hexdigest()
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('draft_advisor.py')]}
    write_json(output/'evaluation.json',report);write_json(output/'queries.json',all_rows)
    pd.DataFrame(component_rows).to_csv(output/'component_audit.csv',index=False,encoding='utf-8-sig')
    lines=['# So sánh công thức pick hiện tại và bản đơn giản','',
        'Cùng dữ liệu lịch sử đóng băng, cùng candidate/role pool và luật loại trừ. Không tự đổi bản chính.',
        'Dữ liệu đã dùng trong audit cũ; đây là so sánh phát triển, không phải independent final test.','',
        '| Tập | Công thức | Queries | Recall@5 | MRR@5 | Coverage |','|---|---|---:|---:|---:|---:|']
    deltas=[]
    for part,value in report['results'].items():
        for mode,m in value['metrics'].items():lines.append(f"| {part} | {mode} | {m['queries']} | {m['recall_at_5']:.4f} | {m['mrr_at_5']:.4f} | {m['candidate_coverage']:.4f} |")
        deltas.append(f"{part}: delta Recall@5 simple-current {value['delta_recall5_simple_minus_current']}; top5 đổi {value['top5_changes']}.")
    lines+=['']+deltas
    lines+=['',report['decision'],'','component_audit.csv chỉ đo độ nhạy khi bỏ từng thành phần trên cùng pool; thay top1 không chứng minh thành phần đó cần thiết về chiến thuật.','',
        '## Giới hạn','']+['- '+x for x in report['limitations']]
    (output/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--region',default='WLDS');p.add_argument('--patch',default='16.20')
    p.add_argument('--output',type=Path,default=ROOT/'reports/pick_scoring_comparison');p.add_argument('--limit-per-split',type=int,default=0)
    a=p.parse_args()
    if a.limit_per_split<0:p.error('Limit must be nonnegative; 0 means all queries')
    r=evaluate(a.region,a.patch,a.output,a.limit_per_split);print(json.dumps({'default':r['default_after'],'observed_test_decline':r['observed_test_decline']}))
