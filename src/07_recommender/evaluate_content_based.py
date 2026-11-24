"""Chapter 6 demonstration on a prespecified chronological validation holdout."""
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '06_machine_learning'))
from draft_model import load_pivoted_draft_data, POSITIONS
from validation import split_groups, fingerprint
from content_based import ContentBasedRecommender


def summarize(rows):
    if not rows:
        return {'queries': 0}
    result = {'queries': len(rows), 'candidate_coverage': float(np.mean([r['covered'] for r in rows]))}
    for k in [5, 10]:
        hit = float(np.mean([r['rank'] <= k for r in rows]))
        result[f'recall_at_{k}'] = hit
        result[f'precision_at_{k}'] = hit / k
        result[f'mrr_at_{k}'] = float(np.mean([1/r['rank'] if r['rank'] <= k else 0 for r in rows]))
    return result


def evaluate():
    draft = load_pivoted_draft_data()
    parts, _ = split_groups(draft)
    heldout = parts['validation']
    cutoff = pd.to_datetime(heldout.date, utc=True).min()
    model = ContentBasedRecommender(before=cutoff)
    players = model.players  # historical only
    # Names are identifiers available at the event, never features from that event.
    from analysis_data import load_clean_tables
    all_players = load_clean_tables()[2]
    queries = all_players[all_players.gameid.isin(heldout.gameid)].sort_values(['gameid','participantid'])
    exclusion = all_players.groupby('gameid').champion.agg(set).to_dict()
    rows = {'content_based': [], 'popularity': [], 'player_frequency': []}
    for q in queries.itertuples(index=False):
        unavailable = exclusion[q.gameid] - {q.champion}
        response = model.recommend_for_player(q.playername, q.position, already_banned=unavailable, top_k=10000)
        catalog = model.catalog(q.position)
        eligible = [c for c, v in catalog['vectors'].iterrows()
                    if c not in unavailable and np.linalg.norm(v.to_numpy()) > 0]
        own = catalog['players'][catalog['players'].playername.eq(q.playername)].groupby('champion').size()
        popularity = sorted(eligible, key=lambda c: (-int(catalog['games'].loc[c]), c))
        personal = sorted(eligible, key=lambda c: (-int(own.get(c,0)), -int(catalog['games'].loc[c]), c))
        recommendations = [r['champion'] for r in response['recommendations']]
        for name, items in [('content_based',recommendations), ('popularity',popularity), ('player_frequency',personal)]:
            rows[name].append({'gameid':q.gameid, 'covered':q.champion in eligible,
                               'warm':response['status']=='ok',
                               'rank':items.index(q.champion)+1 if q.champion in items else float('inf')})
    metrics = {name:summarize(values) for name,values in rows.items()}
    warm = {name:summarize([r for r in values if r['warm']]) for name,values in rows.items()}
    # Optional extension: uncertainty over whole games rather than individual slots.
    groups = sorted(heldout.gameid.unique())
    lookup = {g:[i for i,r in enumerate(rows['content_based']) if r['gameid']==g] for g in groups}
    rng = np.random.default_rng(42)
    values = []
    for _ in range(300):
        indices = [i for g in rng.choice(groups,len(groups),replace=True) for i in lookup[g]]
        values.append(summarize([rows['content_based'][i] for i in indices])['precision_at_10'])
    example = model.recommend_similar('Ahri','mid',top_k=5)
    player_example = model.recommend_for_player('Faker','mid',top_k=5)
    report = {'method':'content_based_cosine', 'evaluation_partition':'validation_not_final_test',
              'protocol':'retrospective_final_draft_slot_retrieval_with_known_player',
              'data_fingerprint':fingerprint(draft), 'historical_cutoff_exclusive':cutoff.isoformat(),
              'historical_games':int(players.gameid.nunique()), 'heldout_games':len(groups),
              'features':list(model.catalog('mid')['raw'].columns), 'min_profile_games':model.min_games,
              'overall':metrics, 'warm_user_cohort':warm,
              'user_profile_coverage':float(np.mean([r['warm'] for r in rows['content_based']])),
              'precision_at_10_ci95_game_bootstrap':np.quantile(values,[.025,.975]).tolist(),
              'examples':{'similar_to_ahri':example, 'player_faker':player_example},
              'limitations':['One observed pick is relevant per query; Precision@K=Recall@K/K with unfilled slots treated as misses.',
                             'Retrospective query sees other nine picks, not real draft pick order or bans.',
                             'This is validation evidence, not a fresh final-test claim or a winrate-uplift experiment.',
                             'Observed picks reflect team/coach/patch constraints; frequency is implicit preference.',
                             'Raw item attributes summarize past full-match performance, not champion mechanics.']}
    root = Path(__file__).resolve().parents[2]
    (root/'reports/content_based_evaluation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    profile = model.catalog('mid')
    profile['raw'].assign(games=profile['games']).to_csv(root/'reports/content_based_mid_profiles.csv')
    lines = ['# Content-based filtering — minh chứng Chương 6','',
             'Item profile: trung bình chỉ số thực đo của tướng/vị trí. User profile: trung bình item vectors, trọng số số lần tuyển thủ chọn tướng.',
             'Chuẩn hóa min-max theo vị trí, rồi cosine similarity. Không sử dụng winrate hoặc bảng synergy/thuộc tính chuyên gia.',
             f'Chỉ tổng hợp dữ liệu trước {cutoff.isoformat()}; {len(groups)} trận validation, {len(queries)} truy vấn. Không huấn luyện mô hình dự đoán.', '',
             '| Phương pháp | Precision@10 | Recall@10 | Recall@5 | MRR@5 |','|---|---:|---:|---:|---:|']
    for name,m in metrics.items():
        lines.append(f"| {name} | {m['precision_at_10']:.4f} | {m['recall_at_10']:.4f} | {m['recall_at_5']:.4f} | {m['mrr_at_5']:.4f} |")
    lines.extend(['',f"User profile coverage: {report['user_profile_coverage']:.2%}.",
                  'Precision@10 CI95 (mở rộng bootstrap): '+str(report['precision_at_10_ci95_game_bootstrap']),
                  '', 'Có một nhãn liên quan mỗi truy vấn nên Precision@10 tối đa 0.1. Các lựa chọn khác chưa được chấm là phù hợp/không phù hợp.',
                  'Không diễn giải truy hồi lựa chọn thành chọn tối ưu hoặc tăng tỷ lệ thắng. Baseline popularity/player frequency dùng cùng tập ứng viên.',
                  'Slide tham chiếu: Chương 6, trang 11–13 (item profile), 16–19 (user profile/cosine), 47 (Precision at top 10).',
                  'Các mở rộng: thuộc tính hành vi từ lịch sử, implicit pick weights, cắt thời gian và bootstrap; không coi là nội dung slide nguyên văn.'])
    (root/'reports/content_based_evaluation.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='examples'},indent=2,ensure_ascii=False))
    return report


if __name__=='__main__':evaluate()
