"""Compare every saved pick with legal alternatives at that exact public state."""
import argparse
import hashlib
import json
from pathlib import Path
from draft_advisor import DraftAdvisor,AdvisorPolicy
from draft_meta import MetaPolicy

ROOT=Path(__file__).resolve().parents[2]


def compact(row):
    return {k:row[k] for k in ['champion','score','games','historical','evidence_status','score_components',
            'base_priority','composition_lift','enemy_context_coverage','enemy_context_evidence',
            'mechanical_counter_status','selection_basis','review_required','composition_evidence',
            'player_history','cosine_similarity','score_formula','reasons'] if k in row}


def diagnostic_score(row,without):
    """Diagnostic ablation only; never changes simulator scoring or saved decisions."""
    parts=row['score_components']
    base_parts={k:p for k,p in parts.items()if k!='composition' and k!=without}
    weight=sum(p['weight'] for p in base_parts.values())
    if not weight:raise ValueError('No base components after ablation')
    base=sum(p['value']*p['weight']for p in base_parts.values())/weight
    factor=1. if without=='composition' else row['composition_lift']**parts.get('composition',{}).get('weight',0)
    return base*factor/(1-base+base*factor)


def ablation(ranked,champion,without):
    order=sorted(ranked,key=lambda r:(r.get('evidence_status')=='sparse_candidate',-diagnostic_score(r,without),-r['games'],r['champion']))
    return {'removed_component':without,'top':order[0]['champion'] if order else None,
            'original_rank':next((i+1 for i,r in enumerate(order)if r['champion']==champion),None),
            'interpretation':'sensitivity_of_same_candidate_pool_not_alternative_match_outcome'}


def audit(path=ROOT/'reports/worlds_fearless_bo5/series.json',output=ROOT/'reports/draft_choice_audit'):
    source=json.loads(Path(path).read_text(encoding='utf-8'))
    games=source.get('games',[source]);advisors={};decisions=[]
    for number,game in enumerate(games,1):
        meta=game['meta_scope'];key=json.dumps([meta,game['policy'],game.get('candidate_min_games',5)],sort_keys=True)
        if key not in advisors:
            advisors[key]=DraftAdvisor(policy=AdvisorPolicy(weights=game['policy'],min_games=game.get('evidence_min_games',5),
                         candidate_min_games=game.get('candidate_min_games',5)),
                         meta_policy=MetaPolicy(as_of=meta['requested_as_of'],patch=meta['dataset_patch'],
                             lookback_days=meta['lookback_days'],half_life_days=meta['half_life_days']))
        advisor=advisors[key];picks={'blue':{},'red':{}};banned=set(game['used_champions'])
        for h in game['history']:
            side=h['side'];other='red' if side=='blue' else 'blue'
            if h['action']=='ban':banned.add(h['champion']);continue
            role=h['role'];unavailable=banned|set(picks['blue'].values())|set(picks['red'].values())
            slot=('F' if side==game['first_pick_side'] else 'S')+str(len(picks[side])+1)
            kwargs=dict(already_banned=unavailable,player_name=game['rosters'][side].get(role),
                        region=game['region'],top_k=10000,draft_slot=slot)
            ranked=advisor.recommend_picks(role,picks[side],picks[other],**kwargs)
            blind=advisor.recommend_picks(role,picks[side],{},**kwargs)
            original=next((r for r in ranked if r['champion']==h['champion']),None)
            other_rows=[r for r in ranked if r['champion']!=h['champion']]
            decisions.append({'game_number':number,'turn':h['turn'],'team':game['teams'][side],'role':role,
                'slot':slot,'actor_side':side,'player':game['rosters'][side].get(role),'meta_scope':meta,
                'original_pick':h['champion'],'own_revealed':dict(picks[side]),'enemy_revealed':dict(picks[other]),
                'unavailable':sorted(unavailable),'original_rank_now':next((i+1 for i,r in enumerate(ranked) if r['champion']==h['champion']),None),
                'original_pick_evidence':compact(original) if original else None,
                'original_rank_without_enemy_context':next((i+1 for i,r in enumerate(blind) if r['champion']==h['champion']),None),
                'top_candidates':[compact(r) for r in ranked[:5]],
                'alternatives': [compact(r) for r in other_rows[:5]],
                'candidate_count':len(ranked),
                'score_gap_to_best_alternative':original['score']-other_rows[0]['score'] if original and other_rows else None,
                'diagnostic_ablations':{key:ablation(ranked,h['champion'],key)for key in ['meta','content','composition','mastery','matchup']},
                'recorded_score':h.get('advice',{}).get('ranking_score'),
                'top_choice_changed':bool(ranked and ranked[0]['champion']!=h['champion']),
                'counter_claim':'not_established_mechanics_evaluator_missing'})
            picks[side][role]=h['champion']
    report={'source_session':str(path),'protocol':'frozen_saved_state_all_picks_same_role_same_legal_pool',
            'source_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'decisions':decisions,'checks':{'picks_audited':len(decisions),
              'top_choice_changed_count':sum(r['top_choice_changed'] for r in decisions),
              'mechanical_counter_claims':0},
            'limitations':['Cross-role outcomes are observational; five opponents are not independent experiments.',
                          'No verified patch-specific skills/items/engage/frontline evaluator; no mechanical counter claims.',
                          'This compares priorities, not counterfactual match outcomes or proof of better alternatives.']}
    output=Path(output);output.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Audit lựa chọn tại đúng lượt draft','',
           'Đối chiếu mọi lượt chọn, không loại/gán điểm riêng một tên tướng. Cột top mới là ưu tiên thống kê, không chứng minh mạnh hơn về cơ chế hoặc tăng thắng.',
           '', '| Ván | Lượt | Đội | Role | Pick đã lưu | Rank hiện tại | Top hiện tại | Coverage địch của pick cũ |',
           '|---:|---:|---|---|---|---:|---|---:|']
    for d in decisions:
        ev=d['original_pick_evidence'];top=d['top_candidates'][0]['champion'] if d['top_candidates'] else '—'
        lines.append(f"| {d['game_number']} | {d['turn']} | {d['team']} | {d['role']} | {d['original_pick']} | {d['original_rank_now']} | {top} | {ev['enemy_context_coverage']:.0%} |" if ev else
                     f"| {d['game_number']} | {d['turn']} | {d['team']} | {d['role']} | {d['original_pick']} | — | {top} | thiếu dữ liệu |")
    lines+=['','Mỗi lượt có top5 ứng viên, điểm từng thành phần, số mẫu/CI và trạng thái cơ chế trong JSON cùng tên. Chưa có nhãn counter được chuyên gia xác nhận hoặc evaluator cơ chế, vì vậy không xác nhận bất kỳ pick nào là counter tối ưu.']
    output.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(report['checks'],ensure_ascii=False))
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--session',type=Path,default=ROOT/'reports/worlds_fearless_bo5/series.json')
    p.add_argument('--output',type=Path,default=ROOT/'reports/draft_choice_audit');a=p.parse_args();audit(a.session,a.output)
