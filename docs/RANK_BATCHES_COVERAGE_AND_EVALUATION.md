# Thu theo đợt, báo cáo độ phủ và điều kiện phát triển Rank

**Tiếp nối:** đã có kho SQLite tăngdần/hàngđợi và thốngkê ngay, xem [CONTINUOUS_RANK_EVIDENCE.md](CONTINUOUS_RANK_EVIDENCE.md). Các số10accepted/49tests bên dưới là mốc4run cũ; datasetRank hiệnhành xem [bảng mới](../reports/rank_matchups_live/REPORT.md). Recommender/benchmark độc lập vẫn tách khỏi việc cậpnhật thốngkê.

Đã thực hiện bước thu thêm và báo cáo độ phủ theo yêu cầu24/11/2026. **Điều kiện “khi đủ mẫu” chưa đạt**, nên chưa dựng recommender Rank, chưa chạy metric/baseline và chưa làm giao diện. Runtime Giải/legacy/contextual không đổi.

## Thu nhiều đợt có giới hạn

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/collect_rank_batches.py --batches 3 --matches-per-batch 5 --seeds-per-batch 5 --seed-offset 5 --request-budget 200
.\.venv\Scripts\python.exe src/01_data_pipeline/rank_coverage.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_rank*.py' -v
```

Lệnh đầu cần API key đã cấu hình; hai lệnh sau offline. Giữ chuẩn cả10người Master+ tại lúc kiểm tra, snapshot sau end tối đa24giờ, độ trải tối đa15phút. Không nới ngưỡng để ép thêm accepted. `seed-offset` chọn các đoạn khác nhau trong danh sách Thách Đấu; registry private ngăn chọn lại cùng seed trong một campaign nếu danh sách thay đổi. Tối đa300entry; thứ tự danh sách và lựa chọn seed vẫn là convenience sampling, không phải mẫu đại diện.

Campaign chạy tuần tự với cùng RiotClient/rate limiter. `request-budget` đếm **HTTP attempt thật, gồm retry**, kiểm trước mỗi attempt; hết budget dừng và giữ partialreport, không bắt đầu batch sau lỗi terminal. Đã nhận/loại một match ID ở run cũ thì bỏ qua lúc discovery để không mua lại cùng trận; missing được phép kiểm lại ở run sau. Snapshot vẫn mới mỗi run, không lấy snapshot cũ thay currentrank. Cổng này không tự tạo lịch chạy nền hay thu vô hạn; lệnh mỗi lần là một campaign có ngân sách hữu hạn.

`collect_rank_snapshots.py` thêm seed-offset, exclusion, private seed_selection.json; `RiotClient` thêm max_requests/request_attempts và budget error. Các CLI cũ không đổi cơ chế chụp/rank gate. Nguồn kỹ thuật: [Riot API](https://developer.riotgames.com/apis), [HTTP/rate limits](https://developer.riotgames.com/docs/portal).

## Kết quả thật của campaign

Campaign `20261124T060507936864Z`,3batch mới cùng ngày,15seed khác nhau,179/200HTTPattempt:

| Run UTC | Ứng viên | Nhận | Loại quá24h | Thiếu | Người kiểm duy nhất trongrun |
|---|---:|---:|---:|---:|---:|
| 20261124T060507936998Z |5|3|2|0|45|
| 20261124T060626740398Z |5|2|3|0|46|
| 20261124T060747435457Z |5|3|2|0|40|

Không cộng45+46+40 thành số người độc lập toàn campaign vì có người lặp. File [campaign manifest](../reports/rank_snapshot_collection/campaigns/20261124T060507936864Z.json) giữ request usage và summary từng batch; raw seed IDs nằm private. Cả15candidate đều all10Master+ tại observation,7bị loại do tuổi trận, không do tier thấp.8accepted mới; gộp2accepted lần trước thành **10trận/100dòng participant/72người khác nhau**. Bốn run là4lần fetch trong cùng ngày, không giả thành4ngày hoặc4period độc lập.

## Báo cáo độ phủ

`rank_coverage.py` đọc tất cả run có schema snapshot, chỉ nhận đúngfloor/age/spread của policy hiện hành. Recompute classification từ private raw/snapshots, reject nếu status không khớp report. Một match accepted nhiều lần chỉ giữ lần đủ điều kiện sớm nhất; payload cùng ID mâu thuẫn thì lỗi, không tăng n. PUUID chỉ trong bộ nhớ để đếmdistinct, không xuất ra bảng công khai. Identity tướng dùng **championId**, không gộp tên kiểu fuzzy; nhãn raw championName từ Riot cần chuẩn catalog đúngpatch trước dùngchungPro/UI.

Accepted cung cấp n. Tướng/role thấy ở candidate rejected chỉ được thêm vào **universe tên/ID** để báo hàng0, không thêm trận/người/winrate hoặc phép đo. Universe này không phải mọi tướng/role chơi được trong game. Cặp cùng đường là có hướng A→B; B→A cùng trận có liên hệ, không phải hai trận độc lập.

Outputs tại `reports/rank_coverage/`:

| File | Nội dung |
|---|---|
| `games.csv` | Match ID duy nhất, server/queue/patch/floor, start/end/available_at và run được chọn. |
| `observations.csv` |100dòng accepted, role/IDtướng/IDđối thủ/result/tier/time và chỉ số thật nếu có; không PUUID. |
| `patch_coverage.csv` | Trận/người riêng từngserver/queue/patch/floor; có0n nếu chỉ thấy candidate names. |
| `role_coverage.csv` | Thêmrole, đếm trận vàngười trongrole, không chia tổng đội thành dữ liệu đường. |
| `champion_role_coverage.csv` | ntrận/người từng tướng-role, games_needed/players_needed/supported. |
| `lane_matchup_coverage.csv` | ntrận/người hai phía của từng cặp cùng đường; có hàng0, deficit từng phía và supported. |
| `summary.json`, `REPORT.md` | Runs/phạm vi/dedup/sourcehashes/giới hạn; bảngtheorole và blockers. |
| `readiness.json` | Cổng kỹ thuật, targetscope, kế hoạch history/validation/test và số history thật sự có trước validation. |
| `checks.json`, `tests.log` | Minh chứng unit/integration và tính bất biến DB/raw. |

Đã có115target champion-role và2.156cặp cùng đường có hướng trong universe candidate, **0champion-role và0cặp đạt ngưỡng**,46champion-role và2.058cặp chưa có evidenceaccepted. Accepted đều KR/420/16.23/Master+; patch16.22 chỉ có tên ở candidate cũ, naccepted0. Không trộn hai patch này.

| Role patch16.23 | Trận | Người khác nhau | n cao nhất của1tướng |
|---|---:|---:|---:|
| Top |10|17|2|
| Jungle |10|15|3|
| Mid |10|17|3|
| Bot |10|16|4|
| Support |10|15|4|

**Ngưỡng làm việc:** một champion-role có>=5trận,>=3người; kèo có>=5trận và>=3người mỗi phía. Readiness để triển khai prototype đầy đủ5role yêu cầu>=2tướng đạt ngưỡng mỗirole, history>=5/validation>=2/test>=2trận. Đây là policy kỹ thuật do nhóm thiết kế, **không phải phân tích statistical power, không chứng minh dữ liệu đủ tin cậy chiến thuật**. Không hạ ngưỡng sau khi xem kết quả.

## Tách thời gian và tránh rò rỉ từ snapshot

Targetscope là server/queue/patch/floor của accepted game mới nhất; report vẫn giữ các scope khác riêng, không lấy một patch cũ bị loại để chặn/đánh giá nhầm patch mục tiêu. Chia60/20/20 theo thời điểm bắt đầu khác nhau; các trận trùng thời điểm giữ cùng partition. Cả trận và các dòng player không được chia qua hai tập.

`available_at` là max timestamp đủ10snapshot và lúc fetch detail (đã biết kết quả); nếu không có provenance thì bảo thủ dùng runfinished_at. Khi freeze trước validation, **history phải đã kết thúc và có snapshot cohort/detail trước cutoff**. Chỉ có gameDate cũ không đủ: dùng tier chụp sau heldout để chọn trainingcohort gây thông tin nhìn về sau. Đây là lý do nhiều batch vài phút không tự thành đánh giá tương lai hợp lệ.

Mẫu hiện tại chia danh nghĩa6/2/2trận, nhưng **0trận history có đủ snapshot trước validationstart**, và0tướng đạt n5. `ready=false`, `evaluation_status=not_run`, `metrics=null`. Không tạo Recall/accuracy giả hoặc thay bằng chia random. Cần tích lũy các đợt ở thời điểm sau để history đã biết trước những trận query thật sự mới.

## Thiết kế bước recommender và evaluation còn điều kiện

Khi đủ mẫu, thiết kế Rank riêng nhận role, patch/server/queue, tướng đồng đội/địch **đã lộ**, bans và pool cá nhân. Gợi ý giữ cùng poolhợplệ, kèm n/người/CI/coverage; thiếu thì báo thiếu, không hardcode counter, không gọi heuristic là xác suất thắng. Chương6 content-based có thể tái sử dụng item/user profiles/cosine khi có feature Rank đã quan sát trước cutoff; chưa hiện thực phần đó ở lượt này.

Baselines dự kiến: popularity theo role trong frozen Rank history, và historical team-result với Wilson cùngpool. Metric dự kiến: Recall@k/MRR/candidatecoverage và chênh so baseline kèm bất định theo game, công khai cohortbias; không nhận retrieval là tăng thắng. Validation để chọn policy, test giữ riêng, fit/scaling/counts/profile từ history trước cutoff và không tune bằngtest. Có người lặp thì công khai mức trùng và phân tích thêm, không tự gọi là player-disjoint.

Match-v5 không cung cấp lịch draft Rank đầy đủ. Muốn replay ngữ cảnh thật cần log lựa chọn có timestamp/đãlộ được ghi riêng; không suy thứ tự từ participant array hoặc đem cả đội hình cuối trận vào giả làm thông tin sẵn có lúc pick. Nếu làm masked-lineup retrieval thì phải đặt tên bài toán riêng, không gọi replaythật.

**Chưa có** `rank_recommender.py`, modelRank, runtimeRank, reportmetric/baselineRank hoặc giao diện mới. Những output đó còn kế hoạch có điều kiện, không được nhận như đãxong. Không thay runtimeGiải hoặc cohort historical-highgate. Mapping phương pháp/nguồn/output/trạng thái ở sổ mục21/MR-19/NV-15; nền Chương1/2/4/5x/6 đã dùng trước, phần campaign/readiness/temporal availability là policy mở rộng tự thiết kế.
