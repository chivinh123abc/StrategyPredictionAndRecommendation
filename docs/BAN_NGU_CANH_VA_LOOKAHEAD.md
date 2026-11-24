> **LỊCH SỬ — đã ngừng sử dụng24/11/2026.** Lookahead đã được gỡ theo yêu cầu người dùng; tài liệu/đầu ra này chỉ giữ minh chứng phiên cũ, không phải chức năng hiện hành. Xem `reports/legacy_contextual_comparison/COMPARISON.md` và `docs/BAN_LEGACY_VA_CONTEXTUAL.md` cho phạm vi mới.

# Ban theo ngữ cảnh và xét nhánh phản ứng — 24/11/2026

Đã triển khai ba phần được giao: (1) điểm cấm theo ngữ cảnh hai đội, (2) xét một số nhánh phản ứng tiếp theo, (3) chạy đối chiếu T1–Gen.G đủ5draft với cách cũ. Mục tiêu là làm các lượt cấm phụ thuộc vào tình huống thực tế; không ép mỗi ván phải có các tướng cấm khác nhau.

## 1. Trước và sau thay đổi

| Thành phần | Cách cũ (`legacy`) | Ngữ cảnh (`contextual`) | Xét nhánh (`lookahead`) |
|---|---|---|---|
| Mục tiêu | Presence + ưu tiên đối thủ + gap | Giảm pool đối thủ, trừ chi phí tự cấm | Giá trị dự kiến sau rollout + một phần điểm ngữ cảnh |
| Bên lấy tướng trước | Chỉ gián tiếp qua slot | Đọc lượt pick kế tiếp từ lịch thật | Thực hiện đúng lịch trong từng nhánh |
| Bể tướng | Tín hiệu mastery trong điểm chọn | Dùng điểm của từng tuyển thủ ở cả hai đội | Giữ cùng bộ chấm điểm trong rollout |
| Fearless | Loại tướng đã dùng | Loại tướng và tính lại pool/backup theo role | Mọi nhánh giữ nguyên pool đã khóa |
| Đội mình định lấy gì | Không tính chi phí ban tướng mình cần | Cấm tướng làm mất backup/tướng ưu tiên của mình có chi phí | Rollout cho thấy lựa chọn nào có thể còn/mất |
| Phản ứng đối thủ | Không rẽ nhánh | Chỉ điểm tại trạng thái hiện tại | Tối đa2phản ứng ở lượt đầu của đối thủ; các lượt tiếp đi greedy |

Không có bảng ban theo số ván, penalty cho tướng bị cấm lặp hoặc case riêng theo tên tướng/đội tuyển. Ván thay đổi vì thứ tự lấy tướng, lựa chọn trước đó, bể tướng, pool và backup thay đổi. Nếu cùng một ban vẫn tốt theo mục tiêu thì được phép lặp.

## 2. Công thức và chức năng

Hiện thực: [ban_planner.py](../src/07_recommender/ban_planner.py), `BanPlanner` và `BanSearchPolicy`.

### Pool và điểm cấm theo ngữ cảnh

1. Với mỗi role còn trống của mỗi đội, lấy danh sách hợp lệ từ `DraftAdvisor.recommend_picks`, dùng tuyển thủ của đội đó, đồng đội/địch đã lộ và slot tiếp theo. Điểm có meta, lịch sử, cosine và association như ranker đang có. Không đưa lượt chọn tương lai thật vào đầu vào.
2. Ưu tiên lớp có đủ5trận; chỉ backoff lớp ít mẫu nếu role không còn lựa chọn đủ mẫu. Tướng đã dùng trong series, đã cấm/chọn trong ván hoặc bị người dùng bảo vệ không được ban ở root.
3. Giá trị pool một role là trung bình điểm của tối đa3ứng viên đầu. Tính mức giảm giá trị khi loại ứng viên ban C, cho cả mình và địch. Số lựa chọn trước/sau và các backup cụ thể được lưu.
4. Chi phí tự cấm bằng loss pool mình nhân1 nếu mình lấy lượt pick kế tiếp trước địch, nhân0.5 nếu địch lấy trước. Đọc từ lịch `DraftState.schedule`, bao gồm pha2 và Red-first, không đồng nhất Blue với first-pick.
5. `contextual_score = (enemy_pool_loss - own_access_cost) / 5`. Mẫu số5 cố định theo số role. Chi phí/trọng số là policy chung do nhóm thiết kế, chưa được tune độc lập. `enemy_role_scarcity` dùng số lựa chọn còn lại để giải thích và xử lý hòa điểm, không là tier theo tên.

Pool tính trên catalog có dữ liệu, chưa đại diện toàn bộ champion hợp lệ chính thức. Điều này có thể làm phóng đại sự khan hiếm nếu champion mới/flex ít mẫu không lọt pool.

### Xét nhánh phản ứng giới hạn

`lookahead` lấy tối đa6ứng viên đầu theo điểm ngữ cảnh, thử ban từng ứng viên trên bản sao trạng thái. Sau đó:

- Theo lịch thật đến lượt đầu tiên của đối thủ. Nếu có lượt liên tiếp của đội mình trong pha2 thì thực hiện các lượt đó bằng policy ngữ cảnh trước khi rẽ nhánh.
- Dùng `OpponentModel` đã lưu để xếp hạng phản ứng hợp lệ trong pool hiện tại, lấy tối đa2phản ứng khác tướng. Role flex của cùng một tướng không được tính thành hai khối xác suất. Không train hoặc fit lại model.
- Nếu không cấp model hoặc model không phủ hành động nào trong pool thì dùng softmax điểm ngữ cảnh làm proxy phản ứng và ghi nguồn fallback. Đây không phải xác suất hành vi được hiệu chỉnh.
- Sau nhánh phản ứng đầu tiên, đi tiếp greedy bằng điểm ngữ cảnh/điểm chọn, đến khi thực hiện3lượt pick mới hoặc đạt12hành động, hoặc hết draft. Không tiếp tục rẽ ở mọi lượt, nên đây **không phải full expectimax/minimax**.
- Đánh giá leaf: `(tổng điểm các pick mới đã lấy + tổng giá trị pool role còn trống)/5` của mình, trừ giá trị tương ứng của địch. Các pick đã có trước root giữ nguyên trong ngữ cảnh chấm điểm, không cộng lại thành phần secured. Điểm của pick mới được chốt tại thời điểm giả định chọn. Leaf không mô phỏng kỹ năng/combat hoặc kết quả trận.
- `ban_priority = expected_leaf_proxy + 0.25*contextual_score`. Expected chỉ chuẩn hóa trên các nhánh được giữ lại. Lưu cả tổng xác suất model nằm trong pool hỗ trợ, khối được giữ, khối bị cắt và xác suất có điều kiện để người đọc không nhầm đây là kỳ vọng toàn bộ phản ứng.

Budget mặc định trong `BanSearchPolicy`: root6, response2, pick-horizon3, max-plies12, top-pool3, own-cost-weight1, contextual-weight0.25. Không tune sau khi nhìn kết quả thực nghiệm này.

### Độ bất định do cắt nhánh

Với q là khối phản ứng được giữ trong pool hỗ trợ, giá trị có điều kiện v và leaf trong[-1,1], lưu khoảng nhạy `[q*v-(1-q), q*v+(1-q)]`. Đây là **khoảng nhạy đối với phần phản ứng chưa xét**, không phải confidence interval thống kê hoặc khoảng xác suất thắng. Khi q thấp, khoảng rộng và lựa chọn gốc có thể thay đổi nếu mở thêm nhánh.

Nguồn khái niệm ngoài môn: [Stanford CS221, Games II](https://web.stanford.edu/class/archive/cs/cs221/cs221.1196/lectures/games2-6pp.pdf), phần depth-limited search và evaluation function. Tài liệu giải thích vì sao cần giới hạn tìm kiếm và evaluator; **công thức pool, chi phí tự cấm và leaf LMHT là thiết kế của nhóm**, không do nguồn Stanford xác nhận.

## 3. Đầu ra để kiểm tra từng lượt

Ban trong `game_N.json` có:

| Trường | Ý nghĩa |
|---|---|
| `advice.contextual_score` | Điểm loss pool địch trừ chi phí tự cấm |
| `advice.pool_impact` | Theo role hai đội: số lựa chọn, top trước/sau, giá trị trước/sau và loss |
| `advice.own_next_pick_before_enemy` | Đội mình lấy lượt pick tới trước đối thủ hay không |
| `advice.fearless_locked_count` | Số tướng bị khóa từ các ván trước |
| `advice.search_trace.state` | Trạng thái công khai trước root, history chỉ chứa action đã lộ, không chứa kết quả tương lai |
| `advice.search_trace.candidate_summary` | Điểm6root hoặc ít hơn; so ban được chọn với ban bị loại |
| `advice.search_trace.root_evaluations` | Mỗi root có toàn bộ branch, leaf, weight, coverage và khoảng nhạy |
| `advice.branches` | Các nhánh của ban được chốt; mỗi bước có turn/side/action/champion/role và cách chọn |
| `ban_truncation_sensitivity` | Khoảng nhạy do cắt nhánh, tách rõ khỏi CI/probability |
| `advice.search_trace.elapsed_seconds` | Thời gian chấm lượt ban; có cache |

`why N` trên simulator in điểm, chi phí tự cấm và phản ứng được xét. Report Markdown vẫn hiển thị Ban1–5/Pick1–5 từng đội, lượt toàn cục1–20, role và nhãn thiếu tin cậy của pick. Hướng lựa chọn thể hiện bằng pool bị tác động/nhánh kế tiếp, chưa có tên chiến thuật cơ chế như “dive comp” do model mới học được.

## 4. Đã chạy đối chiếu ba chế độ

Đầu vào giữ nguyên: T1 Blue, Gen.G Red, Worlds cutoff13/11/2026, patch **dataset16.20**, roster trong snapshot và lịch chọn trước T1/Gen.G/T1/Gen.G/T1. Bật `--allow-statistical-auto` theo yêu cầu test; không gán kết quả ván hoặc ép tỉ số2-2.

Đã chạy3series×5draft: mỗi series100hành động,50picks khác nhau, khóa0/10/20/30/40. Cách cũ có1tập6ban đầu lặp qua5ván; contextual và lookahead có5tập khác nhau. **Đây là thay đổi hành vi, chưa chứng minh mạnh hơn về chiến thuật**. Các chế độ dẫn đến pool/pick sau đó khác nhau, nên không là thí nghiệm nhân quả có kiểm soát về thắng/thua.

Kết quả và số liệu lấy trực tiếp từ:

- [COMPARISON.md](../reports/ban_strategy_comparison/COMPARISON.md): bảng sáu ban đầu trước/sau, Jaccard/lặp, latency, độ bất định.
- [comparison.json](../reports/ban_strategy_comparison/comparison.json): metrics, replay checks, hash nguồn.
- [Lookahead QUICK_VIEW](../reports/ban_strategy_comparison/lookahead/QUICK_VIEW.md): đúng100lượt để tự đánh giá.
- [Lookahead REPORT](../reports/ban_strategy_comparison/lookahead/REPORT.md): thêm lý do/nhánh từng ban; `game_1.json`…`game_5.json` và log cùng thư mục.
- [Legacy QUICK_VIEW](../reports/ban_strategy_comparison/legacy/QUICK_VIEW.md), [Contextual QUICK_VIEW](../reports/ban_strategy_comparison/contextual/QUICK_VIEW.md): đối chiếu trước/sau và ablation không search.

Đã replay583đường nhánh thuộc295root trên trạng thái gốc, kiểm tra đúng lượt và loại tướng đã khóa; sâu tối đa9plies ở lần chạy này, dưới budget12. Search chọn khác top ngữ cảnh ở23/50lượt ban. Model chỉ phủ trung bình khoảng21.1% khối phản ứng có hỗ trợ bằng hai nhánh giữ lại; thấp nhất5.8%. **48/50lượt có khoảng nhạy chồng lấn ứng viên khác**, nên không được khẳng định root được chọn chắc chắn tốt hơn. Model phản ứng chưa calibrated và evaluator vẫn là proxy.

Regression:57testsPASS, gồm6test mới về first-pick/self-denial, Fearless/protected pool, branch legality/depth/budget/không mutation, pha2, deterministic tie-break và khối xác suất bị bỏ. Thêm kiểm tra trace serialize không circular và không tham chiếu history sống. Không retrain model; SQLite/raw/model cũ không đổi.

## 5. Chạy lại

```powershell
# Cách mới, giữ test chọn top1 khi thiếu tin cậy
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --ban-strategy lookahead --ban-response-model models/opponent_model.pkl --output-dir reports/ban_strategy_comparison/lookahead

# Đối chứng: đổi chiến lược và thư mục output
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --ban-strategy legacy --output-dir reports/ban_strategy_comparison/legacy
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --allow-statistical-auto --ban-strategy contextual --output-dir reports/ban_strategy_comparison/contextual

# Validate3series, replay nhánh và xuất báo cáo so sánh
.\.venv\Scripts\python.exe src/07_recommender/compare_ban_strategies.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`legacy` vẫn là mặc định để không ngầm thay đổi lệnh cũ. Chọn `contextual`/`lookahead` tường minh khi chạy mới. Nếu không truyền response-model thì lookahead dùng proxy softmax có nhãn. Nếu truyền model khác giải hoặc state trước thời điểm train thì từ chối, không dùng thông tin tương lai. Bỏ test override thì gate review của pick vẫn có thể dừng series.

## 6. Kiến thức và phạm vi còn thiếu

Nền môn học: Chương1 về trung bình/xác suất/kỳ vọng; Chương5x groupby/filter dữ liệu; Chương6 content/cosine làm một phần điểm chọn; Chương4 là nền mô hình dự đoán hành động đã có. **MR mới**: loss pool, self-denial, shortlist, rollout theo phản ứng, evaluator proxy và độ nhạy cắt nhánh. **NV**: CLI, trace, so sánh và đánh số report. Các công thức này phải được mô tả trong phần mở rộng, không gọi là toàn bộ nằm nguyên trong slide.

Chưa làm: search đầy đủ mọi lượt ban/pick, học chiến thuật phản thực từ kết quả thực, tự đánh giá cơ chế counter/engage/frontline/damage, tối ưu phân vai flex nhiều nhánh hoặc để dành tướng qua toàn BO5. Việc ban đã bớt lặp không xử lý hết vấn đề chọn/cặp tướng, ví dụ Lucian không luôn được ghép cùng partner phổ biến khi draft bị tác động. Giữ rõ nhãn thiếu mẫu thay vì chỉnh tướng bằng tay để làm đẹp kết quả.
