# Content-based filtering — minh chứng Chương 6

Item profile: trung bình chỉ số thực đo của tướng/vị trí. User profile: trung bình item vectors, trọng số số lần tuyển thủ chọn tướng.
Chuẩn hóa min-max theo vị trí, rồi cosine similarity. Không sử dụng winrate hoặc bảng synergy/thuộc tính chuyên gia.
Chỉ tổng hợp dữ liệu trước 2026-04-29T08:05:12+00:00; 299 trận validation, 2990 truy vấn. Không huấn luyện mô hình dự đoán.

| Phương pháp | Precision@10 | Recall@10 | Recall@5 | MRR@5 |
|---|---:|---:|---:|---:|
| content_based | 0.0494 | 0.4936 | 0.2990 | 0.1390 |
| popularity | 0.0749 | 0.7492 | 0.4652 | 0.2212 |
| player_frequency | 0.0756 | 0.7559 | 0.4839 | 0.2403 |

User profile coverage: 96.02%.
Precision@10 CI95 (mở rộng bootstrap): [0.04787541806020067, 0.051339464882943144]

Có một nhãn liên quan mỗi truy vấn nên Precision@10 tối đa 0.1. Các lựa chọn khác chưa được chấm là phù hợp/không phù hợp.
Không diễn giải truy hồi lựa chọn thành chọn tối ưu hoặc tăng tỷ lệ thắng. Baseline popularity/player frequency dùng cùng tập ứng viên.
Slide tham chiếu: Chương 6, trang 11–13 (item profile), 16–19 (user profile/cosine), 47 (Precision at top 10).
Các mở rộng: thuộc tính hành vi từ lịch sử, implicit pick weights, cắt thời gian và bootstrap; không coi là nội dung slide nguyên văn.
