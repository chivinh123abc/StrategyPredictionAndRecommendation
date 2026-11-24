# DANH MỤC CÁC CỔNG API MỞ, BỘ DỮ LIỆU CHUẨN & TÀI NGUYÊN KỸ THUẬT
**Môn học: Nhập môn Khoa học Dữ liệu (Introduction to Data Science) - PTIT**

Tài liệu này tổng hợp toàn bộ các đường link API chính thức, bộ dữ liệu benchmark mở và tài liệu kỹ thuật phục vụ cho dự án **Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) trong Esports Liên Minh Huyền Thoại**.

---

## CHỦ ĐỀ: ESPORTS & LEAGUE OF LEGENDS (LIÊN MINH HUYỀN THOẠI)

### 🔗 Link 1.1: Riot Games Data Dragon (Static CDN API - Hoàn toàn mở, không cần Key)
* **Trang thông tin:** [https://developer.riotgames.com/docs/lol#data-dragon](https://developer.riotgames.com/docs/lol#data-dragon)
* **Endpoint kiểm tra phiên bản mới nhất:** `https://ddragon.leagueoflegends.com/api/versions.json`
* **Endpoint 173 vị Tướng tiếng Việt (Bản 16.18.1):** `https://ddragon.leagueoflegends.com/cdn/16.18.1/data/vi_VN/champion.json`
* **Endpoint Trang bị (Items tiếng Việt):** `https://ddragon.leagueoflegends.com/cdn/16.18.1/data/vi_VN/item.json`
* **Ghi chú:** Không cần API Key, không giới hạn tốc độ gọi (Rate Limit), dữ liệu vĩnh viễn không bao giờ hết hạn. Cung cấp toàn bộ chỉ số HP, giáp, sát thương, tầm đánh, độ khó và hình ảnh tướng phục vụ giao diện Web App.

### 🔗 Link 1.2: Riot Games Developer Portal (Dynamic Match & Rank API)
* **Trang chủ:** [https://developer.riotgames.com/](https://developer.riotgames.com/)
* **Tài liệu các hàm API (API Reference):** [https://developer.riotgames.com/apis](https://developer.riotgames.com/apis)
* **Endpoint chi tiết trận đấu (`MATCH-V5`):** `https://developer.riotgames.com/apis#match-v5`
* **Endpoint dòng thời gian từng phút (`MATCH-V5 TIMELINE`):** `https://developer.riotgames.com/apis#match-v5/GET_getTimeline`
* **Endpoint bảng xếp hạng (`LEAGUE-V4`):** `https://developer.riotgames.com/apis#league-v4`
* **Ghi chú:** Đăng nhập bằng tài khoản Riot để lấy Development API Key miễn phí (20 req/s, 100 req/2 phút).

### 🔗 Link 1.3: Tập dữ liệu 9,879 Trận đấu Rank Kim Cương (Kaggle & GitHub)
* **Link Kaggle:** [League of Legends Diamond Ranked Games (10 min)](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min)
* **Link tải trực tiếp CSV (GitHub Raw):** [high_diamond_ranked_10min.csv](https://raw.githubusercontent.com/SharnSingh/LeagueOfLegends_Diamond_PredictiveAnalysis/master/high_diamond_ranked_10min.csv)
* **Ghi chú:** Chứa 9,879 trận đấu rank Kim Cương với 40 chỉ số ở mốc 10 phút (vàng, rồng, mạng hạ gục, mắt cắm).

### 🔗 Link 1.4: Nền tảng Thống kê Trực tiếp để Tham chiếu (OP.GG / U.GG)
* **OP.GG Champions Analytics:** [https://www.op.gg/champions](https://www.op.gg/champions)
* **U.GG Meta Tier List:** [https://u.gg/lol/tier-list](https://u.gg/lol/tier-list)

### 🔗 Link 1.5: Oracle's Elixir (Kho dữ liệu Đấu Giải Chuyên Nghiệp LCK, LPL, LCP, MSI, WLDS, EWC)
* **Trang chủ & Tải dữ liệu:** [https://oracleselixir.com/tools/downloads](https://oracleselixir.com/tools/downloads)
* **Thư mục Google Drive dùng chung (13 mùa giải 2014 - nay):** [Google Drive Folder ID: `1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`](https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH)
* **Module tự động đồng bộ về máy trạm:** [`src/01_data_pipeline/sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py) (Xem tài liệu tại [`README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md))
* **Kaggle Mirror Dataset:** [League of Legends Pro Matches (Oracle's Elixir)](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-database)
* **Định nghĩa các trường dữ liệu:** [https://oracleselixir.com/definitions](https://oracleselixir.com/definitions)
* **Ghi chú:** Kho lưu trữ toàn diện dữ liệu các giải đấu chuyên nghiệp toàn cầu từ 2014 đến nay. Chứa đầy đủ: Tên đội, tên tuyển thủ, 10 lượt Cấm (`ban1` - `ban5`), 10 lượt Chọn theo 5 vị trí (`top`, `jng`, `mid`, `bot`, `sup`), chỉ số kinh tế mốc 10 phút (`goldat10`, `xpat10`, `csat10`, `golddiffat10`), rồng đầu, sâu hư không và trụ.

### 🔗 Link 1.6: Leaguepedia MediaWiki Cargo API (Cổng REST API Đấu Giải LoL Esports Mở 100%)
* **Endpoint API chính:** `https://lol.fandom.com/api.php`
* **Tài liệu hướng dẫn Cargo API:** [https://lol.fandom.com/wiki/Help:Cargo_API](https://lol.fandom.com/wiki/Help:Cargo_API)
* **Bảng dữ liệu trọng tâm:** `ScoreboardGames`, `ScoreboardPlayers`.
