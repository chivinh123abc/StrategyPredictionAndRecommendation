# Kho Rank tăng dần và bảng đối đầu cập nhật liên tục

**Phạm vi hiện hành24/11:** đã rút mốc2.000trận/kèo; mặc định không quota. Báo n/nguồn/CI thực có, U.GG reference chưa nạp nên không khẳng định tương đương. Xem [phạm vi đồ án vừa sức](PHAM_VI_DO_AN_VUA_SUC.md). Các con số mục tiêu/PID bên dưới là lịch sử trước điều chỉnh; tiến trình/log hiện hành theo collector_process.json.

**Bổ sung 24/11/2026:** đã thêm bảng `pooled_*.csv` gộp các patch/server thực có và tiến độ mục tiêu 2.000 trận/kèo; bảng tách patch vẫn được giữ. Xem [phạm vi, cách đọc và lệnh thu nhiều server](POOLED_MATCHUPS_UGG_STYLE.md). Số liệu 88 trận bên dưới là mốc trước bổ sung; số liệu mới nhất ở `reports/rank_matchups_live/summary.json`.

Theo yêu cầu24/11/2026: không đặt trần tổng1.000trận, không chờ đủ1.000mới cập nhật dữ liệu. Mỗi trận đủ điều kiện được ghi ngay vào SQLite; các bảng thống kê làm mới sau mỗi5job xử lý hoặc checkpoint khoảng60giây và lúc kết thúc phiên. Đây là kho bằng chứng/thống kê, chưa là recommender Rank hoặc đánh giá tăng thắng của ban/pick giải.

## Chạy và tiếp tục

```powershell
# Một phiên hữu hạn, giữ toàn bộ hàng đợi và kết quả cho lần sau
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --platforms kr --max-requests 600 --max-minutes 15

# Chạy tiếp nhiều phiên cho tới khi dừng hoặc API gặp lỗi terminal
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --platforms kr --watch --max-requests 600 --max-minutes 15 --pause-seconds 60

# Chỉ cập nhật CSV/report từ dữ liệu SQLite đã có, không gọi Riot
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --export-only

# Kiểm thử, không thu thập mạng thật
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_rank*.py' -v
```

`--watch` chạy ở tiến trình người dùng đang mở, không tự cài service/Task Scheduler hoặc chạy nền sau khi process đã dừng. Ctrl+C dừng có checkpoint; phiên sau dùng chính lệnh cũ tiếp tục, không thu lại từ0. Mỗi phiên có cap request **tính cả retry** và deadline; request đang thực hiện có thể hoàn tất sau mốc thời gian do timeout. Hết budget/thời gian là hết **phiên**, không phải đạt trần tổng dữ liệu. Không có cam kết sẽ đạt số trận tương đương U.GG trong một phiên/API key cá nhân.

Khóa chỉ ở `.env`/biến môi trường qua settings và header gửi Riot, không ở command/log/DB. Có thể chọn `--platforms kr,euw1,na1` hoặc server hỗ trợ khác; dữ liệu các server/patch luôn giữ scope riêng. Mỗi host được gọi qua client có nhịp tối thiểu1.3giây và Retry-After; không né rate limit hoặc tăng tải bằng nhiều key. Key lỗi401/403 hoặc mạng/server lỗi terminal thì dừng, cần xử lý nguyên nhân trước khi tiếp tục. [Riot API/rate limits](https://developer.riotgames.com/docs/portal).

## Tăng số trận hữu ích trên mỗi request

- Bootstrap danh sách **Challenger, Grandmaster, Master** bằng3League-v4endpoint mỗi server, refresh sau6giờ. Đây là seed để dò, không thay kiểm tier10người.
- Dò tối đa100match ID/page với queue420 và startTime trong24giờ, có pagination lưu cursor. Không chỉ lấy1trận của vài seed đầu. Seed được poll lại sau tối thiểu10phút; ưu tiên C/GM rồiMaster và chưapoll.
- Match ID là khóa duy nhất; đã có job thì không thêm bản sao. Hàng đợi và last_polled/page_start lưu SQLite qua các phiên. Người Master+ đã quan sát trong trận cũng thêm vào seed pool.
- Kiểm cấu trúc/tuổi trận trước khi tốn10requesttier. Mỗi participant vẫn phải có Solo/Duo entry đúngserver và đạt ngưỡng; không suy cả trận từ seed.
- Snapshot cache tối đa15phút, chỉ dùng khi timestamp snapshot sau lúc trận kết thúc. Giữ **observed_at gốc**, không sửa thành thời điểmcachehit. Nếu trận mới hơn snapshot hoặc cache quá hạn thì gọi lại API. Cả10snapshot vẫn phải đáp ứng spread15phút; không nới để ép nhận.
- Raw detail/timeline được cache; tier snapshot được lưu archive riêng có timestamp. Qualification lưu riêng trước khi tải timeline. Nếu bị ngắt sau khi đủrank nhưng trước timeline, lần sau lấy tiếp timeline bằng qualification đã ghi, không đánh mất cohort vì thời gian thực đã qua24giờ.

Đủ cả10người Master+ là **tại các thời điểm snapshot trong cửa sổ**, không xác nhận tier lịch sử lúc trận hoặc MMR. Master+/24h/15min là policy hiện hành; đổi policy phải dùng kho riêng, không âm thầm trộn điều kiện với kho cũ. Match-v5/League-v4: [Riot API](https://developer.riotgames.com/apis).

## Dữ liệu được cập nhật vào đâu?

**Kho mới thật:** `data/database/ranked_evidence.db`, schema `rank-lake-v1`, private/gitignored. Không sửa schema hoặc dữ liệu của `lol_live_data.db`, không nạp Rank vào model/score Giải. Seed/tier/PUUID chỉ trong kho private và raw.

| Bảng | Vai trò |
|---|---|
| `metadata` | Schema version, fingerprint policy, lịch bootstrap |
| `seeds` | Khóa(platform,puuid), tier/source/time, last_polled và page_start |
| `jobs` | Match ID duy nhất, routing/status/path/provenance/qualification/availability và retrytime |
| `snapshots` | Snapshot mới nhất mỗi(platform,puuid), giữ timestamp thật và source archive |
| `observations` |10dòng hoàn chỉnh/trận, khóa(match_id,team_id,role), role/champID/opponentID/privateperson IDs và JSON phép đo |
| `sessions` | Trạng thái, giờ bắtđầu/kếtthúc, request count và lýdo dừng mỗi phiên |

Raw mới ở `data/raw/rank_lake/`: detail/timeline theo match ID, snapshots/{hashPUUID}/{timestamp}.json. Các10trận đã nhận từ collector trước được import idempotent; không biến92trận lịch sử chưa tierverified hoặc các trận bị loại thành samples. SQL transaction ghi đủ10role, khóa chính chống đếm lặp. Một writer/filelock cho mỗiDB, lock tự giải phóng khi process đóng; WAL hỗ trợ đọc dữ liệu khi collector ghi. `.db`, WAL vàlock đều gitignored.

Nếu chỉ đủ tier nhưng timeline chưa xong, jobs cóaccepted trong khi observations chưa có; report phân biệt `counts.accepted` và `games_with_observations`. Thống kê chỉ lấy observations hoàn chỉnh. Raw tồn tại sau crash trước SQL checkpoint được đọc lại với availability bảo thủ, không bịa thời điểm sớm. Payload sai/404 được báo trong trạng thái, không biến thành n/tier/measurement0.

## Bảng thống kê theo hướng U.GG công khai

[Trang Lee Sin của U.GG](https://u.gg/lol/champions/leesin/counter) công khai tách winrate matchup và GD15. Đây là tham khảo cách trình bày/loại chỉ số; không tải lại số liệu họ thành dataset, không biết/tái tạo toàn bộ thuật toán nội bộ hoặc gọi output giống hệt U.GG. MụcU.GG mặc định/tênpatch có thể khác nguồnRiot, không tự đồng nhất các cohort.

Outputs cập nhật tại `reports/rank_matchups_live/`:

| File | Nội dung |
|---|---|
| `all_matchups.csv` | Mọi kèo quan sát được, gồm sparse, games/wins/rawwinrate/Wilson CI/số người; gold/XP/CS10/15 mean,median,SD,meanCI,nriêng |
| `best_full_game_matchups.csv` | Theo từng đối thủ/role/server/patch/floor: winrate thắng trận giảm dần, n>=5 mặc định |
| `unfavorable_full_game_matchups.csv` | Cùng scope, winrate thấp trước |
| `early_gold_advantages.csv` | GD15mean cao trước, cần nGD15>=5; tách thắng trận và lợi thế đầu trận |
| `observations.csv` | Rows bằng chứng khôngPUUID/tên người chơi, timestamp/patch/role/metric thật |
| `summary.json`, `REPORT.md` | Corpus counts/phạm vi/giới hạn; summary mới có generated_at và dataset fingerprint |
| `sessions/{session_id}.json` | Request usage và trạng thái từng phiên, không PUUID |
| `checks.json`, `tests.log` | Minh chứng nghiệm thu, được tạo sau phiên kiểm tra |

Sparse rows được ghi và xem ngay, không chờ1.000trận. Bảng xếp rỗng nghĩa kèo chưa n5, không có top giả. n5 chỉ là ngưỡng hiển thị làm việc, không phải chứng minh mạnh/đủpower; xem cùng số người vàCI, không nhận mẫu nhiều trận của cùng OTP là nhiều người độc lập. Score này chưa được đưa vào contextual.

Gold/XP/CS lấy frame thật gần10/15phút trong±1000ms, cóframe timestamp; chỉ là thống kê hậu draft. Missing không điền0 và n của từng metric có thể thấp hơn games. Không dùng chúng như feature sẵn có khi đang chọn tướng.

Wilson95 cho kết quả cả trận dùng lại phương pháp của dự án. CImean mới: `mean ± t(.975,n-1)*SD/sqrt(n)` khi n>1; n1 thiếuSD/CI. Nguồn [NIST confidence limits for the mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). Cần giả định độc lập/phân phối phù hợp; người lặp, outlier và nhỏn làm CI kém tin cậy. Không nói “95% xác suất kèo thật nằm trong khoảng” như xác suất hậu nghiệm. CI riêng từng kèo không giải quyết multiple comparisons khi xếp nhiều kèo.

`early_status` ghi observed_early_advantage/disadvantage khi CImeanGD15 cùng dấu, inconclusive khi chứa0, insufficient_samples khi n<ngưỡng. Đây là bằng chứng quan sát, không kiểm định nhân quả/counter bộ kỹ năng. Gold của rừng không phải duel đi lane; bot/support cần xét thêm đối tác và gank/roam/đội hình. Chưa điều chỉnh championbase strength/skill/side hoặc chiaRank/Prođểchứngminhtransfer.

## Phạm vi đã hoàn thành và còn kế hoạch

Đã hiện thực và nghiệmthu khoDB/hàngđợi/checkpoint/cache/tiếp tục/nguồnseedrộng và bảngthốngkê riêngstage10–15/fullgame. Phiên đầu `20261124T063723199769Z` dùng600request, phiên tiếp tục `20261124T065152611238Z` dùng2request và hoàn tất timeline còn dangdở với0snapshot mới. Tổng **88trận đủ observations (78mới +10import),880dòng,382người khác nhau**,714cặp có hướng,8cặp đạt n5. Kho có11.012seed,5jobpending và7rejected; seedkhôngphảimatchcount.63tests vàintegration DBintegrity/FK/rebuild78qualification/10roles/mirror/privacy/idempotentimport/canonicalDBhashPASS; xem [checks](../reports/rank_matchups_live/checks.json). Có thể chạy lại hoặc --watch để corpus tăng qua nhiều phiên mà không có ngưỡng tổng1.000. Hai phiên nghiệmthu đã kết thúc, không có service nền được cài hoặc để chạy ngầm.

Không thêm gợiý ban/pick giả định tốiưu, model mới, runtimeRank/UI hay tíchhợpPro. Cácbước đó cần đánhgiá riêng trên dữliệumới đã biết trướcquerytime; việc hiểnthị thốngkê hiện tại không đòi chờfinaltest nhưng không thay finaltest. Nềnmôn học Chương1/2/5/5x; CImean/tailcache/queue/sampling policy mởrộng được truyvết ởsổ mục22/MR-20/NV-16. KhôngretrainML.
