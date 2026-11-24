# Contextual Pro / Rank: thử nghiệm tín hiệu đối đầu

Freeze: 2026-11-24T07:36:57.203162+00:00. Rank: 261 trận. Prospective ready: False.
Bản chính không thay điểm. Rank và Pro không trộn số trận; hybrid chỉ trộn residual ở kèo Rank đủ mẫu.
Chưa có dữ liệu giải độc lập sau freeze thì kết quả prospective để null, không tạo metric giả.

Thống kê vàng/XP/CS chỉ để giải thích; tín hiệu thử nghiệm dùng kết quả thắng lịch sử cùng role.

## diagnostic

**Thăm dò hành vi trên dữ liệu cũ; có thể dùng Rank thu sau trận giải. Không chứng minh nâng chất lượng, không dùng để promote.**

| Tập | Mode | Queries | Recall@5 | MRR@5 | Rank hỗ trợ |
|---|---|---:|---:|---:|---:|
| validation | pro_only | 30 | 0.6 | 0.3138888888888889 | 6 |
| validation | rank_only | 30 | 0.6 | 0.3138888888888889 | 6 |
| validation | hybrid | 30 | 0.6 | 0.3138888888888889 | 6 |
| test | pro_only | 30 | 0.5333333333333333 | 0.315 | 7 |
| test | rank_only | 30 | 0.5333333333333333 | 0.315 | 7 |
| test | hybrid | 30 | 0.5333333333333333 | 0.315 | 7 |

validation: delta Recall@5 hybrid={'series': 2, 'delta': 0.0, 'ci95': [0.0, 0.0], 'kind': 'paired_reconstructed_series_bootstrap_1000_seed42'}; changed top5=0.

test: delta Recall@5 hybrid={'series': 2, 'delta': 0.0, 'ci95': [0.0, 0.0], 'kind': 'paired_reconstructed_series_bootstrap_1000_seed42'}; changed top5=0.

Series được tái dựng, chưa phải ID giải chính thức. N5 và 5+5 series là policy thử nghiệm, không bảo đảm power. CI bootstrap suy biến không chứng minh tương đương. Điểm không phải xác suất thắng.
