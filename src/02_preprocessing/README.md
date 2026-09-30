# Module 02: Tiền Xử Lý Dữ Liệu & Khử Ngoại Lai (Data Preprocessing & Outlier Handling)

## 1. Mục tiêu & Trách nhiệm
Module này chịu trách nhiệm làm sạch, chuẩn hóa và khử ngoại lai toàn diện cho cả hai nguồn dữ liệu (Riot API và Oracle's Elixir) theo đúng chuẩn giáo trình **Chương 2 (Data Preparation)**:
- **Lọc bỏ trận đấu bất thường (Domain Filtering):** Loại bỏ 100% các trận Remake (< 10 phút) và trận có người chơi AFK/thoát game sớm ($CS_{10} < 10$).
- **Khử khuyết thiếu (Missing Value Imputation):**
  - Zero-Imputation cho các biến mục tiêu count/sự kiện (`elders`, `atakhans`, `doublekills`...).
  - Categorical-Imputation (`'NoBan'`) cho các lượt cấm bị bỏ qua.
  - Phân luồng dữ liệu thông minh theo `datacompleteness` cho tác vụ mốc 10 phút.
- **Xử lý giá trị ngoại lai (Outlier Handling):** Áp dụng 2 thuật toán **IQR (Interquartile Range)** và **Z-Score**; hỗ trợ cả 2 cơ chế Trimming (Lọc bỏ) và Winsorization (Cắt ngọn/Capping).
- **Kỹ nghệ đặc trưng (Feature Engineering):** Tính toán các chỉ số chuẩn hóa `goldDiffPerMin10`, `csDiffPerMin10`, `kda` phục vụ phân tích EDA và huấn luyện mô hình.

---

## 2. Dữ liệu vào (Input)
- `data/database/lol_live_data.db` (3 bảng: `matches_10min`, `tournament_matches`, `tournament_players`).

---

## 3. Dữ liệu ra (Output tại `data/processed/`)
1. **`clean_ranked_10min.csv`:** Dữ liệu Solo Rank Thách Đấu/Cao Thủ sạch mốc 10 phút.
2. **`clean_tournament_10min.csv`:** Dữ liệu Đấu Giải sạch mốc 10 phút (phục vụ mô hình Snowball & kiểm định T-test).
3. **`clean_tournament_draft.csv`:** Toàn bộ 3,000 trận đấu giải đỉnh cao sạch (phục vụ mô hình Cấm/Chọn Draft AI & Recommender).
4. **`clean_tournament_players.csv`:** Dữ liệu 10 vị trí tuyển thủ cá nhân đã làm sạch.

---

## 4. Hướng dẫn chạy Script (`cleaner.py`)
```bash
# 1. Chạy làm sạch mặc định (phương pháp IQR, lọc bỏ ngoại lai):
python src/02_preprocessing/cleaner.py

# 2. Chạy với phương pháp Z-Score (|Z| > 3.0):
python src/02_preprocessing/cleaner.py --outlier-method zscore

# 3. Chạy kết hợp đồng thuận cả IQR & Z-Score (tỷ lệ giữ lại > 96%):
python src/02_preprocessing/cleaner.py --outlier-method both

# 4. Chạy chế độ Winsorization / Capping (cắt ngọn thay vì xóa dòng):
python src/02_preprocessing/cleaner.py --outlier-action cap
```

