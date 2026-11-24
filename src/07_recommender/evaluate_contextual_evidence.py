"""Frozen same-role Rank signal experiment; prospective gate plus labelled diagnostics."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/01_data_pipeline')]
from analysis_data import load_clean_tables,DB_PATH
from matchup_evidence import CATALOG,RANK_DB,SourceView,read_rank_snapshot,normalize_rank,available_before
from rank_data_contract import ChampionCatalog
from ranked_matchups import write_json
from historical_recommender import HistoricalRecommender,evidence
from draft_meta import MetaPolicy
from draft_states import build_states
from evaluate_rank_transfer import normalize_tables,split_series,TransferAdvisor,replay,metrics,paired_interval


class LaneRankEvidence:
    def __init__(self,rows):self.view=SourceView(rows)

    def evaluate(self,role,champ,masses,baseline,enemy_count,min_games,prior):
        residual=covered=0.;rows=[]
        for opponent,prob in masses.get(role,{}).items():
            found=self.view.lookup(role,champ,opponent);n=found['games']
            ev={**evidence(found['wins'],n),'enemy_role':role,'opponent':opponent,
                'role_probability':prob,'domain':'rank','status':'observed_context' if n>=min_games else 'insufficient_context'}
            rows.append(ev)
            if n>=min_games:
                residual+=prob*(found['winrate']-baseline)*n/(n+prior);covered+=prob
        return float(np.clip(.5+residual/max(1,enemy_count),0,1)),rows,covered/max(1,enemy_count)


def freeze_records(rows):
    return rows.astype(object).where(rows.notna(),None).to_dict('records')


def prospective_partitions(states,freeze,validation_series=5,test_series=5):
    groups={}
    for state in states:
        if state['action']=='pick':groups.setdefault(state['series_id'],[]).append(state)
    eligible={k:v for k,v in groups.items() if min(pd.Timestamp(s['date']) for s in v)>pd.Timestamp(freeze)}
    ordered=sorted(eligible,key=lambda k:min(s['date'] for s in eligible[k]))
    a,b=validation_series,validation_series+test_series
    ids={'validation':ordered[:a],'test':ordered[a:b]}
    partitions={name:sorted([s for sid in series for s in eligible[sid]],key=lambda s:(s['date'],s['gameid'],s['turn'])) for name,series in ids.items()}
    separated=not (partitions['validation'] and partitions['test']) or (
        max(s['date'] for s in partitions['validation'])<min(s['date'] for s in partitions['test']))
    return partitions,ids,len(ordered)>=b and separated


def summarize(rows):
    result={}
    for part in ['validation','test']:
        subset=[r for r in rows if r['partition']==part]
        control=[r for r in subset if r['mode']=='pro_only']
        result[part]={'metrics':{mode:metrics([r for r in subset if r['mode']==mode]) for mode in ['pro_only','rank_only','hybrid']},
            'delta_recall5':{mode:paired_interval(subset,mode) for mode in ['rank_only','hybrid']},
            'top5_changed':{mode:sum(a['top5']!=b['top5'] for a,b in zip(control,[r for r in subset if r['mode']==mode])) for mode in ['rank_only','hybrid']}}
    return result


def run(args):
    catalog=ChampionCatalog.read(args.catalog)
    output=args.output;output.mkdir(parents=True,exist_ok=True)
    if args.freeze:
        frozen=json.loads(args.freeze.read_text(encoding='utf-8'))
        rank=pd.DataFrame(frozen['rank_rows']);freeze=frozen['freeze_at'];private=args.freeze.resolve()
    else:
        rank,unknown=normalize_rank(read_rank_snapshot(args.rank_db),catalog)
        freeze=pd.Timestamp.now(tz='UTC').isoformat()
        rank=available_before(rank,freeze)
        sid=pd.Timestamp(freeze).strftime('%Y%m%dT%H%M%S%fZ')
        private=ROOT/'data/raw/contextual_evidence_experiments'/sid/'freeze.json'
        frozen={'freeze_at':freeze,'catalog_version':catalog.version,'unknown_rank_games_excluded':unknown,
            'region':args.region,'patch':args.patch,
            'rank_rows':freeze_records(rank),'hybrid_weight':.5,'min_games':5,
            'validation_series':5,'test_series':5,'rank_patch_scope':'all observed','rank_tier':'Master+ current snapshots, not historical tier'}
        write_json(private,frozen)
    if frozen['catalog_version']!=catalog.version:raise ValueError('Frozen catalog mismatch')
    if frozen.get('region')!=args.region or frozen.get('patch')!=args.patch:raise ValueError('Frozen region/patch mismatch')
    rank=available_before(rank,freeze)
    _,matches,players=load_clean_tables()
    matches,players,_=normalize_tables(matches,players,catalog)
    states,manifest=build_states(matches,args.region)
    parts,ids,ready=prospective_partitions(states,freeze)
    strict={'rank_games_frozen':int(rank.match_id.nunique()) if len(rank) else 0,'freeze_at':freeze,
        'pro_latest_date':pd.to_datetime(matches.date,utc=True).max().isoformat(),
        'prospective_series':{k:len(v) for k,v in ids.items()},'ready':ready,
        'result':None,'status':'ready' if ready else 'awaiting_prospective_pro_series',
        'policy':'next 5 complete reconstructed series validation, following 5 test; no tuning; all start after freeze',
        'private_freeze':str(private.relative_to(ROOT)) if private.is_relative_to(ROOT) else str(private),
        'private_freeze_sha256':hashlib.sha256(private.read_bytes()).hexdigest(),
        'state_manifest':manifest,'main_score_changed':False}
    if ready:
        rows=run_replay(parts,matches,players,rank,freeze,args)
        strict['result']=summarize(rows)
        write_json(output/'prospective_queries.json',rows)
    write_json(output/'prospective_readiness.json',strict)
    report={'protocol':'contextual_same_role_rank_supplement_v1','prospective':strict,
        'diagnostic':None,'integration_enabled':False,'promotion_allowed':False,
        'only_changed_component':'matchup; Pro control unchanged, Rank same-role, hybrid fixed 50/50 supported pairs; no gold/XP/CS postgame features',
        'rank_scope':'all frozen patches/servers, common official champion identity; current Master+ snapshot proxy',
        'metrics_meaning':'observed-pick retrieval; not win uplift, probability calibration, ban quality or optimal BO5',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'pro_db_sha256':hashlib.sha256(DB_PATH.read_bytes()).hexdigest()}
    if args.retrospective_diagnostic:
        diagnostic_parts,diagnostic_ids=split_series(states,args.patch)
        cutoff=(pd.to_datetime(diagnostic_parts['validation'][0]['date'],utc=True)-pd.Timedelta(nanoseconds=1)).isoformat()
        selected={k:v[:args.max_queries_per_split] if args.max_queries_per_split else v for k,v in diagnostic_parts.items() if k!='history'}
        rows=run_replay(selected,matches,players,rank,cutoff,args)
        write_json(output/'diagnostic_queries.json',rows)
        legal=available_before(rank,cutoff)
        report['diagnostic']={'status':'retrospective_behavior_diagnostic_not_independent_evaluation',
            'pro_history_cutoff':cutoff,'series_ids':diagnostic_ids,
            'rank_games_actually_known_at_cutoff':int(legal.match_id.nunique()) if len(legal) else 0,
            'uses_post_cutoff_rank':len(legal)!=len(rank),'reused_pro_dataset':True,
            'query_limit_per_split':args.max_queries_per_split,'results':summarize(rows),
            'promotion_eligible':False}
    if strict['result']:
        test=strict['result']['test'];delta=test['delta_recall5']['hybrid']
        report['retrieval_review_gate_passed']=bool(delta['ci95'] and delta['ci95'][0]>0 and
            test['metrics']['hybrid']['mrr_at_5']>=test['metrics']['pro_only']['mrr_at_5'])
        report['promotion_meaning']='eligible for human review of retrieval improvement only; does not automatically change runtime'
    write_json(output/'evaluation.json',report)
    text=['# Contextual Pro / Rank: thử nghiệm tín hiệu đối đầu','',
        f"Freeze: {freeze}. Rank: {strict['rank_games_frozen']} trận. Prospective ready: {ready}.",
        'Bản chính không thay điểm. Rank và Pro không trộn số trận; hybrid chỉ trộn residual ở kèo Rank đủ mẫu.',
        'Chưa có dữ liệu giải độc lập sau freeze thì kết quả prospective để null, không tạo metric giả.','',
        'Thống kê vàng/XP/CS chỉ để giải thích; tín hiệu thử nghiệm dùng kết quả thắng lịch sử cùng role.','']
    for name,value in [('prospective',strict['result']),('diagnostic',report['diagnostic']['results'] if report['diagnostic'] else None)]:
        if not value:continue
        text+=['## '+name,'']
        if name=='diagnostic':text+=['**Thăm dò hành vi trên dữ liệu cũ; có thể dùng Rank thu sau trận giải. Không chứng minh nâng chất lượng, không dùng để promote.**','']
        text+=['| Tập | Mode | Queries | Recall@5 | MRR@5 | Rank hỗ trợ |','|---|---|---:|---:|---:|---:|']
        for part,values in value.items():
            for mode,m in values['metrics'].items():text.append(f"| {part} | {mode} | {m['queries']} | {m['recall_at_5']} | {m['mrr_at_5']} | {m.get('queries_with_supported_rank_candidate')} |")
        for part,v in value.items():text.append(f"\n{part}: delta Recall@5 hybrid={v['delta_recall5']['hybrid']}; changed top5={v['top5_changed']['hybrid']}.")
    text+=['','Series được tái dựng, chưa phải ID giải chính thức. N5 và 5+5 series là policy thử nghiệm, không bảo đảm power. CI bootstrap suy biến không chứng minh tương đương. Điểm không phải xác suất thắng.']
    (output/'REPORT.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    return report


def run_replay(parts,matches,players,rank,cutoff,args):
    ends=pd.to_datetime(matches.date,utc=True)+pd.to_timedelta(matches.gamelength,unit='s')
    history=matches[ends.le(pd.Timestamp(cutoff))]
    hist=HistoricalRecommender.from_frames(history,players[players.gameid.isin(history.gameid)])
    advisor=TransferAdvisor(historical=hist,meta_policy=MetaPolicy(as_of=cutoff,patch=args.patch),
        rank_evidence=LaneRankEvidence(rank),explain_matchups=False)
    rows=[]
    for part in ['validation','test']:
        print(f'{part}: {len(parts[part])} queries x 3 modes',flush=True)
        rows.extend(dict(r,partition=part) for r in replay(parts[part],advisor,args.region))
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'reports/contextual_rank_experiment')
    p.add_argument('--rank-db',type=Path,default=RANK_DB);p.add_argument('--catalog',type=Path,default=CATALOG)
    p.add_argument('--freeze',type=Path);p.add_argument('--region',default='WLDS');p.add_argument('--patch',default='16.20')
    p.add_argument('--retrospective-diagnostic',action='store_true');p.add_argument('--max-queries-per-split',type=int,default=30)
    a=p.parse_args()
    if a.max_queries_per_split<0:p.error('Query limit must be nonnegative; 0 means all queries')
    result=run(a);print(json.dumps({'prospective_ready':result['prospective']['ready'],'promotion_allowed':result['promotion_allowed']}))
