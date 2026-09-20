# PROJECT TASKS & ATOMIC CHECKLIST

Trạng thái:
- `[x] DONE`: Đã hoàn thành và xác minh bằng kiểm thử/dữ liệu thực tế.
- `[-] IN PROGRESS`: Đang trong quá trình thực hiện.
- `[ ] NOT STARTED`: Chưa bắt đầu.
- `[!] BLOCKED`: Bị chặn bởi phụ thuộc kỹ thuật.

---

## 🟢 GIAI ĐOẠN 1: THU THẬP, LÀM SẠCH & THIẾT KẾ CSDL (CHƯƠNG 2, 5)

- [x] **Task 1.0 [Cả nhóm]: Thiết lập cấu hình tập trung `src/config` & Cấu trúc thư mục Pipeline chuẩn**
  - *Mục tiêu:* Tạo package cấu hình chuẩn `src/config/` (`settings.py`, `__init__.py`), bảo vệ Riot API key, nạp `.env`. Khởi tạo đầy đủ cây thư mục từ `02` đến `07`, `notebooks/`, `reports/figures/` đi kèm file tài liệu `README.md` chuẩn hóa.
  - *Kết quả:* Đã hoàn tất và kiểm thử 100% trơn tru.

- [-] **Task 1.1 [Thành viên 1]: Cào dữ liệu Live Rank VN & KR từ Riot Games API**
  - *Mục tiêu:* Tích lũy tối thiểu 500 - 1,000 trận rank cao (VN2 & KR) đạt chuẩn 1NF/3NF vào `data/database/lol_live_data.db`.
  - *Hiện trạng:* Đã cào được 100 trận đầu tiên (99 VN2, 1 KR). Script đã tích hợp module cấu hình `src.config`, key hoạt động, kết nối Data Dragon 173 tướng ổn định. Đang chờ kích hoạt cào bổ sung máy chủ KR.
  - *Acceptance Criteria:* Bảng `matches_10min` có $\ge 500$ trận, không có giá trị NULL ở các cột chỉ số chính, tỷ lệ VN2 và KR cân bằng hơn.

- [ ] **Task 1.2 [Thành viên 1]: Nạp dữ liệu giải đấu chuyên nghiệp 2026 vào SQLite**
  - *Mục tiêu:* Viết script ETL đọc `data/raw/2026_LoL_esports_match_data_from_OraclesElixir.csv` nạp vào 2 bảng `tournament_matches` và `tournament_players`.
  - *Acceptance Criteria:* CSDL có 2 bảng mới, truy vấn thử lấy đúng thông tin các giải LCK, LPL, VCS năm 2026.

- [ ] **Task 1.3 [Thành viên 1]: Viết module làm sạch dữ liệu & khử ngoại lai (IQR/Z-Score)**
  - *Mục tiêu:* Viết hàm trong `src/02_preprocessing/cleaner.py` lọc bỏ 100% trận Remake (< 10 phút), AFK (CS < 10), và outlier chênh lệch vàng bất thường.
  - *Acceptance Criteria:* Có thống kê số lượng bản ghi trước và sau khi lọc, không làm mất tính toàn vẹn dữ liệu.

- [ ] **Task 1.4 [Thành viên 1 + 2]: Viết 5 câu truy vấn SQL nâng cao theo Chương 5**
  - *Truy vấn 1:* Kèo đấu đối đầu 1v1 (Lane Matchup) dùng `JOIN` và `GROUP BY`.
  - *Truy vấn 2:* Cặp đôi ăn ý đường dưới (Synergy) có `HAVING count(*) >= 10`.
  - *Truy vấn 3:* Subquery tìm top tướng có tỷ lệ cấm/chọn (Presence) cao nhất.
  - *Truy vấn 4:* Thống kê chỉ số lấn đường phút thứ 10 (`golddiffat10`, `csdiffat10`).
  - *Truy vấn 5:* MultiIndex / Pivot Table đối chiếu tỷ lệ thắng.
  - *Acceptance Criteria:* Viết trong file `src/03_database_sql/queries.sql` hoặc notebook, chạy ra kết quả bảng dữ liệu chính xác.

- [ ] **Milestone 1:** Nghiệm thu toàn bộ CSDL SQLite `lol_live_data.db` hoàn chỉnh cả 2 nguồn dữ liệu.

---

## 🔵 GIAI ĐOẠN 2: THỐNG KÊ SUY DIỄN & TRỰC QUAN HÓA EDA (CHƯƠNG 1, 3)

- [ ] **Task 2.1 [Thành viên 2]:** Kiểm định A/B Lợi thế Phe Xanh ($Z$-test tỷ lệ 2 phía, $\alpha = 0.05$).
- [ ] **Task 2.2 [Thành viên 2]:** Kiểm định $t$-test Lăn Cầu Tuyết (Snowball Lead) Đấu giải vs Rank Solo.
- [ ] **Task 2.3 [Thành viên 2]:** Kiểm định Chi-square Mục tiêu lớn (Rồng Nguyên Tố vs 3 Sâu Hư Không).
- [ ] **Task 2.4 [Thành viên 2]:** Vẽ bộ 5 biểu đồ EDA 300 DPI lưu vào `reports/figures/`.
- [ ] **Milestone 2:** Báo cáo Thống kê & EDA hoàn tất trong Notebook `01_kham_pha_du_lieu_EDA.ipynb`.

---

## 🟠 GIAI ĐOẠN 3: XÂY DỰNG MACHINE LEARNING 2 GIAI ĐOẠN & BAN/PICK AI (CHƯƠNG 4, 6)

- [ ] **Task 3.1 [Thành viên 3]:** Xây dựng Mô hình Draft Prediction lúc cấm chọn (Phút 0). Áp dụng Sliding Window + Sample Weighting.
- [ ] **Task 3.2 [Thành viên 3]:** Xây dựng Mô hình Snowball Prediction trong trận (Phút 10 - Random Forest / XGBoost). Kỳ vọng Accuracy > 80%.
- [ ] **Task 3.3 [Thành viên 3]:** Đánh giá mô hình: ROC-AUC Curve, Confusion Matrix, Feature Importance.
- [ ] **Task 3.4 [Thành viên 3]:** Phân cụm K-Means: Phân loại 4 trường phái đội hình chiến thuật.
- [ ] **Task 3.5 [Thành viên 3 + 1]:** Xây dựng Hệ thống Gợi ý Cấm/Chọn (Counter Pick & Synergy Apriori).
- [ ] **Milestone 3:** Xuất các file mô hình `draft_model.pkl`, `snowball_model.pkl`, `recommender.pkl`.

---

## 🟣 GIAI ĐOẠN 4: ĐÓNG GÓI REST API (FASTAPI) & DỰNG WEB APP (GIAI ĐOẠN 1 MÔN KH DỮ LIỆU)

- [ ] **Task 4.1 [Thành viên 1]:** Xây dựng Backend REST API bằng **FastAPI** (`src/api/`):
  - `POST /api/v1/predict`: Dự đoán tỉ lệ thắng.
  - `GET /api/v1/champions`: Danh sách 173 tướng.
  - `POST /api/v1/recommend`: Gợi ý cấm/chọn.
- [ ] **Task 4.2 [Thành viên 1 + 3]:** Xây dựng Giao diện Web App tương tác (`web/` hoặc Streamlit).
- [ ] **Milestone 4:** Demo hoàn chỉnh Web App kết nối API nộp môn Nhập môn Khoa học Dữ liệu.

---

## 🔴 GIAI ĐOẠN 5: MOBILE APP ANDROID & BÁO CÁO TỔNG KẾT

- [ ] **Task 5.1 [Thành viên 1]:** Phát triển ứng dụng Android (Java/Kotlin, RecyclerView, Retrofit) gọi API FastAPI (Môn Di động).
- [ ] **Task 5.2 [Cả nhóm]:** Viết báo cáo tổng kết Word/PDF.
- [ ] **Task 5.3 [Cả nhóm]:** Thiết kế Slide thuyết trình PowerPoint.
- [ ] **Task 5.4 [Cả nhóm]:** Tổng duyệt demo và bảo vệ đồ án trước hội đồng.
- [ ] **Milestone 5:** Đạt điểm số tối đa cả 2 môn học.
