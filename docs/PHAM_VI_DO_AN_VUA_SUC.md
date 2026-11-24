> **Cập nhật theo yêu cầu rõ của user24/11:** đã bổ sung UI nhỏ React+TypeScript và FastAPI adapter reuse engine, không mở thành nền tảng production. Không thêm mô hình/công thức khoa học. [Phạm vi UI và lệnh chạy](UI_REACT_TYPESCRIPT.md), sổ27/NV-21. Các giới hạn nghiên cứu/globalBO5 bên dưới giữ nguyên.

# Phạm vi đồ án vừa sức môn học

**Bổ sung sau yêu cầu so sánh:** đã có một công thức thử `simple` với ba tín hiệu dễ giải thích, được so với current trên cùng pool và chạy BO5. Simple giảm Recall@5 test từ49.375% xuống42.5%, nên chưa thay mặc định. Xem [bảng giữ/bỏ, kết quả và lệnh demo](TINH_GIAN_DIEM_RECOMMENDER.md), sổ26/MR-23/NV-20. Đây là phép thử được user giao, không phải tự thêm một chiến lược ban hoặc framework mới.

Mốc rà soát:24/11/2026, theo yêu cầu giữ dự án vừa phải, vận dụng các chương đã học và một số mở rộng cần thiết. Tài liệu này là hướng dẫn đọc và giới hạn phát triển hiện hành; các báo cáo nghiên cứu cũ vẫn giữ để truy vết.

## Đánh giá hiện trạng

Luồng dữ liệu sạch, SQL, biểu đồ, mô hình đã đánh giá và minh chứng content-based đủ tạo thành một đồ án có nội dung. Điểm cần cải thiện là phạm vi đã lan rộng sang nhiều nghiên cứu draft và hệ thống thu dữ liệu.

Kiểm kê mã Python trong `src` tại mốc rà soát: pipeline12file/~3.785dòng, recommender19file/~4.505dòng, ML5file/~1.580dòng. Số dòng không đo chất lượng; nó chỉ cho thấy pipeline + recommender đang chiếm phần lớn công sức. Có nhiều collector/evaluator phục vụ các mốc nghiên cứu khác nhau. Không cần phát triển tất cả thành sản phẩm hoàn chỉnh để hoàn thành môn.

Các phần làm sạch, thống kê đối đầu và content-based đang dùng được. Xếp hạng contextual hiện vẫn có công thức kết hợp nhiều thành phần và một số mở rộng tự thiết kế. **Đợt này chưa thay thuật toán xếp hạng đó thành một thuật toán đơn giản hơn**, vì thay điểm cần so sánh lại kết quả; không được chỉ đổi tên thành “trong môn” để coi là đã thu gọn.

## Phạm vi báo cáo chính và demo

| Phần giữ làm cốt lõi | Căn cứ đã đối chiếu | Mức triển khai vừa sức và nơi xem |
|---|---|---|
| Câu hỏi nghiên cứu, số liệu mô tả | Chương1, MH-01..03 | Nêu một mục tiêu chính: hỗ trợ ban/pick dựa trên lịch sử và tương đồng; không hứa tối ưu hoặc tăng thắng |
| Thu/làm sạch dữ liệu | Chương2, MH-04..05 | Dùng luồng sạch chung `analysis_data.py`; giữ dấu âm, missing và nguồn; dữ liệu Rank/Pro riêng |
| Biểu đồ EDA | Chương3, MH-06 | Chọn các hình phục vụ câu hỏi; không bổ sung dashboard phân tích phức tạp |
| Bài toán ML | Chương4, MH-07..09 | Trình bày Draft làm bài toán liên quan trực tiếp ban/pick; Snowball là phân tích bổ sung ở phút10. Chọn một làm bài toán chính, dùng lại kết quả hiện có và công khai chất lượng còn hạn chế; không tạo thêm mô hình |
| Lưu trữ và tổng hợp | Chương5/5x, MH-10..11 | SQLite, SQL, Pandas filter/groupby/merge; một đường chạy dữ liệu chính, không bắt buộc hệ thống phân tán |
| Recommender minh chứng môn học | Chương6, MH-12..14 | `content_based.py`: item profile tướng/role, user profile từ lịch sử pick, min-max và cosine, có baseline. Không bắt buộc thêm collaborative filtering khi content-based đã bám chương |
| Ứng dụng ban/pick | Vận dụng + policy mở rộng | Giữ chọn tay/tự chọn, legacy/contextual và Fearless hợp lệ, giải thích dữ liệu. Gọi đúng là gợi ý dựa thống kê, không tối ưu toàn BO5 |

Chương0 chỉ nêu đề cương Chương1–6, không quy định phải xây một nền tảng Web/API hoàn chỉnh. Sản phẩm hiện tại có thể demo qua Python CLI/notebook, CSV và hình. Giao diện nhỏ chỉ phục vụ nhập lựa chọn/xem gợi ý nếu cần, không mặc định phải bổ sung FastAPI/React/dịch vụ nền.

## Phần mở rộng giữ có mục đích

- Khoảng tin cậy cho winrate và trung bình tài nguyên: giúp đọc đúng dữ liệu ít mẫu. Dùng lại công thức đang có, giải thích ý nghĩa và giới hạn.
- XGBoost/CUDA hiện có: ghi rõ là mở rộng từ nền boosting Chương4; không nhận XGBoost là tên thuật toán được slide dạy nguyên vẹn. Không đổi GPU policy hoặc retrain chỉ để chỉnh phạm vi/tài liệu.
- Policy ban/pick và nguồn dữ liệu: luật draft/Fearless, lọc lịch sử, contextual và nguồn Rank bổ sung. Đây là ứng dụng/thiết kế riêng; không phải mọi công thức đều thuộc Chương6.

Các nhóm trên giúp định hướng trình bày, không xóa sự tồn tại của các mục MR trong sổ kiến thức. Đặc biệt shrinkage/lift/geometric-odds, role-mass và calibration hiện có vẫn là mở rộng khi thực sự được dùng. Nếu không giải thích được một công thức trong báo cáo, ưu tiên đơn giản hóa sau khi kiểm tra thay vì thêm lớp mới.

## Phần để ở phụ lục hoặc lộ trình

| Phần | Trạng thái thật và cách giới hạn |
|---|---|
| `opponent_model.py` | Prototype có tùy chọn gọi, không bắt buộc trong demo chính; không tiếp tục nâng cấp mô hình dự đoán đối thủ ở phạm vi hiện hành |
| Lookahead/tìm cây/global BO5 optimizer | Không phải runtime đang duy trì; không dựng lại |
| `evaluate_rank_transfer.py`, `evaluate_contextual_evidence.py` | Công cụ nghiên cứu nguồn dữ liệu; kết quả thăm dò chưa chứng minh cải thiện, không là điều kiện để hoàn thành đồ án |
| K-Means/PCA archetypes chiến thuật | K-Means/PCA có trong môn, nhưng vector/nhãn chiến thuật dựa metadata chuyên gia và artifact cũ chưa tái nghiệm thu. Để bổ sung, không nhận là học ra counter/chiến thuật khách quan |
| Nhiều collector Rank | Dùng `update_rank_evidence.py` làm lệnh thu hiện hành. Các collector cũ giữ để tái lập và vì có helper được tái sử dụng; không phát triển song song nhiều luồng |
| Thu dữ liệu ngang quy mô U.GG | Không phải tiêu chí nghiệm thu đồ án; không đòi xây hạ tầng tương đương một dịch vụ thống kê lớn |

Không xóa các file nghiên cứu trong đợt rà soát này, vì có phụ thuộc và minh chứng cũ. Không thêm framework, model hoặc profile chạy mới để giải quyết việc thu gọn.

## Tiếp tục phần U.GG và bỏ mốc2.000

Đã bỏ mặc định2.000trận/kèo trong báo cáo và CLI. `target_games`, `games_remaining`, `target_reached` đểnull khi không có mục tiêu; giữ tên cột và tùy chọn cũ chỉ để tái lập lịch sử. Báo cáo tập trung vào n thực, nguồn và độ bất định. N5 vẫn là ngưỡng hiển thị làm việc, không phải bảo đảm chất lượng.

Phân biệt hai mong muốn:

1. Có cách trình bày như U.GG: winrate, GD15, số mẫu và bộ lọc — dự án đã có dạng thống kê này.
2. Có cùng số trận/độ phủ/chất lượng như U.GG — chưa xác minh, vì chưa nạp được bộ tham chiếu theo cùng bộ lọc. Lần thử trước metadata truy cập được, trang và JSON matchup trả403. Không bịa số tham chiếu hoặc nhận kết quả của họ thành mẫu tự thu.

Nguồn ngoài nếu truy cập và dùng được sẽ được ghi thành nguồn thống kê riêng; không cần tự thu lại tất cả các trận của họ. Hiện chưa tạo adapter U.GG hoặc cam kết tái tạo thuật toán nội bộ. Bước thu gọn này không thêm một hệ thống scraping phức tạp.

## Quy định cho lần làm tiếp

Mỗi thay đổi chọn một vấn đề cụ thể và ưu tiên giải pháp từ bài học hoặc thư viện đã dùng. Chỉ thêm mở rộng khi chỉ ra lợi ích đo được hoặc nhu cầu đã được giao, cùng cách giải thích, vị trí dùng và output trong sổ kiến thức. Ưu tiên sửa/làm rõ cái đang có; không tự mở rộng mô hình, số mode, API/Web stack hoặc nghiên cứu BO5.

Các bước tiếp theo hợp lý là chốt một đường demo, kiểm tra người dùng đọc được bảng giải thích, và hoàn thiện báo cáo. Nếu tinh giản công thức xếp hạng hiện có thì làm thành thay đổi riêng với baseline; không âm thầm đổi điểm trong lúc sửa mục tiêu thu dữ liệu.

Sổ kiến thức [mục25/NV-19](TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md) ghi thay đổi phạm vi, output và kiểm chứng. Đây là chính sách do người dùng yêu cầu, không phải lý thuyết nâng cao mới.
