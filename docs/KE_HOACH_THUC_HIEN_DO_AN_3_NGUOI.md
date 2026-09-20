# KẾ HOẠCH & CHECKLIST THỰC HIỆN ĐỒ ÁN TOÀN DIỆN (NHÓM 3 NGƯỜI)
**Chiến lược kép:** Hoàn thành xuất sắc môn **Nhập môn Khoa học Dữ liệu** & Tái sử dụng trọn vẹn cho môn **Lập trình Thiết bị Di động**  
**Học viện:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Giảng viên Data Science:** TS. Thái Tuyết Hải  
**Đề tài chính thức:** **Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) trong Esports Liên Minh Huyền Thoại**  

---

## 🏛️ KIẾN TRÚC TỔNG THỂ DÙNG CHUNG CHO CẢ 2 MÔN HỌC

```
                      [ 🧠 DATA SCIENCE & BACKEND ENGINE ]
                     (Phục vụ môn Nhập môn Khoa học Dữ liệu)
                                        │
           ├── CSDL SQLite chuẩn 1NF & 3NF (lol_live_data.db)
           ├── Pipeline làm sạch, khử ngoại lai & EDA đa chiều
           ├── Mô hình Machine Learning 2 giai đoạn (Draft & Snowball)
           └── Thuật toán Gợi ý Cấm/Chọn Recommender (Chương 6)
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
 [ 📊 GIAO DIỆN WEB STREAMLIT ]                        [ 📱 GIAO DIỆN MOBILE APP ]
   (Phục vụ Báo cáo & Demo trước hội đồng)             (Phục vụ nộp môn Lập trình Di động)
   - Chiếu slide & Demo trực tiếp máy chiếu            - Ứng dụng Android/Flutter chạy điện thoại
   - Biểu đồ Seaborn/Plotly tương tác cao              - Giao diện tra cứu 173 tướng từ Riot CDN
   - Bảng truy vấn SQL & Kiểm định A/B                 - Phòng Ban/Pick Live & Dự đoán tỷ lệ thắng
```

---

## 👥 PHÂN CHIA VAI TRÒ TRONG NHÓM (TEAM ROLES)

| Thành viên | Vị trí phân công | Trọng tâm phụ trách chính | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **Thành viên 1** *(Trưởng nhóm)* | **Data Engineer & Backend Lead** | Pipeline cào dữ liệu Riot API, chuẩn hóa CSDL 1NF/3NF, thiết kế REST API (FastAPI) & Mobile Client. | `lol_live_data.db`, `crawl_riot_matches.py`, `api_service.py`, Mobile App. |
| **Thành viên 2** | **Data Analyst & Statistician** | Thống kê suy diễn, kiểm định giả thuyết A/B ($t$-test, $Z$-test), trực quan hóa dữ liệu khám phá EDA đa chiều. | Báo cáo Thống kê Chương 1, Bộ biểu đồ 300 DPI Chương 3. |
| **Thành viên 3** | **AI / Machine Learning Lead** | Huấn luyện mô hình ML 2 giai đoạn (Draft & Snowball), đánh giá mô hình, thuật toán Gợi ý Cấm/Chọn (Recommender). | Pipeline Machine Learning Chương 4, Thuật toán Gợi ý Chương 6. |
| **Cả 3 thành viên** | **Tích hợp & Báo cáo** | Viết báo cáo Word chính thức, thiết kế slide bảo vệ, Web Demo Streamlit và tổng duyệt thuyết trình. | File Word, Slide PowerPoint, Web Demo. |

---

## 📅 LỘ TRÌNH 5 GIAI ĐOẠN (TIMELINE & ATOMIC CHECKLIST)

```
[ Giai đoạn 1 ] ──► [ Giai đoạn 2 ] ──► [ Giai đoạn 3 ] ──► [ Giai đoạn 4 ] ──► [ Giai đoạn 5 ]
  Dữ liệu & SQL       Thống kê & EDA       Machine Learning     Đóng gói API & Web    Mobile App & Báo cáo
   (Tuần 1 - 2)        (Tuần 2 - 3)          (Tuần 3 - 4)          (Tuần 4)            (Tuần 5)
```

---

### 🟢 GIAI ĐOẠN 1: THU THẬP, LÀM SẠCH & THIẾT KẾ CSDL (CHƯƠNG 2, 5)
*Mục tiêu:* Có kho dữ liệu sạch gồm cả Đấu Rank VN, Đấu Rank Hàn và Đấu Giải 2026 được nạp chuẩn chỉnh vào SQLite.

- [ ] **Task 1.1 [Thành viên 1]:** Chạy script `crawl_riot_matches.py` tích lũy tối thiểu $1,000 - 3,000$ trận rank Việt Nam (VN2) và Hàn Quốc (KR) mới nhất vào `lol_live_data.db`.
  * *Tiêu chí hoàn thành:* Bảng `matches_10min` có đủ 10 tướng theo 5 lane nguyên tử (`blueTop`..`redSupport`), 10 bans, và kinh tế phút 10.
  * *Chuẩn hóa CSDL 1NF & 3NF:* Triệt tiêu các cột gộp chuỗi `blueChampions`/`redChampions` (1NF) và loại bỏ cột `country` do phụ thuộc hàm vào `server` (3NF).
  * *Chiến lược Multi-server:* Server Hàn Quốc (`kr`) đóng vai trò đại diện cho đấu trường Solo Queue đỉnh cao của khu vực Đông Á (nơi các tuyển thủ Trung Quốc LPL và Hàn Quốc LCK cùng thi đấu).
- [ ] **Task 1.2 [Thành viên 1]:** Xây dựng module trích xuất file `2026_LoL_esports_match_data_from_OraclesElixir.csv` vào CSDL SQLite.
  * *Tiêu chí hoàn thành:* Tạo 2 bảng quan hệ `tournament_matches` (thông tin trận, đội, kết quả) và `tournament_players` (10 vị trí cá nhân).
- [ ] **Task 1.3 [Thành viên 1]:** Viết hàm làm sạch dữ liệu (Data Cleaning) theo Chương 2:
  * Lọc bỏ $100\%$ trận Remake ($<10$ phút) và AFK qua chỉ số lính ($CS < 10$ lúc 10 phút).
  * Phát hiện và xử lý ngoại lai (Outliers) bằng thuật toán IQR và Z-Score.
- [ ] **Task 1.4 [Thành viên 2 + 1]:** Viết 5 truy vấn SQL nâng cao theo Chương 5:
  * Truy vấn 1: Phân tích Kèo đấu Khắc chế 1v1 (Lane Matchup: Top Akali vs Jax, Mid Katarina vs Lissandra) dùng `JOIN` và `GROUP BY`.
  * Truy vấn 2: Phân tích Cặp đôi Ăn ý Đường Dưới (Bot Lane Synergy: Lucian+Nami, Jinx+Thresh) có `HAVING count(*) >= 10`.
  * Truy vấn 3: `Subquery` tìm các tướng có tỷ lệ Cấm/Chọn (Presence) cao nhất giải đấu LCK/LPL.
  * Truy vấn 4: Thống kê chỉ số lấn đường mốc 10 phút (`golddiffat10`, `csdiffat10`) của các tuyển thủ hàng đầu (Faker, Chovy, Levi).
  * Truy vấn 5: `MultiIndex` và Pivot Table bằng Pandas (Chương 5x) đối chiếu winrate theo tổ hợp vai trò.
- [ ] **Milestone 1:** Họp nhóm nghiệm thu CSDL SQLite hoàn chỉnh, export ra 2 file CSV sạch (`clean_ranked_10min.csv` và `clean_tournament_10min.csv`).

---

### 🔵 GIAI ĐOẠN 2: THỐNG KÊ SUY DIỄN & TRỰC QUAN HÓA EDA (CHƯƠNG 1, 3)
*Mục tiêu:* Chứng minh các giả thuyết bằng toán học thống kê và tạo bộ biểu đồ trực quan sắc nét.

- [ ] **Task 2.1 [Thành viên 2]:** Thực hiện Kiểm định giả thuyết A/B số 1 (Chương 1):
  * *Bài toán:* "Lợi thế Phe Xanh (Blue Side Advantage) có ý nghĩa thống kê hay không?"
  * *Phương pháp:* $Z$-test tỷ lệ 2 phía ($\alpha = 0.05$). Tính toán tỷ lệ thắng thực tế, $Z$-score và $p$-value.
- [ ] **Task 2.2 [Thành viên 2]:** Thực hiện Kiểm định giả thuyết A/B số 2 (Trọng tâm đồ án):
  * *Bài toán:* "Hiệu quả Lăn Cầu Tuyết (Snowball Lead) ở Đấu Giải chuyên nghiệp có vượt trội hơn Đấu Rank Kim Cương có ý nghĩa thống kê không?"
  * *Phương pháp:* Independent Two-sample $t$-test so sánh tỷ lệ chuyển hóa lợi thế $2,000$ vàng lúc 10 phút.
- [ ] **Task 2.3 [Thành viên 2]:** Kiểm định Chi-square ($\chi^2$) hoặc ANOVA:
  * Đội ăn 3 Sâu Hư Không đầu tiên vs Đội ăn Rồng Nguyên Tố đầu tiên $\rightarrow$ Mục tiêu nào đem lại winrate cao hơn?
- [ ] **Task 2.4 [Thành viên 2]:** Vẽ bộ biểu đồ trực quan hóa EDA theo Chương 3:
  * Biểu đồ 1: **Subplot đôi** so sánh Meta Tướng: Top 10 tướng ưu tiên ở Đấu Giải vs Top 10 tướng ở Rank Việt Nam & Hàn Quốc.
  * Biểu đồ 2: **Heatmap Ma trận Khắc chế 1v1** (Counter-pick Lane Heatmap) cho đường Giữa và đường Trên.
  * Biểu đồ 3: **Radar Chart (Biểu đồ Mạng nhện)** so sánh 5 trục sức mạnh đội hình.
  * Biểu đồ 4: **Boxplot** phân phối % sát thương đóng góp theo 5 vị trí thi đấu.
  * Biểu đồ 5: **Histogram & KDE plot** phân bố chênh lệch vàng phút 10 (`golddiffat10`).
- [ ] **Milestone 2:** Hoàn thiện toàn bộ code, bảng số liệu kiểm định và lưu các hình biểu đồ chất lượng cao (PNG 300 DPI) vào thư mục `reports/figures/`.

---

### 🟠 GIAI ĐOẠN 3: XÂY DỰNG MACHINE LEARNING 2 GIAI ĐOẠN & BAN/PICK AI (CHƯƠNG 4, 6)
*Mục tiêu:* Huấn luyện các mô hình dự đoán và xây dựng công cụ gợi ý cấm/chọn thông minh.

- [ ] **Task 3.1 [Thành viên 3]:** Xây dựng Mô hình Tầng 1 — **Draft Prediction (Phút 0)**:
  * *Đầu vào:* 10 tướng theo 5 lane đối đầu + 10 bans (One-hot encoding / Champion embeddings).
  * *Mô hình thử nghiệm:* Logistic Regression, Naive Bayes, LightGBM/XGBoost. Kỳ vọng: Độ chính xác $\approx 58 - 62\%$.
  * *Xử lý Concept Drift & Học liên tục:* Kết hợp **Sliding Window** (theo `gameVersion`) và **Exponential Time-Decay Sample Weighting** ($w_i = e^{-\lambda \Delta t}$) theo `crawled_at`.
- [ ] **Task 3.2 [Thành viên 3]:** Xây dựng Mô hình Tầng 2 — **In-Game Snowball Prediction (Phút 10)**:
  * *Đầu vào:* Chất tướng + Chỉ số kinh tế phút 10 (chênh lệch vàng, trụ, rồng, sâu, lính 5 đường).
  * *Mô hình thử nghiệm:* Random Forest, Gradient Boosting, Multi-Layer Perceptron. Kỳ vọng: Độ chính xác $\approx 80 - 85\%$.
- [ ] **Task 3.3 [Thành viên 3]:** Đánh giá & So sánh mô hình: Vẽ ROC Curve, AUC, Confusion Matrix, Feature Importance.
- [ ] **Task 3.4 [Thành viên 3]:** Phân cụm K-Means: Phân loại đội hình thành 4 trường phái chiến thuật (*Poke, Dive, Teamfight, Split-push*).
- [ ] **Task 3.5 [Thành viên 3 + 1]:** Xây dựng Hệ thống Gợi ý Cấm/Chọn Thông minh (Chương 6):
  * **Chức năng 1 (Counter Pick):** Gợi ý tướng khắc chế trực tiếp theo đường (đối phương pick Zed Mid $\rightarrow$ gợi ý Lissandra/Malzahar).
  * **Chức năng 2 (Synergy Pick):** Khai phá luật kết hợp Apriori tìm cặp đôi ăn ý (Yasuo $\rightarrow$ Gragas/Diana; Lucian $\rightarrow$ Nami).
- [ ] **Milestone 3:** Lưu trữ các mô hình đã huấn luyện thành công vào file (`draft_model.pkl`, `snowball_model.pkl`, `recommender.pkl`).

---

### 🟣 GIAI ĐOẠN 4: ĐÓNG GÓI REST API (FASTAPI) & DỰNG WEB DEMO (STREAMLIT)
*Mục tiêu:* Tạo "cầu nối" API để mô hình Machine Learning có thể phục vụ đồng thời cho cả Web thuyết trình lẫn Mobile App.

- [ ] **Task 4.1 [Thành viên 1]:** Xây dựng Backend REST API bằng **FastAPI** (`src/api/app.py`):
  * `GET /api/champions`: Trả về danh sách 173 tướng, ảnh đại diện và thuộc tính.
  * `POST /api/predict/draft`: Nhận 10 tướng $\rightarrow$ trả về xác suất thắng lúc chọn tướng.
  * `POST /api/predict/snowball`: Nhận 10 tướng + kinh tế phút 10 $\rightarrow$ trả về xác suất thắng lúc 10 phút.
  * `GET /api/recommend/counter`: Nhận tên tướng đối thủ $\rightarrow$ trả về top 3 tướng khắc chế và winrate.
  * `GET /api/stats/matchups`: Trả về lịch sử đối đầu 1v1 từ CSDL SQLite.
- [ ] **Task 4.2 [Thành viên 1 + 3]:** Dựng Web Dashboard bằng **Streamlit** (`src/web_dashboard/app.py`):
  * Giao diện 3 Tab trực quan: Tra cứu CSDL SQLite, Dự đoán tỷ lệ thắng live, và Gợi ý Cấm/Chọn.
  * Phục vụ demo trực tiếp trên máy chiếu giảng đường khi bảo vệ đồ án Data Science.
- [ ] **Milestone 4:** Chạy thử nghiệm thành công toàn bộ hệ thống qua Web Streamlit và kiểm tra Swagger Docs tại `http://localhost:8000/docs`.

---

### 🔴 GIAI ĐOẠN 5: XÂY DỰNG MOBILE APP, VIẾT BÁO CÁO & BẢO VỆ ĐỒ ÁN
*Mục tiêu:* Đóng gói sản phẩm hoàn hảo cho cả 2 môn học, sẵn sàng đạt điểm 10 tuyệt đối.

- [ ] **Task 5.1 [Thành viên 1 — Môn Lập trình Di động]:** Xây dựng Ứng dụng Mobile (Android Native / Flutter):
  * **Màn hình 1 (Danh mục tướng):** `GridView` 173 tướng tải ảnh bất đồng bộ từ Riot Data Dragon CDN qua URL.
  * **Màn hình 2 (Phòng Cấm/Chọn Thông minh):** Chọn tướng 2 phe $\rightarrow$ gọi API `predict/draft` $\rightarrow$ hiển thị thanh `ProgressBar` tỷ lệ thắng kèm animation.
  * **Màn hình 3 (Trợ lý Khắc chế):** Chọn tướng địch $\rightarrow$ gọi API `recommend/counter` $\rightarrow$ hiển thị thẻ gợi ý tướng khắc chế.
  * **Màn hình 4 (Tra cứu CSDL):** Xem tỷ lệ thắng của các kèo đấu đối đầu từ SQLite.
- [ ] **Task 5.2 [Thành viên 1, 2, 3 — Môn Data Science]:** Soạn thảo Báo cáo tổng thể Word/PDF:
  * Thành viên 1: Phần Mở đầu, Chương 2 (Tiền xử lý), Chương 5 (CSDL SQL & Pandas), Kiến trúc API.
  * Thành viên 2: Chương 1 (Thống kê suy diễn), Chương 3 (Trực quan hóa EDA), nhận xét biểu đồ.
  * Thành viên 3: Chương 4 (Machine Learning 2 giai đoạn), Chương 6 (Gợi ý Cấm/Chọn), Đánh giá mô hình.
- [ ] **Task 5.3 [Cả 3 thành viên]:** Thiết kế Slide thuyết trình PowerPoint ($20 - 25$ slides trực quan).
- [ ] **Task 5.4 [Cả 3 thành viên]:** Kịch bản Demo Live:
  * Trình chiếu Web Dashboard Streamlit trên máy chiếu.
  * Cầm điện thoại mở Mobile App thao tác trực tiếp $\rightarrow$ Cả 2 nền tảng cùng nhận kết quả từ mô hình Machine Learning.
- [ ] **Milestone 5:** Bảo vệ thành công đồ án với điểm số tối đa ở cả 2 môn học!

---

## 🛠️ NGUYÊN TẮC PHỐI HỢP CỦA NHÓM 3 NGƯỜI
1. **Quản lý Code chung trên GitHub / Git:**
   * Tạo 3 nhánh làm việc độc lập: `feature/data-sql-api` (Thành viên 1), `feature/stats-eda` (Thành viên 2), `feature/ml-recsys` (Thành viên 3).
2. **Quy tắc "Không chặn nhau" (No Blockers):**
   * Do đã có sẵn file `2026_LoL_esports_match_data_from_OraclesElixir.csv` và CSDL mẫu `lol_live_data.db`, Thành viên 2 và Thành viên 3 có thể làm ngay Thống kê, EDA và Machine Learning mà không cần đợi Thành viên 1!
