# MODULE 01: RIOT GAMES API DATA PIPELINE

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

## 5. HỆ THỐNG ĐỒNG BỘ GOOGLE DRIVE (SYNC_GOOGLE_DRIVE.PY)

Module [sync_google_drive.py](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/01_data_pipeline/sync_google_drive.py) kết nối trực tiếp với Thư mục Google Drive lưu trữ toàn bộ các mùa giải Oracle's Elixir (2014 - 2026):

### Các lệnh vận hành:
1. **Liệt kê danh mục file trên Drive mà không tải (siêu nhẹ):**
   ```bash
   python src/01_data_pipeline/sync_google_drive.py --list
   ```
2. **Đồng bộ file mùa giải 2026 (mặc định):**
   ```bash
   python src/01_data_pipeline/sync_google_drive.py
   ```
   *(Tự động kiểm tra file local, nếu dung lượng khớp sẽ bỏ qua để tiết kiệm băng thông).*
3. **Bắt buộc tải lại bản cập nhật mới nhất:**
   ```bash
   python src/01_data_pipeline/sync_google_drive.py --force
   ```
4. **Tải file của một năm cụ thể (ví dụ 2024):**
   ```bash
   python src/01_data_pipeline/sync_google_drive.py --year 2024
   ```
5. **Đồng bộ toàn bộ lịch sử 13 năm (2014 - 2026):**
   ```bash
   python src/01_data_pipeline/sync_google_drive.py --all
   ```

---

## 6. CÁC MÃ LỖI THƯỜNG GẶP & CÁCH XỬ LÝ

| Mã lỗi | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **HTTP 403 Forbidden** | Riot API Key đã hết hạn (sau 24h) hoặc nhập sai key. | Vào trang `developer.riotgames.com`, bấm **Regenerate API Key**, dán lại vào `.env`. |
| **HTTP 429 Rate Limit** | Tần suất gọi API vượt quá 100 req/2 phút. | Script sẽ tự động ngủ từ 10 - 120 giây và tự chạy tiếp, không cần can thiệp. |
| **HTTP 404 Not Found** | Trận đấu quá cũ hoặc không có dữ liệu Timeline mốc 10 phút. | Script tự động bỏ qua trận này và chuyển sang trận tiếp theo. |
| **ValueError (.env)** | Chưa có file `.env` hoặc key bị để trống. | Sao chép `.env.example` thành `.env` và điền key hợp lệ. |
