# CHANGELOG (NHẬT KÝ THAY ĐỔI DỰ ÁN)

Tất cả các thay đổi quan trọng về code, CSDL và tài liệu kiến trúc được ghi lại tại đây theo thứ tự thời gian.

---

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
