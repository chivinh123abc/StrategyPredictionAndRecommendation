# Dữ liệu đối đầu Rank riêng với dữ liệu giải

**Cập nhật:** đã tiếp tục chuẩn hóa và thử nghiệm ba cấu hình ở [RANK_TRANSFER_PROTOCOL.md](RANK_TRANSFER_PROTOCOL.md), kết quả [Rank transfer](../reports/rank_transfer_evaluation/REPORT.md). Mục dưới giữ hướng dẫn/mốc smoke5trận; các giới hạn “chưa có benchmark” là trạng thái trước phép thử thăm dò. Chưa tích hợp vào contextual hoặc có final test mới độc lập.

Đã hiện thực bước thu thập và thống kê, chưa đưa Rank vào điểm `legacy/contextual`.
Module: `src/01_data_pipeline/ranked_matchups.py`. Không gọi constructor crawler cũ và không ghi vào SQLite canonical.

Lấy thử tối đa5trận KR bằng `RIOT_API_KEY` đã đặt trong `.env` hoặc biến môi trường, không chép khóa vào mã/lệnh:

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/ranked_matchups.py --collect --platform kr --limit 5 --frame-policy nearest
```

Tái tạo báo cáo offline từ cache đã có:

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/ranked_matchups.py --frame-policy nearest
```

Có thể dùng `--match-id KR_...` nhiều lần thay cho seed Thách Đấu; `--limit` giới hạn số trận mỗi lần, tối đa100. `--platform vn2 --routing sea` chọn routing rõ ràng nếu cần; kiểm tra routing theo tài liệu Riot, không thử dò nhiều host tự động. `--pro-league LCK`, `--patch 16.20`, `--as-of 2026-11-13` lọc báo cáo; cutoff theo ngày bao gồm cả ngày UTC. Patch dùng mã dữ liệu major.minor, không tự suy diễn mã marketing. Mặc định Pro là Worlds (`WLDs` trong DB, CLI không phân biệt hoa/thường), toàn bộ thời gian sẵn có; lọc từng patch khi thống kê.

## Thu thập và đo lường

- API dùng Match-v5 detail/timeline, chỉ Solo/Duo queue420, bản đồ11, trận dài ít nhất10phút. Seed lấy tối đa3người đầu danh sách Thách Đấu hiện tại; không phải lấy mẫu ngẫu nhiên. Một seed có thể cung cấp đủ5trận, vì vậy không gọi đây là tập đại diện high elo. Chưa thu rank từng người, rank tại thời điểm trận là **unknown**.
- Ghép đối thủ cùng `teamPosition` qua `teamId`, không dựa vị trí phần tử trong mảng. Chỉ nhận đủ10participant ID duy nhất, hai đội đủ5role không trùng và kết quả thắng thống nhất. Role Riot là phân loại sau trận, không xác nhận role dự định lúc draft/đổi đường. Thiếu hoặc mơ hồ thì loại, không tự điền.
- `extract_match` mặc định `before`: chọn frame gần mốc nhất, không sau mốc, sai lệch tối đa1000ms. `nearest` cho phép cả hai phía trong1000ms, **chỉ thống kê mô tả**. Hai policy và ngưỡng1000ms là thiết kế kỹ thuật của nhóm, chưa tối ưu bằng benchmark. Không lấy frame9phút thay10phút và không nội suy. Các cột `frame_ms_10/15` ghi timestamp thật; chế độnearest có thể dùng số liệu sau mốc nên không được nối vào Snowball dự báo đúng10phút. Không thấy frame/phép đo/trận kết thúc sớm thì để missing, không điền0.
- Vàng/XP lấy trực tiếp từ participant frame. CS Rank cộng `minionsKilled + jungleMinionsKilled`; Pro dùng `csat10/15` từ nguồn, cần xác minh hoàn toàn tương thích trước khi làm feature chung. Giữ chênh lệch âm và hai hướng đối xứng.
- Pro đi qua `load_clean_tables`; mỗi trận đủ10dòng/5role mỗi phe. Chỉ trừ `goldat10/15`, `xpat10/15`, `csat10/15` giữa hai người khi dữ liệu complete và đủ phép đo. Không lấy tổng cuối trận chia cho từng đường.
- HTTP timeout25giây, tối đa3attempt;401/403 dừng.429 tuân thủ Retry-After; nếu trên30giây thì dừng thay vì gọi lại sớm. Không in headers/token; không đi theo redirect mang token. Cache có sẵn không tải lại match/timeline.

## File đầu ra và trạng thái thật

Cache local trong `data/raw/riot_matchups/` (đã nằm trong gitignore): `{matchId}.match.json`, `{matchId}.timeline.json`, provenance cho từng response và `collection_manifest.json`. Raw chứa định danh Riot nên không được xem là dữ liệu phân tích đã ẩn danh. Manifest lưu ngày fetch/route/seed method; provenance thời gian fetch không phải thời gian trận.

Trong `reports/rank_pro_matchups/`:

| File | Nội dung |
|---|---|
| `rank_observations.csv` | Mỗi trận10dòng có hướng, ngày trận/gameVersion/role/tướng/đối thủ/kết quả/timestamp và chênh lệch; không có PUUID hoặc tên người chơi. |
| `pro_observations.csv` | Dữ liệu giải tương ứng, không có định danh người chơi. |
| `rank_matchups.csv`, `pro_matchups.csv` | Nhóm theo miền riêng, platform/queue/patch/role/tướng/đối thủ; games/wins/winrate/Wilson CI95 và n/mean/SD từng phép đo. SD không là CI cho mean; n1 thì SD missing. |
| `rank_pro_same_patch.csv` | Chỉ ghép cùng mã patch/role/tướng/đối thủ; giữ platform riêng, không cộng số mẫu hai miền. Chưa chuẩn hóa mọi alias tướng, nên có thể bỏ sót ghép; không suy đoán tên. |
| `summary.json`, `REPORT.md` | Scope/ngày/patch/coverage/policy/cache SHA256/giới hạn và diễn giải. |
| `checks.json` | Minh chứng chạy thực tế kiểm tra số dòng, signed mirror, timestamp, missing, DB không đổi và kết quả test. |

Đã tải thật5trận KR, ngày22/11/2026 UTC, patch16.23,50dòng role. Với `nearest`, tất cả50dòng đủ6phép đo10/15; frame thường sau mốc vài trămms, offset cụ thể trong summary. Worlds local có206trận/2060dòng từ2025–2026 trên4patch15.17/15.20/16.17/16.20;1940dòng đủ phép đo mỗi chỉ số. **Không có patch trùng giữa Rank smoke và Worlds**, CSV ghép chỉ có header. Đây không phải bằng chứng Rank vô ích hoặc chuyển miền thành công.

## Ý nghĩa và giới hạn

Winrate là kết quả thắng cả đội khi gặp cặp đó, không phải tỷ lệ thắng đường hay xác suất thắng do counter. Không kiểm soát trình độ/người chơi, phe, rừng/support, đội hình và drift. Hai hướng cùng trận có liên hệ; không coi50dòng là50trận độc lập. Wilson là khoảng tham khảo theo giả định trận độc lập; việc người chơi xuất hiện nhiều lần làm giả định này yếu.5trận chỉ kiểm tra kỹ thuật, quá nhỏ để xếp hạng matchup.

Chưa có benchmark Pro-only/Rank-only/hybrid, trọng số chuyển miền hoặc điều chỉnh contextual. Các đầu ra benchmark/hybrid đó **chưa tồn tại**. Bước đánh giá sau cần dữ liệu đủ cùng patch hoặc công khai khác patch, chia theo trận/thời gian, tránh người chơi/trận trùng giữa tập, giữ test giải độc lập và so baseline. Rank không cung cấp lịch20lượt draft giải; không suy thứ tự pick từ participant array. Không thay mô hình CB Chương6 bằng bảng đối đầu này.

Nền môn học: Chương2 các mục thu thập/làm sạch/missing (MH-04 trong sổ), Chương1 thống kê mô tả (37–44), Chương5x group/filter/join. Wilson dùng lại MR đã có; API/timestamp/role và kiểm soát miền là NV/MR tự thiết kế, không nhận là thuật toán Chương6 hay kỹ thuật chuyển miền đã kiểm chứng. Mapping tập trung ở mục17/MR-15/NV-11 của sổ kiến thức.

Nguồn chính: [Riot LoL routing/data](https://developer.riotgames.com/docs/lol), [Match-v5 reference](https://developer.riotgames.com/apis#match-v5/GET_getMatch), [HTTP/rate limits](https://developer.riotgames.com/docs/portal).
