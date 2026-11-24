# Hai chế độ ban/pick và tiêu chuẩn dữ liệu Rank cao

**Cập nhật tiếp theo:** collector snapshot cá nhân đã hiện thực và chạy thật, xem [COLLECTOR_RANK_SNAPSHOTS.md](COLLECTOR_RANK_SNAPSHOTS.md). Các câu “collector chưa triển khai” bên dưới là mốc thiết kế trước bước này. Historical gate và runtime Rank/Giải không đổi; cohort snapshot mới không phải historical-high.

Chốt thiết kế theo yêu cầu người dùng24/11/2026. **Đã có cấu hình và công cụ kiểm tra dữ liệu; chưa có runtime/giao diện chế độ Rank.** Chế độ Giải hiện có legacy/contextual dùng lịch sử Pro; Rank chưa được đưa vào điểm.

## Hai chế độ sản phẩm

| Nội dung | Rank | Giải |
|---|---|---|
| Mục tiêu | Hỗ trợ lựa chọn của người chơi trong trận xếp hạng | Hỗ trợ draft đội tuyển theo giải/patch/đội hình/thể thức |
| Dữ liệu chính | Rank, tách queue/server/patch/bậc rank | Pro, tách giải/patch/cutoff; Rank **cao** chỉ là nguồn bổ sung |
| Cá nhân hóa | Role, bậc rank và sở thích/pool do người dùng cung cấp; không giả định biết định danh đối thủ | Roster/pool quan sát trước cutoff và tướng đã lộ |
| Thể thức | Thiết kế ban/pick Rank riêng, không dùng nguyên lịch20action của Tournament Draft | Lịch Tournament Draft hiện có; Fearless chỉ khi bật đúng thể thức sự kiện |
| Series | Không áp khóa Fearless BO5 của giải vào các trận rank độc lập | Quản lý khóa các ván trước khi thể thức yêu cầu; chưa tối ưu toàn bộ BO5 |
| Đầu ra dự kiến | Gợi ý có thứ hạng, lý do, số mẫu/CI, nhãn tier/patch và thiếu dữ liệu | Ban/Pick có số lượt, role/evidence, n/CI và review_required theo runtime hiện có |
| Trạng thái | Thiết kế + admission audit, chưa có recommender/CLI chơi Rank | legacy/contextual đã có, chưa bật Rank signal |

`rank/pro` là trục chế độ sản phẩm. `legacy/contextual` là chiến lược ban đang có trong luồng Giải; không đồng nghĩa với hai chế độ mới. Chưa nhận rằng đổi một cờ ở simulator giải là đã hỗ trợ Rank.

Riot mô tả hệ thống10ban đồng thời trong matchmaking, khác draft giải: [nguồn Riot](https://www.leagueoflegends.com/en-us/news/dev/dev-making-matchmaking-better/). Khi hiện thực runtime Rank cần đối chiếu luật client/queue hiện hành, không suy lịch thao tác từ mảng participant của Match-v5. Prototype Rank ban đầu dự kiến Solo/Duo420; Flex phải là scope riêng, chưa triển khai.

## Ngưỡng Rank cao và cấu hình

Nguồn cấu hình có hiệu lực với audit: `src/config/draft_modes.json`.

- Ngưỡng làm việc hiện tại: **Master+**, gồm Master/Grandmaster/Challenger. Đây là định nghĩa vận hành do nhóm lựa chọn, chỉnh được trong config, chưa được tối ưu bằng thực nghiệm hoặc coi là ngưỡng duy nhất người dùng đã chốt.
- Cùng queue Solo/Duo, server và patch phù hợp. Không dùng rank Flex thay Solo/Duo, không gộp server/patch rồi gọi tất cả là cùng meta.
- Để gắn nhãn **cả trận Rank cao tại thời điểm trận** phục vụ Giải: yêu cầu đủ10người, mỗi người có bằng chứng lịch sử đạt ngưỡng. Không suy tier từ seed, tên tuyển thủ, đồng đội/đối thủ, winrate hoặc MMR tự ước lượng.
- Nếu chỉ đủ bằng chứng cho2người của một kèo thì chưa gọi cả trận là high elo. Admission riêng cho kèo là hướng khác cần thiết kế/đánh giá riêng, chưa hiện thực ở lượt này.
- Ngưỡng tier và ngưỡng n>=5 đối đầu là hai khái niệm khác nhau; đổi tier không tự thay n hoặc chứng minh counter.

## Phân biệt các loại bằng chứng

| Nhãn audit | Ý nghĩa | Được nhận làm dữ liệu Rank cao lịch sử cho Giải? |
|---|---|---|
| `challenger_seed_only` | Trận lấy từ lịch sử seed trong danh sách Thách Đấu lúc fetch | Chưa đủ |
| `all_ten_high_at_observation_only` | Đủ10snapshot đạt ngưỡng tại lúc quan sát, chưa có lịch sử lúc trận | Chưa đủ cho nhãn lịch sử; chỉ làm cohort proxy có công khai riêng |
| `documented_high_all_ten` | Cả10người có interval lịch sử đúng queue/server/bao phủ thời điểm trận, có source_ref và available trước cutoff | Đạt hợp đồng dữ liệu; công cụ chưa xác thực độc lập nguồn bên ngoài |
| `historical_rank_unknown` | Không biết/không đủ bằng chứng lịch sử | Không, nhưng **không gọi là rank thấp** |
| `known_below_floor_present` | Có bằng chứng lịch sử ít nhất1người dưới ngưỡng | Không theo policy cả trận Master+ |
| `rank_evidence_conflict` | Các interval lịch sử mâu thuẫn | Loại chờ rà soát |

Riot League-v4 cho thông tin rank quan sát khi gọi API; Match-v5 không cung cấp sẵn bằng chứng lịch sử tier của cả10người cho trận cũ. Nguồn API: [Riot reference](https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntriesByPUUID), [LoL docs](https://developer.riotgames.com/docs/lol). Không biến snapshot hiện tại thành lịch sử. Công cụ lượt này không gọi411request chỉ để lấy current rank rồi dùng nó gán ngược cho tháng10.

Với dữ liệu mới nên thu snapshot của từng participant, lưu observed_at/queue/platform/source và theo dõi cùng match event time. Snapshot gần trận vẫn là **proxy**, không tự tạo interval valid_from/valid_until bằng±24giờ hoặc tự nhận chính xác lịch sử. Có thể làm phép thử cohort snapshot rõ tên trong tương lai; chưa là admission lịch sử nghiêm ngặt trong config này.

## Hợp đồng bằng chứng và kiểm tra

`rank_eligibility.py` nhận tùy chọn `--evidence` là file JSON private có list record:

```json
[
  {
    "puuid": "PRIVATE_PARTICIPANT_ID",
    "platform": "KR",
    "queue": "RANKED_SOLO_5x5",
    "tier": "MASTER",
    "kind": "historical_interval",
    "observed_at": "2026-10-14T00:00:00Z",
    "valid_from": "2026-10-13T00:00:00Z",
    "valid_until": "2026-10-15T00:00:00Z",
    "source_ref": "archive-reference-with-real-supporting-evidence"
  }
]
```

Đây là **ví dụ schema**, không phải chứng cứ thật. Chỉ ghi interval nếu nguồn thật hỗ trợ, không suy từ một snapshot. Với `kind=snapshot`, không yêu cầu interval nhưng cũng không có quyền nhận như historical. Record phải đúng PUUID/platform/queue, tier hợp lệ, timezone rõ, có source_ref; observed_at không sau knowledge cutoff. Interval dùng `[valid_from,valid_until)`, phải bao phủ lúc bắt đầu trận; mâu thuẫn thì không tự chọn record thuận lợi. Source_ref chỉ là truy vết, không phải chữ ký/xác thực độc lập. Dữ liệu định danh giữ private trong data/raw; report chỉ xuất counts/nhãn/lý do, không PUUID hay tên người chơi.

Kiểm cấu trúc trận: queue420/map11, đủ10PUUID/participant ID duy nhất, mỗi phe5người đủ5role và trận dài ít nhất10phút. “Có thể tiếp nhận dữ liệu cho Rank” chỉ là cổng dữ liệu cơ bản; không đồng nghĩa đã có mô hình tốt hoặc đủ nhãn tier để cá nhân hóa.

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/rank_eligibility.py --knowledge-cutoff 2026-10-26T18:03:08.999999Z
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_rank*.py' -v
```

Outputs: `reports/rank_cohort_audit/{REPORT.md,summary.json,matches.json,checks.json,tests.log}`. Audit92trận hiện có: **92seed-only,0đủ bằng chứng lịch sử cả10người**. Đây là0đã xác nhận, không phải92trận rank thấp. Không sửa/xóa raw hay thay kết quả thăm dò cũ.

## Chặn so sánh Giải dùng nhầm cohort

`evaluate_rank_transfer.py` giờ mặc định chạy admission audit đúng cutoff của phép thử; nếu không có trận đủ bằng chứng thì dừng exit2 trước replay, không ghi đè metric cũ. Có nguồn lịch sử thật thì truyền `--rank-evidence PATH`; chỉ các match ID đạt hợp đồng được tiếp tục lọc patch/server/end time như trước.

Để tái lập **nghiên cứu seed-only cũ**, phải chỉ rõ:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/evaluate_rank_transfer.py --allow-seed-only-research --output reports/rank_transfer_seed_only_reproduction
```

Output tái lập ở folder trên **chưa tồn tại** khi chưa chạy lệnh. Flag này chỉ công khai cách lấy mẫu để tái lập, không nâng cohort thành high elo verified và không bật hybrid. Kết quả mốc18/83trận vẫn chỉ nghiên cứu seed-selected; Recall@5 không tăng trong mẫu đó không là kết luận về mọi dữ liệu Rank cao.

## Những phần còn kế hoạch

Runtime/CLI/giao diện Rank; collector snapshot từng participant; đánh giá riêng theo tier cho Rank; dữ liệu lịch sử được xác minh độc lập hoặc nghiên cứu snapshot-proxy có protocol; final test giải mới và tích hợp Rank cao nếu có bằng chứng cải thiện. Chưa có output runtime Rank hoặc model Rank mới, không nhận chúng là đã xong.

Kiến thức: nền Chương2 làm sạch/nguồn/missing, Chương5x phân tầng/lọc/ghép; đây chủ yếu là NV-13 và policy MR-17 tự thiết kế về provenance/temporal admission, không phải mô hình CF/CB mới hoặc ngưỡng được dạy trong môn. Mapping tập trung ở mục19 của sổ kiến thức; không retrain vì thay đổi hợp đồng dữ liệu và thiết kế.
