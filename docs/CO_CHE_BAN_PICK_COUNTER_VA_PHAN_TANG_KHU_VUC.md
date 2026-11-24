# TÀI LIỆU KỸ THUẬT TOÀN DIỆN: CƠ CHẾ THUẬT TOÁN CẤM/CHỌN (BAN/PICK AI), KHẮC CHẾ ĐƯỜNG TỔNG QUÁT, ĐÁNH GIÁ TIER & PHÂN TẦNG KHU VỰC (2026)

*Cập nhật lần cuối:* `2026-11-23`  
*Phạm vi áp dụng:* Toàn bộ 173 tướng, 5 vị trí thi đấu (`Top`, `Jungle`, `Mid`, `Bot`, `Support`), 3,098 cặp đối đầu trực tiếp 1v1 và 6 giải đấu chuyên nghiệp (`LCK`, `LPL`, `LCP`, `MSI`, `WLDS`/CKTG, `EWC`).  
*Mã nguồn thực thi:*
- [`src/07_recommender/recommender_engine.py`](../src/07_recommender/recommender_engine.py)
- [`src/07_recommender/simulate_draft_match.py`](../src/07_recommender/simulate_draft_match.py)
- [`src/06_machine_learning/draft_model.py`](../src/06_machine_learning/draft_model.py)
- [`src/06_machine_learning/snowball_model.py`](../src/06_machine_learning/snowball_model.py)

---

## 1. NGUYÊN TẮC THIẾT KẾ CỐT LÕI (ZERO-HARDCODE & 100% ALGORITHMIC DRIVEN)

Toàn bộ hệ thống Gợi ý Cấm/Chọn và Dự đoán Thắng/Thua tuân thủ tuyệt đối nguyên tắc:
1. **Không suy luận chủ quan & Không Hardcode tình huống lẻ:** Không bao giờ gán cứng kết quả cho một cặp tướng cụ thể (ví dụ không bao giờ viết `if enemy == 'Gnar': pick('Kennen')`).
2. **Thuật toán tổng quát trên dữ liệu thực nghiệm:** Mọi quyết định đều được tính toán tự động từ **37,009 bản ghi CSDL SQLite** ([`data/database/lol_live_data.db`](../data/database/lol_live_data.db)), gồm `30,000` bản ghi tuyển thủ đấu giải (`tournament_players`), `6,000` bản ghi đội hình đấu giải (`tournament_matches`) và `1,009` trận Solo Rank Thách Đấu (`matches_10min`).
3. **Kiểm soát nhiễu mẫu nhỏ bằng Thống kê Bayes:** Mọi tỷ lệ thắng và chênh lệch kinh tế đều được làm mịn qua tiên nghiệm thực nghiệm Bayes (**Empirical Bayes Shrinkage**) và trọng số độ tin cậy mẫu (**Smooth Sample Confidence**).

---

## 2. TĂNG TỐC HUẤN LUYỆN GPU (CUDA) & TỐI ƯU HÓA TRUY VẤN CSDL

1. **Huấn luyện bằng GPU NVIDIA CUDA (`device='cuda', tree_method='hist'`):**
   - Trong [`src/06_machine_learning/draft_model.py`](../src/06_machine_learning/draft_model.py) và [`src/06_machine_learning/snowball_model.py`](../src/06_machine_learning/snowball_model.py), hàm `_check_xgb_gpu_support()` tự động kiểm thử khả năng khởi tạo `XGBClassifier` trên nhân CUDA (NVIDIA GeForce RTX 4070 Laptop GPU).
   - Nếu GPU khả dụng, toàn bộ quá trình xây dựng cây quyết định Gradient Boosting dùng thuật toán histogram trên VRAM (`tree_method='hist'`, `device='cuda'`), kèm cơ chế fallback tự động về đa luồng CPU (`n_jobs=-1`) để đảm bảo tính tương thích trên mọi máy trạm.
2. **Composite Indexes tối ưu hóa Self-JOIN SQLite:**
   - Bổ sung 2 chỉ mục phức hợp trong [`src/01_data_pipeline/load_esports_to_db.py`](../src/01_data_pipeline/load_esports_to_db.py):
     - `idx_tp_game_pos_side ON tournament_players(gameid, position, side)`
     - `idx_tp_game_side_pos ON tournament_players(gameid, side, position)`
   - Giúp rút ngắn thời gian thực thi truy vấn ma trận 3,098 cặp kèo đối đầu 1v1 và cặp đôi Synergy từ hơn 25 giây xuống dưới **0.4 giây**.

---

## 3. PHÂN TẦNG META CẤM/CHỌN THEO KHU VỰC & GIẢI ĐẤU QUỐC TẾ

Mỗi khu vực Esports LMHT có bản sắc chiến thuật và mức độ ưu tiên tướng khác biệt rõ rệt. Hệ thống phân tách dữ liệu thành 8 chế độ khu vực/giải đấu trong `REGIONAL_PROFILES`:

| Mã Khu Vực (`--region`) | Giải đấu bao gồm | Số trận thực tế trong DB | Đặc trưng Meta được trích xuất từ dữ liệu |
| :--- | :--- | :---: | :--- |
| **`LCK`** | LCK (Hàn Quốc) | **812 trận** | Kiểm soát tầm nhìn, đi đường chuẩn chỉ, ưu tiên tướng mở giao tranh & kiểm soát mục tiêu (`Vi`, `Jarvan IV`, `Azir`, `Orianna`, `Rumble`, `Corki`). |
| **`LPL`** | LPL (Trung Quốc) | **1,092 trận** | Giao tranh liên tục, ưu tiên tướng cơ động & băng xả sát thương mạnh từ sớm (`Xin Zhao`, `Taliyah`, `Ambessa`, `Jax`, `Varus`, `K'Sante`). |
| **`LCP`** | LCP (Châu Á - TBD / VCS / PCS) | **474 trận** | Đột biến giao tranh sớm, tận dụng mạnh các quân bài thuận tay của khu vực. |
| **`WLDS`** *(hoặc `CKTG`)* | Chung Kết Thế Giới (Worlds) | **206 trận** | Meta giao thoa đỉnh cao cuối mùa giải, nơi các đội LCK, LPL, LCP chạm trán trực tiếp. |
| **`MSI`** | Mid-Season Invitational | **151 trận** | Meta giao thoa giữa mùa giải với thể thức Fearless / Bo5 cường độ cao. |
| **`EWC`** | Esports World Cup | **265 trận** | Giải đấu quốc tế nhịp độ nhanh. |
| **`INTERNATIONAL`** | Gộp `WLDS + MSI + EWC` | **622 trận** | Toàn bộ các trận va chạm liên khu vực trên sân khấu quốc tế. |
| **`ALL`** | Toàn bộ 6 giải đấu | **3,000 trận** | Meta tổng hợp toàn cầu. |

### Công thức Hòa trộn Thống kê Khu vực & Toàn cầu (Adaptive Regional Blending)
Để vừa giữ đúng bản sắc khu vực (ví dụ `LCK` hoặc `WLDS`), vừa tránh thiếu hụt cỡ mẫu ở các giải ngắn ngày (như `MSI` hoặc `WLDS`), hệ thống tính trọng số tin cậy khu vực dựa trên số trận thực tế:
$$w_{\text{reg}} = \frac{n_{\text{reg}}}{n_{\text{reg}} + \tau}$$
Trong đó $\tau$ là hằng số làm mượt ($\tau = 5$ cho kèo đối đầu 1v1, $\tau = 4$ cho cặp đôi Synergy). Các chỉ số tỷ lệ thắng và chênh lệch vàng phút 10 được kết hợp mượt mà:
$$\text{Metric}_{\text{blended}} = w_{\text{reg}} \cdot \text{Metric}_{\text{region}} + (1 - w_{\text{reg}}) \cdot \text{Metric}_{\text{global}}$$

---

## 4. CƠ CHẾ LƯU TRỮ & TÍNH TOÁN TARGET BAN TUYỂN THỦ (VD: `Target trực tiếp Faker`)

Khi hệ thống xuất dòng chữ: `& Target trực tiếp Faker (39 trận giải, WR 61.5%)`, dữ liệu **không hề được gán cứng trong code**, mà được trích xuất tự động từ 3 nguồn lưu trữ sau:

1. **Nguồn gốc chính (95% dữ liệu): Bảng `tournament_players` trong SQLite [`data/database/lol_live_data.db`](../data/database/lol_live_data.db)**
   - Chứa **30,000 bản ghi** thi đấu giải chuyên nghiệp.
   - Hàm `TargetBanEngine._load_tournament_player_stats()` trong [`src/07_recommender/recommender_engine.py`](../src/07_recommender/recommender_engine.py) chạy câu truy vấn `GROUP BY LOWER(playername), position, champion` (và phân tách thêm theo từng `league` cho `regional_player_db`) để thống kê cho từng tuyển thủ:
     - Số ván sử dụng (`games`), số ván thắng (`wins`), Tỷ lệ thắng làm mịn Bayes (`bayesian_wr`).
     - Chênh lệch vàng phút 10 (`avg_gd10`), chênh lệch lính phút 10 (`avg_csd10`), chỉ số KDA (`kda`) và tỷ trọng sát thương (`avg_dmg_share`).
   - *Ví dụ hồ sơ thực tế của `Faker` trong SQLite:* `Azir` (39 trận, thắng 61.5%, KDA 4.46), `Taliyah` (25 trận, thắng 68.0%, KDA 6.08, `GD10: +183g`), `Orianna` (22 trận, thắng 72.7%, KDA 6.60, `GD10: +161g`), `Galio` (12 trận, thắng 75.0%), `Ahri` (12 trận, thắng 58.3%, `GD10: +276g`).
2. **Nguồn bổ trợ Solo Rank (Hidden Pocket Pick): [`data/pro_player_accounts.json`](../data/pro_player_accounts.json)**
   - Lưu danh sách tài khoản Riot ID (`Hide on bush#KR1`, `Keria#KR1`, `Chovy#KR1`...) và lịch sử 30 trận Rank Thách Đấu gần nhất để phát hiện bài dị đang bí mật tập luyện (`spike_detected = True`, `WR >= 70%`).
3. **Tệp Cache Mô hình Đóng gói: [`models/recommender_engine.pkl`](../models/recommender_engine.pkl)**
   - Lưu toàn bộ cấu trúc `player_db` và `regional_player_db` đã huấn luyện để khi chạy mô phỏng hoặc gọi API chỉ mất `< 10ms` tra cứu.

---

## 5. CƠ CHẾ ĐÁNH GIÁ & PHÂN HẠNG TIER (`TIER S+`, `TIER S`, `COUNTER-PICK`, `SYNERGY`)

Hệ thống **không dùng bảng Tier tĩnh**, mà tính toán **Điểm Hiệu Quả Thực Chiến (`eff_score`)** động theo từng giải đấu, từng giai đoạn Cấm/Chọn (`Phase 1` vs `Phase 2`) và từng tình huống đội hình:

### A. Công thức Điểm Hiệu Quả Meta (`eff_score`)
1. **Tỷ lệ hiện diện (Presence Rate):**
   $$\text{Presence} = \frac{\text{Picks} + \text{Bans}}{\text{Total Matches in Region}}$$
2. **Tỷ lệ thắng làm mịn Bayes (Bayesian Smoothed Winrate, $C = 10$):**
   $$WR_{\text{bayes}} = \frac{\text{Wins} + 10 \times 0.50}{\text{Picks} + 10}$$
3. **Chỉ số áp đảo đường 10 phút chuẩn hóa (`gd10_norm`):**
   $$\text{GD10}_{\text{norm}} = \text{clip}\left(\frac{\overline{\text{GD@10}} + 300}{600},\ 0.1,\ 1.0\right)$$
4. **Trọng số độ tin cậy cỡ mẫu (`sample_confidence`):**
   $$\text{Conf}_{\text{sample}} = \min\left(1.0,\ \frac{\text{Picks}}{18.0}\right)$$

### B. Hệ thống Nhãn Phân Hạng (Badge / Tier Classification)
- **Trong giai đoạn CẤM (Ban Phase):**
  - `🔥 META BAN TIER S+`: Tướng vừa có tần suất xuất hiện/cấm chọn áp đảo giải đấu, vừa là tướng tủ nguy hiểm của tuyển thủ đối phương (`threat_score >= 0.35`).
  - `🚫 LƯỢT CẤM META (PHASE 1/2)`: Tướng có điểm thống trị Meta cao nhất giải đấu tại vị trí đang xét.
  - `🎯 TARGET BAN TUYỂN THỦ`: Tướng tủ thương hiệu hoặc Pocket Pick đang spam rank của tuyển thủ đối diện ở các vị trí chưa lộ tướng.
- **Trong giai đoạn CHỌN (Pick Phase):**
  - `🔥 COMBO SYNERGY`: Kích hoạt cặp đôi đồng đội có tỷ lệ thắng thực chiến vượt trội trong CSDL (`Synergy >= 0.85`).
  - `⚔️ COUNTER-PICK (META)` / `⚔️ COUNTER TÌNH HUỐNG`: Tướng khắc chế trực tiếp đối thủ cùng đường (thắng đường $\text{GD@10} > 0$ và thắng trận $\ge 52\%$).
  - `🔥 TƯỚNG TỦ TUYỂN THỦ`: Tuyển thủ cầm quân bài sở trường có $\ge 6$ trận giải, $WR_{\text{bayes}} \ge 53\%$ và **không bị đối thủ cùng đường khắc chế**.
  - `⭐ META TIER S+`: Tướng trụ cột toàn giải ($\ge 150$ lượt chọn toàn cầu hoặc thống trị tuyệt đối tại khu vực).
  - `⭐ META TIER S`: Tướng chuẩn Meta ($\ge 40$ lượt chọn, tỷ lệ thắng ổn định).
  - `✨ LỰA CHỌN CHIẾN THUẬT`: Quân bài chiến thuật chuyên biệt ($\ge 15$ lượt chọn).
  - `🔄 FLEX SWAP`: Quân bài cho phép đảo vị trí một tướng đã chọn trước đó sang đường khác để né kèo khắc chế của đối thủ.

---

## 6. THUẬT TOÁN KHẮC CHẾ & ĐI ĐƯỜNG TỔNG QUÁT (UNIVERSAL COUNTER-PICK VS BLIND-PICK ENGINE)

Đây là thuật toán cốt lõi giải quyết triệt để bài toán: **"Khi đối thủ đã lộ tướng cùng đường, AI tuyệt đối không bao giờ chọn tướng thua đường/thua kèo chỉ vì đó là tướng phổ biến hay tướng thuận tay, mà bắt buộc phải chọn tướng THẮNG ĐƯỜNG hoặc HÒA ĐƯỜNG & THẮNG GIAO TRANH"** trên toàn bộ **5 vị trí** và **3,098 cặp đối đầu 1v1**.

### A. Bước 1: Nhận diện 1-1 Tướng Đối Thủ Cùng Đường (`_infer_enemy_lane_assignment`)
- Khi truyền `enemy_picks` dưới dạng từ điển `{'top': ..., 'jng': ..., 'mid': ..., 'bot': ..., 'sup': ...}` (trong [`simulate_draft_match.py`](../src/07_recommender/simulate_draft_match.py)), hệ thống ánh xạ chính xác 1-1 từng đường (`db_lane`).
- Khi truyền danh sách tướng phẳng qua CLI (`--enemy "Gnar,Lee Sin,Azir"`), hàm `_infer_enemy_lane_assignment()` giải bài toán phân bổ 1-1 tối ưu dựa trên xác suất vị trí thực tế từ 30,000 bản ghi giải đấu để xác định chính xác ai đang đứng ở đường nào.

### B. Bước 2: Phân tách 2 Chế độ Chấm điểm (`Blind Pick` vs `Counter Pick`)

#### Chế độ 1: `BLIND PICK` (Đối thủ CHƯA lộ tướng cùng đường)
Khi `enemy_lane_opponent is None`, trọng số ưu tiên sự an toàn, đa dụng và phối hợp đội hình:
$$\text{Score}_{\text{blind}} = 0.36 \cdot \text{Eff}_{\text{meta}} + 0.16 \cdot \text{Counter}_{\text{team}} + 0.24 \cdot \text{Synergy}_{\text{ally}} + 0.24 \cdot \text{Balance}_{\text{comp}} + \text{Bonus}_{\text{player}} + \text{Bonus}_{\text{punisher}}$$

#### Chế độ 2: `COUNTER PICK` (Đối thủ ĐÃ lộ tướng cùng đường)
Khi `enemy_lane_opponent is not None`, hệ thống kích hoạt **Bộ lọc Ngắt Cứng Tổng Quát (Universal Hard Cut-off)** và **Hàm Thưởng Khắc Chế Thực Chiến**:

1. **Bộ lọc Ngắt Cứng Tổng Quát (Universal Hard Cut-off - Loại bỏ hoàn toàn kèo thua):**
   Mọi ứng viên có dữ liệu đối đầu ($\ge 3$ trận) với `enemy_lane_opponent` sẽ bị **LOẠI BỎ NGAY LẬP TỨC (`continue`)** nếu vi phạm bất kỳ điều kiện nào sau đây:
   - **Thua trận đối đầu:** Tỷ lệ thắng thực tế $WR_{\text{raw}} < 47.5\%$ HOẶC Tỷ lệ thắng Bayes ($C=10$) $WR_{\text{bayes}} < 48.8\%$.
   - **Thua đường (Laning Deficit lúc 10 phút):**
     - Với `Top`, `Jungle`, `Mid`, `Bot`: Bị dẫn vàng phút 10 vượt ngưỡng $\overline{\text{GD@10}} < -110\text{ vàng}$.
     - Với `Support`: Bị dẫn vàng phút 10 vượt ngưỡng $\overline{\text{GD@10}} < -150\text{ vàng}$ mà tỷ lệ thắng lật kèo giao tranh không đạt $52.5\%$.
   - **Thua đường nghiêm trọng:** $\overline{\text{GD@10}} < -200\text{ vàng}$ ở bất kỳ vị trí nào (dù winrate mẫu nhỏ có trên $50\%$ do đồng đội gánh cũng bị loại để không gợi ý kèo tự hủy đường).

2. **Khóa Điểm Tướng Tủ (`player_bonus`) khi gặp Kèo Chưa Kiểm Chứng hoặc Kèo Dưới:**
   - Trong chế độ `Counter Pick`, một tuyển thủ chỉ được nhận trọn vẹn điểm thưởng Tướng Tủ nếu quân bài đó **đã được chứng minh thắng kèo hoặc hòa đường thắng trận** trước chính tướng đối diện ($n \ge 2$, $WR_{\text{bayes}} \ge 50\%$, $\text{GD@10} \ge -80\text{g}$).
   - Nếu tướng tủ rơi vào kèo dưới hoặc chưa từng được kiểm chứng đối đầu với tướng địch cùng đường, `player_bonus` bị cắt giảm **85% – 90%** để ngăn chặn triệt để hiện tượng "nhắm mắt pick tướng tủ đâm đầu vào kèo thua" (ví dụ ngăn Kiin pick `K'Sante` vào `Gnar`).

3. **Công thức Điểm Đối Đầu 1v1 (`lane_matchup_score`) có Làm Mượt Độ Tin Cậy Mẫu:**
   Với các ứng viên vượt qua bộ lọc, hệ thống tính hệ số tin cậy mẫu $\alpha = \frac{n}{n + 8.0}$ (ngăn các tướng chỉ thắng ăn may 2–3 trận vượt mặt các tướng khắc chế chuẩn meta 15–150 trận):
   $$\text{Score}_{\text{matchup}} = 0.50 + \alpha \cdot \left[ 1.35 \cdot (WR_{\text{bayes}} - 0.50) + 0.14 \cdot \tanh\left(\frac{\overline{\text{GD@10}}}{250.0}\right) \right]$$
   - Cộng thêm thưởng đặc biệt (`+0.08 * alpha`) cho các quân bài **Thắng Kép (Double Dominance)**: Vừa đè đường ($\text{GD@10} \ge +30\text{g}$), vừa thắng trận ($WR_{\text{raw}} \ge 52\%$).
   - Tổng điểm trong chế độ `Counter Pick`:
     $$\text{Score}_{\text{counter}} = 0.24 \cdot \text{Eff}_{\text{meta}} + 0.44 \cdot \text{Score}_{\text{matchup}} + 0.16 \cdot \text{Synergy}_{\text{ally}} + 0.16 \cdot \text{Balance}_{\text{comp}} + \text{Bonus}_{\text{player}} + \text{Bonus}_{\text{punisher}}$$

4. **Bộ lọc Độ Tinh Khiết Vị Trí (Role Purity Filter):**
   - Để ngăn các tướng trái vị trí có mẫu siêu nhỏ (như `Dr. Mundo` Rừng 4 trận hay `Elise` Hỗ trợ 5 trận) lọt vào danh sách khắc chế, bất kỳ tướng nào có vị trí gốc (`meta['lane']`) khác với đường đang xét bắt buộc phải có ít nhất $\ge 35$ trận đấu giải toàn cầu hoặc $\ge 15$ trận tại khu vực đó ở đúng vị trí flex này.

---

## 7. BẢNG KIỂM CHỨNG THỰC TẾ TRÊN CẢ 5 VỊ TRÍ

| Vị trí & Kèo đối đầu | Top Khắc Chế / Hòa & Thắng Đường được Thuật toán lựa chọn | Các tướng phổ biến đã bị Thuật toán tự động loại bỏ vì thua đường / thua trận |
| :--- | :--- | :--- |
| **TOP vs `Gnar`** *(LCK)* | 1. **Rumble** (`18 trận`, Thắng `61.1%`, `GD10: +40g`)<br>2. **Olaf** (`10 trận`, Thắng `60.0%`, `GD10: +191g`)<br>3. **Kennen** (`5 trận`, Thắng `61.0%`, `GD10: +324g`) | ❌ `K'Sante` (`GD10: -252g`, WR `42%`)<br>❌ `Sion` (`GD10: -327g`, WR `41%`)<br>❌ `Jax` (`GD10: -175g`, WR `43%`)<br>❌ `Renekton` (`GD10: -119g`, WR `40%`) |
| **TOP vs `K'Sante`** *(LCK)* | 1. **Rumble** (`147 trận`, Thắng `52.0%`, `GD10: +103g`)<br>2. **Renekton** (`69 trận`, Thắng `66.2%`, `GD10: +150g`)<br>3. **Gwen** (`18 trận`, Thắng `73.4%`, `GD10: +65g`)<br>4. **Ambessa** (`29 trận`, Thắng `56.0%`, `GD10: +104g`)<br>5. **Gnar** (`26 trận`, Đè đường `GD10: +246g`, Thắng `50.0%`) | ❌ Các tướng chống chịu bị K'Sante đè đường hoặc thua giao tranh tổng |
| **MID vs `Azir`** *(LCK)* | 1. **Orianna** (`70 trận`, Thắng `59.2%`, `GD10: +151g`)<br>2. **Ryze** (`36 trận`, Thắng `52.9%`, `GD10: +132g`)<br>3. **Yone** (`42 trận`, Thắng `77.9%`, `GD10: -58g` - Hòa đường & Thắng giao tranh)<br>4. **Viktor** (`8 trận`, Thắng `52.5%`, `GD10: +71g`) | ❌ `Ahri` (`31 trận`, WR `29.0%`)<br>❌ `Corki` (`44 trận`, WR `38.6%`)<br>❌ `Taliyah` (`65 trận`, WR `47.1%`) |
| **JUNGLE vs `Lee Sin`** *(ALL)* | 1. **Xin Zhao** (`18 trận`, Thắng `59.8%`, `GD10: +34g`)<br>2. **Wukong** (`17 trận`, Thắng `59.7%`, `GD10: -102g` - Thắng giao tranh)<br>3. **Poppy** (`6 trận`, Thắng `75.0%`, `GD10: +302g`) | ❌ `Vi` (`22 trận`, WR `36.4%`, `GD10: -120g`)<br>❌ `Sejuani` (`18 trận`, WR `38.9%`, `GD10: -195g`) |
| **BOT vs `Ezreal`** *(LCK)* | 1. **Sivir** (`10 trận`, Thắng `73.5%`, `GD10: +180g`)<br>2. **Corki** (`34 trận`, Thắng `56.6%`, `GD10: -32g`)<br>3. **Varus** (`44 trận`, Thắng `54.5%`, `GD10: +167g`) | ❌ `Kai'Sa` (`46 trận`, `GD10: -215g`, WR `45.7%`)<br>❌ `Miss Fortune` (`GD10: -185g`) |
| **SUPPORT vs `Leona`** *(LCK)* | 1. **Alistar** (`74 trận`, Thắng `59.4%`, `GD10: +17g`)<br>2. **Rakan** (`54 trận`, Thắng `66.1%`, `GD10: +5g`)<br>3. **Braum** (`47 trận`, Thắng `60.2%`, `GD10: -15g`)<br>4. **Nautilus** (`54 trận`, Thắng `60.4%`, `GD10: +28g`) | ❌ Các tướng Hỗ trợ máu giấy bị Leona mở giao tranh sốc sát thương |
