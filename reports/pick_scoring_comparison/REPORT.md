# So sánh công thức pick hiện tại và bản đơn giản

Cùng dữ liệu lịch sử đóng băng, cùng candidate/role pool và luật loại trừ. Không tự đổi bản chính.
Dữ liệu đã dùng trong audit cũ; đây là so sánh phát triển, không phải independent final test.

| Tập | Công thức | Queries | Recall@5 | MRR@5 | Coverage |
|---|---|---:|---:|---:|---:|
| validation | current | 200 | 0.5150 | 0.2728 | 0.7650 |
| validation | simple | 200 | 0.4250 | 0.2256 | 0.7650 |
| validation | recent_presence | 200 | 0.4200 | 0.2048 | 0.7650 |
| test | current | 320 | 0.4938 | 0.3026 | 0.7688 |
| test | simple | 320 | 0.4250 | 0.2334 | 0.7688 |
| test | recent_presence | 320 | 0.4500 | 0.2554 | 0.7688 |

validation: delta Recall@5 simple-current {'series': 9, 'delta': -0.09, 'ci95': [-0.17002083333333334, -0.021052631578947368], 'kind': 'paired_reconstructed_series_bootstrap_1000_seed42'}; top5 đổi 193.
test: delta Recall@5 simple-current {'series': 10, 'delta': -0.06875, 'ci95': [-0.1103448275862069, -0.03234768907563026], 'kind': 'paired_reconstructed_series_bootstrap_1000_seed42'}; top5 đổi 306.

Keep current default; simple is an explicit demo/comparison option. Independent tactical-quality evidence is unavailable.

component_audit.csv chỉ đo độ nhạy khi bỏ từng thành phần trên cùng pool; thay top1 không chứng minh thành phần đó cần thiết về chiến thuật.

## Giới hạn

- Reused Pro audit data: development comparison, not a fresh independent final test.
- Recall/MRR retrieve observed picks, not tactical quality/counter/win improvement.
- No weight tuning or test-driven formula changes; no Rank or postgame query resources used.
- Different missing-profile patterns change the count of averaged signals in simple.
- Simple scores same-role matchups only; synergy/team interactions remain descriptive.
- Reconstructed series IDs and existing flexible-role inference remain shared extensions.
- Bootstrap CI is conditional on this small sample; [0,0] does not prove equivalence.
