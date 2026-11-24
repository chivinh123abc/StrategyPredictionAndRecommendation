# Xử lý lựa chọn thiếu căn cứ theo đội hình — 24/11/2026

**Phạm vi chốt theo yêu cầu người dùng:** hoàn tất rà soát/sửa vấn đề Trundle và những lựa chọn tương tự, sau đó dừng. Không tiếp tục phát triển dự đoán đối thủ, search hoặc tối ưu BO5 trong đợt này.

## 1. Lỗi xác nhận được

Phiên cũ `reports/worlds_fearless_bo5/game_2.json`, lượt20, Gen.G chọn Trundle rừng. Địch đã lộ JarvanIV, Locke, Lulu, Yunara, Gnar. Đối đầu cùng vị trí Trundle–JarvanIV không có mẫu. Điểm matchup cũ trung tính; các thành phần meta/đội mình đưa Trundle lên đầu và chế độ auto vẫn chốt. Không có evaluator cơ chế kỹ năng để xác nhận đây là counter hoặc tốt hơn các lựa chọn khác.

Không thể kết luận “cứ gặp tank là pick Trundle” hoặc “không counter thì luôn cấm Trundle”. [Mô tả Trundle chính thức của Riot](https://www.leagueoflegends.com/en-us/champions/trundle/) nêu cơ chế lấy máu/giáp/kháng phép; mô tả này không tự cung cấp trọng số, phân loại toàn bộ đội hình hoặc xác nhận hiệu quả của lượt draft lịch sử. Chưa có lớp đặc trưng cơ chế được xác minh theo patch, vì vậy không bịa ma trận khắc chế.

## 2. Sửa tổng quát đã hiện thực

| Thay đổi | Nơi dùng | Chức năng |
|---|---|---|
| Đối đầu với toàn bộ role địch đã lộ | `draft_meta.py`: `enemy_evidence`; `draft_advisor.py`: `evaluate_enemy_context` | Ghép đúng game, phe đối thủ và cả hai role. Không chỉ xét cặp cùng đường. |
| Giữ độ bất định của flex và số mẫu | `infer_enemy_roles`, `enemy_context_evidence` | Suy role theo lịch sử, không coi role đang gán là chắc chắn; lưu n/WR/Wilson/role probability cho từng đối thủ. |
| Coverage đối đầu và nhãn thiếu căn cứ | `enemy_context_coverage`, `mechanical_counter_status`, `selection_basis`, `review_required` | Khi không có đối đầu đủ mẫu, không diễn giải điểm meta/cosine/co-pick thành chứng minh counter. |
| So sánh các ứng viên tại đúng lượt | `audit_draft_choices.py`; `pick_candidates` | Giữ nguyên pool hợp lệ, role, lịch sử đã lộ và cutoff; xuất top5/điểm/số mẫu. Phiên live lưu3 phương án cùng role. |
| Dừng tự chốt khi chưa đủ căn cứ đáp trả đội hình địch đầy đủ | `simulate_draft_match.py`: `needs_tactical_review`, vòng chạy simulator | Khi địch đã lộ5tướng và ứng viên auto có coverage đủ mẫu bằng0, dừng trước khi apply pick; lưu `manual_review` và `complete:false`. |

Công thức thống kê bổ sung: với mỗi đối thủ/role có n≥5, lấy residual `WR(C|địch)-WR(C)`, shrink `n/(n+10)`, trộn theo xác suất role và chia số tướng địch đã lộ, cộng nền0.5. Không đủ mẫu không cộng residual. Địch có nhiều role không làm các quan sát trở thành các trận độc lập; đây vẫn là dữ liệu kết quả cả trận, không đo cơ chế counter hoặc thắng đường. Công thức kết hợp là policy mở rộng tự thiết kế, chưa được tune/kiểm chứng chiến thuật độc lập.

Điểm này **không tự biến một tướng khác thành lựa chọn tốt hơn** khi tất cả đều thiếu căn cứ. Với dữ liệu hiện tại chỉ5/50pick cũ có coverage đối đầu>0; do đó tự ép chọn một tên khác sẽ che giấu vấn đề thiếu dữ liệu.

## 3. Hành vi sau sửa

- Mặc định auto, nếu điều kiện trên xảy ra: dừng trước pick, `manual_review` ghi ứng viên, role, địch đã lộ và phương án khác; CLI một ván trả exit code3. Không ghi đủ20lượt giả và không tính dự báo cho đội hình thiếu tướng.
- Chọn tay ở phe người dùng vẫn được phép; đây là quyết định của người dùng, không nâng nhãn counter thành đã xác nhận.
- Blind pick khi địch chưa đủ5tướng không bị chặn bởi rule này. Có một ít bằng chứng đối đầu cũng chưa chứng minh tối ưu; hệ thống vẫn giữ `mechanical_counter_status:not_evaluated`.
- Có `--allow-statistical-auto` cho **demo một ván thuần điểm thống kê**. Đây là lựa chọn tường minh cho phép auto thiếu căn cứ, không phải khuyến nghị chiến thuật hoặc cách vượt qua phép kiểm chứng.
- Driver series dừng và lưu phiên dở nếu một ván cần tactical review. Các báo cáo5ván cũ được giữ làm lịch sử trước gate này, không gọi là kết quả chiến thuật đã được xác nhận.

## 4. Kết quả xác minh

### Đúng trường hợp Trundle được yêu cầu

[trundle_case_review.json](../reports/trundle_case_review.json) tái dựng19lượt đầu của ván2 với pool Fearless và cutoff cũ. Xếp hạng thống kê tại lượt20:

| Ứng viên rừng | Điểm xấp xỉ | Coverage đối đầu đủ mẫu với địch |
|---|---:|---:|
| Trundle | 0.187 | 0% |
| Skarner | 0.179 | 0% |
| Naafiri | 0.153 | 0% |
| Xin Zhao | 0.151 | 0% |
| Maokai | 0.111 | 0% |

Sau gate: **không apply Trundle**, giữ19hành động và vị trí rừng trống. Trundle vẫn có điểm cao nhất trong heuristic nhưng không được tự chốt như đáp án tối ưu. Đây là xử lý đúng mức thiếu căn cứ; chưa có chứng minh tướng thay thế nào thực sự mạnh hơn.

### Tình huống tương tự và regression

- Audit cả50pick cũ: [draft_choice_audit.md](../reports/draft_choice_audit.md), [JSON](../reports/draft_choice_audit.json); không chỉ phân tích một tên tướng. Thêm cross-role context chưa làm đổi top1 ở50lượt cũ; không dùng kết quả đó để tuyên bố cải thiện chất lượng chiến thuật.
- CLI live Gen.G–BLG ở Worlds, cutoff13/11, dừng tại lượt20 trước khi auto chốt **Pantheon**, lưu19actions và manual_review. Điều này cho thấy rule áp dụng cả tướng khác, không phải blacklist Trundle.
- Kết quả CLI: [tactical_review_session.json](../reports/tactical_review_session.json), [tactical_review_checks.json](../reports/tactical_review_checks.json). Expected exit3 đã kiểm tra qua subprocess; không nhầm PowerShell stderr wrapper với trạng thái của Python.
- **51 regression tests PASS**, gồm cross-role counts/không ghép đồng đội thành đối thủ, thay role địch làm đổi điểm context, gate không phụ thuộc tên tướng, không chặn blind pick, override demo giữ nhãn chưa xác nhận, state trước lượt/role feasibility và các kiểm tra cũ.

```powershell
# Audit lại các lượt trong series đã lưu, không tạo kết quả thắng/thua phản thực
.\.venv\Scripts\python.exe src/07_recommender/audit_draft_choices.py

# Auto thận trọng: có thể trả3 và chờ tactical review
.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py --auto --region WLDS --blue-team "Gen.G" --red-team "Bilibili Gaming" --as-of 2026-11-13 --patch 16.20 --save-session reports/tactical_review_session.json

.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 5. Kiến thức và điều còn thiếu

Nền tảng: Chương1 về thống kê/xác suất có điều kiện, Chương5x về groupby/merge. Phần MR: cross-role residual shrinkage, coverage và chính sách abstention. Phần NV: lưu audit/alternative/manual-review, exit3 và giữ phiên chưa hoàn chỉnh. Đây không phải công thức counter được dạy sẵn trong slide.

Còn thiếu evaluator cơ chế tướng/đội hình theo patch với nguồn xác nhận, đánh giá lựa chọn thay thế và trạng thái đủ dữ liệu; chưa có căn cứ để tuyên bố “chọn tối ưu” hoặc tăng thắng. Các mục đó được giữ ở backlog, **không triển khai tiếp sau khi người dùng yêu cầu dừng**. Sổ kiến thức tổng hợp ghi rõ tình trạng này.
