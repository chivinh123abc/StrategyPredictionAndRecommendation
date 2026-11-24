# Khắc phục độ đúng dữ liệu và đánh giá — 2026-11-23

Tài liệu này mô tả phần đã sửa trong dự án đang triển khai. API, web và bảo vệ đồ án tiếp tục nằm trong lộ trình, không bị coi là lỗi vì chưa thực hiện.

## 1. Phân biệt kết quả và quy tắc

- `win_probability_pct`: xác suất ước lượng từ model schema v2, qua hiệu chỉnh trên tập riêng. Không phải lợi ích nhân quả do chọn tướng.
- `ranking_score`: điểm xếp hạng 0–100, không có đơn vị %. Các trường cũ `score` (0–1), `priority_pct` (điểm 0–100) chỉ giữ để tương thích CLI; tên trường cũ không có nghĩa đây là xác suất.
- `historical.winrate`: tỷ lệ thắng cả trận trong lịch sử, kèm `wins`, `games`, `ci95_wilson`. Không phải tỷ lệ thắng đường hay xác suất thắng của một trận sắp tới.
- `expected_winrate_delta`, `causal_uplift`, `winrate_impact`: không có ước lượng hợp lệ nên để `null`, không còn các giá trị +18.5%, +14.2%…
- Radar, nhận xét đội hình và thẻ chiến thuật vẫn dùng bảng thuộc tính/quy tắc chuyên gia. Đây là nội dung định tính, không phải khám phá nhân quả từ dữ liệu. Bộ gợi ý lịch sử không lấy điểm từ các bảng này.
- Ma trận khắc chế riêng từng tướng và bảng synergy gán tay không còn tham gia xếp hạng. Không suy ra vị trí đối thủ từ danh sách tướng khi không có vị trí xác nhận.

## 2. Chính sách dữ liệu dùng chung

`src/analysis_data.py` đọc SQLite chỉ để đọc, lọc domain và tạo snapshot sạch trong bộ nhớ. Không đổi schema hoặc nội dung raw DB. Export CSV, SQL, kiểm định, EDA, ML và recommender dùng cùng chính sách.

- Giữ chênh lệch vàng/XP âm; tính lại chênh lệch từ hai tổng thực đo để bảo đảm đối xứng.
- Lọc trận dưới 600 giây, nhãn không hợp lệ, phép đếm/tổng bất khả thi và bản ghi thiếu phép đo bắt buộc. Không tuyên bố phát hiện tất cả AFK.
- Giữ các trận có lợi thế lớn hợp lệ. IQR/Z-score chỉ là công cụ khảo sát riêng, không tự động biến trận đó thành dữ liệu sai và không fit ngưỡng trên toàn bộ tập trước khi chia.
- Phép đo bị khuyết không được điền thành 0. Bài toán phút 10 chỉ nhận trận có cả hai phía và đủ năm biến macro bắt buộc.
- `tournament_matches_10min` chỉ là bảng snapshot trong SQLite bộ nhớ phục vụ truy vấn; không phải bảng mới trong raw DB.
- Crawler mới kiểm tra timestamp sự kiện <=600000 ms. Không thể xác minh lại timeline rank cũ vì dự án không lưu JSON timeline; đây là giới hạn dữ liệu hiện có.

Snowball v2 chỉ dùng chênh vàng, XP, CS, kills/deaths lúc 10 phút và đặc trưng dẫn xuất từ chúng, phe, nguồn. Không dùng số rồng/sâu/trụ cả trận của Pro và không tạo vàng từng đường bằng tỷ lệ 25/20/25/25/5.

Mục tiêu phút 10 chỉ phân tích Rank, mỗi trận lấy một phía Blue cố định. Có rồng trước phút 10 không đồng nghĩa ăn rồng đầu tiên. Pro chưa có timeline phù hợp nên trả trạng thái unavailable; không so sánh với tổng mục tiêu cả trận. Dùng Fisher exact cho hai mục tiêu, ngưỡng Bonferroni alpha/2. Các liên hệ vẫn có thể bị nhiễu bởi team/player/patch.

## 3. Huấn luyện và đánh giá

- Chia khoảng 60% train, 10% validation, 10% calibration, 20% test theo nhóm trận. Các trận cùng timestamp Pro không đi qua ranh giới thời gian.
- Pro chia theo ngày sự kiện; rank thiếu timestamp trận nên dùng grouped random seed=42, không gán `crawled_at` thành ngày thi đấu. Vì vậy kết quả rank chưa đo khả năng tổng quát sang tương lai.
- Draft: winrate/matchup/synergy trên train dùng expanding-window encoding 6 block, chỉ tham khảo các ngày trước block hiện tại. Vocabulary chỉ dùng tên tướng, không dùng nhãn. Validation/calibration/test chỉ sử dụng thống kê của train.
- XGBoost CUDA depth 2 và 4, chọn bằng log loss trên validation. Không chọn trên test. Không cam kết accuracy mục tiêu.
- Hiệu chỉnh riêng: chọn alpha trên calibration, `p = alpha*p_model + (1-alpha)*p_train`. Alpha xét trên lưới [0,1] bước .01. Đây là shrinkage xác suất, không phải bằng chứng mọi dự báo đã đúng xác suất.
- Baseline prior và lớp đa số lấy từ train. Snowball có thêm side prior và quy tắc dấu chênh vàng. Quy tắc dấu vàng dùng .75/.25/.5 để tính score, được ghi rõ là quy tắc chưa hiệu chỉnh. Baseline lớp đa số chỉ báo accuracy, không gán xác suất 0/1 để làm đẹp so sánh log loss.
- AUC, accuracy, log loss, Brier và reliability bins trên test. CI95 dùng 300 bootstrap theo toàn bộ trận, không bootstrap từng dòng Blue/Red độc lập. CI chưa mô hình hóa tương quan giữa các trận cùng đội/tuyển thủ.
- Model lưu schema v2, manifest gameid từng tập, fingerprint dữ liệu, cấu hình calibration, thiết bị huấn luyện và kết quả. Script đánh giá từ chối khi fingerprint hoặc số dòng test lệch. Model v1 bị từ chối với hướng dẫn retrain.

Kết quả và baseline hiện tại: [evaluation_report.md](../src/06_machine_learning/evaluation_report.md). Chi tiết máy đọc: `models/*.evaluation.json`. AUC không được diễn giải thành mức tăng tỷ lệ thắng.

## 4. Giới hạn và đánh giá recommender

Ứng viên phải có ít nhất 5 trận tại vị trí/khu vực yêu cầu. Không có dữ liệu thì trả danh sách rỗng, không lặng lẽ thay bằng các tướng định sẵn. Các thành phần có thể gồm lịch sử vai trò, đối thủ cùng đường đã biết, đồng đội và tuyển thủ chỉ định.

Mỗi thành phần có cùng làm mịn Beta(5,5): `(wins+5)/(games+10)`. Điểm là trung bình có trọng số `games/(games+10)` của các thành phần đủ mẫu. Đây là công thức heuristic công khai, các thành phần có tương quan; không dùng CI của riêng một thành phần để tuyên bố CI của điểm tổng hoặc chắc chắn khắc chế.

Benchmark dùng 600 trận test theo thời gian, thống kê chỉ từ 2.400 trận trước cutoff, 6.000 ô cần tìm lại. Che một ô trong đội hình cuối cùng, nhìn thấy chín ô còn lại; so Recall@5, MRR@5 và coverage với baseline phổ biến trên cùng tập ứng viên. CI bootstrap theo gameid. Benchmark không mô phỏng thứ tự pick thật, không biết lượt ban tại thời điểm đó, không coi lựa chọn đã xảy ra là lựa chọn tối ưu, không đo tăng thắng.

Kết quả: [recommender_evaluation.json](../reports/recommender_evaluation.json). Heuristic đang yếu hơn baseline phổ biến về truy hồi; không được mô tả là đã vượt baseline. Các lần cải thiện tiếp theo cần tập validation riêng, không dùng test này để chỉnh tham số rồi tiếp tục gọi là test độc lập.

## 5. Chạy lại

Trong thư mục gốc, dùng `.venv/Scripts/python.exe` trên Windows:

```powershell
.\.venv\Scripts\python.exe src/02_preprocessing/cleaner.py
.\.venv\Scripts\python.exe src/06_machine_learning/draft_model.py --train
.\.venv\Scripts\python.exe src/06_machine_learning/snowball_model.py --train
.\.venv\Scripts\python.exe src/06_machine_learning/evaluate_models.py
.\.venv\Scripts\python.exe src/07_recommender/evaluate_recommender.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Không cần Riot API key để làm sạch/phân tích offline. Crawler vẫn yêu cầu key tại ranh giới gọi mạng. XGBoost pin 3.0.5 để phù hợp driver CUDA 12 của máy hiện tại; không cần nâng driver hệ thống. Kiểm tra cấu hình booster sau fit để ngăn âm thầm chuyển sang CPU.

## 6. Việc còn lại trong lộ trình

Thu thập event timestamp trận rank; timeline mục tiêu Pro; lưu provenance JSON/hash; đánh giá sang patch/thời gian mới; kiểm soát team/player/side/patch và độ lệch chọn mẫu; cải thiện recommender trên validation. API/web, báo cáo cuối kỳ và slide tiếp tục theo roadmap. Fig 10–11 là kết quả phân cụm chuyên gia cũ, chưa huấn luyện lại trong đợt sửa này.


## Bổ sung Chương 6 (2026-11-23)

Content-based đã được triển khai riêng với item/user profiles và cosine similarity. Tham chiếu slide, dữ liệu, công thức và lệnh chạy: [CHUONG_6_CONTENT_BASED.md](CHUONG_6_CONTENT_BASED.md). Benchmark dùng validation theo thời gian; chưa vượt baseline popularity về truy hồi. Đây không phải collaborative filtering hay phép đo tăng tỷ lệ thắng.
