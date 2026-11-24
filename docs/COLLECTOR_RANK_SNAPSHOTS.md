# Collector snapshot rank đủ10người — 24/11/2026

**Tiếp nối:** đã thu3đợt mới và xuất coverage/readiness, xem [RANK_BATCHES_COVERAGE_AND_EVALUATION.md](RANK_BATCHES_COVERAGE_AND_EVALUATION.md). Mốc5trận/2accepted bên dưới được giữ nguyên như run ban đầu; tổng hiện tại10accepted. Collector có thêm seed-offset/exclusion và cap HTTPattempt kể cảretry, không thay tiêu chuẩn cohort.

Đã hiện thực `src/01_data_pipeline/collect_rank_snapshots.py` để tạo cohort **Master+ tại lúc kiểm tra**, có timestamp và độ trễ so với trận. Đây là bước thu thập, không phải runtime ban/pick Rank hoặc tích hợp tín hiệu vào Giải. Quy tắc historical-all-ten trong `rank_eligibility.py` vẫn giữ nguyên; snapshot không được biến thành historical_interval.

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/collect_rank_snapshots.py --platform kr --limit 5 --seed-players 5 --matches-per-seed 1
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_rank*.py' -v
```

Khóa lấy từ `RIOT_API_KEY` đã cấu hình, không cần đưa vào command/code. `--match-id KR_...` (lặp lại được) thay bước seed. CLI giới hạn tối đa20trận/20seed; chọn queue Solo/Duo420. Routing theo serverconfig hoặc `--routing`; không tự dò host khác khi lỗi.

## Cách thu thập

1. Đọc seed Thách Đấu hiện tại, lấy match ID gần nhất mỗi seed; dedup ID. Không suy cả10người high elo từ seed.
2. Lấy Match-v5 detail để biết chính xác PUUID của10người, team/role/server/queue/ngày trận. Raw chứa định danh được giữ private.
3. Gọi **League-v4 entries/by-puuid** cho từng participant. Chỉ dùng entry `RANKED_SOLO_5x5`, lưu tier/division/LP, server, queue, observed_at sau response, nguồn và rawresponse. Snapshot dùng lại cho cùng người/server **chỉ trong cùng run**, không dùng snapshot cũ của lần trước để giả fresh.
4. Lấy timeline, phân loại và xuất report/dataset. Mỗi run có ID UTC riêng; không ghi đè snapshot của run trước. Mặc định nghỉ tối thiểu1.3giây giữa request, timeout25giây, retry tối đa3attempt qua client sẵn có; Retry-After được tôn trọng.

League-v4 là trạng thái lúc gọi API, không phải tier lịch sử của trận. Request không được snapshot đồng thời: observed_at từng người và độ trải được giữ rõ. Nguồn: [Riot API](https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntriesByPUUID), [HTTP/rate limits](https://developer.riotgames.com/docs/portal).

## Điều kiện nhận/loại/thiếu

Config `src/config/draft_modes.json:snapshot_collection`, tier floor đọc từ `pro.rank_tier_floor` (hiện Master+). CLI có thể override `--max-match-age-hours` và `--max-snapshot-spread-minutes`.

- **Nhận (`accepted`)**: trận Solo/Duo/map11, đủ10identity/5role mỗi phe hợp lệ, dài>=10phút;10entry Solo/Duo xác nhận tier>=floor, đúngserver/identity và timestamp hợp lệ. Tất cả snapshot sau kết thúc trận; snapshot cuối cách lúc kết thúc tối đa24giờ, thời gian giữa snapshot đầu/cuối của10người tối đa15phút.
- **Loại (`rejected`)**: đã biết có người dưới floor, trận sai cấu trúc, snapshot quá xa trận hoặc độ trải quá lớn. Có thể có nhiều lý do; một trận dưới floor vẫn có thể đồng thời thiếu người khác.
- **Thiếu (`missing`)**: chưa có10snapshot xác nhận và chưa có lý do loại đã biết. API trả danh sách không có Solo/Duo entry không được suy thành Diamond/Iron/rank thấp. Flex không thay Solo/Duo; nhiều entry Solo trùng/unknown tier/mismatch identity là dữ liệu thiếu cần rà soát.

24giờ/15phút là ngưỡng kỹ thuật làm việc do nhóm chọn, chỉnh được, chưa tối ưu; không làm snapshot thành rank lúc trận. Không nới ngưỡng sau khi xem kết quả để ép nhiều trận đạt. Báo cáo riêng `all_ten_high_at_observation_games` cho biết cả nhóm đạt tier ngay cả khi trận quá cũ để nhận làm proxy gần trận.

Lỗi401/403, rate limit không thể chờ trong budget, hoặc lỗi mạng/server sau retry: dừng request tiếp theo, lưu tiến độ và báo `collection_status=api_stopped`, CLIexit2.404 của participant đánh dấu thiếu rồi kiểm người tiếp theo. Raw response chỉ lưu khi nhận JSON thành công; lỗi chỉ ghi mã/trạng thái, không lưu token/header/request URL chứa PUUID vào report. Báo cáo một collection dừng ở discovery có thể0candidate; không bịa số trận đã kiểm.

## Đầu ra

| Vị trí | Nội dung |
|---|---|
| `data/raw/riot_rank_snapshots/{run_id}/` | Match/timeline/provenance; `snapshots/{sha256_puuid}.json` raw tier responses; `rank_snapshots.json` normalized records có PUUID; manifest. Toàn bộ private/gitignored. Hash filename không phải tuyên bố đã ẩn danh raw. |
| `reports/rank_snapshot_collection/{run_id}/summary.json` | Settings thực tế, server/queue/timestamps, count nhận/loại/thiếu, unique people, API requests/issues và reason counts. |
| `matches.json`, `REPORT.md` | Mỗi trận và10participant chỉ có ID vị trí trong trận/role/tier/observed_at/status; không PUUID, tên tài khoản hoặc LP công khai. |
| `accepted_match_ids.json` | Match ID qua điều kiện cohort snapshot. |
| `accepted_observations.csv` | Mỗi trận đủ cohort **và timeline extraction** có10dòng role/signedgold-XP-CS10/15 + tier_at_observation/rank_observed_at/cohort/historical_rank_verifiedFalse. Giữ gameVersion/patch/server/queue, không pooling miền. |
| `checks.json`, `tests.log` | Minh chứng kiểm thử và đối chiếu dữ liệu thật của run. |
| `reports/rank_snapshot_collection/latest.json` | Trỏ tới run mới nhất, không phải dữ liệu evidence thay thế. |

Match đủ cohort nhưng timeline thiếu vẫn nằm trong accepted IDs; observation dataset có thể ít trận hơn. Báo cáo có lý do timeline riêng và số dòng xuất; không giả đủ phép đo. Frame `nearest` tối đa±1000ms chỉ mô tả, không đưa các chỉ số sau draft vào gợi ý draft hoặc model đúng phút10. Tên raw championName trong export; chuẩn hóa catalog đúng patch trước các bước dùng chung với Pro, không tự áp catalog16.20 cho tướng mới của16.23.

## Lần chạy thật

Run `20261124T055630861038Z`, UTC05:56:30–05:58:10 (12:56–12:58 giờ Việt Nam),5seed KR,65request cấp client (không gồm retry nếu có),49participant khác nhau;50lượt participant ở5trận có1người lặp và dùng cache trong run.

- 5trận đều đủ10entry Master+ tại lúc kiểm tra, không missing/below floor.
- 2trận nhận: `KR_8471023945`, `KR_8471089359`; xuất20dòng observations.
- 3trận loại vì quá24giờ: `KR_8469965352`, `KR_8466534427`, `KR_8455107965`; không phải bị loại vì rank thấp.
- Không issues API, không thiếu timeline.40testsPASS (11mới), kiểm lại snapshot raw/normalized/timestamp/status/public privacy và DB không đổi.

[Báo cáo run](../reports/rank_snapshot_collection/20261124T055630861038Z/REPORT.md), [summary](../reports/rank_snapshot_collection/20261124T055630861038Z/summary.json), [dataset](../reports/rank_snapshot_collection/20261124T055630861038Z/accepted_observations.csv).

Nhóm này **chưa phải historical-high đã xác nhận** và không thay thế benchmark Pro-only/Rank-only/hybrid trước đó. Chưa có đánh giá recommender mới, chưa bật Rank signal cho Giải hoặc triển khai runtime Rank. Kiến thức dùng lại Chương2/5x cho dữ liệu/missing/lọc/ghép; NV-14/MR-18 là cohort snapshot, giới hạn recency/spread và điều khiển collector tự thiết kế, ghi ở mục20 của sổ kiến thức.
