# Hai chiến lược hiện hành: legacy và contextual

**Cập nhật24/11/2026:** theo yêu cầu người dùng, chỉ duy trì hai chế độ này. Lookahead đã được gỡ khỏi mã tìm kiếm ban, CLI và luồng so sánh hiện hành. Các báo cáo cũ giữ làm lịch sử; không tiếp tục dùng chúng để đánh giá phiên bản hiện tại.

## Legacy

- Nơi dùng: `DraftAdvisor.recommend_bans` trong `src/07_recommender/draft_advisor.py`.
- Chấm theo presence gần đây, điểm ưu tiên của đối thủ và chênh lệch lựa chọn thay thế.
- Công thức hiện có: `0.6*presence + 0.25*enemy_priority + 0.15*min(1,denial_loss)`.
- Giữ làm baseline và mặc định của CLI để tái lập lệnh cũ. Có thể lặp ban khi dữ liệu/pool ưu tiên chưa thay đổi.

## Contextual

- Nơi dùng: `BanPlanner.contextual/recommend` và `ContextualBanPolicy` trong `src/07_recommender/ban_planner.py`.
- Dùng bảng chọn của từng role/tuyển thủ ở cả hai đội; lọc tướng đã khóa bởi Fearless, đã ban/pick và lựa chọn được bảo vệ.
- Giá trị pool mỗi role là trung bình điểm tối đa3ứng viên đầu, ưu tiên lớp có đủ mẫu trước lớp ít mẫu. Tính loss khi loại từng ứng viên ban, theo cả pool địch và pool mình.
- Chi phí tự cấm = loss pool mình ×1 nếu mình lấy lượt pick tiếp trước địch, ×0.5 nếu lấy sau. Thứ tự lấy tướng đọc từ lịch draft, độc lập màuBlue/Red.
- `contextual_score = (sum(enemy_role_loss) - own_cost_weight*sum(own_role_loss)*access_factor)/5`. Mặc định own_cost_weight1; trọng số chung do nhóm thiết kế, chưa tune bằng benchmark chiến thuật độc lập.
- Xếp hạng một bước, **không dự đoán hoặc duyệt nhánh phản ứng**. Không có bonus ép các ván phải ban khác nhau, không có case theo tên tướng.
- Đầu ra ban: `pool_impact` ghi role/backup/số lựa chọn/value trước-sau; `contextual_trace` ghi trạng thái đã lộ, danh sách ứng viên/điểm và latency. Không còn `search_trace`, branches hoặc sensitivity của cây tìm kiếm trong kết quả mới.

## Chạy và đọc kết quả

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --ban-strategy legacy --output-dir reports/legacy_contextual_comparison/legacy
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --ban-strategy contextual --output-dir reports/legacy_contextual_comparison/contextual
.\.venv\Scripts\python.exe src/07_recommender/compare_ban_strategies.py
```

`--allow-statistical-auto` giữ yêu cầu test trước đó: thiếu tin cậy vẫn chọn gợi ý1, ghi nhãn thay vì nâng độ tin cậy. Bỏ flag thì gate xem lại chiến thuật có thể dừng series. Không có kết quả thắng/thua hoặc tỉ số giả lập để ép đi đủ5ván.

- [So sánh chỉ legacy/contextual](../reports/legacy_contextual_comparison/COMPARISON.md).
- [Legacy: bảng100lượt](../reports/legacy_contextual_comparison/legacy/QUICK_VIEW.md).
- [Contextual: bảng100lượt](../reports/legacy_contextual_comparison/contextual/QUICK_VIEW.md).
- [Contextual: căn cứ từng lượt](../reports/legacy_contextual_comparison/contextual/REPORT.md).

Các file `series.json`, `game_1.json`…`game_5.json` và log nằm cạnh report; `comparison.json` chứa metric/giới hạn. Ban1–5/Pick1–5 của từng đội vẫn giữ số thứ tự toàn cục và role.

## Kiến thức và giới hạn

Nền MH/UD: Chương1 thống kê/xác suất; Chương5x lọc/groupby; điểm chọn vẫn có content-based Chương6 và thống kê trận trước. MR: hai công thức xếp hạng/pool loss/self-denial do nhóm thiết kế, không phải công thức nguyên bản trong slide. NV: CLI, khóa Fearless, trace và báo cáo.

Điểm ban khác nhau hoặc ban bớt lặp không chứng minh chiến thuật mạnh hơn. Contextual chưa có evaluator cơ chế counter, chưa tự tìm nhiều nhánh flex và chưa tối ưu để dành tướng cảBO5. Phần đối thủ-model đã có từ trước được giữ độc lập, không được contextual gọi để chấm ban. Không fit lại model hoặc sửa DB trong đợt bỏ lookahead này.
