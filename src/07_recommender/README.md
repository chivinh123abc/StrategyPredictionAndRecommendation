# Module 07: Hệ Thống Gợi Ý Cấm/Chọn & Nhận Diện Điều Kiện Thắng (Ban/Pick Recommender & Win Condition Engine)

## Mục tiêu & Trách nhiệm
Xây dựng thuật toán đề xuất cấm/chọn tối ưu phục vụ Chương 6 (Recommendation Systems) và Phân tích Chiến thuật (ADR-014):
- **Gợi ý khắc chế (Counter Pick):** Dựa vào tỉ lệ thắng đối đầu trực tiếp giữa 2 tướng cùng đường (Lane Matchup Winrate).
- **Gợi ý tương thích (Synergy Pick):** Khai phá luật kết hợp Apriori đề xuất cặp đôi/bộ ba tướng có khả năng kết hợp tốt nhất với đồng minh đã chọn trước.
- **Gợi ý lượt Cấm (Ban Recommendation):** Đề xuất tướng khắc chế cứng của đội hình đối phương cần cấm.
- **Engine Phân Tích Điều Kiện Thắng (Win Condition Card - ADR-014):** Tự động trích xuất Thẻ chiến thuật:
  - Chủ lực gánh đội (Core Carry: Jinx, Smolder, Draven, Renekton...).
  - Điểm rơi sức mạnh (Power Spike Timing: Trước phút 25 vs Sau phút 25).
  - Mục tiêu ưu tiên số 1 (Primary Objective: Rồng, Sâu Hư Không, Trụ, Baron).
  - Điều kiện thất bại cần tránh (Lose Condition: Để thua > 2,000 vàng lúc 10 phút...).

## Dữ liệu ra (Output)
- Xuất file mô hình: `models/recommender.pkl`, `models/win_condition_engine.pkl`.

