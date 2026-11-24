# Bằng chứng đối đầu Pro / Rank và thử nghiệm contextual

Cập nhật 24/11/2026. Ba phần: thống kê Pro thật, giải thích gợi ý bằng hai nguồn riêng, và thử nghiệm tín hiệu Rank không đổi bản chính.

## Thống kê Pro

`src/07_recommender/matchup_evidence.py:pro_observations/export_pro` dùng `analysis_data.load_clean_tables`, không sửa SQLite. Chỉ nhận trận đủ hai đội và năm role mỗi đội; không nhận role trùng. Ghép cùng `gameid/position`, khác `side`. Tên và ID tướng đối chiếu catalog Riot chính thức đã ghim16.20.1; không thêm ngoại lệ tên thủ công. Nếu không xác nhận được danh tính tướng thì không dùng trận đó; summary công khai số input và số xuất.

GD/XPD/CSD tại10/15 = chỉ số người chọn trừ chỉ số đối thủ cùng role trong chính trận. Dùng chỉ số từng người thực có, không suy từ số liệu tổng đội; giữ âm. Chỉ đo khi cả hai giá trị không âm, hữu hạn, không thiếu và trận đã kéo dài tới mốc tương ứng. Thiếu không điền0. CS là trường `csat10/csat15` của nguồn; audit trước đó đã đối chiếu dữ liệu CS, không suy creep từ tiền.

Kết quả đã xuất ở `reports/pro_matchups/`:3.000trận/30.000dòng,24.370phép đo mỗi chỉ số phút10 và24.380phút15;3.098kèo gộp/1.170kèo có n>=5. Hai hướng cùng kèo là cùng tập trận nhìn từ hai phía, không phải hai lần số trận độc lập.

| File | Ý nghĩa |
|---|---|
| `observations.csv` | Kèo từng trận, role, side, thời gian, kết quả, các chênh lệch; không xuất danh tính người chơi |
| `all_matchups.csv` | Tách league/patch/role/hướng tướng |
| `pooled_all_matchups.csv` | Gộp league/patch thực có; giữ danh sách nguồn, số người và khoảng tin cậy |
| `best_full_game_matchups.csv` | Winrate cao trước, theo đối thủ/role, n>=5 |
| `unfavorable_full_game_matchups.csv` | Winrate thấp trước |
| `early_gold_advantages.csv` | GD15 cao trước, cần nGD15>=5 |
| `summary.json`, `REPORT.md` | Độ phủ, cách hiểu và hash DB |

Winrate là kết quả cả đội, không phải tỷ lệ thắng duel. Wilson95 cho winrate và Student-t95 cho trung bình dùng lại phương pháp MR-20. Số người được đếm từ tên tuyển thủ nguồn, không xác thực danh tính xuyên mọi hệ thống. Người chơi lặp, gank, đội hình, side và patch gây phụ thuộc/confounding. N5 chỉ là ngưỡng hiển thị.

## Bảng giải thích cho từng ứng viên

`DraftAdvisor.recommend_picks` thêm `matchup_source_comparison`; không sửa score, weights, thứ tự xếp hoặc policy ban. `simulate_draft_match.show_candidates/explain` hiển thị bảng trong gợi ý và lệnh `why N`. JSON phiên giữ cùng bằng chứng.

Địch còn flex thì dùng phân bố role đã có của advisor, ghi `p(role)`; không coi vị trí tạm gán là sự thật. Chỉ giải thích kèo cùng role mà phân bố hỗ trợ. Khi chưa lộ đối thủ cùng role, không bịa kèo. Thống kê này không thay thế phần đánh giá toàn bộ đội địch đã có.

- Pro dùng đúng region và cửa sổ lịch sử của snapshot advisor, chỉ các trận đã kết thúc trước cutoff. Các số là thống kê mô tả không trọng số; không phải diễn giải từng phép nhân trong score meta có trọng số thời gian.
- Rank đọc một transaction SQLite chỉ đọc, có thể đọc trong khi collector ghi WAL. Bản chụp giữ cố định trong một instance advisor; mở phiên mới để lấy dữ liệu mới. Gộp các patch/server thực có, vẫn giữ provenance. Không đọc tuần tự nhiều CSV đang cập nhật để tránh trộn các mốc export.
- Thời điểm Rank khả dụng = max(thời điểm qualification, thời điểm ghi observations vào kho). Trận đã kết thúc nhưng timeline được tải muộn không được coi là đã biết từ trước. Trận/nguồn khả dụng sau `as_of` không được đưa vào bảng cho quá khứ.
- Nguồn Rank là đủ10Master+ tại thời điểm kiểm tra theo policy collector, không phải xác minh chính xác rank lịch sử hoặc MMR. Không nhập Pro vào mẫu Rank.

Mỗi nguồn có số trận, winrate/Wilson, GD/XPD/CSD10/15, n đo được riêng, CI của từng trung bình trong JSON, cùng danh sách patch/server. Console hiển thị sáu trung bình, n và CI GD15/Wilson. Không có mẫu thì WR/mean/CI đểNA, không hiển thị0% giả.

`compare_sources` phân biệt thiếu mẫu; thiếu phép đo; trung bình GD15 trái dấu nhưng chưa chắc chắn; và hai CI GD15 nằm hoàn toàn ở hai phía0. Flag WR trái chiều chỉ là hai raw winrate ở hai phía50%, không phải kiểm định ý nghĩa. Cùng chiều cũng không xác nhận counter bền qua patch. Không trộn hai khoảng tin cậy thành một.

Ví dụ đã chạy ở `reports/pro_rank_explanations/recommendations.json` và `REPORT.md`: WLDS bot gặpEzreal, trả Jhin/Yunara/Lucian/Ashe/Kai'Sa cùng bằng chứng. Đây là ví dụ lấy từ dữ liệu, không phải luật gán cứng cho cặp này. Test bảo đảm bật/tắt giải thích không đổi score/thứ tự; test console kiểm tra cả hai nguồn và missing.

## Thử nghiệm nguồn Rank

`evaluate_contextual_evidence.py` dùng `TransferAdvisor` hiện có, chỉ thay thành phần matchup. `LaneRankEvidence` chỉ cung cấp same-role counts từ snapshot Rank. Pro-only giữ bản hiện tại; Rank-only chỉ thay nguồn của thành phần matchup, các thành phần khác vẫn Pro. Hybrid cố định50/50 residual ở kèo Rank n>=5, thiếu thì giữ Pro; không cộng số trận hai miền. Prior10 và ngưỡng5 dùng lại policy hiện hành; không tune từ test. Gold/XP/CS chỉ giải thích, không được dùng như feature đã biết trước draft.

Mỗi lần tạo freeze lưu raw snapshot riêng trong `data/raw/contextual_evidence_experiments/{timestamp}/freeze.json` (private, không public PUUID), cùng thời điểm/catalog/region/patch/policy. Có thể tái lập bằng `--freeze` cùng file. Freeze chuyển missing thành JSONnull, giữ số âm.

Đánh giá đúng thời gian dùng5series hoàn chỉnh đầu tiên sau freeze làm validation và5series tiếp theo làm test, không overlap. Đây là thiết kế của nhóm, chưa phải phân tích power. Series được tái dựng từ dữ liệu, chưa xác thực ID chính thức. Pro history và Rank đều đóng băng trước query. Hiện dữ liệu giải mới nhất14/11, trong khi freeze24/11, nên chưa có series tương lai: `prospective_readiness.json` phải `ready=false/result=null`, không tạo metric giả.

`--retrospective-diagnostic` chạy thăm dò trên phần Worlds16.20 tách series theo60/20/20 thời gian như evaluator trước; giới hạn mặc định30query mỗi phần validation/test. Nguồn Rank có thể được thu sau các trận này; các trận Pro cũng đã xuất hiện trong audit cũ. Report ghi `uses_post_cutoff_rank`, `reused_pro_dataset`, `promotion_eligible=false`. Chỉ dùng để thấy cơ chế đổi gợi ý, không phải kiểm chứng nâng chất lượng. Không gọi tập này là final test độc lập mới. Đặt `--max-queries-per-split 0` để chạy toàn bộ thăm dò, không biến nó thành độc lập.

Outputs `reports/contextual_rank_experiment/`: `evaluation.json`, `prospective_readiness.json`, `diagnostic_queries.json`, `REPORT.md`. `prospective_queries.json` CHƯA TỒN TẠI vì chưa đủ dữ liệu tương lai. Các metric Recall@1/5, MRR@5, coverage và bootstrap delta theo series chỉ đo truy hồi pick đã quan sát, không đo chiến thuật/tăng thắng/chất lượng ban hoặc tối ưuBO5. CI[0,0] khi hit/miss giống nhau không chứng minh tương đương tổng thể.

Không thay điểm bản chính hoặc bật `rank_signal_enabled`. Nếu đủ dữ liệu prospective, gate kỹ thuật chỉ ghi `retrieval_review_gate_passed` khi CI deltaRecall5 phía dưới>0 và MRR không giảm; không tự bật runtime. Điều đó vẫn chưa chứng minh counter chiến thuật.

## Chạy lại và truy vết

```powershell
.\.venv\Scripts\python.exe src/07_recommender/matchup_evidence.py
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py --region WLDS --as-of 2026-11-24 --patch 16.20 --ban-strategy contextual
.\.venv\Scripts\python.exe src/07_recommender/evaluate_contextual_evidence.py --retrospective-diagnostic --max-queries-per-split 30
```

Thống kê không retrain model. Nền môn: thống kê mô tả, làm sạch, SQL/groupby/ghép khóa; MR mở rộng: CI và thiết kế thăm dò/holdout, policy residual dùng lại. Không thêm thuật toán CB/CF hoặc kiến thức mới Chương6. Truy vết đầy đủ tại sổ kiến thức mục24/MR-22/NV-18.

Nguồn: [Oracle data dictionary](https://lol.timsevenhuysen.com/matchdata/match-data-dictionary/), [Riot API](https://developer.riotgames.com/apis), [NIST CI mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). Cách chia tập, ngưỡng và công thức hybrid là policy của dự án, không nhận là thuật toán của U.GG.
