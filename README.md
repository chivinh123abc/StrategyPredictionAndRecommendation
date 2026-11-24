> **UI mới gọn và kiểm kèo đã lộ:** thiết lập trên đầu; gợiý trái/chọntay phải; giải thích dưới. Chọn tay tự xếp đường phổ biến nhất còn trống, kéo thả đổi đường. Galio0mẫuvsAmbessa không autochốt; cùngrolexétWilsonlowerbound,Renekton2/2đượchiệnđúngn/CIvàlêntop2trongcaseđãaudit. CLI nhiềuván bắtbuộc`--first-picks`,choBluehoặcRedcả5. [Hướngdẫn](docs/UI_COMPACT_VA_KIEM_KEO_DA_LO.md),[minhchứng178tests/5Edge](reports/ui_lane_revision/REPORT.md). Tảilạihttp://127.0.0.1:8000/Phiênmớinếucần.

> **Giữ cặp bot + chọn trước từngván:** contextualpickđãkiểmtrapartnerpooltrướcbansđểtránhcaseNautilus→điTop→mấthếtADCđủmẫu. Scorecurrentgiữnguyên,lýdoưu tiênriêng;khôngnhậncặptốiưu. UIchọnBlue/Redđitrướcmỗiván,khôngtựluânphiên;CLI`--first-picks red,red,blue,blue,red`. [Phươngpháp](docs/GIU_CAP_BOT_VA_FIRST_SELECTION.md), [regression/BO5/minhchứng](reports/pair_reservation_revision/REPORT.md).170tests/3EdgePASS. Tảilại http://127.0.0.1:8000 vàPhiênmới nếu fingerprintcũkhôngkhớp.

> **UI hiện hành — hai khu riêng/contextual v2:** Gợiý và Chọntay đồnghiện, confirmriêng. ThanhcấuhìnhhiệnBan/Pick/ngày/mãsnapshot; đổi nguồn/config khônglặnglẽtrộnkếtquả. Contextual sửa utilitypoolítbackup;80banstates cùngpool giảm31probe bất nhất→0 nhưngRecall5banlịchsửkhôngtăng, chưaclaimchiếnthuậttốthơn.159tests/2EdgePASS. [Báocáo](reports/contextual_ui_revision/REPORT.md), [cáchdùng](docs/UI_REACT_TYPESCRIPT.md). Chạy `.\start_ui.ps1`, mở http://127.0.0.1:8000.

> **UI React + TypeScript đã chạy (24/11):** `.\start_ui.ps1` rồi mở **http://127.0.0.1:8000**. [Cài đặt và cách dùng](docs/UI_REACT_TYPESCRIPT.md), [ảnh và kiểm tra](reports/ui_demo/REPORT.md). Ban/pick tay hoặc gợi ý, flex, undo, lịch sử, Fearless tối đa5ván, Pro/Rank riêng, lưu phiên và xuất JSON.154Python tests và browserEdgePASS. Bản này phục vụ Pro draft, Rank là bằng chứng; chưa có UI Rank riêng hoặc tối ưu toànBO5.

> **Thử tinh giản điểm pick24/11:** [rà8thành phần và công thức đơn giản](docs/TINH_GIAN_DIEM_RECOMMENDER.md), [so sánh520lượt chọn](reports/pick_scoring_comparison/REPORT.md), [BO5T1–Gen.G đủ100lượt ban/pick và lý do](reports/simple_scoring_bo5/REPORT.md). Simple giảm Recall@5 test từ49.375% xuống42.5%, nên default vẫncurrent; explicit `--pick-scoring simple` chỉ để demo/so sánh.146tests vàintegrationPASS. Kiến thức/phần giữ-bỏ/output ởsổmục26.

> **Phạm vi hiện hành24/11:** đồ án vừa sức Chương1–6 và một số mở rộng giải thích được. [Phạm vi cốt lõi/phần phụ và đánh giá hiện trạng](docs/PHAM_VI_DO_AN_VUA_SUC.md). Giữ demo legacy/contextual/Fearless; không bắt buộc nghiên cứu toànBO5 hoặc Web/API đầy đủ. Đã bỏ quota mặc định2.000trận/kèo; U.GG reference chưa nạp, không nhận đã ngang số mẫu.139testsPASS ởmốctrước; collector khôngquota, PID/log hiện hành ở reports/rank_matchups_live/collector_process.json.

> **Mốc trước — bằng chứng Pro/Rank:** đã xuất thống kê từ3.000trận Pro, thêm bảng hai nguồn ở gợi ý/`why N`, không thay điểm chính. [Cách chạy và giới hạn](docs/PRO_RANK_MATCHUP_EVIDENCE.md), [ví dụ](reports/pro_rank_explanations/REPORT.md), [thử nghiệm](reports/contextual_rank_experiment/REPORT.md).138testsPASS tại mốc đó; thử nghiệm thăm dò chưa cải thiện, đánh giá độc lập chờ dữ liệu giải sau freeze.

> **Hiện hành24/11: chỉ legacy và contextual.** Lookahead đã gỡ khỏi code/CLI. Hai chế độ đều được chạy kiểm tra đủ5draftT1–Gen.G;57testsPASS ở mốc cũ. [Phương pháp/lệnhchạy](docs/BAN_LEGACY_VA_CONTEXTUAL.md). Những mô tảsearch phía dưới là lịch sử trước quyết định này.

> **24/11 — sửa tự chọn thiếu căn cứ:** auto dừng chờreview khi địch đã lộ5và pick không có đối đầu đủ mẫu, lưu alternatives/completefalse; không xác nhậncounter. [Phạm viTrundle, kết quả và lệnh chạy](docs/RA_SOAT_LUA_CHON_THEO_DOI_HINH.md). 51testsPASS; dừng phát triển tiếp theo yêu cầu người dùng.

> **Tài liệu dùng viết báo cáo:** [Tổng hợp kiến thức từng chương, phần mở rộng, nơi sử dụng và file kết quả](docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md). Có phân biệt rõ chức năng đã có với mục tiêu tính trước đối thủ/để dành tướng/tối ưu BO5 chưa hiện thực.

> **5ván Worlds Fearless:** chạy `.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py`. Đã validate100lượt,50picks khác nhau, khóa0/10/20/30/40,38testsPASS. Không gán kết quả game. [Ban/pick đầy đủ](reports/worlds_fearless_bo5/REPORT.md).

> **Draft Worlds và phối hợp toàn đội:** đã thêm association cho mọi cặp role, counts/CI và ma trận10cặp/đội; không gán cứng combo theo tên. 35 tests PASS, 2 phiên Worlds20lượt; audit200lượt Recall@5=36% so với baseline30%, chưa là final test hoặc bằng chứng tăng thắng. [Kết quả và lệnh chạy](docs/WORLDS_ROLE_PAIR_REVIEW.md).

> **Minh chứng Chương 6:** đã bổ sung content-based item/user profiles + cosine; đã kiểm chứng (16 tests, notebook 6 cell mã, CLI/engine PASS). Xem [hướng dẫn](docs/CHUONG_6_CONTENT_BASED.md).

> **Cập nhật 2026-11-23 — Integrity v2:** Dự án vẫn theo lộ trình triển khai. Phần dữ liệu, đánh giá và gợi ý đã được sửa theo [chính sách hiện hành](docs/INTEGRITY_V2.md). Dùng [báo cáo ML mới](src/06_machine_learning/evaluation_report.md) và [benchmark recommender](reports/recommender_evaluation.json); số liệu/đích accuracy trong phần kế hoạch cũ bên dưới không phải kết quả nghiệm thu. Điểm xếp hạng không phải xác suất. Pro chưa có timeline mục tiêu phút 10; rank chưa có event timestamp.

# HỆ THỐNG TRỢ LÝ PHÂN TÍCH CẤM/CHỌN (BAN/PICK AI), DỰ ĐOÁN THẮNG THUA SỚM 2 GIAI ĐOẠN & ĐỐI CHIẾU CHIẾN THUẬT ĐẤU GIẢI (PRO PLAY) VS ĐẤU XẾP HẠNG (SOLO QUEUE) TRONG ESPORTS LIÊN MINH HUYỀN THOẠI

> ⚡ **KÍCH HOẠT MÔI TRƯỜNG ẢO (.venv) TRƯỚC KHI CHẠY:**
> - **PowerShell:** `.\.venv\Scripts\Activate.ps1`
> - **Command Prompt (CMD):** `.\.venv\Scripts\activate.bat`
> - **Git Bash / Linux:** `source .venv/Scripts/activate`
> *(Trong VS Code, môi trường `.venv` đã được cấu hình tự động nhận diện tại `.vscode/settings.json`).*

---

**Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science) - Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
**Nhóm sinh viên thực hiện:** Nhóm 3 thành viên  

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

Kho Rank tăng dần hiện hành: [hướng dẫn collector/resume/watch](docs/CONTINUOUS_RANK_EVIDENCE.md), [thống kê đối đầu mới nhất](reports/rank_matchups_live/REPORT.md). Dữ liệu ghi vào `data/database/ranked_evidence.db`, không có trần tổng1.000trận; n/CI và sparse status được cập nhật theo dữ liệu thật. Không thay đổi mô hình hoặc điểm draft giải.

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --watch --platforms kr --max-requests 600 --max-minutes 15
```

Lệnh chạy trong tiến trình hiện tại cho đến khi dừng hoặc lỗi API terminal, mỗi phiên có ngân sách/rate limit và lưu hàng đợi. Bỏ `--watch` để chạy một phiên; dùng `--export-only` để xuất bảng offline. Chi tiết trạng thái/nghiệmthu/giới hạn ở hướng dẫn, sổ kiến thức mục22.

* [Kế hoạch thực hiện đồ án 3 người](docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md)
* [Từ điển Danh mục Hàm & Module toàn dự án (Function Catalog)](docs/DANH_MUC_HAM_VA_MODULES.md)
* [Danh mục API & Dataset](docs/DANH_MUC_API_VA_DATASET.md)
* [Nhật ký thay đổi kỹ thuật (Changelog)](AI/CHANGELOG.md)
