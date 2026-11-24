"""Run and audit consecutive Fearless drafts; no fabricated game outcomes."""
import argparse
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(Path(__file__).resolve().parent)]
from draft_advisor import DraftAdvisor,AdvisorPolicy,ROLES
from draft_meta import MetaPolicy
from recommender_engine import RecommenderEngine
from simulate_draft_match import run_pro_tournament_draft_simulation,draft_schedule

RULE_SOURCE='https://lolesports.com/en-GB/news/fst-2025-primer'


def validate_game(game,used):
    """Check draft order and carry only previously picked champions, never bans."""
    if not game['complete'] or len(game['history'])!=20:raise ValueError('Incomplete draft; no fabricated completion')
    if set(game['used_champions'])!=set(used):raise ValueError('Incorrect Fearless lock pool')
    if [(h['side'],h['action']) for h in game['history']]!=draft_schedule(game['first_pick_side']):
        raise ValueError('Invalid draft turn order')
    champions=[h['champion'] for h in game['history']]
    if len(set(champions))!=20 or set(champions)&set(used):raise ValueError('Duplicate or Fearless-locked champion')
    for side in ['blue','red']:
        if set(game['picks'][side])!=set(ROLES) or len(game['bans'][side])!=5:
            raise ValueError('Invalid role/ban count')
    picked=[c for picks in game['picks'].values() for c in picks.values()]
    actions_picked=[h['champion'] for h in game['history'] if h['action']=='pick']
    actions_banned=[h['champion'] for h in game['history'] if h['action']=='ban']
    if sorted(picked)!=sorted(actions_picked) or sorted(sum(game['bans'].values(),[]))!=sorted(actions_banned):
        raise ValueError('Board and action history disagree')
    return list(used)+picked


def markdown_report(report):
    teams=report['games'][0]['teams']
    lines=[f"# {report['region']}: {len(report['games'])} ván draft Fearless — {teams['blue']} vs {teams['red']}",'',
           'Đây là 5 phiên draft liên tiếp, không mô phỏng trận chiến hoặc gán tỉ số thắng/thua. Không dùng kết quả giả để ép BO5 đi đủ5ván.',
           '',f"Luật: [Fearless của Riot]({RULE_SOURCE}). Tướng đã pick bởi bất kỳ đội nào bị khóa cho cả hai đội đến hết series; ban thường chỉ có hiệu lực trong ván đó. Ván5 không reset pool.",
           '',f"Snapshot: `{report['meta_scope']}`.",
           '',f"Lịch thử nghiệm: giữ {teams['blue']} ở Blue và {teams['red']} ở Red; đội chọn trước từng ván: {', '.join(g['first_pick_side'] for g in report['games'])}. Quyền chọn trước độc lập màu đội, theo cấu hình người dùng; không suy từ thắng/thua. Nguồn luật Fearless bên trên không xác nhận một luật First Selection mới.",
           '',f"Cho phép test chọn số1 khi thiếu tin cậy: {report.get('allow_statistical_auto',False)}. Không nâng nhãn counter hoặc độ tin cậy khi bật chế độ này.",
           '',f"Chiến lược ban: {report.get('ban_strategy','legacy')}. Chỉ legacy/contextual; không tìm nhánh phản ứng hoặc tối ưu toàn BO5.",
           '',f"Ứng viên: ít nhất {report['candidate_min_games']} lần quan sát đúng role; ngưỡng bằng chứng {report['evidence_min_games']} trận. Ưu tiên ứng viên đủ mẫu trước; chỉ xét lớp ít mẫu khi không còn ứng viên đủ mẫu ở role đang xét. Khi so giữa các role mở cũng ưu tiên lớp đủ mẫu; người dùng wishlist vẫn là lựa chọn chủ đích riêng. Đây là pool gợi ý có dữ liệu, chưa là danh mục tướng hợp lệ chính thức của sự kiện.",
           '',f"Cách tính điểm pick: {report.get('pick_scoring','current')}.",
           '', ('Simple: trung bình tần suất chọn, cosine nếu có và WR đối đầu cùng role; thiếu matchup dùng WR lịch sử có nhãn. Không dùng synergy/lift/odds để chấm điểm. Thống kê cặp ở dưới chỉ để tham khảo.' if report.get('pick_scoring')=='simple' else
           'Association dương được shrink thêm theo số mẫu cặp; association âm theo số quan sát đồng đội. Không cho một cặp một-mẫu tạo bonus lift lớn như cặp có nhiều mẫu.')]
    for n,g in enumerate(report['games'],1):
        lines+=['',f"## Ván {n} — {g['teams'][g['first_pick_side']]} chọn trước",'',
                f"Fearless khóa {len(g['used_champions'])} tướng từ các ván trước.",'',
                '| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |',
                '|---|---|---|']
        for side in ['blue','red']:
            b=g['bans'][side]
            lines.append(f"| {g['teams'][side]} | {', '.join(b[:3])} | {', '.join(b[3:])} |")
        lines+=['',f"| Vị trí | {teams['blue']} | {teams['red']} |",'|---|---|---|']
        for role in ROLES:lines.append(f"| {role} | {g['picks']['blue'][role]} | {g['picks']['red'][role]} |")
        lines+=['','### Toàn bộ20lượt','', '| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |','|---:|---|---|---|---|---|']
        counts={side:{'ban':0,'pick':0}for side in ['blue','red']}
        for h in g['history']:
            counts[h['side']][h['action']]+=1
            label=f"{h['action'].title()} {counts[h['side']][h['action']]}"
            ev=h.get('advice',{})
            confidence=('Thiếu mẫu — test chọn số1' if ev.get('review_required') else
                        'Chưa lộ địch' if not ev.get('enemy_context_evidence') else
                        f"Coverage {ev.get('enemy_context_coverage',0):.0%}; chưa xác nhận counter") if h['action']=='pick' else 'Điểm cấm thống kê'
            lines.append(f"| {h['turn']} | {g['teams'][h['side']]} | {label} | {h['champion']} | {h['role'] or '—'} | {confidence} |")
        sparse=[f"{g['teams'][h['side']]} {h['champion']} ({h['advice']['games']} trận)" for h in g['history']
                if h['action']=='pick' and h['advice'].get('evidence_status')=='sparse_candidate']
        lines+=['','Lựa chọn ít mẫu: '+('; '.join(sparse) if sparse else 'không có dưới ngưỡng5trận')+'.']
        lines+=['','### Căn cứ từng lượt pick','',
            '| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |','|---:|---|---|---:|---|---|']
        for h in g['history']:
            if h['action']!='pick':continue
            advice=h['advice']
            components='; '.join(f"{k}={v['value']:.3f}" for k,v in advice.get('score_components',{}).items())
            pairs='; '.join(f"{e['opponent']} n={e['games']}" for e in advice.get('matchup_candidates',[])) or 'Chưa lộ/không suy được cùng role'
            if advice.get('review_required'):pairs+='; thiếu hỗ trợ, test chọn số1'
            if advice.get('matchup_scope')=='same_role_only':pairs+='; chưa chấm tương tác khác role'
            lines.append(f"| {h['turn']} | {g['teams'][h['side']]} | {h['champion']} | {advice['ranking_score']} | {components} | {pairs} |")
        for side in ['blue','red']:
            c=g['composition_summary'][side]
            lines.append(f"Cặp {g['teams'][side]}: đủ mẫu {c['observed_pairs']}, ít mẫu {c['sparse_pairs']}, chưa thấy {c['unobserved_pairs']}, thiếu anchor {c['insufficient_anchor_pairs']}.")
        searched=[h for h in g['history']if h['action']=='ban' and h.get('advice',{}).get('contextual_trace')]
        if searched:
            lines+=['','### Căn cứ từng lượt ban','',
                    '| Lượt | Đội | Ban | Lý do | Ghi chú |','|---:|---|---|---|---|']
            for h in searched:
                advice=h['advice']
                lines.append(f"| {h['turn']} | {g['teams'][h['side']]} | {h['champion']} | {advice['reason']} | Không tìm nhánh phản ứng |")
    lines+=['','## Kiểm chứng','',json.dumps(report['checks'],ensure_ascii=False,indent=2),
            '', 'Giới hạn: chọn tham lam theo từng lượt; chưa tối ưu phân bổ champion pool cho cả series, chưa có mô hình tương tác3/5tướng hoặc combat simulator. Chưa chứng minh tăng thắng.']
    return '\n'.join(lines)+'\n'


def first_selection_order(games,first_picks=None):
    if games not in range(1,6):raise ValueError('Choose 1..5 draft games')
    if first_picks is None and games>1:
        raise ValueError('Chọn rõ đội đi trước từng ván bằng --first-picks, ví dụ blue,blue,blue,blue,blue. Không tự luân phiên.')
    if first_picks is not None and (len(first_picks)!=games or any(s not in ['blue','red'] for s in first_picks)):
        raise ValueError('Choose one blue/red first-selection team for every game')
    return list(first_picks) if first_picks is not None else ['blue']


def run_series(blue='Gen.G',red='Bilibili Gaming',region='WLDS',as_of='2026-11-13',patch='16.20',
               games=5,candidate_min_games=1,output_dir=ROOT/'reports/worlds_fearless_bo5',opponent_model_path=None,
               allow_statistical_auto=False,ban_strategy='legacy',pick_scoring='current',first_picks=None):
    order=first_selection_order(games,first_picks)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    advisor=DraftAdvisor(policy=AdvisorPolicy(candidate_min_games=candidate_min_games,scoring=pick_scoring),
                         meta_policy=MetaPolicy(as_of=as_of,patch=patch))
    engine=RecommenderEngine();snapshot,_,_=advisor.context(region)
    report={'mode':'five_drafts_no_game_results','rule_source':RULE_SOURCE,'region':region,
            'allow_statistical_auto':allow_statistical_auto,
            'ban_strategy':ban_strategy,
            'pick_scoring':pick_scoring,
            'meta_scope':snapshot.metadata(),'candidate_min_games':candidate_min_games,
            'evidence_min_games':advisor.policy.min_games,'games':[],'complete':False,
            'schedule':'Fixed Blue/Red teams; explicitly configured first selection independent of map side',
            'first_selection_policy':'user_configured' if first_picks is not None else 'single_game_default_blue',
            'first_picks':order,'first_selection_rule_source':'user session configuration; Fearless reference above does not establish this rule'}
    used=[]
    for n in range(1,games+1):
        first=order[n-1]
        with redirect_stdout(StringIO()) as log:
            game=run_pro_tournament_draft_simulation(blue,red,interactive=False,region=region,
                  first_side=first,advisor=advisor,engine=engine,used_champions=used,
                  save_session=out/f'game_{n}.json',opponent_model_path=opponent_model_path,
                  allow_statistical_auto=allow_statistical_auto,ban_strategy=ban_strategy)
        (out/f'game_{n}.log').write_text(log.getvalue(),encoding='utf-8')
        report['games'].append(game)
        if not game['complete']:
            (out/'series.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            if game.get('manual_review'):raise ValueError(f'Game {n} requires tactical review; unsupported pick not auto-finalized. Partial evidence saved.')
            raise ValueError(f'Game {n} cannot complete with the supported candidate pool; partial evidence saved')
        used=validate_game(game,used)
        print(f"Game {n}: complete, {len(game['used_champions'])} Fearless locks, {len(used)} unique picks used",flush=True)
    report['complete']=True
    report['checks']={'completed_games':len(report['games']),'total_actions':sum(len(g['history']) for g in report['games']),
                      'unique_picks_across_series':len(set(used)),'no_repeated_pick':len(used)==len(set(used)),
                      'prior_lock_counts':[len(g['used_champions']) for g in report['games']],
                      'draft_order_legal':True,'no_locked_champion_picked_or_banned':True,
                      'only_picks_carry_over_not_standard_bans':True}
    (out/'series.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'REPORT.md').write_text(markdown_report(report),encoding='utf-8')
    print('Saved',out/'REPORT.md')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blue-team',default='Gen.G');parser.add_argument('--red-team',default='Bilibili Gaming')
    parser.add_argument('--region',default='WLDS');parser.add_argument('--as-of',default='2026-11-13')
    parser.add_argument('--patch',default='16.20');parser.add_argument('--games',type=int,default=5)
    parser.add_argument('--candidate-min-games',type=int,default=1)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'reports/worlds_fearless_bo5')
    parser.add_argument('--opponent-model',type=Path,nargs='?',const=ROOT/'models/opponent_model.pkl')
    parser.add_argument('--allow-statistical-auto',action='store_true',help='Test: chốt gợi ý số1 dù thiếu tin cậy; giữ nguyên nhãn bằng chứng')
    parser.add_argument('--ban-strategy',choices=['legacy','contextual'],default='legacy')
    parser.add_argument('--pick-scoring',choices=['current','simple'],default='current')
    parser.add_argument('--first-picks',help='Comma-separated blue/red for each game, independent of map side')
    args=parser.parse_args()
    if args.games>1 and not args.first_picks:parser.error('Cần --first-picks cho từng ván; có thể blue,blue,blue,blue,blue hoặc red,red,red,red,red.')
    run_series(args.blue_team,args.red_team,args.region,args.as_of,args.patch,args.games,args.candidate_min_games,args.output_dir,args.opponent_model,args.allow_statistical_auto,args.ban_strategy,args.pick_scoring,
               [s.strip().lower() for s in args.first_picks.split(',')] if args.first_picks else None)
