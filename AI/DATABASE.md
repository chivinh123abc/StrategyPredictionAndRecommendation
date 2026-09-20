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

## 2. QUY TẮC CHUẨN HÓA ĐÃ ĐƯỢC CHỨNG MINH
1. **Chuẩn 1NF (Tính nguyên tử):**
   - Không dùng mảng ghép hay chuỗi ghép tướng cho đội hình. Toàn bộ 10 vị trí thi đấu được tách thành 10 cột nguyên tử độc lập (`blueTop`..`blueSupport`, `redTop`..`redSupport`).
2. **Chuẩn 3NF (Khử phụ thuộc hàm bắc cầu):**
   - Loại bỏ cột `country` vì $server \rightarrow country$ là phụ thuộc hàm hiển nhiên (`VN2` $\rightarrow$ Vietnam, `KR` $\rightarrow$ Korea). Giữ lại cột `server` làm khóa ngoại logic để triệt tiêu dư thừa.

---

## 3. CÁC BẢNG KẾ HOẠCH BỔ SUNG (TASK 1.2)
- **`tournament_matches`**: Lưu thông tin cấp trận đấu giải đấu 2026 (`gameid`, `league`, `year`, `split`, `date`, `patch`, `teamname`, `result`, `gamelength`, `golddiffat10`, `killsat10`,...).
- **`tournament_players`**: Lưu thông tin chi tiết 10 tuyển thủ (`playername`, `playerid`, `position`, `champion`, `kills`, `deaths`, `assists`, `goldat10`, `csat10`,...).
