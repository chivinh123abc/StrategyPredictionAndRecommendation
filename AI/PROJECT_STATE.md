# PROJECT STATE (TRẠNG THÁI DỰ ÁN THỰC TẾ)

*Thời điểm audit thực tế:* 2026-09-28  
*Nguồn dữ liệu:* Khảo sát trực tiếp từ mã nguồn, CSDL SQLite, file hệ thống và lệnh `pip list`.

---

## 1. TỔNG QUAN HIỆN TRẠNG
- **Tên dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Môn học chính:** Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT).
- **Môn học mở rộng:** Lập trình trên thiết bị di động (ThS. Nguyễn Trung Hiếu, PTITHCM).
- **Giai đoạn hiện tại:** Đang hoàn tất Giai đoạn 2 (Thống kê suy diễn & Trực quan hóa EDA - Chương 1, 3). Sẵn sàng đóng gói Milestone 2.
- **Đánh giá tiến độ tổng:** ~65% (Hoàn thành 100% Giai đoạn 1 + Hoàn thành 100% Task 2.1, Task 2.2, Task 2.3, Task 2.4).

---

## 2. HIỆN TRẠNG MÃ NGUỒN (SOURCE CODE AUDIT)

| Thư mục / File | Trạng thái thực tế | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| `src/config/` | `VERIFIED - WORKING` | Package cấu hình trung tâm dự án (`settings.py`, `__init__.py`). Nạp `.env`, thẩm định API key, quản lý đường dẫn và metadata. |
| `src/01_data_pipeline/` | `VERIFIED - WORKING` | Gồm `crawl_riot_matches.py`, `sync_google_drive.py` (OAuth 2.0 2 tầng, bộ lọc giải đấu LCK/LCP/LPL/MSI/WLDS/EWC), `load_esports_to_db.py` (ETL nạp CSDL SQLite) và 3 file README đặc tả. |
| `.env` / `.env.example` | `VERIFIED - WORKING` | File cấu hình biến môi trường và file mẫu template an toàn. `.gitignore` đã chặn `.env`. |
| `src/02_preprocessing/` | `VERIFIED - WORKING` | Gồm `cleaner.py` (Domain Filtering Remake/AFK, 5 nhóm Missing Imputation, IQR/Z-Score Outlier Trimming & Winsorization), `__init__.py` và `README.md`. Hoàn thành Task 1.3. |
| `src/03_database_sql/` | `VERIFIED - WORKING` | Gồm `queries.sql` (5 câu truy vấn SQL nâng cao Chương 5 & 5x), `execute_queries.py` (CLI runner tự động xuất 5 file CSV kết quả), `__init__.py` và `README.md`. Hoàn thành Task 1.4. |
| `src/04_hypothesis_testing/` | `VERIFIED - WORKING` | Gồm `test_blue_side_advantage.py` & `.md` (Task 2.1: Z-test lợi thế Phe Xanh), `test_snowball_effect.py` & `.md` (Task 2.2: Two-sample Welch t-test & Z-test Lăn cầu tuyết Pro vs Rank), `test_voidgrubs_vs_dragon.py` & `.md` (Task 2.3: Chi-square & Odds Ratio 3 Sâu vs Rồng 1), `__init__.py` và `README.md`. **Hoàn thành trọn vẹn 3 bài toán Thống kê suy diễn (100% Chương 1)**. |
| `src/05_visualization/` | `VERIFIED - WORKING` | Gồm `plot_eda_figures.py` (Bộ 5 biểu đồ EDA 300 DPI theo Giáo trình Chương 3), `plot_eda_figures.md`, `__init__.py` và `README.md`. Xuất 5 tệp PNG 300 DPI vào `reports/figures/`. Hoàn thành Task 2.4. |
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
- **Số bảng hiện có:** 3 bảng đạt chuẩn 1NF/3NF (FACT / VERIFIED):
  1. `matches_10min`: 1,009 dòng (550 VN2, 459 KR), 42 cột đạt chuẩn 1NF & 3NF.
  2. `tournament_matches`: 6,000 dòng (3,000 trận $\times$ 2 đội Xanh/Đỏ), 155 cột. Khóa chính: `(gameid, side)`.
  3. `tournament_players`: 30,000 dòng (3,000 trận $\times$ 10 tuyển thủ), 129 cột. Khóa chính: `(gameid, participantid)`, Khóa ngoại: `(gameid, side) REFERENCES tournament_matches(gameid, side)`.
- **Tổng số dòng dữ liệu trong DB:** **37,009 dòng** (FACT / VERIFIED).
- **Hệ thống Index tối ưu truy vấn:** 12 indexes đã được tạo tự động cho các trường lọc/nhóm phổ biến (`league, year`, `teamname`, `date`, `patch`, `playername`, `champion`, `position`...).

### Các tệp dữ liệu sạch tại `data/processed/`:
1. `data/processed/clean_ranked_10min.csv`: Dữ liệu Solo Rank sạch mốc 10 phút (977 dòng khi áp dụng filter both IQR/Z-score, 1,009 dòng khi áp dụng capping).
2. `data/processed/clean_tournament_10min.csv`: Dữ liệu Đấu Giải sạch mốc 10 phút (4,636 dòng khi áp dụng filter both, 4,752 dòng khi áp dụng capping).
3. `data/processed/clean_tournament_draft.csv`: Toàn bộ 3,000 trận Đấu Giải sạch (6,000 dòng) phục vụ mô hình Cấm/Chọn.
4. `data/processed/clean_tournament_players.csv`: Dữ liệu 10 vị trí tuyển thủ sạch (28,880 dòng khi áp dụng filter both, 30,000 dòng khi áp dụng capping).
5. `data/processed/lol_live_ranked_10min.csv`: Dữ liệu Rank thô ban đầu (1,009 dòng $\times$ 42 cột).
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
2. **Dữ liệu đấu giải 2026 nạp vào CSDL:** `[RESOLVED 100%]` Đã nạp thành công 6,000 dòng `tournament_matches` và 30,000 dòng `tournament_players` vào `lol_live_data.db` qua `load_esports_to_db.py`.
3. **Các thư mục code phân tầng tiếp theo:** Cần tiếp tục triển khai module làm sạch dữ liệu (`src/02_preprocessing/cleaner.py` - Task 1.3) và 5 truy vấn SQL (`src/03_database_sql/queries.sql` - Task 1.4).

