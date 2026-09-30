# DATABASE SPECIFICATION & SCHEMA DICTIONARY

*Công nghệ:* SQLite 3  
*Đường dẫn tệp:* `data/database/lol_live_data.db`  
*Tiêu chuẩn thiết kế:* Chuẩn hóa dữ liệu 1NF và 3NF.

---

## 1. BẢNG HIỆN HỮU: `matches_10min`
Bảng lưu trữ thông số các trận đấu Solo Rank cao (Thách Đấu / Kim Cương) được cào từ Riot Games API mốc 10 phút.

### Cấu trúc 42 Cột Chi Tiết:

| Nhóm | Tên Cột | Kiểu dữ liệu | Ràng buộc | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- | :--- |
| **Định danh** | `gameId` | TEXT | PRIMARY KEY | Mã định danh trận đấu duy nhất của Riot (vd: `VN2_12345678`) |
| | `gameVersion` | TEXT | NOT NULL | Phiên bản bản vá của game (vd: `14.5.1`) |
| | `gameDuration` | INTEGER | NOT NULL | Tổng thời lượng trận đấu thực tế (tính bằng giây) |
| | `crawled_at` | TEXT | NOT NULL | Dấu thời gian cào dữ liệu (ISO format) |
| | `server` | TEXT | NOT NULL | Mã máy chủ cào (`VN2` hoặc `KR`) |
| **Mục tiêu chính**| `blueWins` | INTEGER | NOT NULL | Kết quả chung cuộc: `1` = Đội Xanh thắng, `0` = Đội Đỏ thắng |
| **Kinh tế Đội Xanh**| `blueTotalGold` | INTEGER | NOT NULL | Tổng lượng vàng Đội Xanh kiếm được tại phút thứ 10 |
| | `blueTotalExperience` | INTEGER | NOT NULL | Tổng kinh nghiệm Đội Xanh tích lũy tại phút 10 |
| | `blueTotalMinionsKilled`| INTEGER | NOT NULL | Tổng số lính thường Đội Xanh tiêu diệt tại phút 10 |
| | `blueTotalJungleMinionsKilled` | INTEGER | NOT NULL | Tổng số quái rừng Đội Xanh tiêu diệt tại phút 10 |
| | `blueKills` | INTEGER | NOT NULL | Tổng số mạng hạ gục của Đội Xanh lúc 10 phút |
| | `blueDeaths` | INTEGER | NOT NULL | Tổng số lần nằm xuống của Đội Xanh lúc 10 phút |
| | `blueDragons` | INTEGER | NOT NULL | Số Rồng Nguyên Tố Đội Xanh ăn được trước phút 10 |
| | `blueHeralds` | INTEGER | NOT NULL | Số Sứ Giả Khe Nứt Đội Xanh ăn được trước phút 10 |
| | `blueVoidgrubs`| INTEGER | NOT NULL | Số Sâu Hư Không Đội Xanh ăn được trước phút 10 |
| | `blueTowersDestroyed` | INTEGER | NOT NULL | Số trụ Đội Xanh phá được trước phút 10 |
| | `blueGoldDiff` | INTEGER | NOT NULL | Chênh lệch vàng (`blueTotalGold - redTotalGold`) |
| | `blueExperienceDiff` | INTEGER | NOT NULL | Chênh lệch kinh nghiệm (`blueTotalExp - redTotalExp`) |
| **Kinh tế Đội Đỏ** | `redTotalGold` | INTEGER | NOT NULL | Tổng lượng vàng Đội Đỏ kiếm được tại phút 10 |
| | `redTotalExperience` | INTEGER | NOT NULL | Tổng kinh nghiệm Đội Đỏ tích lũy tại phút 10 |
| | `redTotalMinionsKilled` | INTEGER | NOT NULL | Tổng số lính thường Đội Đỏ tiêu diệt tại phút 10 |
| | `redTotalJungleMinionsKilled` | INTEGER | NOT NULL | Tổng số quái rừng Đội Đỏ tiêu diệt tại phút 10 |
| | `redKills` | INTEGER | NOT NULL | Tổng số mạng hạ gục của Đội Đỏ lúc 10 phút |
| | `redDeaths` | INTEGER | NOT NULL | Tổng số lần nằm xuống của Đội Đỏ lúc 10 phút |
| | `redDragons` | INTEGER | NOT NULL | Số Rồng Nguyên Tố Đội Đỏ ăn được trước phút 10 |
| | `redHeralds` | INTEGER | NOT NULL | Số Sứ Giả Khe Nứt Đội Đỏ ăn được trước phút 10 |
| | `redVoidgrubs` | INTEGER | NOT NULL | Số Sâu Hư Không Đội Đỏ ăn được trước phút 10 |
| | `redTowersDestroyed` | INTEGER | NOT NULL | Số trụ Đội Đỏ phá được trước phút 10 |
| | `redGoldDiff` | INTEGER | NOT NULL | Chênh lệch vàng (`redTotalGold - blueTotalGold`) |
| | `redExperienceDiff` | INTEGER | NOT NULL | Chênh lệch kinh nghiệm (`redTotalExp - blueTotalExp`) |
| **Cấm / Chọn (1NF)**| `blueTop` | TEXT | | Tên tướng Đội Xanh đi đường Trên |
| | `blueJungle` | TEXT | | Tên tướng Đội Xanh đi Rừng |
| | `blueMid` | TEXT | | Tên tướng Đội Xanh đi đường Giữa |
| | `blueAdc` | TEXT | | Tên tướng Đội Xanh Xạ Thủ |
| | `blueSupport` | TEXT | | Tên tướng Đội Xanh Hỗ Trợ |
| | `redTop` | TEXT | | Tên tướng Đội Đỏ đi đường Trên |
| | `redJungle` | TEXT | | Tên tướng Đội Đỏ đi Rừng |
| | `redMid` | TEXT | | Tên tướng Đội Đỏ đi đường Giữa |
| | `redAdc` | TEXT | | Tên tướng Đội Đỏ Xạ Thủ |
| | `redSupport` | TEXT | | Tên tướng Đội Đỏ Hỗ Trợ |
| | `blueBans` | TEXT | | Chuỗi danh sách các tướng Đội Xanh cấm |
| | `redBans` | TEXT | | Chuỗi danh sách các tướng Đội Đỏ cấm |

---

---

## 2. BẢNG HIỆN HỮU: `tournament_matches`
Bảng lưu trữ thông số cấp độ trận đấu và đội tuyển (Team Level) từ dữ liệu giải đấu chuyên nghiệp (Oracle's Elixir), gồm 6 giải đấu hàng đầu (`LCK, LCP, LPL, MSI, WLDS, EWC`).
- **Quy mô thực tế:** 6,000 dòng (3,000 trận đấu độc lập $\times$ 2 phe Xanh / Đỏ).
- **Khóa chính (Primary Key):** `(gameid, side)`
- **Số lượng cột:** 155 cột (đã loại bỏ các cột rỗng cấp cá nhân và chuẩn hóa snake_case).
- **Các nhóm chỉ số chính:**
  - *Định danh & Bối cảnh:* `gameid`, `league`, `year`, `split`, `playoffs`, `date`, `game`, `patch`, `participantid` (100=Blue, 200=Red), `side`, `teamname`, `teamid`.
  - *Cấm / Chọn (Draft Phase):* `firstPick`, `ban1`..`ban5`, `pick1`..`pick5`.
  - *Kết quả & Giao tranh:* `gamelength`, `result` (1=Win, 0=Loss), `kills`, `deaths`, `assists`, `teamkills`, `teamdeaths`, `doublekills`..`pentakills`, `firstblood`, `team_kpm`, `ckpm`.
  - *Mục tiêu lớn:* `firstdragon`, `dragons`, `opp_dragons`, `elementaldrakes`, `elders`, `firstherald`, `heralds`, `void_grubs`, `opp_void_grubs`, `firstbaron`, `barons`, `atakhans`, `firsttower`, `towers`, `turretplates`, `inhibitors`.
  - *Sát thương & Tầm nhìn:* `damagetochampions`, `dpm`, `damagetakenperminute`, `damagemitigatedperminute`, `damagetotowers`, `wardsplaced`, `wpm`, `wardskilled`, `wcpm`, `controlwardsbought`, `visionscore`, `vspm`.
  - *Kinh tế & Lính:* `totalgold`, `earnedgold`, `earned_gpm`, `goldspent`, `minionkills`, `monsterkills`, `cspm`.
  - *Chỉ số Timeline mốc 10 phút:* `goldat10`, `xpat10`, `csat10`, `opp_goldat10`, `opp_xpat10`, `opp_csat10`, `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`, `assistsat10`, `deathsat10`, `opp_killsat10`, `opp_assistsat10`, `opp_deathsat10`.
  - *Chỉ số Timeline mốc 15, 20, 25 phút:* `goldat15`..`goldat25`, `golddiffat15`..`golddiffat25`,...

---

## 3. BẢNG HIỆN HỮU: `tournament_players`
Bảng lưu trữ thông số chi tiết của từng tuyển thủ chuyên nghiệp thi đấu ở 5 vị trí (`top`, `jng`, `mid`, `bot`, `sup`).
- **Quy mô thực tế:** 30,000 dòng (3,000 trận đấu độc lập $\times$ 10 tuyển thủ).
- **Khóa chính (Primary Key):** `(gameid, participantid)` (với `participantid` từ 1..10).
- **Khóa ngoại (Foreign Key):** `FOREIGN KEY (gameid, side) REFERENCES tournament_matches(gameid, side) ON DELETE CASCADE`.
- **Số lượng cột:** 129 cột.
- **Các nhóm chỉ số chính:**
  - *Định danh tuyển thủ:* `gameid`, `participantid`, `side`, `position`, `playername`, `playerid`, `teamname`, `teamid`, `champion`.
  - *Hiệu suất cá nhân:* `kills`, `deaths`, `assists`, `firstbloodkill`, `firstbloodassist`, `damagetochampions`, `dpm`, `damageshare`, `earnedgoldshare`, `total_cs`, `cspm`.
  - *Chỉ số đối đầu cá nhân mốc 10 phút:* `goldat10`, `xpat10`, `csat10`, `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`, `deathsat10`, `assistsat10`.

---

## 4. QUY TẮC CHUẨN HÓA ĐÃ ĐƯỢC CHỨNG MINH
1. **Chuẩn 1NF (Tính nguyên tử):**
   - Không dùng mảng ghép hay chuỗi ghép tướng cho đội hình. Toàn bộ 10 vị trí thi đấu trong Rank được tách thành 10 cột nguyên tử độc lập (`blueTop`..`blueSupport`, `redTop`..`redSupport`).
   - Trong dữ liệu giải đấu, mỗi tuyển thủ là 1 dòng độc lập trong `tournament_players`, liên kết với cấp trận qua `gameid`.
2. **Chuẩn 3NF (Khử phụ thuộc hàm bắc cầu):**
   - Loại bỏ cột `country` trong `matches_10min` vì $server \rightarrow country$ là phụ thuộc hàm hiển nhiên.
   - Phân tách rạch ròi cấp độ đội tuyển (`tournament_matches`) và cấp độ cá nhân (`tournament_players`), loại bỏ các cột thừa ở từng cấp.

---

## 5. BỘ TRUY VẤN SQL PHÂN TÍCH NÂNG CAO (CHƯƠNG 5 & 5x)
Tệp triển khai: [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql) & [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py).

| Mã Query | Kỹ thuật SQL | Bảng sử dụng | Đầu ra phân tích | File xuất CSV |
| :---: | :--- | :--- | :--- | :--- |
| **Q1** | `Self-JOIN`, `GROUP BY`, `HAVING` | `tournament_players` | Thống kê kèo đối đầu 1v1 theo từng đường (Top/Mid/Bot), winrate Đội Xanh, chênh lệch vàng & CS lúc 10 phút. | `data/processed/sql_query_1_result.csv` |
| **Q2** | `Intra-team JOIN`, `HAVING COUNT(*) >= 10` | `tournament_players` | Thống kê 125 cặp đôi Xạ thủ + Hỗ trợ (Bot + Sup) ăn ý nhất giải đấu, winrate, vàng chung phút 10. | `data/processed/sql_query_2_result.csv` |
| **Q3** | `CTE / Subquery`, `Unpivot UNION ALL`, `FULL JOIN` | `tournament_players`, `tournament_matches` | Top 20 tướng có Tỷ lệ Cấm/Chọn (Presence Rate) cao nhất giải đấu. | `data/processed/sql_query_3_result.csv` |
| **Q4** | `Window Functions: DENSE_RANK()`, `AVG() OVER()` | `tournament_players` | Xếp hạng top 3 tuyển thủ đè đường phút 10 theo từng vị trí (Top/Jng/Mid/Bot/Sup) và so với Benchmark toàn giải. | `data/processed/sql_query_4_result.csv` |
| **Q5** | `UNION ALL`, `CASE WHEN`, `GROUP BY` | `tournament_matches`, `matches_10min` | Đối chiếu hiệu quả lăn cầu tuyết (Snowball Lead) giữa Đấu Giải vs Solo Rank theo 5 phân tầng chênh lệch vàng phút 10. | `data/processed/sql_query_5_result.csv` |

---

## 6. HỆ THỐNG INDEXES TỐI ƯU TRUY VẤN (14 INDEXES)
- `idx_tm_league_year`: `tournament_matches(league, year)`
- `idx_tm_team`: `tournament_matches(teamname)`
- `idx_tm_date`: `tournament_matches(date)`
- `idx_tm_patch`: `tournament_matches(patch)`
- `idx_tm_playoffs`: `tournament_matches(playoffs)`
- `idx_tp_player`: `tournament_players(playername)`
- `idx_tp_champ`: `tournament_players(champion)`
- `idx_tp_pos`: `tournament_players(position)`
- `idx_tp_team`: `tournament_players(teamname)`
- `idx_tp_league`: `tournament_players(league)`
- `idx_tp_patch`: `tournament_players(patch)`
- `idx_tp_champ_pos`: `tournament_players(champion, position)`
- `idx_tp_game_pos_side`: `tournament_players(gameid, position, side)` *(Tối ưu hóa Q1 Self-JOIN)*
- `idx_tp_game_side_pos`: `tournament_players(gameid, side, position)` *(Tối ưu hóa Q2 Duo JOIN)*


