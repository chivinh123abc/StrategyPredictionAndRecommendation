# CHANGELOG (NHẬT KÝ THAY ĐỔI DỰ ÁN)

Tất cả các thay đổi quan trọng về code, CSDL và tài liệu kiến trúc được ghi lại tại đây theo thứ tự thời gian.

---

## [2026-09-20] - XÂY DỰNG HOÀN TẤT MODULE ĐỒNG BỘ GOOGLE DRIVE (SYNC_GOOGLE_DRIVE.PY)
- **Triển khai module [src/01_data_pipeline/sync_google_drive.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/sync_google_drive.py):**
  - Tích hợp kết nối trực tiếp với Thư mục Google Drive Oracle's Elixir (`1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`).
  - Sử dụng `gdown` để quét danh mục siêu nhẹ 13 mùa giải (2014-2026) mà không cần tải dữ liệu nặng (`--list`).
  - Cơ chế Cache Manifest (`.drive_sync_manifest.json`): Tự động phát hiện dung lượng file cục bộ để bỏ qua tải trùng lặp, tiết kiệm 71 MB băng thông mạng.
  - Hỗ trợ tham số linh hoạt: Tải năm chỉ định (`--year`), tải toàn bộ lịch sử (`--all`), và ép buộc làm mới (`--force`).
- **Cập nhật cấu hình & tài liệu:**
  - Thêm `GOOGLE_DRIVE_FOLDER_ID` vào `src/config/settings.py`, `src/config/__init__.py`, `.env`, `.env.example`.
  - Bổ sung `gdown>=6.4.0` vào `requirements.txt`.
  - Cập nhật tài liệu hướng dẫn vận hành trong [src/01_data_pipeline/README.md](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/README.md).
  - Hoàn thành nghiệm thu **Task 1.5** trong [AI/TASKS.md](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/AI/TASKS.md).

---

## [2026-09-20] - BỔ SUNG KIẾN TRÚC & TASK ĐỒNG BỘ DỮ LIỆU TỰ ĐỘNG TỪ GOOGLE DRIVE
- **Quy hoạch tính năng Cloud Data Auto-Sync (Task 1.5):**
  - Bổ sung quyết định kiến trúc [ADR-010](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/AI/DECISIONS.md) và phân rã nhiệm vụ trong [AI/TASKS.md](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/AI/TASKS.md).
  - Cơ chế: Hệ thống tự động kiểm tra thời gian cập nhật (`modifiedTime`) hoặc hash `md5Checksum` của tệp/thư mục Google Drive chia sẻ (tập dữ liệu giải đấu, nhãn bổ sung).
  - Tối ưu hóa: Chỉ tải về `data/raw/` khi trên Drive có dữ liệu mới; tự động kích hoạt pipeline làm sạch và cập nhật CSDL SQLite phục vụ làm việc nhóm khép kín.

---

## [2026-09-20] - FIX BUG ĐIỀU KIỆN DỪNG CỦA CRAWLER TRÊN CSDL ĐA MÁY CHỦ
- **Sửa lỗi ngắt sớm tại hàm `get_match_ids` trong [src/01_data_pipeline/crawl_riot_matches.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/crawl_riot_matches.py):**
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
  - Tạo package [src/config/](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/config/) gồm `settings.py` và `__init__.py`.
  - Quản lý tập trung toàn bộ biến môi trường (`.env`), xác thực Riot API key, đường dẫn thư mục I/O (`BASE_DIR`, `DATA_DIR`, `OUTPUT_CSV`, `OUTPUT_DB`), thông số server (`ACTIVE_SERVERS`, `SERVER_METADATA`).
  - Xóa file `config.py` ở thư mục gốc Project để giữ cấu trúc thư mục sạch sẽ, không có file lẻ đứng giữa đường.
- **Cập nhật script crawler [src/01_data_pipeline/crawl_riot_matches.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/crawl_riot_matches.py):**
  - Import cấu hình trực tiếp từ `src.config` (kèm fallback an toàn).
  - Loại bỏ các khối logic kiểm tra key trùng lặp vì module cấu hình đã tự động kiểm tra ngay khi nạp.
  - Chạy thử nghiệm thành công 100% không phát sinh bất kỳ lỗi đường dẫn nào.
- **Quy tắc Git:** Tuyệt đối không commit hay push tự động; giữ toàn bộ thay đổi ở Working Tree để User toàn quyền kiểm soát.

---

## [2026-09-20] - HOÀN NGUYÊN NGUYÊN TRẠNG BẢN CRAWLER ĐƠN LẬP (COMMIT 40dced0)
- **Hoàn nguyên mã nguồn [src/01_data_pipeline/crawl_riot_matches.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/crawl_riot_matches.py):**
  - Giữ nguyên cấu trúc xác định thư mục gốc `BASE_DIR = os.path.dirname(...)` nguyên bản.
  - Giữ nguyên toàn bộ cấu hình `.env`, biến môi trường, đường dẫn I/O và metadata tập trung trong một file duy nhất.
  - Dọn sạch toàn bộ các file cấu hình phát sinh ngoài luồng (`src/config.py`, `src/logger.py`, `pyproject.toml`, `tests/`, `.github/`).
- **Cập nhật quy tắc quản trị [AI/AI_RULES.md](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/AI/AI_RULES.md):**
  - Bổ sung quy định bắt buộc: **TUYỆT ĐỐI KHÔNG tự ý chạy lệnh `git push` lên GitHub** khi chưa có sự cho phép trực tiếp từ User.


## [2026-09-20] - DỌN DẸP DỰ ÁN TINH GỌN (CLEAN CODEBASE)
- **Xóa bỏ file trùng lặp:**
  - Xóa file `crawl_riot_matches.py` ở root, chỉ giữ lại một file chính thức duy nhất tại [src/01_data_pipeline/crawl_riot_matches.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/crawl_riot_matches.py).
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
