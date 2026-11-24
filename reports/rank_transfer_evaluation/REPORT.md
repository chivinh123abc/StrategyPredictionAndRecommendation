# Thử nghiệm nguồn đối đầu Rank / Pro

**Chú thích cohort bổ sung24/11:** 83trận hợp scope patch/time được lấy từ seed Thách Đấu; chưa xác nhận rank lịch sử của cả10người. Đây không là đánh giá nhóm high elo đã xác nhận. Admission policy mới kiểm92trận cache cho0trận đủ bằng chứng lịch sử (không có nghĩa rank thấp). Metric gốc bên dưới giữ nguyên; xem [cohort audit](../rank_cohort_audit/REPORT.md) và [thiết kế hai chế độ](../../docs/HAI_CHE_DO_VA_TIEU_CHUAN_RANK_CAO.md).

Patch 16.20, cutoff 2026-10-26T18:03:08.999999999+00:00. Rank hợp lệ: 83/92 trận cache.
Đánh giá thăm dò trên dữ liệu giải cũ, không phải final test mới. Chưa bật tích hợp contextual.

| Tập | Cấu hình | Queries | Recall@5 | MRR@5 | Queries có ứng viên đủ mẫu Rank |
|---|---|---:|---:|---:|---:|
| validation | pro_only | 200 | 0.5150 | 0.2728 | 18 |
| validation | rank_only | 200 | 0.5150 | 0.2720 | 18 |
| validation | hybrid | 200 | 0.5150 | 0.2728 | 18 |
| test | pro_only | 320 | 0.4938 | 0.3026 | 13 |
| test | rank_only | 320 | 0.4938 | 0.3026 | 13 |
| test | hybrid | 320 | 0.4938 | 0.3026 | 13 |

Chênh Recall@5 so Pro và CI95 bootstrap theo series:
- validation/rank_only: 0.0000, CI95 [0.0, 0.0]; 9 series.
- validation/hybrid: 0.0000, CI95 [0.0, 0.0]; 9 series.
- test/rank_only: 0.0000, CI95 [0.0, 0.0]; 10 series.
- test/hybrid: 0.0000, CI95 [0.0, 0.0]; 10 series.

Chỉ thay thành phần matchup; cùng pool hợp lệ, role chỉ suy từ lịch sử đã đóng băng và tướng đã lộ. Hybrid cố định50/50, không tune từ test.

CI [0,0] ở metric có cùng hit/miss không chứng minh hai phương pháp tương đương trong tổng thể. Đọc cùng coverage và số series nhỏ.

## Giới hạn

- Retrieval of observed picks is not proof of strategic quality/counter/win uplift.
- Existing Worlds games used in previous project audits: chronological holdout is not a fresh final test.
- Rank seed selection uses present-day Challenger status, subject to survivor/selection bias; historical ranks unknown.
- Hard Fearless series IDs reconstructed, not officially verified; exclusions in splits.json.
- Rank-only means only matchup counts from Rank; other components remain Pro, not an entirely Rank-trained system.
- Hybrid averages residuals 50/50 only for Rank pairs with n>=5, otherwise preserves Pro; not pooled counts/probabilities.
- Pro snapshot retains its existing earlier-patch backfill; Rank requires exact target patch/platform and pre-cutoff event time.
- Gold/XP/CS are descriptive exports, excluded from draft inputs to avoid post-draft leakage.
- A degenerate bootstrap CI [0,0] from identical hit patterns is not proof of equivalence or zero population uncertainty.
- Scores are heuristic priorities, not calibrated probabilities; this experiment cannot assess probability calibration.
- No observed-pick retrieval benchmark validates ban decisions or BO5 optimality.
