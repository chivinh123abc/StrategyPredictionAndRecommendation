# Rà thành phần điểm và thử công thức đơn giản

Mốc24/11/2026. Đã thử đúng một công thức đơn giản, so trên cùng lịch sử và candidate pool, rồi chạy BO5 minh họa. **Chưa thay mặc định**, vì bản đơn giản giảm khả năng truy hồi pick đã quan sát.

## Rà tám thành phần hiện tại

| Thành phần hiện tại | Cách dùng và trọng số cũ | Căn cứ | Trong bản đơn giản |
|---|---|---|---|
| Meta | Presence gần đây, có decay;1.0 | Đếm là Chương1/5x; cửa sổ/decay là MR-01 | Thay bằng số lần chọn tướng đúng role chia số lần của tướng được chọn nhiều nhất cùng role; không cộng presence có decay |
| Draft order | Ưu tiên slot có prior10;1.0 | Policy MR-05 | Bỏ phần cộng điểm, giữ đúng lịch và luật draft |
| Historical | Cận dưới Wilson của WR theo role;0.25 | Thống kê Chương1, Wilson MR-02 | Không là thành phần riêng; WR lịch sử chỉ fallback khi thiếu đối đầu |
| Matchup | Residual so WR nền, shrink n/(n+10), suy role và xét cả đội địch;0.5 | Đếm/ghép là Chương1/5x; suy role/shrink/kết hợp là MR-04/05 | Dùng raw team WR đối đầu cùng role khi n>=5; trung bình theo xác suất role nếu flex; thiếu thì fallback có nhãn |
| Synergy | Residual WR đồng đội có shrink;0.25 | Thống kê lịch sử + policy mở rộng | Bỏ điểm; không nhận cặp đồng đội là cơ chế phối hợp đã được xác nhận |
| Composition | Co-pick với prior, lift, geometric mean và biến đổi odds;1.0 | MR-03 tự thiết kế, không phải nguyên công thức Chương6 | Bỏ khỏi điểm; bảng cặp đội hình sau draft chỉ tham khảo |
| Mastery | Tỷ trọng chọn của tuyển thủ có decay;0.5 | Tần suất + MR-01/05; không phải mức thành thạo thật | Bỏ điểm riêng; lịch sử tuyển thủ vẫn dùng lập user profile content-based |
| Content | Cosine từ item/user profile;0.1 | MH-05, MH-12/13: Chương2 và6 | Giữ cosine thành một tín hiệu; không có profile thì bỏ thành phần, không gán similarity0 giả |

Như vậy cơ sở từ môn được giữ là thống kê/ghép nhóm, hồ sơ item/user và cosine. Các luật role, draft, Fearless cần cho bài toán ứng dụng. Khoảng tin cậy cần để giải thích số liệu ít mẫu. Chưa thể kết luận mọi công thức mở rộng hiện tại đều cần, hoặc có thể bỏ hết mà chất lượng không đổi.

## Công thức thử nghiệm

Trong `draft_advisor.py`, `AdvisorPolicy.scoring='simple'` chọn `_simple_rows`:

1. `frequency = số lượt chọn tướng/role / max số lượt chọn cùng role` trong snapshot lịch sử đóng băng. Đây là phép đổi thang đơn giản do dự án chọn, không gọi là mô hình meta mới.
2. `content = cosine(item profile, user profile)` khi có hồ sơ hợp lệ.
3. Khi đã lộ địch, `matchup` là trung bình WR cùng role của các kèo có n>=5, trọng số là xác suất role đã có. Nếu không có kèo đủ mẫu, dùng WR lịch sử chung của chính tướng/role và ghi `historical_role_winrate_fallback`.
4. Điểm cuối là trung bình cộng các tín hiệu hiện có, mỗi tín hiệu trọng số1. Khi chưa lộ địch thì không tạo matchup; khi thiếu cosine thì mẫu số giảm. Đây là lựa chọn policy đơn giản, chưa tối ưu; mẫu số khác nhau giữa các ứng viên là một giới hạn.

Điểm không phải xác suất thắng, không có uplift. N5 chỉ là ngưỡng làm việc. Raw WR vẫn chịu ảnh hưởng đội/người chơi/patch và số mẫu. Simple chỉ chấm đối đầu cùng role, không chấm tương tác với bốn vị trí khác hoặc synergy; không được gọi là “đã xét tốt toàn đội địch”.

Suy role flex, lọc patch/cutoff, cửa sổ60ngày, time-decay dùng trong role-mass và luật loại trừ vẫn dùng chung với bản hiện tại để so sánh công bằng. Do đó **chỉ công thức chấm điểm được rút gọn**, không khẳng định toàn bộ hệ thống đã trở thành thuần kiến thức trong môn. Candidate factory lịch sử vẫn được tái sử dụng; điểm sơ bộ của factory không được dùng làm điểm cuối simple.

Không tạo framework/model mới hoặc thêm chiến lược ban. Chỉ thêm một tùy chọn công thức để so sánh và tái lập; legacy/contextual vẫn là hai chiến lược ban hiện hành. Mặc định của CLI và `AdvisorPolicy` vẫn là `current`.

Phạm vi rút gọn là **điểm pick**. Contextual ban vẫn dùng phép đo mất pool đối thủ và chi phí tự mất tướng hiện có; không khẳng định cả ban/pick chỉ còn ba phép tính. Điểm pick đổi có thể làm ban đổi vì ban planner sử dụng bảng xếp pick, dù công thức ban không đổi.

## So sánh thực tế

`compare_pick_scoring.py` dùng lại `draft_states`, `split_series`, phép đo và bootstrap có sẵn. Dữ liệu Worlds16.20 chia theo series/thời gian60/20/20. Pro history gồm các trận đã kết thúc trước validation; đóng băng cho cả hai phần đánh giá. Không dùng Rank hoặc tài nguyên trong chính trận query để tạo feature draft. Công thức cố định trước phép so sánh, không tune sau khi xem test.

Hai bản dùng cùng snapshot, roster từ lịch sử, suy role, ngưỡng ứng viên5, bans/picks đã lộ và khóa Fearless. Từng query kiểm đúng cùng tập `(role, champion)` và lưu hash pool để đối chiếu. Bảng recent_presence là baseline bổ sung dùng cùng pool. Tướng thật ngoài pool vẫn bị tính miss; không bỏ query khó để tăng metric.

| Tập | Số lượt chọn | Current Recall@5 | Simple Recall@5 | Current MRR@5 | Simple MRR@5 |
|---|---:|---:|---:|---:|---:|
| Validation |200|0.5150|0.4250|0.2728|0.2256|
| Test |320|0.49375|0.4250|0.3026|0.2334|

Test có cùng candidate coverage0.76875. Chênh Recall@5 simple-current =-0.06875, CI95 bootstrap theo10series khoảng[-0.11034,-0.03235]. Kết luận ở phép so sánh này: giảm6.875điểm phần trăm về truy hồi, nên giữ công thức mặc định. Đây không phải đo chênh xác suất thắng.

Dữ liệu Pro này đã dùng trong các audit trước; không gọi đây là final test độc lập mới. Series là tái dựng từ nguồn, chưa xác thực ID giải chính thức. Không suy kết quả truy hồi thành chất lượng chiến thuật hoặc khắc chế cơ chế.

## Thành phần nào có bằng chứng hữu ích?

`component_audit.csv` bỏ lần lượt từng thành phần của **current** trên cùng tập ứng viên, không tune lại trọng số. Trên320query test:

| Thành phần bị bỏ | Top1 đổi | Số hit Recall5 current nhiều hơn bản bỏ thành phần |
|---|---:|---:|
| Meta |137|8|
| Draft order |27|3|
| Historical |39|-2|
| Matchup |17|1|
| Synergy |7|0|
| Composition |78|12|
| Mastery |96|3|
| Content |18|-2|

Số âm nghĩa bản bỏ thành phần có nhiều hit hơn ở mẫu này. Không được kết luận cosine “sai” hoặc mọi thành phần dương đều bắt buộc. Tín hiệu phụ thuộc nhau và đang dùng trọng số cũ. Synergy là ứng viên đáng xem lại nếu có đợt tinh giản khác; đợt này không dùng test để tạo thêm nhiều phiên bản rồi chọn bản thắng. Meta/composition/mastery cho thấy bỏ đồng loạt có thể mất thông tin hữu ích, giải thích một phần vì sao simple giảm kết quả; đây vẫn là quan sát có điều kiện.

## BO5 minh họa đã chạy

T1–Gen.G, WLDS, snapshot patch16.20 tới14/11 và yêu cầu as_of24/11; không gọi là live meta. Dùng contextual ban và simple pick; đội ở Blue/Red cố định, quyền chọn trước luân phiên chỉ để demo.

Đã đủ5draft/100lượt/50tướng pick không lặp. `REPORT.md` liệt kê toàn bộ Ban1..5/Pick1..5 mỗi đội mỗi ván, thứ tự toàn cục và bảng lý do/điểm thành phần.5pick là ứng viên dưới ngưỡng5trận;44/50pick thiếu đối đầu cùng role đủ mẫu nên dùng fallback lịch sử. Các trường hợp này được ghi rõ, không nâng thành counter đáng tin.

Demo dùng `--allow-statistical-auto` để chọn số1 khi thiếu bằng chứng, đúng mục đích thử đủ5ván. Không tạo tỉ số trận, winner hoặc kết quả chiến đấu giả. Luật Fearless giữ khóa0/10/20/30/40tướng trước mỗi ván; ban thường reset. Validation kiểm đúng20action,5ban/5pick mỗi đội, đủ5role và không ban/pick lại tướng đã bị khóa.

## File kết quả và lệnh chạy

- [So sánh](../reports/pick_scoring_comparison/REPORT.md): `evaluation.json`, `queries.json` với1.560records cho520query ×3cách xếp, `component_audit.csv`, `checks.json`, `tests.log` cùng folder.
- [BO5 đầy đủ](../reports/simple_scoring_bo5/REPORT.md): `series.json`, `game_1..5.json` và log tương ứng. JSON giữ lý do, thành phần, phạm vi matchup và bảng Pro/Rank nếu đã có.
- [Kiểm chứng](../reports/pick_scoring_comparison/checks.json):146unit testsPASS, cùng role-pool theo từng query, split disjoint/frozen, dựng lại điểm trung bình, draft/Fearless hợp lệ và DB hash không đổi.

```powershell
.\.venv\Scripts\python.exe src/07_recommender/compare_pick_scoring.py
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-24 --patch 16.20 --games 5 --ban-strategy contextual --pick-scoring simple --allow-statistical-auto --output-dir reports/simple_scoring_bo5
```

Không retrain, thay SQLite, đổi default hoặc tự phát triển thêm mô hình. Kiến thức/phần giữ-bỏ/output được cập nhật tập trung ở sổ mục26/MR-23/NV-20. Simple là minh chứng thử nghiệm và demo vừa sức; hiện chưa đủ căn cứ thay bản chính.
