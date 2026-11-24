# UI gọn, tự xếp đường và kiểm tra kèo đã lộ

Cập nhật 24/11/2026 theo ba yêu cầu UI/Galio/First Selection và phản hồi về Renekton. Phân loại: **NV-24 và sửa policy review MR-12**; không thêm model, framework hay dữ liệu huấn luyện mới.

## Thao tác trên UI

- Thiết lập phiên và chuyển ván nằm trên đầu trang. Hai bảng đội hình giữ bố cục cũ ở giữa, mỗi đội5vị trí xếp dọc; **gợi ý dọc bên trái, bảng đội hình ở giữa, chọn tướng dọc bên phải**, cả ba cùng hàng trên desktop từ900px; phần Hiểu lựa chọn ở dưới. Màn hình nhỏ xếp thành một cột.
- Khi chọn tướng bằng khu Chọn tay, không cần chọn role. Hệ thống đếm số lần tướng được chơi ở từng role trong **snapshot Pro của phiên**, lấy role phổ biến nhất còn trống; nếu đã có tướng thì lấy role tiếp theo. Preview hiển thị role và số lần quan sát trước khi xác nhận.
- Hòa số mẫu được xử lý ổn định theo thứ tự role Top/Jungle/Mid/Bot/Support. Chỉ dùng role có ít nhất một quan sát. Nếu không còn role đã quan sát nào trống, hệ thống yêu cầu tạo chỗ bằng đổi đội hình hoặc chọn tướng khác; không bịa ra role phổ biến thứ hai có số mẫu0.
- Kéo tướng trên bảng đội hình đến role trống để chuyển đường, hoặc đến role đã có tướng để đổi chỗ. Chỉ áp dụng trong cùng đội, ván đang thao tác. Menu đổi đường vẫn có cho bàn phím/màn hình chạm; không nhận đã có drag bằng cảm ứng.
- Tự xếp đường là tiện ích cho **tướng do người dùng chọn**, không phải xác nhận đường đó tối ưu trong kèo. Chọn tay vẫn được phép chấp nhận rủi ro; tự chọn tướng bằng engine có gate review riêng.
- Lịch sử20lượt giữ thứ tự cấm/chọn thật. Đổi đường được lưu bằng swap; không sửa lại lịch sử để làm như tướng đã được pick ở lượt khác.

## Galio gặp Ambessa: lỗi đã xác định

Trong phiên lưu ở `reports/pair_reservation_revision/same_prefix_completed.json`, Red chọn Ambessa Top ở lượt17, Blue chọn Galio Top ở lượt19, tức pick thứ9 toàn trận. Red lúc đó có4tướng. Gate trước đây chờ đủ5tướng địch mới chặn thiếu bằng chứng nên bỏ lọt tình huống này.

`draft_safety.annotate_lane_support` hiện tra trực tiếp cặp **role đang gán**: Galio Top–Ambessa Top. Số mẫu dưới ngưỡng hiện hành5 sẽ có `lane_review.requires_review=true`; auto phải dừng để xem lại ngay khi đối thủ cùng role đã lộ. Không cần chờ cả đội hình5tướng. Blind pick chưa có đối thủ cùng role không bị gán thành kèo0mẫu đã quan sát.

Khi so trong role được lọc hoặc khi mọi role mình còn trống đều đã có đối thủ cùng role, thứ tự dùng:

1. Wishlist của người dùng và lớp ứng viên đủ mẫu tổng thể như trước.
2. Ràng buộc giữ cặp bot đã có.
3. **Sửa v3 sau phản hồi Milio:** chỉ tách kèo đủ ngưỡng5mẫu khỏi nhóm chưa đủ mẫu, rồi dùng điểm tổng gốc và tie-break cũ trong mỗi nhóm. Không dùng Wilson để xếp hạng; các kèo0–4mẫu cùng nhóm, không để một trận thắng đẩy tướng lên trên chỉ nhờ cận dưới cao hơn. Wilson vẫn hiển thị để tham khảo. Có đủ mẫu cũng không chứng minh kèo có lợi.

Không tự coi role còn blind là tốt hơn role đã lộ địch. Trong trạng thái nhiều role mở mà đối thủ chưa lộ hết các role tương ứng, không dùng tiêu chí này để đẩy tất cả blind role lên đầu. Gate thiếu mẫu vẫn áp dụng cho tướng được auto chọn.

Wilson và ngưỡngn5 là phương pháp đã có trong dự án. Đây là policy thứ tự do nhóm thiết kế theo phản hồi, **không chứng minh counter cơ chế hoặc tối ưu chiến thuật**. Ít hơn5mẫu vẫn cần review, kể cả có cận dưới tốt hơn ứng viên khác. Test override vẫn cho đi tiếp và giữ nhãn; chọn tay không bị cấm.

## Vì sao Renekton từng xếp cuối?

Ở đúng snapshot này:

| Kèo với Ambessa Top | Số trận Pro | WR cả trận | CI95 Wilson | GD15 trung bình | CI95 mean GD15 |
|---|---:|---:|---|---:|---|
| Galio | 0 | — | — | — | — |
| Gnar | 6 | 83.3% | 43.6–97.0% | +686 | +283…+1.089 |
| Renekton | 2 | 100% | 34.2–100% | +787 | +520…+1.054 |

100% là2/2, không phải xác suất thắng được xác nhận. Khoảng tin cậy còn rộng và chồng lấn với Gnar; chênh trung bình vàng không chứng minh Renekton vượt trội. Từng metric vẫn có số mẫu riêng; không suy số đo từ kết quả thắng.

Điểm cũ còn xét meta, lịch sử, hồ sơ nội dung và phối hợp toàn đội. Renekton có effective composition lift khoảng0.718, Gnar0.940, Galio1.045 nên thứ tự cũ chịu ảnh hưởng của association này; đó không phải bằng chứng cơ chế phối hợp. WR kèo Renekton chỉ2mẫu chưa vào phần đối đầu đủn5; vàng/XP/CS đầu trận hiện **là bảng giải thích**, chưa phải đầu vào điểm tổng.

Bản v2 từng dùng Wilson trước điểm tổng và đưa Renekton lên thứ2; đã thay vì làm các kèo rất ít mẫu đảo thứ tự điểm tổng. **Hiện hành v3:** Gnar6mẫu đứng trước, nhóm còn lại đều thiếu5mẫu được xếp theo điểm gốc: Galio, Camille, K’Sante, Renekton. Galio/Renekton vẫn cần review trước auto; không gọi bất kỳ tướng nào trong nhóm này là counter được xác nhận. Thẻ hiện số mẫu kèo/WR/CI/GD15 và “điểm gốc”, nhãn “Kèo đủ mẫu” hoặc “Giữ cặp trước ban” nếu có ưu tiên riêng. Khi tất cả kèo đều thiếu mẫu và cùng lớp ứng viên/pairpriority, thứ tự theo điểm gốc. Không cộng vàng vào score hoặc ép tên tướng đứng đầu.

## First Selection

Blue hoặc Red có thể chọn trước mọi ván theo lựa chọn người dùng, kể cả cùng một bên5ván liên tiếp. UI có bộ chọn và nút Sang ván ở phần thiết lập trên đầu. Màu đội giữ nguyên, không tự suy từ kết quả trận hay luân phiên.

**CLI cho series nhiều ván nay bắt buộc `--first-picks`**; đã bỏ cả fallback luân phiên cũ. Ví dụ:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-24 --games 5 --ban-strategy contextual --first-picks blue,blue,blue,blue,blue --allow-statistical-auto --output-dir reports/ui_lane_revision/bo5_blue_first
```

Đổi chuỗi thành `red,red,red,red,red` nếu muốn Red cả5ván. Mỗi phần tử ứng với mộtván. Mộtván không chỉ định vẫn dùng defaultBlue; nhiềuván thiếu danh sách bị từ chối. Đây là luật phiên theo yêu cầu người dùng, không khẳng định mọi giải chính thức áp dụng như vậy.

## Truy vết

- `draft_safety.py`: `role_preferences/infer_free_role` dùng tần suất và lọc slot trống (vận dụng Chương1/5x); `annotate_lane_support` dùng `enemy_evidence`/Wilson hiện có và policy review MR-12 tự thiết kế.
- `simulate_draft_match.py`: gate auto và comparator theo role đã lộ, lưu `lane_review`/version; điểm current, weights, BanPlanner và Rank score không đổi.
- `src/api/app.py`: role preview, infer role khi request chọn tay thiếu role, whitelist và fingerprint thêm `lane_review_policy/manual_role_policy`; cùng snapshot cho preview và commit.
- `App.tsx/styles.css`: bố cục gọn, auto-role preview, drag/drop cùng đội, dữ liệu thẻ và inspector phía dưới. React/TS và native drag/drop là kỹ thuật ngoài môn NV-24; không thêm thư viện.
- [Báo cáo và kiểm tra](../reports/ui_lane_revision/REPORT.md), [audit kèo/điểm](../reports/ui_lane_revision/lane_audit.json), [ảnh](../reports/ui_lane_revision/lane-audit.png), [BO5Blue5ván](../reports/ui_lane_revision/bo5_blue_first/REPORT.md).

Mục30 trong sổ kiến thức ghi minh chứng thực thi. Không retrain, không sửa SQLite Pro hoặc collector Rank; không gọi regression này là đánh giá chất lượng chiến thuật độc lập.

**Chỉnh trình bày mới nhất:** [hai bảng căn giữa như cũ](../reports/ui_centered_board/REPORT.md), phần xung quanh vẫn theo yêu cầu. Không đổi score/rolepolicy hoặc API.

**Làm rõ bố cục hiện hành:** [Gợiý | Độihình | Chọntay cùnghàng](../reports/ui_flanking_choices/REPORT.md).

**Sửa responsive mới nhất:** [ba cột cùng hàng từ900px, kiểm7kíchthước](../reports/ui_sidebars_fit/REPORT.md).

**Hiểu lựa chọn — thao tác hiện hành:** ẩn mặc định. Bấm một tướng ở gợiý/chọntay để mở; bấm lại đúng tướng để bỏchọn vàẩn. NútĐóng thu phầngiảithích nhưnggiữlựachọn, cóthểMởlại; khi bỏchọn thì khôngcònnútmở. Sanglượt/đổiván/reloadkhôngtựmở. [Minhchứng7Edge tests](../reports/ui_inspector_toggle/REPORT.md). Khôngđổiđiểmgợiý.

**Thu gọn toàn bộ phần giải thích:** bấm “Thu gọn toàn bộ” trên tiêu đề để ẩn cả nội dung/bảng nguồn, chỉ giữ một thanh nhỏ; phần Diễn biến lập tức dịch lên. Bấm “Mở rộng” để xem lại, không mất tướng đang chọn. [Kiểm tra](../reports/ui_inspector_collapse/REPORT.md).

**Thu gọn toàn bộ phần giải thích:** bấm “Thu gọn toàn bộ” trên tiêu đề để ẩn cả nội dung/bảng nguồn, chỉ giữ một thanh nhỏ; phần Diễn biến lập tức dịch lên. Bấm “Mở rộng” để xem lại, không mất tướng đang chọn. [Kiểm tra](../reports/ui_inspector_collapse/REPORT.md).
