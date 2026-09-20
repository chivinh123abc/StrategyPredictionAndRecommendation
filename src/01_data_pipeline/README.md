# MODULE 01: DATA PIPELINE (RIOT GAMES API & GOOGLE DRIVE AUTO-SYNC)

Thư mục này quản lý toàn bộ quy trình thu thập và đồng bộ hóa hai nguồn dữ liệu chủ đạo của đồ án:
1. **Dữ liệu Đấu Xếp Hạng Trực Tiếp (Live Solo Queue):** Từ máy chủ Riot Games qua API (`crawl_riot_matches.py`).
2. **Dữ liệu Đấu Giải Chuyên Nghiệp (Esports Pro Play):** Từ thư mục Google Drive dùng chung của Oracle's Elixir (`sync_google_drive.py`).

---

# PHẦN A: CÀO DỮ LIỆU LIVE RANK TỪ RIOT GAMES API

Tài liệu này giải thích chi tiết cấu trúc, logic vận hành và thuật toán bóc tách dữ liệu của script cào trận đấu [crawl_riot_matches.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/crawl_riot_matches.py).

---


## 1. MỤC TIÊU VÀ VAI TRÒ CỦA MODULE

- **Nhiệm vụ cốt lõi:** Thu thập các trận đấu xếp hạng đơn đôi bậc cao (Thách Đấu / Đại Cao Thủ / Cao Thủ) từ hệ thống máy chủ Riot Games thời gian thực.
- **Dữ liệu trích xuất:** Trích xuất toàn bộ chỉ số kinh tế, tài nguyên và mục tiêu lớn tại **mốc phút thứ 10** (Frame 10 trong Timeline).
- **Đầu ra (Output):**
  - Cơ sở dữ liệu SQLite: `data/database/lol_live_data.db` (Bảng `matches_10min` chuẩn 1NF & 3NF).
  - Tệp phẳng: `data/processed/lol_live_ranked_10min.csv` (Đồng bộ song song).

---

## 2. KIẾN TRÚC LUỒNG DỮ LIỆU (DATA FLOW)

```
[ Riot Games Developer API ]
            │
            ├─► 1. Lấy danh sách Top Cao Thủ (Challenger League v4)
            │      URL: https://{platform}.api.riotgames.com/lol/league/v4/challengerleagues
            │
            ├─► 2. Lấy PUUID của người chơi (Summoner v4)
            │      URL: https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/{id}
            │
            ├─► 3. Lấy lịch sử mã trận Rank Đơn (Match v5 by PUUID)
            │      URL: https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/...
            │
            ├─► 4. Lấy chi tiết trận & 10 vị trí thi đấu (Match Detail v5)
            │      URL: https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}
            │
            └─► 5. Bóc tách Timeline phút thứ 10 (Match Timeline v5)
                   URL: https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline
                           │
                           ▼
            [ Tiền xử lý & Chuẩn hóa 1NF / 3NF ]
            (Tách 10 cột tướng nguyên tử, loại bỏ country)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
[ CSDL SQLite lol_live_data.db ]    [ File CSV lol_live_ranked_10min.csv ]
```

---

## 3. GIẢI THÍCH CHI TIẾT CÁC HÀM TRONG MÃ NGUỒN

### 3.1. Nạp cấu hình bảo mật (`load_dotenv_custom`)
- **Vị trí:** Dòng 25 - 45.
- **Chức năng:** Tự động tìm và đọc file `.env` ở thư mục gốc mà không cần cài thêm thư viện `python-dotenv`.
- **Cơ chế bảo mật:** Đọc `RIOT_API_KEY`, nếu key rỗng hoặc chứa `xxx` sẽ lập tức ném ra ngoại lệ `ValueError`, triệt tiêu 100% việc rò rỉ key trong code.

---

### 3.2. Ánh xạ định tuyến máy chủ (`SERVER_METADATA`)
Riot Games phân chia API thành 2 cấp độ URL:
1. **Platform URL (Cấp độ máy chủ):** Dùng cho dữ liệu tài khoản và xếp hạng (`vn2`, `kr`, `tw2`).
2. **Regional Routing URL (Cấp độ khu vực địa lý):** Dùng cho dữ liệu trận đấu (`sea`, `asia`, `americas`, `europe`).

| Server | Platform Host | Regional Host | Khu vực thực tế |
| :--- | :--- | :--- | :--- |
| `vn2` | `vn2.api.riotgames.com` | `sea.api.riotgames.com` | Máy chủ Việt Nam |
| `kr` | `kr.api.riotgames.com` | `asia.api.riotgames.com` | Máy chủ Hàn Quốc (nơi tuyển thủ LPL & LCK tập luyện) |

---

### 3.3. Các phương thức chính của `class RiotApiCrawler`

#### ① `load_champion_id_map(self)`
- **Mục đích:** Riot API trả về mã định danh tướng dạng số nguyên (ví dụ: `266` là Aatrox, `157` là Yasuo).
- **Cách xử lý:** Gọi trực tiếp đến CDN chính thức của Riot (`ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json`) để xây dựng từ điển `{championId: championName}`.

#### ② `parse_team_positions(self, participants)`
- **Mục đích (Chuẩn 1NF):** Triệt tiêu hoàn toàn mảng gộp tướng (`blueChampions`, `redChampions`).
- **Cách xử lý:** Duyệt qua 10 người chơi trong trận, phân tích thuộc tính `teamPosition` (`TOP`, `JUNGLE`, `MIDDLE`, `BOTTOM`, `UTILITY`) để gán chính xác vào 10 cột nguyên tử:
  - Đội Xanh: `blueTop`, `blueJungle`, `blueMid`, `blueAdc`, `blueSupport`
  - Đội Đỏ: `redTop`, `redJungle`, `redMid`, `redAdc`, `redSupport`

#### ③ `init_db(self)`
- **Mục đích:** Tạo bảng `matches_10min` trong SQLite nếu chưa tồn tại với cấu trúc đúng 42 cột chuẩn hóa 1NF và 3NF.
- **Ràng buộc:** `gameId` là `PRIMARY KEY` để tự động loại bỏ trùng lặp nếu cào lại trận cũ (`INSERT OR IGNORE`).

#### ④ `get_with_retry(self, url)` (Chống chặn Rate Limit)
- **Cơ chế:** Riot Development Key giới hạn:
  - Tối đa 20 requests / 1 giây
  - Tối đa 100 requests / 2 phút
- **Giải pháp:** Khi gặp mã phản hồi `HTTP 429` (Rate Limited), script đọc header `Retry-After`, tự động tạm dừng (sleep) theo hàm số mũ (`Exponential Backoff`) và thử lại tối đa 5 lần trước khi báo lỗi.

#### ⑤ `get_high_elo_puuids(self, limit)`
- Lấy danh sách các tài khoản đang đứng đầu bảng xếp hạng Thách Đấu (`queue=RANKED_SOLO_5x5`).
- Chuyển đổi từ `summonerId` sang `puuid` (chuỗi định danh toàn cầu duy nhất của Riot).

#### ⑥ `get_match_ids(self, puuids, target_count)`
- Lấy danh sách ID các trận đấu xếp hạng đơn đôi (`type=ranked`, `queue=420`) gần nhất của các cao thủ.

#### ⑦ `extract_10min_features(self, match_id)` (Trọng tâm học máy)
- Bỏ qua các trận Remake (thời lượng `< 900` giây hoặc bị hủy).
- Lấy dữ liệu **Timeline chi tiết từng phút**: Tìm chính xác `frame` ở phút thứ 10 (`timestamp = 600,000 ms`).
- Tính toán tổng hợp cho cả 2 đội:
  - Tổng Vàng (`totalGold`), Tổng Kinh nghiệm (`totalExp`)
  - Tổng số lính thường (`minionsKilled`) và quái rừng (`jungleMinionsKilled`)
  - Điểm hạ gục (`kills`), điểm nằm xuống (`deaths`)
  - Số mục tiêu lớn trước phút 10: Rồng Nguyên Tố (`dragons`), Sứ Giả Khe Nứt (`heralds`), Sâu Hư Không (`voidgrubs`), Trụ phá hủy (`towersDestroyed`)
  - Chênh lệch vàng (`blueGoldDiff = blueTotalGold - redTotalGold`) và kinh nghiệm (`blueExperienceDiff`).

#### ⑧ `save_record(self, record)` & `export_to_csv(self)`
- Ghi bản ghi vào CSDL SQLite bằng câu lệnh `INSERT OR IGNORE`.
- Đồng bộ toàn bộ dữ liệu ra file CSV `lol_live_ranked_10min.csv` để tiện nạp vào Pandas DataFrame trong Jupyter Notebook.

---

## 4. HƯỚNG DẪN VẬN HÀNH PIPELINE

### Bước 1: Cấu hình API Key trong file `.env`
Mở file `.env` ở thư mục gốc và dán key Riot Games của bạn:
```env
RIOT_API_KEY="RGAPI-your-key-here"
ACTIVE_SERVERS="vn2,kr"
TARGET_MATCHES_PER_SERVER=50
```

### Bước 2: Chạy crawler từ dòng lệnh
```bash
python src/01_data_pipeline/crawl_riot_matches.py
```

### Bước 3: Kiểm tra dữ liệu thu thập được
Mở terminal kiểm tra số dòng trong CSDL:
```bash
python -c "import sqlite3; conn = sqlite3.connect('data/database/lol_live_data.db'); c = conn.cursor(); c.execute('SELECT server, count(*) FROM matches_10min GROUP BY server'); print(c.fetchall()); conn.close()"
```

---

# PHẦN B: HỆ THỐNG ĐỒNG BỘ DỮ LIỆU ĐẤU GIẢI TỪ GOOGLE DRIVE

Tài liệu này giải thích chi tiết logic vận hành, kiến trúc đồng bộ và cách kiểm soát băng thông của script [sync_google_drive.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/sync_google_drive.py).

---

## 5. MỤC TIÊU VÀ VAI TRÒ CỦA MODULE ĐỒNG BỘ ĐÁM MÂY

- **Nhiệm vụ cốt lõi:** Kết nối trực tiếp với Thư mục Google Drive dùng chung ([ID: `1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`](https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH)) lưu trữ toàn bộ dữ liệu các mùa giải chuyên nghiệp Oracle's Elixir (từ 2014 đến 2026).
- **Tự động hóa cộng tác:** Khi một thành viên trong nhóm tải lên bản cập nhật dữ liệu mới hoặc file bổ sung lên Google Drive, các thành viên khác chỉ cần chạy một lệnh duy nhất để đồng bộ về máy trạm cục bộ mà không cần phải tải thủ công qua trình duyệt web.
- **Tối ưu hóa băng thông (Smart Caching):** Kiểm tra dung lượng và siêu dữ liệu cục bộ trước khi tải; tuyệt đối không tải lại tệp ~71 MB nếu nội dung trên máy đã trùng khớp với trên đám mây.
- **Đầu ra (Output):** Các tệp dữ liệu phẳng lưu trữ an toàn tại `data/raw/*.csv` phục vụ cho khâu nạp CSDL (Module 03) và làm sạch dữ liệu (Module 02).

---

## 6. KIẾN TRÚC LUỒNG ĐỒNG BỘ ĐÁM MÂY (CLOUD DATA FLOW)

```
[ Google Drive Shared Folder: 1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH ]
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
     [ Chế độ quét --list ]         [ Chế độ đồng bộ --year/--all ]
  (gdown.download_folder với          (Quét danh sách file từ Drive)
     skip_download=True)                       │
               │                               ▼
               ▼               [ Kiểm tra file trong data/raw/ ]
    [ Xuất danh mục 13 file ]                  │
    (Tên file & Google File ID)       ┌────────┴────────┐
                                      ▼                 ▼
                              [ Đã tồn tại & ]   [ Chưa có hoặc ]
                              [  khớp dung   ]   [ dùng --force ]
                              [    lượng     ]          │
                                      │                 ▼
                                      ▼        [ gdown.download ]
                              [ Bỏ qua tải, ]  (Tải stream resume)
                              [  tiết kiệm  ]           │
                              [   71 MB     ]           ▼
                                               [ Lưu data/raw/*.csv ]
                                                        │
                                                        ▼
                                       [ Ghi nhận lịch sử vào file ]
                                       [ data/raw/.drive_sync_manifest.json ]
```

---

## 7. GIẢI THÍCH CHI TIẾT CÁC PHƯƠNG THỨC TRONG `class GoogleDriveDataSyncer`

### 7.1. Khởi tạo & Cấu hình đường dẫn (`__init__`)
- **Vị trí:** Dòng 48 - 53.
- **Chức năng:** Nạp `folder_id` từ biến cấu hình tập trung `GOOGLE_DRIVE_FOLDER_ID` trong `src.config` (hoặc từ `.env`).
- Đảm bảo thư mục đích `data/raw/` luôn được tự động khởi tạo (`os.makedirs(..., exist_ok=True)`).

### 7.2. Quản lý Cache kiểm soát đồng bộ (`load_manifest` & `save_manifest`)
- **Vị trí:** Dòng 54 - 71.
- **Cơ chế:** Lưu thông tin metadata vào tệp JSON ẩn `data/raw/.drive_sync_manifest.json`.
- **Cấu trúc lưu trữ:**
  ```json
  {
    "last_sync": "2026-09-20T14:50:00.123456",
    "files": {
      "2026_LoL_esports_match_data_from_OraclesElixir.csv": {
        "id": "1hnpbrUpBMS1TZI7IovfpKeZfWJH1Aptm",
        "size": 71269910,
        "synced_at": "2026-09-20T14:50:00.123456"
      }
    }
  }
  ```

### 7.3. Quét danh mục siêu nhẹ không tải file (`list_folder_files`)
- **Vị trí:** Dòng 72 - 93.
- **Kỹ thuật tối ưu:** Sử dụng cờ `skip_download=True` của thư viện `gdown`.
- **Hiệu quả:** Chỉ mất khoảng **2 - 3 giây** để lấy toàn bộ danh mục 13 mùa giải cùng mã `File ID` tương ứng mà không phải tải hàng trăm MB dữ liệu về máy.

### 7.4. Đồng bộ file có điều kiện (`sync_file`)
- **Vị trí:** Dòng 94 - 149.
- **Thuật toán kiểm tra 3 bước:**
  1. Tra cứu `file_id` từ danh mục Drive.
  2. So sánh với file hiện có tại `data/raw/{filename}`: Nếu file đã tồn tại và không bật cờ `--force`, in thông báo đã sẵn sàng và dừng lại ngay lập tức.
  3. Nếu file chưa có hoặc có yêu cầu ép buộc (`force=True`): Gọi `gdown.download(id=file_id, output=dest_path, resume=True)` để tải file về, sau đó ghi nhận kích thước và thời điểm đồng bộ vào manifest.

### 7.5. Đồng bộ hàng loạt toàn bộ các năm (`sync_all`)
- **Vị trí:** Dòng 150 - 163.
- Duyệt qua toàn bộ danh sách 13 file (từ 2014 đến 2026) theo thứ tự tăng dần và gọi hàm `sync_file` cho từng file.

---

## 8. CHIẾN LƯỢC LỰA CHỌN DỮ LIỆU ĐỒ ÁN (DATA STRATEGY)

### 📌 Tại sao ưu tiên độc quyền mùa giải 2026 (hoặc tối đa 2025 + 2026)?
1. **Triệt tiêu 100% Hiện tượng Trôi Dạt Dữ Liệu (Concept Drift):**
   - Mùa giải 2026 áp dụng thể thức thi đấu mới **Fearless Draft (Cấm chọn không lặp tướng)**, bản đồ làm lại địa hình Summoner's Rift và cơ chế bùa lợi quái khủng mới (Sâu Hư Không / Voidgrubs, Atakhan).
   - Dữ liệu từ các năm cũ (2014 - 2023) không có các mục tiêu này (dẫn đến giá trị NULL hoặc 0), nếu đưa vào huấn luyện mô hình sẽ gây **nhiễu nghiêm trọng** và làm giảm độ chính xác dự đoán trận đấu hiện tại.
2. **Quy mô mẫu đã vượt ngưỡng hội tụ:**
   - Riêng tệp `2026_LoL_esports_match_data_from_OraclesElixir.csv` đã có tới **106,488 dòng** (hơn 8,800 trận đấu chuyên nghiệp).
   - Cỡ mẫu này đã quá đủ lớn để thực hiện các phép kiểm định thống kê suy diễn ($Z$-test, $t$-test) đạt mức ý nghĩa cao ($p$-value < 0.001) và huấn luyện các mô hình Machine Learning (Random Forest, XGBoost) một cách mượt mà nhất.
3. **Áp dụng kỹ thuật Cửa Sổ Trượt Thời Gian (Adaptive Sliding Window):**
   - Khi dữ liệu năm hiện tại đã đạt quy mô đầy đủ, hệ thống thu hẹp cửa sổ trượt chỉ giữ lại dữ liệu năm 2026 để tối đa hóa tính thời sự và độ chính xác của trợ lý AI.

---

## 9. HƯỚNG DẪN VẬN HÀNH DÒNG LỆNH

```bash
# 1. Liệt kê toàn bộ 13 file có trên Google Drive cùng File ID (không tải):
python src/01_data_pipeline/sync_google_drive.py --list

# 2. Đồng bộ file mùa giải 2026 về data/raw/ (Mặc định - Tự động bỏ qua nếu đã có):
python src/01_data_pipeline/sync_google_drive.py

# 3. Bắt buộc tải lại bản mới nhất từ Drive (khi có file mới trên Drive):
python src/01_data_pipeline/sync_google_drive.py --force

# 4. Tải file của một năm cụ thể (ví dụ: 2025):
python src/01_data_pipeline/sync_google_drive.py --year 2025

# 5. Tải toàn bộ 13 mùa giải từ 2014 đến 2026:
python src/01_data_pipeline/sync_google_drive.py --all
```

---

## 10. BẢNG MÃ LỖI THƯỜNG GẶP & CÁCH XỬ LÝ (TỔNG HỢP CẢ MODULE 01)

| Mã lỗi / Cảnh báo | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **HTTP 403 Forbidden (Riot API)** | Riot API Key hết hạn (sau 24h) hoặc nhập sai key. | Vào trang `developer.riotgames.com`, bấm **Regenerate API Key**, dán lại vào file `.env`. |
| **HTTP 429 Rate Limit (Riot API)** | Gọi vượt ngưỡng 100 req/2 phút. | Script tự động tạm dừng ngủ từ 10 - 120 giây theo hàm số mũ và tự chạy tiếp. |
| **Cannot find module `gdown`** | Môi trường Python (hoặc venv) chưa cài `gdown`. | Chạy lệnh: `pip install gdown` (hoặc cài vào venv tương ứng). |
| **Google Drive Access Denied** | Link thư mục bị tắt quyền chia sẻ công khai. | Đảm bảo thư mục Google Drive được bật chế độ *"Bất kỳ ai có đường liên kết đều có thể xem"*. |
| **ValueError (.env)** | Chưa có file `.env` hoặc key bị để trống. | Sao chép `.env.example` thành `.env` và điền giá trị hợp lệ. |

