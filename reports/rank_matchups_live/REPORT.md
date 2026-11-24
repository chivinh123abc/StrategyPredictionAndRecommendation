# Dữ liệu đối đầu cập nhật tăng dần

Đã có 931 trận với observations; 6588 cặp có hướng, 134 cặp đạt n>=5.
Hàng đợi: {'accepted': 931, 'pending': 1, 'rejected': 42, 'accepted_observations': 9310, 'seeds': 33681}. Không có mốc dừng tổng ở1.000trận; mỗi phiên có cap tài nguyên và có thể tiếp tục.
all_matchups.csv chứa cả kèo ít mẫu; ba bảng xếp riêng theo winrate thắng trận/GD15, không trì hoãn cập nhật đến khi đủ1000.
Các bảng xếp chỉ hiện kèo qua ngưỡng n; rỗng nghĩa chưa đủ mẫu, không gán kết quả giả.

| Bảng | Ý nghĩa |
|---|---|
| best_full_game_matchups.csv | Winrate cao khi gặp đối thủ cùng role; kết quả cả đội |
| unfavorable_full_game_matchups.csv | Winrate thấp khi gặp đối thủ |
| early_gold_advantages.csv | Chênh vàng phút15 cao, tách khỏi thắng trận |
| all_matchups.csv | n/người/Wilson, mean/median/SD/CI của gold-XP-CS10/15; giữ cả sparse |

Bảng pooled_*.csv gộp mọi patch/server thực có, vẫn tách queue/tier/role; không gọi ALL_OBSERVED là dữ liệu toàn thế giới đầy đủ.
matchup_collection_progress.csv chỉ báo số mẫu/độ phủ thực có. Không đặt mốc cố định mỗi kèo; target/remaining/reached để trống khi chưa có mục tiêu được xác định.
Chưa nạp bộ đối chiếu U.GG theo cùng bộ lọc: không khẳng định đã bằng số mẫu, độ phủ hoặc chất lượng của họ.
patches/platforms ghi nguồn gộp; gd15_patch_direction phát hiện trung bình trái dấu ở các patch đủ n. Cùng dấu không chứng minh counter bền vững.

Chỉ học cách phân biệt thống kê công khai từ U.GG, không biết/tái tạo thuật toán nội bộ hoặc sao chép số liệu của họ.
GD10/GD15 và XP/CS là phép đo quan sát hậu draft, không dùng trực tiếp làm feature dự báo trước draft.

## Giới hạn

- Same-role gold/XP/CS include jungle/support/roams/team and player effects.
- Jungle is not a literal laning duel; support/bot context needs separate analysis.
- Snapshots are near-match proxies, not historical tiers. Rank and Pro are not pooled.
- No adjustment for champion base strength, skill, side or selection bias is claimed.
- Low n remains low reliability even if mean gold or raw winrate is extreme.
- Matchup ranking is descriptive; no win uplift, mechanical counter or BO5 optimality claim.
