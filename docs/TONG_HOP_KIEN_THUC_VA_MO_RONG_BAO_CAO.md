# Tổng hợp kiến thức môn học, phần mở rộng và minh chứng kết quả

> **Phạm vi hiện hành — 24/11/2026:** chỉ duy trì **legacy và contextual**. Lookahead đã gỡ khỏi runtime/CLI; các mục mô tảsearch và kết quả3chếđộ bên dưới là lịch sử, không phải tính năng còn được hỗ trợ. Tra cứu chính: [BAN_LEGACY_VA_CONTEXTUAL.md](BAN_LEGACY_VA_CONTEXTUAL.md) và mục15.

**Cập nhật:** 24/11/2026. **Định hướng được giữ:** vận dụng kiến thức môn học, có phần mở rộng; hỗ trợ dự đoán lựa chọn đối thủ, tính trước các nhánh cấm/chọn và phân bổ tướng qua BO5 Fearless.

Đây là tài liệu tổng hợp dùng làm căn cứ viết báo cáo. Mỗi nội dung được nối với chương học, nơi sử dụng, chức năng và file đầu ra. Mục tiêu phát triển được tách rõ khỏi chức năng đã triển khai. Không lấy mô tả thiết kế cũ hoặc dòng import thư viện làm bằng chứng tính năng đã chạy.

## 1. Quy ước phân loại và trạng thái

| Nhãn | Ý nghĩa |
|---|---|
| **MH — Môn học** | Khái niệm/phương pháp được trình bày trong bộ slide của môn. Việc áp dụng vào dữ liệu LMHT vẫn là lựa chọn thực nghiệm của nhóm. |
| **UD — Vận dụng** | Dùng kiến thức đã học để chọn đặc trưng, định nghĩa user/item, thống kê giải đấu hoặc dựng bài toán cụ thể; không gọi đây là thuật toán mới được dạy trong slide. |
| **MR — Mở rộng** | Công thức, kỹ thuật hoặc quy trình vượt nội dung được trình bày cụ thể trong slide. Phải giải thích lý do sử dụng và cách đánh giá. |
| **NV — Nghiệp vụ/kỹ thuật** | Luật LMHT, Fearless, state machine, CLI, lưu JSON, kiểm tra hợp lệ; phục vụ ứng dụng, không phải thuật toán ML được giảng trong môn. |
| **Đã có** | Có hiện thực trong mã nguồn hiện hành. File kết quả chỉ chứng minh những gì phép đánh giá đó đo. |
| **Đã chạy** | Có artifact/kết quả thực thi đã kiểm tra. Không đồng nghĩa đạt chất lượng tối ưu. |
| **Dự kiến** | Chưa hiện thực; tên module/file đầu ra là thiết kế đề xuất, chưa phải artifact thật. |

Nguồn học liệu: [Chương 0](course_slides/Chapter%200_%20Course%20Info.pdf), [Chương 1](course_slides/Chapter%201_%20Preliminaries.pdf), [Chương 2](course_slides/Chapter%202_%20Data%20Preparation.pdf), [Chương 3](course_slides/Chapter%203_%20Data%20Visualization.pdf), [Chương 4](course_slides/Chapter%204_%20Machine%20Learning.pdf), [Chương 5](course_slides/Chapter%205_%20Databases%20and%20SQL.pdf), [Chương 5x](course_slides/Chapter%205x_%20Data%20Manipulation%20-%20Pandas.pdf), [Chương 6](course_slides/Chapter%206_%20Recommendation%20Systems.pdf). Số trang bên dưới là số trang trong bộ slide local, không phải số dòng mã nguồn.

## 2. Kiến thức từng chương đang dùng ở đâu?

| ID | Chương/kiến thức | Dùng ở đâu | Chức năng trong dự án | File kết quả/minh chứng | Phân loại và giới hạn |
|---|---|---|---|---|---|
| MH-01 | Chương 1: vector, ma trận, trung bình, phương sai | [content_based.py](../src/07_recommender/content_based.py): `catalog`, `recommend_for_player`; [plot_eda_figures.py](../src/05_visualization/plot_eda_figures.py) | Biểu diễn hồ sơ tướng/tuyển thủ và mô tả phân phối dữ liệu | [content_based_mid_profiles.csv](../reports/content_based_mid_profiles.csv), notebook 02, các hình EDA | MH+UD; đặc trưng hành vi trận đấu do nhóm lựa chọn, không phải thuộc tính kỹ năng tướng thuần túy. |
| MH-02 | Chương 1 trang 23–27: xác suất có điều kiện, độc lập, Bayes | [draft_meta.py](../src/07_recommender/draft_meta.py): `role_probabilities`, `pair_evidence`; [historical_recommender.py](../src/07_recommender/historical_recommender.py): `stats`, `evidence` | Thống kê role, kết quả trận, tần suất ghép cặp | JSON phiên draft: `historical`, `composition_evidence`, `composition_summary` | Xác suất/tần suất cơ bản là MH+UD. Shrinkage/lift/odds dùng sau đó là MR, không gộp hết vào Chương 1. |
| MH-03 | Chương 1 trang 37–44: thống kê mô tả, khái niệm kiểm định giả thuyết | [test_blue_side_advantage.py](../src/04_hypothesis_testing/test_blue_side_advantage.py), [test_snowball_effect.py](../src/04_hypothesis_testing/test_snowball_effect.py), [test_voidgrubs_vs_dragon.py](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py) | Phân tích phe, chênh lệch vàng, kịch bản mục tiêu | `data/processed/hypothesis_test_1_blue_side.csv`, `hypothesis_test_2_snowball.csv`, `hypothesis_test_3_objectives.csv` | Khái niệm kiểm định có trong bài. Các biến thể z/t/chi-square cụ thể cần ghi là vận dụng/tra cứu thêm nếu slide không trình bày chi tiết. Quan sát không chứng minh nhân quả; Pro mục tiêu phút10 chưa có timeline xác nhận thì unavailable. |
| MH-04 | Chương 2: thu thập và làm sạch; xử lý thiếu/sai dữ liệu | [load_esports_to_db.py](../src/01_data_pipeline/load_esports_to_db.py), [analysis_data.py](../src/analysis_data.py): `clean_ranked`, `clean_matches`, `complete_10min`, `clean_players`; [cleaner.py](../src/02_preprocessing/cleaner.py) | Đọc CSV/SQLite, chuẩn hóa, giữ dấu chênh lệch, chọn các phép đo thực sự có | `data/database/lol_live_data.db`; `data/processed/clean_ranked_10min.csv`, `clean_tournament_10min.csv`, `clean_tournament_draft.csv`, `clean_tournament_players.csv` | MH+UD. Raw CSV là đầu vào, không phải kết quả thuật toán. Snapshot sạch dùng chung; không suy tạo dữ liệu đường/phút10. |
| MH-05 | Chương 2 trang 32–39: chuẩn hóa min-max/z-score | [content_based.py](../src/07_recommender/content_based.py): `catalog` | Đưa năm đặc trưng hành vi về thang so sánh để tính cosine | `raw` và vector chuẩn hóa trong hồ sơ/JSON content-based; CSV profiles là bảng raw mean và số mẫu | MH+UD; không lấy min/max từ tập được giữ lại để đánh giá. Không mô tả mọi CSV profiles là vector chuẩn hóa nếu file lưu giá trị raw. |
| MH-06 | Chương 3: bar/scatter/boxplot/histogram/density và trực quan độ biến thiên | [plot_eda_figures.py](../src/05_visualization/plot_eda_figures.py), [notebook 01](../notebooks/01_kham_pha_du_lieu_EDA.ipynb) | Khám phá dữ liệu, trình bày phân phối và tương quan | [figures](../reports/figures/README.md): fig1–fig5; giải thích hình ở `docs/figure_explain/` | Cách vẽ thuộc MH; diễn giải chiến thuật là UD. Tương quan không đồng nghĩa tác động nhân quả. |
| MH-07 | Chương 4 trang9: holdout/cross-validation; overfit/underfit, lựa chọn mô hình | [validation.py](../src/06_machine_learning/validation.py): `split_groups`, `evaluate_training` | Tách dữ liệu và đánh giá tổng quát hóa | [draft_model.evaluation.json](../models/draft_model.evaluation.json), [snowball_model.evaluation.json](../models/snowball_model.evaluation.json) | Nền tảng là MH; chia theo game/time, bốn partition và expanding encoding là UD/MR về thiết kế thực nghiệm. Pro chia thời gian; rank chưa có event time nên grouped random, không gọi là đánh giá tương lai. |
| MH-08 | Chương 4 trang59–75: cây quyết định, Random Forest, bagging/boosting | [draft_model.py](../src/06_machine_learning/draft_model.py), [snowball_model.py](../src/06_machine_learning/snowball_model.py), [validation.py](../src/06_machine_learning/validation.py): `gpu_candidates` | Nền tảng cho phân loại kết quả trận | [draft_model.pkl](../models/draft_model.pkl), [snowball_model.pkl](../models/snowball_model.pkl), manifest tương ứng | Bài có RF/AdaBoost/GradientBoosting. **Luồng fit hiện hành chọn giữa hai cấu hình XGBoost CUDA**, không phải RF đang được fit chỉ vì file có import RF. XGBoost cụ thể là MR dựa trên nền boosting. |
| MH-09 | Chương 2 trang53–54; Chương 4 trang77–80: PCA, K-Means | [cluster_archetypes.py](../src/06_machine_learning/cluster_archetypes.py): `compute_team_composition_vector`, `fit_and_evaluate` | Giảm chiều và khám phá nhóm đội hình | [archetype_kmeans.pkl](../models/archetype_kmeans.pkl); hình fig10, fig11 | Thuật toán là MH; vector năm trục và tên nhóm chiến thuật dựa metadata/quy tắc chuyên gia. Artifact cũ chưa được tái nghiệm thu như mô hình chiến thuật học hoàn toàn từ dữ liệu. |
| MH-10 | Chương 5: SQL, quan hệ, truy vấn tổng hợp | [queries.sql](../src/03_database_sql/queries.sql), [execute_queries.py](../src/03_database_sql/execute_queries.py): `run_query`; [analysis_data.py](../src/analysis_data.py): `open_clean_connection` | Truy vấn đội, tướng, giải, thống kê nhóm trên dữ liệu sạch | `data/processed/sql_query_1_result.csv` đến `sql_query_5_result.csv`; SQLite | MH+UD. Tối ưu index/schema là kỹ thuật triển khai; dữ liệu sạch và raw phải được phân biệt. |
| MH-11 | Chương 5x: lọc, groupby, merge, pivot trong Pandas | [analysis_data.py](../src/analysis_data.py), [content_based.py](../src/07_recommender/content_based.py), [draft_meta.py](../src/07_recommender/draft_meta.py): `_build_role_pairs` | Tổng hợp theo role/patch/player, ghép đúng game+side+cả hai role | CSV sạch/profiles; JSON metadata và cặp tướng trong từng phiên | MH+UD. Không ghép hai đối thủ thành đồng đội, không trộn flex role khi thống kê cặp. |
| MH-12 | Chương 6 trang11–13: content-based, item profile | [content_based.py](../src/07_recommender/content_based.py): `catalog`, `recommend_similar` | Một item là tướng/role; hồ sơ gồm DPM, CSPM, WPM, damage-taken/min, earned-gold-share | [notebook 02](../notebooks/02_content_based_recommender.ipynb), profiles CSV, JSON `examples` của benchmark | Content-based là MH; cách chọn năm thuộc tính LMHT và điều kiện role/giải là UD. |
| MH-13 | Chương 6 trang16–20: user profile, cosine; trang9: suy sở thích từ hành vi | [content_based.py](../src/07_recommender/content_based.py): `recommend_for_player`, `_rank`; [draft_advisor.py](../src/07_recommender/draft_advisor.py): `content_scores` | Hồ sơ tuyển thủ là trung bình có trọng số các item đã chọn; xếp hạng tương đồng | JSON/console khi chạy content-based; `examples.player_faker` trong evaluation | MH+UD. Pick count là implicit preference, không phải rating tự khai hoặc mức thành thạo được xác nhận. Cosine không là xác suất thắng. |
| MH-14 | Chương 6 trang45–47: evaluation, Precision@10 | [evaluate_content_based.py](../src/07_recommender/evaluate_content_based.py) | Đo truy hồi tướng đã chọn và so baseline trên cùng pool | [content_based_evaluation.md](../reports/content_based_evaluation.md), [content_based_evaluation.json](../reports/content_based_evaluation.json) | Precision@10 trong bài; Recall/MRR/CI-bootstrap và thiết kế thời gian là MR/UD. Một nhãn/truy vấn nên Precision@10 tối đa0.1. |

**Không nhận vơ phần chưa có:** Chương6 còn dạy user-user/item-item collaborative filtering (trang24–43, item-item ở35–40). Module minh chứng hiện hành là **content-based**. Role-pair co-occurrence/lift hiện tại không tự động trở thành hiện thực đầy đủ của công thức CF trong slide. Nếu bổ sung CF đúng nghĩa cần utility matrix, similarity, neighbor aggregation và đánh giá riêng.

## 3. Phần mở rộng đã hiện thực: dùng ở đâu, làm gì, cho ra gì?

| ID | Kiến thức/kỹ thuật mở rộng | Nơi dùng và chức năng | Đầu ra hiện có | Giới hạn khi viết báo cáo |
|---|---|---|---|---|
| MR-01 | Snapshot theo cutoff, patch, cửa sổ và time decay | `DraftMetaSnapshot`, `MetaPolicy` trong `draft_meta.py`; ưu tiên dữ liệu mới, ngăn nhìn tương lai, từ chối patch không có dữ liệu | `meta_scope`: patch, data_through, requested_as_of, staleness, số trận; `--max-data-age-days` | Lọc/groupby dựa MH; chính sách decay `2^(-age/21)` là thiết kế mở rộng. Không gọi snapshot lịch sử là live meta. |
| MR-02 | Wilson confidence interval | `historical_recommender.wilson`, `evidence`; `draft_meta.pair_evidence` | `historical.ci95_wilson`, `co_pick_share_ci95_wilson` trong JSON | Khoảng winrate và khoảng tần suất ghép cặp có mẫu số khác nhau; giả định độc lập có hạn chế với các ván trong series. |
| MR-03 | Conditional co-pick shrinkage, lift, độ tin cậy, geometric aggregation, biến đổi odds điểm | `draft_meta.pair_evidence`; `DraftAdvisor.recommend_picks` | `composition_evidence`, `base_priority`, `composition_lift`, `score_formula`, `composition_summary` trong game JSON | Mục đích: không thưởng quá mạnh tướng phổ biến/cặp một-mẫu; xét mọi10cặp role. Không chứng minh synergy cơ học hoặc tương tác3/5tướng. Prior/trọng số là policy thủ công công khai. |
| MR-04 | Suy role flex bằng các cách gán role một-một | `DraftAdvisor.infer_enemy_roles` | `matchup_candidates` có role_probability, số mẫu và kết quả trận | Phân phối giả định từ lịch sử, không đọc được ý đồ thật của đối thủ. **Đây chưa phải mô hình dự đoán hành động cấm/chọn tiếp theo.** |
| MR-05 | Hybrid heuristic và one-step denial | `AdvisorPolicy`, `recommend_picks`, `recommend_bans` trong `draft_advisor.py` | Điểm thành phần, lý do pick, ban_priority, denial_loss trong từng lượt | Kết hợp meta/slot/history/mastery/content/association. Ban xét ưu tiên hiện tại của đối thủ, chưa duyệt cây phản ứng. Không có bằng chứng tối ưu toàn cục. |
| MR-06 | Tách pool ứng viên khỏi ngưỡng bằng chứng, ưu tiên lớp đủ mẫu | `AdvisorPolicy.candidate_min_games`, `min_games`; `pick_candidates` | `candidate_min_games`, `evidence_min_games`, `evidence_status`, số mẫu từng pick | Series thử cho pool>=1 nhưng evidence5; mặc định một ván vẫn5/5. Đây là chính sách dữ liệu, không phải luật hợp lệ champion của giải. |
| MR-07 | XGBoost và CUDA training | `validation.gpu_candidates`, `check_gpu`; Draft/Snowball training | Hai `.pkl`, manifest có training_device/validation_candidates/fingerprint | Boosting có trong bài, XGBoost/CUDA là mở rộng triển khai. Kết quả lưu không chứng minh dự đoán đúng meta mới hoặc thắng BO5. |
| MR-08 | Expanding historical encoding, chia theo trận/thời gian và chống leakage | `draft_model.py` và `validation.evaluate_training`/`split_groups` | partitions, gameids, split_policy, data_fingerprint trong manifest | Là quy trình đánh giá bổ sung; không dùng dữ liệu tương lai để tạo đặc trưng train. Cần đánh giá theo series thêm khi tối ưu BO5. |
| MR-09 | Calibration về prior, log-loss/Brier, reliability bins | `validation.calibrate`, `metrics`, `calibration_bins` | `calibration`, `test`, `reliability_bins` trong manifest; fig6–fig9 | Phân biệt xác suất từ model với điểm quy tắc/cosine. Công thức calibration hiện tại là shrink về training prior, không ghi nhầm thành Platt/isotonic. |
| MR-10 | Bootstrap theo game, baseline, Recall/MRR, replay thứ tự draft | `validation.bootstrap_intervals`; `evaluate_recommender.py`, `evaluate_content_based.py`, `evaluate_draft_policy.py` | Các evaluation JSON; CI và baseline, ví dụ truy vấn | Tập audit đã xem không thành final test mới. Bootstrap theo game chưa xử lý hết phụ thuộc theo series. |
| MR-11 | Expert metadata, radar và thẻ chiến thuật | `recommender_engine.py`, `cluster_archetypes.py`; phần summary của simulator | Radar/thẻ hiển thị console, fig10/11 và model phân cụm cũ | Có quy tắc/thuộc tính chuyên gia, không được gọi toàn hệ thống zero-hardcode. Không dùng radar để bịa probability; cơ chế tướng và lời khuyên cần nguồn xác nhận trước khi làm bằng chứng khoa học. |

### Công thức phối hợp hiện hành để đưa vào phần phương pháp

Với ứng viên C ở role R, đồng đội A ở role S, lấy trên cùng snapshot và đúng game/side:

1. Đếm số ghép cặp, số quan sát A/S và tỷ trọng nền p của C/R. Các số đếm để tính điểm có decay; số mẫu/CI mô tả vẫn lưu riêng.
2. `q = (weighted_pair + 10*p) / (weighted_anchor + 10)`; `raw_lift = q/p` khi p>0.
3. Association dương dùng `r = weighted_pair/(weighted_pair+10)`; association âm dùng `r = weighted_anchor/(weighted_anchor+10)`.
4. `effective_lift = exp(r*log(raw_lift))`. Nếu thiếu lịch sử anchor thì gắn nhãn, không lấy làm bằng chứng phối hợp.
5. Tổng hợp geometric lift L qua các đồng đội đủ điều kiện, trọng số `weighted_anchor/(weighted_anchor+10)`.
6. Với điểm nền b và số mũ composition w mặc định1: `priority = b*L^w/(1-b+b*L^w)`.

**Toàn bộ công thức kết hợp này là MR tự thiết kế**, sử dụng nền xác suất/thống kê; không ghi rằng Chương1 hoặc Chương6 dạy nguyên công thức. Priority trong[0,1] vẫn chỉ là điểm ưu tiên, không phải xác suất thắng. Các hằng số10/21/trọng số policy chưa được tối ưu trên validation độc lập cho BO5.

## 4. Luật và kỹ thuật ứng dụng: đã làm đến đâu?

| ID | Chức năng | Nơi hiện thực | Đầu ra và trạng thái |
|---|---|---|---|
| NV-01 | Một ván20lượt, đúng bên, hai pha cấm/chọn, không trùng tướng/role | `simulate_draft_match.py`: `draft_schedule`, `DraftState.apply`, `swap` | Đã chạy; game JSON có history/picks/bans/swaps/complete. |
| NV-02 | Gợi ý/giải thích/chọn tay cho một phe | `choose_interactively`, `explain`, `run_pro_tournament_draft_simulation` | Đã có; CLI có why, role filter, swap, wishlist, auto, quit. Chế độ nhập tay cả hai phe xuyên5ván chưa hoàn thiện. |
| NV-03 | Fearless carry tướng đã PICK từ mọi ván trước cho cả hai đội; bans thường không carry; ván5 không reset | `simulate_fearless_series.py`: `run_series`, `validate_game` | Đã chạy5draft; `reports/worlds_fearless_bo5/series.json`, game1–5 JSON/log, REPORT.md. |
| NV-04 | Lịch first-pick độc lập màu phe | `draft_schedule(first_side)`, `--first-pick`; driver series luân phiên B/R/B/R/B | Đã có lịch demo. **Chưa mô phỏng quyền lựa chọn sau kết quả từng ván**, chưa có game winner. |
| NV-05 | Lưu nguồn dữ liệu và giải thích quyết định | `meta_scope`, `roster_sources`, history.advice, composition_summary | Đã có, trace được số mẫu/điểm. Lineup là trận gần nhất trong snapshot, không là roster cập nhật trực tiếp. |

Nguồn luật: [Fearless của Riot](https://lolesports.com/en-GB/news/fst-2025-primer), [First Selection2026 của Riot](https://lolesports.com/en-GB/news/season-start-2026-lol-esports). Đây là kiến thức nghiệp vụ ngoài slide KHDL, dùng để định nghĩa tập hành động hợp lệ. Danh mục champion bị khóa riêng theo sự kiện cần bổ sung nguồn, không suy từ việc không có trong pool thống kê.

## 5. Mục tiêu giữ lại: tính trước đối thủ, để dành tướng và tối ưu BO5

**Cập nhật24/11: đã có rollout ban giới hạn trong một ván (mục14); chưa có planner phân bổ tướng toàn BO5.** `run_series` hiện gọi bộ chọn tham lam từng lượt rồi cập nhật khóa Fearless. Chạy đủ5ván không chứng minh đã tối ưu phân bổ tướng cho5ván. `Draft model` dự đoán kết quả đội hình không phải mô hình đoán đối thủ sẽ chọn/cấm gì.

Cập nhật24/11: KH-01 đã có dataset trước lượt và model dự đoán hành động ban/pick ban đầu; các trace/search/planner còn lại vẫn DỰ KIẾN. Người dùng sau đó yêu cầu chỉ hoàn tất vấn đề Trundle rồi dừng; không tiếp tục phát triển opponent/search/BO5 trong đợt này. Các output chưa hiện thực bên dưới vẫn là thiết kế đề xuất.

| ID | Kiến thức mở rộng dự kiến | Dùng ở đâu, chức năng | Đầu ra dự kiến, chưa có | Cách nghiệm thu cần có |
|---|---|---|---|---|
| KH-01 | Opponent modeling ban/pick — **đã có bản đầu, tạm dừng phát triển tiếp theo chỉ đạo người dùng** | `draft_states.py`: `build_states`, `game_states`, `state_features`; `opponent_model.py`: `train`, `rank`, `public_simulation_state`. Đầu vào chỉ trạng thái công khai trước lượt; không phải counter evaluator. | Đã có `data/processed/wlds_draft_states.jsonl`, `reports/wlds_draft_states_manifest.json`, `models/opponent_model.pkl`, manifest/evaluation JSON, `reports/opponent_prediction.json` | CUDA fit, chia series/thời gian và baseline; 840lượt phát triển Recall5=.3917 so slot=.2202, coverage=.9905. Probability chưa calibrated; source đã xem nên không gọi là fresh final test. |
| KH-02 | Search phản ứng — **đã thử và đã gỡ theo yêu cầu24/11**, không còn runtime hỗ trợ | `ban_planner.py` hiện chỉ one-stepcontextual, không còn evaluate_root/rollout/response_distribution | Báo cáolookaheadcũ giữ làm lịch sử; đầu ra hiện hành ở `reports/legacy_contextual_comparison/` | Không tuyên bố search hoặc planner BO5 đang được duy trì. |
| KH-03 | Lập kế hoạch nhiều ván, trạng thái pool/role/series và giá trị cơ hội của tướng | Module dự kiến `src/07_recommender/series_planner.py`; so chọn tướng ngay với để dành cho các ván sau; rollout qua cả2đội và khóa Fearless | `reports/bo5_planner_trace.json`, `reports/bo5_planner_report.md` | Lưu pool trước/sau mỗi ván, nhánh đối thủ, lý do giữ/dùng tướng, mục tiêu và giả định. So chiến lược greedy không để dành; nhiều series/seed/budget và nhiều patch. |
| KH-04 | Evaluator trạng thái chưa hoàn tất và đội hình hoàn chỉnh, xử lý flex/tương tác | Tầng đánh giá dự kiến dùng chung cho search/planner; có thể tái sử dụng feature, không mặc định model cũ đủ tốt | `reports/state_evaluator_evaluation.json`, version/fingerprint của evaluator | Chỉ dùng thông tin có ở state; kiểm tra domain shift, thiếu mẫu, calibration nếu là probability. Chưa có nhãn phản thực cho mọi draft nên phải ghi giới hạn. |
| KH-05 | MCTS/UCT nếu cây tìm kiếm quá lớn | Phương án thay thế/mở rộng search sau khi có evaluator đáng tin; **không bắt buộc triển khai đồng thời mọi thuật toán** | Trace có simulation count, seed, exploration policy, budget và CI mô phỏng phù hợp | So cùng compute budget; kiểm tra hội tụ/độ ổn định. Nhiều rollout không khắc phục evaluator sai và không tự chứng minh tăng thắng thực tế. |
| KH-06 | Điều khiển hai phe, quản lý series thực và First Selection dựa kết quả | Mở rộng giao diện/state series; nhận kết quả do người dùng nhập hoặc nguồn thật | Session gồm lựa chọn phe/thứ tự/quyền chọn, số ván và tỉ số thực | BO5 thật dừng khi có đội thắng3ván. Bài thử5draft hiện tại không gán2-2 giả để ép đi đủ5. |

### Tối ưu cái gì và có thể tuyên bố đến mức nào?

- **Giai đoạn hiện tại:** tối đa điểm xếp hạng của lượt hiện tại, sau lọc luật/pool. Không nhìn trước.
- **Planner dự kiến:** tìm phương án có giá trị kỳ vọng cao theo evaluator và mô hình phản ứng, xét hậu quả lên các ván sau và pool còn lại. Khi search bị giới hạn nhánh/độ sâu/ngân sách, đây là tối ưu xấp xỉ trong mô hình đã chọn.
- **Tối ưu xác suất thắng series:** chỉ dùng cách gọi này khi có evaluator xác suất được kiểm chứng, trạng thái tỉ số và chuyển tiếp kết quả ván phù hợp. Nếu chưa có thì chỉ báo cáo điểm chiến lược/độ phủ pool dự kiến, không đổi điểm thành phần trăm thắng BO5.
- **Tính phản ứng đối thủ:** trả nhiều kịch bản với giả định/độ tin cậy, không khẳng định biết chắc ý đồ. Minimax và expectimax là các giả định đối thủ khác nhau, cần lựa chọn và mô tả rõ.
- **Để dành tướng:** là kết quả so sánh nhánh khi dùng ngay và khi giữ lại, không viết bảng “luôn giữ tướng X đến ván5”.

Trình tự triển khai: KH-01 + KH-04 → KH-02 giới hạn độ sâu → KH-03 qua series → đánh giá độc lập; chỉ cân nhắc KH-05 nếu cần. Feature/ML nền có thể vận dụng Chương4, nhưng search/planning thuộc MR ngoài học phần. Nhóm chưa lựa chọn/thử nghiệm một planner cuối cùng trong tài liệu này.

Nguồn tham khảo để viết phần mở rộng: [Stanford CS221 — Games I](https://web.stanford.edu/class/archive/cs/cs221/cs221.1196/lectures/games1-6pp.pdf) trình bày game-tree/expectimax/minimax; [Games II](https://web.stanford.edu/class/archive/cs/cs221/cs221.1196/lectures/games2-6pp.pdf) bàn depth-limited search và evaluator. [Browne và cộng sự,2012 — A Survey of Monte Carlo Tree Search Methods](https://www.lamsade.dauphine.fr/~cazenave/A%2BSurvey%2Bof%2BMonte%2BCarlo%2BTree%2BSearch%2BMethods.pdf) là nguồn tham khảo MCTS/UCT. Các tài liệu này giải thích kỹ thuật tìm kiếm, không chứng minh áp dụng vào LMHT sẽ hiệu quả; phép áp dụng và đánh giá vẫn là việc của đồ án.

## 6. Danh mục file kết quả thật và cách sử dụng trong báo cáo

| File/thư mục | Nó là gì? | Dùng để minh chứng điều gì? |
|---|---|---|
| `data/raw/esports_active_matches.csv`, CSV năm2025/2026 | Dữ liệu đầu vào | Nguồn và phạm vi dữ liệu; không phải dự đoán/kết quả model. |
| `data/database/lol_live_data.db` | SQLite cho dữ liệu trận/đội/tuyển thủ | Mô hình lưu trữ/truy vấn; tên file có live không chứng minh dữ liệu đang live. |
| Bốn `data/processed/clean_*.csv` nêu ởMH-04 | Bảng sạch xuất từ shared policy | Tiền xử lý và đối chiếu dữ liệu trước/sau; file có thể được ghi lại khi chạy pipeline. |
| `data/processed/sql_query_1_result.csv`…`sql_query_5_result.csv` | Kết quả truy vấn | Ứng dụng SQL/Pandas. |
| `data/processed/hypothesis_test_*.csv` | Thống kê/kiểm định/kịch bản có dữ liệu | Câu hỏi phân tích cụ thể; không mặc định mọi giả thuyết đều được xác nhận. |
| [notebook01](../notebooks/01_kham_pha_du_lieu_EDA.ipynb), [notebook02](../notebooks/02_content_based_recommender.ipynb) | Quy trình có code/output | EDA và minh chứng content-based. Không coi notebook01 là toàn bộ tài liệu ML/search. |
| `reports/figures/*.png` | Hình EDA/đánh giá/phân cụm | Hình đưa vào báo cáo; đọc chú giải và trạng thái artifact. |
| [draft_model.pkl](../models/draft_model.pkl), [snowball_model.pkl](../models/snowball_model.pkl) | Model được serialize | Tải để suy luận; **không phải bảng kết quả để đọc trực tiếp**. |
| [draft_model.evaluation.json](../models/draft_model.evaluation.json), [snowball_model.evaluation.json](../models/snowball_model.evaluation.json), [evaluation_report.md](../src/06_machine_learning/evaluation_report.md) | Manifest + kết quả đánh giá | Model/partition/device/fingerprint, metric, baseline, CI, giới hạn. Ưu tiên manifest hiện hành hơn mục tiêu accuracy trong README cũ. |
| [content_based_evaluation.md](../reports/content_based_evaluation.md), [JSON](../reports/content_based_evaluation.json), [profilesCSV](../reports/content_based_mid_profiles.csv) | Benchmark và hồ sơ ví dụ | Chương6: vector, user profile, cosine, Precision@10 và baseline. |
| [recommender_evaluation.json](../reports/recommender_evaluation.json) | Benchmark ranker lịch sử riêng | Không phải kết quả planner hoặc benchmark content-based. |
| [wlds_draft_policy_evaluation.json](../reports/wlds_draft_policy_evaluation.json) | Audit replay thứ tự draft Worlds | Khả năng truy hồi lựa chọn thực tế; có baseline, coverage, CI. **Chưa replay đầy đủ Fearless trong benchmark này.** |
| [worlds_fearless_bo5/REPORT.md](../reports/worlds_fearless_bo5/REPORT.md) | Báo cáo dễ đọc của5draft đã chạy | Mỗi ván cấm/chọn gì, đủ100lượt, pool khóa và mẫu ít. |
| [worlds_fearless_bo5/series.json](../reports/worlds_fearless_bo5/series.json) | Toàn bộ series có cấu trúc | Snapshot/policy/checks/cả5ván; dùng tái kiểm tra50tướng không lặp. |
| `reports/worlds_fearless_bo5/game_1.json`…`game_5.json` | Kết quả riêng từng ván | `history`20lượt; mỗi lượt có advice; `picks`/`bans`/`used_champions`; `composition_summary`10cặp/đội. |
| `reports/worlds_fearless_bo5/game_1.log`…`game_5.log` | Nhật ký console | Đối chiếu lời giải thích khi chạy; dùng JSON khi cần phân tích tự động. |
| [series.json checks](../reports/worlds_fearless_bo5/series.json), [tests](../tests/test_fearless_series.py), [role-pair tests](../tests/test_role_pair_composition.py) | Kiểm chứng logic/trạng thái | 38tests đạt tại mốc23/11; không đồng nghĩa thuật toán có chất lượng chiến thuật cao. |
| [archetype_kmeans.pkl](../models/archetype_kmeans.pkl), [recommender_engine.pkl](../models/recommender_engine.pkl) | Artifact cũ của phân cụm/engine | Phải đối chiếu source/schema; không lấy ngày tồn tại file làm bằng chứng đã retrain hoặc toàn bộ recommender đã học từ dữ liệu. |

Đọc một `game_N.json`: `meta_scope` trả lời dữ liệu đến đâu; `used_champions` là pool khóa trước ván; `history` là đúng thứ tự hành động; `history[].advice` giải thích điểm và số mẫu; `picks` là đội hình theo role; `composition_summary` mô tả các cặp. `score_formula/base_priority/composition_lift` là phép xếp hạng, không phải nhánh search. Đã có artifact `opponent_model_evaluation` của bản dự đoán hành động ban đầu; **chưa có** `draft_search_trace` hoặc `bo5_planner_trace`.

## 7. Số liệu đã xác minh tại mốc tài liệu này

| Hạng mục | Kết quả thật | Cách diễn giải đúng |
|---|---|---|
| Draft model | Accuracy0.5517; AUC0.5628; log-loss0.6834 | Chất lượng dự đoán còn hạn chế; không đủ để tự tin làm evaluator tối ưu BO5. |
| Snowball model | Accuracy0.6718; AUC0.7413; log-loss0.6004 | Dùng dữ liệu phút10 đủ phép đo; **không dùng thông tin phút10 chưa xảy ra để draft trước trận**. |
| Content-based | 299trận validation/2990query; Precision@10=.0494; Recall@5=.2990; popularity Recall@5=.4652 | Có minh chứng Chương6 nhưng chưa vượt baseline. Một nhãn/query, Precision@10 tối đa.1. |
| Audit draft Worlds hiện hành | 20trận/200lượt; Recall@5=.36 so recent-presence=.30; MRR@5=.184; coverage=.86 | Audit phát triển nhỏ, đã xem trong quá trình làm; CI mô tả chênh Recall5 khoảng[+.015,+.102625]; chưa là final test hoặc tăng thắng. |
| Chạy5draft Fearless | 5ván,100actions,50uniquePicks; pool khóa[0,10,20,30,40];38testsPASS | Đã kiểm tra tuân thủ khóa tướng và trình tự, **chưa kiểm chứng tối ưu series**. Có1pick ít mẫu: Yuumi4trận. |
| Snapshot cho5draft | WLDS, cutoff13/11/2026, patch dataset16.20,106ván/94ván patch đích; trận mới nhất trong snapshot09/11 | Không dùng4ván final14/11; không gọi đây là meta live hoặc đồng nhất mã patch dataset với mã public mà không có mapping xác nhận. |

Các file benchmark có thể bị ghi lại khi chạy; khi đưa vào báo cáo cuối cần chốt ngày, phiên bản code, cutoff/policy, fingerprint và artifact, không trộn chỉ số từ hai phiên bản khác nhau. Các báo cáo cũ như `worlds_replay_before_role_pairs.json`, `worlds_role_pair_checks.json` phục vụ lịch sử/so sánh, không ghi đè chỉ số hiện hành bằng số ở mốc cũ.

## 8. Lệnh tạo/tái kiểm tra đầu ra

Chạy tại thư mục gốc Project, dùng `.venv`. Các lệnh đánh giá/giả lập có thể ghi lại report tương ứng; **không cần train lại chỉ để lấy một bảng ban/pick**.

```powershell
# Minh chứng content-based Chương6
.\.venv\Scripts\python.exe src/07_recommender/recommender_engine.py --content-based --seed-champion Ahri --lane mid
.\.venv\Scripts\python.exe src/07_recommender/evaluate_content_based.py

# Audit lựa chọn thực tế trên Worlds, chưa phải fullFearless benchmark
.\.venv\Scripts\python.exe src/07_recommender/evaluate_draft_policy.py --region WLDS

# Chạy5draft Fearless, có JSON/report/log
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py

# Kiểm tra logic dữ liệu/recommender/Fearless
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Planner chưa có lệnh chạy. Opponent model đã có CLI trong `opponent_model.py` nhưng đã dừng phát triển tiếp theo chỉ đạo người dùng; không mô tả nó là evaluator chiến thuật hoặc planner. Nếu huấn luyện predictive ML mới thì tuân thủ yêu cầu CUDA của dự án, giữ validation/test độc lập và tạo manifest mới; không làm thay đổi kết quả đã báo cáo mà không lưu phiên bản.

## 9. Cách dùng tài liệu này khi viết báo cáo

1. **Cơ sở lý thuyết:** dùng MH-01…MH-14; chỉ rõ phần nào đúng nội dung slide và phần nào là lựa chọn áp dụng. Chương0 dùng mô tả học phần, không phải nguồn thuật toán.
2. **Phương pháp/hiện thực:** nối nguồn dữ liệu → tiền xử lý → SQL/Pandas/EDA → content-based/ML → ranking → state Fearless. Trình bày MR-01…MR-11 thành mục mở rộng, giữ công thức/tham số và lý do chọn.
3. **Thực nghiệm:** trích artifact cụ thể ở mục6–7; nêu baseline, cutoff, số mẫu, nguồn và giới hạn. Chạy đúng luật khác với chọn chiến thuật tốt.
4. **Định hướng phát triển:** KH-01…KH-06 hiện phải ở mục dự kiến. Khi thật sự triển khai, chuyển trạng thái từng mục, ghi hàm/file thật, thêm kết quả thực nghiệm và nguồn tham khảo vào chính tài liệu này.
5. **Câu mô tả hiện tại có thể dùng:** “Đồ án vận dụng tiền xử lý, thống kê, SQL/Pandas, trực quan hóa, học máy và content-based recommendation; mở rộng bằng snapshot theo thời gian, thống kê phối hợp cặp tướng và mô phỏng quy trình Fearless. Bản dự đoán hành động đối thủ ban đầu đã có; tìm kiếm nhánh phản ứng và phân bổ tướng tối ưu qua BO5 chưa triển khai và đang dừng theo chỉ đạo người dùng.”

**Không dùng ở mốc hiện tại:** “đã biết trước đối thủ sẽ chọn gì”, “đã tối ưu BO5”, “tăng thắng X% do ban/pick”, “toàn bộ thuật toán đều có trong bài”, hoặc “100% zero-hardcode”. Thay bằng phát biểu có căn cứ và cập nhật sau khi có minh chứng mới.

## 10. Quy định duy trì sổ kiến thức cho các công việc sau

**NV-06 — Quản trị truy vết kiến thức, có hiệu lực23/11/2026.** Đây là quy trình kỹ thuật phục vụ báo cáo, không phải thuật toán khoa học dữ liệu được học trong một chương cụ thể.

- Quy định đầy đủ: [AI/KNOWLEDGE_RULES.md](../AI/KNOWLEDGE_RULES.md). Mỗi lần thêm/sửa phương pháp, chức năng, đánh giá hoặc output phải cập nhật chính sổ này trong cùng đợt thay đổi.
- Mỗi mục phải có ID, MH/UD/MR/NV, chương/trang hoặc nguồn/chính sách tự thiết kế, module/hàm, chức năng/giả định, file kết quả/lệnh tái lập, trạng thái/minh chứng và giới hạn. Nội dung dự kiến phải giữ nhãn chưa hiện thực/chưa có output.
- Rule được dẫn từ [AGENTS.md](../AGENTS.md), [GEMINI.md](../GEMINI.md), [AI/AI_RULES.md](../AI/AI_RULES.md) và nguyên tắcVI của [SpecKit constitution](../.specify/memory/constitution.md), version1.1.0.
- Nơi áp dụng: `.specify/templates/overrides/spec-template.md`, `plan-template.md`, `tasks-template.md`, `checklist-template.md`. Spec/plan có yêu cầu mapping; tasks có việc cập nhật/xác minh; checklist xét chất lượng yêu cầu. Analyze vẫn chỉ đọc và báo chỗ thiếu. Không đặt rule trong manifest cài đặt.
- Đầu ra: sổ kiến thức được cập nhật, bảng mapping trong spec/plan, task minh chứng trong tasks và phát hiện consistency khi review. Đây là yêu cầu quy trình cho AI/người phát triển, **chưa phải cơ chế CI tự động bảo đảm mọi thay đổi tương lai đều được ghi**.
- Kiểm chứng cấu hình: `.specify/scripts/powershell/check-knowledge-templates.ps1` kiểm tra resolver SpecKit thật sự chọn4override; `scratch/check_knowledge_doc.py` kiểm tra link của sổ tại lượt cập nhật. Với chỉnh sửa không ảnh hưởng kiến thức/chức năng, ghi lý do no-impact trong task/changelog; không tạo lý thuyết giả hoặc train model không đổi.
- Khi nâng cấp SpecKit, kiểm tra constitution/override còn hiệu lực. Không được đánh dấu công việc liên quan hoàn tất khi sổ còn thiếu/sai; cập nhật chủ động trong phạm vi đã được giao.

## 11. MR-12 / NV-07 — Đối đầu toàn đội và dừng auto khi thiếu căn cứ (24/11/2026)

**Trạng thái: đã hiện thực và kiểm chứng; hoàn tất phạm vi Trundle rồi dừng theo yêu cầu người dùng.** Báo cáo tập trung: [RA_SOAT_LUA_CHON_THEO_DOI_HINH.md](RA_SOAT_LUA_CHON_THEO_DOI_HINH.md).

- **Nền môn học:** Chương1 xác suất có điều kiện/thống kê; Chương5x groupby/merge. **MR tự thiết kế:** cross-role enemy outcome residual, shrinkage theo mẫu, mixture flex, coverage và abstention. **NV:** bảng alternative, manual_review và exit3. Không gọi đây là mô hình cơ chế counter được dạy trong bài.
- **Nơi dùng:** `DraftMetaSnapshot.enemy_evidence`; `DraftAdvisor.evaluate_enemy_context`, `recommend_picks`; `pick_candidates`, `needs_tactical_review` và vòng chạy `simulate_draft_match.py`; `audit_draft_choices.py`. Xét mọi role địch, không vá riêng Trundle.
- **Chức năng/công thức:** khi n≥5, residual WR theo đối thủ so với WR nền ứng viên, shrink n/(n+10), mixture role địch và trung bình trên số địch lộ. Lưu `enemy_context_evidence`, `enemy_context_coverage`, `mechanical_counter_status:not_evaluated`, `review_required`, `selection_basis`; không suy kết quả cả trận thành thắng đường/counter nhân quả.
- **Gate mặc định:** địch đã lộ5tướng và ứng viên auto không có đối đầu đủ mẫu (coverage0) thì không apply pick, lưu `manual_review`, `complete:false`, CLI một ván exit3; chọn tay phe người dùng vẫn được phép. Có `--allow-statistical-auto` cho demo một ván chỉ theo điểm, không thay nhãn counter. Driver series dừng khi gặp review; báo cáo5ván cũ thuộc phiên bản trước gate.
- **Đầu ra thật:** [draft_choice_audit.md](../reports/draft_choice_audit.md), JSON cùng tên (50pick, top5/score/evidence); [trundle_case_review.json](../reports/trundle_case_review.json) (tái dựng đúng ván2lượt20); [tactical_review_session.json](../reports/tactical_review_session.json) và [checks](../reports/tactical_review_checks.json).
- **Minh chứng:** Trundle vẫn top điểm thống kê, nhưng cả5đối thủ không có cặp đủ5mẫu. Các ứng viên đầu khác cũng coverage0. Gate không tự chốt, giữ19lượt và jungle trống. CLI live cũng dừng trước Pantheon ở case khác;51testsPASS. Thêm context chưa đổi top1 của50pick cũ; chưa chứng minh chọn mạnh hơn.
- **Giới hạn:** chưa có evaluator cơ chế kỹ năng/đội hình được xác minh theo patch, không xác nhận tướng thay thế nào tối ưu; blind pick chưa đủ5địch không bị gate này chặn. Có vài mẫu đối đầu vẫn không tự chứng minh counter. Nguồn nghiệp vụ tham khảo: [Riot Trundle](https://www.leagueoflegends.com/en-us/champions/trundle/), chỉ xác nhận mô tả kỹ năng, không cung cấp bảng counter/điểm/tỷ lệ thắng.
- **Tái lập:** `python src/07_recommender/audit_draft_choices.py` và các lệnh `.venv` trong báo cáo tập trung. Không cần train model để kiểm tra gate.

### Các phần đã thực hiện trước khi người dùng thu hẹp phạm vi

Ghi để không mất dấu kết quả đã tạo; **không tiếp tục phát triển các mục này trong đợt hiện tại**.

- `draft_states.py` dựng4120state/206ván/93seriesWorlds; seriesID tái dựng bảo thủ theo league/year/split/cặp đội/game1rồigame tiếp trong24h, không là ID chính thức. Input feature allowlist không có target/outcome/final role. Fearless carry picks, không carry bans; prefix/series lỗi bị loại thay vì điền giả. Output JSONL và manifest chứa hash/phạm vi/giới hạn.
- `opponent_model.py` fit2cấu hình XGBoost40trees bằng CUDA (đã xác nhậncuda:0), chọn bằng validation log-loss. Train142ván/65series (2840state), validation22ván/14series (440), holdout phát triển42ván/14series (840); tách thời gian và không trùngseries/game. Bộ vector610features fit train-only;122classes. InferenceCPU, không hạ yêu cầu GPU khi training.
- Role-feasibility mask dùng role quan sát **chỉ trong train**, không dùng role cuối trận cần dự đoán; có thể bỏ sót flex mới. Mẫu không dự đoán được tính miss. Top5=.3917, top1=.1202,MRR5=.2212; baseline slot top5=.2202; CI mô tả chênh theo series khoảng[.1376,.2076]. Không phải fresh final test hoặc tăng thắng; probability chưa calibrated, không là winrate.
- File đã tạo: `models/opponent_model.pkl`, `models/opponent_model.evaluation.json`, `reports/opponent_model_evaluation.json`, `reports/opponent_prediction.json`; model lưu payload schema1 để tải từ module/CLI ổn định. KH-01 có bản đầu; KH-02..05/search/planner/evaluator cơ chế vẫn chưa có.
- `--opponent-model` từng được nối vào simulator trước chỉ đạo dừng: forecast trạng thái trước lượt được lưu riêng, không đổi điểm chọn chiến thuật. Các artifact `reports/draft_with_opponent_forecasts.json` và `reports/worlds_fearless_with_forecasts/` được tạo trước gate review; là lịch sử chạy, không bằng chứng tối ưuBO5. Không train tiếp hoặc mở rộng planner sau khi người dùng thu hẹp phạm vi.

## 12. Tái kiểm tra T1–Gen.G BO5 — 24/11/2026

Không phát sinh kiến thức/phương pháp/chức năng mới; MR-12/NV-07 giữnguyên. Yêu cầu5draftWorlds nhưng chỉhoànthànhván1 và19lượtván2; trướcCamillelượt20manualreview, khôngchạyván3–5.39actions/19picks, khônglặptướngvàkhóa0/10đúng. [Báo cáo](../reports/t1_geng_bo5_20261124/REPORT.md), [checks](../reports/t1_geng_bo5_20261124/checks.json), [series](../reports/t1_geng_bo5_20261124/series.json). Khôngtựnhậppickhoặcoverrideđểéphoànthành.

Giới hạn rõhơn: Trundle vẫnđượcchọntrướckhiđịchlộđủ5vớicoverage0. Gateabstentionhiệnhànhkhôngxửlýhếtchấtlượngcountercủamọi state; tasktrướckhôngđượcmôtảlàđãcóevaluatorcơchếhoặctốiưucounter. Lượtnàychỉchạythửvàghiartifact, khôngsửathuậttoán/model/DB hoặcretrain.

## 13. NV-08 — Test5draft và đánh số từng Ban/Pick (24/11/2026)

Người dùng cho phép test: thiếu độ tin cậy vẫn chọngợiý1. `simulate_fearless_series.run_series` truyền `allow_statistical_auto` xuống simulator; CLIseries có `--allow-statistical-auto`, mặc địnhFalse. `markdown_report` lấy tênđộiđộng, lưuBan1–5/Pick1–5mỗiđội và sốturn1–20, giữnhãnthiếumẫu; đây làNVkỹthuật, khôngthuậttoánmới trongchươnghọc. Khôngđổicôngthứcthốngkê/MR-12, khôngfitmodel.

ĐãchạyWorlds T1–Gen.G5draft, cutoff13/11 patchdataset16.20;100actions/50picks khácnhau, locks0/10/20/30/40, validate_game và đánh sốreportPASS. [Quickview](../reports/t1_geng_bo5_test_20261124/QUICK_VIEW.md), [100lượt/căn cứ](../reports/t1_geng_bo5_test_20261124/REPORT.md), [checks](../reports/t1_geng_bo5_test_20261124/checks.json). Khôngtựnângđộtincậy, khôngtỉsốgame, khôngclaimcounter/tốiưu.

Táilập: `.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --output-dir reports/t1_geng_bo5_test_20261124`. Khôngbậtflagthìgatecũvẫncóthểdừngseries.

## 14. MR-13 / KH-02 — Lịch sử thử nghiệm trước khi bỏ lookahead (24/11/2026)

**Đã hiện thực và chạy3mục theo yêu cầu mới của người dùng.** Trạng thái dừng trước đó đã được thay bằng nhiệm vụ cụ thể này; KH-03 fullseriesplanner vẫn chưa triển khai.

| Nội dung | Mapping phục vụ báo cáo |
|---|---|
| Phân loại/nguồn | MH nền: Chương1 trung bình/xác suất/kỳ vọng, Chương5x tổng hợp/lọc dữ liệu; điểmcontent có Chương6, mô hình phản ứng nềnChương4. MR tựthiết kế: loss pool/self-denial/accessfactor, shortlist/rollout/leafproxy/sensitivity. NV: CLI/trace/report. [Nguồnsearch/evaluatorStanfordCS221](https://web.stanford.edu/class/archive/cs/cs221/cs221.1196/lectures/games2-6pp.pdf) là tham khảo khái niệm, không xác nhận công thứcLMHT của nhóm. |
| Nơi sử dụng | `ban_planner.py`: `BanSearchPolicy`, `BanPlanner.contextual`, `response_distribution`, `evaluate_root`, `finish_rollout`, `leaf_value`, `recommend`; simulator/series gọi qua `--ban-strategy`; `compare_ban_strategies.py` validate/replay/xuấtso sánh. |
| Chức năng | Xét chi phí mất tướng mình cần và giảm lựa chọn địch theo roster/role/slot/Fearless; banroot6ứngviên, rẽ2phản ứng địch đầu rồi tiếp tụcgreedy đúnglịchthật đến3pick mới/max12plies. Không random/épđadạng/casetheotên. |
| Công thức/policy | Poolrole=mean top3priority, đủmẫu trước. Context=(lossđịch-lossmình×accessfactor)/5, factor1khi lấy picktớitrước,.5khi sau. Leaf=(securednewpickscore+remainingpoolvalue)mình/5 trừđịch/5; khôngcộnglạipicktrướcroot. Ban=expectedleaf+.25context. Trọng số thủcông chưa tune. |
| Giả định đối thủ | Dùng OpponentModelđãlưu,saucắtmaskhợplệ;2nhánh giữ lại đượcrenormalize; lưu supported/selected/omittedmass. Khôngmodel hoặc noprediction trongpool thìsoftmaxproxycónhãn. Không fit/trainmới. Cácbướccòn lại làgreedy, khônggọifullminimax/expectimax. |
| Bất định | Lưu sensitivity `[q*v-(1-q),q*v+(1-q)]` cho phầnnhánh chưa xét trongpool hỗ trợ, không CIthốngkê hoặcwinprobability. Meanq21.1%,min5.8%;48/50lượtchồnglấnứngviênkhác nên khôngclaimchắcchắnrootđượcchọntốtnhất. |
| File kết quả thật | [COMPARISON.md](../reports/ban_strategy_comparison/COMPARISON.md), [comparison.json](../reports/ban_strategy_comparison/comparison.json), [checks.json](../reports/ban_strategy_comparison/checks.json); từngmodelegacy/contextual/lookahead cóseries.json,game1..5JSON/log,REPORTvàQUICK_VIEW. [Lookahead100lượt](../reports/ban_strategy_comparison/lookahead/QUICK_VIEW.md) ghiBan1–5/Pick1–5mỗiđội,#turn vàrole. |
| Trace cần đọc | `advice.pool_impact`:rolepoolbefore/after/backup/loss; `search_trace.state`:trạngtháiđãlộ; `candidate_summary` và`root_evaluations`:từngroot/nhánh/leaf/weight; `response_coverage`; top-levelban `ban_truncation_sensitivity`. Lưu elapsed/budget, trace có thểserializedkhôngvòngthamchiếu. |
| Kiểm chứng |57testsPASS, gồm6testbanplanner mới vàregressioncũ;3mode×5draft đều100actions/50uniquePicks, locks0/10/20/30/40. Replay583branch từ295root đúnglịch/Fearless, sâu tốiđa9<12. Snapshot/roster/firstpick/testmodegiốngnhau. Legacy6banđầu1setlặp5ván; contextual/lookahead5set; Jaccard1/.471/.145. Đây chỉ behavioralcomparison, không causalqualitybenchmark. |
| Hiệu năng/giới hạn | Meanbansearch .471s,p95.787s,max1.371s tronglầnchạycócache;23/50banđổi so contexttop1. 41/50picklookaheadvẫnthiếucontextđủmẫu. Chưa evaluatorcơchếcounter, tựflexsearch, tốiưuđểdànhtướngBO5 hoặc independentbanqualitybenchmark. |

Chi tiết công thức, nguồn, ví dụ và lệnh tái lập: [BAN_NGU_CANH_VA_LOOKAHEAD.md](BAN_NGU_CANH_VA_LOOKAHEAD.md). `legacy` vẫn mặc định; bật `--ban-strategy lookahead --ban-response-model models/opponent_model.pkl`. Series test thêm `--allow-statistical-auto`, không nâng độ tin cậy của cácpick thiếu mẫu. Chạy `compare_ban_strategies.py` để validate/cậpnhật report từ3series đãtạo. Các lệnh ghiđè report thì phải lưu mốc/hash phù hợp, không trộnmetriccũ.

### MR-13 / NV-08: bản contextual riêng — 24/11/2026

Không phát sinh kiến thức/phương pháp/chức năng mới. Chạy lại contextual T1–Gen.G5draft với cùngWorldscutoff13/11patchdataset16.20 vàtestoverride. [BảngBan/Pick](../reports/t1_geng_contextual_20261124/QUICK_VIEW.md), [report/căn cứ](../reports/t1_geng_contextual_20261124/REPORT.md), [checks](../reports/t1_geng_contextual_20261124/checks.json). Đã validate100actions/50uniquePicks,khóa0/10/20/30/40vàđánh sốBan/Pick; giữ38pickthiếumẫu có nhãn. Không sửa thuậttoán/model/DB, khôngtrain; không cótỉsố hoặcchứngminhtốiưu.

Tái lập: `.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --ban-strategy contextual --output-dir reports/t1_geng_contextual_20261124`.

## 15. MR-13 / NV-09 — Chỉ duy trì legacy và contextual (24/11/2026)

**Trạng thái: đã thực hiện theo yêu cầu người dùng.** Tài liệu chính: [BAN_LEGACY_VA_CONTEXTUAL.md](BAN_LEGACY_VA_CONTEXTUAL.md). Không thêm lý thuyết mới; MR-13 được thu gọn còn contextual one-step, NV-09 là gỡ luồng/CLI search và thu gọn báo cáo so sánh.

- **Nơi dùng:** `draft_advisor.py:recommend_bans`giữlegacy; `ban_planner.py:ContextualBanPolicy/BanPlanner.contextual/recommend`chỉpoolloss/self-denial; simulator vàserieschỉnhận `--ban-strategy legacy|contextual`; `compare_ban_strategies.py:summarize`chỉđọchaimode. Gỡ ban-response-model và code tìmnhánh, khônggiữsearchngầm.
- **Kiến thức:** legacy làheuristicpresence/priority/gap; contextuallàMRtựthiếtkếpoolmean/top3vàchi phí tựban theofirstpick/Fearless/roster, nềnChương1/5xvàđiểmcontentChương6đãcó. Khôngcònápdụngdepth-limitedsearchtrongbanchạythực. Phươngphápđãbỏgiữmốclịchsửchứkhôngnhậnlàkiếnthứcđangsửdụng.
- **Đầu ra mới:** `advice.contextual_trace`chostate/ứngviên/score/latency;giữ `pool_impact`,khôngcònsearch_trace/branches/treesensitivity. [So sánh2mode](../reports/legacy_contextual_comparison/COMPARISON.md), [metrics](../reports/legacy_contextual_comparison/comparison.json), [checks](../reports/legacy_contextual_comparison/checks.json), [contextual100lượt](../reports/legacy_contextual_comparison/contextual/QUICK_VIEW.md), [legacy100lượt](../reports/legacy_contextual_comparison/legacy/QUICK_VIEW.md).
- **Minh chứng:**57testsPASS;hai series mới5draft/100lượt/50pickskhácnhauđúngFearless0/10/20/30/40; tấtcảpick/ban hai mode giốngmốctrướcgỡsearch. HaiCLIrejectlookahead(exit2),helpkhôngcònban-response-model,outputkhôngsearchfield. Testoverridechọnsố1thiếutincậyđượcgiữ, khôngnângnhãnđộtincậy.
- **Tái lập:** lệnhhai modevàcomparatortrongdocchính; comparator mặc định `reports/legacy_contextual_comparison`, khôngghiđèlịchsử3mode. Các folderlookahead/report3modecũđánh dấuLỊCHSỬ. Khôngtrainmới/xóamodel/đổiDB/raw. Legacydefaultvẫnnhưcũ; contextualphảiđượcchọnquaCLI.
- **Giới hạn:** cảhai làheuristicmộtbước, chưacounterevaluator/fullflex/fullBO5optimalplanner. Banbớtlặpkhôngchứngminhmạnhhơn; modelđốithủcũđượcgiữđộc lập nhưngngoàiphạmviquantâmhiệnhành, khôngđượccontextualgọi.
