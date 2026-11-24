# Hai khu lựa chọn và contextual v2 — 24/11/2026

Gợi ý và Chọn tay hiện cùng lúc ở hai panel, có nút xác nhận riêng. Chọn tay không ẩn gợi ý; xác nhận một khu sẽ chuyển lượt, cập nhật cả hai. Hướng dẫn: [UI](../../docs/UI_REACT_TYPESCRIPT.md).

Contextual v2 sửa cách tính utility pool ít lựa chọn. Cũ: mean(top min(3,n)); mới: sum(max(score,0) của top3)/3. Ví dụ [0.9,0.6] có utility cũ0.75; bỏ backup0.6 thì thành0.9, loss bị clip0 dù mất backup. Mới0.5→0.3, loss0.2. Slot không có lựa chọn có utility0 là quy ước scoring, **không** điền dữ liệu thống kê thiếu bằng0. Selfcost/accessfactor/weights, luật draft và pickcurrent giữ nguyên. Không hardcode tên tướng hoặc ép đa dạng ban.

## Kiểm tra cùng dữ liệu

WLDS16.20,80pre-action ban states thật:40validation/40test, lấy cách đều theo thời gian trong mỗi partition đã xác định. History đóng băng trước validation, có guard matchend; splitseries dùng lại protocol hiện có. Cả hai cách chấm dùng cùngsnapshot/currentpick/roster/suyrole/exclusions/pool. Không dùng role cuối trận, vàng/XP/CS trong trận query, winner hoặc Rank để score. Không tune sau khi nhìn test.

| Phép đo | Validation40 | Test40 |
|---|---:|---:|
| Số probe bỏ tướng nhưng tăng pool — cũ→v2 | 10→0 | 21→0 |
| Trạng thái có pool role dưới3lựa chọn | 2 | 6 |
| Top1 thay đổi | 1 | 7 |
| Top5 có đổi thứ tự hoặc thành viên | 3 | 8 |
| Recall@5 ban lịch sử — cũ→v2 | 67.5%→67.5% | 52.5%→52.5% |

[comparison.json](comparison.json) lưu cutoff/split/sourcehash/metrics; [queries.json](queries.json) lưu từng câu hỏi và top5/rank/poolhash. Recall ban quan sát không phải nhãn ban tối ưu. Dữ liệu từng dùng audit nên không là independent final test. Đây là sửa tính đơn điệu của utilitypool, **chưa chứng minh tăng chính xác chiến thuật, counter hoặc tỷ lệ thắng**. Không thêm một model hoặc chiến lược thứba.

## Cấu hình và tái lập

Thanh cấu hình hiện Ban contextual/legacy, Pick current, ngàycutoff và snapshotID. Session mới được chốt ngàyUTC khi ngày trống; session/export giữ ngày đó. ID hash nguồnPro/scope/đội-roster/scoring-ngưỡng/versioncontextual; cấu hình hoặc nguồn không khớp trả409. Nếu chínhProDB đổi trong vòng đời cache, API đòi restart. Fingerprint không lưu một bản saoDB/code cũ và không tự hồi phục enginephiênbảntrước. Phiênxungđột vẫn xuấtinputs cũ/tạophiênmới được.

## Kiểm chứng triển khai

- TypeScript/Vite buildPASS.159Python testsPASS, gồm2testutilitypool và3testpin/replay/config/sourcecache. [Log](tests.log).
- 2workflowEdgePASS: hai panel cùnghiện, ban tay/gợi ý, pick cóbảngProRank, flex/undo, autođủ1ván, sangván2khóa10, archive/export/reload/mobile390px; và snapshotconflict vẫnexport/tạophiênmới. Khôngpageerror/trànngang. [Browserlog](browser.log), [desktop](desktop.png), [mobile](mobile.png), [exportthật](export.json).
- CanonicalSQLiteSHA20e3d973...giữnguyên, khôngretrain/nhậpRank/commit/push; publicexport khôngplayeridentifiers/APIkey. [Checks](checks.json). Rankcollector khôngđược thayđổi trong lượt này.
- UI/API bản mới đang phục vụ127.0.0.1:8000; PIDtạm ở [process.json](process.json), cần xácminh trước khi dừng. Thư mụcui_demo giữ nguyên mốcv1, không phải ảnhbảnhiệnhành.

Tái lập: `.\.venv\Scripts\python.exe scratch/check_contextual_revision.py`; `npm --prefix web run build`; `.\.venv\Scripts\python.exe -m unittest discover -s tests`; `.\start_ui.ps1`; tạiweb`npm run test:e2e` khiAPIđãchạy vàcóEdge.
