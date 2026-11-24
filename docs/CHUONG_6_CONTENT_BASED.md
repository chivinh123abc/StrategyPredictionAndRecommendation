# Minh chứng Chương 6: Content-based filtering

Hướng đồ án: **Vận dụng kiến thức môn học, có phần mở rộng.**

## Đối chiếu slide của môn học

Nguồn: `docs/course_slides/Chapter 6_ Recommendation Systems.pdf` (số trang hiển thị trên slide).

| Nội dung bài học | Trang | Hiện thực trong dự án |
|---|---:|---|
| Gợi ý item có thuộc tính tương đồng | 11 | `recommend_similar`: tìm tướng thay thế gần hồ sơ tướng mẫu, cùng vị trí |
| Item profile là vector đặc trưng | 12–13 | Một item = cặp tướng/vị trí; vector chỉ số lịch sử thực đo |
| User profile là trung bình có trọng số của item profiles | 16–18 | Hồ sơ tuyển thủ = trung bình vector tướng, trọng số số lượt chọn trong lịch sử |
| So sánh user profile với item bằng cosine | 19–20 | `recommend_for_player` và `sklearn.metrics.pairwise.cosine_similarity` |
| Đánh giá Precision at top 10 | 47 | Benchmark có Precision@10 và baseline cùng tập ứng viên |

**Đây là content-based, không gọi là collaborative filtering.** Không lấy tỷ lệ thắng hay bảng synergy gán sẵn làm cosine. TF-IDF trong slide áp dụng cho nội dung văn bản; dự án dùng thuộc tính số nên không ép áp dụng TF-IDF.

## Dữ liệu và công thức

`src/07_recommender/content_based.py` đọc `tournament_players` qua chính sách sạch chung. Các đặc trưng là **DPM**, **CS/phút**, **ward/phút**, **sát thương nhận/phút**, **tỷ trọng vàng kiếm được**. Đây là hành vi đã quan sát ở trận trước, không phải thông số kỹ năng/chất tướng thuần túy. Đội, tuyển thủ, đối thủ và patch có thể ảnh hưởng các chỉ số.

1. Giới hạn lịch sử bằng `before` khi đánh giá; lọc đúng vai trò/khu vực.
2. Bỏ dòng thiếu/không hợp lệ ở năm phép đo, không điền giả. Tướng phải có ít nhất năm trận đủ phép đo để lập item profile.
3. Lấy trung bình từng phép đo theo tướng/vị trí, chuẩn hóa min-max trong catalog lịch sử cùng vị trí. Bỏ chiều không biến thiên; không dùng min/max từ holdout.
4. Hồ sơ tuyển thủ: `u = sum(n_c * v_c) / sum(n_c)` với `n_c` là số lượt chọn tướng trong lịch sử. Đây là **implicit preference** (sở thích suy từ hành vi), không phải điểm rating được tuyển thủ cung cấp. Loại phần lịch sử chưa có item profile, công bố cả `history_games` và `represented_games`.
5. Xếp hạng bằng `cos(u,v) = dot(u,v)/(norm(u)*norm(v))`. Chế độ tướng mẫu thay `u` bằng vector tướng đó. Loại tướng mẫu/tướng cấm; không sinh kết quả cho user/item chưa đủ lịch sử hoặc vector bằng 0.

`cosine_similarity` là độ tương đồng, không phải xác suất thắng, mức thành thạo hoặc tác động nhân quả. Hồ sơ raw, vector chuẩn hóa, số mẫu, trọng số user và query vector đều có trong đầu ra để kiểm tra phép tính. Không huấn luyện một bộ dự đoán mới; chỉ tổng hợp thuộc tính và tính cosine.

## Phần mở rộng, tách khỏi nội dung slide

Chọn đặc trưng hành vi LMHT, lấy tần suất chọn làm trọng số implicit, ngưỡng số mẫu, chuẩn hóa theo role và chia thời gian là các lựa chọn ứng dụng của đồ án. Recall/MRR và khoảng tin cậy bootstrap là phần mở rộng, không phải nguyên văn bài học. Phần này giữ riêng với `HistoricalRecommender` (heuristic từ thống kê thắng/thua).

## Minh chứng thực nghiệm

Chạy `evaluate_content_based.py`: dùng tập **validation theo thời gian**, item profile/user history/scaling chỉ lấy trước cutoff. Không thay đổi hoặc tối ưu trên tập test đã dùng trước đó. Che tướng đã chọn của tuyển thủ, dùng chín tướng còn lại làm giới hạn ứng viên trong bài toán hồi cứu. So sánh với phổ biến toàn giải và tần suất chọn của chính tuyển thủ trên cùng catalog.

Mỗi truy vấn có một nhãn đã quan sát, vì vậy `Precision@10 = Recall@10 / 10`, tối đa 0.1. Điều đó không có nghĩa chín tướng còn lại chắc chắn không phù hợp. Có báo cáo toàn bộ truy vấn (cold-start tính là bỏ lỡ) và cohort có hồ sơ. Không suy ra chọn tối ưu hoặc tăng thắng từ benchmark truy hồi.

Kết quả thực tế: [content_based_evaluation.md](../reports/content_based_evaluation.md), [JSON kèm hồ sơ ví dụ](../reports/content_based_evaluation.json), [bảng item profiles Mid](../reports/content_based_mid_profiles.csv). Notebook: `notebooks/02_content_based_recommender.ipynb`.

## Chạy minh họa

```powershell
.\.venv\Scripts\python.exe src/07_recommender/recommender_engine.py --content-based --seed-champion Ahri --lane mid
.\.venv\Scripts\python.exe src/07_recommender/recommender_engine.py --content-based --content-player Faker --lane mid
.\.venv\Scripts\python.exe src/07_recommender/evaluate_content_based.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
