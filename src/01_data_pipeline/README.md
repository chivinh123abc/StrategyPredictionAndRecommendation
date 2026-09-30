# MODULE 01: DATA PIPELINE (THU THẬP & ĐỒNG BỘ DỮ LIỆU)

Thư mục này quản lý toàn bộ quy trình thu thập, trích xuất và đồng bộ hóa hai nguồn dữ liệu chủ đạo của đồ án:

| Nguồn dữ liệu | Tệp mã nguồn | Tài liệu hướng dẫn chi tiết | Mục tiêu & Đầu ra |
| :--- | :--- | :--- | :--- |
| **1. Live Ranked Solo Queue (Riot Games API)** | [`crawl_riot_matches.py`](crawl_riot_matches.py) | 📖 [**`README_CRAWL_RIOT.md`**](README_CRAWL_RIOT.md) | Cào trận đấu Rank Thách Đấu/Cao Thủ thời gian thực tại mốc phút thứ 10.<br>$\rightarrow$ Xuất vào `data/database/lol_live_data.db` (bảng `matches_10min`) và `data/processed/lol_live_ranked_10min.csv`. |
| **2. Esports Pro Play (Google Drive Cloud Sync)** | [`sync_google_drive.py`](sync_google_drive.py) | 📖 [**`README_SYNC_DRIVE.md`**](README_SYNC_DRIVE.md) | Tự động đồng bộ các mùa giải chuyên nghiệp Oracle's Elixir từ Google Drive dùng chung.<br>$\rightarrow$ Tự động đón đầu các mùa giải mới nhất và trích xuất `data/raw/esports_active_matches.csv`. |
| **3. Esports ETL Loader (SQLite Database)** | [`load_esports_to_db.py`](load_esports_to_db.py) | 📖 Hướng dẫn bên dưới | Nạp dữ liệu giải đấu chuyên nghiệp vào CSDL SQLite chuẩn hóa 1NF/3NF.<br>$\rightarrow$ Nạp 2 bảng `tournament_matches` (6,000 dòng) và `tournament_players` (30,000 dòng) vào `lol_live_data.db`. |

---

## TỔNG QUAN CÁC NHÁNH PIPELINE

### 1. Nhánh 1: Cào Dữ Liệu Live Rank từ Riot Games API
- **Tài liệu:** Đọc hướng dẫn toàn diện tại [**`README_CRAWL_RIOT.md`**](README_CRAWL_RIOT.md).
- **Điểm nổi bật:**
  - Chuẩn hóa 1NF & 3NF: Tách 10 vị trí thi đấu nguyên tử (`blueTop`, `blueMid`...).
  - Trích xuất Timeline chi tiết mốc phút thứ 10 (chênh lệch vàng, kinh nghiệm, rồng, sâu hư không...).
  - Cơ chế tự động nghỉ (Exponential Backoff) khi gặp Rate Limit `HTTP 429`.
- **Lệnh chạy nhanh:**
  ```bash
  python src/01_data_pipeline/crawl_riot_matches.py
  ```

---

### 2. Nhánh 2: Đồng Bộ Dữ Liệu Đấu Giải từ Google Drive
- **Tài liệu:** Đọc hướng dẫn toàn diện tại [**`README_SYNC_DRIVE.md`**](README_SYNC_DRIVE.md).
- **Điểm nổi bật:**
  - Tự động nhận diện thư mục Google Drive chung chứa 13 mùa giải (2014 - nay).
  - Thuật toán quyết định mùa giải thông minh (ADR-013): Ưu tiên năm mới nhất; nếu đầu mùa chưa đủ mẫu thì tự động ghép thích ứng với phần cuối năm trước (CKTG / Mùa Hè).
  - Hỗ trợ bộ lọc giải đấu linh hoạt (`--leagues LCK,LCP,LPL,MSI,WLDS,EWC`) và xuất ra tệp hoạt động `data/raw/esports_active_matches.csv` (26.8 MB, 3,000 trận đỉnh cao, 36,000 dòng).
  - Hàm lọc chuyên biệt `filter_esports_by_leagues()` và cờ CLI `--filter --filter-leagues LCK,LCP,LPL,MSI,WLDS,EWC` cho phép lọc offline không cần tải lại.
  - Tối ưu băng thông (Smart Caching): Tự động kiểm tra và bỏ qua không tải lại các file đã có sẵn trên máy trạm.
  - Cơ chế chống Quota Exceeded 2 tầng: Tầng 1 (`gdown` tải ẩn danh nhanh) $\rightarrow$ Tầng 2 (`Google Drive API v3 + OAuth2` sao chép My Drive vượt hạn ngạch).
- **Lệnh chạy nhanh:**
  ```bash
  # Tự động thẩm định mùa giải mới nhất và đồng bộ:
  python src/01_data_pipeline/sync_google_drive.py

  # Đồng bộ trọn vẹn 6 giải đấu đỉnh cao (LCK, LCP, LPL, MSI, WLDS, EWC):
  python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL,MSI,WLDS,EWC

  # Lọc trực tiếp từ file đã có trên máy:
  python src/01_data_pipeline/sync_google_drive.py --filter --filter-leagues LCK,LCP,LPL,MSI,WLDS,EWC

  # Kiểm tra độ sạch & sức khỏe dữ liệu (Data Health Card):
  python src/01_data_pipeline/sync_google_drive.py --check
  ```

---

### 3. Nhánh 3: Nạp Dữ Liệu Đấu Giải Vào SQLite (ETL Pipeline)
- **Mã nguồn:** [`load_esports_to_db.py`](load_esports_to_db.py)
- **Điểm nổi bật:**
  - Tự động đọc tệp hoạt động `esports_active_matches.csv` và bóc tách thành 2 bảng quan hệ chuẩn 1NF/3NF:
    - `tournament_matches`: 6,000 dòng (3,000 trận $\times$ 2 đội Xanh/Đỏ), 155 cột.
    - `tournament_players`: 30,000 dòng (3,000 trận $\times$ 10 tuyển thủ), 129 cột.
  - Tự động chuẩn hóa tên cột (snake_case, khử khoảng trắng và ký tự đặc biệt).
  - Thiết lập khóa chính composite (`PRIMARY KEY`), khóa ngoại (`FOREIGN KEY (gameid, side)`), và 12 Indexes tối ưu truy vấn SQL.
  - Tích hợp báo cáo kiểm định chất lượng dữ liệu tự động (Data Integrity Audit) ngay sau khi nạp.
- **Lệnh chạy nhanh:**
  ```bash
  # Nạp dữ liệu vào CSDL SQLite mặc định (lol_live_data.db):
  python src/01_data_pipeline/load_esports_to_db.py

  # Ép buộc xóa và tái tạo bảng từ đầu:
  python src/01_data_pipeline/load_esports_to_db.py --force

  # Chỉ chạy kiểm định và hiển thị báo cáo dữ liệu hiện có trong DB:
  python src/01_data_pipeline/load_esports_to_db.py --verify
  ```
