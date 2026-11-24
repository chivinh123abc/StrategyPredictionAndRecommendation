# Rà soát và chạy thử draft LCK — 23/11/2026

Đã chạy hai phiên T1 vs GEN.G trước/sau sửa, lưu đầy đủ 20 lượt và căn cứ. Đây là trận giả lập theo dữ liệu LCK, không phải một trận chính thức giữa hai đội và chưa có chứng minh tối ưu chiến thuật.

## Vấn đề xác nhận được

- Policy cũ gộp LCK 2025–2026 (812 ván), không có ngày/patch/cửa sổ chung cho các thành phần.
- Percentile thay đổi khi ứng viên bị cấm; cosine và bể tướng có thể lấn át bằng chứng đối đầu.
- Ban theo chênh top1/top2 đơn lẻ dẫn đến lượt cấm Yorick trong phiên thử cũ; không có đủ căn cứ gọi đó là cấm đúng meta.
- Roster preset có thể cũ; mới đã đọc lineup từ trận gần nhất, GEN.G quan sát được có Duro.

## Thay đổi đã chạy

`draft_meta.py` tạo snapshot dùng chung, cutoff thời gian, patch đích, decay, tần suất slot F1/S1… và nguồn lineup. `draft_advisor.py` tính điểm tuyệt đối, ưu tiên presence/thứ tự chọn, content chỉ hỗ trợ. Flex địch suy từ các cách gán role một-một. Không có bảng tier hay counter gán riêng theo tên tướng. Có freshness guard và danh sách tướng đã dùng ở ván trước. Công thức đầy đủ trong [hướng dẫn](GIA_LAP_BAN_PICK.md).

LCK local mới nhất: 13/09/2026, patch **dataset 16.16**. Snapshot 60 ngày chứa 153 ván, trong đó 80 ván patch đích. So với ngày 23/11/2026 dữ liệu cũ 71 ngày. Riot đã có [patch notes 26.23](https://www.leagueoflegends.com/en-us/news/game-updates/league-of-legends-patch-26-23-notes/); không đồng nhất mã patch của hai nguồn hoặc dùng notes để gán tỷ lệ thắng mới. LCK không thi đấu trên mọi patch live, nên dữ liệu live mới cũng không tự thành meta LCK.

## Ví dụ đầu ra

Thứ tự dưới đây là Top / Jungle / Mid / Bot / Support.

| Phiên | T1 | GEN.G |
|---|---|---|
| Trước | Ambessa / Jarvan IV / Taliyah / Caitlyn / Neeko | Rumble / Xin Zhao / Azir / Yunara / Lulu |
| Sau | Olaf / Naafiri / Ryze / Lucian / Shen | K'Sante / Lee Sin / Syndra / Ezreal / Karma |

Phiên sau cấm T1: Cassiopeia, Nocturne, Bard, Jayce, Lulu; GEN.G: Vi, Orianna, Camille, Pantheon, Jarvan IV. Ví dụ Cassiopeia có presence có trọng số 84.3%, ban rate 73.2% trong cửa sổ local. Đó là lý do thống kê của lượt cấm, không phải tier được nhập tay. Không đánh giá phiên sau tốt hơn chỉ vì tên tướng trông hợp lý hơn.

Nguồn: `reports/lck_draft_before.json`, `reports/lck_draft_after.json`. Phiên sau đóng băng ở `--as-of 2026-09-13 --patch 16.16`; không lấy dự báo winrate model làm thước đo chất lượng.

## Đối chiếu lượt chọn thực tế

Chạy `evaluate_draft_policy.py`: đóng băng trước 04/09/2026 08:07:52 UTC; snapshot 133 trận, 60 trận patch đích. Replay 20 trận sau đó, 200 lượt; chỉ truyền tướng và cấm đã được lộ, không truyền kết quả trận hoặc vị trí cuối cùng. Baseline dùng cùng tập ứng viên hợp lệ; không đổi trọng số sau khi nhìn kết quả audit.

| Phương pháp | Recall@1 | Recall@5 | MRR@5 |
|---|---:|---:|---:|
| Presence toàn lịch sử | 1% | 24% | 0.0776 |
| Presence gần đây có decay | 6.5% | 27% | 0.1355 |
| Policy patch + slot + ngữ cảnh | 7% | 28.5% | 0.1485 |

Paired bootstrap theo ván, 300 lần, CI95 chênh Recall@5 so với recent presence: **[-1.5, +4.5] điểm phần trăm**. Chưa đủ chứng minh vượt baseline. Candidate coverage 84.5%: 15.5% lượt thực tế không nằm trong pool do hạn chế mẫu/role/patch. Đây là audit phát triển nhỏ, chưa là final test độc lập, chưa đánh giá lượt cấm hoặc tăng thắng. Benchmark chưa dựng lại tướng đã dùng ở các ván trước theo Fearless; các lượt trong cùng series cũng có phụ thuộc chưa được phản ánh bằng bootstrap theo series. Chi tiết và ví dụ từng lượt: `reports/lck_draft_policy_evaluation.json`.

## Hướng cải thiện tiếp theo theo ưu tiên

1. Dữ liệu và luật theo sự kiện: lưu provenance, patch, roster, thứ tự draft, series/ván, pool Fearless và tướng bị khóa bởi giải. Không trộn ranked live vào LCK như cùng một phân phối. Riot có [Open Access qua GRID](https://lolesports.com/en-US/news/build-with-official-league-of-legends-esports-data), bắt đầu với Worlds 2026; phải kiểm tra phạm vi quyền truy cập, không mặc định có toàn bộ LCK. Chưa tích hợp hoặc tải nguồn này.
2. Thay trọng số thủ công bằng learning-to-rank hoặc mô hình dự đoán lựa chọn tiếp theo: học trên quá khứ, chọn hyperparameters bằng validation theo thời gian/series, final test riêng và nhiều patch. So sánh popularity, recent presence, slot-only, mastery-only và ablation content; đo Recall/NDCG/MRR/coverage. Chỉ giữ content nếu có lợi ích đo được; phần minh chứng Chương 6 vẫn có pipeline riêng.
3. Xử lý patch ít mẫu bằng hierarchical shrinkage/backoff có nhãn độ tin cậy; tránh ngưỡng cứng 5 trận làm mất toàn bộ tướng mới. Đánh giá riêng patch mới và tuyển thủ/đội chưa thấy.
4. Sau khi có evaluator đáng tin, dùng beam search/minimax giới hạn hoặc MCTS để xét phản ứng đối thủ và flex, cùng trạng thái toàn series Fearless. Tìm kiếm sâu trên evaluator yếu chỉ tối ưu sai số của evaluator; hiện chưa triển khai hay tuyên bố tối ưu toàn cục.

## Chạy lại

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py --auto --blue-team T1 --red-team GEN.G --region LCK --as-of 2026-09-13 --patch 16.16 --save-session reports/lck_draft_after.json
.\.venv\Scripts\python.exe src/07_recommender/evaluate_draft_policy.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Bỏ `--auto` để tự chọn. Thêm `--first-pick red` để đổi bên draft trước, độc lập màu phe theo [First Selection chính thức](https://lolesports.com/en-GB/news/season-start-2026-lol-esports). Để kiểm tra dữ liệu mới so với hôm nay, bỏ `--as-of` và thêm `--max-data-age-days 14`: hiện LCK sẽ bị từ chối vì dữ liệu quá cũ.

Kiểm chứng thực thi: **31 unit tests PASS, 6 CLI scenarios PASS**; 4 phiên hoàn thành 20 hành động/tướng khác nhau, 2 phiên từ chối đúng dữ liệu cũ/patch thiếu. Biên bản: `reports/lck_meta_checks.json`. Đã đồng bộ PROJECT_STATE/TASKS/CHANGELOG/ARCHITECTURE/DECISIONS; không thay schema, raw DB hoặc huấn luyện model.
