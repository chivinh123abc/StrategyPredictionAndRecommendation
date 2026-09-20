# PROJECT STATE (TRẠNG THÁI DỰ ÁN THỰC TẾ)

*Thời điểm audit thực tế:* 2026-09-20  
*Nguồn dữ liệu:* Khảo sát trực tiếp từ mã nguồn, CSDL SQLite, file hệ thống và lệnh `pip list`.

---

## 1. TỔNG QUAN HIỆN TRẠNG
- **Tên dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Môn học chính:** Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT).
- **Môn học mở rộng:** Lập trình trên thiết bị di động (ThS. Nguyễn Trung Hiếu, PTITHCM).
- **Giai đoạn hiện tại:** Giai đoạn 1 (Thu thập, Làm sạch Dữ liệu & Thiết kế CSDL).
- **Đánh giá tiến độ tổng:** ~20% (Đã hoàn thành Task 1.0, Task 1.1, Task 1.5; sẵn sàng triển khai Task 1.2 nạp dữ liệu giải đấu vào SQLite).

---

## 2. HIỆN TRẠNG MÃ NGUỒN (SOURCE CODE AUDIT)

| Thư mục / File | Trạng thái thực tế | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| `src/config/` | `VERIFIED - WORKING` | Package cấu hình trung tâm dự án (`settings.py`, `__init__.py`). Nạp `.env`, thẩm định API key, quản lý đường dẫn và metadata. |
| `src/01_data_pipeline/` | `VERIFIED - WORKING` | Gồm `crawl_riot_matches.py`, `sync_google_drive.py` (hỗ trợ OAuth 2.0 2 tầng, bộ lọc giải đấu LCK/LCP/LPL) và 2 file README đặc tả. |
| `.env` / `.env.example` | `VERIFIED - WORKING` | File cấu hình biến môi trường và file mẫu template an toàn. `.gitignore` đã chặn `.env`. |
| `src/02_preprocessing/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` quy định luồng xử lý outlier IQR. Sẵn sàng viết code. |
| `src/03_database_sql/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` đặc tả schema và 5 câu query SQL. Chuẩn bị thực hiện Task 1.2. |
| `src/04_hypothesis_testing/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` quy định 3 bài kiểm định Z/t/Chi-square. Sẵn sàng viết code. |
| `src/05_visualization/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` đặc tả 5 biểu đồ EDA 300 DPI. Sẵn sàng viết code. |
| `src/06_machine_learning/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` đặc tả mô hình 2 tầng. Sẵn sàng viết code. |
| `src/07_recommender/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` thuật toán gợi ý cấm/chọn. Sẵn sàng viết code. |
| `src/api/` | `NOT CREATED (FACT)` | Chưa tạo thư mục mã nguồn Backend FastAPI. |
| `web/` | `NOT CREATED (FACT)` | Chưa tạo thư mục giao diện Web App. |
| `mobile_app/` | `NOT CREATED (FACT)` | Chưa tạo thư mục ứng dụng Android (theo kế hoạch là Giai đoạn 2). |
| `notebooks/` | `INITIALIZED` | Đã khởi tạo thư mục kèm tài liệu `README.md` phục vụ thử nghiệm `.ipynb`. |
| `reports/figures/` | `INITIALIZED` | Đã khởi tạo thư mục kèm tài liệu `README.md` sẵn sàng nhận ảnh xuất 300 DPI từ bước EDA. |

---

## 3. HIỆN TRẠNG DỮ LIỆU & CƠ SỞ DỮ LIỆU (DATABASE AUDIT)

### CSDL SQLite chính: `data/database/lol_live_data.db`
- **Số bảng hiện có:** 1 bảng duy nhất: `matches_10min` (FACT).
- **Tổng số dòng dữ liệu:** 1,009 dòng (FACT / VERIFIED).
- **Phân bổ máy chủ:** 
  - `VN2` (Việt Nam): 550 trận (~54.5%).
  - `KR` (Hàn Quốc): 459 trận (~45.5%).
- **Số lượng cột:** Đúng 42 cột đạt chuẩn 1NF (10 cột tướng nguyên tử `blueTop`..`blueSupport`, `redTop`..`redSupport`) và 3NF (không có cột `country`, có cột `server`).
- **Các bảng chuẩn bị nạp (Task 1.2):** `tournament_matches`, `tournament_players` từ dữ liệu `esports_active_matches.csv`.

### Các tệp dữ liệu phẳng (CSV):
1. `data/processed/lol_live_ranked_10min.csv`: 1,009 dòng dữ liệu tương ứng bảng `matches_10min` (1,009 $\times$ 42 cột). Kích thước: ~550 KB (FACT).
2. `data/raw/2026_LoL_esports_match_data_from_OraclesElixir.csv`: 106,896 dòng, 165 cột dữ liệu đấu giải chuyên nghiệp năm 2026 (8,908 trận). Kích thước: 71.5 MB (FACT / VERIFIED).
3. `data/raw/2025_LoL_esports_match_data_from_OraclesElixir.csv`: Dữ liệu mùa giải 2025 dùng cho cơ chế bù đắp mẫu thích ứng (Adaptive Merging). Kích thước: 79.1 MB (FACT / VERIFIED).
4. `data/raw/esports_active_matches.csv`: Tệp dữ liệu hoạt động được tạo bởi `sync_google_drive.py` tích hợp bộ 6 giải đấu đỉnh cao (`LCK, LCP, LPL, MSI, WLDS, EWC`) kết hợp ghép đuôi thích ứng (ADR-013). Kích thước: 26.8 MB, 36,000 dòng, đúng **3,000 trận đấu đỉnh cao**: LPL (1,160), LCK (850), LCP (466), EWC (265), MSI (151), WLDS (108). Tỷ lệ có Timeline 10 phút đạt **79.0% (2,369 / 3,000 trận)** (FACT / VERIFIED).
5. `.drive_sync_manifest.json`: Lưu vết thời gian và kích thước file đồng bộ từ Google Drive.

---

## 4. HIỆN TRẠNG MÔI TRƯỜNG THỰC THI (ENVIRONMENT AUDIT)
- **Hệ điều hành:** Windows x64 (FACT).
- **Môi trường ảo cô lập (.venv):** Đã khởi tạo tại thư mục gốc dự án: `d:\Chivinh\2026_MonHoc\Nhập môn khoa học dữ liệu\Project\.venv` (VERIFIED - Python 3.13.14).
- **Cấu hình VS Code:** Đã tạo `.vscode/settings.json` trỏ tự động `python.defaultInterpreterPath` về `.venv`.
- **Các package ĐÃ CÀI ĐẶT ĐẦY ĐỦ TRONG `.venv`:**
  - `pandas == 3.0.6`
  - `numpy == 2.5.3`
  - `scipy == 1.18.1`
  - `scikit-learn == 1.9.1`
  - `matplotlib == 3.11.2`
  - `seaborn == 0.13.2`
  - `gdown == 6.4.0`
  - `requests == 2.34.2`
  - `python-docx == 1.2.0`
  - `jupyter == 1.1.1` & `ipykernel == 7.3.0`
  - `google-api-python-client == 2.200.0`
  - `google-auth-oauthlib == 1.4.1`
  - `google-auth-httplib2 == 0.4.2`
- **Kết nối Riot Games API:**
  - Trạng thái: `VERIFIED - HTTP 200` (Đang hoạt động tốt).
- **Xác thực Google Cloud Drive API v3:**
  - Trạng thái: `VERIFIED - WORKING` (`credentials.json` và `.gdrive_token.json` đã lưu an toàn trong `.gitignore`).

---

## 5. CÁC RỦI RO & VẤN ĐỀ ĐANG TỒN TẠI (KNOWN RISKS)
1. **Google Drive Quota Exceeded:** `[RESOLVED 100%]` Đã khắc phục triệt để bằng cơ chế tải 2 tầng tích hợp Google Drive API v3 (OAuth 2.0 Smart Copy). Đã kiểm thử tải trực tiếp thành công 100% với `--force`.
2. **Dữ liệu đấu giải 2026 chưa vào CSDL:** File đấu giải chuyên nghiệp `esports_active_matches.csv` đã sẵn sàng, cần được ETL vào bảng SQLite `tournament_matches` và `tournament_players` trong `lol_live_data.db` (Task 1.2).
3. **Các thư mục code phân tầng hiện đang trống:** Cần tiếp tục triển khai các module chức năng chính thức trong `src/` theo đúng tiến độ lộ trình đồ án.
