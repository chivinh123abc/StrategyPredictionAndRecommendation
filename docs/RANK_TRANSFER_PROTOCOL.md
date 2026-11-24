# Phép thử Rank / Pro cho thành phần đối đầu — 24/11/2026

**Cập nhật cohort:** dữ liệu trong phép thử này lấy từ seed Thách Đấu, chưa xác nhận rank lịch sử cả10người. Không gọi kết quả này là benchmark Rank cao đã xác nhận. Thiết kế hai chế độ và admission policy mới: [HAI_CHE_DO_VA_TIEU_CHUAN_RANK_CAO.md](HAI_CHE_DO_VA_TIEU_CHUAN_RANK_CAO.md). Evaluator hiện mặc định chặn cohort thiếu bằng chứng; lệnh tái lập bên dưới dùng flag nghiên cứu công khai và output riêng, folder tái lập đó chưa tồn tại khi chưa chạy.

Phạm vi: chuẩn hóa dữ liệu, lấy thêm mẫu, đánh giá ba nguồn đối đầu và quyết định có đủ bằng chứng để cân nhắc tích hợp hay chưa. Không sửa `draft_advisor.py`, ban planner, model hoặc SQLite. Đây là **phép thử thăm dò**: dữ liệu Worlds hiện có đã được dùng trong các audit trước, nên không gọi test lần này là final test hoàn toàn mới.

## Quy ước đã chốt trước khi chạy evaluator

- Tên tướng: Data Dragon chính thức, pin `16.20.1`, ID số -> tên hiển thị; alias nội bộ và tên hiển thị chuẩn hóa bằng ký tự/chữ hoa-thường. Tên không có trong catalog gây lỗi/loại có lý do, không fuzzy-match hoặc viết danh sách tướng ngoại lệ. Pro ban/pick/player đều chuẩn hóa cùng nguồn.
- Rank: tối đa20seed từ danh sách Thách Đấu KR hiện tại, mỗi seed tối đa5match ID, tổng tối đa100trận; query UTC01–14/10/2026 để có dữ liệu trước holdout Worlds. Dedup match ID; lưu seed_counts và query_start/end trong collection_manifest. Đây là lấy mẫu thuận tiện, không phải mẫu rank đại diện hoặc xác nhận trình độ10người lúc trận diễn ra.
- Chuẩn dữ liệu giữ strict5role mỗi đội; CS Rank là lính+quái. [Từ điển Oracle's Elixir](https://lol.timsevenhuysen.com/matchdata/match-data-dictionary/) cũng mô tả CS gồm lính và quái, loại ward/đơn vị khác; vẫn chưa chứng minh mọi cơ chế đếm quái qua patch giống nhau. Audit tổng CS Pro = minionkills+monsterkills và các diff10/15 khi có cột; role sau trận không là lane occupancy được xác nhận.
- Timeline: nearest±1000ms chỉ thống kê mô tả; lưu offset thật, không giả exact10/15 và không dùng gold/XP/CS sau draft làm input draft. `ended_at` Rank bảo thủ lấy max(start+duration, gameEndTimestamp) để không dùng kết quả trận chưa kết thúc trước freeze.
- Pro: tái dựng state chỉ có tướng/ban đã lộ và khóa Fearless các ván trước bằng builder sẵn có. Series ID tái dựng, chưa có ID chính thức; giữ/explain exclusions. Không dùng role cuối trận làm feature hoặc tự suy lịch draft rank.
- Chọn các series patch16.20 theo thời gian, chia60%history/20%validation/20%test, không tách cùng series qua hai tập. Với snapshot hiện có:27/9/10series,46/20/32trận. Freeze toàn bộ thống kê ở ngay trước validation bắt đầu26/10/2026 18:03:09 UTC, không cập nhật với kết quả validation hoặc test. Pro chỉ nhận trận đã kết thúc trước freeze; Rank bắt buộc đúng patch16.20/KR, nằm trong60ngày và đã kết thúc trước freeze. Không lấy rank16.23 hiện tại đánh giá ngược Worlds16.20.

## Ba cấu hình so sánh

Giữ nguyên pool, điểm meta/draft slot/content/mastery/synergy/composition, baseline winrate Pro, prior10, min_games5 và suy role từ lịch sử trước cutoff. Chỉ đổi nguồn đếm đối đầu cả đội địch đã lộ:

| Cấu hình | Thành phần matchup |
|---|---|
| `pro_only` | Đúng `DraftAdvisor.evaluate_enemy_context` hiện tại. |
| `rank_only` | Counts/wins lấy từ Rank theo cả hai role; cùng công thức residual và shrinkage như control. Thiếu n5 thì neutral0.5. Đây không phải hệ thống mọi thành phần đều học từ Rank. |
| `hybrid` | Với từng cặp Rank đạt n5, trung bình50/50 residual Pro và Rank; nếu Rank thiếu mẫu giữ nguyên Pro. Không có chuyện thiếu dữ liệu Rank mà vẫn giảm điểm Pro về0.5 rồi nhận là cải thiện nhờ Rank. Không cộng counts hai miền. |

Trọng số50/50 và cách chia tập là policy nghiên cứu do nhóm tự thiết kế, chưa được tối ưu. Không tune từ test, không fit mô hình ML mới. Validation có báo cáo riêng; không đổi policy sau khi xem kết quả rồi gọi cùng test là độc lập.

## Đo lường và quyết định

Replay pick quan sát trên cùng pool hợp lệ, Recall@1/@5, MRR@5, candidate coverage và số query có ít nhất1ứng viên đủ bằng chứng Rank. So chênh Recall@5 với Pro bằng paired bootstrap1000lần theo series tái dựng, seed42, CI95. Query thiếu ứng viên vẫn tính là miss; không chỉ báo cáo phần dễ được phủ. Giữ trace top5/truth/rank/game/turn, kiểm cùng pool cả3mode và không chọn tướng unavailable.

Truy hồi pick thật chỉ đo mức bắt chước lựa chọn chuyên nghiệp, không xác minh counter cơ chế/tăng thắng/chất lượng ban/tối ưu BO5. Cùng người chơi có nhiều trận và ít series làm bootstrap có giới hạn. Chưa sửa chênh kỹ năng/selection bias hoặc chứng minh tương thích CS từng patch.

**Không tự bật hybrid vào contextual.** Chỉ cân nhắc sau khi có coverage đủ dùng, kết quả cải thiện đủ rõ trên phép thử độc lập mới (không chỉ một điểm trung bình hoặc CI bao0), không lệch nhóm/patch bất thường và có review. Do dữ liệu Pro lần này đã được dùng trước, dù metric đẹp cũng chỉ là bằng chứng phát triển; cần dữ liệu giải mới cho xác nhận độc lập.

## Module và lệnh tái lập

```powershell
.\.venv\Scripts\python.exe src/01_data_pipeline/rank_data_contract.py --version 16.20.1 --output data/raw/riot_matchups_study/champion_16.20.1.json
.\.venv\Scripts\python.exe src/01_data_pipeline/ranked_matchups.py --collect --platform kr --seed-players 20 --matches-per-seed 5 --limit 100 --start-time 2026-10-01T00:00:00Z --end-time 2026-10-14T23:59:59Z --frame-policy nearest --catalog data/raw/riot_matchups_study/champion_16.20.1.json --cache data/raw/riot_matchups_study --output reports/rank_pro_study_data
.\.venv\Scripts\python.exe src/07_recommender/evaluate_rank_transfer.py --allow-seed-only-research --output reports/rank_transfer_seed_only_reproduction
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_rank*.py' -v
```

Hai lệnh đầu cần mạng; evaluator dùng cache offline. `rank_data_contract.py` không dùng API token khi tải catalog công khai. Riot token chỉ ở header gửi Riot, không in ra. Collector nghỉ tối thiểu1.3giây giữa request, vẫn tuân thủ429; lỗi/hết khóa dừng có thông báo. Không commit/push.

Outputs evaluator tại `reports/rank_transfer_evaluation/`: `data_contract.json` (định nghĩa/kiểm tra), `name_normalization.json`, `splits.json`, `validation_queries.json`, `test_queries.json`, `evaluation.json`, `REPORT.md`. Trạng thái và số liệu chạy thật được cập nhật ở sổ kiến thức; file chưa sinh không coi là đã có.

Nền môn học: Chương1 thống kê và xác suất (MH-02/03), Chương2 làm sạch (MH-04), Chương4 trang9 nền tách tập (MH-07), Chương5x group/merge (MH-11), Chương6 trang47 nền đánh giá retrieval (MH-14). Chuẩn hóa theo catalog/temporal series split/domain residual mixture/paired series bootstrap là NV/MR dùng lại hoặc policy mở rộng tự thiết kế, không nhận toàn bộ có sẵn trong bài. Truy vết mục18/MR-16/NV-12 của sổ kiến thức.
