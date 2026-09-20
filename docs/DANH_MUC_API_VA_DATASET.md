# DANH MỤC CÁC CỔNG API MỞ, BỘ DỮ LIỆU CHUẨN & TÀI NGUYÊN KỸ THUẬT
**Môn học: Nhập môn Khoa học Dữ liệu (Introduction to Data Science) - PTIT**

Tài liệu này tổng hợp toàn bộ các đường link API chính thức, bộ dữ liệu benchmark mở và tài liệu kỹ thuật được phân loại chi tiết theo từng chủ đề. Mỗi chủ đề bao gồm nhiều nguồn link phục vụ cho từng khâu trong quy trình Khoa học Dữ liệu (Thu thập, SQL, Thống kê, Machine Learning, Recommender System).

---

## 1. CHỦ ĐỀ: ESPORTS & LEAGUE OF LEGENDS (LIÊN MINH HUYỀN THOẠI)

### 🔗 Link 1.1: Riot Games Data Dragon (Static CDN API - Hoàn toàn mở, không cần Key)
* **Trang thông tin:** [https://developer.riotgames.com/docs/lol#data-dragon](https://developer.riotgames.com/docs/lol#data-dragon)
* **Endpoint kiểm tra phiên bản mới nhất:** `https://ddragon.leagueoflegends.com/api/versions.json`
* **Endpoint 173 vị Tướng tiếng Việt (Bản 16.18.1):** `https://ddragon.leagueoflegends.com/cdn/16.18.1/data/vi_VN/champion.json`
* **Endpoint Trang bị (Items tiếng Việt):** `https://ddragon.leagueoflegends.com/cdn/16.18.1/data/vi_VN/item.json`
* **Ghi chú:** Không cần API Key, không giới hạn tốc độ gọi (Rate Limit), dữ liệu vĩnh viễn không bao giờ hết hạn. Cung cấp toàn bộ chỉ số HP, giáp, sát thương, tầm đánh, độ khó và văn bản cốt truyện (dùng cho TF-IDF Recommender).

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
* **Ghi chú:** Chứa 9,879 trận đấu rank Kim Cương với 40 chỉ số ở mốc 10 phút (vàng, rồng, mạng hạ gục, mắt cắm). Đã được kiểm chứng tải thành công 100% bằng Pandas trong 1 giây.

### 🔗 Link 1.4: Nền tảng Thống kê Trực tiếp để Crawl (OP.GG / U.GG)
* **OP.GG Champions Analytics:** [https://www.op.gg/champions](https://www.op.gg/champions)
* **U.GG Meta Tier List:** [https://u.gg/lol/tier-list](https://u.gg/lol/tier-list)
* **Ghi chú:** Dùng thư viện `BeautifulSoup` và `Requests` để crawl tỷ lệ thắng (winrate) và tỷ lệ cấm/chọn (pick/ban rate) theo từng phiên bản giải đấu.

### 🔗 Link 1.5: Oracle's Elixir (Kho dữ liệu Đấu Giải Chuyên Nghiệp VCS, LCK, LPL, CKTG)
* **Trang chủ & Tải dữ liệu:** [https://oracleselixir.com/tools/downloads](https://oracleselixir.com/tools/downloads)
* **Kaggle Mirror Dataset:** [League of Legends Pro Matches (Oracle's Elixir)](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-database)
* **Định nghĩa các trường dữ liệu:** [https://oracleselixir.com/definitions](https://oracleselixir.com/definitions)
* **Ghi chú:** Kho lưu trữ toàn diện dữ liệu các giải đấu chuyên nghiệp toàn cầu (VCS Việt Nam, LCK Hàn Quốc, LPL Trung Quốc, CKTG/Worlds) từ 2014 đến 2026. Chứa đầy đủ: Tên đội (T1, Gen.G, GAM Esports), tên tuyển thủ (Faker, Chovy, Levi), 10 lượt Cấm (`ban1` - `ban5`), 10 lượt Chọn theo 5 vị trí (`top`, `jng`, `mid`, `bot`, `sup`), chỉ số kinh tế mốc 10 phút (`goldat10`, `xpat10`, `csat10`, `golddiffat10`), rồng đầu, sâu hư không và trụ. Đây là nguồn dữ liệu chuẩn mực để thực hiện Kiểm định giả thuyết A/B (Chương 1) và so sánh Meta Đấu Giải vs Đấu Rank (Chương 3, 4).

### 🔗 Link 1.6: Leaguepedia MediaWiki Cargo API (Cổng REST API Đấu Giải LoL Esports Mở 100%)
* **Endpoint API chính:** `https://lol.fandom.com/api.php`
* **Tài liệu hướng dẫn Cargo API:** [https://lol.fandom.com/wiki/Help:Cargo_API](https://lol.fandom.com/wiki/Help:Cargo_API)
* **Bảng dữ liệu trọng tâm:**
  - `ScoreboardGames`: Chứa tên giải đấu (`OverviewPage`), Đội 1, Đội 2, Đội thắng (`Winner`), danh sách tướng chọn (`Team1Picks`, `Team2Picks`), danh sách tướng cấm (`Team1Bans`, `Team2Bans`), thời lượng trận (`Gamelength`).
  - `ScoreboardPlayers`: Chi tiết KDA, lượng vàng, chỉ số lính, tướng sử dụng của từng tuyển thủ.
* **Ghi chú:** Hoàn toàn miễn phí, không cần đăng ký API Key. Gọi qua phương thức GET với `action=cargoquery&tables=ScoreboardGames&format=json` kèm User-Agent chuẩn là có thể trích xuất trực tiếp JSON các giải đấu VCS, LCK, Worlds.

---

## 2. CHỦ ĐỀ: COMPETITIVE POKÉMON (CHAMPIONS VGC & SHOWDOWN)

### 🔗 Link 2.1: PokéAPI (REST API Chuẩn Quốc Tế - Miễn phí 100%, không cần Key)
* **Trang chủ & Docs:** [https://pokeapi.co/](https://pokeapi.co/)
* **Endpoint toàn bộ 1,025 loài Pokémon:** `https://pokeapi.co/api/v2/pokemon?limit=1025`
* **Endpoint 900+ Chiêu thức (Moves):** `https://pokeapi.co/api/v2/move?limit=900`
* **Endpoint 18 Hệ tương khắc (Types):** `https://pokeapi.co/api/v2/type`
* **Ghi chú:** Cung cấp chi tiết Base Stats (HP, Attack, Defense, Sp.Atk, Sp.Def, Speed), chỉ số tổng BST, đặc tính (Abilities) và bảng ma trận tương khắc hệ (Type Damage Relations) dùng để xây dựng thuật toán **Chọn con tối ưu khắc chế**.

### 🔗 Link 2.2: Smogon University Competitive Usage Stats (Kho dữ liệu Meta thi đấu)
* **Thư mục thống kê hàng tháng:** [https://www.smogon.com/stats/](https://www.smogon.com/stats/)
* **Dữ liệu tỷ lệ chọn & moveset format VGC:** [Smogon VGC Moveset Stats](https://www.smogon.com/stats/2026-02/moveset/)
* **Ghi chú:** File định dạng text/json chuẩn chứa tỉ lệ chọn Pokémon, các chiêu thức hay dùng nhất, trang bị (held items) và danh sách **Teammates** (các đồng đội hay đi kèm). Đây là nguồn dữ liệu tuyệt vời để làm ma trận **Collaborative Filtering** cho tính năng Team Builder.

### 🔗 Link 2.3: Pokémon Showdown Replays (Dữ liệu Trận đấu Thực tế)
* **Trang chủ Replay:** [https://replay.pokemonshowdown.com/](https://replay.pokemonshowdown.com/)
* **Cấu trúc tải dữ liệu trận JSON:** `https://replay.pokemonshowdown.com/{replay_id}.json`
* **Ghi chú:** Hàng triệu ván đấu thi đấu tự do và xếp hạng được lưu trữ dưới dạng log văn bản chi tiết từng lượt đánh (Turn-by-turn log), cực kỳ thích hợp cho bài toán Machine Learning dự đoán đội thắng cuộc.

### 🔗 Link 2.4: Bộ dữ liệu Tổng hợp Pokémon trên Kaggle
* **Link Kaggle:** [The Complete Pokemon Dataset (Gen 1 - Gen 9)](https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420)
* **Ghi chú:** Bảng tổng hợp sẵn dạng CSV với đầy đủ tên, hệ, chỉ số, tỉ lệ bắt, tốc độ tăng trưởng, giúp nạp nhanh vào CSDL SQLite / PostgreSQL.

---

## 3. CHỦ ĐỀ: THỊ TRƯỜNG THẺ BÀI CHIẾN THUẬT TCG (POKÉMON TCG & YU-GI-OH!)

### 🔗 Link 3.1: Pokémon TCG Developer Portal & API (pokemontcg.io)
* **Trang chủ & Đăng ký API Key:** [https://pokemontcg.io/](https://pokemontcg.io/)
* **Tài liệu API chính thức:** [https://docs.pokemontcg.io/](https://docs.pokemontcg.io/)
* **Endpoint tìm kiếm thẻ bài:** `https://api.pokemontcg.io/v2/cards`
* **Endpoint danh mục bộ thẻ (Sets):** `https://api.pokemontcg.io/v2/sets`
* **Endpoint giá thị trường theo thời gian:** Tích hợp trực tiếp dữ liệu giá từ sàn **TCGPlayer** và **Cardmarket** trong từng thẻ bài.
* **Ghi chú:** Miễn phí hoàn toàn. Nếu đăng ký tài khoản lấy API Key (chỉ mất 1 phút), bạn được nâng giới hạn lên đến **20,000 requests/ngày**.

### 🔗 Link 3.2: YGOPRODeck Yu-Gi-Oh! REST API (Mở 100%, không cần Key)
* **Trang chủ & API Guide:** [https://ygoprodeck.com/api-guide/](https://ygoprodeck.com/api-guide/)
* **Endpoint toàn bộ 13,000+ thẻ bài:** `https://db.ygoprodeck.com/api/v7/cardinfo.php`
* **Endpoint lọc theo Archetype/Tộc:** `https://db.ygoprodeck.com/api/v7/cardinfo.php?archetype=Blue-Eyes`
* **Endpoint danh sách bộ bài vô địch giải đấu (Tournament Decks):** `https://ygoprodeck.com/api/tournament-decks`
* **Ghi chú:** Cung cấp đầy đủ: ID, tên, hệ, thuộc tính, ATK, DEF, văn bản mô tả hiệu ứng (Card Text) và giá sàn sàn TCGPlayer / Cardmarket / eBay / Amazon.

### 🔗 Link 3.3: Sàn giao dịch Giá Thẻ bài TCGPlayer & Cardmarket
* **TCGPlayer Marketplace:** [https://www.tcgplayer.com/](https://www.tcgplayer.com/)
* **Cardmarket Europe:** [https://www.cardmarket.com/](https://www.cardmarket.com/)
* **Ghi chú:** Cung cấp chỉ số giá sàn (Market Price), giá bán thực tế (Median Price) và biến động tăng giảm giá phục vụ bài toán hồi quy (Regression) dự báo giá trị thẻ bài.

### 🔗 Link 3.4: Scryfall API (Dành cho Magic: The Gathering nếu quan tâm)
* **Trang chủ API:** [https://scryfall.com/docs/api](https://scryfall.com/docs/api)
* **Ghi chú:** Được đánh giá là REST API thẻ bài có thiết kế kiến trúc chuẩn mực và sạch sẽ nhất thế giới.

---

## 4. CHỦ ĐỀ: SPOTIFY MUSIC INTELLIGENCE & PLAYLIST RECOMMENDER

### 🔗 Link 4.1: Spotify for Developers Portal
* **Trang chủ:** [https://developer.spotify.com/](https://developer.spotify.com/)
* **Tài liệu API:** [https://developer.spotify.com/documentation/web-api](https://developer.spotify.com/documentation/web-api)
* **Endpoint đặc trưng sóng âm (Audio Features):** `https://developer.spotify.com/documentation/web-api/reference/get-audio-features`
* **Ghi chú:** Cung cấp các thuộc tính vật lý của bài hát: `danceability`, `energy`, `valence`, `tempo`, `loudness`, `acousticness`, `speechiness`. Tạo App miễn phí trên dashboard để lấy `Client_ID` và `Client_Secret`.

### 🔗 Link 4.2: Thư viện Python Spotipy (Wrapper chuẩn)
* **Tài liệu:** [https://spotipy.readthedocs.io/](https://spotipy.readthedocs.io/)
* **Cài đặt:** `pip install spotipy`
* **Ghi chú:** Giúp kết nối và kéo dữ liệu từ Spotify chỉ với 3 dòng lệnh Python mà không cần tự xử lý OAuth token thủ công.

### 🔗 Link 4.3: Tập dữ liệu 160,000+ Bài hát Spotify trên Kaggle (1921 - Nay)
* **Link Kaggle:** [Spotify Dataset 1921-2020 (160k+ Tracks)](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-160k-tracks)
* **Ghi chú:** Dataset cực kỳ đầy đủ và chuẩn hóa với 160,000 bài hát, có sẵn điểm Popularity (0-100) và 10 thuộc tính sóng âm, sẵn sàng cho bài toán phân cụm K-Means và Recommender.

### 🔗 Link 4.4: Spotify Million Playlist Dataset (Ma trận Tiện ích Lớn)
* **Link AICrowd:** [The Million Playlist Dataset Challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)
* **Ghi chú:** Chứa 1,000,000 danh sách phát (playlists) do người dùng tạo ra, là bộ dữ liệu chuẩn mực nhất để huấn luyện thuật toán **Item-Item Collaborative Filtering** cho bài toán gợi ý nhạc.

---

## 5. CHỦ ĐỀ: BẤT ĐỘNG SẢN & AN CƯ ĐÔ THỊ VIỆT NAM (ƯU TIÊN CUỐI CÙNG)

### 🔗 Link 5.1: Chợ Tốt Gateway API (JSON trực tiếp, mở 100%)
* **Endpoint BĐS TP.HCM:** `https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1000&limit=20`
* **Endpoint BĐS Hà Nội:** `https://gateway.chotot.com/v1/public/ad-listing?region_v2=12000&cg=1000&limit=20`
* **Danh mục phân loại (cg):** `1010` (Căn hộ chung cư), `1020` (Nhà ở), `1040` (Phòng trọ sinh viên/công nhân).
* **Ghi chú:** Trả về dữ liệu JSON sạch 100% gồm giá số nguyên, diện tích $m^2$, quận huyện, phường xã, tên đường, tọa độ GPS thực tế (`latitude`, `longitude`) và bài viết mô tả chi tiết bằng tiếng Việt. Không cần API Key.

### 🔗 Link 5.2: Alonhadat HTML Scraper (Dành cho Web Scraping với BeautifulSoup)
* **Trang chủ:** [https://alonhadat.com.vn/](https://alonhadat.com.vn/)
* **Ghi chú:** Cấu trúc HTML cực kỳ đơn giản, không dùng Cloudflare chống bot, các thẻ `div` phân tách giá tiền, diện tích, địa chỉ rất rõ ràng. Chuẩn mực cho bài thực hành Chương 2 về Web Scraping.

### 🔗 Link 5.3: Batdongsan.com.vn Portal
* **Trang chủ:** [https://batdongsan.com.vn/](https://batdongsan.com.vn/)
* **Ghi chú:** Cổng thông tin BĐS lớn nhất Việt Nam, dùng để tham khảo dữ liệu giá dự án căn hộ và phân tích các bài toán kinh tế đô thị vĩ mô.

### 🔗 Link 5.4: Bộ dữ liệu Vietnam Housing trên Kaggle
* **Link Kaggle:** [Vietnam Housing Dataset / HCMC Real Estate Market](https://www.kaggle.com/datasets/hcmc-real-estate-market)
* **Ghi chú:** Tập dữ liệu hơn 25,000 tin rao bán và cho thuê nhà đất tại Hà Nội và TP.HCM đã được cộng đồng làm sạch sẵn dạng CSV, có thể dùng ngay làm phương án dự phòng.

### 🔗 Link 5.5: OpenStreetMap Overpass API (Dữ liệu Địa lý & Tiện ích Công cộng)
* **Trang web truy vấn:** [https://overpass-turbo.eu/](https://overpass-turbo.eu/)
* **Ghi chú:** Trích xuất tọa độ GPS của các tiện ích công cộng (14 nhà ga tuyến Metro số 1 Bến Thành - Suối Tiên, trường đại học, bệnh viện, trạm xe buýt) để tính khoảng cách và kiểm định giả thuyết A/B testing về tác động của hạ tầng giao thông đến giá thuê nhà.
