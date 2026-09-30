# Module 07: Hệ Thống Gợi Ý Cấm/Chọn & Nhận Diện Điều Kiện Thắng (Ban/Pick Recommender & Win Condition Engine)

## Mục tiêu & Trách nhiệm
Xây dựng thuật toán đề xuất cấm/chọn tối ưu phục vụ Chương 6 (Recommendation Systems) và Phân tích Chiến thuật (ADR-014):

### 1. Phân hệ CẤM Lai Ghép mục tiêu theo Tuyển thủ Đối phương (Hybrid Opponent Target Ban)
- **Tầng 1: Phân tích Đấu Giải (Tournament Established Picks - Trọng số 60-70%):**
  - Tự động phân tích lịch sử 30,000 bản ghi tuyển thủ (`tournament_players` trong CSDL `lol_live_data.db`).
  - Tính toán **Chỉ số Tướng Tủ Nguy Hiểm (Signature Threat Index)** dựa trên: Tần suất chọn (Pick Rate), Tỷ lệ thắng làm mịn Bayes (Bayesian Smoothed Winrate) và Chỉ số đè đường 10 phút (`golddiffat10`, `csdiffat10`).
  - Tự động nhận diện và cập nhật hồ sơ tuyển thủ mới (Tân binh LCK/LPL/VCS) ngay khi nạp dữ liệu giải mới.
- **Tầng 2: Phân tích Solo Rank Gần Nhất (Recent Solo Queue Trend & Hidden Weapon Detector - Trọng số 30-40%):**
  - Khai thác lịch sử đấu 20-50 trận gần nhất của tuyển thủ trên máy chủ Rank Thách Đấu (KR/VN) qua Riot Games API & Riot PUUID bất biến.
  - Tự động phát hiện hiện tượng spam bài dị bất thường (**Spike in Pick Rate** & Winrate > 65% trong Rank).
- **Pro Player Registry & Dynamic Account Linking (`data/pro_player_accounts.json`):**
  - Quản lý danh mục Riot ID của các tuyển thủ chuyên nghiệp (`gameName#tagLine`).
  - Cho phép thêm / cập nhật linh hoạt qua CLI hoặc API `POST /api/v1/players/link-account`.
  - Cơ chế **Graceful Fallback**: Nếu tuyển thủ chưa có Riot ID hoặc API hết hạn, hệ thống tự động fallback 100% về dữ liệu Đấu Giải.
- **Đầu ra:** Tự động xuất **Top 3 - 5 tướng bắt buộc phải CẤM (Target Ban & Pocket Pick Alert 🚨)** khi đối đầu với tuyển thủ chỉ định (ví dụ: Keria -> *Bard, Renata, Camille*, Kiaya -> *Rumble, Renekton*, Chovy -> *Yone, Ahri*).

### 2. Phân hệ CHỌN theo Chuẩn Meta & Tối ưu Đội hình (Meta-based Pick Recommender)
- **Gợi ý khắc chế (Counter Pick):** Dựa vào tỉ lệ thắng đối đầu trực tiếp giữa 2 tướng cùng đường (Lane Matchup Winrate).
- **Gợi ý tương thích (Synergy Pick):** Khai phá luật kết hợp đề xuất cặp đôi/bộ ba tướng có khả năng kết hợp tốt nhất trong Meta (Mid-Jungle, Bot-Sup).
- **Cân bằng thành phần đội hình:** Tự động phát hiện thiếu hụt sát thương phép (AP), sát thương vật lý (AD), hiệu ứng khống chế cứng (Hard CC) hoặc khả năng mở giao tranh (Engage).

### 3. Phân hệ Nhận Diện Lỗ Hổng Cấm/Chọn Của Địch & Con Bài Trừng Phạt (Draft Flaw & Punisher Recommender)
- Quét và đối chiếu Vector thuộc tính 5 tướng của địch:
  - **Lỗ hổng Heavy Melee (3-4 tướng cận chiến):** Bật cảnh báo đỏ và đẩy mạnh gợi ý các con bài trừng phạt chống càn diện rộng (**Illaoi, Darius, Mordekaiser, Cassiopeia, Brand**).
  - **Lỗ hổng Full AD (Không có AP):** Gợi ý siêu đỡ đòn giáp (**Malphite, Rammus, K'Sante, Taric**).
  - **Lỗ hổng Zero Hard CC (Không có làm choáng/hất tung):** Gợi ý siêu sát thủ quẩy combat (**Master Yi, Katarina, Irelia, Zeri**).
  - **Lỗ hổng Full Squishy (Không có tướng chống chịu):** Gợi ý càn quét bắt lẻ mở giao tranh (**Nocturne, Jarvan IV, Hecarim, Akali**).

### 4. Engine Phân Tích Điều Kiện Thắng (Win Condition Card - ADR-014)
- Tự động trích xuất Thẻ chiến thuật:
  - Chủ lực gánh đội (Core Carry: Jinx, Smolder, Draven, Renekton...).
  - Điểm rơi sức mạnh (Power Spike Timing: Trước phút 25 vs Sau phút 25).
  - Mục tiêu ưu tiên số 1 (Primary Objective: Rồng, Sâu Hư Không, Trụ, Baron).
  - Điều kiện thất bại cần tránh (Lose Condition: Để thua > 2,000 vàng lúc 10 phút...).

## Dữ liệu ra (Output)
- Xuất file mô hình & động cơ: `models/recommender.pkl`, `models/target_ban_engine.pkl`, `models/punisher_engine.pkl`, `models/win_condition_engine.pkl`.

