# MODULE 01: DATA PIPELINE (THU THẬP & ĐỒNG BỘ DỮ LIỆU)

Thư mục này quản lý toàn bộ quy trình thu thập, trích xuất và đồng bộ hóa hai nguồn dữ liệu chủ đạo của đồ án:

| Nguồn dữ liệu | Tệp mã nguồn | Tài liệu hướng dẫn chi tiết | Mục tiêu & Đầu ra |
| :--- | :--- | :--- | :--- |
| **1. Live Ranked Solo Queue (Riot Games API)** | [`crawl_riot_matches.py`](crawl_riot_matches.py) | 📖 [**`README_CRAWL_RIOT.md`**](README_CRAWL_RIOT.md) | Cào trận đấu Rank Thách Đấu/Cao Thủ thời gian thực tại mốc phút thứ 10.<br>$\rightarrow$ Xuất vào `data/database/lol_live_data.db` và `data/processed/lol_live_ranked_10min.csv`. |
| **2. Esports Pro Play (Google Drive Cloud Sync)** | [`sync_google_drive.py`](sync_google_drive.py) | 📖 [**`README_SYNC_DRIVE.md`**](README_SYNC_DRIVE.md) | Tự động đồng bộ các mùa giải chuyên nghiệp Oracle's Elixir từ Google Drive dùng chung.<br>$\rightarrow$ Tự động đón đầu các mùa giải mới nhất và lưu vào `data/raw/*.csv`. |

---

## TỔNG QUAN HAI NHÁNH DỮ LIỆU

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
  - Thuật toán quyết định mùa giải thông minh (ADR-013): Ưu tiên năm mới nhất; nếu đầu mùa chưa đủ mẫu thì tự động ghép với phần cuối năm trước.
  - Hỗ trợ bộ lọc giải đấu linh hoạt (`--leagues LCK,LCP,LPL`) để lọc đúng giải mong muốn vào `data/raw/esports_active_matches.csv`.
  - Tối ưu băng thông (Smart Caching): Tự động kiểm tra và bỏ qua không tải lại các file đã có sẵn trên máy trạm.
- **Lệnh chạy nhanh:**
  ```bash
  # Tự động thẩm định mùa giải mới nhất và đồng bộ:
  python src/01_data_pipeline/sync_google_drive.py
  
  # Chỉ lấy các giải đấu trọng tâm (LCK, LCP, LPL):
  python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL
  
  # Liệt kê danh mục file trên Drive:
  python src/01_data_pipeline/sync_google_drive.py --list
  ```
