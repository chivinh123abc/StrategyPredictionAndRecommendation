"""Validate existing paired runs and summarize behavior, not match-win improvement."""
from itertools import combinations
import argparse
import json
from pathlib import Path
import numpy as np
from simulate_fearless_series import validate_game,markdown_report

ROOT=Path(__file__).resolve().parents[2]


def quick_view(series):
    teams=series['games'][0]['teams']
    lines=[f"# {teams['blue']}–{teams['red']}: {series.get('ban_strategy','legacy')}",'',
           'Số# là lượt toàn cục. * là pick không có đối đầu đủ mẫu với địch đã lộ; vẫn chọn gợi ý1 đểtest. Không có dấu* cũng chưa xác nhậncounter.']
    for n,g in enumerate(series['games'],1):
        lines+=['',f"## Ván{n} — {teams[g['first_pick_side']]} chọn trước",'',
                f"| Ban/Pick số | {teams['blue']} | {teams['red']} |",'|---|---|---|']
        counts={s:{'ban':0,'pick':0}for s in teams};rows={}
        for h in g['history']:
            counts[h['side']][h['action']]+=1;key=(h['action'],counts[h['side']][h['action']])
            star='*'if h['advice'].get('review_required')else''
            rows.setdefault(key,{})[h['side']]=f"#{h['turn']} {h['champion']}"+(f" ({h['role']})"if h['role']else'')+star
        order=[('ban',i)for i in range(1,4)]+[('pick',i)for i in range(1,4)]+[('ban',i)for i in range(4,6)]+[('pick',i)for i in range(4,6)]
        for action,i in order:lines.append(f"| {action.title()} {i} | {rows[action,i]['blue']} | {rows[action,i]['red']} |")
    return '\n'.join(lines)+'\n'


def summarize(directory=ROOT/'reports/legacy_contextual_comparison'):
    directory=Path(directory);runs={};metrics={}
    for name in ['legacy','contextual']:
        run=json.loads((directory/name/'series.json').read_text(encoding='utf-8'))
        if run.get('ban_strategy')!=name or not run['complete'] or len(run['games'])!=5:
            raise ValueError(f'{name}: wrong strategy or incomplete series')
        used=[]
        for g in run['games']:used=validate_game(g,used)
        if len(set(used))!=50:raise ValueError('Need50distinctpicks')
        runs[name]=run
        openings=[{h['champion']for h in g['history'][:6]}for g in run['games']]
        metrics[name]={'completed_games':5,'actions':100,'unique_picks':50,
             'distinct_opening_ban_sets':len({tuple(sorted(v))for v in openings}),
             'mean_pairwise_opening_jaccard':float(np.mean([len(a&b)/len(a|b)for a,b in combinations(openings,2)])),
             'review_required_picks':sum(h['advice'].get('review_required',False)for g in run['games']for h in g['history']if h['action']=='pick')}
        (directory/name/'QUICK_VIEW.md').write_text(quick_view(run),encoding='utf-8')
        (directory/name/'REPORT.md').write_text(markdown_report(run),encoding='utf-8')
    a,b=runs['legacy'],runs['contextual']
    if a['meta_scope']!=b['meta_scope']:raise ValueError('Snapshot mismatch')
    for x,y in zip(a['games'],b['games']):
        if x['rosters']!=y['rosters'] or x['first_pick_side']!=y['first_pick_side']:
            raise ValueError('Roster/schedule mismatch')
    if a['allow_statistical_auto']!=b['allow_statistical_auto']:raise ValueError('Test policy mismatch')
    report={'active_strategies':['legacy','contextual'],'snapshot':a['meta_scope'],'metrics':metrics,
            'checks':{'all_series_complete':True,'same_snapshot_rosters_schedule':True,'per_series_distinct_picks':50},
            'limitations':['Ban diversity does not establish better strategy or winrate.',
                           'Different ban policies lead to different subsequent picks and pools.',
                           'No response search or full BO5 optimization; manual weights remain.']}
    (directory/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# So sánh hiện hành: legacy và contextual','',
           'Chỉ hai chiến lược hiện hành; kết quả tìm nhánh cũ được lưu riêng như lịch sử, không nằm trong đánh giá này.',
           '', '| Chế độ | Draft hoàn thành | Pick không lặp | Tập6ban đầu khác nhau | Jaccard trung bình |','|---|---:|---:|---:|---:|']
    for name,m in metrics.items():
        lines.append(f"| {name} | {m['completed_games']} | {m['unique_picks']} | {m['distinct_opening_ban_sets']}/5 | {m['mean_pairwise_opening_jaccard']:.3f} |")
    lines+=['','| Ván | Legacy:T1Ban1–3 | Legacy:Gen.GBan1–3 | Contextual:T1Ban1–3 | Contextual:Gen.GBan1–3 |',
            '|---:|---|---|---|---|']
    for n,(x,y)in enumerate(zip(a['games'],b['games']),1):
        lines.append(f"| {n} | {', '.join(x['bans']['blue'][:3])} | {', '.join(x['bans']['red'][:3])} | {', '.join(y['bans']['blue'][:3])} | {', '.join(y['bans']['red'][:3])} |")
    lines+=['','- [Legacy: đủ100lượt](legacy/QUICK_VIEW.md)',
            '- [Contextual: đủ100lượt](contextual/QUICK_VIEW.md)',
            '- [Contextual: căn cứ từng lượt](contextual/REPORT.md)',
            '', 'Contextual lưu pool_impact và contextual_trace để giải thích chi phí tự cấm/lựa chọn địch còn lại. Không tìm nhánh phản ứng, không chứng minh counter hoặc tối ưu BO5. Số lượt ban khác nhau chỉ là thay đổi hành vi, không đo tăng thắng.']
    (directory/'COMPARISON.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,default=ROOT/'reports/legacy_contextual_comparison')
    summarize(p.parse_args().directory)
