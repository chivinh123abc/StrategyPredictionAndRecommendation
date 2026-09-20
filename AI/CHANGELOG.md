# CHANGELOG (NHẬT KÝ THAY ĐỔI DỰ ÁN)

Tất cả các thay đổi quan trọng về code, CSDL và tài liệu kiến trúc được ghi lại tại đây theo thứ tự thời gian.

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
