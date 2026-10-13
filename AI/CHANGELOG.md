# CHANGELOG (NHẬT KÝ THAY ĐỔI DỰ ÁN)

Tất cả các thay đổi quan trọng về code, CSDL và tài liệu kiến trúc được ghi lại tại đây theo thứ tự thời gian.

---

## [2026-10-10] - CẬP NHẬT TOÀN DIỆN RECOMMENDER: SỬA LỖI MẪU NHỎ, LỌC LANE PHASE 1/2, MÔ PHỎNG ĐA KỊCH BẢN (ĐỘI VÔ DANH VS T1) & GHI CHÚ ROADMAP
- **Tổng hợp Những Việc Đã Hoàn Thành (Completed Enhancements):**
  - **1. Khử Thiên kiến Mẫu nhỏ (Small Sample Bias):** Khắc phục triệt để lỗi Rek'Sai Jungle 2 trận thắng 100% bị tính Tier S+ 99.0% nhờ kỹ thuật Bayesian Shrinkage và Sample Confidence Weighting.
  - **2. Sửa lỗi Lọc Cấm theo Vị trí:** Khắc phục lỗi mất tướng khi lọc theo lane (Karma ở bảng tổng nhưng gõ `sp` bị mất); đồng bộ chuẩn xác `ban_phase` giữa Meta Bans và Target Bans.
  - **3. Sửa lỗi cú pháp & runtime:** Khắc phục lỗi `NameError: reason_text` và `KeyError: tournament_stats` khi xử lý dữ liệu tuyển thủ tân binh/ẩn danh.
  - **4. Nâng cấp Mô phỏng Tournament Draft ([`src/07_recommender/simulate_draft_match.py`](../src/07_recommender/simulate_draft_match.py)):**
    - Hỗ trợ đầy đủ tương tác 2 chiều cho cả Phe Xanh (First Pick) và Phe Đỏ (Counter Last Pick).
    - Tích hợp Menu chọn kịch bản trực quan: Hỗ trợ "ĐỘI VÔ DANH (Bạn) vs T1 (Faker, Oner, Keria, Doran, Peyz)", GAM vs T1, T1 vs GEN.G.
    - T1 AI cấm theo Meta toàn cầu đối với tuyển thủ vô danh; người dùng nhận gợi ý bóc tách toàn bộ tướng tủ của từng thành viên T1.
  - **5. Bộ lọc Ngắt cứng Kèo thua rõ rệt (Hard Cut-off Filter):** Khi đối thủ đã pick trước tướng cùng đường, loại bỏ hoàn toàn các tướng có Winrate đối đầu $< 45\%$ khỏi danh sách gợi ý chọn (loại trừ các kèo bị counter cứng).
  - **6. Khuếch đại Điểm Kèo trên Thực thụ:** Thưởng điểm mạnh cho các kèo trên ($\ge 52\%$) có mẫu tin cậy để đưa Vi (65%), Poppy (80%), Trundle (50%), Jarvan IV (54.1%) lên Top đầu.
- **Đánh dấu Định hướng Cải thiện Toàn diện Tương lai (Global Roadmap Backlog):**
  - Bắt buộc quay lại rà soát và đánh giá lại **TOÀN BỘ hệ thống Ma trận Kèo Đấu (Head-to-Head Matchup Matrix) trên TẤT CẢ các cặp tướng và 5 vị trí**, đối chiếu giữa *Cảm nhận người chơi (Perception)* vs *Dữ liệu thực chiến (Reality)*, và mô phỏng chi phí cơ hội *Đánh đổi Tài nguyên Chéo Bản đồ (Macro Tradeoff)*.

---

## [2026-10-08] - HOÀN THÀNH TASK 3.5 & MILESTONE 3: HỆ THỐNG GỢI Ý CẤM/CHỌN THÔNG MINH, NHẬN DIỆN LỖ HỔNG & THẺ ĐIỀU KIỆN THẮNG
- **Triển khai module Recommender [`src/07_recommender/recommender_engine.py`](../src/07_recommender/recommender_engine.py):**
  - **Phân hệ 1: TargetBanEngine (Hybrid Opponent Target Ban):**
    - Kết hợp 65% Trọng số Đấu Giải (30,000 bản ghi `tournament_players`, Bayesian Smoothed Winrate, 10m Laning Dominance, KDA, Damage Share) + 35% Solo Rank 30 trận gần nhất (`data/pro_player_accounts.json`).
    - Nhận diện đột biến (Spike in Pick Rate & Winrate >= 70%) phát hiện và gắn cờ `🚨 POCKET PICK SPAM RANK` / `🔥 TƯỚNG TỦ THƯƠNG HIỆU`.
    - Đã kiểm thử xuất sắc trên Keria (Bard, Camille, Renata), Chovy (Yone, Tristana, Ahri), Kiaya (Rumble, Urgot, Gwen), Levi, Knight, Bin, Ruler.
  - **Phân hệ 2: MetaPickRecommender (Gợi ý Chọn Chuẩn Meta & Synergy):**
    - Tích hợp Counter-Pick đối đầu lane trực tiếp, Duo Synergy (Mid-Jng, Bot-Sup) và Dynamic Composition Balance (bù đắp AP khi Full AD, bổ sung Hard CC và Frontline).
  - **Phân hệ 3: PunisherEngine (Quét Lỗ Hổng & Con Bài Trừng Phạt):**
    - Nhận diện 4 lỗ hổng cấm/chọn chí mạng: Heavy Melee (3-4 cận chiến -> Illaoi, Darius, Cassiopeia, Brand), Full AD (0 AP -> Malphite, Rammus, Taric), Zero Hard CC (Master Yi, Katarina, Zeri), Full Squishy (Nocturne, Jarvan IV).
    - Tác động gia tăng +12% đến +18.5% Winrate dự đoán (minh chứng qua Hiện tượng Siwoo Illaoi tại LCK).
  - **Phân hệ 4: WinConditionEngine (ADR-014: Thẻ Điều Kiện Thắng):**
    - Tích hợp mô hình K-Means `models/archetype_kmeans.pkl` xác định trường phái đội hình, vẽ Radar 5 trục và trích xuất Thẻ Chiến thuật hoàn chỉnh: Core Carry, Power Spike Timing, Primary Objective, Win Condition, Lose Condition, Do's & Don'ts.
- **Đóng gói mô hình & Artifacts:**
  - Xuất file mô hình đóng gói [`models/recommender_engine.pkl`](../models/recommender_engine.pkl).
  - Danh mục tuyển thủ & Rank tracking: [`data/pro_player_accounts.json`](../data/pro_player_accounts.json).
  - Soạn thảo báo cáo khoa học toàn diện [`src/07_recommender/recommender_engine.md`](../src/07_recommender/recommender_engine.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md) và [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
- **🎉 HOÀN THÀNH 100% MILESTONE 3 (GIAI ĐOẠN 3: MACHINE LEARNING & BAN/PICK AI)!** Sẵn sàng bước sang Giai đoạn 4 (REST API FastAPI & Web App).

---

## [2026-10-08] - HOÀN THÀNH TASK 3.4: PHÂN CỤM K-MEANS & PCA NHẬN DIỆN 4 TRƯỜNG PHÁI ĐỘI HÌNH
- **Triển khai module Machine Learning [`src/06_machine_learning/cluster_archetypes.py`](../src/06_machine_learning/cluster_archetypes.py):**
  - **Vector hóa 160+ tướng:** Xây dựng từ điển thuộc tính chiến thuật 5 trục chuẩn hóa [Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control] và tính toán Vector Đội hình có trọng số vị trí.
  - **Phân cụm K-Means & PCA (Chương 4):**
    - Khảo sát tìm số cụm tối ưu K=4 qua phương pháp Elbow (WCSS giảm mạnh từ 21,122 về 15,966) và Silhouette Analysis (0.1799).
    - Giảm chiều PCA 2D giải thích 68.98% phương sai tích lũy (PC1: 45.95% Tempo, PC2: 23.03% Combat Scale).
    - Phân tích và định danh 4 trường phái đội hình kinh điển:
      1. **Early Snowball & Dive (24.1%):** Đè đường, ép trụ và kết thúc sớm (Win condition: Ăn Sâu Hư Không đợt 1, Trụ Đầu trước phút 14).
      2. **Wombocombo & Objective Control (16.3%):** Giao tranh diện rộng 5v5 quanh hang Rồng và Baron.
      3. **Late-Game Hypercarry (22.7%):** Nuôi siêu chủ lực (Smolder, Jinx, Azir, Kayle) đánh về cuối trận.
      4. **Pick & Split-Push 1-3-1 (36.9%):** Đẩy lẻ 2 cánh và bắt lẻ mục tiêu đơn lập.
  - **Đóng gói mô hình:** Lưu trữ thành công vào [`models/archetype_kmeans.pkl`](../models/archetype_kmeans.pkl). Hỗ trợ CLI `--train` và `--predict`.
  - **Xuất bản bộ 2 biểu đồ 300 DPI vào [`reports/figures/`](../reports/figures/):**
    - **Fig 10:** [`fig10_kmeans_elbow_silhouette.png`](../reports/figures/fig10_kmeans_elbow_silhouette.png) - Phương pháp Elbow & Silhouette Score.
    - **Fig 11:** [`fig11_draft_archetypes_pca_clusters.png`](../reports/figures/fig11_draft_archetypes_pca_clusters.png) - Không gian phân cụm PCA 2D & Bộ 4 biểu đồ Radar 5 trục.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học chi tiết [`src/06_machine_learning/cluster_archetypes.md`](../src/06_machine_learning/cluster_archetypes.md).
  - Soạn thảo 2 tệp giải thích học thuật trong `docs/figure_explain/` (`fig10` và `fig11`) và đồng bộ `reports/figures/figure_explain/`.
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.4.** Sẵn sàng bước sang Task 3.5 (Hệ thống Gợi ý Cấm/Chọn Thông Minh).

---

## [2026-10-04] - HOÀN THÀNH TASK 3.3: ĐÁNH GIÁ TOÀN DIỆN MÔ HÌNH VÀ XUẤT BẢN BỘ 4 BIỂU ĐỒ DIAGNOSTICS (300 DPI)
- **Triển khai module Machine Learning [`src/06_machine_learning/evaluate_models.py`](../src/06_machine_learning/evaluate_models.py):**
  - **Đánh giá hiệu năng 2 giai đoạn:**
    - Cấm/Chọn (Phút 0): Random Forest đạt ROC-AUC = 0.5510, Accuracy = 53.83%, Brier Score = 0.2487, F1 = 0.5771.
    - Thực chiến (Phút 10): Random Forest đạt ROC-AUC = 0.7780, Accuracy = 70.75%, Brier Score = 0.1925, F1 = 0.7023.
  - **Thiết kế và xuất bản bộ 4 biểu đồ nghiên cứu khoa học (300 DPI) vào [`reports/figures/`](../reports/figures/):**
    - **Fig 6:** [`fig6_roc_auc_comparison.png`](../reports/figures/fig6_roc_auc_comparison.png) - Đường cong ROC và Precision-Recall đối chiếu Phút 0 vs Phút 10.
    - **Fig 7:** [`fig7_confusion_matrices.png`](../reports/figures/fig7_confusion_matrices.png) - Ma trận nhầm lẫn (Confusion Matrices Heatmap).
    - **Fig 8:** [`fig8_calibration_curve.png`](../reports/figures/fig8_calibration_curve.png) - Biểu đồ độ tin cậy hiệu chuẩn xác suất (Reliability Diagram).
    - **Fig 9:** [`fig9_draft_vs_snowball_feature_importance.png`](../reports/figures/fig9_draft_vs_snowball_feature_importance.png) - So sánh cơ chế đặc trưng quyết định Phút 0 vs Phút 10.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học chi tiết [`src/06_machine_learning/evaluation_report.md`](../src/06_machine_learning/evaluation_report.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.3.** Sẵn sàng bước sang Task 3.4 (Phân cụm 4 Trường phái Đội hình) và Task 3.5 (Hệ thống Gợi ý Ban/Pick Thông Minh).

---

## [2026-10-04] - HOÀN THÀNH TASK 3.2: XÂY DỰNG MÔ HÌNH SNOWBALL PREDICTION (PHÚT 10)
- **Triển khai module Machine Learning [`src/06_machine_learning/snowball_model.py`](../src/06_machine_learning/snowball_model.py):**
  - **Tích hợp dữ liệu đa nguồn:** Trích xuất và hợp nhất 6,770 quan sát mốc 10 phút từ CSDL SQLite `lol_live_data.db` (4,752 Pro Play bóc tách 5 lane + 2,018 Solo Rank Thách Đấu VN2/KR).
  - **Kỹ thuật 22 đặc trưng chiến thuật:**
    - Macro: `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`, `deathsat10`, `kill_diff`, `kda_ratio`.
    - Micro 5 Lanes: `top_golddiff`, `jng_golddiff`, `mid_golddiff`, `bot_golddiff`, `sup_golddiff`, `carry_gold_lead` (Mid + Bot).
    - Mục tiêu lớn: `firstdragon`, `void_grubs`, `has_3_grubs`, `firsttower`, `double_neutral_control`.
    - Synergy phi tuyến & Context: `gold_dragon_synergy`, `gold_grubs_synergy`, `is_blue_side`, `is_pro_play`.
  - **So sánh mô hình (Test Set 1,354 trận):**
    - Random Forest (150 trees): **ROC-AUC = 0.7780**, Accuracy = 70.75%, Log Loss = 0.5682, Brier Score = 0.1925.
    - Soft Voting Ensemble (LGB + XGB + RF + LR): Accuracy = 71.20%, ROC-AUC = 0.7774.
    - XGBoost: Accuracy = 71.20%, ROC-AUC = 0.7751.
    - Logistic Regression L2: Accuracy = 71.20%, ROC-AUC = 0.7746.
    - LightGBM: Accuracy = 71.27%, ROC-AUC = 0.7730.
  - **Đối chiếu Đấu Giải vs Solo Rank:**
    - Solo Rank: **ROC-AUC = 0.8189**, Accuracy = 73.54% (Lăn cầu tuyết tàn phá tâm lý và không thể lật kèo do thiếu phối hợp).
    - Pro Play: **ROC-AUC = 0.7572**, Accuracy = 69.47% (Các đội chuyên nghiệp kiểm soát tầm nhìn và có thể lật kèo nhờ đội hình Scaling).
  - **Đóng gói mô hình:** Lưu trữ thành công vào [`models/snowball_model.pkl`](../models/snowball_model.pkl). Hỗ trợ CLI `--train` và `--predict`.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học [`src/06_machine_learning/snowball_model.md`](../src/06_machine_learning/snowball_model.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.2.** Sẵn sàng bước sang Task 3.3 (Đánh giá mô hình ROC-AUC & Confusion Matrix).

---

## [2026-10-04] - HOÀN THÀNH TASK 3.1: XÂY DỰNG MÔ HÌNH DRAFT PREDICTION (PHÚT 0)
- **Triển khai module Machine Learning [`src/06_machine_learning/draft_model.py`](../src/06_machine_learning/draft_model.py):**
  - **Trích xuất dữ liệu:** Nạp và xoay trục 3,000 trận đấu giải đỉnh cao (6,000 dòng đội) chuẩn 1NF/3NF từ CSDL SQLite `lol_live_data.db`.
  - **Feature Pipeline đa tầng (799 chiều):**
    - Position-specific Differential One-Hot Vectors (+1 Blue, -1 Red theo 5 lane $\times$ 158 tướng = 790 cột).
    - Tỷ lệ thắng làm mịn Bayes (Bayesian Smoothed Winrates C=10).
    - Tương quan đối đầu trực tiếp 5 cặp đường (Lane Matchup Advantage).
    - Phối hợp cặp đôi (Synergy Duo Mid-Jng và Bot-Sup).
    - Cân bằng thuộc tính đội hình (AD/AP ratio, Hard CC, Tankiness, Early vs Late Scaling).
    - Trọng số suy giảm theo thời gian (Time-decay sample weights Half-life 90 ngày).
  - **So sánh mô hình (Test Set 600 trận theo thời gian):**
    - Random Forest (150 trees): **ROC-AUC = 0.5510**, Brier Score = 0.2487 (Mô hình tối ưu nhất).
    - Logistic Regression L2: **Accuracy = 54.33%**, ROC-AUC = 0.5485.
    - Soft Voting Ensemble: ROC-AUC = 0.5492.
  - **Đóng gói mô hình:** Lưu trữ thành công vào [`models/draft_model.pkl`](../models/draft_model.pkl).
  - **Hỗ trợ CLI Runner:** `--train` để huấn luyện, `--predict` để dự đoán tỷ lệ thắng và bóc tách lợi thế 5 lane theo thời gian thực.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học chi tiết [`src/06_machine_learning/draft_model.md`](../src/06_machine_learning/draft_model.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.1.** Sẵn sàng bước sang Task 3.2 (Mô hình Snowball Phút 10).

---

## [2026-09-30] - BỔ SUNG KIẾN TRÚC DRAFT FLAW & PUNISHER RECOMMENDER
- **Cập nhật đặc tả Task 3.5, Task 4.1 & Module `src/07_recommender/`:**
  - **Phân hệ Nhận diện Lỗ hổng Cấm/Chọn của Địch (Draft Flaw Exploitation):** Tự động phát hiện 4 lỗ hổng chí mạng của đội hình địch: Heavy Melee (3-4 cận chiến), Full AD (không có AP), Zero Hard CC (không có khống chế cứng), Full Squishy (máu giấy không có tanker/mở combat).
  - **Gợi ý Con Bài Trừng Phạt (Punisher Pick Recommender):** Tự động đề xuất các con bài trừng phạt tối thượng tương ứng như trận Siwoo Illaoi (Illaoi/Darius khắc chế Heavy Melee, Malphite/Rammus khắc chế Full AD, Master Yi/Katarina trừng phạt Zero CC) giúp tăng vọt +15% đến +20% winrate dự đoán.
  - **Bổ sung Endpoint API & Web UI:** `POST /api/v1/detect-flaws` trả về Thẻ Cảnh báo Lỗ hổng & Con bài Trừng phạt (Punisher Card) trực quan trên giao diện cấm/chọn.
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`src/07_recommender/README.md`](../src/07_recommender/README.md).

---

## [2026-09-30] - HOÀN THÀNH VÀ ĐÓNG GÓI MILESTONE 2: JUPYTER NOTEBOOK EDA
- **Hoàn thành và đóng gói Notebook [`notebooks/01_kham_pha_du_lieu_EDA.ipynb`](../notebooks/01_kham_pha_du_lieu_EDA.ipynb):**
  - Tích hợp toàn diện 21 cells (6 Markdown dẫn nhập & tổng kết học thuật, 15 Code cells thực thi) bao phủ trọn vẹn chương trình môn học:
    - **Phần 1: Khởi tạo & Tổng quan CSDL SQLite (Chương 2, 5):** Thống kê quy mô 37,009 bản ghi chuẩn 1NF/3NF từ 2 nguồn Đấu Giải và Solo Rank.
    - **Phần 2: 5 Truy vấn SQL nâng cao (Chương 5 & 5x):** Kèo 1v1 đường trên, Cặp đôi đường dưới, Tỷ lệ chọn tướng, Xếp hạng đè đường DENSE_RANK và Phân tầng Lăn cầu tuyết.
    - **Phần 3: 3 Bài toán Thống kê suy diễn (Chương 1):** Two-sample Proportion Z-test Lợi thế Phe Xanh, Two-sample Welch's t-test & Z-test Lăn cầu tuyết lead >= 2,000g, Chi-square & Odds Ratio 3 Sâu Hư Không vs Rồng 1.
    - **Phần 4: Bộ 5 Biểu đồ Trực quan hóa EDA 300 DPI (Chương 3):** Fig 1 (Correlation Heatmap 9x9), Fig 2 (Histogram + KDE Chênh vàng 10p), Fig 3 (Boxplot Kinh tế 5 vị trí), Fig 4 (Scatter + OLS Vàng dẫn vs Thời lượng), Fig 5 (Ma trận 8 tổ hợp mục tiêu lớn Pro vs Rank).
    - **Phần 5: Tổng kết Insights & Định hướng Kỹ thuật:** Tổng hợp 5 phát hiện cốt lõi và tiêu chuẩn kỹ thuật chuyển giao cho Giai đoạn 3 (Machine Learning 2 Giai Đoạn).
  - Đã thực thi qua kernel Jupyter/nbconvert, lưu trữ toàn vẹn toàn bộ outputs bảng số liệu và hình ảnh đồ họa chất lượng cao sẵn sàng nộp và trình chiếu.
  - Hoàn tất 100% Giai đoạn 2 và Milestone 2.

---

## [2026-09-30] - NÂNG CẤP BIỂU ĐỒ FIG 5 (MA TRẬN 8 TỔ HỢP) & XÂY DỰNG BỘ TÀI LIỆU GIẢI THÍCH DOCS/FIGURE_EXPLAIN/
- **Nâng cấp mã nguồn trực quan hóa [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py):**
  - **Tối ưu đồ họa Fig 1 (Correlation Heatmap):** Chuẩn hóa thang đo Colorbar $[-1.0, +1.0]$, căn thẳng hàng tuyệt đối với ma trận bằng `make_axes_locatable`, khử 100% đường lưới trục ngầm bằng `sns.axes_style("white")`.
  - **Nâng cấp toàn diện Fig 5 (Biểu đồ 2 Subplots 8 Tổ Hợp):** Phân rã trọn vẹn 4 mức Sâu Hư Không ($0, 1, 2, 3\text{ Sâu}$) theo 2 trạng thái $Có Rồng 1$ vs $Mất Rồng 1$ cho cả Đấu Giải Chuyên Nghiệp (4,752 quan sát) và Solo Rank Thách Đấu (2,018 quan sát), kèm đường tham chiếu cân bằng 50% và số % trên đầu cột.
  - **Xuất lại toàn bộ bộ 5 biểu đồ 300 DPI** vào [`reports/figures/`](../reports/figures/).
- **Xây dựng bộ tài liệu giải thích chi tiết [`docs/figure_explain/`](../docs/figure_explain/):**
  - Khởi tạo 5 file tài liệu giải thích chuyên sâu (tên file tương ứng khớp 1-1 với từng biểu đồ) và 1 file [`README.md`](../docs/figure_explain/README.md) mục lục:
    1. [`fig1_correlation_heatmap.md`](../docs/figure_explain/fig1_correlation_heatmap.md): Ma trận tương quan Pearson, Colorbar, tại sao đường chéo = 1, phân biệt hệ số r vs tỷ lệ thắng %.
    2. [`fig2_gold_diff_distribution.md`](../docs/figure_explain/fig2_gold_diff_distribution.md): Phân phối chênh lệch vàng (Histogram + KDE), kiểm tra tính chuẩn Gaussian, so sánh Pro vs Rank.
    3. [`fig3_lane_economy_boxplot.md`](../docs/figure_explain/fig3_lane_economy_boxplot.md): Boxplot kinh tế 5 vị trí (Bot 642g > Top 616g > Jng 572g > Mid 556g > Sup 328g), giải thích tính đối xứng gương qua 0 và ngoại lai.
    4. [`fig4_gold_lead_vs_duration.md`](../docs/figure_explain/fig4_gold_lead_vs_duration.md): Vàng dẫn trước vs Thời lượng (Scatter + OLS), ranh giới 20p Baron vs 15p FF15, các trận 11-13p do AFK/Open Mid.
    5. [`fig5_neutral_objectives_scenarios.md`](../docs/figure_explain/fig5_neutral_objectives_scenarios.md): Ma trận 8 tổ hợp mục tiêu (Rồng 1 x 0, 1, 2, 3 Sâu), hiệu ứng bảo hiểm trên 50% của Rồng 1, kèo chia sâu 1R+1S vs 0R+2S, tại sao các cặp đối đầu bù trừ đúng 100%, xử lý bỏ sâu/sâu biến mất.
  - Đồng bộ sang [`reports/figures/figure_explain/`](../reports/figures/figure_explain/).
- **Cập nhật tài liệu quản trị:**
  - Cập nhật [`AI/PROJECT_STATE.md`](PROJECT_STATE.md) (Tiến độ tổng đạt ~65%, Giai đoạn 2 đạt 95%).
  - Cập nhật [`src/05_visualization/plot_eda_figures.md`](../src/05_visualization/plot_eda_figures.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 2.4: TRỰC QUAN HÓA DỮ LIỆU EDA (BỘ 5 BIỂU ĐỒ 300 DPI - CHƯƠNG 3)
- **Triển khai module trực quan hóa dữ liệu EDA [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py):**
  - **Phương pháp & Đồ họa (Chương 3):** Sử dụng `matplotlib` và `seaborn`, thiết lập độ phân giải cao **300 DPI**, bảng màu phân cực chuyên nghiệp (Blue/Red side và Pro/Rank).
  - **Bộ 5 biểu đồ EDA chất lượng cao xuất tại [`reports/figures/`](../reports/figures/):**
    1. **Fig 1:** [`fig1_correlation_heatmap.png`](../reports/figures/fig1_correlation_heatmap.png) - Ma trận tương quan tuyến tính Pearson Heatmap (Tam giác trên) giữa các chỉ số 10p và tỷ lệ thắng.
    2. **Fig 2:** [`fig2_gold_diff_distribution_kde.png`](../reports/figures/fig2_gold_diff_distribution_kde.png) - Phân phối chênh lệch vàng (Histogram 40 bins + KDE Density) đối chiếu Đội Thắng vs Đội Thua ở cả 2 môi trường.
    3. **Fig 3:** [`fig3_lane_economy_boxplot.png`](../reports/figures/fig3_lane_economy_boxplot.png) - Phân bố kinh tế và ngoại lai 5 vị trí thi đấu (Top, Jungle, Mid, Bot, Support) với dải 1.5 IQR.
    4. **Fig 4:** [`fig4_gold_lead_vs_duration_scatter.png`](../reports/figures/fig4_gold_lead_vs_duration_scatter.png) - Mối quan hệ Vàng dẫn trước 10p vs Thời lượng trận đấu (Scatter + Đường hồi quy OLS + Mốc Baron 20p / Đầu hàng sớm FF15).
    5. **Fig 5:** [`fig5_neutral_objectives_scenarios_bar.png`](../reports/figures/fig5_neutral_objectives_scenarios_bar.png) - Grouped Bar Chart So sánh Tỷ lệ thắng 4 Kịch bản Kiểm soát Mục tiêu lớn (3 Sâu vs Rồng 1) kèm vạch 50%.
- **Tài liệu & Báo cáo:**
  - Tạo mới file báo cáo phân tích chi tiết [`src/05_visualization/plot_eda_figures.md`](../src/05_visualization/plot_eda_figures.md).
  - Cập nhật [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).
  - Hoàn tất 100% Task 2.4. Sẵn sàng đóng gói Milestone 2 vào Jupyter Notebook `notebooks/01_kham_pha_du_lieu_EDA.ipynb`.

---

## [2026-09-28] - HOÀN THÀNH TASK 2.3: KIỂM ĐỊNH CHI-SQUARE (χ²) & TỶ SỐ CHÊNH (ODDS RATIO): 3 SÂU HƯ KHÔNG VS RỒNG 1
- **Triển khai module kiểm định giả thuyết thống kê [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py):**
  - **Phương pháp toán học (Chương 1):** Bảng chéo 2x2 (Contingency Table), Kiểm định tính độc lập Chi-square ($\chi^2$), Tỷ số Chênh (Odds Ratio - OR), Woolf Logit 95% CI và Relative Risk (RR).
  - **Kết quả kiểm định thực nghiệm:**
    1. **Đấu Giải Chuyên Nghiệp (Pro Play):**
       - **Rồng Đầu Tiên (First Dragon):** Winrate **59.43%** vs **40.57%**, $\chi^2 = 167.39, p = 2.75 \times 10^{-38} < 0.0001$, $\text{Odds Ratio} = \mathbf{2.145}$ (CI 95%: $[1.910, 2.409]$) $\rightarrow$ Tăng cơ hội thắng gấp **2.15 lần**.
       - **3 Sâu Hư Không (Voidgrubs):** Winrate **55.81%** vs **46.96%**, $\chi^2 = 33.11, p = 8.73 \times 10^{-9} < 0.0001$, $\text{Odds Ratio} = \mathbf{1.427}$ (CI 95%: $[1.265, 1.609]$) $\rightarrow$ Tăng cơ hội thắng gấp **1.43 lần**.
       - **Đổi chéo mục tiêu (Cross-trade):** Đội chỉ ăn Rồng 1 (bỏ Sâu) thắng **55.92%**, trong khi đội chỉ ăn Sâu (bỏ Rồng) chỉ thắng **47.23%** (Rơi xuống dưới 50%!).
    2. **Solo Rank (Thách Đấu):**
       - **Rồng Đầu:** $\text{Odds Ratio} = \mathbf{2.306}$ ($p = 1.60 \times 10^{-18}$).
       - **3 Sâu Hư Không:** $\text{Odds Ratio} = \mathbf{2.031}$ ($p = 2.67 \times 10^{-13}$) $\rightarrow$ Ở Solo Rank, 3 Sâu có giá trị cao hơn Pro Play do người chơi tự đẩy trụ lấy tiền giáp trụ (Plates) lăn cầu tuyết cá nhân.
    3. **Ma trận 4 Kịch bản:** Đội ăn cả 2 (3 Sâu + Rồng 1) thắng **68.66%** ở Pro và **76.28%** ở Rank. Đội mất trắng cả 2 chỉ thắng **35.90%** (Pro) và **36.42%** (Rank).
  - Xuất bảng số liệu ra [`data/processed/hypothesis_test_3_objectives.csv`](../data/processed/hypothesis_test_3_objectives.csv).
- **Cập nhật tài liệu:**
  - Tạo mới file báo cáo phân tích chi tiết [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md).
  - Cập nhật [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).
  - **HOÀN THÀNH 100% CẢ 3 BÀI TOÁN THỐNG KÊ SUY DIỄN CHƯƠNG 1** (Task 2.1 Z-test + Task 2.2 t-test + Task 2.3 Chi-square).

---

## [2026-09-28] - HOÀN THÀNH TASK 2.2: KIỂM ĐỊNH TWO-SAMPLE WELCH T-TEST & Z-TEST HIỆU QUẢ LĂN CẦU TUYẾT (SNOWBALL LEAD >= 2000G)
- **Triển khai module kiểm định giả thuyết thống kê [`src/04_hypothesis_testing/test_snowball_effect.py`](../src/04_hypothesis_testing/test_snowball_effect.py):**
  - **Phương pháp toán học (Chương 1):**
    1. *Two-sample Proportion Z-test:* So sánh Tỷ lệ chuyển hóa chiến thắng (Winrate Conversion) khi dẫn $\ge 2,000$ vàng lúc 10 phút.
    2. *Two-sample Independent Welch's t-test:* So sánh Thời lượng kết thúc trận đấu trung bình (Game Duration).
    3. *Levene's Test for Variance:* Kiểm định tính đồng nhất phương sai đo lường tính ổn định & kỷ luật kiểm soát thế trận.
  - **Kết quả kiểm định thực nghiệm:**
    - **1. Tỷ lệ thắng (Winrate):** Đấu Giải đạt **83.48%** (192/230), Solo Rank đạt **86.04%** (339/394). $Z = -0.8671, p = 0.3859 > 0.05 \rightarrow$ **Chưa đủ bằng chứng bác bỏ $H_0$** (Dẫn 2,000g lúc 10p ở cả 2 môi trường đều nắm chắc $\sim 85\%$ chiến thắng, khác biệt là ngẫu nhiên).
    - **2. Thời lượng trận đấu (Duration):** Đấu Giải = **29.75 phút** vs Solo Rank = **24.46 phút**. $t = +11.4618, p = 1.16 \times 10^{-27} < 0.0001 \rightarrow$ **Bác bỏ $H_0$ cực kỳ mạnh mẽ** (Trận Solo Rank kết thúc nhanh hơn Đấu Giải trung bình **5.3 phút** do văn hóa đầu hàng sớm FF15 và lối đánh giao tranh liên tục).
    - **3. Tính ổn định & Kỷ luật (Variance):** Độ lệch chuẩn Pro Play $\sigma = 4.68$ phút vs Solo Rank $\sigma = 6.80$ phút. $\text{Levene Stat} = 53.1630, p = 9.37 \times 10^{-13} < 0.0001 \rightarrow$ **Bác bỏ $H_0$** (Đấu Giải ổn định, kỷ luật hơn rõ rệt).
    - **Phân tầng 4 mốc:** Mở rộng kiểm định trên các mốc $\ge 1,000$g, $\ge 1,500$g, $\ge 2,000$g, $\ge 3,000$g.
  - Xuất bảng số liệu ra [`data/processed/hypothesis_test_2_snowball.csv`](../data/processed/hypothesis_test_2_snowball.csv).
- **Cập nhật tài liệu:**
  - Tạo mới file báo cáo phân tích chi tiết [`src/04_hypothesis_testing/test_snowball_effect.md`](../src/04_hypothesis_testing/test_snowball_effect.md).
  - Cập nhật [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 2.1: KIỂM ĐỊNH A/B LỢI THẾ PHE XANH (BLUE SIDE ADVANTAGE) QUA Z-TEST 2 PHÍA
- **Triển khai module kiểm định giả thuyết thống kê [`src/04_hypothesis_testing/test_blue_side_advantage.py`](../src/04_hypothesis_testing/test_blue_side_advantage.py):**
  - **Phương pháp toán học:** $Z$-test tỷ lệ 2 phía ($\alpha = 0.05$) kiểm định $H_0: p = 0.5$ vs $H_1: p \neq 0.5$. Tính $Z$-score, $p$-value 2 phía và khoảng tin cậy 95% (Wald & Wilson).
  - **Kết quả kiểm định thực nghiệm:**
    1. **Đấu Giải Chuyên Nghiệp (Pro Play - 3,000 trận):** Tỷ lệ thắng Phe Xanh đạt **53.50%** ($Z = +3.8341, p = 0.000126 < 0.001$, CI: $[51.72\%, 55.28\%]$). **Bác bỏ $H_0$** $\rightarrow$ Lợi thế First Pick & góc nhìn bản đồ của Phe Xanh vượt trội có ý nghĩa thống kê cao.
    2. **Solo Rank (1,009 trận):** Tỷ lệ thắng Phe Xanh đạt **45.49%** ($Z = -2.8648, p = 0.004173 < 0.01$, CI: $[42.42\%, 48.56\%]$). **Bác bỏ $H_0$** $\rightarrow$ Phe Đỏ thắng $54.51\%$ cao hơn do Matchmaking Riot xếp đội có MMR cao hơn sang Phe Đỏ.
    3. **Phân rã theo giải đấu:** LCP ($p=0.0262^*$) và MSI ($p=0.0280^*$) đều bác bỏ $H_0$.
  - Xuất bảng tổng hợp kết quả ra [`data/processed/hypothesis_test_1_blue_side.csv`](../data/processed/hypothesis_test_1_blue_side.csv).
- **Cập nhật tài liệu:**
  - Tạo mới file giải thích báo cáo chi tiết song song [`src/04_hypothesis_testing/test_blue_side_advantage.md`](../src/04_hypothesis_testing/test_blue_side_advantage.md).
  - Cập nhật [`src/04_hypothesis_testing/README.md`](../src/04_hypothesis_testing/README.md), [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).

---

## [2026-09-28] - KHỞI TẠO TỪ ĐIỂN DANH MỤC HÀM, CLASS & API NỘI BỘ DỰ ÁN (DOCS/DANH_MUC_HAM_VA_MODULES.MD)
- **Biên soạn tài liệu tra cứu toàn diện [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md):**
  - Hệ thống hóa $100\%$ các Class, Phương thức (Methods), Hàm độc lập và Hằng số cấu hình thuộc toàn bộ các module mã nguồn hiện có trong `src/`.
  - Phân loại rõ ràng theo 4 module chính:
    1. `src/config/`: `load_dotenv_custom()`, `get_active_esports_season()`, `get_active_esports_file()` và các hằng số toàn cục.
    2. `src/01_data_pipeline/`: Class `RiotApiCrawler` (12 methods), Class `GoogleDriveDataSyncer` (10 methods + 5 module functions), Class `EsportsDatabaseLoader` (7 methods + 2 module functions).
    3. `src/02_preprocessing/`: Class `DataCleaner` (9 methods: IQR, Z-score, Trimming, Winsorization, Domain Filtering, Imputation).
    4. `src/03_database_sql/`: Class `SQLQueryRunner` (4 methods), `extract_queries_from_sql_file()` và đặc tả 5 câu truy vấn SQL trong `queries.sql`.
  - Bổ sung bảng Cheat Sheet tra cứu nhanh (Function Quick Reference Index).
- **Cập nhật hệ thống Prompt khởi động phiên làm việc trong `docs/prompt_ne/`:**
  - Cập nhật [`docs/prompt_ne/prompt1.txt`](../docs/prompt_ne/prompt1.txt) và [`docs/prompt_ne/prompt3.txt`](../docs/prompt_ne/prompt3.txt) bổ sung danh mục file context mới (`DANH_MUC_HAM_VA_MODULES.md`, `KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`) và quy định bắt buộc về `.venv` & Git.
  - Tạo mới [`docs/prompt_ne/prompt4_giai_doan_2_stats_eda.txt`](../docs/prompt_ne/prompt4_giai_doan_2_stats_eda.txt) chuyên dụng để bắt đầu Giai đoạn 2 (Thống kê suy diễn & EDA - Chương 1, 3).

---

## [2026-09-28] - HOÀN THÀNH TASK 1.4: TRIỂN KHAI 5 CÂU TRUY VẤN SQL NÂNG CAO (CHƯƠNG 5 & 5X) & ĐẠT MILESTONE 1
- **Triển khai 5 câu truy vấn SQL phân tích chuyên sâu chuẩn giáo trình Chương 5 & 5x trong [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql):**
  1. **Truy vấn 1 (Kèo đối đầu trực tiếp 1v1 - Lane Matchup):** Áp dụng `Self-JOIN` ghép bảng `tournament_players` qua `gameid`, `position`, `side = 'Blue'` và `side = 'Red'`, kết hợp `GROUP BY` và `HAVING` thống kê tỉ lệ thắng, chênh lệch vàng/lính lúc 10 phút để phát hiện Counter-Pick.
  2. **Truy vấn 2 (Cặp đôi ăn ý đường dưới - Bot Lane Synergy Duo):** Áp dụng `Intra-team JOIN` ghép tuyển thủ Bot + Sup cùng phe, `GROUP BY`, `HAVING count(*) >= 10` xếp hạng cặp đôi có tỷ lệ thắng cao nhất phục vụ thuật toán Gợi ý Cấm/Chọn.
  3. **Truy vấn 3 (Tướng có tỷ lệ Cấm/Chọn cao nhất - Meta Presence Rate):** Áp dụng `CTE (Common Table Expressions)`, `Subqueries` và `Unpivot UNION ALL` tính toán Presence Rate = (Picks + Bans) / Tổng số trận.
  4. **Truy vấn 4 (Xếp hạng tuyển thủ đè đường phút 10 - Lane Dominance Ranking):** Áp dụng `Window Functions: DENSE_RANK() OVER (PARTITION BY position ORDER BY avg_gold_diff_10 DESC)` và `AVG() OVER (PARTITION BY position)` đối chiếu với chuẩn trung bình (Benchmark) toàn giải.
  5. **Truy vấn 5 (Đối chiếu hiệu quả Lăn cầu tuyết: Đấu Giải vs Rank Đơn):** Áp dụng `UNION ALL`, phân tầng rời rạc hóa `CASE WHEN` chênh lệch vàng 10 phút, `GROUP BY` so sánh khả năng chuyển hóa lợi thế thành chiến thắng giữa Pro Play và Solo Queue.
- **Xây dựng Script thực thi và xuất dữ liệu tự động [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py):**
  - Hỗ trợ giao diện CLI chuyên nghiệp: `--query 1..5`, `--limit N`, `--export`.
  - Tự động xuất 5 tệp kết quả phân tích sạch vào `data/processed/sql_query_[1-5]_result.csv`.
- **Nghiệm thu Milestone 1:** Hoàn thành 100% Giai đoạn 1 (Task 1.0, 1.1, 1.2, 1.3, 1.4, 1.5).

---

## [2026-09-28] - TÍCH HỢP QUYẾT ĐỊNH KIẾN TRÚC ADR-014: NHẬN DIỆN ĐIỀU KIỆN THẮNG & TRƯỜNG PHÁI ĐỘI HÌNH
- **Ghi nhận quyết định kiến trúc [ADR-014](DECISIONS.md) trong [`AI/DECISIONS.md`](DECISIONS.md):**
  - Tích hợp tính năng phân tích **Trường phái đội hình (Draft Archetypes qua K-Means & PCA)** và **Khuyến nghị Điều kiện thắng (Win Condition Card)** cho Giai đoạn 3 (ML & Recommender), Giai đoạn 4 (FastAPI Backend endpoint `/api/v1/win-condition` & Web Streamlit) và Giai đoạn 5 (Android App).
  - Phân loại 4 trường phái: *Early Snowball / Dive, Dragon Soul Stacking, Late-Game Hypercarry Scaling, Pick & Split-Push 1-3-1*.
  - Xuất Thẻ điều kiện thắng tự động gồm: Chủ lực gánh đội (Core Carry), Điểm rơi sức mạnh (Power Spike Timing), Mục tiêu ưu tiên số 1 (Primary Objective), và Điều kiện thất bại cần tránh (Lose Condition).
- **Đồng bộ toàn bộ tài liệu:**
  - Cập nhật [`AI/TASKS.md`](TASKS.md) (Task 3.4, 3.5, 4.1, 4.2), [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md), [`src/06_machine_learning/README.md`](../src/06_machine_learning/README.md), [`src/07_recommender/README.md`](../src/07_recommender/README.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 1.3: TIỀN XỬ LÝ, LÀM SẠCH & KHỬ NGOẠI LAI IQR/Z-SCORE (SRC/02_PREPROCESSING/CLEANER.PY)
- **Triển khai module tiền xử lý dữ liệu chuẩn giáo trình Chương 2 [`src/02_preprocessing/cleaner.py`](../src/02_preprocessing/cleaner.py):**
  - **Domain Filtering:** Loại bỏ 100% trận Remake (< 10 phút) và AFK ($CS < 10$).
  - **Khử Missing Values:**
    - Zero Imputation cho biến sự kiện đếm (`elders`, `atakhans`, `doublekills`...).
    - Categorical Imputation (`'NoBan'`) cho các lượt cấm để trống.
    - Phân luồng dữ liệu thông minh qua `datacompleteness` cho bài toán Snowball mốc 10 phút.
  - **Khử Outlier linh hoạt (IQR & Z-Score):**
    - Hỗ trợ cả 2 thuật toán: IQR ($1.5 \times IQR$) và Z-Score ($|Z| > 3.0$).
    - Hỗ trợ cả 2 cơ chế: Trimming (Lọc bỏ ngoại lai) và Winsorization / Capping (Cắt ngọn giữ nguyên cỡ mẫu).
  - **Kỹ nghệ đặc trưng:** Tính toán các chỉ số bổ trợ `goldDiffPerMin10`, `csDiffPerMin10`, `kda`.
  - **Xuất thành công 4 tệp dữ liệu sạch vào `data/processed/`:**
    1. `clean_ranked_10min.csv`: 977 dòng sạch.
    2. `clean_tournament_10min.csv`: 4,636 dòng sạch.
    3. `clean_tournament_draft.csv`: 6,000 dòng sạch (3,000 trận đỉnh cao).
    4. `clean_tournament_players.csv`: 28,880 dòng sạch.
  - Tích hợp báo cáo kiểm định chất lượng làm sạch trực quan (Data Cleaning Card).
- **Cập nhật tài liệu:**
  - Cập nhật [`src/02_preprocessing/README.md`](../src/02_preprocessing/README.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md), [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 1.2: NẠP DỮ LIỆU ĐẤU GIẢI VÀO CSDL SQLITE (TOURNAMENT_MATCHES & TOURNAMENT_PLAYERS)
- **Triển khai module ETL [`src/01_data_pipeline/load_esports_to_db.py`](../src/01_data_pipeline/load_esports_to_db.py):**
  - Đọc và làm sạch dữ liệu từ tệp hoạt động `data/raw/esports_active_matches.csv` (3,000 trận đỉnh cao, 36,000 dòng).
  - Tự động chuẩn hóa tên cột (snake_case hợp lệ, xử lý ký tự đặc biệt như `dragons (type unknown)` $\rightarrow$ `dragons_type_unknown`, `team kpm` $\rightarrow$ `team_kpm`, `earned gpm` $\rightarrow$ `earned_gpm`, `total cs` $\rightarrow$ `total_cs`).
  - Phân tách và nạp thành công 2 bảng CSDL chuẩn 1NF/3NF vào `data/database/lol_live_data.db`:
    1. `tournament_matches`: **6,000 dòng** (3,000 trận $\times$ 2 đội Xanh/Đỏ), 155 cột. Khóa chính: `(gameid, side)`.
    2. `tournament_players`: **30,000 dòng** (3,000 trận $\times$ 10 tuyển thủ), 129 cột. Khóa chính: `(gameid, participantid)`. Khóa ngoại: `(gameid, side) REFERENCES tournament_matches(gameid, side) ON DELETE CASCADE`.
  - Tự động tạo 12 Indexes tối ưu hóa tốc độ truy vấn cho các câu lệnh SQL ở Module 03.
  - Tích hợp báo cáo kiểm định chất lượng dữ liệu tự động (Data Integrity Audit): Xác thực số trận, phân bổ giải đấu (LPL: 1,160; LCK: 850; LCP: 466; EWC: 265; MSI: 151; WLDS: 108), tỷ lệ có timeline 10 phút (79.0%), và chạy thử nghiệm các truy vấn phân tích (Top Pick Champions, Top Winrate Teams).
- **Cập nhật tài liệu:**
  - Cập nhật [`src/01_data_pipeline/README.md`](../src/01_data_pipeline/README.md), [`src/03_database_sql/README.md`](../src/03_database_sql/README.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/DATABASE.md`](DATABASE.md), [`AI/TASKS.md`](TASKS.md), [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md).

---

## [2026-09-20] - TÍCH HỢP BỘ 6 GIẢI ĐẤU QUỐC TẾ (MSI, WLDS, EWC) & CHỨC NĂNG THẨM ĐỊNH SỨC KHỎE DỮ LIỆU (--CHECK)
- **Tích hợp các giải đấu quốc tế danh giá vào tập dữ liệu:**
  - Bổ sung các mã giải quốc tế chính thức của Oracle's Elixir: `WLDS` (World Championship / CKTG), `MSI` (Mid-Season Invitational), `EWC` (Esports World Cup).
  - Chạy đồng bộ lệnh: `python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL,MSI,WLDS,EWC`.
  - Kết quả: Tập dữ liệu đạt **3,000 trận (36,000 dòng, 26.8 MB)**, trong đó số trận có Timeline mốc 10 phút tăng vọt từ 70.4% lên **79.0% (2,369 / 3,000 trận)**.
  - Phân bổ chi tiết: LPL (1,160 trận), LCK (850 trận), LCP (466 trận), EWC (265 trận), MSI (151 trận), WLDS (108 trận).
- **Phát triển module Thẩm định Sức khỏe Dữ liệu (Data Health Card):**
  - Thêm phương thức `check_data_health(filepath)` trong `GoogleDriveDataSyncer` và hàm cấp module `check_esports_data_health()`.
  - Hỗ trợ cờ CLI `python src/01_data_pipeline/sync_google_drive.py --check`.
  - Thẩm định đa tầng: Quy mô, cấu trúc chuẩn 12 dòng/trận của Oracle's Elixir (đạt 100% hoàn hảo), phân bổ giải đấu, và audit missing values theo phân tầng: Cốt lõi, Mục tiêu Team (0% khuyết), và Timeline mốc 10 phút.
- **Giải quyết triệt để lỗi Google Drive Quota Exceeded (Lỗi 403 tải ẩn danh):**
  - Tích hợp kiến trúc tải 2 tầng trong `src/01_data_pipeline/sync_google_drive.py`:
    - **Tầng 1:** `gdown` tải ẩn danh nhanh; kiểm tra tính toàn vẹn (file > 100 KB, không phải HTML lỗi).
    - **Tầng 2:** Kích hoạt tự động khi gặp Quota Exceeded, dùng Google Drive API v3 kết hợp OAuth 2.0 (`credentials.json` Desktop Client, lưu token cache `.gdrive_token.json`).
    - Áp dụng thuật toán **Smart Copy**: Tự nhân bản file công khai vào Google Drive cá nhân của người dùng qua `service.files().copy()` $\rightarrow$ Vượt 100% hạn ngạch công khai $\rightarrow$ Stream tải 8MB/chunk $\rightarrow$ Tự động xóa bản sao tạm bằng `service.files().delete()`.
- **Bảo mật & Cập nhật tài liệu:**
  - Bổ sung `credentials.json`, `token.json`, `.gdrive_token.json` vào `.gitignore`.
  - Đồng bộ toàn bộ tài liệu: `README.md`, `README_SYNC_DRIVE.md`, `AI/PROJECT_STATE.md`, `AI/TASKS.md`, `docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`.

---

## [2026-09-20] - HOÀN THÀNH TASK 1.1: TÍCH LŨY 1,009 TRẬN RANK ĐỈNH CAO (VN2 & KR) ĐẠT CHUẨN 1NF/3NF
- **Cào dữ liệu Live Rank hoàn tất qua `crawl_riot_matches.py`:**
  - Tích lũy thành công **1,009 trận** xếp hạng đơn/đôi (vượt mốc chỉ tiêu 1,000 trận).
  - Phân bổ cân đối Multi-server: **550 trận** máy chủ Việt Nam (`VN2`) và **459 trận** máy chủ Hàn Quốc (`KR`).
  - Đảm bảo 100% chuẩn 1NF (10 cột lane nguyên tử `blueTop`..`redSupport`), 3NF (loại bỏ cột `country` phụ thuộc hàm, lưu cột `server`).
  - Thu thập đầy đủ 10 lượt cấm (`blueBans`, `redBans`) và chỉ số kinh tế mốc 10 phút.
  - Đồng bộ lưu song song vào CSDL SQLite `data/database/lol_live_data.db` (bảng `matches_10min`) và file `data/processed/lol_live_ranked_10min.csv` (1,009 $\times$ 42 cột, 0 giá trị NULL ở các cột chính).
- **Cập nhật trạng thái:**
  - Đánh dấu hoàn thành Task 1.1 trong [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md) và [`AI/TASKS.md`](TASKS.md).

---

## [2026-09-20] - THUẬT TOÁN QUYẾT ĐỊNH MÙA GIẢI THÔNG MINH (ADR-013) & BỘ LỌC GIẢI ĐẤU (LCK, LCP, LPL...)
- **Nâng cấp `src/01_data_pipeline/sync_google_drive.py`:**
  - Bổ sung hàm `parse_leagues()` và hỗ trợ tham số `--leagues` (ví dụ: `LCK,LCP,LPL`, `VCS`...).
  - Bổ sung hàm `count_matches(filepath, leagues=None)` đếm số lượng trận đấu độc lập trong phạm vi giải đấu chỉ định.
  - Bổ sung hàm `build_adaptive_dataset(latest_year, previous_year, min_matches, leagues=None)`:
    - Lấy toàn bộ năm mới nhất + trích xuất phần cuối năm trước (CKTG / Mùa Hè) cho đến khi đủ số lượng yêu cầu.
  - Bổ sung hàm `sync_smart_latest(min_matches, leagues, force)`:
    - Tự động thẩm định số trận trong phạm vi giải đấu chỉ định.
    - Xuất tệp hoạt động `data/raw/esports_active_matches.csv` lọc chuẩn xác các giải đấu yêu cầu.
- **Nâng cấp `src/config/settings.py` & `src/config/__init__.py`:**
  - Bổ sung cấu hình `ESPORTS_TARGET_LEAGUES` đọc từ `.env`.
  - Cập nhật hàm `get_active_esports_file()` tự động nhận diện `esports_active_matches.csv` nếu có.
- **Cập nhật tài liệu & file mẫu:**
  - Cập nhật [`src/01_data_pipeline/README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md), `.env.example`, và ghi nhận kiến trúc [ADR-013](DECISIONS.md) trong [`AI/DECISIONS.md`](DECISIONS.md).

---

## [2026-09-20] - THIẾT LẬP MÔI TRƯỜNG ẢO NỘI BỘ (.VENV) & ĐỒNG BỘ TOÀN DIỆN TÀI LIỆU DỰ ÁN
- **Khởi tạo môi trường ảo `.venv` cục bộ (Python 3.13.14):**
  - Tọa lạc tại: `d:\Chivinh\2026_MonHoc\Nhập môn khoa học dữ liệu\Project\.venv`.
  - Cài đặt đầy đủ 100% các package trong `requirements.txt`: `pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `gdown`, `requests`, `python-docx`, `jupyter`, `ipykernel`.
  - Thiết lập `.vscode/settings.json` tự động nhận diện và kích hoạt `.venv` khi chạy mã trong VS Code.
  - Bảo vệ Git: Cả `.venv/` và `.vscode/` đều được chặn commit an toàn trong `.gitignore`.
- **Cập nhật đồng bộ toàn bộ hệ thống tài liệu Markdown (`.md`):**
  - [`README.md`](../README.md): Viết lại hoàn chỉnh với khối lệnh kích hoạt `.venv` nổi bật, cập nhật cây thư mục mới, và hướng dẫn Quick Start 4 bước rõ ràng.
  - [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md): Cập nhật Giai đoạn 1 với Task 1.0 (.venv) và Task 1.5 (Cloud Data Auto-Sync).
  - [`docs/DANH_MUC_API_VA_DATASET.md`](../docs/DANH_MUC_API_VA_DATASET.md): Bổ sung liên kết Google Drive dùng chung và module `sync_google_drive.py`.
  - [`AI/TASKS.md`](TASKS.md): Nghiệm thu Task 1.0 và làm giàu tiêu chí Task 1.5.
  - [`AI/DECISIONS.md`](DECISIONS.md): Ghi nhận quyết định kiến trúc [ADR-011](DECISIONS.md) (.venv) và [ADR-012](DECISIONS.md) (Tự động phát hiện mùa giải & Phân tách tài liệu).
  - [`AI/ARCHITECTURE.md`](ARCHITECTURE.md): Bổ sung trách nhiệm 2 script module 01 và chuẩn môi trường thực thi Section 3.
  - [`AI/PROJECT_STATE.md`](PROJECT_STATE.md): Cập nhật trạng thái môi trường thực thi `.venv` đã xác thực.

---

## [2026-09-20] - PHÂN TÁCH TÀI LIỆU PIPELINE THÀNH 2 FILE ĐỘC LẬP & TỰ ĐỘNG HÓA MÙA GIẢI ĐỘNG
- **Phân tách tài liệu chi tiết thành 2 file chuyên biệt:**
  - [`src/01_data_pipeline/README_CRAWL_RIOT.md`](../src/01_data_pipeline/README_CRAWL_RIOT.md): Hướng dẫn toàn diện module cào Live Rank từ Riot Games API (kiến trúc, bóc tách timeline phút thứ 10, chuẩn 1NF/3NF, chống Rate Limit HTTP 429).
  - [`src/01_data_pipeline/README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md): Hướng dẫn toàn diện module đồng bộ Google Drive Oracle's Elixir (kiến trúc, cache manifest, regex trích xuất năm, hướng dẫn vượt hạn ngạch Google Drive Quota Exceeded).
  - [`src/01_data_pipeline/README.md`](../src/01_data_pipeline/README.md): Chuyển thành trang Tổng quan / Hub điều hướng liên kết trực tiếp tới 2 tài liệu trên.
- **Nâng cấp thuật toán tự động đón đầu tương lai (Future-Proof Season Discovery):**
  - Cập nhật [`sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py) hàm `get_recent_years(n_recent=2)` quét regex `^(\d{4})_LoL_...csv` trên Drive.
  - Tự động nhận diện và đồng bộ mùa giải mới nhất (khi có 2027 sẽ tự động kéo `[2026, 2027]` mà không cần sửa code).

---

## [2026-09-20] - XÂY DỰNG HOÀN TẤT MODULE ĐỒNG BỘ GOOGLE DRIVE (SYNC_GOOGLE_DRIVE.PY)
- **Triển khai module [src/01_data_pipeline/sync_google_drive.py](../src/01_data_pipeline/sync_google_drive.py):**
  - Tích hợp kết nối trực tiếp với Thư mục Google Drive Oracle's Elixir (`1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`).
  - Sử dụng `gdown` để quét danh mục siêu nhẹ 13 mùa giải (2014-2026) mà không cần tải dữ liệu nặng (`--list`).
  - Cơ chế Cache Manifest (`.drive_sync_manifest.json`): Tự động phát hiện dung lượng file cục bộ để bỏ qua tải trùng lặp, tiết kiệm 71 MB băng thông mạng.
  - Hỗ trợ tham số linh hoạt: Tải năm chỉ định (`--year`), tải toàn bộ lịch sử (`--all`), và ép buộc làm mới (`--force`).
- **Cập nhật cấu hình & tài liệu:**
  - Thêm `GOOGLE_DRIVE_FOLDER_ID` vào `src/config/settings.py`, `src/config/__init__.py`, `.env`, `.env.example`.
  - Bổ sung `gdown>=6.4.0` vào `requirements.txt`.
  - Cập nhật tài liệu hướng dẫn vận hành trong [src/01_data_pipeline/README.md](../src/01_data_pipeline/README.md).
  - Hoàn thành nghiệm thu **Task 1.5** trong [AI/TASKS.md](TASKS.md).

---

## [2026-09-20] - BỔ SUNG KIẾN TRÚC & TASK ĐỒNG BỘ DỮ LIỆU TỰ ĐỘNG TỪ GOOGLE DRIVE
- **Quy hoạch tính năng Cloud Data Auto-Sync (Task 1.5):**
  - Bổ sung quyết định kiến trúc [ADR-010](DECISIONS.md) và phân rã nhiệm vụ trong [AI/TASKS.md](TASKS.md).
  - Cơ chế: Hệ thống tự động kiểm tra thời gian cập nhật (`modifiedTime`) hoặc hash `md5Checksum` của tệp/thư mục Google Drive chia sẻ (tập dữ liệu giải đấu, nhãn bổ sung).
  - Tối ưu hóa: Chỉ tải về `data/raw/` khi trên Drive có dữ liệu mới; tự động kích hoạt pipeline làm sạch và cập nhật CSDL SQLite phục vụ làm việc nhóm khép kín.

---

## [2026-09-20] - FIX BUG ĐIỀU KIỆN DỪNG CỦA CRAWLER TRÊN CSDL ĐA MÁY CHỦ
- **Sửa lỗi ngắt sớm tại hàm `get_match_ids` trong [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py):**
  - Nguyên nhân: Trước đó điều kiện dừng kiểm tra `len(match_ids) + len(existing_ids) >= target_count`. Do CSDL đã có sẵn 99 trận từ máy chủ VN2 (`existing_ids = 99`), khi máy chủ KR vừa cào được đúng 1 trận (`1 + 99 = 100`) thì bị kích hoạt lệnh `break` dừng sớm.
  - Khắc phục: Sửa điều kiện dừng thành `len(match_ids) >= target_count`. Biến `existing_ids` chỉ dùng để lọc trùng lặp trận đã có trong DB (`if m_id not in existing_ids`).
  - Kết quả: Đảm bảo crawler cào đủ số lượng trận độc lập cho từng máy chủ theo đúng cấu hình `TARGET_MATCHES_PER_SERVER`.

---

## [2026-09-20] - KHÔI PHỤC CẤU TRÚC THƯ MỤC PIPELINE & BỔ SUNG README.MD CHUẨN HÓA
- **Khôi phục toàn bộ các thư mục theo kiến trúc chuẩn:**
  - Khôi phục các thư mục từ bước 02 đến 07: `src/02_preprocessing/`, `src/03_database_sql/`, `src/04_hypothesis_testing/`, `src/05_visualization/`, `src/06_machine_learning/`, `src/07_recommender/`.
  - Khôi phục các thư mục bổ trợ: `notebooks/`, `reports/figures/`.
- **Chuẩn hóa tài liệu nội bộ từng module:**
  - Thay thế toàn bộ các file tạm `.gitkeep` bằng các file `README.md` chi tiết cho từng thư mục.
  - Mỗi file `README.md` mô tả rõ mục tiêu, trách nhiệm phân công, dữ liệu đầu vào (Input), dữ liệu đầu ra (Output) và tiêu chuẩn chất lượng.
  - Vừa giúp Git theo dõi và duy trì cấu trúc thư mục vĩnh viễn, vừa phục vụ tài liệu tra cứu trực quan khi làm việc nhóm và nộp bài.

---

## [2026-09-20] - ĐÓNG GÓI CẤU HÌNH VÀO PACKAGE SRC/CONFIG/
- **Tách cấu hình vào thư mục riêng chuẩn mực:**
  - Tạo package [src/config/](../src/config/) gồm `settings.py` và `__init__.py`.
  - Quản lý tập trung toàn bộ biến môi trường (`.env`), xác thực Riot API key, đường dẫn thư mục I/O (`BASE_DIR`, `DATA_DIR`, `OUTPUT_CSV`, `OUTPUT_DB`), thông số server (`ACTIVE_SERVERS`, `SERVER_METADATA`).
  - Xóa file `config.py` ở thư mục gốc Project để giữ cấu trúc thư mục sạch sẽ, không có file lẻ đứng giữa đường.
- **Cập nhật script crawler [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py):**
  - Import cấu hình trực tiếp từ `src.config` (kèm fallback an toàn).
  - Loại bỏ các khối logic kiểm tra key trùng lặp vì module cấu hình đã tự động kiểm tra ngay khi nạp.
  - Chạy thử nghiệm thành công 100% không phát sinh bất kỳ lỗi đường dẫn nào.
- **Quy tắc Git:** Tuyệt đối không commit hay push tự động; giữ toàn bộ thay đổi ở Working Tree để User toàn quyền kiểm soát.

---

## [2026-09-20] - HOÀN NGUYÊN NGUYÊN TRẠNG BẢN CRAWLER ĐƠN LẬP (COMMIT 40dced0)
- **Hoàn nguyên mã nguồn [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py):**
  - Giữ nguyên cấu trúc xác định thư mục gốc `BASE_DIR = os.path.dirname(...)` nguyên bản.
  - Giữ nguyên toàn bộ cấu hình `.env`, biến môi trường, đường dẫn I/O và metadata tập trung trong một file duy nhất.
  - Dọn sạch toàn bộ các file cấu hình phát sinh ngoài luồng (`src/config.py`, `src/logger.py`, `pyproject.toml`, `tests/`, `.github/`).
- **Cập nhật quy tắc quản trị [AI/AI_RULES.md](AI_RULES.md):**
  - Bổ sung quy định bắt buộc: **TUYỆT ĐỐI KHÔNG tự ý chạy lệnh `git push` lên GitHub** khi chưa có sự cho phép trực tiếp từ User.


## [2026-09-20] - DỌN DẸP DỰ ÁN TINH GỌN (CLEAN CODEBASE)
- **Xóa bỏ file trùng lặp:**
  - Xóa file `crawl_riot_matches.py` ở root, chỉ giữ lại một file chính thức duy nhất tại [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py).
- **Xóa bỏ thư mục không dùng (`archive/`):**
  - Xóa toàn bộ thư mục `archive/` chứa các script nháp cũ không liên quan (`vietnam_housing.db`, `test_pull_housing.py`, các file test nháp).
- **Đồng bộ hóa tài liệu:**
  - Cập nhật `README.md` và `AI/PROJECT_STATE.md`.
  - Đẩy thay đổi dọn dẹp lên GitHub repository.

## [2026-09-20] - KẾT NỐI VÀ ĐẨY DỰ ÁN LÊN GITHUB REPOSITORY
- **Git & Remote:**
  - Khởi tạo Git repository cục bộ (`git init`).
  - Thiết lập nhánh mặc định là `main` (`git branch -M main`).
  - Thêm remote origin: `https://github.com/chivinh123abc/StrategyPredictionAndRecommendation.git`.
  - Thực hiện commit đầu tiên gồm 42 files (toàn bộ source code, thư mục `AI/`, `docs/`, `data/processed/`).
  - Đẩy thành công lên GitHub (`git push -u origin main` - SUCCESS).
  - Đảm bảo an toàn: File `.env` chứa key và file dữ liệu thô 71.1 MB được giữ cục bộ an toàn, không bị commit lên GitHub.

## [2026-09-20] - CẤU HÌNH BIẾN MÔI TRƯỜNG (.ENV) VÀ BẢO VỆ API KEY
- **Bảo mật:**
  - Cập nhật `.gitignore` bỏ qua `.env`, `.env.*` (ngoại trừ `.env.example`).
  - Tạo `.env` chứa `RIOT_API_KEY`, `ACTIVE_SERVERS`, `TARGET_MATCHES_PER_SERVER`.
  - Tạo `.env.example` làm mẫu cấu hình an toàn cho repository.
  - **Triệt tiêu 100% hardcode:** Xóa hoàn toàn giá trị fallback cũ trong mã nguồn `os.getenv()`, thêm exception `ValueError` cảnh báo bắt buộc nạp key từ `.env`.
- **Mã nguồn:**
  - Cập nhật `crawl_riot_matches.py` và `src/01_data_pipeline/crawl_riot_matches.py` tự động đọc cấu hình từ `.env` bằng thư viện chuẩn `os`.
  - Test kiểm thử: Nạp thành công key từ `.env` không phụ thuộc vào code (PASS).

## [2026-09-20] - AUDIT DỰ ÁN & THIẾT LẬP HỆ THỐNG QUẢN TRỊ NGỮ CẢNH (AI/)
- **Thực hiện:** Kiểm tra toàn bộ mã nguồn, dữ liệu thực tế, các gói thư viện cài đặt và CSDL SQLite.
- **Phát hiện quan trọng:**
  - `src/01_data_pipeline/crawl_riot_matches.py` và `crawl_riot_matches.py` đã hoạt động tốt, CSDL có 100 trận (99 VN2, 1 KR).
  - Các thư mục `src/02_` đến `src/07_`, `notebooks/`, `reports/` hiện đang rỗng.
  - Python 3.10.11 đã cài đặt `pandas`, `numpy`, `matplotlib`, `requests`. Chưa cài đặt `scikit-learn`, `scipy`, `fastapi`, `uvicorn`.
- **Tài liệu tạo mới trong `AI/`:**
  - `AI/AI_RULES.md`: Bộ quy tắc làm việc và giao thức bắt buộc cho AI sessions.
  - `AI/PROJECT_STATE.md`: Hiện trạng thực tế sau audit.
  - `AI/ARCHITECTURE.md`: Kiến trúc hệ thống 3 tầng (Data $\rightarrow$ FastAPI $\rightarrow$ Web/Mobile).
  - `AI/DATABASE.md`: Đặc tả chi tiết 42 cột của bảng `matches_10min` và các bảng giải đấu dự kiến.
  - `AI/TASKS.md`: Atomic checklist chi tiết 5 giai đoạn cho 3 thành viên.
  - `AI/DECISIONS.md`: Ghi nhận 7 quyết định kiến trúc cốt lõi (ADR-001 đến ADR-007).
  - `AI/CHANGELOG.md`: Nhật ký thay đổi này.
- **Tài liệu hỗ trợ quản lý:**
  - Tạo `docs/clickup_import_lol_project.csv` hỗ trợ kéo thả toàn bộ 23 task vào ClickUp trong 30 giây.
  - Cập nhật `README.md` phân tầng rõ ràng Giao diện Web App (Giai đoạn 1) và Mobile App (Giai đoạn 2).

---

## [2026-09-19] - CHUẨN HÓA CSDL 1NF & 3NF VÀ XỬ LÝ LỖI PIPELINE
- **Mã nguồn:**
  - Sửa lỗi `NameError: TARGET_MATCHES_PER_SERVER` trong `crawl_riot_matches.py`.
  - Tích hợp xử lý giới hạn tốc độ (Rate Limit 429) với cơ chế Exponential Backoff.
- **Cơ sở dữ liệu & Dữ liệu:**
  - **1NF:** Tách bỏ `blueChampions` và `redChampions` thành 10 cột nguyên tử (`blueTop`..`blueSupport`, `redTop`..`redSupport`).
  - **3NF:** Xóa bỏ cột `country` do phụ thuộc hàm vào `server`.
  - Tái tạo bảng `matches_10min` trong `data/database/lol_live_data.db` và file `data/processed/lol_live_ranked_10min.csv` về đúng 42 cột chuẩn mực.
  - Tạo tệp `data/raw/sample_2026_esports_100.csv` (100 dòng) từ file 71.1 MB của Oracle's Elixir để chống đơ VS Code.

---

## [2026-09-18] - KHỞI TẠO DỰ ÁN & ĐẶC TẢ ĐỒ ÁN
- Khởi tạo cấu trúc dự án `src/`, `data/`, `docs/`, `notebooks/`, `reports/`.
- Soạn thảo đặc tả đề tài liên môn gửi TS. Thái Tuyết Hải và ThS. Nguyễn Trung Hiếu.
- Viết crawler ban đầu kết nối Riot Games Developer API.
