# PROJECT TASKS & ATOMIC CHECKLIST

Trạng thái:
- `[x] DONE`: Đã hoàn thành và xác minh bằng kiểm thử/dữ liệu thực tế.
- `[-] IN PROGRESS`: Đang trong quá trình thực hiện.
- `[ ] NOT STARTED`: Chưa bắt đầu.
- `[!] BLOCKED`: Bị chặn bởi phụ thuộc kỹ thuật.

---

## 🟢 GIAI ĐOẠN 1: THU THẬP, LÀM SẠCH & THIẾT KẾ CSDL (CHƯƠNG 2, 5)

- [x] **Task 1.0 [Cả nhóm]: Thiết lập môi trường ảo `.venv`, cấu hình tập trung `src/config` & Cấu trúc thư mục Pipeline chuẩn**
  - *Mục tiêu:* Khởi tạo `.venv` nội bộ tại thư mục gốc dự án (Python 3.13), cài đầy đủ `requirements.txt` (`pandas`, `scipy`, `scikit-learn`, `gdown`, `jupyter`, `google-api-python-client`...), cấu hình `.vscode/settings.json` tự động trỏ interpreter. Tạo package cấu hình chuẩn `src/config/` (`settings.py`, `__init__.py`), bảo vệ Riot API key, nạp `.env`. Khởi tạo đầy đủ cây thư mục từ `02` đến `07`, `notebooks/`, `reports/figures/` đi kèm file tài liệu `README.md` chuẩn hóa.
  - *Kết quả:* Đã hoàn tất, kích hoạt thành công qua `.\.venv\Scripts\Activate.ps1` và kiểm thử 100% trơn tru.

- [x] **Task 1.1 [Thành viên 1]: Cào dữ liệu Live Rank VN & KR từ Riot Games API**
  - *Mục tiêu:* Tích lũy tối thiểu 1,000 - 3,000 trận rank cao (VN2 & KR) đạt chuẩn 1NF/3NF vào `data/database/lol_live_data.db`.
  - *Kết quả:* Đã tích lũy thành công **1,009 trận** thực tế (550 trận VN2, 459 trận KR), xuất song song ra `data/processed/lol_live_ranked_10min.csv` (1,009 dòng $\times$ 42 cột).
  - *Acceptance Criteria:* Bảng `matches_10min` có $\ge 1,000$ trận, 0 giá trị NULL ở các cột kinh tế và 10 tướng, tỷ lệ VN2 (54.5%) và KR (45.5%) cân đối hoàn hảo. Đạt chuẩn 1NF (10 cột lane nguyên tử) và 3NF (khử cột phụ thuộc hàm). Hoàn thành 100%.

- [x] **Task 1.2 [Thành viên 1]: Nạp dữ liệu giải đấu chuyên nghiệp vào SQLite**
  - *Mục tiêu:* Viết script ETL đọc tệp dữ liệu hoạt động (`get_active_esports_file()` / `data/raw/esports_active_matches.csv`) nạp vào 2 bảng `tournament_matches` và `tournament_players` trong `lol_live_data.db`.
  - *Kết quả:* Đã hoàn thành module [`src/01_data_pipeline/load_esports_to_db.py`](../src/01_data_pipeline/load_esports_to_db.py). Nạp thành công **6,000 dòng** vào `tournament_matches` (3,000 trận $\times$ 2 đội) và **30,000 dòng** vào `tournament_players` (3,000 trận $\times$ 10 tuyển thủ).
  - *Acceptance Criteria:* CSDL có 2 bảng mới chuẩn hóa 1NF/3NF, có composite Primary Key `(gameid, side)` cho matches, `(gameid, participantid)` cho players, và Foreign Key `(gameid, side) REFERENCES tournament_matches(gameid, side)`. Tự động tạo 12 Indexes tối ưu hóa truy vấn SQL. Chạy kiểm thử xác thực 100% trơn tru. Hoàn thành 100%.

- [x] **Task 1.3 [Thành viên 1]: Viết module làm sạch dữ liệu & khử ngoại lai (IQR/Z-Score)**
  - *Mục tiêu:* Viết hàm trong `src/02_preprocessing/cleaner.py` lọc bỏ 100% trận Remake (< 10 phút), AFK (CS < 10), xử lý missing values theo 5 nhóm chuẩn và lọc/cắt ngọn outlier chênh lệch vàng bất thường bằng IQR & Z-score.
  - *Kết quả:* Đã hoàn thành module [`src/02_preprocessing/cleaner.py`](../src/02_preprocessing/cleaner.py) và package `src/02_preprocessing/`.
    - Lọc bỏ 100% trận Remake và AFK.
    - Xử lý triệt để Missing Values: Impute `0` cho biến đếm mục tiêu, `'NoBan'` cho lượt cấm rỗng, phân luồng `datacompleteness` cho bài toán mốc 10 phút.
    - Khử ngoại lai linh hoạt qua 2 thuật toán: IQR ($1.5 \times IQR$) và Z-Score ($|Z| > 3.0$), hỗ trợ cả 2 chế độ Trimming (Lọc bỏ) và Winsorization (Cắt ngọn/Capping).
    - Xuất thành công 4 tập dữ liệu sạch vào `data/processed/`: `clean_ranked_10min.csv`, `clean_tournament_10min.csv`, `clean_tournament_draft.csv`, `clean_tournament_players.csv`.
  - *Acceptance Criteria:* Có thống kê số lượng bản ghi trước và sau khi lọc, tỷ lệ giữ lại đạt $> 96\%$ ở chế độ đồng thuận, không làm mất tính toàn vẹn dữ liệu. Hoàn thành 100%.

- [x] **Task 1.4 [Thành viên 1 + 2]: Viết 5 câu truy vấn SQL nâng cao theo Chương 5 & 5x**
  - *Mục tiêu:* Viết 5 câu truy vấn SQL phân tích nâng cao theo chuẩn giáo trình Chương 5 & 5x (Databases, SQL & Pandas) trên CSDL SQLite `data/database/lol_live_data.db`.
  - *Kết quả:* Đã hoàn thành [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql), [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py) và tài liệu [`src/03_database_sql/README.md`](../src/03_database_sql/README.md).
    - **Truy vấn 1:** Kèo đối đầu 1v1 (`Self-JOIN`, `GROUP BY`, `HAVING`) đánh giá tỷ lệ thắng và chênh lệch vàng/lính lúc 10 phút.
    - **Truy vấn 2:** Cặp đôi ăn ý đường dưới Xạ thủ + Hỗ trợ (`Intra-team JOIN`, `HAVING COUNT(*) >= 10`).
    - **Truy vấn 3:** Tướng có tỷ lệ Cấm/Chọn cao nhất (`Subqueries / CTE`, `Unpivot UNION ALL`).
    - **Truy vấn 4:** Xếp hạng tuyển thủ đè đường phút 10 (`Window Functions: DENSE_RANK()`, `PARTITION BY`, `AVG() OVER()`).
    - **Truy vấn 5:** Đối chiếu hiệu quả Lăn cầu tuyết Đấu Giải vs Solo Rank (`UNION ALL`, `CASE WHEN`).
    - Hỗ trợ CLI đa năng: `--query 1..5`, `--limit`, `--export`, xuất tự động 5 file CSV kết quả vào `data/processed/sql_query_*.csv`.
  - *Acceptance Criteria:* 100% truy vấn thực thi chính xác trên SQLite, trả về bảng dữ liệu phân tích nghiệp vụ rõ ràng, hỗ trợ xuất CSV. Hoàn thành 100%.

- [x] **Task 1.5 [Thành viên 1]: Xây dựng Module Đồng Bộ Dữ Liệu Tự Động từ Google Drive (Cloud Data Auto-Sync)**
  - *Mục tiêu:* Xây dựng module tự động kết nối thư mục Google Drive (`1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`) lưu trữ toàn bộ mùa giải Oracle's Elixir (2014-2026).
  - *Kết quả:* Đã hoàn thành module [`src/01_data_pipeline/sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py).
    - Hỗ trợ kiểm tra danh mục siêu nhẹ (`--list`), tự động bỏ qua nếu file cục bộ đã khớp dung lượng, hỗ trợ tải từng năm (`--year`), tải toàn bộ (`--all`) và ép buộc tải mới (`--force`).
    - Nâng cấp thuật toán quyết định mùa giải thông minh (ADR-013): Tự động phát hiện năm mới nhất; nếu chưa đủ số trận (`min_matches`), tự động ghép toàn bộ năm mới + trích xuất phần cuối năm trước (CKTG / Mùa Hè) cho đến khi đủ số lượng.
    - Hỗ trợ bộ lọc giải đấu linh hoạt (`--leagues LCK,LCP,LPL,MSI,WLDS,EWC`): Tự động trích xuất đúng các giải đấu chỉ định kết hợp các giải quốc tế danh giá (Worlds, MSI, EWC), xuất tệp hoạt động `data/raw/esports_active_matches.csv` (26.8 MB, 36,000 dòng, đúng 3,000 trận đỉnh cao: 1,774 trận từ 2026 + 1,226 trận từ cuối 2025). Tỷ lệ có Timeline 10 phút tăng vọt lên **79.0% (2,369 / 3,000 trận)**.
    - Bổ sung hàm chuyên dụng `filter_leagues()` và `filter_esports_by_leagues()` cùng cờ CLI `--filter --filter-leagues`.
    - Bổ sung hàm kiểm tra sức khỏe và độ sạch dữ liệu `check_data_health()` / `check_esports_data_health()` cùng cờ CLI `--check` xuất Data Health Card trực quan.
    - Cơ chế chống Quota Exceeded 2 tầng: Tầng 1 (gdown trực tiếp), Tầng 2 (Google Drive API v3 + OAuth 2.0 Desktop App qua cơ chế Smart Copy vào My Drive rồi tự dọn dẹp file tạm). Đã kiểm thử live thành công 100%.
    - Phân tách tài liệu chi tiết thành 2 file chuyên biệt [`README_CRAWL_RIOT.md`](../src/01_data_pipeline/README_CRAWL_RIOT.md) và [`README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md). Hoàn thành 100%.

- [x] **Milestone 1:** Nghiệm thu toàn bộ CSDL SQLite `lol_live_data.db` hoàn chỉnh cả 2 nguồn dữ liệu, module tiền xử lý dữ liệu sạch, bộ truy vấn SQL phân tích nâng cao và cơ chế đồng bộ tự động.

---

## 🔵 GIAI ĐOẠN 2: THỐNG KÊ SUY DIỄN & TRỰC QUAN HÓA EDA (CHƯƠNG 1, 3)

- [x] **Task 2.1 [Thành viên 2]: Kiểm định A/B Lợi thế Phe Xanh (Blue Side Advantage) qua $Z$-test 2 phía**
  - *Mục tiêu:* Thực hiện $Z$-test tỷ lệ 2 phía ($\alpha = 0.05$) để kiểm định giả thuyết: $H_0: p_{blue} = 0.5$ vs $H_1: p_{blue} \neq 0.5$.
  - *Kết quả:* Đã hoàn thành module [`src/04_hypothesis_testing/test_blue_side_advantage.py`](../src/04_hypothesis_testing/test_blue_side_advantage.py) và package `src/04_hypothesis_testing/`.
    - **Đấu Giải (Pro Play - 3,000 trận):** Tỷ lệ thắng Phe Xanh đạt **53.50%** (1,605 thắng), $Z = +3.8341$, $p\text{-value} = 0.000126 < 0.001$, CI 95%: $[51.72\%, 55.28\%]$ $\rightarrow$ **Bác bỏ $H_0$** (Phe Xanh có lợi thế First Pick và góc nhìn camera vượt trội có ý nghĩa thống kê cao).
    - **Solo Rank (1,009 trận):** Tỷ lệ thắng Phe Xanh đạt **45.49%**, Phe Đỏ đạt **54.51%**, $Z = -2.8648$, $p\text{-value} = 0.004173 < 0.01$ $\rightarrow$ **Bác bỏ $H_0$** (Phe Đỏ thắng cao hơn do thuật toán Matchmaking xếp đội có MMR cao hơn sang Phe Đỏ).
    - **Từng giải đấu:** LCP ($p=0.0262^*$), MSI ($p=0.0280^*$) đều bác bỏ $H_0$.
    - Xuất tệp kết quả: `data/processed/hypothesis_test_1_blue_side.csv`.
  - *Acceptance Criteria:* Chạy lệnh CLI không lỗi, xuất đầy đủ $Z$-score, $p$-value, khoảng tin cậy 95%, bảng số liệu và phân tích nghiệp vụ. Hoàn thành 100%.

- [x] **Task 2.2 [Thành viên 2]: Kiểm định Two-sample Welch's $t$-test & $Z$-test về Hiệu quả Lăn Cầu Tuyết (Snowball Lead $\ge 2,000$g lúc 10 phút)**
  - *Mục tiêu:* So sánh khả năng chuyển hóa chiến thắng, thời lượng trận đấu và tính ổn định khi dẫn $\ge 2,000$ vàng lúc 10 phút giữa Đấu Giải Chuyên Nghiệp (Pro Play) và Đấu Solo Rank Thách Đấu.
  - *Kết quả:* Đã hoàn thành module [`src/04_hypothesis_testing/test_snowball_effect.py`](../src/04_hypothesis_testing/test_snowball_effect.py), tài liệu phân tích chi tiết [`src/04_hypothesis_testing/test_snowball_effect.md`](../src/04_hypothesis_testing/test_snowball_effect.md) và xuất tệp số liệu [`data/processed/hypothesis_test_2_snowball.csv`](../data/processed/hypothesis_test_2_snowball.csv).
    - **1. Tỷ lệ thắng (Two-sample Proportion Z-test):** Pro Play thắng **83.48%** (192/230), Solo Rank thắng **86.04%** (339/394). $Z = -0.8671, p = 0.3859 > 0.05 \rightarrow$ **Chưa đủ bằng chứng bác bỏ $H_0$** (Cả 2 môi trường đều chuyển hóa thành thắng lợi $\sim 85-86\%$, sự chênh lệch là ngẫu nhiên).
    - **2. Thời lượng trận đấu (Welch's $t$-test):** Pro Play = **29.75 phút** vs Solo Rank = **24.46 phút**. $t = +11.4618, p = 1.16 \times 10^{-27} < 0.0001 \rightarrow$ **Bác bỏ $H_0$ cực kỳ mạnh mẽ** (Trận Solo Rank kết thúc nhanh hơn trung bình **5.3 phút** do cơ chế đầu hàng sớm FF15 và lối đánh giao tranh liên tục).
    - **3. Tính ổn định & Kỷ luật (Levene's Variance Test):** Độ lệch chuẩn Pro Play $\sigma = 4.68$ phút vs Solo Rank $\sigma = 6.80$ phút. $\text{Levene Stat} = 53.1630, p = 9.37 \times 10^{-13} < 0.0001 \rightarrow$ **Bác bỏ $H_0$** (Đấu Giải có tính kỷ luật, kiểm soát chặt chẽ và ít bị đột biến quăng game hơn).
    - **Phân tầng đa mốc:** Mở rộng kiểm định trên 4 mốc ($\ge 1,000$g, $\ge 1,500$g, $\ge 2,000$g, $\ge 3,000$g).
  - *Acceptance Criteria:* Chạy lệnh CLI hoàn hảo, xuất đủ 3 bài toán thống kê theo Giáo trình Chương 1, có bảng phân tầng và phân tích nghiệp vụ sâu sắc. Hoàn thành 100%.

- [x] **Task 2.3 [Thành viên 2]: Kiểm định Chi-square (χ²) & Tỷ Số Chênh (Odds Ratio): 3 Sâu Hư Không đầu vs Rồng 1**
  - *Mục tiêu:* Đánh giá mối quan hệ độc lập giữa việc kiểm soát mục tiêu trung lập (3 Sâu Hư Không đợt 1 vs Rồng Nguyên Tố đầu) và kết quả trận đấu; định lượng mức độ gia tăng cơ hội chiến thắng qua Odds Ratio (OR) và ma trận 4 kịch bản đối đầu.
  - *Kết quả:* Đã hoàn thành module [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py), tài liệu phân tích chi tiết [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md) và xuất tệp số liệu [`data/processed/hypothesis_test_3_objectives.csv`](../data/processed/hypothesis_test_3_objectives.csv).
    - **1. Đấu Giải (Pro Play):**
      - **Rồng Đầu Tiên (First Dragon):** Winrate **59.43%** vs **40.57%**, $\chi^2 = 167.39, p = 2.75 \times 10^{-38} < 0.0001$, $\text{Odds Ratio} = \mathbf{2.145}$ (CI 95%: $[1.910, 2.409]$) $\rightarrow$ Tăng cơ hội thắng gấp **2.15 lần**.
      - **3 Sâu Hư Không (Voidgrubs):** Winrate **55.81%** vs **46.96%**, $\chi^2 = 33.11, p = 8.73 \times 10^{-9} < 0.0001$, $\text{Odds Ratio} = \mathbf{1.427}$ (CI 95%: $[1.265, 1.609]$) $\rightarrow$ Tăng cơ hội thắng gấp **1.43 lần**.
      - **Đổi chéo mục tiêu (Cross-trade):** Đội chỉ ăn Rồng 1 (bỏ Sâu) thắng **55.92%**, đội chỉ ăn Sâu (bỏ Rồng) chỉ thắng **47.23%** (Rơi xuống dưới 50%!).
    - **2. Solo Rank (Thách Đấu):**
      - **Rồng Đầu:** $\text{Odds Ratio} = \mathbf{2.306}$ ($p = 1.60 \times 10^{-18}$).
      - **3 Sâu Hư Không:** $\text{Odds Ratio} = \mathbf{2.031}$ ($p = 2.67 \times 10^{-13}$) $\rightarrow$ Ở Solo Rank, 3 Sâu có giá trị cao hơn hẳn Pro Play do người chơi tự đẩy trụ lấy tiền giáp trụ (Plates) lăn cầu tuyết cá nhân.
    - **3. Kịch bản Double Neutral Control:** Đội ăn cả 2 (3 Sâu + Rồng 1) thắng **68.66%** ở Pro và **76.28%** ở Rank. Đội mất trắng cả 2 chỉ còn **35.90%** (Pro) và **36.42%** (Rank).
  - *Acceptance Criteria:* Chạy lệnh CLI hoàn hảo, tính đủ Chi-square, Odds Ratio, Woolf CI 95%, Relative Risk và ma trận 4 kịch bản. Hoàn thành 100%.

- [x] **Task 2.4 [Thành viên 2]: Trực quan hóa dữ liệu EDA (Bộ 5 biểu đồ 300 DPI - Chương 3)**
  - *Mục tiêu:* Thiết kế và xuất bản bộ 5 biểu đồ EDA theo chuẩn đồ họa nghiên cứu khoa học (Publication-Ready, 300 DPI) phân tích các đặc trưng kinh tế, mục tiêu và nhịp độ trận đấu mốc 10 phút.
  - *Kết quả:* Đã hoàn thành module [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py), tài liệu phân tích chuyên sâu [`src/05_visualization/plot_eda_figures.md`](../src/05_visualization/plot_eda_figures.md) và xuất 5 tệp hình ảnh 300 DPI vào thư mục [`reports/figures/`](../reports/figures/):
    - **Fig 1:** [`fig1_correlation_heatmap.png`](../reports/figures/fig1_correlation_heatmap.png) - Ma trận tương quan Pearson Heatmap (Tam giác trên).
    - **Fig 2:** [`fig2_gold_diff_distribution_kde.png`](../reports/figures/fig2_gold_diff_distribution_kde.png) - Phân phối chênh lệch vàng (Histogram + KDE Thắng vs Thua).
    - **Fig 3:** [`fig3_lane_economy_boxplot.png`](../reports/figures/fig3_lane_economy_boxplot.png) - Phân bố kinh tế & ngoại lai 5 vị trí thi đấu (Boxplot 1.5 IQR).
    - **Fig 4:** [`fig4_gold_lead_vs_duration_scatter.png`](../reports/figures/fig4_gold_lead_vs_duration_scatter.png) - Vàng dẫn trước 10p vs Thời lượng kết thúc trận (Scatter + Hồi quy OLS + Mốc Baron 20p/FF15).
    - **Fig 5:** [`fig5_neutral_objectives_scenarios_bar.png`](../reports/figures/fig5_neutral_objectives_scenarios_bar.png) - Ma trận 8 tổ hợp mục tiêu lớn (Rồng 1 x 0, 1, 2, 3 Sâu) đối chiếu Đấu Giải vs Solo Rank.
  - *Tài liệu giải thích chuyên sâu:* Đã xây dựng trọn bộ 6 tệp tài liệu trong thư mục [`docs/figure_explain/`](../docs/figure_explain/) (đồng bộ tại `reports/figures/figure_explain/`).
  - *Acceptance Criteria:* Chạy lệnh CLI trơn tru (hỗ trợ cả `--all` và `--fig 1..5`), xuất file ảnh 300 DPI sắc nét, có chú thích học thuật rõ ràng, không lỗi font Tiếng Việt. Hoàn thành 100%.

- [ ] **Milestone 2:** Báo cáo Thống kê & EDA hoàn tất trong Notebook `01_kham_pha_du_lieu_EDA.ipynb`.

---

## 🟠 GIAI ĐOẠN 3: XÂY DỰNG MACHINE LEARNING 2 GIAI ĐOẠN & BAN/PICK AI (CHƯƠNG 4, 6)

- [ ] **Task 3.1 [Thành viên 3]:** Xây dựng Mô hình Draft Prediction lúc cấm chọn (Phút 0). Áp dụng Sliding Window + Sample Weighting.
- [ ] **Task 3.2 [Thành viên 3]:** Xây dựng Mô hình Snowball Prediction trong trận (Phút 10 - Random Forest / XGBoost). Kỳ vọng Accuracy > 80%.
- [ ] **Task 3.3 [Thành viên 3]:** Đánh giá mô hình: ROC-AUC Curve, Confusion Matrix, Feature Importance.
- [ ] **Task 3.4 [Thành viên 3]: Phân cụm K-Means & Nhận diện 4 Trường phái Đội hình (Draft Archetypes - Chương 4)**
  - *Mục tiêu:* Vector hóa 159 tướng theo 5 trục sức mạnh `[Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control]`. Dùng K-Means + PCA gom cụm nhận diện 4 trường phái đội hình: Early Snowball / Dive, Dragon Soul Stacking, Late-Game Hypercarry, Pick & Split-Push 1-3-1.
- [ ] **Task 3.5 [Thành viên 3 + 1]: Hệ thống Gợi ý Cấm/Chọn (Counter Pick & Synergy Apriori) & Engine Phân tích Điều kiện thắng (Win Condition Card - ADR-014)**
  - *Mục tiêu:* Xây dựng Recommender gợi ý Counter-Pick và Synergy Duo; tự động xuất Thẻ Điều kiện thắng (Win Condition Card) chỉ rõ: Chủ lực gánh đội (Core Carry), Điểm rơi sức mạnh (Power Spike Timing), Mục tiêu ưu tiên số 1 (Primary Objective), và Điều kiện thất bại cần tránh (Lose Condition).
- [ ] **Milestone 3:** Xuất các file mô hình `draft_model.pkl`, `snowball_model.pkl`, `archetype_kmeans.pkl`, `recommender.pkl`.

---

## 🟣 GIAI ĐOẠN 4: ĐÓNG GÓI REST API (FASTAPI) & DỰNG WEB APP (GIAI ĐOẠN 1 MÔN KH DỮ LIỆU)

- [ ] **Task 4.1 [Thành viên 1]:** Xây dựng Backend REST API bằng **FastAPI** (`src/api/`):
  - `POST /api/v1/predict`: Dự đoán tỉ lệ thắng 2 giai đoạn (Phút 0 & Phút 10).
  - `GET /api/v1/champions`: Danh sách 173 tướng + Vector thuộc tính.
  - `POST /api/v1/recommend`: Gợi ý cấm/chọn tối ưu (Counter & Synergy).
  - `POST /api/v1/win-condition`: Trích xuất Radar Chart 5 trục & Thẻ điều kiện thắng của đội hình (ADR-014).
  - `GET /api/v1/analytics`: Số liệu thống kê Meta giải đấu & Rank.
- [ ] **Task 4.2 [Thành viên 1 + 3]:** Xây dựng Giao diện Web App tương tác (`web/` hoặc Streamlit) tích hợp Radar Chart 5 trục và Thẻ chiến thuật Win Condition trực quan.
- [ ] **Milestone 4:** Demo hoàn chỉnh Web App kết nối API nộp môn Nhập môn Khoa học Dữ liệu.

---

## 🔴 GIAI ĐOẠN 5: MOBILE APP ANDROID & BÁO CÁO TỔNG KẾT

- [ ] **Task 5.1 [Thành viên 1]:** Phát triển ứng dụng Android (Java/Kotlin, RecyclerView, Retrofit) gọi API FastAPI (Môn Di động).
- [ ] **Task 5.2 [Cả nhóm]:** Viết báo cáo tổng kết Word/PDF.
- [ ] **Task 5.3 [Cả nhóm]:** Thiết kế Slide thuyết trình PowerPoint.
- [ ] **Task 5.4 [Cả nhóm]:** Tổng duyệt demo và bảo vệ đồ án trước hội đồng.
- [ ] **Milestone 5:** Đạt điểm số tối đa cả 2 môn học.
