## Hiện hành24/11: chỉ legacy và contextual

Lookahead và ban-response-model đã gỡ khỏi runtime/CLI. Dùng `--ban-strategy legacy` hoặc `--ban-strategy contextual`; mặc địnhlegacy, testchọnsố1thiếutincậyvẫnqua `--allow-statistical-auto`. [Phương pháp và lệnhhai mode](BAN_LEGACY_VA_CONTEXTUAL.md), [so sánhhiệnhành](../reports/legacy_contextual_comparison/COMPARISON.md). Những mụcsearch/lookaheadbên dưới là lịch sử, không là lệnh còn chạy được.57testsPASS,hai mode rerunđủ5draft/50picks khônglặp.

## Mới24/11 — Ban theo ngữ cảnh và xét nhánh

`--ban-strategy contextual` xét loss pool2đội/roster/firstpick/Fearless. `--ban-strategy lookahead --ban-response-model models/opponent_model.pkl` thêm6root/2firstopponentresponses vàgreedyrollout đến3pick/max12plies; đây khôngphảifullBO5planner. Dùngđượctrongcảsimulator1vánvàdriver5ván, `legacy`vẫnmặcđịnh. Cho test đủ5ván thêm`--allow-statistical-auto` theoủyquyềnngườidùng, giữnguyênnhãnthiếutin cậy.

[Côngthức/giới hạn/lệnhchạy](BAN_NGU_CANH_VA_LOOKAHEAD.md), [so sánh trước/sau](../reports/ban_strategy_comparison/COMPARISON.md), [Ban/Pick100lượt](../reports/ban_strategy_comparison/lookahead/QUICK_VIEW.md). `why N`xemchi phítựbanvànhánhđáp trả;JSONgiữmọiroot/branch,selected/omittedmass vàsensitivitybounds. 57testsPASS,15draft/150picks (50khácnhau trongmỗiseries), khôngcóbằngchứngtăngthắng.

## Hiện hành24/11/2026 — gate kiểm tra lựa chọn thiếu căn cứ

Auto mặc định có thể dừng trướclượt20 nếu địch đủ5và ứng viên không có đối đầu đủ mẫu; lưu manual_review vàcompletefalse, CLIonegame exit3. Chọn tay phe người dùng vẫn được phép. `--allow-statistical-auto` chỉ dành demoonegame chốt thuầnđiểm, không xác nhậncounter. Driver5ván dừng khi cầnreview; ví dụ5ván cũ bên dưới thuộc phiên trướcgate. [Lý do, caseTrundle, alternative và51tests](RA_SOAT_LUA_CHON_THEO_DOI_HINH.md). Phần forecast đã có bảnđầu trước khi thu hẹp phạm vi, hiện không tiếp tục phát triển.

## Chạy5vánFearless — hiện hành23/11/2026

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py
```

Gen.G–Bilibili Gaming, dữ liệu Worlds trước14/11, 5draft liên tiếp, không mô phỏng kết quả game. Tướng đã PICK khóa cho cả hai đội đến hết series, bans thường chỉ trong ván. Candidate threshold1và evidence5 tách riêng; lớp>=5 ưu tiên trước, mẫu ít có nhãn. Association được shrink bổ sung theo độ phủ: effective_lift=exp(reliability*log(raw_lift)), reliability dương dùng weighted_pair/(weighted_pair+10), âm dùng weighted_anchor/(weighted_anchor+10); công thức priority dùng effective_lift. Báo cáo đủ100lượt: [REPORT.md](../reports/worlds_fearless_bo5/REPORT.md). 38testsPASS; 50picks khác nhau. Chưa tối ưu việc để dành tướng cho ván sau, không gán kết quả thắng/thua. Các benchmark/mẫu ở phần dưới là mốc trước nâng cấp confidence này; báo cáo Worlds mới có Recall5=.36,MRR5=.184.

# Giả lập cấm/chọn tương tác: lịch sử + content-based

## Chạy nhanh

Tại thư mục gốc `Project`, mở terminal PowerShell:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py
```

Chọn kịch bản trong menu, sau đó chọn khu vực (`ALL`, `LCK`, `LPL`, `LCP`, `MSI`, `WLDS`…). Bạn điều khiển một phe; phe còn lại tự chọn theo cùng thuật toán. Lineup ưu tiên 5 tuyển thủ trong trận gần nhất của đội ở snapshot; không đồng nghĩa roster hiện tại. Đội chưa quan sát có preset demo với nhãn riêng.

Chạy thẳng T1 vs GEN.G, bạn điều khiển Blue:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py --blue-team T1 --red-team GEN.G --user-side blue --region LCK
```

Bạn điều khiển đội vô danh ở Red:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py --blue-team T1 --red-team UNDERDOG --user-side red --region ALL
```

Các tùy chọn:

- `--first-pick red`: Red là bên draft trước, độc lập với phe bạn điều khiển. Mặc định Blue draft trước.
- `--wishlist "Zeri,Lulu"`: ưu tiên chủ đích của người chơi, có nhãn riêng; không gán điểm cao giả. Khi đủ hồ sơ, tướng mẫu còn được dùng để tìm lựa chọn tương đồng.
- `--auto`: AI điều khiển cả hai phe.
- `--as-of 2026-09-13 --patch 16.16`: tái lập snapshot lịch sử; patch theo mã trong dataset, không tự suy thành mã Riot khác.
- `--lookback-days 60 --half-life-days 21`: cửa sổ và tốc độ giảm trọng số theo tuổi trận.
- `--max-data-age-days 14`: từ chối chạy nếu snapshot quá cũ so với ngày yêu cầu; không có cờ này thì vẫn cho xem lịch sử và in tuổi dữ liệu.
- `--used-champions "Olaf,Ryze,Shen"`: loại các tướng đã sử dụng ở ván trước của series; người dùng cung cấp danh sách.
- `--save-session reports/draft_sessions/demo.json`: lưu trạng thái, 20 lượt, các lần đổi vị trí và căn cứ/điểm thành phần. Phiên dừng sớm được ghi `complete: false`.

## Điều khiển từng lượt

| Nhập | Tác dụng |
|---|---|
| Enter hoặc số `1`, `2`… | Chốt gợi ý tương ứng |
| `top`, `jng`, `mid`, `bot`, `sup` | Lọc gợi ý theo vị trí |
| `all` | Xem lại các vị trí còn trống |
| `why 1` | Xem mẫu đối đầu/phối hợp, cosine và từng điểm thành phần |
| `mid Ahri` | Chọn trực tiếp tướng cho vị trí còn trống |
| `Ahri` | Chọn trực tiếp; suy vị trí còn trống từ tần suất lịch sử, nếu đủ căn cứ |
| `swap Ahri top` | Chuyển/hoán đổi vị trí trong các tướng đội bạn đã chọn |
| `auto` | Giao phần còn lại cho AI |
| `quit` hoặc Ctrl+C/EOF | Dừng; không tự bịa lựa chọn của người chơi |

Mọi lượt kiểm tra đúng bên, không trùng tướng đã cấm/chọn, không ghi đè vị trí đã có tướng. Không đủ dữ liệu cho khu vực thì hệ thống dừng hoặc cho chọn thủ công; không ngầm gán tướng dự phòng cố định.

Vị trí địch được suy bằng phân phối tần suất lịch sử, chuẩn hóa trên các cách gán vị trí một-một. Không coi role đang gán trong giao diện là vị trí chắc chắn của flex pick. Vị trí đội mình vẫn là phân công tạm thời, có thể đổi bằng `swap`.

## “Tối ưu” theo tiêu chí nào?

Đây là **tối đa điểm xếp hạng tại lượt hiện tại**, không phải chứng minh đội hình tối ưu toàn cục hoặc thắng trận.

`DraftAdvisor` kết hợp các thành phần trên cùng tập ứng viên theo vị trí:

| Thành phần | Giá trị | Trọng số mặc định |
|---|---|---:|
| Meta | Presence pick/ban, mỗi tướng đếm một lần/trận; trọng số thời gian | 1 |
| Thứ tự chọn | Tần suất tại slot F1/S1…; shrink về pick share với prior 10 trận | 1 |
| Bằng chứng lịch sử | Cận dưới Wilson CI winrate cả trận trong cửa sổ | 0.25 |
| Đối đầu | 0.5 + residual so với WR nền, shrink `n/(n+10)`, trộn theo xác suất role địch | 0.5 |
| Phối hợp | 0.5 + trung bình residual WR cặp so với WR nền, shrink theo n | 0.25 |
| Bể tướng | Tỷ trọng lượt chọn của tuyển thủ tại role, trọng số thời gian | 0.5 |
| Content-based | Cosine gốc từ hồ sơ tuyển thủ hoặc tướng mẫu | 0.1 |

Các thành phần trong bảng tạo điểm nền b bằng trung bình có trọng số. Sau đó điều chỉnh bằng geometric role-pair lift L với mọi đồng đội đã chọn: `priority=b*L/(1-b+b*L)`. Composition có số mũ mặc định1, không phải một thành phần cộng tuyến tính. Lift lấy tần suất ghép cặp đúng game/side/cả hai role, shrink về pick share nền; cặp chưa thấy nhưng anchor đủ mẫu bị giảm ưu tiên, anchor chưa đủ mẫu không tham gia. Có counts/CI và trạng thái thiếu dữ liệu cho toàn bộ 10 cặp trong đội. Công thức, benchmark Worlds và giới hạn: [WORLDS_ROLE_PAIR_REVIEW.md](WORLDS_ROLE_PAIR_REVIEW.md).

Bỏ percentile để loại ứng viên không làm đổi thang điểm. Meta/lịch sử luôn có; bể tướng/content chỉ dùng khi có hồ sơ. Matchup n<5 dùng trung tính; synergy theo winrate cũng yêu cầu n≥5 và đã giữ cả role của hai tướng. Các hằng số/trọng số là policy công khai, chưa được học/tối ưu bằng validation. Không phải xác suất hay cam kết tối ưu toàn cục.

Điểm cấm = `0.6*presence + 0.25*ưu_tiên_đối_thủ + 0.15*min(1,chênh_top1_top2)`. Xét mọi ứng viên hợp lệ ở role đối thủ còn trống, thay vì chỉ top1 của mỗi role. Vị trí còn trống của đối thủ khi cấm vẫn dựa trên phân công tạm trong phiên; chưa tối ưu mọi cách flex ở cây tìm kiếm. Không biến chênh điểm thành tăng thắng.

Mọi thành phần lấy cùng snapshot: đúng khu vực, trước `as_of`, cửa sổ mặc định 60 ngày đến trận cuối patch đích, cùng major season; giảm trọng số `2^(-tuổi_trận/21)` cho presence, slot và pick share. Counts/Wilson, residual và hồ sơ content lấy dữ liệu trong cửa sổ nhưng không áp decay. Ứng viên cần ≥5 trận tại role trong cửa sổ và có pick/ban trên patch đích. Vì vậy tướng mới/ít mẫu có thể bị bỏ sót; không tự bịa sức mạnh từ patch notes.

Wishlist là chủ đích người chơi. Benchmark riêng historical/content-based giữ nguyên. Audit draft mới: 20 trận/200 lượt, Recall@5 28.5% so với recent presence 27%; CI chênh lệch [-1.5,4.5] điểm phần trăm, chưa chứng minh ưu thế. Xem [rà soát LCK](LCK_DRAFT_REVIEW.md).

Số liệu LCK trên là phiên bản trước role-pair association. Audit hiện hành trên Worlds: policy36%, recent presence30%, CI mô tả [+1,+12] điểm phần trăm; chưa là final test hoặc bằng chứng tăng thắng. Có thể chạy `evaluate_draft_policy.py --region WLDS`.

## Lượt và phạm vi mô phỏng

Mô phỏng **một ván**, hai pha, mỗi bên 5 cấm và 5 chọn. Gọi A là bên draft trước, B là bên sau:

- Cấm 1: A B A B A B.
- Chọn 1: A B B A A B.
- Cấm 2: B A B A.
- Chọn 2: B A A B.

Không gắn cứng “Blue luôn pick trước”. Riot công bố First Selection năm 2026 cho phép tách lựa chọn màu phe và thứ tự draft; tùy chọn `--first-pick` phục vụ trường hợp này. [Nguồn chính thức: Season Start 2026, mục First Selection](https://lolesports.com/en-GB/news/season-start-2026-lol-esports).

Có thể nhập tướng ván trước bằng `--used-champions`, nhưng chưa quản lý tự động toàn bộ series Fearless, timer hay lobby Riot. Phiên `--as-of` bỏ dự báo model lưu sẵn để tránh dùng model fit sau mốc lịch sử. Phiên không chỉ định mốc có thể hiện dự báo Draft model cũ; model chưa biết patch/slot, không dùng nó để chứng minh policy mới tốt hơn. Radar/thẻ chiến thuật là quy tắc chuyên gia.

Draft model hiện dùng đội hình/khu vực, chưa có biến thứ tự pick riêng của phiên; dự báo này không định lượng lợi ích của First Selection.

## Liên hệ môn học và kiểm chứng

Chương 6: content-based item/user profiles, cosine; hybrid rank aggregation là phần mở rộng ứng dụng. Chương 1: thống kê lịch sử và độ bất định; Chương 5/5x: dữ liệu và nhóm theo vị trí. State machine/draft policy là phần kỹ thuật phục vụ demo.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Kiểm chứng bao gồm: lượt A/B độc lập màu phe, 20 hành động, không trùng tướng/vị trí, swap, lọc đường/why, thao tác từ cả Blue/Red, cold-start, EOF không tự chọn, lưu/tải JSON và cách tính điểm. Biên bản smoke test CLI: `reports/draft_simulator_checks.json`.
