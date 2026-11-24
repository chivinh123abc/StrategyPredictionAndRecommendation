# Mục lục Báo cáo & Minh chứng (`reports/`)

Tài liệu này phân loại các thư mục và tệp kết quả trong `reports/` thành **3 nhóm rõ ràng** để tránh trích dẫn nhầm số liệu lịch sử vào báo cáo cuối kỳ. Đối chiếu đầy đủ kiến thức môn học và phần mở rộng xem tại [sổ kiến thức báo cáo](../docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md).

---

## 1. Sản phẩm nộp môn học (Core Deliverables)

| Đường dẫn | Nội dung | Trạng thái |
|---|---|---|
| [reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx](final_report/BAO_CAO_CUOI_KY_PTIT.docx) · [BAO_CAO_CUOI_KY.md](final_report/BAO_CAO_CUOI_KY.md) | Báo cáo tổng kết đồ án cuối kỳ (bản Word `.docx` gắn 13 biểu đồ/ảnh minh chứng + phân tích mạch giá trị & bản Markdown) | **Đã có bản Word hoàn chỉnh** |
| `reports/slides/` | Slide thuyết trình bảo vệ đồ án | **Chưa có file** (chờ biên soạn) |
| [reports/figures/](figures/README.md) | 11 biểu đồ EDA, đánh giá ML và phân cụm (`fig1`–`fig11`, 300 DPI) | Đã có (`fig10`–`fig11` thuộc artifact phân cụm cũ) |

---

## 2. Minh chứng kỹ thuật hiện hành (Active & Current)

Dùng nhóm này khi trích dẫn kết quả đang vận hành trong mã nguồn hiện tại:

### Học máy & Recommender cốt lõi (Chương 4 & Chương 6)
- [src/06_machine_learning/evaluation_report.md](../src/06_machine_learning/evaluation_report.md) — Kết quả đánh giá ML v2 hiện hành (`Draft`: Acc `0.5517`, AUC `0.5628`; `Snowball`: Acc `0.6718`, AUC `0.7413`).
- [content_based_evaluation.md](content_based_evaluation.md) & [content_based_evaluation.json](content_based_evaluation.json) — Benchmark Content-based Chương 6 (Precision@10, Recall@5 so với popularity baseline) và [content_based_mid_profiles.csv](content_based_mid_profiles.csv).
- [recommender_evaluation.json](recommender_evaluation.json) — Benchmark historical ranker riêng.
- [integrity_summary.json](integrity_summary.json) & [integrity_checks.json](integrity_checks.json) — Kiểm chứng Integrity v2.

### Ban/Pick, Fearless BO5 & So sánh công thức điểm
- [legacy_contextual_comparison/COMPARISON.md](legacy_contextual_comparison/COMPARISON.md) — Đối chiếu 2 chiến lược ban hiện hành (`legacy` vs `contextual`, đã gỡ lookahead).
- [pick_scoring_comparison/REPORT.md](pick_scoring_comparison/REPORT.md) & [simple_scoring_bo5/REPORT.md](simple_scoring_bo5/REPORT.md) — So sánh `current` vs `simple` trên 520 truy vấn (giữ mặc định `current`) và BO5 minh họa.
- [pair_reservation_revision/REPORT.md](pair_reservation_revision/REPORT.md) — Minh chứng cơ chế giữ cặp bot (MR-24) và chọn First Selection từng ván (NV-23).
- [ui_lane_revision/REPORT.md](ui_lane_revision/REPORT.md) — Minh chứng tự xếp đường, kiểm kèo đã lộ (MR-12 sửa / NV-24), BO5 all-Blue và 178 unit tests PASS.
- [contextual_ui_revision/REPORT.md](contextual_ui_revision/REPORT.md) — Minh chứng fixed-capacity `pool_value` v2 trên 80 ban states và snapshot binding.

### Bằng chứng Pro / Rank (Tách nguồn, không gộp điểm)
- [pro_matchups/](pro_matchups/) — Thống kê đối đầu từ 3,000 trận Pro sạch (WR, Wilson CI, GD/XP/CS 10 & 15).
- [rank_matchups_live/REPORT.md](rank_matchups_live/REPORT.md) & [summary.json](rank_matchups_live/summary.json) — Kho Rank tăng dần (`ranked_evidence.db`, schema v3 không quota mặc định).
- [pro_rank_explanations/REPORT.md](pro_rank_explanations/REPORT.md) — Ví dụ bảng giải thích 2 nguồn Pro/Rank riêng biệt trong gợi ý.

### Giao diện Web local (UI NV-24 mới nhất)
- [ui_inspector_collapse/REPORT.md](ui_inspector_collapse/REPORT.md) — Thu gọn toàn bộ panel Hiểu lựa chọn (mốc trình bày mới nhất).
- [ui_inspector_toggle/REPORT.md](ui_inspector_toggle/REPORT.md) — Ẩn mặc định và click-toggle Inspector (7 Edge workflows PASS).
- [ui_sidebars_fit/REPORT.md](ui_sidebars_fit/REPORT.md) — Responsive 3 cột từ `900px` qua 7 độ rộng màn hình + mobile `390px`.

---

## 3. Artifact nghiên cứu phụ & Lịch sử (Historical / Research Archive)

Các thư mục/tệp dưới đây được giữ lại để truy vết và đối chiếu, **không dùng làm mô tả hành vi runtime hiện hành**:

- **Lookahead cũ (đã gỡ khỏi runtime/CLI ngày 24/11):** `ban_strategy_comparison/` (so 3 chế độ gồm lookahead).
- **Prototype dự đoán đối thủ (đã dừng phát triển theo phạm vi vừa sức):** `opponent_model_evaluation.json`, `opponent_prediction.json`, `wlds_draft_states_manifest.json`, `draft_with_opponent_forecasts.json`, `worlds_fearless_with_forecasts/`.
- **Nghiên cứu chuyển miền & độ phủ Rank (thăm dò, chưa tích hợp vào điểm Pro):** `rank_pro_matchups/`, `rank_pro_study_data/`, `rank_transfer_evaluation/`, `rank_cohort_audit/`, `rank_snapshot_collection/`, `rank_coverage/`, `contextual_rank_experiment/`.
- **Các mốc kiểm tra UI trước khi hoàn thiện bố cục 3 cột:** `ui_demo/`, `ui_centered_board/`, `ui_flanking_choices/`.
- **Các phiên chạy & audit lịch sử trước các bản sửa sau:** `worlds_fearless_bo5/`, `t1_geng_bo5_20261124/`, `t1_geng_bo5_test_20261124/`, `t1_geng_contextual_20261124/`, `contextual_pick_review/`, `sparse_lane_priority_fix/`, `draft_choice_audit.*`, `contextual_pick_audit.*`, `trundle_case_review.json`, `tactical_review_*`, `lck_draft_*`, `lck_meta_checks.json`, `worlds_draft_*`, `worlds_replay_before_role_pairs.json`, `worlds_role_pair_checks.json`, `wlds_draft_policy_evaluation.json`, `draft_simulator_checks.json`, `content_based_checks.json`, `knowledge_rules_checks.json`.
