# Độ phủ dữ liệu Rank snapshot

**Phạm vi lịch sử:** đây là báo cáo4run snapshot ban đầu, không tổng corpus mới. Kho SQLite tăng dần và bảng cập nhật hiện hành ở [rank_matchups_live](../rank_matchups_live/REPORT.md); metric/readiness bên dưới giữ nguyên mốc nghiệmthu cũ.

Khử trùng: 10 trận accepted / 100 dòng participant / 72 người duy nhất.
Champion-role đủ n5 và3người: 0/115; kèo cùng đường đủ mẫu/độ đa dạng: 0/2156.
Counts chỉ lấy accepted; rejected/missing không được cộng bằng chứng. Một trận ở nhiều run chỉ giữ lần accepted sớm nhất. Server/queue/patch/floor giữ riêng.
Các hàng0 là thiếu mẫu trong universe tướng/role đã thấy ở các trận ứng viên, không khẳng định toàn bộ tướng/role khả thi của game.

| Server/patch | Role | Trận | Người | Tướng đủ mẫu | Số trận cao nhất của1tướng |
|---|---|---:|---:|---:|---:|
| KR/16.22 | bot | 0 | 0 | 0 | 0 |
| KR/16.22 | jng | 0 | 0 | 0 | 0 |
| KR/16.22 | mid | 0 | 0 | 0 | 0 |
| KR/16.22 | sup | 0 | 0 | 0 | 0 |
| KR/16.22 | top | 0 | 0 | 0 | 0 |
| KR/16.23 | bot | 10 | 16 | 0 | 4 |
| KR/16.23 | jng | 10 | 15 | 0 | 3 |
| KR/16.23 | mid | 10 | 17 | 0 | 3 |
| KR/16.23 | sup | 10 | 15 | 0 | 4 |
| KR/16.23 | top | 10 | 17 | 0 | 2 |

## Chưa đủ điều kiện triển khai/đánh giá recommender

- insufficient_history_with_snapshot_evidence_available_before_validation
- KR/420/16.23/MASTER/top:fewer_than_two_supported_champions
- KR/420/16.23/MASTER/jng:fewer_than_two_supported_champions
- KR/420/16.23/MASTER/mid:fewer_than_two_supported_champions
- KR/420/16.23/MASTER/bot:fewer_than_two_supported_champions
- KR/420/16.23/MASTER/sup:fewer_than_two_supported_champions

Readiness là policy kỹ thuật tự thiết kế, không chứng minh đủ statistical power. Không hạ n5/3người hoặc bỏ cutoff để ép pass.
Snapshot phải có trước thời điểm đánh giá, không chỉ ngày trận trước cutoff. Nhiều batch trong cùng ngày không tự thành kiểm chứng tương lai.
Recommender Rank và phép đánh giá/baseline chưa được chạy trong bước này nếu chưa đủ điều kiện; không có metric giả. Runtime Giải không đổi.

CSV: patch_coverage/role_coverage/champion_role_coverage/lane_matchup_coverage ghi số trận/người và số còn thiếu; games/observations là accepted dataset không PUUID.
Rank hiện chỉ là cohort Master+ gần lúc quan sát, không exact rank lịch sử; không đo MMR, counter nhân quả hoặc tối ưu draft/BO5.
