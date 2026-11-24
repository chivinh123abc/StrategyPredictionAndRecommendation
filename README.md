# HỆ THỐNG TRỢ LÝ PHÂN TÍCH CẤM/CHỌN (BAN/PICK AI), DỰ ĐOÁN THẮNG THUA 2 GIAI ĐOẠN & ĐỐI CHIẾU PRO PLAY VS SOLO QUEUE (LMHT)

**Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science) — Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
**Nhóm thực hiện:** Nhóm 3 thành viên

---

## 📌 TRẠNG THÁI HIỆN HÀNH (24/11/2026)

Dự án đi theo **phạm vi vừa sức môn học** ([docs/PHAM_VI_DO_AN_VUA_SUC.md](docs/PHAM_VI_DO_AN_VUA_SUC.md)): vận dụng Chương 1–6 cùng các mở rộng giải thích được. Chỉ duy trì **legacy** và **contextual** cho Ban/Pick (lookahead đã gỡ khỏi runtime/CLI). Điểm xếp hạng là điểm ưu tiên thống kê, không phải xác suất thắng hay bằng chứng counter cơ chế.

| Hạng mục | Trạng thái hiện hành | Tài liệu & Minh chứng |
|---|---|---|
| **Sổ kiến thức báo cáo** | Tổng hợp đầy đủ MH-01..14, MR-01..24, NV-01..24, nguồn & giới hạn | [TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md](docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md) |
| **Chính sách dữ liệu & ML v2** | Làm sạch chung, XGBoost CUDA, calibration & test manifest | [INTEGRITY_V2.md](docs/INTEGRITY_V2.md) · [evaluation_report.md](src/06_machine_learning/evaluation_report.md) |
| **Content-based (Chương 6)** | Item/user profiles, cosine similarity, notebook & benchmark | [CHUONG_6_CONTENT_BASED.md](docs/CHUONG_6_CONTENT_BASED.md) · [content_based_evaluation.md](reports/content_based_evaluation.md) |
| **Ban/Pick & Fearless BO5** | Legacy / Contextual v2, Pair Reservation, Lane Review, First Selection | [BAN_LEGACY_VA_CONTEXTUAL.md](docs/BAN_LEGACY_VA_CONTEXTUAL.md) · [GIU_CAP_BOT_VA_FIRST_SELECTION.md](docs/GIU_CAP_BOT_VA_FIRST_SELECTION.md) |
| **So sánh điểm `current` vs `simple`** | Giữ mặc định `current` (Recall@5 `0.49375` vs `0.425`) | [TINH_GIAN_DIEM_RECOMMENDER.md](docs/TINH_GIAN_DIEM_RECOMMENDER.md) · [REPORT.md](reports/pick_scoring_comparison/REPORT.md) |
| **Giao diện Web local (React/TS + FastAPI)** | 3 cột (Gợi ý \| Đội hình \| Chọn tay), kéo-thả đổi đường, thu gọn giải thích | [UI_REACT_TYPESCRIPT.md](docs/UI_REACT_TYPESCRIPT.md) · [UI_COMPACT_VA_KIEM_KEO_DA_LO.md](docs/UI_COMPACT_VA_KIEM_KEO_DA_LO.md) |
| **Bằng chứng Pro / Rank riêng** | Bảng đối chiếu hai nguồn độc lập, không gộp điểm; Rank collector không quota | [PRO_RANK_MATCHUP_EVIDENCE.md](docs/PRO_RANK_MATCHUP_EVIDENCE.md) · [reports/README.md](reports/README.md) |

> ⚡ **Chạy nhanh Web UI local:** chạy `.\start_ui.ps1` rồi mở `http://127.0.0.1:8000` (nhấn `Ctrl+C` để dừng).  
> ⚡ **Kích hoạt môi trường ảo Python (`.venv`):**
> - **PowerShell:** `.\.venv\Scripts\Activate.ps1`
> - **Command Prompt (CMD):** `.\.venv\Scripts\activate.bat`
> - **Git Bash / Linux:** `source .venv/Scripts/activate`  

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT REPOSITORY LAYOUT)

```text
Project/
├── .venv/                              # Môi trường ảo Python cục bộ (đã cài đủ requirements)
├── .vscode/                            # Cấu hình IDE tự động kích hoạt .venv
├── docs/                               # Tài liệu học tập, giáo trình & kế hoạch đồ án
│   ├── course_slides/                  # Slide bài giảng từ Chương 0 đến Chương 6
│   ├── Dac_Ta_De_Tai_Va_Ke_Hoach_Data_Science_PTIT.docx   # Bản đặc tả Word chính thức
│   ├── DANH_MUC_API_VA_DATASET.md                         # Danh mục API & Dataset tham chiếu
│   └── KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md                # Checklist phân công 3 người
│
├── data/                               # Quản lý dữ liệu phân tầng chuẩn mực
│   ├── raw/                            # Dữ liệu thô ban đầu (File 2026 Pro Play 71 MB từ Drive)
│   ├── processed/                      # Dữ liệu sạch đã qua tiền xử lý, lọc outlier, chuẩn hóa
│   │   └── lol_live_ranked_10min.csv   # Dữ liệu cào Live Rank VN & KR mốc 10 phút
│   └── database/                       # Cơ sở dữ liệu quan hệ SQLite
│       └── lol_live_data.db            # Database chính thức chứa các bảng dữ liệu
│
├── src/                                # Toàn bộ mã nguồn cốt lõi chia theo module
│   ├── config/                         # Cấu hình tập trung (.env, settings, hằng số đường dẫn)
│   ├── 01_data_pipeline/               # Module cào & đồng bộ dữ liệu
│   │   ├── crawl_riot_matches.py       # Crawler cào Live Rank VN & KR mốc phút thứ 10
│   │   ├── sync_google_drive.py        # Tự động phát hiện & đồng bộ mùa giải mới từ Drive
│   │   ├── README.md                   # Trang tổng quan điều hướng Module 01
│   │   ├── README_CRAWL_RIOT.md        # Hướng dẫn chi tiết cào Riot API & chuẩn 1NF/3NF
│   │   └── README_SYNC_DRIVE.md        # Hướng dẫn chi tiết đồng bộ Google Drive
│   ├── 02_preprocessing/               # Module làm sạch, lọc outlier, remakes (Chương 2)
│   ├── 03_database_sql/                # Module CSDL & Truy vấn SQL/Pandas (Chương 5, 5x)
│   ├── 04_hypothesis_testing/          # Module thống kê suy diễn & kiểm định A/B (Chương 1)
│   ├── 05_visualization/               # Module trực quan hóa EDA đa chiều (Chương 3)
│   ├── 06_machine_learning/            # Module ML 2 giai đoạn: Draft & Snowball (Chương 4)
│   ├── 07_recommender/                 # Module Trợ lý Cấm/Chọn Ban/Pick AI (Chương 6)
│   └── api/                            # Backend REST API (FastAPI) kết nối Model AI & CSDL
│
├── web/                                # Giao diện Web App tương tác
├── notebooks/                          # Jupyter Notebooks tương tác (EDA, thử nghiệm mô hình)
├── reports/                            # Báo cáo, slide thuyết trình & biểu đồ xuất bản
│   ├── figures/                        # Hình ảnh biểu đồ PNG độ phân giải cao 300 DPI
│   ├── slides/                         # Slide PowerPoint bảo vệ đồ án
│   └── final_report/                   # Báo cáo tổng kết đồ án Word/PDF
│
├── requirements.txt                    # Danh sách thư viện Python chuẩn mực
├── .env.example                        # File mẫu cấu hình biến môi trường
└── .gitignore                          # Cấu hình bỏ qua file nặng (.venv, .env, raw CSV)
```

---

## 🚀 HƯỚNG DẪN BẮT ĐẦU NHANH (QUICK START)

### 1. Kích hoạt Môi trường Ảo (.venv)
Môi trường ảo `.venv` đã được tạo sẵn tại thư mục gốc. Chạy lệnh kích hoạt tương ứng:
```powershell
# PowerShell:
.\.venv\Scripts\Activate.ps1

# Hoặc Command Prompt:
.\.venv\Scripts\activate.bat
```
*(Nếu cần cài thêm thư viện mới: `pip install -r requirements.txt`).*

---

### 2. Thiết lập Biến môi trường (`.env`)
Sao chép file `.env.example` thành `.env` và điền Riot API Key:
```env
RIOT_API_KEY="RGAPI-your-key-here"
ACTIVE_SERVERS="vn2,kr"
TARGET_MATCHES_PER_SERVER=50
GOOGLE_DRIVE_FOLDER_ID="1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH"
```

---

### 3. Vận hành Pipeline Dữ liệu (Module 01)

Dự án sở hữu 2 nhánh dữ liệu độc lập phục vụ đối chiếu:

#### 🔹 Nhánh A: Cào Dữ Liệu Xếp Hạng Trực Tiếp (Live Solo Queue - Riot API)
Cào các trận đấu Rank Thách Đấu/Cao Thủ thời gian thực tại mốc phút thứ 10:
```bash
python src/01_data_pipeline/crawl_riot_matches.py
```
- **CSDL SQLite:** `data/database/lol_live_data.db` (Bảng `matches_10min` chuẩn 1NF & 3NF).
- **Tệp CSV:** `data/processed/lol_live_ranked_10min.csv`.
- 📖 *Xem hướng dẫn chi tiết:* [`src/01_data_pipeline/README_CRAWL_RIOT.md`](src/01_data_pipeline/README_CRAWL_RIOT.md)

#### 🔹 Nhánh B: Đồng Bộ Dữ Liệu Đấu Giải Chuyên Nghiệp (Pro Play - Google Drive)
Tự động quét và đồng bộ các mùa giải Oracle's Elixir từ Google Drive dùng chung:
```bash
# Tự động đồng bộ các mùa giải mới nhất (Mặc định: 2 mùa gần nhất):
python src/01_data_pipeline/sync_google_drive.py

# Liệt kê danh mục 13 file có sẵn trên Google Drive:
python src/01_data_pipeline/sync_google_drive.py --list
```
- **Dữ liệu thô:** Lưu trữ tại `data/raw/*.csv` (File mùa giải 2026 ~71 MB).
- **Tính năng Future-Proof:** Tự động phát hiện và kéo dữ liệu mùa giải mới (2027...) khi được cập nhật lên Drive.
- 📖 *Xem hướng dẫn chi tiết:* [`src/01_data_pipeline/README_SYNC_DRIVE.md`](src/01_data_pipeline/README_SYNC_DRIVE.md)

---

### 4. Tiền Xử Lý & Làm Sạch Dữ Liệu (Module 02 - Chương 2)
Chạy module lọc bỏ Remake/AFK, xử lý missing values và khử ngoại lai IQR/Z-Score:
```bash
# Tiền xử lý toàn bộ và xuất 4 file dữ liệu sạch:
python src/02_preprocessing/cleaner.py

# Xuất ra data/processed/: clean_ranked_10min.csv, clean_tournament_10min.csv, clean_tournament_draft.csv, clean_tournament_players.csv
```

---

### 5. Thực Thi 5 Truy Vấn SQL Nâng Cao (Module 03 - Chương 5 & 5x)
Thực thi 5 câu truy vấn phân tích chuyên sâu trên CSDL SQLite:
```bash
# Thực thi cả 5 truy vấn và tự động xuất file CSV kết quả:
python src/03_database_sql/execute_queries.py --export

# Thực thi riêng câu truy vấn chỉ định (ví dụ: Q4 Xếp hạng tuyển thủ đè đường):
python src/03_database_sql/execute_queries.py --query 4 --limit 15
```

---

### 6. Kiểm tra Dữ liệu Đã Thu Thập & Làm Sạch
Kiểm tra số lượng bản ghi trận đấu trong SQLite:
```bash
python -c "import sqlite3; conn = sqlite3.connect('data/database/lol_live_data.db'); c = conn.cursor(); c.execute('SELECT count(*) FROM tournament_matches'); print('Trận đấu giải:', c.fetchone()[0]); c.execute('SELECT count(*) FROM matches_10min'); print('Trận Rank:', c.fetchone()[0]); conn.close()"
```

---

## 🧠 CHIẾN LƯỢC KỸ THUẬT & QUẢN TRỊ DỮ LIỆU CỐT LÕI

1. **Chuẩn hóa CSDL đạt chuẩn 1NF & 3NF (Data Normalization):**
   * **Chuẩn 1NF:** Triệt tiêu hoàn toàn các cột gộp chuỗi (`blueChampions`, `redChampions`). Toàn bộ 10 tướng được lưu trữ tại 10 cột nguyên tử tách bạch theo vị trí thi đấu: `blueTop` $\rightarrow$ `blueSupport` và `redTop` $\rightarrow$ `redSupport`.
   * **Chuẩn 3NF (Khử phụ thuộc hàm):** Loại bỏ cột `country` vì phụ thuộc trực tiếp vào `server` (`VN2` $\rightarrow$ `Vietnam`, `KR` $\rightarrow$ `Korea`). Giữ lại duy nhất mã định danh `server` để triệt tiêu dư thừa dữ liệu (khi trực quan hóa EDA chỉ cần ánh xạ nhãn qua dictionary).
2. **Chiến lược dữ liệu Đa máy chủ (Multi-server):**
   * Hỗ trợ cào dữ liệu rank cao song song từ máy chủ Việt Nam (`vn2`) và Hàn Quốc (`kr`).
   * Máy chủ Hàn Quốc (`kr`) đóng vai trò đại diện cho đấu trường Solo Queue đỉnh cao của khu vực Đông Á (nơi các tuyển thủ Trung Quốc LPL và Hàn Quốc LCK cùng thi đấu xếp hạng).
   * Dữ liệu giải đấu chuyên nghiệp Trung Quốc (LPL) được phân tích độc lập thông qua bộ dữ liệu chuẩn hơn 8,800 trận đấu từ **Oracle's Elixir** (`2026_LoL_esports_match_data_from_OraclesElixir.csv`).
3. **Cơ chế xử lý Concept Drift & Học liên tục (Continual Learning):**
   * Đối phó với việc Riot cập nhật bản vá 2 tuần/lần làm thay đổi meta: Áp dụng kỹ thuật kết hợp giữa **Sliding Window** (lọc theo `gameVersion`) và **Exponential Time-Decay Sample Weighting** ($w_i = e^{-\lambda \Delta t}$) khi huấn luyện mô hình Machine Learning.
   * Giúp mô hình luôn ưu tiên cập nhật sức mạnh tướng của meta mới nhất mà không làm giảm kích thước mẫu (sample size).

---

## 👥 PHÂN CÔNG VAI TRÒ NHÓM 3 NGƯỜI

* **Thành viên 1 (Data Engineer, Backend API & Web App Lead):** Phụ trách `src/01_data_pipeline`, `src/02_preprocessing`, `src/03_database_sql` (Chương 2, 5, 5x), đóng gói Backend REST API (FastAPI) và phát triển giao diện Web App tương tác.
* **Thành viên 2 (Data Analyst & Statistician):** Phụ trách `src/04_hypothesis_testing`, `src/05_visualization` (Chương 1, 3 Thống kê A/B & Biểu đồ EDA).
* **Thành viên 3 (AI / Machine Learning Lead):** Phụ trách `src/06_machine_learning`, `src/07_recommender` (Chương 4, 6 Mô hình ML 2 giai đoạn & Ban/Pick AI).

---

## 📚 TÀI LIỆU THAM KHẢO NỘI BỘ

Kho Rank tăng dần hiện hành: [hướng dẫn collector/resume/watch](docs/CONTINUOUS_RANK_EVIDENCE.md), [thống kê đối đầu mới nhất](reports/rank_matchups_live/REPORT.md). Dữ liệu ghi vào `data/database/ranked_evidence.db`, không có trần cố định 1,000 trận hay quota mặc định; `n`, CI và trạng thái sparse được cập nhật theo dữ liệu thật. Không thay đổi mô hình hoặc điểm draft giải.

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --watch --platforms kr --max-requests 600 --max-minutes 15
```

Lệnh chạy trong tiến trình hiện tại cho đến khi dừng hoặc gặp lỗi API terminal, mỗi phiên có ngân sách/rate limit và lưu hàng đợi. Bỏ `--watch` để chạy một phiên; dùng `--export-only` để xuất bảng offline. Chi tiết trạng thái, nghiệm thu và giới hạn xem ở hướng dẫn và sổ kiến thức mục 22 & 25.

* [Mục lục toàn bộ báo cáo & minh chứng (`reports/README.md`)](reports/README.md)
* [Kế hoạch thực hiện đồ án 3 người](docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md)
* [Từ điển Danh mục Hàm & Module toàn dự án (Function Catalog)](docs/DANH_MUC_HAM_VA_MODULES.md)
* [Danh mục API & Dataset](docs/DANH_MUC_API_VA_DATASET.md)
* [Nhật ký thay đổi kỹ thuật (Changelog)](AI/CHANGELOG.md)
