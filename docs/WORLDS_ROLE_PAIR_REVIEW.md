> **Cập nhật hiện hành23/11/2026:** đã chạy5vánFearless và sửa thưởng association ít mẫu: positive log-lift shrink theo số mẫu cặp, negative theo số quan sát đồng đội. Audit mới giữ Recall@5=36%, Recall@1=9.5%,MRR@5=.184, CI mô tả chênh recent[+1.5,+10.2625]điểm phần trăm. Bảng MRR và ví dụ bên dưới là mốc trước sửa này. Pool/evidence tách riêng cho series; báo cáo100lượt/50picks ở [Fearless REPORT](../reports/worlds_fearless_bo5/REPORT.md). 38testsPASS; không có dữ liệu/model mới được fit.

# Worlds: đánh giá phối hợp cho toàn bộ đội hình

Ngày thực hiện: 23/11/2026. Thay đổi áp dụng cho **mọi cặp tướng ở hai vị trí khác nhau**, không có danh sách combo tốt/xấu gán sẵn. Năm vị trí tạo 10 cặp không phân thứ tự (20 chiều truy vấn), bao gồm bot–support, rừng–mid, rừng–top và các cặp còn lại.

## Lỗi trước sửa

Policy chủ yếu cộng điểm riêng của tướng. Thành phần synergy cũ dùng kết quả cả trận của các cặp đủ mẫu; cặp không thấy hoặc ít mẫu nhận giá trị trung tính. Mức phổ biến của tướng có thể lấn át việc cặp gần như chưa được chơi. Thống kê cặp cũ còn chỉ lưu tên đồng đội, không giữ role đồng đội, nên có thể trộn các vị trí flex.

Ví dụ trong dữ liệu local: LCK 2026 Lucian–Milio 63/88 lượt Lucian, Worlds 2026 17/20; Lucian–Shen 0 lượt trong cả hai tập. Không khái quát thành mọi mùa: LCK 2025 local có Lucian–Braum 44/69 lượt. Trong cửa sổ LCK gần nhất: Lucian–Milio26, Yuumi2. Tần suất chỉ là hành vi draft được quan sát, chưa chứng minh tối ưu cơ học hoặc tăng thắng.

## Cơ chế tổng quát mới

`DraftMetaSnapshot` ghép dữ liệu theo **gameid + side**, yêu cầu đủ 5 role duy nhất, giữ cả role và tên của hai tướng. Dùng cùng cutoff, khu vực, patch/window của phiên; không lấy đối thủ làm đồng đội.

Với tướng ứng viên C tại role R và đồng đội A tại role S:

- `n`: số lần cặp C/R + A/S xuất hiện; `N`: số đội có A/S trong dữ liệu hợp lệ.
- Hiển thị n/N và Wilson CI95 cho tần suất ghép cặp; hiển thị riêng winrate/CI cả trận của cặp. Hai khoảng tin cậy này có ý nghĩa khác nhau.
- Tính pick share nền `p(C tại R)` trên các đội có đủ dữ liệu hai role; các tần suất tính điểm có decay thời gian.
- `q(C|A) = (weighted_pair_count + 10*p) / (weighted_anchor_count + 10)`.
- `lift = q/p`: so với mức có thể gặp chỉ vì C phổ biến. Cặp chưa thấy nhưng A đã có nhiều quan sát có lift<1; không mặc định phối hợp tốt. Cặp chưa đủ lịch sử của A được gắn `insufficient_anchor_history`, không tham gia điều chỉnh.
- Lấy trung bình hình học lift với các đồng đội đã chọn, trọng số độ phủ `weighted_anchor_count/(weighted_anchor_count+10)`. Mỗi role/cặp dùng cùng công thức.

Để mức phổ biến riêng không lấn át một cách dễ dàng, association **điều chỉnh odds của điểm ưu tiên**, thay vì chỉ cộng một bonus nhỏ. Gọi b là trung bình các thành phần nền (meta, slot, historical, matchup, winrate cặp, mastery, cosine), L là geometric lift, w là `composition` mặc định1:

`priority = b*L^w / (1-b+b*L^w)`

Đây là phép biến đổi điểm heuristic có miền [0,1], **không phải xác suất thắng**. JSON lưu b, L, w và công thức; `why` giải thích cách tính. Các trọng số và prior là policy công khai, chưa học từ validation. Synergy theo winrate còn giữ trọng số0.25 nhưng đã sửa để không trộn role; không diễn giải winrate như tác động nhân quả.

Mỗi phiên lưu ma trận 10 cặp/đội ở `composition_summary`, phân biệt `observed_pair` (n≥5), `sparse_pair` (0<n<5), `unobserved_pair` (n=0 nhưng anchor đủ mẫu), `insufficient_anchor_history`. Không khóa cứng cặp chưa thấy; đội hình mới vẫn có thể được chọn nếu các bằng chứng khác đủ mạnh.

## Chạy thử Worlds

Gen.G–Bilibili Gaming, cutoff **13/11/2026**, patch **dataset16.20**, 106 ván lịch sử/94 ván patch đích. Không đưa 4 ván chung kết 14/11 vào phiên này. Đây là draft giả định trước chung kết, không phải tái hiện đội hình chính thức hoặc dự báo kết quả trận đã biết.

| Role | Gen.G | Bilibili Gaming |
|---|---|---|
| Top | Ambessa | Gnar |
| Jungle | Pantheon | Lee Sin |
| Mid | Locke | Orianna |
| Bot | Ezreal | Kai'Sa |
| Support | Karma | Nautilus |

Lineup đọc từ trận gần nhất trước cutoff, không gọi là live roster. Phiên này không ép phải chọn Lucian để làm đẹp ví dụ. Dữ liệu và căn cứ: `reports/worlds_draft_role_pairs.json`; kiểm tra hai thứ tự chọn: `reports/worlds_role_pair_checks.json`.

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py --auto --region WLDS --blue-team "Gen.G" --red-team "Bilibili Gaming" --as-of 2026-11-13 --patch 16.20 --save-session reports/worlds_draft_role_pairs.json
```

Bỏ `--auto` để tự điều khiển. `why N` xem căn cứ cặp của ứng viên. `--used-champions` nhập pool bị khóa từ các ván trước; chưa có planner Fearless tự động cho cả series.

## Audit retrieval trên Worlds

Đóng băng trước 20 trận cuối, replay 200 lượt, chỉ dùng thông tin đã lộ; cùng pool ứng viên, cutoff và baseline. Kết quả policy cũ được lưu trước thay đổi. Đây là tập audit phát triển đã được xem trong quá trình làm, không phải final test độc lập.

| Phương pháp | Recall@1 | Recall@5 | MRR@5 |
|---|---:|---:|---:|
| Presence toàn lịch sử | 4% | 29% | 0.1196 |
| Recent presence | 9.5% | 30% | 0.1656 |
| Policy trước sửa cặp | 8% | 30% | 0.1569 |
| Policy có role-pair association | 13.5% | 36% | 0.2123 |

CI95 bootstrap theo ván cho chênh Recall@5 policy mới so với recent presence: **[+1,+12] điểm phần trăm**, 300 mẫu bootstrap. Đây là CI mô tả trong audit nhỏ, chưa phản ánh việc dùng lại tập phát triển hoặc phụ thuộc giữa các ván trong series. Coverage vẫn86%; 14% lựa chọn thực tế ngoài candidate pool. Benchmark chưa dựng lại Fearless pool từ các ván trước. Không đánh giá tác động lên xác suất thắng hay chất lượng lượt cấm.

Chi tiết: `reports/worlds_replay_before_role_pairs.json`, `reports/wlds_draft_policy_evaluation.json`.

```powershell
.\.venv\Scripts\python.exe src/07_recommender/evaluate_draft_policy.py --region WLDS
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Giới hạn kiến thức và hướng tiếp tục

Đây là mở rộng association giữa các item từ hành vi đồng chọn; content-based item/user profile và cosine theo Chương6 vẫn được giữ, không biến cosine thành khả năng phối hợp. Chưa mô hình hóa tương tác ba/năm tướng, điều kiện giao tranh, damage profile, engage/disengage, độ khó vận hành hoặc biến động sức mạnh do patch. Cặp thường chơi có thể do đội/tuyển thủ, phong cách hoặc lịch đấu; cặp mới chưa thấy không đồng nghĩa yếu. Để đi tiếp cần đặc trưng cơ chế tướng có nguồn xác nhận, đánh giá theo series/thời gian và nhiều patch, validation/test độc lập trước khi dùng tìm kiếm sâu.

Kiểm chứng: **35 unit tests PASS**; hai phiên Worlds đổi bên chọn trước đều hoàn thành20lượt/tướng khác nhau, đủ10cặp/đội và có công thức/căn cứ trong JSON. Truy vấn support khi đã có Lucian cho Milio đứng đầu ở cả hai snapshot LCK/Worlds kiểm tra; không ép Lucian xuất hiện trong phiên tự động. Đã cập nhật PROJECT_STATE/TASKS/CHANGELOG/ARCHITECTURE/DECISIONS, README và danh mục modules.
