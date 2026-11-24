# Thống kê đối đầu theo hướng U.GG — 24/11/2026

**Phạm vi mới:** đã bỏ mặc định2.000trận/kèo theo yêu cầu người dùng. Độ phủ/số mẫu thực có được báo ngay; target/remaining/reached đểnull khi chưa có mục tiêu. Chưa nạp bộ tham chiếu U.GG theo cùng bộ lọc nên không nhận đã bằng số mẫu hoặc chất lượng của họ. Mốc150trận/PID23100 bên dưới là lịch sử; PID/log mới xem `collector_process.json`, số liệu mới xem summary.json. Phạm vi vừa sức môn học ở [tài liệu này](PHAM_VI_DO_AN_VUA_SUC.md).

Collector đã nạp lại cấu hình08:05:27UTC/15:05VN24/11, launcher29828/worker7992. Manifest có `worker_pids`, `stdout`, `stderr`, `stop_command`; cần dùng cả launcher/worker khi dừng, không chỉ PID cũ. Log hiện hành `collector_watch_no_quota.log` và `collector_watch_no_quota_errors.log`. Nghiệm thu trước lần khởi chạy này:418trận/1.626người/2.806kèo gộp;70ranktests +integration và139fulltestsPASS. Các số150/69tests ở mốc cũ phía dưới giữ làm lịch sử; checks.json hiện đã cập nhật mốc418, summary tiếp tục tăng.

**Mốc nghiệm thu:**150trận/725người,1.170kèo gộp (1.248kèo tách scope),0đạt2.000;69tests vàintegrationPASS,389membership đốichiếu raw. [checks](../reports/rank_matchups_live/checks.json) là mốc trướcwatch; [summary](../reports/rank_matchups_live/summary.json) là bản cậpnhật mới nhất. Watch nền đãkhởichạy14:17VN24/11, PID23100 trong [collector_process](../reports/rank_matchups_live/collector_process.json), log cùngfolder. Kiểmtra process/log để biết cònchạy hay không. Dữliệuthật đợtnày ởpatch16.23; chếđộgộpđa patch đãtest, cần tíchlũyqua cácphiênbản tiếp theo.

Yêu cầu hiện hành: bảng đối đầu có winrate/GD15/số mẫu và nguồn rõ ràng như hướng trình bày U.GG; xem gộp nhiều patch/server thực có. Không có quota mẫu cố định. Mục tiêu2.000 ở mốc trước đã được rút lại.

## Phần học theo nguồn công khai

[U.GG Lee Sin](https://u.gg/lol/champions/leesin/counter) phân biệt kết quả cả trận và lợi thế vàng phút 15, có số trận từng kèo. Nội dung được công cụ tìm kiếm lập chỉ mục ngày 24/11/2026 hiển thị World Emerald+ và patch 26.23; có cả kèo dưới 2.000 mẫu. Không xác nhận được thuật toán nội bộ, chính sách chọn mẫu hoặc hạ tầng thu dữ liệu của họ. Dự án tự tính từ Riot API, không nhập số liệu của U.GG làm mẫu.

Giả thuyết một kèo luôn giữ counter qua nhiều patch chưa được chứng minh. [Riot patch 25.10](https://www.leagueoflegends.com/en-us/news/game-updates/patch-25-10-notes/) có thay đổi tướng, trang bị và vai trò; đây là căn cứ cần giữ phiên bản để kiểm tra thay vì xóa thông tin. Gộp patch là lựa chọn phân tích được người dùng yêu cầu, không khẳng định tính bất biến của kèo.

## Các đầu ra thật

Trong `reports/rank_matchups_live/`:

| File | Cách đọc |
|---|---|
| `pooled_all_matchups.csv` | Gộp mọi patch/server thực có; giữ queue, tier floor, role và hướng tướng→đối thủ riêng |
| `pooled_best_full_game_matchups.csv` | Winrate thắng cả trận cao trước, theo từng đối thủ/role |
| `pooled_unfavorable_full_game_matchups.csv` | Winrate thấp trước |
| `pooled_early_gold_advantages.csv` | Chênh vàng phút 15 cao trước, có n đo được riêng |
| `matchup_collection_progress.csv` | Số mẫu/độ phủ thực; các trường mục tiêu đểnull, reference_status=not_loaded khi chưa có số liệu U.GG |
| `all_matchups.csv` và ba bảng không có tiền tố pooled | Vẫn tách server/patch để đối chiếu |

`ALL_OBSERVED` chỉ là các nguồn đã thu được, không có nghĩa đã bao phủ toàn thế giới. Cùng match ID/team/role chỉ đếm một lần. Hai hướng A→B và B→A là hai dòng mô tả cùng các trận, không cộng thành hai lần số trận độc lập. Kèo chưa xuất hiện không nằm trong bảng tiến độ; không nhận mục tiêu toàn bộ mọi cặp tướng đã hoàn thành khi chỉ các kèo xuất hiện đạt ngưỡng.

Các trường `patches/platforms/patch_count/platform_count` công khai phạm vi. `patch_gd15_details` lưu n và trung bình GD15 của từng patch có n>=ngưỡng hiển thị. `gd15_patch_direction` là `mixed_directions` nếu có cả trung bình dương và âm; cần ít nhất hai patch đủ mẫu mới mô tả cùng chiều. Cùng chiều không xác nhận ổn định hoặc ý nghĩa thống kê. Khác server giữa các patch cũng có thể góp phần làm khác dấu.

Ngưỡng hiển thị mặc định n5 vẫn chỉ để lọc bảng xếp, không phải chứng nhận chất lượng. Wilson cho winrate và Student-t CI cho mean giữ như mục MR-20; không thêm trọng số patch, làm mịn, kiểm định counter hay xác suất dự báo mới. Không đặt một con số mẫu làm điều kiện nghiệm thu. Vẫn giữ số người và CI; người chơi lặp có thể làm giả định độc lập yếu đi. Tùy chọn target cũ chỉ còn để tái lập cấu hình lịch sử, không tự nhận là số liệu U.GG.

## Thu và cập nhật

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --platforms kr,euw1,na1 --watch
```

Mỗi phiên mặc định 600 HTTP attempts/15 phút, tiếp tục sau 60 giây khi có `--watch`; Ctrl+C để dừng. SQLite giữ hàng đợi, seed, checkpoint và mẫu qua các phiên. Chạy lại không nhân mẫu cũ. Đạt mục tiêu không dừng thu. Theo [Riot portal](https://developer.riotgames.com/docs/portal), key/quota có giới hạn; updater giữ rate limit và dừng/checkpoint khi lỗi terminal. Không hứa đạt 2.000 mẫu mọi kèo trong một phiên.

Nếu collector được khởi chạy nền trong đợt này, `reports/rank_matchups_live/collector_process.json` ghi PID/thời điểm/lệnh/log; `collector_watch.log` và `collector_watch_errors.log` ghi tiến trình/lỗi. Đây là một process Python, không cài service hoặc tự khởi động cùng Windows. Không khởi chạy thêm writer nếu process đó còn sống; file lock sẽ từ chối. Với phiên nền không có cửa sổ để Ctrl+C: kiểm tra PID trong file, dùng `Get-Process -Id <PID>` rồi `Stop-Process -Id <PID>` nếu muốn dừng. Dừng cưỡng bức có thể để phiên đang dở ở trạng thái running; các raw/checkpoint/transaction đã hoàn tất được giữ, lần sau tiếp tục. Phiên nghiệm thu hữu hạn đã đóng mới được ghi là hoàn tất; không gọi session nền đang chạy là đã hoàn tất.

Giữ tiêu chuẩn đủ 10 người Master+ tại lúc kiểm tra, tuổi trận tối đa24h/spread15phút; mở nhiều server không hạ tiêu chuẩn sang Emerald+ để khớp U.GG. Vì vậy quy mô và quần thể khác U.GG. Bật một server không đồng nghĩa đã có trận đạt chuẩn từ server đó; xem nguồn thực trong CSV.

Để tăng số trận trên cùng ngân sách API, bootstrap lưu nguyên response các endpoint League-v4 Master/Grandmaster/Challenger Solo/Duo trong `data/raw/rank_lake/league_lists/{platform}/{tier}/`. Mỗi thành viên có PUUID trong danh sách được lưu snapshot với tier của response, cùng observed_at thật và source_kind=league_list_membership; không suy rank từ một seed sang chín người khác. Kiểm đúng tier/queue trước khi nhận, transaction theo danh sách thay vì commit từng người. Refresh danh sách sau15phút thay cho seed-only6giờ cũ. Chỉ reuse cho người có tên thực, cache<=15phút và snapshot>=matchend; thiếu, cache cũ hoặc trận kết thúc sau snapshot thì gọi entries-by-puuid. Mỗi người vẫn qua classify_match và lưu bằng chứng đủ10người. Không suy người vắng danh sách là rank thấp hoặc xóa bằng chứng cũ; chỉ không dùng cache cũ để xác nhận trận mới. Nguồn [League-v4 chính thức](https://developer.riotgames.com/apis#league-v4).

`next_job` luân phiên server và khám phá seed ở server khác ngay khi một server còn backlog, cursor lưu metadata. Mục đích là tránh một server chiếm mọi lượt; đây là policy thu tự thiết kế, không chứng minh lấy mẫu ngẫu nhiên hoặc tối ưu.

Chỉ xuất lại bảng, không gọi mạng:

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/update_rank_evidence.py --export-only
```

Đây là thống kê Rank bổ sung. Không tự trộn Pro vào mẫu Rank, bật tín hiệu Pro hoặc chứng minh cải thiện draft. Đánh giá chuyển giao sang Pro vẫn là bước riêng. Code: `rank_matchup_tables.aggregate/export_tables` và CLI `update_rank_evidence.main`. Không thay schema SQLite, không retrain ML. Truy vết kiến thức tại sổ mục23/MR-21/NV-17.
