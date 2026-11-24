"""Readable review of frozen contextual picks; diagnostics never alter strategy."""
from collections import Counter
import argparse
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
COMPONENTS=['meta','content','composition','mastery','matchup']


def review(audit_path=ROOT/'reports/contextual_pick_audit.json',output=ROOT/'reports/contextual_pick_review'):
    report=json.loads(Path(audit_path).read_text(encoding='utf-8'))
    source=json.loads(Path(report['source_session']).read_text(encoding='utf-8'))
    if source['ban_strategy']!='contextual':raise ValueError('This review requires a contextual series')
    decisions=report['decisions'];index={(d['game_number'],d['turn']):d for d in decisions}
    if len(index)!=len(decisions):raise ValueError('Duplicate audited turn')
    checked=0;alternative_count=0
    for n,game in enumerate(source['games'],1):
        if game.get('swaps'):raise ValueError('Swap history requires a separate state replay; do not silently use final assignments')
        picks={'blue':{},'red':{}};unavailable=set(game['used_champions'])
        for h in game['history']:
            if h['action']=='ban':unavailable.add(h['champion']);continue
            d=index[n,h['turn']];other='red'if h['side']=='blue'else'blue'
            if d['own_revealed']!=picks[h['side']] or d['enemy_revealed']!=picks[other]:raise ValueError('Future/missing revealed picks')
            if set(d['unavailable'])!=unavailable:raise ValueError('Wrong legal candidate pool')
            ev=d['original_pick_evidence']
            if not ev or d['original_rank_now']!=1:raise ValueError('Saved policy differs from the audited policy')
            if abs(round(ev['score']*100,2)-d['recorded_score'])>1e-8:raise ValueError('Saved score differs from recomputation')
            alternatives=d['alternatives']
            if len(alternatives)!=min(5,d['candidate_count']-1):raise ValueError('Missing available alternatives')
            for row in alternatives:
                if row['champion']==h['champion'] or row['champion']in unavailable:raise ValueError('Illegal or duplicate alternative')
                alternative_count+=1
            checked+=1;picks[h['side']][h['role']]=h['champion'];unavailable.add(h['champion'])
    if checked!=50:raise ValueError('Expected50savedpicks')
    blind=[d for d in decisions if not d['enemy_revealed']]
    unsupported=[d for d in decisions if d['original_pick_evidence']['review_required']]
    rare=[d for d in decisions if d['original_pick_evidence']['games']<source['evidence_min_games']]
    ablations={k:sum(d['diagnostic_ablations'][k]['top']!=d['original_pick']for d in decisions)for k in COMPONENTS}
    pair_status=Counter(e['status']for d in decisions for e in d['original_pick_evidence']['composition_evidence'])
    summary={'source':report['source_session'],'source_sha256':report['source_sha256'],
             'scope':'frozen_contextual_pick_audit_no_policy_change','picks_audited':checked,
             'no_enemy_revealed_picks':len(blind),'unsupported_enemy_context_picks':len(unsupported),
             'supported_enemy_context_picks':sum(bool(d['enemy_revealed'])and d['original_pick_evidence']['enemy_context_coverage']>0 for d in decisions),
             'sparse_candidates':[{'game':d['game_number'],'turn':d['turn'],'team':d['team'],'role':d['role'],
                                  'champion':d['original_pick'],'games':d['original_pick_evidence']['games']}for d in rare],
             'top1_changes_under_ablation':ablations,'pair_evidence_statuses':dict(pair_status),
             'checks':{'pre_action_state_matches_saved_history':True,'legal_alternatives_checked':alternative_count,
                       'saved_scores_and_top1_reproduced':checked,'no_model_training':True,'no_pick_policy_changed':True},
             'limitations':['All50picks are simulated outputs, not expert quality labels.',
                            'Ablation changes the scoring formula, not evidence of alternative match outcomes.',
                            'Same-role alternatives do not evaluate other pick roles or flex reassignment.',
                            'Co-pick data and whole-game outcomes do not establish mechanical synergy/counters.']}
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Rà soát50lượt pick contextual — T1/Gen.G','',
           'Đầu vào: 5draftWorlds cutoff13/11/2026 patchdataset16.20, contextual và chếđộtest chọn gợi ý1 khi thiếu tin cậy. Không sửa công thức/đổi lựa chọn, không train model trong audit này.',
           '', '## Kết quả chính','',
           f"- Đã tái dựng và đối chiếu{checked}trạng thái trước lượt; score/top1 khớp phiên đã lưu. Đây là tính tái lập, không chứng minh chọn đúng chiến thuật.",
           f"- {len(unsupported)}/50pick có địch đã lộ nhưng không có đối đầu đủ mẫu; {len(blind)}/50pick chưa thấy địch; {summary['supported_enemy_context_picks']}/50có ít nhất một đối đầu đủ mẫu. Có mẫu vẫn chưa chứng minh counter.",
           f"- Đã kiểm tra{alternative_count}phương án cùng role, hợp lệ tại đúng thời điểm. Nếu còn ít hơn3lựa chọn thì không bịa thêm cho đủ3–5.",
           f"- {len(rare)}pick dưới5trận; xem bảng riêng. Tướng ít mẫu là giới hạn bằng chứng, không tự động là lựa chọn yếu.",
           '', '| Bỏ thành phần để kiểm tra độ nhạy | Số lượt đổi top1 |','|---|---:|']
    for k,n in ablations.items():lines.append(f'| {k} | {n}/50 |')
    lines+=['','Các lượt có thể nhạy với nhiều thành phần nên không cộng các số trên thành số pick sai. Bỏ thành phần là chẩn đoán công thức, không là đề xuất thay đổi policy.',
            '', '## Các lựa chọn ít mẫu','', '| Ván | Lượt | Đội | Role | Pick | Số trận |','|---:|---:|---|---|---|---:|']
    for d in rare:lines.append(f"| {d['game_number']} | {d['turn']} | {d['team']} | {d['role']} | {d['original_pick']} | {d['original_pick_evidence']['games']} |")
    lines+=['','## Các vấn đề cần xử lý tiếp, chưa sửa trong lượt này','',
            '1. Thiếu bằng chứng đối đầu là vấn đề lớn nhất. Không dùng điểmmeta/cosine thay thế bằng chứng counter; cần phân biệt blindpick với cóđịch nhưng thiếu mẫu.',
            '2. Phối hợp làm đổi nhiều lựa chọn khi bỏ thành phần; cần kiểm chứng cặp ít mẫu và các giả định về tần suất đồngchọn, không coi top1 là đáp án chuẩn.',
            '3. Pool cuốiFearless buộc backoff tướng ít mẫu; báo cáo coverage và độ tin cậy trước khi kết luận chất lượng.',
            '4. Audit chỉ so tướng cùng role đang gán. Galio top/mid hoặc tướngflex khác chưa được so như nhiều cách phânvai; đây là phần cần thiết kế sau, không được kết luận Galio top sai chỉ vì hiếm.',
            '', '## Toàn bộ50lượt','',
            '| Ván | Lượt | Đội | Role | Pick | n | Địch lộ | Coverage | Chênh điểm với phương án2 | Phương án khác |',
            '|---:|---:|---|---|---|---:|---:|---:|---:|---|']
    for d in decisions:
        ev=d['original_pick_evidence'];gap=d['score_gap_to_best_alternative']
        lines.append(f"| {d['game_number']} | {d['turn']} | {d['team']} | {d['role']} | {d['original_pick']} | {ev['games']} | {len(d['enemy_revealed'])} | {ev['enemy_context_coverage']:.0%} | {f'{gap*100:.3f}'if gap is not None else '—'} | {', '.join(r['champion']for r in d['alternatives'][:3])or 'Không còn'} |")
    lines+=['','Chênh điểm tính trên thang100; không phải chênh xác suất thắng. Các alternative không được mô tả là tốt hơn về cơ chế.',
            '', '## Căn cứ từng lượt và top5phương án khác','']
    for d in decisions:
        ev=d['original_pick_evidence']
        lines +=[f"### Ván{d['game_number']} lượt{d['turn']}: {d['team']} — {d['original_pick']} ({d['role']}, {d['slot']})",'',
                 f"Đồng đội đã lộ: {json.dumps(d['own_revealed'],ensure_ascii=False)}. Địch đã lộ: {json.dumps(d['enemy_revealed'],ensure_ascii=False)}.",
                 f"Pool hợp lệ tại role:{d['candidate_count']}ứngviên. Pick:{ev['games']}trận; score:{ev['score']*100:.3f}điểm, baseline:{ev['base_priority']:.5f}, geometriclift:{ev['composition_lift']:.5f}.",
                 f"Đối đầu: coverage{ev['enemy_context_coverage']:.0%}, mechanical_counter_status={ev['mechanical_counter_status']}. Chưa có evaluatorcơchế.",'',
                 '| Thành phần | Giá trị | Trọng số |','|---|---:|---:|']
        for k,v in ev['score_components'].items():lines.append(f"| {k} | {v['value']:.5f} | {v['weight']:.3f} |")
        lines+=['','Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.',
                '', '| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |','|---|---:|---|']
        for pair in ev['composition_evidence']:lines.append(f"| {d['original_pick']}–{pair['ally']} ({d['role']}/{pair['ally_role']}) | {pair['games']}/{pair['anchor_games']} | {pair['status']} |")
        if not ev['composition_evidence']:lines.append('| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |')
        lines+=['','| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |','|---|---:|---:|---:|---|']
        for row in d['alternatives']:
            lines.append(f"| {row['champion']} | {row['score']*100:.3f} | {row['games']} | {row['enemy_context_coverage']:.0%} | {row['evidence_status']} |")
        if not d['alternatives']:lines.append('| Không còn ứng viên cùng role | — | — | — | Không bịa phương án |')
        changed=[f"bỏ{k}→{v['top']}"for k,v in d['diagnostic_ablations'].items()if v['top']!=d['original_pick']]
        lines+=['','Kiểm tra độ nhạy: '+('; '.join(changed)or 'Không đổi top1 với các ablation đã thử')+'.',
                f"Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):{d['original_rank_without_enemy_context']}. Không là đo tác động nhân quả.",'']
    lines+=['','## Nguồn và tái lập','',
            f"Audit JSON: `{Path(audit_path)}`; sourceSHA256:`{report['source_sha256']}`. File summary.json cùng thư mục lưu tổng hợp/checks; top_candidates/alternatives vàdiagnostic_ablations nằm trong auditJSON.",
            '', '```powershell',
            '.\\.venv\\Scripts\\python.exe src/07_recommender/audit_draft_choices.py --session reports/legacy_contextual_comparison/contextual/series.json --output reports/contextual_pick_audit',
            '.\\.venv\\Scripts\\python.exe src/07_recommender/review_contextual_picks.py',
            '```']
    (out/'REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2));return summary


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit',type=Path,default=ROOT/'reports/contextual_pick_audit.json')
    p.add_argument('--output',type=Path,default=ROOT/'reports/contextual_pick_review')
    args=p.parse_args();review(args.audit,args.output)
