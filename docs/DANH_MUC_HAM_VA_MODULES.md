# TỪ ĐIỂN DANH MỤC HÀM, CLASS & MODULE TOÀN BỘ DỰ ÁN (FUNCTION & API CATALOG)

> **Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science) - PTIT  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Môi trường thực thi:** Python 3.13 (`.venv`)  
> **Cập nhật lần cuối:** 2026-09-28 (Hoàn thành Milestone 1)

---

## 📑 MỤC LỤC ĐIỀU HƯỚNG NHANH

1. [Module `src/config/` (Quản trị Cấu hình & Biến Môi trường)](#1-module-srcconfig-quản-trị-cấu-hình--biến-môi-trường)
2. [Module `src/01_data_pipeline/` (Thu Thập & Đồng Bộ Dữ Liệu)](#2-module-src01_data_pipeline-thu-thập--đồng-bộ-dữ-liệu)
   - [Script `crawl_riot_matches.py` (Cào Live Rank từ Riot API)](#21-script-crawl_riot_matchespy-cào-live-rank)
   - [Script `sync_google_drive.py` (Đồng bộ Đám mây Google Drive)](#22-script-sync_google_drivepy-đồng-bộ-đám-mây)
   - [Script `load_esports_to_db.py` (ETL Nạp CSDL SQLite)](#23-script-load_esports_to_dbpy-etl-nạp-csdl-sqlite)
3. [Module `src/02_preprocessing/` (Tiền Xử Lý & Khử Ngoại Lai - Chương 2)](#3-module-src02_preprocessing-tiền-xử-lý--khử-ngoại-lai---chương-2)
   - [Class `DataCleaner`](#31-class-datacleaner-src02_preprocessingcleanerpy)
4. [Module `src/03_database_sql/` (Truy Vấn SQL Nâng Cao - Chương 5 & 5x)](#4-module-src03_database_sql-truy-vấn-sql-nâng-cao---chương-5--5x)
   - [Class `SQLQueryRunner`](#41-class-sqlqueryrunner-src03_database_sqlexecute_queriespy)
   - [Danh mục 5 Câu Truy Vấn trong `queries.sql`](#42-danh-mục-5-truy-vấn-sql-trong-queriessql)
5. [Bảng Tra Cứu Nhanh Tất Cả Các Hàm (Cheat Sheet)](#5-bảng-tra-cứu-nhanh-tất-cả-các-hàm-cheat-sheet)

---

## 1. MODULE `src/config/` (QUẢN TRỊ CẤU HÌNH & BIẾN MÔI TRƯỜNG)

Package quản trị tập trung toàn bộ đường dẫn, API Key, thiết lập máy chủ và metadata hệ thống.

* **File:** [`src/config/settings.py`](../src/config/settings.py) & [`src/config/__init__.py`](../src/config/__init__.py)

### 📌 Danh Sách Hàm

#### `load_dotenv_custom(env_path: Path) -> dict`
* **Mô tả:** Đọc và nạp các biến môi trường từ tệp `.env` một cách an toàn mà không làm rò rỉ secret key ra bên ngoài.
* **Tham số:** `env_path` (*Path*): Đường dẫn đến tệp `.env`.
* **Trả về:** `dict`: Từ điển các cặp key-value biến môi trường đã nạp.

#### `get_active_esports_season() -> str`
* **Mô tả:** Tự động phát hiện mùa giải Esports mới nhất có trong thư mục `data/raw/` dựa trên định dạng tên tệp `YYYY_LoL_esports_match_data_from_OraclesElixir.csv`.
* **Trả về:** `str`: Chuỗi năm mùa giải mới nhất (ví dụ: `"2026"`).

#### `get_active_esports_file() -> Path`
* **Mô tả:** Xác định đường dẫn tệp dữ liệu giải đấu hoạt động ưu tiên:
  1. Nếu tồn tại `data/raw/esports_active_matches.csv` (tệp đã qua bộ lọc 6 giải đấu và ghép mẫu thích ứng) $\rightarrow$ Ưu tiên trả về.
  2. Nếu không, tự động trỏ về tệp mùa giải mới nhất `data/raw/{latest_year}_LoL_esports_...csv`.
* **Trả về:** `Path`: Đường dẫn tệp CSV hoạt động chuẩn xác.

### 📌 Các Hằng Số Toàn Cục (Global Constants)
* `BASE_DIR`: Thư mục gốc của toàn bộ dự án (`Path`).
* `DATA_DIR`, `RAW_DATA_DIR`, `PROCESSED_DATA_DIR`, `DATABASE_DIR`: Các thư mục dữ liệu phân tầng.
* `OUTPUT_DB`: Đường dẫn CSDL SQLite chính thức (`data/database/lol_live_data.db`).
* `RIOT_API_KEY`: Khóa API Riot Games Developer lấy từ `.env`.
* `ACTIVE_SERVERS`: Danh sách máy chủ cào rank (`['vn2', 'kr']`).
* `ESPORTS_TARGET_LEAGUES`: Danh sách 6 giải đấu mục tiêu (`['LCK', 'LCP', 'LPL', 'MSI', 'WLDS', 'EWC']`).

---

## 2. MODULE `src/01_data_pipeline/` (THU THẬP & ĐỒNG BỘ DỮ LIỆU)

### 2.1. Script `crawl_riot_matches.py` (Cào Live Rank)
* **File:** [`src/01_data_pipeline/crawl_riot_matches.py`](../src/01_data_pipeline/crawl_riot_matches.py)

#### 🏛️ Class `RiotApiCrawler`

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(api_key, platform)` | `api_key: str`, `platform: str` | `None` | Khởi tạo crawler cho từng máy chủ (`vn2`, `kr`), thiết lập `requests.Session` và ánh xạ khu vực định tuyến. |
| `load_champion_id_map()` | Không | `dict` | Tải bảng ánh xạ `ChampionID -> ChampionName` từ Riot Data Dragon CDN mới nhất để dịch ID số sang tên tướng. |
| `parse_team_positions(participants)` | `participants: list` | `tuple(list, list)` | Tự động phân tích và gán chính xác 5 vị trí thi đấu (TOP, JNG, MID, ADC, SUP) cho 2 đội dựa trên `individualPosition` và phép suy luận bổ trợ. |
| `init_db()` | Không | `None` | Khởi tạo bảng `matches_10min` trong SQLite với đúng 42 cột chuẩn hóa 1NF và 3NF nếu chưa tồn tại. |
| `get_with_retry(url)` | `url: str` | `dict \| None` | Gửi HTTP request kèm cơ chế tự động tạm dừng (Exponential Backoff) khi gặp Rate Limit HTTP 429 (`Retry-After`). |
| `get_high_elo_puuids(limit)` | `limit: int = 100` | `list[str]` | Lấy danh sách định danh PUUID của các tuyển thủ Thách Đấu / Cao Thủ trên máy chủ chỉ định. |
| `get_match_ids(puuids, target_count)` | `puuids: list`, `target_count: int` | `list[str]` | Thu thập danh sách mã trận đấu xếp hạng đơn đôi (`queueId = 420`), tự động loại trừ các trận đã có trong DB. |
| `extract_10min_features(match_id)` | `match_id: str` | `dict \| None` | Gửi request lấy Timeline trận đấu, định vị `frame[10]` (mốc $600,000\text{ ms}$) bóc tách toàn bộ chỉ số vàng, kinh nghiệm, lính, rồng, sâu hư không, trụ. |
| `save_record(record)` | `record: dict` | `None` | Lưu bản ghi trận đấu vào bảng `matches_10min` trong SQLite ngay khi bóc tách xong để chống mất dữ liệu. |
| `export_to_csv()` | Không | `None` | Xuất toàn bộ bảng `matches_10min` từ SQLite ra tệp `data/processed/lol_live_ranked_10min.csv`. |
| `backfill_missing_champions()` | Không | `None` | Hàm bổ trợ tự động quét lại các trận cũ để điền bổ sung lượt Cấm và 10 tướng theo 5 lane nguyên tử. |
| `run_for_server(target_matches)` | `target_matches: int` | `None` | Hàm điều phối chạy toàn bộ luồng cào cho 1 server cụ thể đến khi đủ số lượng yêu cầu. |

---

### 2.2. Script `sync_google_drive.py` (Đồng Bộ Đám Mây)
* **File:** [`src/01_data_pipeline/sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py)

#### 🏛️ Class `GoogleDriveDataSyncer`

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(folder_id)` | `folder_id: str = None` | `None` | Khởi tạo bộ đồng bộ đám mây, nạp manifest cache `.drive_sync_manifest.json`. |
| `load_manifest()` | Không | `dict` | Đọc lịch sử đồng bộ cục bộ để kiểm tra kích thước file, tránh tải lại file nặng 71 MB trùng lặp. |
| `save_manifest(manifest)` | `manifest: dict` | `None` | Lưu vết thời gian và kích thước file sau khi đồng bộ thành công. |
| `list_folder_files(force_refresh)` | `force_refresh: bool` | `list[dict]` | Quét danh mục siêu nhẹ 13 mùa giải (2014-2026) trên Google Drive mà không tải dữ liệu nặng. |
| `get_available_years()` | Không | `list[str]` | Quét regex `^(\d{4})_LoL_...csv` trích xuất danh sách các năm mùa giải có trên Drive. |
| `count_matches(filepath, leagues)` | `filepath: str`, `leagues: list` | `int` | Đếm số lượng trận đấu độc lập (`unique gameid`) trong file CSV có hỗ trợ lọc theo danh sách giải đấu. |
| `sync_smart_latest(min_matches, leagues, force)` | `min_matches: int = 3000`, `leagues: list`, `force: bool` | `Path \| None` | **Thuật toán mùa giải thông minh (ADR-013):** Tự động tải năm mới nhất; nếu chưa đủ 3,000 trận thuộc 6 giải đấu lớn, tự động kích hoạt ghép mẫu thích ứng. |
| `build_adaptive_dataset(latest_year, previous_year, min_matches, leagues)` | `latest_year: str`, `previous_year: str`, `min_matches: int`, `leagues: list` | `Path` | **Ghép dữ liệu thích ứng:** Lấy toàn bộ năm mới + trích xuất phần cuối năm trước (CKTG / Mùa Hè) tạo thành `data/raw/esports_active_matches.csv` (đúng 3,000 trận). |
| `sync_file(filename, force)` | `filename: str`, `force: bool` | `Path \| None` | Tải một file cụ thể từ Google Drive về `data/raw/` bằng cơ chế tải 2 tầng chống Quota Exceeded. |
| `filter_leagues(input_file, output_file, leagues)` | `input_file: str`, `output_file: str`, `leagues: list` | `Path` | Lọc file CSV giải đấu theo danh sách giải chỉ định và lưu ra file đích. |
| `check_data_health(filepath)` | `filepath: str` | `dict` | Kiểm tra tính toàn vẹn dữ liệu: cấu trúc 12 dòng/trận, tỷ lệ missing value mốc 10 phút, xuất Data Health Card. |

#### 🌐 Các Hàm Độc Lập Ở Cấp Module (Module-level Functions)
* `_get_gdrive_service() -> Resource`: Xác thực OAuth 2.0 Desktop App và khởi tạo Google Drive API v3 client.
* `_download_via_api(file_id, dest_path, filename) -> bool`: Tải file qua Google Drive API bằng thuật toán Smart Copy (nhân bản tạm vào My Drive rồi xóa).
* `parse_leagues(leagues_input) -> list[str]`: Chuẩn hóa danh sách giải đấu truyền từ CLI thành list chữ hoa.
* `filter_esports_by_leagues(input_file, output_file, leagues) -> Path`: Hàm tiện ích gọi nhanh bộ lọc giải đấu từ bất kỳ script nào.
* `check_esports_data_health(filepath) -> dict`: Hàm tiện ích kiểm tra sức khỏe dữ liệu nhanh từ bên ngoài.

---

### 2.3. Script `load_esports_to_db.py` (ETL Nạp CSDL SQLite)
* **File:** [`src/01_data_pipeline/load_esports_to_db.py`](../src/01_data_pipeline/load_esports_to_db.py)

#### 🏛️ Class `EsportsDatabaseLoader`

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(source_csv, db_path)` | `source_csv: str`, `db_path: str` | `None` | Khởi tạo ETL loader, tự động trỏ đến tệp hoạt động `esports_active_matches.csv` và CSDL `lol_live_data.db`. |
| `load_and_clean_data()` | Không | `tuple(DataFrame, DataFrame)` | Đọc CSV, chuẩn hóa tên cột `snake_case`, tách thành 2 tập: `matches_df` (6,000 dòng) và `players_df` (30,000 dòng). |
| `create_schema(conn, matches_df, players_df, force)` | `conn`, `matches_df`, `players_df`, `force: bool` | `None` | Tạo cấu trúc 2 bảng với Khóa chính `(gameid, side)` cho matches, `(gameid, participantid)` cho players và Khóa ngoại liên kết. |
| `insert_dataframe(conn, table_name, df, batch_size)` | `conn`, `table_name: str`, `df: DataFrame`, `batch_size: int = 1000` | `int` | Nạp dữ liệu vào SQLite theo lô bằng câu lệnh `INSERT OR REPLACE` tối ưu hóa bộ nhớ. |
| `create_indexes(conn)` | `conn` | `None` | Tạo 14 Composite Indexes tối ưu hóa tốc độ cho các câu truy vấn SQL ở Module 03. |
| `run_validation(conn)` | `conn` | `dict` | Chạy bộ kiểm thử tự động kiểm tra số lượng bản ghi, tỷ lệ timeline 10p, và chạy thử query phân tích. |
| `run(force, verify_only)` | `force: bool`, `verify_only: bool` | `bool` | Thực thi toàn bộ pipeline ETL từ đầu đến cuối. |

#### 🌐 Các Hàm Độc Lập Ở Cấp Module
* `sanitize_column_name(col: str) -> str`: Chuyển đổi tên cột bất kỳ thành định dạng hợp lệ cho SQL (`snake_case`, thay ký tự lạ bằng `_`).
* `infer_sqlite_type(series: pd.Series) -> str`: Tự động suy luận kiểu dữ liệu SQLite (`INTEGER`, `REAL`, `TEXT`) từ kiểu dữ liệu của Pandas Series.

---

## 3. MODULE `src/02_preprocessing/` (TIỀN XỬ LÝ & KHỬ NGOẠI LAI - CHƯƠNG 2)

* **File:** [`src/02_preprocessing/cleaner.py`](../src/02_preprocessing/cleaner.py)

### 3.1. Class `DataCleaner`

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(db_path, output_dir, outlier_method, outlier_action, z_thresh, iqr_multiplier)` | Các tham số cấu hình thuật toán | `None` | Khởi tạo pipeline làm sạch, thiết lập thuật toán ngoại lai (`iqr`, `zscore`, `both`), cơ chế (`trim`, `cap`). |
| `detect_outliers_iqr(df, column)` | `df: DataFrame`, `column: str` | `Series(bool), tuple(float, float)` | Phát hiện ngoại lai theo IQR ($Q_1 - 1.5 \times IQR$, $Q_3 + 1.5 \times IQR$). Trả về mặt nạ boolean và biên chặn. |
| `detect_outliers_zscore(df, column)` | `df: DataFrame`, `column: str` | `Series(bool), tuple(float, float)` | Phát hiện ngoại lai theo Z-Score ($|Z| > 3.0$). Trả về mặt nạ boolean và biên chặn tương ứng. |
| `handle_outliers(df, columns, dataset_name)` | `df: DataFrame`, `columns: list[str]`, `dataset_name: str` | `DataFrame` | Áp dụng lọc bỏ (Trimming) hoặc cắt ngọn (Winsorization/Capping) trên các cột chênh lệch kinh tế. |
| `clean_ranked_data(df_raw)` | `df_raw: DataFrame` | `DataFrame` | Làm sạch dữ liệu Solo Rank: Khử Remake (< 10p), AFK ($CS < 10$), xử lý missing và khử ngoại lai `blueGoldDiff`. |
| `clean_tournament_matches(df_raw)` | `df_raw: DataFrame` | `tuple(DataFrame, DataFrame)` | Làm sạch dữ liệu Đấu Giải cấp Đội: Tách luồng `clean_tournament_10min.csv` (có timeline) và `clean_tournament_draft.csv` (3,000 trận cấm chọn). |
| `clean_tournament_players(df_raw)` | `df_raw: DataFrame` | `DataFrame` | Làm sạch dữ liệu Tuyển thủ 1v1: Khử Remake/AFK, điền missing mục tiêu, khử ngoại lai `golddiffat10` cá nhân. |
| `print_cleaning_report()` | Không | `None` | In Báo Cáo Kiểm Định Chất Lượng Làm Sạch (Data Cleaning Card) so sánh trước/sau khi lọc. |
| `run()` | Không | `dict[str, Path]` | Thực thi toàn bộ quy trình tiền xử lý và lưu 4 tệp CSV sạch vào `data/processed/`. |

---

## 4. MODULE `src/03_database_sql/` (TRUY VẤN SQL NÂNG CAO - CHƯƠNG 5 & 5x)

* **File:** [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py) & [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql)

### 4.1. Class `SQLQueryRunner`

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(db_path)` | `db_path: Path = OUTPUT_DB` | `None` | Khởi tạo runner, nạp 5 câu truy vấn SQL từ tệp `queries.sql`. |
| `run_query(query_id, limit)` | `query_id: int (1..5)`, `limit: int = None` | `DataFrame` | Thực thi một câu truy vấn SQL theo ID và trả về kết quả dưới dạng Pandas DataFrame. |
| `display_query(query_id, limit, export)` | `query_id: int`, `limit: int`, `export: bool` | `DataFrame` | In bảng kết quả truy vấn ra terminal đẹp mắt kèm giải thích nghiệp vụ và xuất CSV nếu có cờ `--export`. |
| `run_all(limit, export)` | `limit: int = 10`, `export: bool = True` | `dict[int, DataFrame]` | Thực thi tuần tự toàn bộ 5 câu truy vấn SQL và xuất 5 file CSV vào `data/processed/`. |

#### 🌐 Hàm Độc Lập Ở Cấp Module
* `extract_queries_from_sql_file(filepath: Path) -> dict[int, dict]`: Bóc tách 5 câu SQL từ tệp `queries.sql` dựa trên thẻ tag đánh dấu `-- !QUERY_X_START` và `-- !QUERY_X_END`.

### 4.2. Danh Mục 5 Truy Vấn SQL trong `queries.sql`

1. **Truy vấn 1 (Kèo đối đầu 1v1 - Lane Matchup):** `Self-JOIN` bảng `tournament_players` qua `gameid`, `position`, `side = 'Blue'` vs `'Red'`, `GROUP BY`, `HAVING` $\rightarrow$ Thống kê đối đầu trực tiếp, tỷ lệ thắng và chênh lệch vàng/lính lúc 10 phút để tìm Counter-Pick.
2. **Truy vấn 2 (Cặp đôi ăn ý đường dưới - Bot Synergy Duo):** `Intra-team JOIN` (Bot + Sup cùng phe), `GROUP BY`, `HAVING COUNT(*) >= 10` $\rightarrow$ Thống kê 125 tổ hợp Xạ thủ + Hỗ trợ ăn ý nhất giải đấu.
3. **Truy vấn 3 (Tướng có Presence Rate cao nhất):** `CTE (Common Table Expressions)`, `Subqueries`, `Unpivot UNION ALL` 5 lượt cấm, `FULL OUTER JOIN` $\rightarrow$ Tính Presence Rate = $\frac{\text{Picks} + \text{Bans}}{\text{Total Games}}$.
4. **Truy vấn 4 (Tuyển thủ đè đường phút 10):** `Window Functions: DENSE_RANK() OVER (PARTITION BY position ORDER BY avg_gold_diff_10 DESC)` & `AVG() OVER (PARTITION BY position)` $\rightarrow$ Xếp hạng tuyển thủ đè đường tốt nhất và so sánh Benchmark.
5. **Truy vấn 5 (Đối chiếu Lăn cầu tuyết: Đấu Giải vs Rank):** `UNION ALL`, phân tầng `CASE WHEN` chênh lệch vàng 10 phút, `GROUP BY` $\rightarrow$ So sánh khả năng chuyển hóa lợi thế vàng thành chiến thắng giữa Pro Play và Solo Queue.

---

## 5. MODULE `src/04_hypothesis_testing/` (THỐNG KÊ SUY DIỄN & KIỂM ĐỊNH GIẢ THUYẾT - CHƯƠNG 1)

* **File:** [`src/04_hypothesis_testing/test_blue_side_advantage.py`](../src/04_hypothesis_testing/test_blue_side_advantage.py)

### 5.1. Class `BlueSideHypothesisTester` (Task 2.1 - Kiểm định Lợi thế Phe Xanh)

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(db_path, alpha)` | `db_path: Path = OUTPUT_DB`, `alpha: float = 0.05` | `None` | Khởi tạo tester, tính toán ngưỡng $Z_{critical} = \Phi^{-1}(1 - \alpha/2) \approx \pm 1.96$. |
| `compute_z_test(wins, total, name)` | `wins: int`, `total: int`, `name: str` | `dict` | Tính toán tỷ lệ mẫu $\hat{p}$, sai số chuẩn $SE_0$, giá trị $Z$-score, $p$-value 2 phía và Khoảng tin cậy 95%. |
| `run_tests()` | Không | `DataFrame` | Thực thi kiểm định đồng thời trên 3 phân vùng: Pro Play (3,000 trận), Solo Rank (1,009 trận), và 6 giải đấu riêng biệt. |
| `display_report(df_results, export)` | `df_results: DataFrame`, `export: bool = True` | `None` | Xuất Báo Cáo Kiểm Định Giả Thuyết Thống Kê (Report Card) và lưu file `data/processed/hypothesis_test_1_blue_side.csv`. |

---

### 5.2. Class `SnowballHypothesisTester` (Task 2.2 - Kiểm định Lăn Cầu Tuyết Đấu Giải vs Rank)
* **File:** [`src/04_hypothesis_testing/test_snowball_effect.py`](../src/04_hypothesis_testing/test_snowball_effect.py)

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(db_path, alpha, lead_gold)` | `db_path: Path`, `alpha: float = 0.05`, `lead_gold: int = 2000` | `None` | Khởi tạo tester, cấu hình mốc dẫn vàng $\ge 2,000$g lúc 10 phút. |
| `load_data()` | Không | `tuple[DataFrame, DataFrame]` | Trích xuất các trận đấu có đội dẫn vàng lúc 10 phút từ CSDL SQLite (`tournament_matches` & `matches_10min`). |
| `test_winrate_difference(df_pro, df_rank)` | `df_pro: DataFrame`, `df_rank: DataFrame` | `dict` | **Two-sample Z-test:** So sánh tỷ lệ chuyển hóa chiến thắng (Winrate Conversion) giữa Pro Play và Solo Rank. |
| `test_duration_difference(df_pro, df_rank)` | `df_pro: DataFrame`, `df_rank: DataFrame` | `dict` | **Two-sample Welch's t-test:** So sánh thời lượng kết thúc trận đấu trung bình giữa Đấu Giải và Solo Rank. |
| `test_variance_stability(df_pro, df_rank)` | `df_pro: DataFrame`, `df_rank: DataFrame` | `dict` | **Levene's Variance Test:** Kiểm định phương sai đo lường tính ổn định, biến động và kỷ luật trận đấu. |
| `run_multi_tier_analysis()` | Không | `DataFrame` | Phân tích kiểm định so sánh phân tầng theo 4 mốc vàng dẫn trước (+1000g, +1500g, +2000g, +3000g). |
| `display_report(export)` | `export: bool = True` | `None` | In Báo Cáo Kiểm Định Giả Thuyết Lăn Cầu Tuyết và xuất file `data/processed/hypothesis_test_2_snowball.csv`. |

---

### 5.3. Class `ObjectiveHypothesisTester` (Task 2.3 - Kiểm định Chi-Square & Odds Ratio Mục Tiêu Lớn)
* **File:** [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py)

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(db_path, alpha)` | `db_path: Path`, `alpha: float = 0.05` | `None` | Khởi tạo tester kiểm định Chi-square và Odds Ratio cho mục tiêu trung lập phút 10. |
| `load_data()` | Không | `tuple[DataFrame, DataFrame]` | Trích xuất dữ liệu mục tiêu lớn lúc 10 phút (`void_grubs`, `firstdragon`, `result`) từ Pro Play và Solo Rank. |
| `compute_contingency_stats(df, feature_col)` | `df: DataFrame`, `feature_col: str` | `dict` | Tính bảng chéo 2x2, Chi-square (χ²), p-value, Odds Ratio (OR), CI 95% (Woolf logit) và Relative Risk (RR). |
| `compute_scenario_matrix(df)` | `df: DataFrame` | `DataFrame` | Phân tích ma trận 4 kịch bản đối đầu kiểm soát mục tiêu (Ăn Cả Hai, Chỉ 3 Sâu, Chỉ Rồng 1, Mất Cả Hai). |
| `compute_8_combination_matrix(df)` | `df: DataFrame` | `DataFrame` | Phân tích ma trận 8 tổ hợp chi tiết: [Có/Mất Rồng 1] x [0, 1, 2, 3 Sâu]. |
| `analyze_head_to_head_split_grubs()` | Không | `dict` | Khảo sát đối đầu trực tiếp cùng trận: Kèo (1 Rồng + 1 Sâu) vs (0 Rồng + 2 Sâu) trên 370 trận Pro. |
| `run_tests()` | Không | `dict` | Thực thi toàn bộ kiểm định Chi-square và Odds Ratio trên cả 2 môi trường. |
| `display_report(export)` | `export: bool = True` | `None` | Xuất Báo Cáo Phân Tích Mục Tiêu Lớn và lưu file `data/processed/hypothesis_test_3_objectives.csv`. |

---

## 6. MODULE `src/05_visualization/` (TRỰC QUAN HÓA DỮ LIỆU EDA - CHƯƠNG 3)

* **File:** [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py)

### 6.1. Class `EDAPlotter` (Task 2.4 - Bộ 5 Biểu Đồ EDA 300 DPI)

| Tên Phương Thức (Method) | Tham Số | Giá Trị Trả Về | Mô Tả Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `__init__(db_path, output_dir, dpi)` | `db_path`, `output_dir`, `dpi = 300` | `None` | Khởi tạo bộ sinh đồ họa, cấu hình Seaborn theme và Matplotlib typography. |
| `load_data()` | Không | `tuple[DataFrame, DataFrame, DataFrame]` | Trích xuất 3 tập dữ liệu phục vụ vẽ hình: Pro Matches, Rank Matches, Pro Players. |
| `plot_fig1_correlation_heatmap()` | Không | `Path` | **Fig 1 (Heatmap):** Ma trận tương quan Pearson giữa các chỉ số 10p và biến Thắng/Thua (thang đo `[-1.0, +1.0]`). |
| `plot_fig2_gold_diff_distribution()` | Không | `Path` | **Fig 2 (KDE/Hist):** Phân phối chênh lệch vàng phút 10 theo Thắng vs Thua (Pro vs Rank). |
| `plot_fig3_lane_economy_boxplot()` | Không | `Path` | **Fig 3 (Boxplot):** Phân bố chênh lệch vàng 10p theo 5 vị trí thi đấu (Top, Jng, Mid, Bot, Sup). |
| `plot_fig4_gold_lead_vs_duration_scatter()` | Không | `Path` | **Fig 4 (Scatter + Reg):** Tương quan giữa Vàng dẫn trước 10p và Thời lượng trận đấu (Mốc 20p Baron vs 15p FF15). |
| `plot_fig5_neutral_objectives_scenarios()` | Không | `Path` | **Fig 5 (Grouped Bar 2 Subplots):** Ma trận 8 tổ hợp mục tiêu lớn (Rồng 1 x 0, 1, 2, 3 Sâu) đối chiếu Pro vs Rank. |
| `plot_all()` | Không | `dict[str, Path]` | Tự động xuất trọn bộ 5 file ảnh PNG 300 DPI vào thư mục `reports/figures/`. |

---

### 6.2. Thư Mục Tài Liệu Giải Thích Biểu Đồ (`docs/figure_explain/`)

Hệ thống tài liệu giải thích chi tiết 5 biểu đồ phục vụ nghiên cứu khoa học và bảo vệ đồ án:
* [`fig1_correlation_heatmap.md`](figure_explain/fig1_correlation_heatmap.md): Giải thích ma trận tương quan Pearson, Colorbar, tại sao đường chéo = 1, phân biệt hệ số r vs tỷ lệ thắng %.
* [`fig2_gold_diff_distribution.md`](figure_explain/fig2_gold_diff_distribution.md): Giải thích phân phối hình chuông KDE, độ lệch tâm (+1,250g vs -1,250g), so sánh Pro vs Rank.
* [`fig3_lane_economy_boxplot.md`](figure_explain/fig3_lane_economy_boxplot.md): Giải thích Boxplot 5 vị trí, IQR từng đường, tính đối xứng gương qua 0 và điểm ngoại lai.
* [`fig4_gold_lead_vs_duration.md`](figure_explain/fig4_gold_lead_vs_duration.md): Giải thích Scatter Plot hồi quy OLS, hiệu ứng Snowball, ranh giới 20p Baron vs 15p FF15, các trận 11-13p.
* [`fig5_neutral_objectives_scenarios.md`](figure_explain/fig5_neutral_objectives_scenarios.md): Giải thích 8 tổ hợp mục tiêu (Rồng 1 x 0, 1, 2, 3 Sâu), hiệu ứng bảo hiểm > 50% của Rồng 1, kèo chia sâu 1R+1S vs 0R+2S.
* [`README.md`](figure_explain/README.md): Mục lục tra cứu và lệnh xuất ảnh.

---

## 7. BẢNG TRA CỨU NHANH TẤT CẢ CÁC HÀM (CHEAT SHEET)

| Tên Hàm / Phương Thức | Nằm Tại File | Module / Class | Mục Đích Chính |
| :--- | :--- | :--- | :--- |
| `get_active_esports_file()` | `src/config/settings.py` | `src.config` | Xác định file CSV giải đấu hoạt động ưu tiên |
| `get_active_esports_season()` | `src/config/settings.py` | `src.config` | Phát hiện mùa giải mới nhất trong `data/raw/` |
| `load_champion_id_map()` | `src/01_data_pipeline/crawl_riot_matches.py` | `RiotApiCrawler` | Tải ánh xạ ID $\rightarrow$ Tên tướng từ CDN |
| `extract_10min_features()` | `src/01_data_pipeline/crawl_riot_matches.py` | `RiotApiCrawler` | Bóc tách timeline phút 10 từ Riot API |
| `sync_smart_latest()` | `src/01_data_pipeline/sync_google_drive.py` | `GoogleDriveDataSyncer` | Tải mùa mới & tự động ghép mẫu thích ứng |
| `build_adaptive_dataset()` | `src/01_data_pipeline/sync_google_drive.py` | `GoogleDriveDataSyncer` | Ghép năm 2026 + cuối 2025 thành 3,000 trận |
| `filter_esports_by_leagues()` | `src/01_data_pipeline/sync_google_drive.py` | Module Function | Lọc dữ liệu theo 6 giải đấu lớn |
| `check_esports_data_health()` | `src/01_data_pipeline/sync_google_drive.py` | Module Function | Kiểm tra sức khỏe và độ sạch dữ liệu |
| `load_and_clean_data()` | `src/01_data_pipeline/load_esports_to_db.py` | `EsportsDatabaseLoader` | Tách 6,000 dòng matches & 30,000 dòng players |
| `create_indexes()` | `src/01_data_pipeline/load_esports_to_db.py` | `EsportsDatabaseLoader` | Tạo 14 chỉ mục tối ưu hóa tốc độ SQL |
| `detect_outliers_iqr()` | `src/02_preprocessing/cleaner.py` | `DataCleaner` | Phát hiện ngoại lai bằng thuật toán IQR |
| `detect_outliers_zscore()` | `src/02_preprocessing/cleaner.py` | `DataCleaner` | Phát hiện ngoại lai bằng thuật toán Z-Score |
| `handle_outliers()` | `src/02_preprocessing/cleaner.py` | `DataCleaner` | Lọc bỏ (Trim) hoặc cắt ngọn (Cap) ngoại lai |
| `clean_ranked_data()` | `src/02_preprocessing/cleaner.py` | `DataCleaner` | Tiền xử lý dữ liệu Solo Rank 10 phút |
| `clean_tournament_matches()` | `src/02_preprocessing/cleaner.py` | `DataCleaner` | Tiền xử lý dữ liệu Đấu Giải cấp Đội tuyển |
| `clean_tournament_players()` | `src/02_preprocessing/cleaner.py` | `DataCleaner` | Tiền xử lý dữ liệu Tuyển thủ 1v1 mốc 10 phút |
| `run_query()` | `src/03_database_sql/execute_queries.py` | `SQLQueryRunner` | Chạy 1 câu truy vấn SQL theo ID |
| `run_all()` | `src/03_database_sql/execute_queries.py` | `SQLQueryRunner` | Chạy cả 5 câu SQL và xuất 5 file CSV |
| `compute_z_test()` | `src/04_hypothesis_testing/test_blue_side_advantage.py` | `BlueSideHypothesisTester` | Tính Z-score, p-value 2 phía & CI 95% |
| `run_tests()` | `src/04_hypothesis_testing/test_blue_side_advantage.py` | `BlueSideHypothesisTester` | Chạy Z-test trên Pro Play, Rank & Leagues |
| `test_winrate_difference()` | `src/04_hypothesis_testing/test_snowball_effect.py` | `SnowballHypothesisTester` | Two-sample Z-test tỷ lệ thắng khi dẫn vàng |
| `test_duration_difference()` | `src/04_hypothesis_testing/test_snowball_effect.py` | `SnowballHypothesisTester` | Two-sample Welch t-test thời lượng trận |
| `test_variance_stability()` | `src/04_hypothesis_testing/test_snowball_effect.py` | `SnowballHypothesisTester` | Levene's test kiểm định phương sai & ổn định |
| `run_multi_tier_analysis()` | `src/04_hypothesis_testing/test_snowball_effect.py` | `SnowballHypothesisTester` | Kiểm định phân tầng 4 mốc chênh lệch vàng |
| `compute_contingency_stats()`| `src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`| `ObjectiveHypothesisTester` | Tính Chi-square (χ²), Odds Ratio & 95% CI |
| `compute_scenario_matrix()` | `src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`| `ObjectiveHypothesisTester` | Phân tích 4 kịch bản đối đầu mục tiêu lớn |
| `plot_all()` | `src/05_visualization/plot_eda_figures.py` | `EDAPlotter` | Tự động xuất bộ 5 biểu đồ EDA 300 DPI |
