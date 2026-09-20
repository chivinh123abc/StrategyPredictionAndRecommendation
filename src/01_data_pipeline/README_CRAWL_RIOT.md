# HƯỚNG DẪN MODULE: CÀO DỮ LIỆU LIVE RANK TỪ RIOT GAMES API

> **Tệp mã nguồn:** [`crawl_riot_matches.py`](crawl_riot_matches.py)  
> **Mục tiêu:** Thu thập dữ liệu trận đấu xếp hạng đơn đôi bậc cao (Thách Đấu / Đại Cao Thủ / Cao Thủ) thời gian thực từ hệ thống máy chủ Riot Games.

---

## 1. MỤC TIÊU VÀ VAI TRÒ CỦA PIPELINE

- **Nhiệm vụ cốt lõi:** Kết nối trực tiếp với cổng lập trình viên Riot Games API để cào dữ liệu các trận đấu xếp hạng đơn đôi cấp cao nhất tại máy chủ Việt Nam (`vn2`) và Hàn Quốc (`kr`).
- **Dữ liệu trích xuất trọng tâm:** Trích xuất toàn bộ chỉ số kinh tế, tài nguyên và mục tiêu lớn tại **mốc phút thứ 10** (Frame 10 trong Timeline trận đấu) để phục vụ bài toán dự đoán tỷ lệ thắng sớm.
- **Đầu ra (Output):**
  - **Cơ sở dữ liệu SQLite:** `data/database/lol_live_data.db` (Bảng `matches_10min` chuẩn 1NF & 3NF).
  - **Tệp phẳng CSV:** `data/processed/lol_live_ranked_10min.csv` (Đồng bộ song song để tiện nạp Pandas DataFrame).

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
- **Chức năng:** Tự động tìm và đọc file `.env` ở thư mục gốc mà không cần cài thêm thư viện phụ trợ `python-dotenv`.
- **Cơ chế bảo mật:** Đọc `RIOT_API_KEY`, nếu key rỗng hoặc chứa chuỗi giữ chỗ mặc định (`xxx`) sẽ lập tức dừng chương trình và ném ra ngoại lệ `ValueError`, triệt tiêu 100% rủi ro rò rỉ key bí mật khi đẩy code lên Git.

---

### 3.2. Ánh xạ định tuyến máy chủ (`SERVER_METADATA`)
Riot Games phân chia API thành 2 cấp độ URL độc lập:
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
- **Cách xử lý:** Gọi trực tiếp đến CDN Data Dragon của Riot (`ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json`) để xây dựng từ điển ánh xạ `{championId: championName}`.

#### ② `parse_team_positions(self, participants)`
- **Mục đích (Chuẩn 1NF):** Triệt tiêu hoàn toàn mảng gộp tướng dạng danh sách (`blueChampions`, `redChampions`).
- **Cách xử lý:** Duyệt qua 10 người chơi trong trận, phân tích thuộc tính `teamPosition` (`TOP`, `JUNGLE`, `MIDDLE`, `BOTTOM`, `UTILITY`) để gán chính xác vào 10 cột nguyên tử:
  - Đội Xanh: `blueTop`, `blueJungle`, `blueMid`, `blueAdc`, `blueSupport`
  - Đội Đỏ: `redTop`, `redJungle`, `redMid`, `redAdc`, `redSupport`

#### ③ `init_db(self)`
- **Mục đích:** Tạo bảng `matches_10min` trong SQLite nếu chưa tồn tại với cấu trúc đúng 42 cột chuẩn hóa 1NF và 3NF.
- **Ràng buộc toàn vẹn:** `gameId` là `PRIMARY KEY` để tự động loại bỏ trùng lặp nếu cào lại trận cũ (`INSERT OR IGNORE`).

#### ④ `get_with_retry(self, url)` (Cơ chế chống chặn Rate Limit)
- **Cơ chế giới hạn của Riot:** Riot Development Key giới hạn:
  - Tối đa 20 requests / 1 giây
  - Tối đa 100 requests / 2 phút
- **Giải pháp xử lý:** Khi gặp mã phản hồi `HTTP 429` (Rate Limited), script đọc header `Retry-After`, tự động tạm dừng (sleep) theo hàm số mũ (`Exponential Backoff`) và thử lại tối đa 5 lần trước khi báo lỗi.

#### ⑤ `get_high_elo_puuids(self, limit)`
- Lấy danh sách các tài khoản đang đứng đầu bảng xếp hạng Thách Đấu (`queue=RANKED_SOLO_5x5`).
- Chuyển đổi từ `summonerId` sang `puuid` (chuỗi định danh toàn cầu duy nhất của Riot).

#### ⑥ `get_match_ids(self, puuids, target_count)`
- Lấy danh sách ID các trận đấu xếp hạng đơn đôi (`type=ranked`, `queue=420`) gần nhất của các cao thủ.

#### ⑦ `extract_10min_features(self, match_id)` (Trọng tâm trích xuất đặc trưng)
- Bỏ qua các trận Remake (thời lượng `< 900` giây hoặc trận bị hủy).
- Lấy dữ liệu **Timeline chi tiết từng phút**: Tìm chính xác `frame` ở phút thứ 10 (`timestamp = 600,000 ms`).
- Tính toán tổng hợp cho cả 2 đội:
  - Tổng Vàng (`totalGold`), Tổng Kinh nghiệm (`totalExp`)
  - Tổng số lính thường (`minionsKilled`) và quái rừng (`jungleMinionsKilled`)
  - Điểm hạ gục (`kills`), điểm nằm xuống (`deaths`)
  - Số mục tiêu lớn trước phút 10: Rồng Nguyên Tố (`dragons`), Sứ Giả Khe Nứt (`heralds`), Sâu Hư Không (`voidgrubs`), Trụ phá hủy (`towersDestroyed`)
  - Chênh lệch vàng (`blueGoldDiff = blueTotalGold - redTotalGold`) và kinh nghiệm (`blueExperienceDiff`).

#### ⑧ `save_record(self, record)` & `export_to_csv(self)`
- Ghi bản ghi vào CSDL SQLite bằng câu lệnh `INSERT OR IGNORE`.
- Đồng bộ toàn bộ dữ liệu ra file CSV `lol_live_ranked_10min.csv` để phục vụ phân tích EDA và huấn luyện mô hình.

---

## 4. HƯỚNG DẪN VẬN HÀNH DÒNG LỆNH

### Bước 1: Cấu hình API Key trong file `.env`
Mở file `.env` ở thư mục gốc dự án và dán key Riot Games của bạn:
```env
RIOT_API_KEY="RGAPI-your-key-here"
ACTIVE_SERVERS="vn2,kr"
TARGET_MATCHES_PER_SERVER=50
```

### Bước 2: Chạy crawler từ terminal
```bash
python src/01_data_pipeline/crawl_riot_matches.py
```

### Bước 3: Kiểm tra dữ liệu thu thập được
Kiểm tra số dòng trong SQLite:
```bash
python -c "import sqlite3; conn = sqlite3.connect('data/database/lol_live_data.db'); c = conn.cursor(); c.execute('SELECT server, count(*) FROM matches_10min GROUP BY server'); print(c.fetchall()); conn.close()"
```

---

## 5. BẢNG MÃ LỖI THƯỜNG GẶP & CÁCH XỬ LÝ

| Mã lỗi / Cảnh báo | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **HTTP 403 Forbidden** | Riot API Key hết hạn (sau 24h đối với Dev Key) hoặc nhập sai key. | Vào trang `developer.riotgames.com`, bấm **Regenerate API Key**, dán lại vào file `.env`. |
| **HTTP 429 Rate Limit** | Gọi vượt ngưỡng 100 requests / 2 phút. | Script tự động ngủ từ 10 - 120 giây theo hàm số mũ và tự động thử lại, không cần can thiệp. |
| **ValueError (.env)** | Chưa có file `.env` hoặc `RIOT_API_KEY` bị để trống/chứa `xxx`. | Sao chép `.env.example` thành `.env` và điền key hợp lệ. |
| **HTTP 404 Not Found** | Trận đấu quá cũ hoặc không tồn tại Timeline. | Script tự động bỏ qua trận này và chuyển sang trận tiếp theo. |
