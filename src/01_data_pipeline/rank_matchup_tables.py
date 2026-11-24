"""Own descriptive tables inspired by public U.GG winrate/GD15 separation.

Not a reproduction of proprietary methodology, a calibrated draft predictor,
or a causal mechanical-counter evaluator. Sparse rows always remain visible.
"""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t

from ranked_matchups import METRICS, write_json
from historical_recommender import wilson

SCOPE=['platform','queue','patch','tier_floor','role']
KEYS=SCOPE+['champion_id','opponent_id']


def aggregate(rows,min_games=5,pooled=False,target_games=None):
    if min_games<1 or (target_games is not None and target_games<1): raise ValueError('Sample thresholds must be positive')
    output=[]
    if rows.empty: return pd.DataFrame(columns=KEYS+['champion','opponent','games','winrate','gold_diff_15_mean'])
    rows=rows.drop_duplicates(['match_id','team_id','role'])
    rows=rows.copy()
    rows['_source_patch']=rows['patch'].astype(str)
    rows['_source_platform']=rows['platform'].astype(str)
    if pooled:
        rows['patch']='ALL_OBSERVED'
        rows['platform']='ALL_OBSERVED'
    for keys,group in rows.groupby(KEYS,dropna=False):
        n=int(group.match_id.nunique()); wins=int(group.win.sum())
        low,high=wilson(wins,n)
        row={**dict(zip(KEYS,keys)),'champion':group.champion.iloc[0],'opponent':group.opponent.iloc[0],
             'games':n,'wins':wins,'winrate':wins/n,'win_ci95_low':low,'win_ci95_high':high,
             'champion_players':int(group._puuid.nunique()),'opponent_players':int(group._enemy_puuid.nunique()),
             'unique_players':len(set(group._puuid)|set(group._enemy_puuid)),
             'evidence_status':'observed' if n>=min_games else 'insufficient_samples'}
        row.update(patch_count=int(group._source_patch.nunique()),
            patches=json.dumps(sorted(group._source_patch.unique().tolist())),
            platform_count=int(group._source_platform.nunique()),
            platforms=json.dumps(sorted(group._source_platform.unique().tolist())),
            target_games=target_games,games_remaining=max(0,target_games-n) if target_games is not None else None,
            target_reached=n>=target_games if target_games is not None else None)
        patch_means=group.assign(_gold=pd.to_numeric(group.get('gold_diff_15',pd.Series(index=group.index,dtype=float)),errors='coerce')).groupby('_source_patch')._gold.agg(['count','mean'])
        patch_means=patch_means[patch_means['count'].ge(min_games)]
        row['supported_patch_count']=len(patch_means)
        row['gd15_patch_direction']=('insufficient_patch_evidence' if len(patch_means)<2 else
            'mixed_directions' if (patch_means['mean'].gt(0).any() and patch_means['mean'].lt(0).any()) else
            'same_direction_observed')
        # Direction is descriptive, not a significance test or a stability guarantee.
        row['patch_gd15_details']=json.dumps({str(p):{'n':int(v['count']),'mean':float(v['mean'])} for p,v in patch_means.iterrows()},sort_keys=True)
        for metric in METRICS:
            values=pd.to_numeric(group[metric],errors='coerce').dropna() if metric in group else pd.Series(dtype=float)
            count=len(values); mean=float(values.mean()) if count else None
            sd=float(values.std(ddof=1)) if count>1 else None
            half=float(t.ppf(.975,count-1)*sd/np.sqrt(count)) if count>1 else None
            row.update({f'{metric}_n':count,f'{metric}_mean':mean,
                f'{metric}_median':float(values.median()) if count else None,f'{metric}_sd':sd,
                f'{metric}_mean_ci95_low':mean-half if half is not None else None,
                f'{metric}_mean_ci95_high':mean+half if half is not None else None})
        lo,hi=row['gold_diff_15_mean_ci95_low'],row['gold_diff_15_mean_ci95_high']
        row['early_status']=('insufficient_samples' if row['gold_diff_15_n']<min_games else
            'observed_early_advantage' if lo is not None and lo>0 else
            'observed_early_disadvantage' if hi is not None and hi<0 else 'inconclusive')
        output.append(row)
    return pd.DataFrame(output)


def export_tables(lake,output,min_games=5,target_games=None):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    records=[json.loads(r[0]) for r in lake.db.execute('SELECT row_json FROM observations ORDER BY match_id,team_id,role')]
    rows=pd.DataFrame(records,columns=None if records else SCOPE+['match_id','team_id','champion_id','opponent_id','champion','opponent','win'])
    table=aggregate(rows,min_games,target_games=target_games)
    def csv(frame,name):
        destination=output/name
        temporary=destination.with_name(destination.name+'.tmp')
        frame.to_csv(temporary,index=False,encoding='utf-8-sig')
        temporary.replace(destination)
    csv(table,'all_matchups.csv')
    pooled=aggregate(rows,min_games,pooled=True,target_games=target_games)
    csv(pooled,'pooled_all_matchups.csv')
    if len(pooled):
        supported_pool=pooled[pooled.games.ge(min_games)]
        order_pool=['queue','tier_floor','role','opponent_id']
        for filename,metric,ascending in [('pooled_best_full_game_matchups.csv','winrate',False),
                ('pooled_unfavorable_full_game_matchups.csv','winrate',True),
                ('pooled_early_gold_advantages.csv','gold_diff_15_mean',False)]:
            subset=supported_pool[supported_pool.gold_diff_15_n.ge(min_games)] if metric=='gold_diff_15_mean' else supported_pool
            csv(subset.sort_values(order_pool+[metric,'games','champion_id'],ascending=[True]*len(order_pool)+[ascending,False,True]),filename)
        progress=pooled[KEYS+['champion','opponent','games','target_games','games_remaining','target_reached','patch_count','platform_count','gd15_patch_direction']].sort_values(['games','role','champion_id','opponent_id'],ascending=[False,True,True,True])
    else:
        progress=pd.DataFrame(columns=KEYS+['champion','opponent','games','target_games','games_remaining','target_reached'])
        for filename in ['pooled_best_full_game_matchups.csv','pooled_unfavorable_full_game_matchups.csv','pooled_early_gold_advantages.csv']:
            csv(pooled,filename)
    progress['reference_status']='not_loaded' if target_games is None else 'manual_target_not_ugg_reference'
    csv(progress,'matchup_collection_progress.csv')
    if len(table):
        supported=table[table.games.ge(min_games)]
        order=SCOPE+['opponent_id']
        best=supported.sort_values(order+['winrate','games','champion_id'],ascending=[True]*len(order)+[False,False,True])
        worst=supported.sort_values(order+['winrate','games','champion_id'],ascending=[True]*len(order)+[True,False,True])
        lane=supported[supported.gold_diff_15_n.ge(min_games)].sort_values(order+['gold_diff_15_mean','games'],ascending=[True]*len(order)+[False,False])
    else: best=worst=lane=table.copy()
    for name,frame in [('best_full_game_matchups',best),('unfavorable_full_game_matchups',worst),('early_gold_advantages',lane)]:
        csv(frame,f'{name}.csv')
    # Public sample rows contain no participant/account identifiers.
    public=rows.drop(columns=[c for c in rows if c.startswith('_')])
    csv(public,'observations.csv')
    counts=lake.counts()
    summary={'schema':'rank-matchup-tables-v3','generated_at':datetime.now(timezone.utc).isoformat(),
        'pooled_matchup_rows':len(pooled),'target_games_per_matchup':target_games,
        'pooled_matchups_at_target':(int(pooled.target_reached.sum()) if len(pooled) else 0) if target_games is not None else None,
        'collection_goal':'observed_matchup_coverage_without_fixed_sample_quota',
        'ugg_reference_status':'not_loaded','ugg_coverage_parity_verified':False,
        'pooled_scope':'all observed patches and platforms; queue/tier_floor/role kept separate',
        'evidence_db':lake.path.name,'dataset_sha256':hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),
        'counts':counts,'games_with_observations':int(rows.match_id.nunique()) if len(rows) else 0,
        'matchup_rows':len(table),'supported_matchups':len(best),'supported_gd15_matchups':len(lane),
        'min_games_for_ranked_tables':min_games,'all_sparse_rows_visible':True,'historical_rank_verified':False,
        'live_draft_signal_enabled':False,'counter_interpretation':'observed_match_result_and_resource_difference_not_causal_counter',
        'mean_ci_method':'Student_t_95_assuming_independent_matches; repeated players weaken this assumption',
        'win_ci_method':'Wilson95; not calibrated model probability',
        'public_inspiration':'https://u.gg/lol/champions/leesin/counter',
        'limitations':['Same-role gold/XP/CS include jungle/support/roams/team and player effects.',
          'Jungle is not a literal laning duel; support/bot context needs separate analysis.',
          'Snapshots are near-match proxies, not historical tiers. Rank and Pro are not pooled.',
          'No adjustment for champion base strength, skill, side or selection bias is claimed.',
          'Low n remains low reliability even if mean gold or raw winrate is extreme.',
          'Matchup ranking is descriptive; no win uplift, mechanical counter or BO5 optimality claim.']}
    write_json(output/'summary.json',summary)
    lines=['# Dữ liệu đối đầu cập nhật tăng dần','',
        f"Đã có {summary['games_with_observations']} trận với observations; {len(table)} cặp có hướng, {len(best)} cặp đạt n>={min_games}.",
        f"Hàng đợi: {counts}. Không có mốc dừng tổng ở1.000trận; mỗi phiên có cap tài nguyên và có thể tiếp tục.",
        'all_matchups.csv chứa cả kèo ít mẫu; ba bảng xếp riêng theo winrate thắng trận/GD15, không trì hoãn cập nhật đến khi đủ1000.',
        'Các bảng xếp chỉ hiện kèo qua ngưỡng n; rỗng nghĩa chưa đủ mẫu, không gán kết quả giả.', '',
        '| Bảng | Ý nghĩa |','|---|---|',
        '| best_full_game_matchups.csv | Winrate cao khi gặp đối thủ cùng role; kết quả cả đội |',
        '| unfavorable_full_game_matchups.csv | Winrate thấp khi gặp đối thủ |',
        '| early_gold_advantages.csv | Chênh vàng phút15 cao, tách khỏi thắng trận |',
        '| all_matchups.csv | n/người/Wilson, mean/median/SD/CI của gold-XP-CS10/15; giữ cả sparse |','',
        'Bảng pooled_*.csv gộp mọi patch/server thực có, vẫn tách queue/tier/role; không gọi ALL_OBSERVED là dữ liệu toàn thế giới đầy đủ.',
        ('matchup_collection_progress.csv chỉ báo số mẫu/độ phủ thực có. Không đặt mốc cố định mỗi kèo; target/remaining/reached để trống khi chưa có mục tiêu được xác định.' if target_games is None else
         f'matchup_collection_progress.csv có mục tiêu thủ công {target_games}, chỉ để tái lập cấu hình cũ; không phải số liệu U.GG.'),
        'Chưa nạp bộ đối chiếu U.GG theo cùng bộ lọc: không khẳng định đã bằng số mẫu, độ phủ hoặc chất lượng của họ.',
        'patches/platforms ghi nguồn gộp; gd15_patch_direction phát hiện trung bình trái dấu ở các patch đủ n. Cùng dấu không chứng minh counter bền vững.', '',
        'Chỉ học cách phân biệt thống kê công khai từ U.GG, không biết/tái tạo thuật toán nội bộ hoặc sao chép số liệu của họ.',
        'GD10/GD15 và XP/CS là phép đo quan sát hậu draft, không dùng trực tiếp làm feature dự báo trước draft.', '',
        '## Giới hạn','']+[f'- {x}' for x in summary['limitations']]
    (output/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return summary
