# BÁO CÁO ĐỒ ÁN CUỐI KỲ
## HỆ THỐNG TRỢ LÝ PHÂN TÍCH CẤM/CHỌN (BAN/PICK), DỰ ĐOÁN KẾT QUẢ 2 GIAI ĐOẠN & ĐỐI CHIẾU PRO PLAY VS SOLO QUEUE TRONG LIÊN MINH HUYỀN THOẠI

---

- **Học phần:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science)
- **Đơn vị:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)
- **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải
- **Nhóm thực hiện:** Nhóm 3 sinh viên
- **Mốc chốt số liệu báo cáo:** 24/11/2026
- **Tài liệu đối chiếu gốc:** [Sổ kiến thức & minh chứng](../../docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md) · [Phạm vi đồ án vừa sức](../../docs/PHAM_VI_DO_AN_VUA_SUC.md) · [Mục lục báo cáo](../README.md)

---

## TÓM TẮT (ABSTRACT)

Đồ án vận dụng quy trình Khoa học Dữ liệu theo nội dung **Chương 1–6** của học phần — bao gồm thu thập và làm sạch dữ liệu, lưu trữ và truy vấn SQL/Pandas, thống kê mô tả và kiểm định giả thuyết, trực quan hóa dữ liệu (EDA), học máy phân loại (Machine Learning) và hệ thống gợi ý dựa trên nội dung (Content-Based Filtering) — áp dụng trên hai tập dữ liệu thực tế của trò chơi Liên Minh Huyền Thoại (LMHT): **3,000 trận đấu giải chuyên nghiệp** (Oracle's Elixir: 6,000 bản ghi đội, 30,000 bản ghi tuyển thủ) và **1,009 trận Solo Queue Rank cao** (Riot Games API: 550 VN2, 459 KR), kèm kho dữ liệu Rank tăng dần tách biệt (`ranked_evidence.db`, 975 trận tại mốc chốt 24/11/2026) để đối chiếu bằng chứng.

Trên nền tảng môn học, nhóm phát triển các phần mở rộng có giải thích rõ ràng gồm: hệ thống mô phỏng Cấm/Chọn theo thể thức Fearless Draft (tối đa 5 ván), chiến lược Ban ngữ cảnh (`contextual` v2), cơ chế kiểm tra độ tin cậy mẫu đối đầu (`lane_review`, `pair_reservation`) và một giao diện Web cục bộ (React/TypeScript + FastAPI) tái sử dụng trực tiếp động cơ Python. Mọi kết quả thực nghiệm đều được công bố minh bạch kèm baseline, khoảng tin cậy và giới hạn: mô hình dự đoán giai đoạn Snowball phút 10 đạt Accuracy `0.6718` (AUC `0.7413`), trong khi mô hình Draft phút 0 đạt Accuracy `0.5517` (AUC `0.5628`, thấp hơn baseline `training_prior` `0.565` về độ chính xác nhãn cứng nhưng cải thiện nhẹ log-loss) và Content-Based đạt Recall@5 `0.2990` (thấp hơn baseline popularity `0.4652`). Đồ án trình bày thẳng thắn nguyên nhân, không phóng đại hiệu năng và không đánh đồng điểm gợi ý thống kê với xác suất thắng hay bằng chứng khắc chế cơ chế.

---

## CHƯƠNG 1. GIỚI THIỆU BÀI TOÁN & PHÂN ĐỊNH KIẾN THỨC MÔN HỌC

### 1.1. Đặt vấn đề và mục tiêu vừa sức

Trong thể thao điện tử Liên Minh Huyền Thoại, giai đoạn Cấm/Chọn (Draft Phase) và 10 phút đầu trận (Early Game / Snowball) đóng vai trò quan trọng trong việc định hình lối chơi. Tuy nhiên, khi phân tích dữ liệu LMHT thường gặp ba vấn đề thực tế:

1. **Dữ liệu nhiễu và trôi dạt meta (Concept Drift):** Các bản vá cập nhật liên tục làm thay đổi sức mạnh tướng; gộp dữ liệu quá cũ hoặc lẫn lộn giữa Đấu Giải (Pro Play) và Xếp Hạng Đơn (Solo Queue) dễ dẫn đến kết luận sai lệch.
2. **Đánh đồng thống kê mô tả với quan hệ nhân quả:** Tỷ lệ thắng của một cặp tướng với cỡ mẫu nhỏ ($n < 5$) thường bị diễn giải nhầm thành "khắc chế cứng" hoặc "đảm bảo thắng".
3. **Nhu cầu hỗ trợ ra quyết định có giải thích:** Người dùng cần biết lý do đằng sau một gợi ý cấm/chọn (số trận quan sát, khoảng tin cậy, chênh lệch vàng/kinh nghiệm/CS ở phút 10–15) thay vì một điểm số hộp đen.

Theo định hướng phạm vi vừa sức của học phần ([PHAM_VI_DO_AN_VUA_SUC.md](../../docs/PHAM_VI_DO_AN_VUA_SUC.md)), đồ án tập trung vào **một luồng dữ liệu và demo rõ ràng**:
- Xây dựng pipeline làm sạch, chuẩn hóa CSDL 1NF/3NF, truy vấn SQL/Pandas, trực quan hóa EDA và kiểm định giả thuyết đối chiếu Pro Play vs Solo Queue.
- Huấn luyện và đánh giá trung thực hai mô hình học máy 2 giai đoạn (`Draft` phút 0 và `Snowball` phút 10).
- Minh chứng thuật toán **Content-Based Filtering** bám sát Chương 6, đồng thời vận dụng làm nền cho hệ thống gợi ý Ban/Pick (duy trì hai chế độ `legacy` và `contextual`, thể thức Fearless Draft, giao diện Web local).
- **Ngoài phạm vi bắt buộc:** Không xây dựng cây tìm kiếm phản ứng (`lookahead` đã gỡ khỏi runtime/CLI), không tuyên bố tối ưu toàn cục chuỗi BO5 và không xây dựng hệ thống sản xuất quy mô lớn.

### 1.2. Phân định Kiến thức Môn học (MH) và Phần Mở rộng (MR / NV)

Để bảo đảm tính trung thực học thuật, báo cáo áp dụng quy ước 4 nhãn thống nhất từ [sổ kiến thức báo cáo](../../docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md):
- **MH (Môn học):** Khái niệm, thuật toán được giảng dạy trong bộ slide Chương 1–6 của môn *Nhập môn Khoa học Dữ liệu*.
- **UD (Vận dụng):** Lựa chọn bài toán, đặc trưng và thiết kế thực nghiệm khi áp dụng kiến thức môn học vào dữ liệu LMHT.
- **MR (Mở rộng):** Công thức, kỹ thuật thống kê/ML hoặc chính sách xếp hạng vượt ra ngoài nội dung cụ thể trong slide; phải nêu rõ nguồn hoặc ghi rõ là chính sách tự thiết kế.
- **NV (Nghiệp vụ / Kỹ thuật):** Luật thi đấu LMHT, Fearless Draft, CLI, API, giao diện Web và kiểm thử tự động.

| Phân loại | ID | Nội dung cốt lõi | Nơi triển khai trong mã nguồn | Ghi chú ranh giới |
|---|---|---|---|---|
| **MH + UD** | MH-01..03 | Vector, ma trận, xác suất có điều kiện, thống kê mô tả, kiểm định giả thuyết (Chương 1) | `content_based.py`, `draft_meta.py`, `src/04_hypothesis_testing/` | Kiểm định cụ thể ($Z$, $t$, hiệu chỉnh Holm) là vận dụng; quan sát không chứng minh nhân quả. |
| **MH + UD** | MH-04..05 | Thu thập, làm sạch dữ liệu, xử lý thiếu/ngoại lai, chuẩn hóa Min-Max (Chương 2) | `analysis_data.py`, `cleaner.py`, `content_based.py` | Giữ dấu âm chênh lệch, giữ `missing`, không fit min/max trên tập kiểm tra. |
| **MH + UD** | MH-06 | Trực quan hóa: heatmap, histogram/KDE, boxplot, scatter, grouped bar (Chương 3) | `plot_eda_figures.py`, `notebooks/01_kham_pha_du_lieu_EDA.ipynb` | 5 biểu đồ EDA 300 DPI (`fig1`–`fig5`). |
| **MH + UD** | MH-07..09 | Holdout/CV, cây quyết định, boosting, PCA/K-Means (Chương 4) | `validation.py`, `draft_model.py`, `snowball_model.py`, `cluster_archetypes.py` | **XGBoost CUDA** là phần mở rộng (`MR-07`) dựa trên nền boosting; K-Means/PCA là artifact phụ dùng metadata chuyên gia. |
| **MH + UD** | MH-10..11 | CSDL quan hệ 1NF/3NF, SQL tổng hợp/Window Functions, Pandas groupby/merge (Chương 5 & 5x) | `load_esports_to_db.py`, `queries.sql`, `execute_queries.py`, `analysis_data.py` | Tối ưu 14 indexes là kỹ thuật triển khai. |
| **MH + UD** | MH-12..14 | Content-Based Filtering: item profile, user profile, cosine similarity, Precision@10 (Chương 6) | `content_based.py`, `evaluate_content_based.py`, `notebooks/02_content_based_recommender.ipynb` | Chưa hiện thực Collaborative Filtering đầy đủ; không nhận nhầm co-pick thành CF. |
| **MR** | MR-01..10 | Time-decay snapshot, Wilson CI95%, shrinkage & geometric co-pick lift, suy role flex, calibration, bootstrap CI | `draft_meta.py`, `draft_advisor.py`, `validation.py`, `historical_recommender.py` | Các chính sách/công thức mở rộng được công khai tham số, chưa tối ưu toàn cục. |
| **MR** | MR-12, MR-13, MR-22..24 | Kiểm kèo đã lộ (`lane_review`), Ban contextual v2 (fixed-capacity pool), bảng bằng chứng Pro/Rank riêng, đối chiếu `simple`, giữ cặp bot (`pair_reservation`) | `ban_planner.py`, `draft_safety.py`, `pair_reservation.py`, `matchup_evidence.py` | Policy tự thiết kế phục vụ bài toán thực tế, không gán vào nội dung slide Chương 6. |
| **NV** | NV-01..24 | Máy trạng thái 20 lượt, Fearless BO5, First Selection, CLI, FastAPI adapter & React/TS Web UI | `simulate_draft_match.py`, `simulate_fearless_series.py`, `src/api/app.py`, `web/` | Phục vụ demo và kiểm soát tính hợp lệ, không phải thuật toán ML mới. |

---

## CHƯƠNG 2. THU THẬP, LÀM SẠCH & CƠ SỞ DỮ LIỆU (CHƯƠNG 2, 5 & 5x)

### 2.1. Nguồn dữ liệu và quy mô

Hệ thống vận hành trên hai luồng dữ liệu độc lập, không gộp lẫn số liệu giữa Đấu Giải và Solo Queue:

1. **Dữ liệu Đấu Giải chuyên nghiệp (Pro Play — Oracle's Elixir):**
   - Đồng bộ tự động từ kho Google Drive qua `src/01_data_pipeline/sync_google_drive.py` và nạp vào SQLite qua `load_esports_to_db.py`.
   - Quy mô trong CSDL chính (`data/database/lol_live_data.db`): **3,000 trận đấu độc lập** thuộc 6 giải đấu hàng đầu (`LCK`, `LPL`, `LCP`, `WLDS`, `MSI`, `EWC`), tương ứng **6,000 dòng** cấp đội (`tournament_matches`) và **30,000 dòng** cấp tuyển thủ (`tournament_players`).
   - Tỷ lệ trận có đủ chỉ số timeline mốc phút 10 là **79.0%** (2,369 / 3,000 trận); ở cấp cá nhân, mỗi phép đo chênh lệch phút 10 (`golddiffat10`, `xpdiffat10`, `csdiffat10`) có **24,370** quan sát hợp lệ và phút 15 có **24,380** quan sát hợp lệ.

2. **Dữ liệu Xếp Hạng Đơn (Solo Queue — Riot Games API):**
   - Nhánh phân tích mốc 10 phút (`crawl_riot_matches.py`): **1,009 trận đấu** lưu tại bảng `matches_10min` (**550 trận VN2** — 54.5% và **459 trận KR** — 45.5%), đầy đủ 42 cột kinh tế/mục tiêu phút 10 và 10 vị trí tướng.
   - Nhánh kho bằng chứng đối đầu tăng dần (`update_rank_evidence.py`, `rank_lake.py`): lưu tách biệt tại `data/database/ranked_evidence.db` (không ghi đè CSDL chính). Tại mốc chốt 24/11/2026 ([summary.json](../rank_matchups_live/summary.json)), kho đã thu nhận **975 trận hoàn chỉnh** (9,750 dòng quan sát trên 3 máy chủ KR/EUW/NA, 5,236 cặp đối đầu gộp, trong đó 148 cặp đạt $n \ge 5$). Đây là cohort *snapshot gần trận* (cả 10 người đạt Master+ tại thời điểm chụp trong vòng 24 giờ sau trận, `historical_rank_verified: false`), chỉ dùng làm bảng tham khảo phụ, không cộng vào điểm Pro.

### 2.2. Thiết kế CSDL chuẩn hóa 1NF/3NF và truy vấn SQL (Chương 5 & 5x)

CSDL chính `data/database/lol_live_data.db` (tổng **37,009 dòng**) được chuẩn hóa theo chuẩn 1NF và 3NF:
- **Chuẩn 1NF (Tính nguyên tử):** Trong `matches_10min`, thay vì lưu chuỗi gộp 5 tướng, hệ thống tách thành 10 cột nguyên tử (`blueTop`..`blueSupport`, `redTop`..`redSupport`). Ở dữ liệu giải, mỗi tuyển thủ là 1 dòng nguyên tử trong `tournament_players`.
- **Chuẩn 3NF (Khử phụ thuộc hàm bắc cầu):** Loại bỏ cột `country` khỏi `matches_10min` do phụ thuộc trực tiếp vào `server`; tách rạch ròi thông số cấp đội (`tournament_matches`, khóa chính `(gameid, side)`, 155 cột) và cấp tuyển thủ (`tournament_players`, khóa chính `(gameid, participantid)`, khóa ngoại tham chiếu `tournament_matches`, 129 cột).
- **Tối ưu truy vấn:** Thiết lập **14 indexes**, nổi bật là hai composite indexes `idx_tp_game_pos_side` và `idx_tp_game_side_pos` phục vụ Self-JOIN và Intra-team JOIN.

Năm truy vấn SQL nâng cao trong `src/03_database_sql/queries.sql` (xuất 5 tệp `data/processed/sql_query_1_result.csv` .. `sql_query_5_result.csv`) vận dụng trực tiếp Chương 5 & 5x:
- **Q1 (`Self-JOIN`, `GROUP BY`, `HAVING`):** Thống kê kèo đối đầu 1v1 cùng đường (tỷ lệ thắng, chênh lệch vàng và CS phút 10).
- **Q2 (`Intra-team JOIN`, `HAVING COUNT(*) >= 10`):** Thống kê các cặp đôi Đường Dưới (Bot + Sup) phối hợp nhiều nhất.
- **Q3 (`CTE`, `UNION ALL`, `FULL JOIN`):** Xếp hạng Top 20 tướng có tỷ lệ Cấm/Chọn (Presence Rate) cao nhất.
- **Q4 (`Window Functions: DENSE_RANK()`, `AVG() OVER()`):** Xếp hạng Top 3 tuyển thủ đè đường phút 10 theo từng vị trí so với trung bình toàn giải.
- **Q5 (`UNION ALL`, `CASE WHEN`):** Đối chiếu hiệu quả lăn cầu tuyết giữa Pro Play và Solo Rank theo 5 phân tầng chênh lệch vàng phút 10.

### 2.3. Chính sách làm sạch chung (Integrity v2 — Chương 2)

Toàn bộ các bước EDA, kiểm định, ML và Recommender dùng chung tầng làm sạch tại `src/analysis_data.py` (chính sách `domain-v2-signed-no-trimming`) để tránh rò rỉ hoặc sai lệch giữa các module:
- **Bảo toàn dấu âm của chênh lệch tài nguyên:** Xác minh thực tế trên `matches_10min` có **525/1,009 trận** mang giá trị `blueGoldDiff < 0` và **0 dòng** sai lệch dấu sau làm sạch ([integrity_summary.json](../integrity_summary.json)). Tuyệt đối không lấy trị tuyệt đối hoặc cắt bỏ đuôi phân phối trước khi chia tập huấn luyện/kiểm tra.
- **Không giả lập dữ liệu thiếu:** Các giá trị thiếu (`missing`) giữ nguyên `NaN`/`null`, không điền `0` cho chênh lệch vàng/XP/CS hay giả định mục tiêu phút 10 của Pro khi thiếu dữ liệu timeline.
- **Chuẩn hóa danh mục tướng chính thức:** Ánh xạ theo Data Dragon phiên bản `16.20.1` (`rank_data_contract.py`), xử lý đúng 18 tên nội bộ khác tên hiển thị mà không dùng fuzzy matching cảm tính.

---

## CHƯƠNG 3. KHÁM PHÁ DỮ LIỆU (EDA) & KIỂM ĐỊNH THỐNG KÊ (CHƯƠNG 1 & 3)

### 3.1. Trực quan hóa dữ liệu khám phá (Chương 3)

Bộ 5 biểu đồ EDA độ phân giải 300 DPI được sinh bởi `src/05_visualization/plot_eda_figures.py` và minh họa trong [notebook 01](../../notebooks/01_kham_pha_du_lieu_EDA.ipynb) (xem mục lục hình tại [reports/figures/README.md](../figures/README.md)):

1. **Hình 1 (`fig1_correlation_heatmap.png`):** Ma trận tương quan Pearson (9×9) giữa các chỉ số phút 10 (chênh lệch vàng, kinh nghiệm, hạ gục, trụ, rồng, sâu) và kết quả thắng trận.
2. **Hình 2 (`fig2_gold_diff_distribution_kde.png`):** Biểu đồ Histogram kết hợp mật độ KDE của chênh lệch vàng phút 10 theo kết quả Thắng/Thua, so sánh trực diện giữa Pro Play và Solo Rank.
3. **Hình 3 (`fig3_lane_economy_boxplot.png`):** Boxplot chênh lệch vàng phút 10 của 5 vị trí (`Top`, `Jng`, `Mid`, `Bot`, `Sup`) cho thấy độ phân tán và các giá trị ngoại lai lớn nhất tập trung ở các đường chủ lực.
4. **Hình 4 (`fig4_gold_lead_vs_duration_scatter.png`):** Scatter plot kèm đường hồi quy tuyến tính OLS giữa mức dẫn vàng phút 10 và tổng thời lượng trận đấu, làm rõ xu hướng kết thúc trận sớm hơn ở Solo Rank.
5. **Hình 5 (`fig5_neutral_objectives_scenarios_bar.png`):** Biểu đồ cột nhóm 8 tổ hợp mục tiêu lớn trước phút 10 (Rồng Nguyên Tố × số Sâu Hư Không).

### 3.2. Kiểm định Giả thuyết 1 — Lợi thế Phe Xanh ($Z$-test, hiệu chỉnh Holm)

Nguồn số liệu: `data/processed/hypothesis_test_1_blue_side.csv` (`src/04_hypothesis_testing/test_blue_side_advantage.py`). Giả thuyết không $H_0: p_{\text{Blue}} = 0.5$ ở mức ý nghĩa $\alpha = 0.05$:

| Tập dữ liệu | Số trận ($n$) | Thắng Xanh | Tỷ lệ thắng Xanh | $Z$-score | $p$-value | $p_{\text{Holm}}$ | Khoảng tin cậy 95% | Kết luận (sau Holm) |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **Toàn bộ Pro Play** | 3,000 | 1,615 | **53.83%** | +4.20 | 0.000027 | **0.00027** | [52.05%, 55.62%] | Bác bỏ $H_0$ (Xanh cao hơn) |
| **Toàn bộ Solo Rank (VN2 & KR)** | 1,009 | 459 | **45.49%** | -2.86 | 0.00417 | **0.03755** | [42.42%, 48.56%] | Bác bỏ $H_0$ (Xanh thấp hơn) |
| — Solo Rank VN2 | 550 | 259 | 47.09% | -1.36 | 0.1724 | 0.5210 | [42.92%, 51.26%] | Chưa đủ bằng chứng bác bỏ $H_0$ |
| — Solo Rank KR | 459 | 200 | 43.57% | -2.75 | 0.00589 | **0.04683** | [39.04%, 48.11%] | Bác bỏ $H_0$ (Xanh thấp hơn) |
| — Giải LCP | 474 | 267 | 56.33% | +2.76 | 0.00585 | **0.04683** | [51.86%, 60.79%] | Bác bỏ $H_0$ (Xanh cao hơn) |
| — Giải LCK | 812 | 434 | 53.45% | +1.97 | 0.04939 | 0.2469 | [50.02%, 56.88%] | Không còn ý nghĩa sau hiệu chỉnh Holm |
| — Giải LPL | 1,092 | 571 | 52.29% | +1.51 | 0.1303 | 0.5210 | [49.33%, 55.25%] | Chưa đủ bằng chứng bác bỏ $H_0$ |
| — Giải MSI / EWC / WLDS | 151 / 265 / 206 | 89 / 143 / 111 | 58.9% / 54.0% / 53.9% | +2.20 / +1.29 / +1.11 | 0.028 / 0.197 / 0.265 | $\ge 0.168$ | — | Chưa đủ bằng chứng sau Holm |

**Diễn giải đúng mực:** Kết quả cho thấy sự tương phản rõ rệt giữa Pro Play (Phe Xanh thắng 53.83%) và mẫu Solo Rank thu thập được (Phe Xanh thắng 45.49%, chủ yếu do mẫu KR). Tuy nhiên, đây là **liên hệ quan sát (observational association)**: trong đấu giải, đội mạnh hơn hoặc đội thua ván trước thường được quyền chọn phe, và các đội/tuyển thủ xuất hiện lặp lại nhiều lần nên không thỏa mãn tuyệt đối giả định độc lập hoàn toàn.

### 3.3. Kiểm định Giả thuyết 2 — Lăn cầu tuyết (Pro Play vs Solo Rank)

Nguồn số liệu: `data/processed/hypothesis_test_2_snowball.csv` (`test_snowball_effect.py`). So sánh tỷ lệ thắng ($Z$-test) và thời lượng kết thúc trận trung bình (Two-sample $t$-test) khi một đội dẫn vàng tại phút 10:

| Ngưỡng dẫn vàng phút 10 | Pro ($n$) | WR Pro | Thời lượng Pro | Rank ($n$) | WR Rank | Thời lượng Rank | Chênh thời lượng | $t$-stat ($p$-value) | WR $p$-value |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\ge +1{,}000\text{g}$ | 951 | 77.08% | 31.5 phút | 657 | 80.37% | 25.0 phút | **+6.6 phút** | 21.45 ($1.2 \times 10^{-86}$) | 0.115 |
| $\ge +1{,}500\text{g}$ | 507 | 81.85% | 30.8 phút | 517 | 84.53% | 24.5 phút | **+6.2 phút** | 16.60 ($1.1 \times 10^{-54}$) | 0.253 |
| $\ge +2{,}000\text{g}$ | 238 | 84.03% | 29.7 phút | 394 | 86.04% | 24.5 phút | **+5.2 phút** | 11.45 ($1.1 \times 10^{-27}$) | 0.490 |
| $\ge +3{,}000\text{g}$ | 53 | 92.45% | 28.8 phút | 208 | 89.90% | 23.1 phút | **+5.7 phút** | 7.81 ($1.0 \times 10^{-12}$) | 0.574 |

**Nhận xét:** Ở cả 4 ngưỡng dẫn vàng, tỷ lệ chuyển hóa thành chiến thắng giữa Pro và Rank **không khác biệt có ý nghĩa thống kê** ($p > 0.11$), nhưng các trận Solo Rank kết thúc nhanh hơn trung bình **5.2 đến 6.6 phút** với ý nghĩa thống kê rất mạnh ($p < 10^{-12}$), phản ánh tính kỷ luật phòng thủ cao hơn ở đấu giải chuyên nghiệp và cơ chế đầu hàng sớm (FF15/FF20) trong xếp hạng đơn.

### 3.4. Kiểm định Giả thuyết 3 — Tổ hợp mục tiêu lớn trước phút 10 (Solo Rank)

Nguồn số liệu: `data/processed/hypothesis_test_3_objectives.csv` (`test_voidgrubs_vs_dragon.py`, thực hiện trên 1,009 trận Solo Rank có đủ timeline mục tiêu phút 10; dữ liệu Pro chưa có mốc thời gian ăn mục tiêu phút 10 nên ghi nhận `unavailable`):

| Kịch bản trước phút 10 | Số trận ($n$) | Số trận thắng | Tỷ lệ thắng | Wilson CI 95% |
|---|---:|---:|---:|---|
| Không có Rồng & $< 3$ Sâu | 463 | 151 | **32.61%** | [28.50%, 37.01%] |
| Không có Rồng & $\ge 3$ Sâu | 285 | 146 | **51.23%** | [45.45%, 56.98%] |
| Có Rồng & $< 3$ Sâu | 168 | 92 | **54.76%** | [47.21%, 62.10%] |
| **Có cả Rồng & $\ge 3$ Sâu** | 93 | 70 | **75.27%** | [65.62%, 82.92%] |

**Lưu ý diễn giải:** Kịch bản ăn đồng thời cả hai mục tiêu gắn với tỷ lệ thắng 75.27%, nhưng đây là thống kê lịch sử (`historical_team_result`), không phải tác động nhân quả thuần túy vì đội kiểm soát được cả hai mục tiêu thường đã có lợi thế đi đường từ trước.

---

## CHƯƠNG 4. HỌC MÁY DỰ ĐOÁN KẾT QUẢ 2 GIAI ĐOẠN (CHƯƠNG 4 & MR-07..09)

### 4.1. Thiết kế thực nghiệm chống rò rỉ dữ liệu

Nhóm xây dựng 2 bài toán phân loại nhị phân (`draft_model.py` cho phút 0 từ đội hình 10 tướng + ngữ cảnh giải đấu; `snowball_model.py` cho phút 10 từ chênh lệch tài nguyên và mục tiêu) dưới điều phối chung của `src/06_machine_learning/validation.py`:
- **Phân chia tập chống leakage (`MR-08`):** Dữ liệu Pro chia theo thứ tự thời gian sự kiện (chronological split); dữ liệu Rank chưa có event timestamp trong bảng cũ nên dùng *grouped random split* theo `gameId` (công khai rõ không phải kiểm thử tương lai). Mã hóa đặc trưng lịch sử dùng *expanding encoding* chỉ tính trên quá khứ.
- **Lựa chọn mô hình & huấn luyện GPU (`MH-08`, `MR-07`):** Trên nền tảng cây quyết định và boosting của Chương 4, luồng huấn luyện hiện hành chọn giữa hai cấu hình **XGBoost CUDA** (`device='cuda'`, `tree_method='hist'`) theo tiêu chí `validation log-loss`, kết hợp tập calibration riêng áp dụng kỹ thuật *shrink-to-training-prior* (`MR-09`). Tập Test được giữ nguyên hoàn toàn trong quá trình chọn mô hình.

### 4.2. Kết quả đánh giá trên tập Test độc lập

Số liệu trích nguyên văn từ [src/06_machine_learning/evaluation_report.md](../../src/06_machine_learning/evaluation_report.md) và các manifest `.evaluation.json` (khoảng tin cậy 95% ước lượng qua 300 lần bootstrap theo trận):

| Mô hình (XGBoost CUDA depth=2) | Tập Test (dòng / trận) | Accuracy (CI 95%) | ROC-AUC (CI 95%) | Log-loss (CI 95%) | Brier Score | Baseline đối chứng |
|---|---:|---:|---:|---:|---:|---|
| **Draft Model** (Phút 0) | 600 / 600 | **0.5517** [0.5116, 0.5950] | **0.5628** [0.5148, 0.6081] | **0.6834** [0.6764, 0.6900] | 0.2452 | `training_prior`: Acc **0.5650**, AUC `0.5000`, Log-loss `0.6873`, Brier `0.2471` |
| **Snowball Model** (Phút 10) | 1,374 / 687 | **0.6718** [0.6321, 0.7082] | **0.7413** [0.7041, 0.7769] | **0.6004** [0.5671, 0.6321] | 0.2066 | `gold_sign_rule`: Acc `0.6536`, AUC `0.6536`, Log-loss `0.6683`, Brier `0.2357` |

*(Chi tiết theo nguồn ở Snowball Model: nguồn Pro đạt Acc `0.6615`, AUC `0.7297`, Log-loss `0.6106`; nguồn Rank đạt Acc `0.6965`, AUC `0.7730`, Log-loss `0.5758`. Biểu đồ ROC, Confusion Matrix, Calibration và Feature Importance lưu tại `reports/figures/fig6`–`fig9`.)*

### 4.3. Giải trình giới hạn của `draft_model` và phân cụm `archetype_kmeans`

1. **Vì sao `draft_model` có Accuracy (`0.5517`) thấp hơn baseline `training_prior` (`0.5650`)?**
   - **Độ nhiễu tự nhiên ở phút 0 rất lớn:** Chỉ biết danh sách 10 tướng và giải đấu không phản ánh được phong độ ngày thi đấu, trình độ chênh lệch giữa hai đội tuyển, kế hoạch di chuyển đầu trận hay sai sót trong giao tranh.
   - **Không gian đặc trưng thưa và thay đổi theo patch:** Với hơn 160 tướng chia cho 5 vị trí và 2 phe, số lượng tổ hợp đội hình vượt xa quy mô 3,000 trận; nhiều cặp tương tác mới xuất hiện ở tập test chưa từng gặp đủ nhiều ở tập train.
   - **Ý nghĩa của các chỉ số xác suất:** Dù Accuracy nhãn cứng (ngưỡng 0.5) thấp hơn baseline chọn luôn lớp đa số (Phe Xanh), `draft_model` vẫn có **ROC-AUC = 0.5628** (CI 95% nằm trên 0.50) và **Log-loss = 0.6834** (nhỏ hơn `0.6873` của prior), cho thấy mô hình học được một phần tín hiệu phân biệt yếu sau khi calibration (`alpha = 0.48`).
   - **Hệ quả thiết kế:** Nhóm **không sử dụng `draft_model` làm hàm mục tiêu để tối ưu hóa chuỗi BO5** và không tuyên bố xác suất đầu ra là tỷ lệ thắng thực tế của một đội hình.
2. **Về mô hình `snowball_model`:** Đạt hiệu năng khả quan hơn rõ rệt (AUC `0.7413`, vượt `gold_sign_rule` ở cả Accuracy, AUC, Log-loss và Brier), nhưng sử dụng thông tin phút 10 nên **tuyệt đối không đưa vào giai đoạn gợi ý cấm/chọn trước trận** để tránh rò rỉ dữ liệu tương lai.
3. **Về phân cụm PCA & K-Means (`cluster_archetypes.py`, `fig10`–`fig11`):** Dù PCA và K-Means là thuật toán thuộc Chương 2 & Chương 4 (`MH-09`), vector 5 trục sức mạnh và tên 4 trường phái đội hình trong artifact cũ (`models/archetype_kmeans.pkl`) dựa trên bảng thuộc tính chuyên gia (`MR-11`) và chưa được tái nghiệm thu theo chuẩn Integrity v2. Do đó, phần này chỉ được xếp vào phụ lục tham khảo, không tuyên bố là phân cụm chiến thuật học thuần túy từ dữ liệu.

---

## CHƯƠNG 5. HỆ THỐNG GỢI Ý (CHƯƠNG 6) & ỨNG DỤNG TRỢ LÝ BAN/PICK

### 5.1. Minh chứng bám sát Chương 6 — Content-Based Filtering

Module `src/07_recommender/content_based.py` (minh họa trực tiếp trong [notebook 02](../../notebooks/02_content_based_recommender.ipynb) và tài liệu [CHUONG_6_CONTENT_BASED.md](../../docs/CHUONG_6_CONTENT_BASED.md)) cài đặt đúng quy trình Content-Based Filtering trong slide Chương 6 (trang 11–20 và 47):
- **Item Profile (`MH-12`):** Mỗi item là một cặp `(champion, position)` được biểu diễn bằng vector trung bình của 5 đặc trưng hành vi thực đo trong lịch sử trước cutoff: sát thương mỗi phút (`DPM`), chỉ số lính mỗi phút (`CSPM`), cắm mắt mỗi phút (`WPM`), sát thương gánh chịu mỗi phút (`damage_taken_per_minute`) và tỷ trọng vàng kiếm được (`earned_gold_share`). Các đặc trưng được chuẩn hóa **Min-Max theo từng vị trí** (`MH-05`) chỉ trên tập dữ liệu lịch sử.
- **User Profile & Cosine Similarity (`MH-13`):** Hồ sơ của mỗi tuyển thủ là trung bình có trọng số các item vector theo số lần tuyển thủ đã chọn tướng đó (implicit preference); ứng viên được xếp hạng bằng **độ tương đồng Cosine** giữa user profile và item profile.
- **Đánh giá (`MH-14`):** Chạy `evaluate_content_based.py` trên dữ liệu cắt thời gian trước `2026-04-29T08:05:12Z` gồm **299 trận validation / 2,990 truy vấn**, tỷ lệ phủ hồ sơ tuyển thủ đạt **96.02%** ([content_based_evaluation.md](../content_based_evaluation.md)):

| Phương pháp (trên cùng tập ứng viên) | Precision@10 | Recall@10 | Recall@5 | MRR@5 |
|---|---:|---:|---:|---:|
| **Content-Based (Cosine)** | **0.0494** (CI 95%: [0.0479, 0.0513]) | 0.4936 | **0.2990** | 0.1390 |
| Baseline: `popularity` | 0.0749 | 0.7492 | 0.4652 | 0.2212 |
| Baseline: `player_frequency` | 0.0756 | 0.7559 | 0.4839 | 0.2403 |

### 5.2. Giải trình giới hạn của `content_based`

1. **Trần toán học của Precision@10 là `0.10`:** Vì mỗi lượt pick trong lịch sử chỉ có đúng **1 tướng thực sự được chọn** (1 nhãn liên quan trên 10 gợi ý), giá trị Precision@10 tối đa về mặt lý thuyết chỉ là $1/10 = 0.10$; mức `0.0494` tương đương xác suất tướng thật nằm trong Top 10 là **49.36%** (`Recall@10`).
2. **Tại sao `content_based` thấp hơn `popularity` và `player_frequency` về truy hồi?**
   - Trong môi trường giải đấu chuyên nghiệp, lựa chọn tướng bị chi phối rất mạnh bởi **meta bản vá** (nhóm tướng mạnh nhất được chọn đi chọn lại) và **bể tướng quen tay** của tuyển thủ — hai tín hiệu mà `popularity` và `player_frequency` khai thác trực tiếp.
   - Ngược lại, Content-Based thuần túy không dùng tần suất chọn hay tỷ lệ thắng, mà chỉ đo **sự giống nhau về phong cách chỉ số** (ví dụ: tìm một tướng Mid cấu rỉa/farm tương đồng với tướng tủ của tuyển thủ). Do đó, phương pháp này không mạnh nhất về truy hồi lựa chọn phổ biến, nhưng có giá trị thực tiễn cao khi cần gợi ý **tướng thay thế cùng lối chơi** trong các ván sau của Fearless Draft (khi các tướng phổ biến nhất đã bị khóa).
3. **Không nhận vơ Collaborative Filtering:** Slide Chương 6 có trình bày User-User / Item-Item Collaborative Filtering, nhưng dự án chọn tập trung hoàn chỉnh Content-Based. Thống kê đồng chọn (co-pick) ở phần mở rộng bên dưới không phải là cài đặt CF đầy đủ và được phân loại riêng là `MR`.

### 5.3. Phần mở rộng ứng dụng: Trợ lý Ban/Pick & Fearless BO5

Trên nền dữ liệu sạch, thống kê tần suất/xác suất (Chương 1, 5x) và điểm tương đồng Content-Based (Chương 6), nhóm tích hợp các cơ chế mở rộng có giải thích rõ ràng (`MR` / `NV`) vào `DraftAdvisor`, `BanPlanner` và giao diện Web cục bộ:

1. **Điểm xếp hạng Pick `current` vs phép thử tinh giản `simple` (`MR-01..06`, `MR-23`):**
   - Bộ xếp hạng `current` kết hợp: mức độ hiện diện theo cửa sổ thời gian có suy giảm hàm mũ `2^(-age/21)` (`MR-01`), thứ tự lượt chọn, lịch sử thắng có Wilson CI95% (`MR-02`), đối đầu theo phân phối role flex (`MR-04`), độ thành thạo tuyển thủ, điểm Cosine (`MH-13`) và hệ số phối hợp tất cả 10 cặp role (`MR-03`, dùng shrinkage và geometric lift điều chỉnh odds điểm nền).
   - Nhóm đã thử nghiệm công thức tinh giản `simple` chỉ gồm 3 tín hiệu (tần suất, cosine, WR đối đầu cùng role) trên cùng tập ứng viên và dữ liệu đóng băng WLDS 16.20 ([pick_scoring_comparison/REPORT.md](../pick_scoring_comparison/REPORT.md)):

| Tập dữ liệu (WLDS 16.20) | Công thức | Truy vấn | Recall@5 | MRR@5 | Coverage | Chênh Recall@5 (`simple - current`, CI 95%) |
|---|---|---:|---:|---:|---:|---|
| Validation (9 series) | `current` | 200 | **0.5150** | 0.2728 | 0.7650 | `-0.0900` [-0.1700, -0.0211] |
| Validation (9 series) | `simple` | 200 | 0.4250 | 0.2256 | 0.7650 | |
| Test (10 series) | `current` | 320 | **0.4938** | **0.3026** | 0.7688 | **`-0.0688`** [-0.1103, -0.0323] |
| Test (10 series) | `simple` | 320 | 0.4250 | 0.2334 | 0.7688 | |
| Test (10 series) | `recent_presence` | 320 | 0.4500 | 0.2554 | 0.7688 | |

   - Vì `simple` làm giảm Recall@5 đáng kể ở cả validation và test, hệ thống giữ mặc định `current` và chỉ cung cấp `--pick-scoring simple` như tùy chọn đối chiếu.

2. **Chiến lược Ban `legacy` vs `contextual` v2 (`MR-13` sửa, `NV-09`, `NV-22`):**
   - `legacy` ưu tiên cấm tướng có độ hiện diện cao và chênh lệch top 1 / top 2 của đối thủ.
   - `contextual` v2 (`BanPlanner`) ước lượng mức sụt giảm giá trị bể tướng của đối thủ trừ chi phí tự cấm chính mình (theo thứ tự pick thật, roster và các tướng đã khóa Fearless). Bản v2 dùng hàm giá trị pool cố định mẫu $k=3$: $V(\text{pool}) = \frac{1}{3}\sum_{i=1}^{3}\max(s_i, 0)$, loại bỏ hoàn toàn **31/31 trường hợp bất nhất** (mất tướng dự phòng nhưng điểm pool lại tăng) trên 80 trạng thái ban WLDS 16.20, giữ nguyên Recall@5 ban lịch sử (`0.675` val / `0.525` test).
   - Đối chiếu 5 ván Fearless T1–Gen.G ([COMPARISON.md](../legacy_contextual_comparison/COMPARISON.md)): cả hai hoàn thành 100 lượt hợp lệ và 50 tướng pick không lặp; `legacy` lặp lại cùng 1 tập 6 ban đầu qua cả 5 ván (Jaccard `1.000`), còn `contextual` thay đổi theo ngữ cảnh từng ván (5/5 tập khác nhau, Jaccard `0.471`). Sự khác biệt này thể hiện thay đổi hành vi theo ngữ cảnh, không tự chứng minh tăng tỷ lệ thắng.

3. **Các chốt an toàn bằng chứng (`MR-12` sửa, `MR-24`, `MR-22`):**
   - **Kiểm kèo đã lộ (`draft_safety.py`):** Ngay khi đối thủ cùng đường đã lộ, hệ thống kiểm tra trực tiếp số mẫu đối đầu (`n < 5` gắn cờ `requires_review`, chặn auto chốt ngầm khi chưa bật test override) và ưu tiên cận dưới khoảng tin cậy Wilson 95% trong cùng mức bằng chứng mà không đưa vàng phút 15 vào điểm gốc.
   - **Giữ cặp đường dưới (`pair_reservation.py`):** Đếm số lượt cấm của địch trước lượt pick tiếp theo của mình; nếu số đối tác bot/sup có bằng chứng đủ mẫu ($n \ge 5$, $\text{lift} \ge 1$) không vượt quá số ban địch sắp tới, ưu tiên bảo toàn đối tác sớm (`secure_now`).
   - **Bảng bằng chứng Pro / Rank tách riêng (`matchup_evidence.py`):** Hiển thị song song số trận, tỷ lệ thắng + Wilson CI95% và chênh lệch Vàng/XP/CS phút 10 & 15 kèm khoảng tin cậy $t$-95% từ hai nguồn Pro và Rank độc lập, không cộng điểm Rank vào Pro.

4. **Giao diện Web cục bộ & Kiểm thử (`NV-21`..`NV-24`):**
   - Đóng gói mỏng qua FastAPI (`src/api/app.py`) và React + TypeScript (`web/`), chạy bằng 1 lệnh `.\start_ui.ps1` tại `http://127.0.0.1:8000`.
   - Bố cục 3 cột responsive (Gợi ý | Đội hình 2 phe | Chọn tay), hỗ trợ chọn First Selection từng ván độc lập màu phe, tự xếp đường theo tần suất Pro quan sát được, kéo-thả đổi vị trí cùng đội, thu gọn khung giải thích (Inspector), lưu trạng thái phiên trên trình duyệt kèm mã `snapshot_id` chống trộn nguồn dữ liệu và xuất tệp JSON.
   - Kiểm chứng tự động đạt **178 unit tests Python PASS** (`reports/ui_lane_revision/`) và **7 kịch bản Edge E2E PASS** (`reports/ui_inspector_toggle/`, `reports/ui_inspector_collapse/`).

---

## CHƯƠNG 6. KẾT LUẬN, HẠN CHẾ & HƯỚNG PHÁT TRIỂN

### 6.1. Kết luận

Đồ án đã hoàn thành đầy đủ chuỗi quy trình Khoa học Dữ liệu của môn học từ thu thập, làm sạch, thiết kế CSDL chuẩn 1NF/3NF, truy vấn SQL/Pandas, kiểm định thống kê, trực quan hóa EDA, huấn luyện và đánh giá mô hình học máy hai giai đoạn đến xây dựng hệ thống gợi ý Content-Based Filtering (Chương 6) và mở rộng thành ứng dụng trợ lý Ban/Pick Fearless Draft có giải thích minh bạch.

> **Tóm lược phạm vi đạt được:** Đồ án vận dụng tiền xử lý, thống kê, SQL/Pandas, trực quan hóa, học máy và content-based recommendation; mở rộng bằng snapshot theo thời gian, thống kê phối hợp cặp tướng, chiến lược ban ngữ cảnh một bước, các chốt kiểm tra độ tin cậy mẫu đối đầu, bảng đối chiếu Pro/Rank tách biệt và giao diện Web cục bộ hỗ trợ quy trình Fearless Draft.

### 6.2. Các hạn chế cần lưu ý

1. **Chưa có tập kiểm thử độc lập hoàn toàn mới (Fresh Independent Final Test):** Các đánh giá so sánh `current` vs `simple`, `contextual` v2 và thăm dò chuyển miền Rank→Pro đều tái sử dụng dữ liệu Worlds 16.20 đã xem trong quá trình phân tích; tập prospective sau mốc freeze 24/11/2026 hiện có `0` series mới (`ready: false`).
2. **Truy hồi lựa chọn lịch sử khác với tối ưu chiến thuật:** Recall@5 và MRR@5 đo khả năng dự đoán lại tướng tuyển thủ đã chọn, không chứng minh tướng được gợi ý khắc chế về mặt cơ chế kỹ năng hay làm tăng tỷ lệ thắng thực tế.
3. **Cỡ mẫu đối đầu còn thưa:** Trong nhiều trạng thái draft cuối chuỗi Fearless, số cặp đối đầu trực tiếp hoặc cặp phối hợp đạt $n \ge 5$ còn ít, dẫn đến cảnh báo `review_required`.
4. **Hạn chế của nguồn dữ liệu Rank:** Kho `ranked_evidence.db` sử dụng snapshot bậc rank gần thời điểm trận đấu (không phải lịch sử bậc rank chính xác tại lúc trận bắt đầu) và chưa điều chỉnh thiên lệch chọn tướng hay trình độ cá nhân lặp lại.
5. **Chưa có bộ lập kế hoạch toàn chuỗi BO5:** Hệ thống hiện hành là gợi ý từng lượt (greedy một bước) có xét các tướng đã bị khóa ở các ván trước, chưa giải bài toán phân bổ tài nguyên tướng tối ưu xuyên suốt cả 5 ván.

### 6.3. Hướng phát triển (Dự kiến — ngoài phạm vi hiện hành)

Các hướng mở rộng đã được ghi nhận ở trạng thái **dự kiến** (`KH-01`..`KH-06` trong sổ kiến thức) để phát triển nếu tiếp tục nghiên cứu sau học phần:
- Thu thập dữ liệu giải đấu mùa giải mới sau mốc freeze để thực hiện đánh giá độc lập (prospective evaluation) cho cả bộ xếp hạng Pro và tín hiệu bổ trợ từ Rank cao.
- Xây dựng tầng đánh giá trạng thái đội hình (`KH-04`) được hiệu chỉnh xác suất tốt hơn trước khi cân nhắc kết hợp với mô hình dự đoán hành động đối thủ (`KH-01`, mới dừng ở bản prototype ban đầu) và lập kế hoạch giữ tướng xuyên chuỗi BO5 (`KH-03`).
- Phát triển chế độ gợi ý và giao diện riêng cho người chơi Solo Queue theo phân tầng bậc Rank và luật cấm/chọn riêng của xếp hạng đơn.

---

## TÀI LIỆU THAM KHẢO & PHỤ LỤC TÁI LẬP

### Tài liệu tham khảo chính
1. Bộ slide bài giảng *Nhập môn Khoa học Dữ liệu* (Chương 0 đến Chương 6, Chương 5x) — Học viện Công nghệ Bưu chính Viễn thông (`docs/course_slides/`).
2. Oracle's Elixir Match Data Dictionary — https://lol.timsevenhuysen.com/matchdata/match-data-dictionary/
3. Riot Games Developer Portal (Match-v5, League-v4, Data Dragon) — https://developer.riotgames.com/docs/lol
4. Riot Games LoL Esports — Fearless Draft Primer (2025) — https://lolesports.com/en-GB/news/fst-2025-primer
5. NIST Engineering Statistics Handbook — Confidence Limits for the Mean — https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm

### Lệnh tái lập các kết quả chính (PowerShell, chạy tại thư mục gốc `Project/`)

```powershell
# 1. Chạy toàn bộ bộ kiểm thử tự động (178 unit tests)
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# 2. Tái tạo benchmark Content-Based Filtering (Chương 6)
.\.venv\Scripts\python.exe src/07_recommender/evaluate_content_based.py

# 3. Tái tạo 5 câu truy vấn SQL (Chương 5 & 5x) và 5 biểu đồ EDA (Chương 3)
.\.venv\Scripts\python.exe src/03_database_sql/execute_queries.py --export
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py

# 4. Chạy mô phỏng 5 ván Fearless Draft qua CLI (chỉ định rõ First Selection từng ván)
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py `
  --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 `
  --games 5 --first-picks blue,blue,blue,blue,blue --ban-strategy contextual --allow-statistical-auto

# 5. Khởi chạy giao diện Web Draft Lab cục bộ (http://127.0.0.1:8000)
.\start_ui.ps1
```
