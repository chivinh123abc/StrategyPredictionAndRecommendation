## Dừng collector Rank chạy nền & chốt số liệu báo cáo — 2026-11-24

Đã dừng tiến trình collector Rank chạy nền (`update_rank_evidence.py --platforms kr,euw1,na1 --watch`, PID `29828` và worker `7992`) theo yêu cầu người dùng; đã kiểm tra không còn tiến trình nào đang chạy (`NO_RANK_COLLECTOR_RUNNING`). Số liệu kho `ranked_evidence.db` đóng băng tại [reports/rank_matchups_live/summary.json](../reports/rank_matchups_live/summary.json): **975 trận hoàn chỉnh**, **9,750 dòng quan sát**, **5,236 cặp gộp**, **148 cặp `n >= 5`** (`dataset_sha256: d4b6dca5...`). Đã cập nhật khớp số liệu `975` vào cả `BAO_CAO_CUOI_KY_PTIT.docx` và `BAO_CAO_CUOI_KY.md`. Không thay đổi phương pháp/code/DB/model, không retrain, không commit/push.

## Xuất Báo cáo cuối kỳ định dạng Word (.docx) kèm 13 biểu đồ & phân tích mạch giá trị — 2026-11-24

Đã tạo [reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx](../reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx) (4,725.6 KB, 105 đoạn, 15 bảng/callout, 13 hình nhúng trực tiếp gồm `fig1`–`fig9`, `fig11` và 3 ảnh chụp Web UI thật) qua `scratch/build_final_report_docx.py`. Mỗi chương đều phân tích rõ mục đích phân tích dữ liệu và đóng góp trực tiếp vào sản phẩm cuối cùng, tách bạch `MH`/`UD` vs `MR`/`NV`, trích số liệu thực từ SQL Q1–Q5, 3 kiểm định giả thuyết, ML v2 và Content-Based Chương 6, kèm giải trình giới hạn của `draft_model` và `content_based`. Đã cập nhật `reports/README.md`. Không thay đổi phương pháp/code/DB/model, không retrain, không commit/push.

## Biên soạn Báo cáo cuối kỳ — 2026-11-24

Đã tạo bản hoàn chỉnh [reports/final_report/BAO_CAO_CUOI_KY.md](../reports/final_report/BAO_CAO_CUOI_KY.md) bám sát Chương 1–6 từ sổ kiến thức và các file kết quả thực tế (`hypothesis_test_*.csv`, `evaluation_report.md`, `content_based_evaluation.md`, `pick_scoring_comparison/REPORT.md`, `legacy_contextual_comparison/COMPARISON.md`, `integrity_summary.json`, `rank_matchups_live/summary.json`). Phân định rõ `MH`/`UD` vs `MR`/`NV`, giải trình thẳng thắn giới hạn của `draft_model` (Acc `0.5517` vs `training_prior` `0.5650`), `content_based` (Recall@5 `0.2990` vs `popularity` `0.4652`), artifact phân cụm cũ và các giới hạn chưa có fresh final test / BO5 planner. Đã cập nhật `reports/README.md`. Không phát sinh thay đổi kiến thức/phương pháp/chức năng/code/DB/model; không retrain, không commit/push.

## Dọn sạch & chuẩn hóa tài liệu, dừng web server nền — 2026-11-24

Đã dừng tiến trình web server nền (`uvicorn src.api.app:app` cổng `127.0.0.1:8000`, PID `28952` / `46456`) theo yêu cầu người dùng; đã kiểm tra cổng `8000` không còn lắng nghe. Đã xóa các đoạn lặp tiêu đề NV-24 và sửa lỗi dính chữ trong `AI/{PROJECT_STATE,ARCHITECTURE,TASKS,CHANGELOG,DECISIONS,DATABASE}.md` và mục 28–30 của `docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md`; thu gọn 14 banner đầu `README.md` thành bảng trạng thái hiện hành và tạo mục lục `reports/README.md` phân tách rõ sản phẩm nộp môn, minh chứng hiện hành và artifact lịch sử. Không phát sinh thay đổi kiến thức/phương pháp/chức năng (các mục MH-01..14, MR-01..24, NV-01..24 giữ nguyên); không thay đổi code/DB/model, không retrain, không commit/push.

## Thu gọn toàn bộ Hiểu lựa chọn — 2026-11-24 (NV-24)

Inspector React thêm `collapsed` state và nút **Thu gọn toàn bộ** ở header. Khi collapsed, unmount toàn bộ body (tên, cảnh báo, lý do, thành phần, bảng nguồn, footer), chỉ giữ header nhỏ có nút Mở rộng / Đóng; `timeline y` giảm khi collapse. Khi mở rộng sẽ khôi phục body như cũ, selection không đổi, hành vi click-only và deselect cũ giữ nguyên. CSS header button dùng flex cùng `aria-expanded`/`aria-controls`. Build TS/Vite PASS; Edge 1 workflow PASS (`body` absent, header < 100px, timeline gần hơn, reopen body > 100px, close/deselect/reset/reload). Minh chứng: `reports/ui_inspector_collapse/{REPORT.md,browser.log}`. Chỉ thay đổi UI presentation (NV-24), không đổi khoa học/API/score/schema/model nên không chạy lại Python test hay retrain; không commit/push.

## Hiểu lựa chọn ẩn mặc định và click-toggle — 2026-11-24 (NV-24)

React App đặt `selected=null` và `inspectorOpen=false` mặc định, cũng như sau khi accept hoặc đổi ván. Bấm thẻ gợi ý / chọn tay sẽ mở Inspector; bấm lại thẻ đang chọn sẽ bỏ chọn và ẩn. Nút Đóng giữ selection và cho phép mở lại qua nút riêng; bỏ chọn (deselect) sẽ không còn nút mở. Lịch sử click để mở / bấm lại để ẩn, không tự popup qua chuyển lượt hay reload. Không tạo fake advice cho lựa chọn tay ngoài pool. Chỉ thay đổi UI state/CSS, không đổi phương pháp khoa học/API/scoring/model/DB nên không train hay chạy lại Python test. TS/Vite build PASS, toàn bộ 7 Edge workflow PASS (layout nhiều độ rộng, draft, Fearless, drag, role, counter case, toggle, reset). Minh chứng: `reports/ui_inspector_toggle/REPORT.md` + `browser.log` + browser artifacts. Sổ kiến thức mục 30 (NV-24) và hướng dẫn sử dụng đã đồng bộ; không commit/push.

## Sửa responsive hai khu chọn bị xuống — 2026-11-24 (NV-24)

CSS breakpoint 3 cột hạ từ `1200px` xuống `900px`, cột co giãn đối xứng `1fr / 2.7fr / 1fr`, bỏ `min-width` nội dung cứng, `margin: 0` và `align-items: stretch` cả 3 khu để cùng hàng và cùng chiều cao. Giữa vẫn giữ role dọc, setup ở trên và inspector ở dưới. Build TS/Vite PASS; Edge 1 layout test qua 7 độ rộng (`900/1024/1100/1199/1366/1553/1920px`) và mobile `390px` không tràn ngang. Minh chứng: `reports/ui_sidebars_fit/{REPORT.md,browser.log,desktop.png,mobile.png}`. Chỉ chỉnh trình bày NV-24, không đổi khoa học/API/score/DB nên không train hay chạy lại Python test; không commit/push.

## Làm rõ hai khu nằm hai bên khung giữa — 2026-11-24 (NV-24)

User làm rõ bố cục desktop: Gợi ý ở cột trái | hai đội hình ở giữa | Chọn tay ở cột phải, cả 3 cùng hàng. CSS Grid `>= 1200px` đã đổi `grid-template-areas`, hai đội vẫn xếp role dọc, căn giữa; setup ở trên và inspector ở dưới. Màn nhỏ responsive giữ nguyên. Không đổi logic/API/score/DB/model; chỉ trình bày NV-24 nên không retrain hay chạy lại Python. TS/Vite build PASS, Edge centered-board test PASS (3 cột trái-giữa-phải, role dọc, inspector, mobile 390). Minh chứng: `reports/ui_flanking_choices/{REPORT.md,browser.log,desktop.png,mobile.png}`. Sổ mục 30 (NV-24) bổ sung mốc làm rõ; không commit/push.

## Căn giữa lại bảng tướng theo bố cục cũ — 2026-11-24 (NV-24)

Theo user chỉnh hướng: bỏ 5 pick cards nằm ngang mới thêm, giữ hai đội Blue/Red ở giữa (`max-width: 1000px`), mỗi đội 5 role hàng dọc với portrait `47px`. Setup trên đầu, gợi ý trái / manual phải, inspector dưới giữ nguyên; drag và auto-role không đổi. Chỉ CSS trình bày, không ảnh hưởng kiến thức khoa học/algorithm/DB/model/API nên không retrain hoặc chạy lại Python tests. TS/Vite build PASS, Edge centered-board test PASS (center, vertical, parallel choices, inspector below, mobile 390 no overflow). Minh chứng: `reports/ui_centered_board/{REPORT.md,browser.log,desktop.png,mobile.png}`; sổ mục 30/NV-24 bổ sung mốc mới. Không commit/push.

## UI gọn / kiểm kèo đã lộ / Renekton / First Selection — 2026-11-24 (MR-12 sửa, NV-24)

Đã hoàn tất yêu cầu: thiết lập trên đầu, gợi ý trái / chọn tay phải, inspector dưới; bảng đội hình gọn, native drag/drop đổi slot cùng đội (trống hoặc đã có tướng), từ chối cross-team và archive, có menu dự phòng bàn phím/chạm. Chọn tay không dùng dropdown role: dựa vào snapshot Pro `role_counts` giảm dần, bỏ slot bận, preview và API commit dùng cùng rule; tướng không rõ hoặc không còn slot đã quan sát sẽ báo lỗi, không tự bịa role. `draft_safety.py` và API trả `role_preferences`.

Tái hiện case Galio Top vs Ambessa ở turn 19 (pick 9 toàn trận, địch mới lộ 4 tướng): gate cũ chờ đủ 5 tướng địch nên bị lọt. `lane_review` kiểm trực tiếp role đang gán và yêu cầu review khi `n < 5` ngay cả khi địch chưa đủ 5; blind role không gán `n=0`. Contextual cùng role hoặc khi mọi role trống đều đã lộ đối thủ sẽ dùng cận dưới Wilson 95% trước base current score (vẫn giữ thứ tự ưu tiên wishlist / lớp đủ mẫu / pair guard ở trên). Cùng prefix: top cũ Galio → top mới Gnar, Renekton lên top 2; thứ tự mới: Gnar / Renekton / Camille / K'Sante / Galio. Raw score không đổi, GD không đưa vào feature, Rank không đưa vào score. Renekton `2/2` WR 100%, GD15 `+787`, Wilson `34.2%–100%`; Gnar `5/6`, GD15 `+686`, Wilson `43.6%–97.0%`; CI chồng lấn nên không tuyên bố vượt trội. Raw Renekton composition lift `0.718` giải thích vị trí cũ, không phải bằng chứng synergy cơ chế.

First Selection trên UI do người dùng cấu hình từng ván; CLI nhiều ván bắt buộc truyền danh sách đủ `n` phần tử, bỏ legacy alternating fallback. Hỗ trợ all-Blue hoặc all-Red cả 5 ván; không tuyên bố là luật chính thức của mọi giải. VERIFIED: 178 tests PASS, TS build PASS, 5 Edge workflow PASS (real prefix auto top Gnar, manual Galio Mid bận → Top, drag occupied/cross-team, reload/export/mobile 0 overflow). CLI all-Blue 5 ván đủ 100 actions / 50 unique picks / locks `0-10-20-30-40` (có test override); all-Red và all-Blue manual legal replay PASS. Chưa có bằng chứng chất lượng độc lập mới hay tăng tỷ lệ thắng. Minh chứng: `reports/ui_lane_revision/` và `bo5_blue_first`. Thêm fingerprint `lane_review`/`manual_role_policy`; phiên cũ có thể cần tạo Phiên mới. Pro DB SHA-256 `20e3d973...` không đổi; không train/Rank collector/commit/push. Sổ mục 30 (MR-12 sửa / NV-24), ADR-043, doc `docs/UI_COMPACT_VA_KIEM_KEO_DA_LO.md`.

## Giữ cặp bot / First Selection người dùng chọn — 2026-11-24 (MR-24/NV-23)

Tái hiện đúng case 10 lượt đầu: Blue Nautilus → Jayce, Red ban Jhin/Kai'Sa → Blue Yunara. Số mẫu cặp (`n=5/6/1`) được kiểm chứng, không nhận yếu/mạnh cơ chế từ mẫu ít. `pair_reservation.py` đếm số ban địch sau lượt hiện tại đến trước pick tiếp theo của mình, quét toàn bộ legal bot/sup (`n >= 5`, `effective_lift >= 1`), ưu tiên `secure_now` khi số đối tác dương `<= ban_budget`. Không đổi score current, có `priority_tier`/lý do/count/CI riêng; giữ wishlist, lớp đủ mẫu, lọc role và chọn tay. Guard bật cho contextual pick ở API/CLI, ban contextual v2 không đổi, không search/lookahead/model mới/nerf Red. Thiếu căn cứ cặp thì auto cần review hoặc test override, không giả synergy.

UI chọn Blue/Red First Selection mỗi ván, bỏ auto luân phiên, bắt buộc chọn trước khi Sang ván; giữ màu đội, cho phép lặp side. `first_side` điều khiển lịch ban/pick độc lập màu map; CLI thêm `--first-picks`, báo cáo ghi lịch từng ván (`user_configured`). Luật phiên do User cung cấp, không gán nguồn Fearless 2025 thành xác nhận luật First Selection mới.

VERIFIED: 170 tests PASS (11 mới), TS/Vite build PASS, 3 Edge workflow/mobile PASS. Cùng prefix: top cũ Jayce → guard chọn Jhin, score gốc chung không đổi, mirrored Red-first cho cùng gợi ý; chạy tiếp 20 lượt hợp lệ Nautilus–Jhin. CLI 5 ván `red,red,blue,blue,red` đủ 100 actions / 50 unique / locks `0-10-20-30-40`, `allow_statistical_auto` giữ nhãn. Đây là regression/legality, không phải bằng chứng accuracy chiến thuật độc lập, cặp tối ưu hay tăng thắng. Minh chứng: `reports/pair_reservation_revision/`. Pro DB SHA-256 `20e3d973...` không đổi, không retrain/Rank collector/commit/push. Sổ mục 29 (MR-24/NV-23), `docs/GIU_CAP_BOT_VA_FIRST_SELECTION.md`, ADR-042 đồng bộ.

## Hai khu UI và contextual v2 — 2026-11-24 (MR-13 sửa / NV-22)

User giao tách gợi ý và chọn tay thành 2 khu và cải thiện contextual. UI bỏ tab: hai panel đồng hiện với nút confirm riêng, input manual reset sau chuyển lượt; gợi ý/auto vẫn dùng current pick và contextual/legacy ban. `BanPlanner.pool_value` v2 = `sum(non-negative top 3) / 3` cố định, slot thiếu có utility 0; không impute 0 vào số đo thực tế. Sửa bất nhất mất backup mà tăng pool value ở `n < 3`; self-cost, access factor, weights, pick formula và luật giữ nguyên. Không lookahead/model mới/case-specific champion.

Đối chiếu ghép cặp 80 ban states thật trên WLDS 16.20 (40 val / 40 test series chronological, freeze history trước val, cùng pool). Số probe tăng ngược khi mất backup giảm từ `10+21 → 0`; top 1 đổi `1/7`, top 5 đổi `3/8`; Recall@5 vẫn `0.675 / 0.525` ở cả 2 bản. Chưa chứng minh tăng accuracy chiến thuật/counter/winrate; dữ liệu audit cũ không phải fresh final test. Minh chứng ở `reports/contextual_ui_revision/`. MR-13 là policy tự thiết kế đã có được sửa, không nhận fixed-capacity là bài Chương 6.

API chốt ngày UTC khi `as_of` trống, trả `snapshot_id` + `configuration` (Ban/Pick/version); hash Pro DB, scope, roster, teams, ngưỡng và version. Session/export ràng buộc mã, lệch trả `409`; Pro DB đổi trong cache đòi restart, không trộn điểm cũ với nguồn mới. Không lưu DB/code historical backup, không claim tái lập engine cũ chỉ từ hash. Browser khi xung đột vẫn export inputs và tạo phiên mới được. 159 unit tests PASS (5 mới), build PASS, 2 Edge workflows PASS. Pro DB hash không đổi, không train/commit/push. Sổ mục 28 (NV-22), ADR-041, docs BAN/UI đồng bộ.

## UI React + TypeScript local đã chạy — 2026-11-24 (NV-21)

Theo user đã chốt TypeScript và giao triển khai, thêm `web/` (React/TS/Vite, CSS thuần) và `src/api/app.py` (FastAPI adapter). Dùng lại `DraftState`/`DraftAdvisor`/`BanPlanner`; default pick `current`, ban `contextual`/`legacy`, không thêm thuật toán/model/lookahead. UI Pro draft có chọn tay/top 5, 20 lượt Ban/Pick đánh số, flex swap/undo, xem lịch sử, auto một ván và test override rõ, Fearless tối đa 5 ván, browser `localStorage` input và xuất JSON. Rank chỉ ở bảng nguồn riêng với n/WR/CI/GD-XP-CS 10/15, missing giữ thiếu. Candidate `n=1` hỗ trợ demo, evidence `n=5`, không gọi điểm là xác suất/counter thật.

Build/typecheck PASS; 154 Python tests PASS (8 API mới); browser Edge thật PASS một ván → ván 2 khóa 10, đổi đường/undo/archive/export/reload/mobile 390px, không `pageerror`. API test riêng validate đủ 5 ván chọn tay/khóa, không claim browser auto 5 ván. Canonical SQLite SHA `20e3d973...` không đổi, không retrain/commit/push. `start_ui.ps1` build và serve local `127.0.0.1:8000`; hướng dẫn `docs/UI_REACT_TYPESCRIPT.md`, minh chứng `reports/ui_demo/`. Sổ kiến thức mục 27 (NV-21): UI/API là kỹ thuật ngoài môn, engine MH/MR cũ giữ nguyên mapping. Rank recommender riêng / đồng bộ nhiều máy / global BO5 chưa triển khai, không là điều kiện UI này. Cache advisor cần restart khi đổi nguồn; DB/key không đưa ra static frontend.

## Đã rà 8 thành phần, thử simple và chạy BO5 — 2026-11-24

User giao 4 phần: review, so sánh, BO5 và truy vết. `AdvisorPolicy.scoring` default `current` giữ nguyên; explicit `simple` gọi `_simple_rows` tính trung bình frequency (`Pick/raw_max`), cosine (nếu có) và WR đối đầu cùng role; thiếu matchup `n >= 5` dùng historical WR fallback có nhãn, thiếu cosine thì bỏ tín hiệu. Bỏ khỏi điểm `simple` các bonus draft order, historical riêng, synergy, composition lift/geometric-odds, mastery riêng; giữ pool, luật, flex và giải thích Pro/Rank. Đây là điểm pick đơn giản, không đơn giản hóa công thức ban hoặc xóa toàn bộ MR khỏi execution. Default `current` không đổi.

`compare_pick_scoring.py` dùng cùng frozen history, role candidate pool và actual draft states (WLDS 16.20, series 60-20-20, 200 val / 320 test × 3 chế độ `current`/`simple`/`recent_presence`; có pool hash mỗi query). Test Recall@5: `current 0.49375` → `simple 0.425`, MRR `0.3026` → `0.2334`, coverage cùng `0.76875`; delta `-0.06875`, CI `[-0.11034, -0.03235]` theo 10 series. `simple` giảm truy hồi nên không promote. Dữ liệu từng dùng audit nên là development comparison, không phải fresh independent final test hay bằng chứng chất lượng counter. `component_audit.csv` có 8 ablation sensitivity, không tune để chọn bản thắng test.

BO5 T1–Gen.G đã đủ 5 draft / 100 actions / 50 unique picks (contextual ban / simple pick, as-of 24/11, patch 16.20, data 14/11). 44/50 pick thiếu matchup đủ mẫu nên fallback WR, 5 sparse candidate; `allow_statistical_auto` giữ nhãn. `reports/simple_scoring_bo5/` có 100 lượt Ban 1..5 / Pick 1..5, lý do, điểm, missing, JSON 5 game và series. Không giả tỉ số/winner. Simulator lưu thêm `matchup_scope` và `source_comparison` để không mất giải thích qua JSON.

VERIFIED: 146 unit tests (7 mới) + integration 520 paired queries / 1,560 records / identical pool hash / split disjoint / freeze / mean reconstruction 50 picks / Fearless legality / DB hash unchanged PASS. Outputs: `reports/pick_scoring_comparison/` và `reports/simple_scoring_bo5/`; doc `docs/TINH_GIAN_DIEM_RECOMMENDER.md`, sổ mục 26 (MR-23/NV-20). Không train/commit/push, không đổi Rank collector hoặc Pro DB.

## Phạm vi vừa sức môn học, không quota mẫu — 2026-11-24

Theo yêu cầu mới, ưu tiên Chương 1–6 và một số mở rộng giải thích được. Rà soát toàn bộ nhóm module, dòng chảy dữ liệu và mapping môn học, kết quả ở `docs/PHAM_VI_DO_AN_VUA_SUC.md`: giữ dữ liệu/SQL-Pandas/EDA/ML hiện có/content-based và demo legacy-contextual-Fearless; prototype/search/global BO5/transfer research/quy mô hạ tầng U.GG là phần phụ, không bắt buộc phát triển. Đã cập nhật `AI_RULES`, `KNOWLEDGE_RULES` và constitution `1.2.0` (Web/API đầy đủ không còn bắt buộc). Chưa thay công thức xếp hạng 8 thành phần hoặc xóa file có phụ thuộc; không nhận gộp MR thành MH để làm đẹp phạm vi.

Đã bỏ default 2,000 kèo: `target=None`, `remaining=None`, `reached=None`, report schema v3 có `ugg_reference_status=not_loaded`, `parity=False`. CLI giữ target explicit chỉ để tái lập cũ, không có quota mặc định. 139 full tests PASS, 70 rank tests + integration PASS: 418 complete games / 4,180 rows / 1,626 người / 2,806 pooled pairs, 408 qualification rebuild / 2,364 bulk membership raw checks; DB integrity/FK/mirror/dedup/privacy/Pro hash không đổi. Pro tables export lại với target null, 3,000 games / 3,098 pairs / `n>=5: 1,170` và 6 metric `n` không đổi. Sổ mục 25 (NV-19); không MR mới, không retrain/commit/push.

Collector cũ PID 23100 / worker 15128 đã được xác minh và nạp lại cấu hình, dữ liệu/checkpoint giữ nguyên; phiên cũ đã tự kết thúc `session_time_limit` trước khi stop nên không sửa journal giả. Watch mới PID 29828 / worker 7992, start 08:05:27 UTC (15:05 VN) 24/11, không tham số 2,000. Manifest `reports/rank_matchups_live/collector_process.json` có PID family, log và `stop_command`; logs `collector_watch_no_quota.log` và `_errors.log`. Số 418 là mốc nghiệm thu trước watch mới, summary tiếp tục tăng. Chưa tải được U.GG matchup (lần thử trước 403), không claim ngang số mẫu hay chất lượng.

## Bằng chứng Pro/Rank trong gợi ý và contextual thử nghiệm — 2026-11-24

Đã thêm matchup_evidence.py: Pro ghép đúng game/role khác side từ luồng sạch, signed GD/XPD/CSD10/15, Wilson/tCI và n riêng; export reports/pro_matchups có3.000trận/30.000rows/3.098pooledpairs/1.170n5. Mỗi metric phút10 có24.370 phép đo, phút15 có24.380; missing giữ thiếu, không suy từ tổng đội. Official catalog16.20.1 chuẩn tên/ID; khôngsửaSQLite. DraftAdvisor thêm matchup_source_comparison sau khi xếp điểm; simulator gợi ý/why hiển thị Pro và Rank riêng, p(role) khi flex, n/WR/CI/tài nguyên/nguồn, thiếu/trái chiều và bất định. ReadonlyRank transaction/available_at=maxqualification,ingestion, snapshot cố định mỗi advisor; Pro đúng cửa sổ/region/as_of. Không đổi score/order/banstrategy/weights, cótest bất biến.

evaluate_contextual_evidence.py freeze261trận Rank lúc07:36:57UTC24/11; controlPro/Rank-only-component/hybrid50-50same-role dùng cùngpool và history, chỉ đổi matchup. Diagnostic30val/30test ×3:Recall5=.6000/.5333,MRR5=.313889/.315 bằng nhau; hybrid0top5đổi, rank-only1testtop5đổi. CófutureRank so trậnPro cũ và Prodata từngaudit nên không độc lập/không promote. Prospective readiness0series/readyFalse/resultNull: Pro mới nhất14/11 trướcfreeze24/11. Hỗ trợ --freeze, protocol5validation+5testseries saufreeze, khôngoverlap; chưa prospective_queries.json. MainintegrationFalse, promotionFalse; không tự bật tín hiệu Rank choPro.

VERIFIED138tests (12mới) + integrationstored6diff/mirror/10roles/console/privacy/hash/scoreinvariance PASS. Artifacts reports/pro_rank_explanations/{REPORT.md,recommendations.json,checks.json,console_example.log,tests.log} và reports/contextual_rank_experiment/{REPORT.md,evaluation.json,diagnostic_queries.json,prospective_readiness.json}; rawfreeze private data/raw/contextual_evidence_experiments. Doc PRO_RANK_MATCHUP_EVIDENCE, sổ24/MR-22/NV-18. CollectorRank nền trướcđó tiếp tục độc lập; không retrain/commit/push. Đã hoàn tất code/thống kê/giải thích/thăm dò; kiểm chứng nângchấtlượng độc lập còn chờ dữ liệu giải saufreeze, không đánh dấu đã chứng minh.

## Bảng gộp theo hướng U.GG và thu nhiều server — 2026-11-24

Mốc kiểm chứng cuối trướcwatch:150completegames/1.500rows/725người,1.248scopedpairs và1.170pooledpairs,0đạt2.000;14scopedpairs n>=5.69tests/integrity/FK/dedup/mirror/privacy/140qualificationrebuild/389bulkmembershiprawchecks/canonicalDBhashPASS ởchecks.json. Thêm62trận so88 cũ qua3phiên153/80/101requests. Khởi chạywatch nền thật lúc2026-11-24T07:17:06Z (14:17VN), PID23100, consolelogcollector_watch.log/errorslog vàcollector_process.json; đãkiểmprocess sốngsaukhởichạy, khôngcamkếtvĩnhviễn. Summarysẽtăngqua checkpoint, khôngcoi150làtrầntổng. Dừng `Stop-Process -Id 23100` saukhi xácnhậnđúngprocess. Khôngservice/autostart.

Đã thêm pooled_all/best/unfavorable/early CSV, matchup_collection_progress mục tiêu2.000 trận/kèo (không cap/chứng nhậncounter), giữ bảng táchpatch và nguồn gộp/dấuGD15. Report schema v2, SQLitev1 khôngđổi. Round-robin KR/EUW/NA cócursor bền vững. Bootstrap lưu rawLeague-v4lists vàbatchsnapshot từmembership mỗiPUUID, refresh15min, cachetimestamp>=matchend/TTL15min; thiếu/cũ/newerend gọiindividual, all10Master+/24h/spread15min vẫn giữ. Đã thu đủ observations từcả3server thật, khôngphảichỉseed. Số liệu hiện hành xem reports/rank_matchups_live/summary.json; checks.json là mốc kiểmchứng cófingerprint, khônglàlivecounter.

69unit tests đãPASS; doc docs/POOLED_MATCHUPS_UGG_STYLE.md, sổmục23/MR-21/NV-17. Phiênthu hữu hạn và backgroundwatch được ghi riêng: sessions/*.json cho lịch sử, collector_process.json ghi PID/thờigian/log khi khởi chạy nền, cần kiểmprocess để biết cònsống; khôngcàiservice/autostart. DừngCtrl+C nếu chạyconsole hoặcStop-Process đúngPID nếu nền; checkpoint giữtiếnđộ. Số88trận/mốc63tests bên dưới là lịch sử trướcđợtnày. Chưa2.000/kèo, khôngclaimcounter bấtbiến, khôngpoolRank/ProhoặcbậtProsignal/retrain.

## Kho Rank tăng dần đã chạy và cập nhật dữ liệu — 2026-11-24

Theo yêu cầu mới không giới hạn tổng1.000trận: đã thêm rank_lake.py/update_rank_evidence.py/rank_matchup_tables.py. NewprivateSQLite data/database/ranked_evidence.db với persistentseed/jobs/snapshots/observations/sessions, import10accepted cũ, bootstrap C/GM/M vàbfsobservedMaster+, chỉrecent24h/all10Master+/spread15min. Resume checkpointgiữqualificationkhibịngắttimeline, cache15mingiữobserved_atgốc, rate/budget/sessiondeadline, writerlock; ProDB khôngđổi. Tableswinrate/GD15/XP/CS10–15xuấtngay vàcheckpoint, sparsegiữrõ, khôngchờ1.000mới cậpnhật.

VERIFIED:63unit tests vàintegrationPASS. Livephiên20261124T063723199769Z dùng600request, phiêntiếp20261124T065152611238Z dùng2request hoànthành timelinecòndangdở với0snapshotmới. Khohiện88completegames(78mới+10cũ),880rows/382người,714directedpairs/8đạtn5,11.012seed,5pending/7rejected. DBintegrity/FK/78newqualification/mirror/10roles/privateexports/idempotentimport vàcanonicalDBhashPASS. Bảng ởreports/rank_matchups_live/{REPORT.md,summary.json,all_matchups.csv,best_full_game_matchups.csv,unfavorable_full_game_matchups.csv,early_gold_advantages.csv,observations.csv,checks.json,tests.log,sessions/...}; rawdata/raw/rank_lake vàprivateSQLite thật. Hướngdẫn docs/CONTINUOUS_RANK_EVIDENCE.md; sổmục22/MR-20/NV-16. Hai phiênfiniteđãkếtthúc; --watch chochạynhiềuphiênkhôngtrầntổngnhưngkhôngserviceẩn. Không nhận tươngđươngU.GGquality; runtimeRank/Prosignal/model/canonicalDB khôngđổi.

## Campaign Rank và coverage/readiness — 2026-11-24

Đã chạy3đợt mới từ15seed khác nhau,15candidateIDmới,179/200HTTPattempt (bao gồm retry), giữ Master+/24h/15min. Thêm8accepted/7loại vì tuổi trận/0missing; gộp runđầu là10accepted/100dòng/72người khác nhau. collect_rank_batches.py dùng seed slices/registry và bỏID đãnhận/loại, giữ snapshotmới mỗi run. RiotClient có budget thật kiểmtrướcmỗiattempt; hết/lỗi terminal lưu partial và dừng batch sau.

VERIFIED: rank_coverage.py revalidate raw/snapshots, khửtrùngaccepted sớmnhất, tách server/queue/patch/floor, đếm n/người/deficit và0evidenceuniverse chỉ từ tên candidate.115champion-role/2.156pair cóhướng,0đạt n5/3người; maxn tướng top2/jng3/mid3/bot4/sup4. Accepted đềuKR16.23,16.22chỉmetadata0accepted. Kế hoạch6/2/2 nhưng0history cósnapshot/detail sẵntrướcvalidationstart, readinessFalse/metricsNull. Theođiềukiện “khi đủ mẫu”, chưa xây recommender Rank hoặc giảmetric/baseline/UI. Protocol đãghi, cầndataởthờiđiểmsau.

49testsPASS + integrationbudget/seeds/IDs/counts/source/privacy/timecutoff/DBrawbấtbiến. Artifacts reports/rank_coverage/: REPORT.md, summary.json, readiness.json, checks.json, games.csv, observations.csv, patch_coverage.csv, role_coverage.csv, champion_role_coverage.csv, lane_matchup_coverage.csv, tests.log. Campaign reports/rank_snapshot_collection/campaigns/20261124T060507936864Z.json, raw3runmới giữprivate. Docs/RANK_BATCHES_COVERAGE_AND_EVALUATION.md, sổmục21/MR-19/NV-15. Giải/legacy/contextual/model/SQLite không đổi, khôngtrain/historicaltierclaim. 4run làcùngngày, không4periodđộclập.

## Collector snapshot rank đủ10người — 2026-11-24

Đã hiện thực collect_rank_snapshots.py, chụp League-v4 Solo/Duo từng participant, raw/private evidence riêng mỗi run, cache cùng người trong run; báo nhận/loại/thiếu và timestamp/age/spread. Configv2 có defaults maxage24giờ/spread15phút, floorMaster+ chỉnh được; chỉ là snapshot-proxy, không historicalrank. RiotError thêm status_code để terminal stop/404missing đúng nghĩa, không in token. Không dùng seed để giảtier cả10người.

VERIFIED LIVE: run20261124T055630861038Z,5seedKR/5trận,65call cấpclient/49participant khác nhau,đủ50lượt participant/49snapshots do1lặp. Cả5all10Master+ tại lúc kiểmtra;2accepted gần trận,3rejected chỉvìquá24giờ,0missing.20acceptedobservations đủgold/XP/CS10/15 thực.40testsPASS + offline rebuild API/records/classification/mirrors/privacy và DB/raw không đổi; historical gate vẫn0eligible khi đưa snapshot vào. Không rankthấp hay historicalclaim. Outputs reports/rank_snapshot_collection/20261124T055630861038Z vàlatest.json, raw data/raw/riot_rank_snapshots; docs/COLLECTOR_RANK_SNAPSHOTS.md, sổ mục20/MR-18/NV-14. RuntimeRank/Pro signal/model/DB không thay, không train/benchmarkmới.

## Hai chế độ Rank/Giải và tiêu chuẩn Rank cao — 2026-11-24

Đã chốt thiết kế hai chế độ, cấu hình src/config/draft_modes.json và audit rank_eligibility.py; chưa triển khai runtime/CLI/giao diện chơi Rank. Rank phân tầng tier/queue/server/patch; Giải dùng Pro chính, Rank cao bổ sung có điều kiện. Master+ là ngưỡng làm việc chỉnh được, chưa tối ưu. Cổng dữ liệu Giải nghiêm ngặt: cả10người có bằng chứng interval lịch sử đạt ngưỡng đúngqueue/server/bao phủ lúc trận, nguồn và observed_at<=cutoff. Seed Thách Đấu hoặc snapshot hiện tại không được hồi tố thành lịch sử; tool kiểm hợp đồng chứ chưa xác thực độc lập nguồn interval.

VERIFIED:92trận đều challenger_seed_only,0đủ bằng chứng lịch sử cả10người, không có nghĩa92trận rank thấp.29testsPASS (10mới); default evaluate_rank_transfer audit đúng freeze và dừng exit2 nếu thiếu dữ liệu đạt chuẩn, metric JSON mốc18 không đổi. Cờ --allow-seed-only-research chỉ tái lập cohort nghiên cứu cũ, không bật hybrid/high-elo claim. Output reports/rank_cohort_audit/ (REPORT/summary/matches/checks/tests.log); docs/HAI_CHE_DO_VA_TIEU_CHUAN_RANK_CAO.md, sổ mục19/MR-17/NV-13. DB/raw/model và runtime draft không đổi, không train. Mốc18 bổ sung chú thích cohort, không thay metric. Collector snapshot cá nhân và runtime Rank còn kế hoạch; không có đầu ra runtime Rank mới.

## Thử nghiệm nguồn đối đầu Rank/Pro — 2026-11-24

Đã làm chuẩn hóa chính thức Data Dragon16.20.1 và thu92trận lịch sử KR từ20seed (96ID trả về,411participant, không xuất định danh);83trận đúngpatch16.20,9trận16.19. Giữ riêng cache/output mới, không ghi đè smoke5trận16.23. CS Pro total=minions+monsters trên30.000dòng và các signed diff10/15 khi đủ phép đo không mismatch; ghi rõ frame Rank lệch104–407ms, role sau trận không xác nhận lane occupancy. Catalog ID/alias giải quyết18tên nội bộ khác tên hiển thị, không fuzzy/ngoại lệ.

VERIFIED EXPLORATORY:19unit tests + integration checks; chia series thời gian27/9/10 (46/20/32trận), freeze trước26/10 18:03:09UTC, chỉ dùng trận đã kết thúc/đúngpatch/KR/trước cutoff. Replay200validation/320testquery ×3mode chỉ đổi nguồn matchup, cùng pool/điểm khác. Test cả3Recall5=.49375/MRR5=.302604; Rank chỉ đủ hỗ trợ13/320query, chưa thấy cải thiện. Hybrid giữ Pro khi Rank thiếu n5;50/50 residual khi đủ. CIbootstrap deltaRecall5[0,0] do hit/miss giống nhau, không bằng chứng tương đương tổng thể. Dữ liệu Worlds đã dùng trong audit trước nên không gọi final test độc lập mới; integration_enabled=false, không đổi contextual runtime.

Outputs `reports/rank_transfer_evaluation/` (REPORT/evaluation/contract/names/splits/validation-testqueries/checks), `reports/rank_pro_study_data/` (CSV/summary). Modules rank_data_contract.py/evaluate_rank_transfer.py và collector v2 ended_at/date range/per-seed/interval1.3s; docs/RANK_TRANSFER_PROTOCOL.md, sổ mục18/MR-16/NV-12. Legacy/contextual/ban/model/SQLite không sửa, không fit ML. Cần coverage và tập giải mới độc lập trước khi cân nhắc tích hợp; không tune threshold/weight để ép metric.

## Đối đầu Rank riêng với Pro — 2026-11-24

Đã thêm `src/01_data_pipeline/ranked_matchups.py`: thu thập Riot có retry hữu hạn/cache/provenance riêng, strict role, gameStartTimestamp/patch thật; xuất signed gold/XP/CS10/15 và n/mean/SD/team-result winrate/Wilson. `before` mặc định không sau mốc và lệch tối đa1000ms; `nearest` ±1000ms chỉ mô tả, lưu timestamp thật, không đưa vào dự báo đúng mốc. Không dùng phút9 thay10 hoặc giả lập dữ liệu đường.

VERIFIED: tải thật5trận KR queue420 ngày22/11/2026 UTC, patch16.23,50dòng; nearest đủ6phép đo, before để missing đúng vì frame sau mốc128–254ms. Seed chỉ1người hiện tại, không chứng minh rank lịch sử cả10người hoặc mẫu đại diện high elo. Worlds local206trận/2060dòng từ2025–2026 trên4patch15.17/15.20/16.17/16.20,1940dòng đủ từng phép đo. Không có patch chung nên bảng ghép0dòng.10unit tests + integration signed mirror/timestamp/missing/cutoff/DB hash PASS;110link sổ PASS.

Artifacts `reports/rank_pro_matchups/`: REPORT.md, summary.json, checks.json, tests.log và5CSV observations/aggregate/comparison. Cache `data/raw/riot_matchups/` gitignored; CSV không PUUID/playername. Hướng dẫn `docs/RIOT_RANK_MATCHUPS.md`, sổ mục17/MR-15/NV-11. Legacy/contextual/model/DB không đổi; chưa benchmark Pro-only/Rank-only/hybrid, chuẩn hóa hết alias, phân tầng rank hoặc kiểm chứng chuyển miền. Không train/khôi phục lookahead.

## Rà soát50pick contextual, chưa sửa điểm chọn — 2026-11-24

VERIFIED AUDIT: user đã đồng ý bước1 trước, nên chỉ tái dựng50state của5draftcontextual và so248alternativecùngrole hợp lệ; khôngthêmsearch/flexhoặcsửapolicy. audit_draft_choices.py bổsungcompositionevidence/playerhistory/slot/sourcehash/scoregap vàdiagnosticablation; review_contextual_picks.py kiểmtra state/pool/score vàxuấtREVIEW/summary. 50score/top1táilậpkhớpphiênđãlưu, đây khônglàqualitylabel. 38/50pickcóđịchlộnhưngthiếumẫuđốidầu;5blind;7cóítmẫuđủngưỡng.3candidateítmẫuván5:Poppy2,Aurora2,Nasus1.100cặpphốihợp:8đủmẫu,59ítmẫu,32chưathấy,1thiếuanchor. Ablationbỏmetađổitop1ở13lượt,composition14,content1,mastery3,matchup3; khôngsuytướngthaythếtốthơnhoặcđếmsốpicksaibằngtổngnày.

Artifacts reports/contextual_pick_audit.json/md, reports/contextual_pick_review/REVIEW.md vàsummary.json. Sourcehash/state/248legalalternatives/savedscorechecksPASS, khôngthayđổiquyếtđịnhđãlưu/model/DB/train. PhươngphápkiểmđộnhạyMRmớighiởsổmục16; nềnChương1/5x, phầnablationngoàimônvớipolicychẩnđoántựthiếtkế. Phạmvihiệnhànhvẫnlegacy/contextual; bướcflex/đa-serieschưalàmtronglượtnày.

## Hiện hành: chỉ legacy và contextual — 2026-11-24

Theo yêu cầu người dùng, đã BỎ lookahead khỏi mã ban và CLI; không chỉ ẩn menu. BanPlanner chỉ còn one-stepcontextual, ContextualBanPolicy(top3pool/owncost). Gỡ response_distribution/evaluate_root/rollout/leaf/predictor dependency và --ban-response-model; --ban-strategy chỉ legacy|contextual, legacygiữmặcđịnh. Contextual dùng pool_impact/contextual_trace, không xuất search_trace/branches/sensitivity. OpponentModelcũ giữ độc lập, không được contextual dùng đểban; không mởrộngchứcnăngkhác.

VERIFIED:57testsPASS;2seriesT1–Gen.GWorldscutoff13/11patchdataset16.20đều5draft/100actions/50uniquePicks,locks0/10/20/30/40, testtop1override. Pick/ban của cảlegacy/contextual giống phiêntrước (đã so cả100lượtmỗiseries); CLIonegame vàseries từchốilookahead(exit2), helpkhôngcònban-response-model. Newoutputs khôngsearchfields. Báocáohiệnhành reports/legacy_contextual_comparison/{COMPARISON.md,comparison.json,checks.json,legacy/,contextual/}; doc docs/BAN_LEGACY_VA_CONTEXTUAL.md. Khôngtrainmodel/đổiDB/raw. Tài liệu vàreportlookaheadcũđánh dấuLỊCHSỬ, khôngxóa artifact/minhchứng; cácmốcbêndướilàlịch sử trướcquyếtđịnhnày.

## Bản chạy contextual riêng T1–Gen.G — 2026-11-24

VERIFIED RUN ONLY: đã chạy contextual riêng theo yêu cầu, xuất reports/t1_geng_contextual_20261124/{QUICK_VIEW.md,REPORT.md,series.json,game_1..5.json/log,checks.json}. Worlds cutoff13/11 patchdataset16.20, T1Blue/Gen.GRed,first-pickluânphiên, test chọn số1thiếutincậy.5draft/100actions/50uniquePicks,locks0/10/20/30/40; validate_game vàBan1–5/Pick1–5PASS.38pickreview_required giữnhãn. Không kiến thức/phương pháp mới, không đổi code/model/DB hoặctrain; MR-13/NV-08 vẫn áp dụng. Không gọi đây là tối ưu hoặc có tỉ số thắng/thua.

## Hoàn tất3mục ban ngữ cảnh, rollout phản ứng và đối chiếu5draft — 2026-11-24

VERIFIED: ban_planner.py/BanPlanner có contextual pool loss địch trừ self-denial theo thứ tựpick thật/roster/Fearless; lookahead shortlist6ban,2response ởfirstopponentturn rồigreedyđến3pick mới/max12plies. OpponentModelđãcó dùng inference, khôngfitmới; fallbacksoftmaxcónhãn. Không épdiversity, khôngcasechampion/team. Mặc địnhlegacy đểtáilập; bật --ban-strategy contextual|lookahead, --ban-response-model PATH. Trace lưu mọiroot/branch/leaf/coverage/omittedmass và sensitivitybounds (khôngCIthốngkê), why/REPORTgiảithích theo lượt.

57testsPASS; so3seriesT1–Gen.GWorlds cùngcutoff13/11patchdataset16.20/rosters/lịchfirstpick, testoverrideTrue theoủyquyền. Mỗi5draft100actions50uniquePicks, khóa0/10/20/30/40; 583branchpaths/295rootreplay hợp lệ, sâu tốiđa9<12. Tập6ban đầu:legacy1tập lặp5ván, contextual5,lookahead5; Jaccard1/.471/.145, khôngclaimđadạng=tốthơn. Lookahead~.471s/banmean,p95.787s,max1.371s trênlầnchạy;cócache. 23/50ban kháccontexttop1. Giữ2response chỉphủmean21.1%khốihỗtrợ,min5.8%;48/50sensitivityboundsoverlap. 41/50pickvẫnthiếucontextđủmẫu. Chưaindependentbanqualitybenchmark/counterevaluator/fullflex hoặcfullBO5plannerđểdànhtướng.

Artifacts: reports/ban_strategy_comparison/COMPARISON.md,comparison.json,checks.json và{legacy,contextual,lookahead}/{QUICK_VIEW.md,REPORT.md,series.json,game_1..5.json/log}. Sổkiếnthứcmục14/MR-13/KH-02 cậpnhật; docs/BAN_NGU_CANH_VA_LOOKAHEAD.md. KhôngđổiDB/schema/raw, khôngtrainmodel, khôngcommit/push. Trạngtháidừngtrướcđượcusergiaotiếprõ3mục; phạmvihoànthànhtạibảnrolloutgiớihạnnày.

## Test đủ5draft T1–Gen.G theo yêu cầu — 2026-11-24

VERIFIED: thêm --allow-statistical-auto cho series, defaultFalse không đổi. User yêu cầu test thiếu tin cậy vẫn chọn số1; toàn bộ5ván chạyTrue, không manualreviewstop nhưng vẫn giữreview_required/counterstatus/coverage. Worlds cutoff13/11 patchdataset16.20.100actions/50uniquePicks, locks0/10/20/30/40 vàvalidate_gamePASS; 38pick thiếu đối đầu đủ mẫu có nhãn. Report dùng đúng tên2đội vàBan1..5/Pick1..5mỗiđội kèmturn1..20. reports/t1_geng_bo5_test_20261124/REPORT.md,QUICK_VIEW.md,series.json,checks.json. Khôngtạo tỉsố hoặc chứngminhcounter/tốiưu. Khôngfitmodel/đổiDB hoặcphươngphápthốngkê. Lượt này chỉ mởtestoverride trongdriver vàđánh sốreport; khôngtiếptụcsearch/planner.

## Chạy lại BO5 T1–Gen.G — 2026-11-24

VERIFIED RUN ONLY: Worlds as-of2026-11-13 patchdataset16.20, 5draft được yêu cầu, mặc địnhtactical-reviewgate, khôngopponentmodel/override. Ván1hoàn thành20actions; ván2dừngtrước20(chỉ19actions) trướcCamille topT1, alternativesRenekton/Jax/Ornnđềucoverage0; ván3–5chưa chạy.39actions/19uniquePicks, khóa0rồi10, khônglặp hoặc dùngtướngbịkhóa. Reports:t1_geng_bo5_20261124/REPORT.md,series.json,game_1/2.json,checks.json.

Giới hạn xác nhận: Trundle vẫn được chọn ởván2trước khiđịch đủ5, coverage0; gatechỉkiểmtrađịchđủ5khônggiảiquyếthếtchấtlượngcounter/cáclựachọnkhác. Không đượcgọiBO5hoànthành hoặcfixcountertoàndiện. Lượtchỉchạyvàghiartifact, khôngđổiphươngpháp/code/model/DB, khôngretrain hoặc chạyregressionsuitekhôngliênquan. Userchỉyêucầuchạythử, khôngtựmởrộngfix/search/planner.

## Hoàn tất phạm vi Trundle/các lựa chọn tương tự, dừng phát triển tiếp — 2026-11-24

VERIFIED: enemy_evidence/evaluate_enemy_context xét mọi role địch, giữ n/CI/coverage và trạng thái mechanical_counter:not_evaluated. Audit50pick đúng state vàtop5, không blacklist tên. Actual Trundle ván2lượt20 vẫn topheuristic nhưng coverage0cũng như alternatives; không có căn cứ xác nhận counter/tướng thay thế tối ưu. Mặc định auto khi địch đủ5và pick thiếu mọi đối đầu đủ mẫu sẽ dừng trướcapply, lưu manual_review/completefalse vàCLIexit3; chọn tay được phép, demoonegame có --allow-statistical-auto rõ nghĩa. Exactcase giữ19actions/jungletrống; CLI casePantheon cũng dừng19actions. 51testsPASS, checks reports/tactical_review_checks.json; docs/RA_SOAT_LUA_CHON_THEO_DOI_HINH.md và sổ kiến thức mục11. Seriesdriver dừng khi cầnreview; các5draft trước đó là lịch sử trướcgate, không được gọicounterđãxác nhận.

Theo chỉ đạo mới, DỪNG sau khi hoàn tất phạm vi trên. Trước chỉ đạo dừng đã dựng4120draftstate/206ván/93seriesWorlds và fit OpponentModel CUDA, validation/time-series split train142/val22/holdout42ván; 840query phát triển R5=.3917 so slot=.2202. Cácmodel/dataset/forecastartifact được giữ, đã ghi sổ; không tiếp tục phát triển hoặc retrain sau thu hẹp phạm vi. Predictor mô phỏng hành vi, không là evaluator cơ chế hoặc planner. Opponent/search/BO5 và nguồn cơ chế patch-specific còn backlog. Không sửa rawDB/schema, không commit/push.

## Quy định cập nhật kiến thức bắt buộc trong SpecKit/agent — 2026-11-23

VERIFIED CONFIGURATION: AI/KNOWLEDGE_RULES.md quy định mọi thay đổi kiến thức/phương pháp/chức năng/output phải cập nhật docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md trong cùng đợt: ID, MH/UD/MR/NV, chương/nguồn, hàm/module, công dụng/giả định, artifact/tái lập, trạng thái/minh chứng/giới hạn. No-impact có lý do; không tạo lý thuyết giả hoặc retrain model không đổi. Root AGENTS.md/GEMINI.md và AI/AI_RULES dẫn quy định; constitution thêmVI, version1.1.0. PrincipleV được làm rõ kiểm chứng theo tác động, không ép sửa tài liệu phải tái tạo.pkl.

SpecKit dùng4project overrides spec/plan/tasks/checklist với mapping và task cập nhật kiến thức bắt buộc; analyze giữread-only, checklist giữreviewownership. Đã kiểm tra actual Resolve-TemplateContent chọn đúng4override;70link sổ kiến thức PASS. Checker bền vững: .specify/scripts/powershell/check-knowledge-templates.ps1. Core templates,9Gemini commandprompts và manifest cài đặt giữ nguyên; không ghi policy vào installation metadata. Đây là policy/template enforcement qua agent và review, chưa là CI bảo đảm tự động mọi thay đổi. Không sửa code thuật toán/model/DB; không train hoặc chạy lại suite ML không liên quan.

## Tổng hợp kiến thức và mục tiêu mở rộng BO5 — 2026-11-23

VERIFIED DOCUMENTATION: docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md là file tổng hợp dùng viết báo cáo: MH-01..14 đối chiếu Chương1..6/5x với hàm, chức năng và đầu ra; MR-01..11 ghi rõ các kỹ thuật ngoài nội dung cụ thể của slide; NV-01..05 ghi nghiệp vụ/Fearless/CLI; KH-01..06 ghi mục tiêu opponent modeling/search/để dành tướng/planner BO5 và đầu ra DỰ KIẾN. Giữ hướng người dùng yêu cầu: vận dụng môn học có mở rộng, có tính trước phản ứng và tối ưu phân bổ tướng cả series. Không ghi planner/opponent model như chức năng đã hiện thực: driver hiện tại vẫn greedy từng lượt.

Đã đối chiếu source, slide text, manifests và artifacts; 65liên kết nội bộ PASS, không link hỏng. Ghi rõ XGBoost CUDA là luồng fit hiện hành; RF/boosting/PCA/K-Means có nền trong bài nhưng import không chứng minh đãfit. Số liệu hiện hành lấy manifest/reports, không trộn mốc cũ. Đây là lượt tài liệu, không đổi thuật toán, DB/model/raw hoặc chạy lại training/benchmark.

## Hiện hành — 5 ván Fearless Worlds (2026-11-23)

VERIFIED: simulate_fearless_series.py chạy đủ5ván Gen.G–Bilibili Gaming, snapshotWLDS as-of2026-11-13 patch dataset16.20 (106ván/94ván patch), cố định Gen.G Blue/BLG Red và luân phiên first-pick B/R/B/R/B theo lịch demo. Không mô phỏng thắng/thua hoặc ép tỉ số2-2; đây là5draft liên tiếp. Fearless khóa mọi tướng PICK trước đó cho cả hai đội, không carry standard bans, không reset ván5. Validator kiểm tra20lượt/5role/5ban mỗi đội và pool dùng trước; 100actions,50uniquePicks, locks[0,10,20,30,40],38testsPASS. Lưu toàn bộ100lượt và căn cứ ở reports/worlds_fearless_bo5/REPORT.md, series.json và game_1..5.json/log.

Pilot min5 dừng ván5 vì pool support không đủ. Tách candidate_min_games khỏi min_games(evidence): series cho ứng viên từ1lần quan sát, giữ evidence5; luôn ưu tiên lớp>=5 trước lớp ít mẫu trong các role đang mở. Chỉ có Yuumi ván5 là sparse_candidate (4trận). Không invent role/tướng hoặc tự giảm ngưỡng tin cậy. Positive log-lift shrink theo weighted_pair/(weighted_pair+10), negative theo weighted_anchor/(weighted_anchor+10), trước geometric aggregation, để chặn bonus lớn từ cặp một-mẫu. Policy có công khai, chưa tối ưu cả series. Default one-game vẫn candidate/evidence5. CLI evaluate WLDS cập nhật audit: Recall@5=.36, Recall@1=.095,MRR5=.184, CI mô tả vsrecent[+.015,+.102625]; benchmark là phát triển nhỏ, chưa đánh giá fullFearless hoặc tăng thắng. Những số liệu36%/MRR.21225 bên dưới thuộc phiên trước shrink bổ sung.

Không đổi DB/schema/raw, tải dữ liệu mới, fit ML hoặc commit/push.

## Hiện hành — phối hợp mọi cặp role, chạy Worlds (2026-11-23)

VERIFIED: DraftMetaSnapshot thống kê đủ 10 cặp role (20 chiều) trên gameid+side, giữ role của cả hai tướng, counts/Wilson cho tần suất ghép cặp và riêng kết quả cả trận. DraftAdvisor dùng conditional co-pick share shrink về marginal, geometric lift qua mọi đồng đội, điều chỉnh odds điểm nền; composition exponent1 là policy công khai chưa học/tune. Synergy WR cũng đã sửa giữ cả hai role. Không có case theo tên tướng, không biến association thành synergy cơ học/tăng thắng. JSON lưu formula/base/lift/evidence và ma trận10cặp/đội; why giải thích công thức.

35 tests PASS, gồm nhiều cặp role, tránh ghép đối thủ, flex role, thiếu mẫu/cutoff, đổi tên tướng không đổi điểm. Hai phiên Gen.G–Bilibili Gaming tại Worlds, Blue/Red first, hoàn thành20lượt/tướng khác nhau; snapshot trước chung kết as-of2026-11-13 patch dataset16.20, 106ván/94ván patch, không dùng4ván final14/11. Lucian–Milio đứng đầu truy vấn support khi đã có Lucian trong hai snapshot LCK/Worlds đã kiểm tra; không ép kết quả hoặc khóa cặp khác.

Audit Worlds200lượt: Recall@5 cũ30%, recent-presence30%, mới36%, MRR@5=0.21225; CI mô tả chênh với baseline[+1,+12]điểm phần trăm. Đây là tập phát triển nhỏ đã xem, chưa phải final test độc lập/đánh giá tăng thắng; chưa tái dựng Fearless series trong benchmark. Candidate coverage86%. Không tải dữ liệu mới, sửa schema/raw DB hoặc huấn luyện ML.

Nguồn hiện hành: docs/WORLDS_ROLE_PAIR_REVIEW.md, reports/worlds_draft_role_pairs.json, reports/worlds_role_pair_checks.json, reports/wlds_draft_policy_evaluation.json; baseline cũ được giữ trong reports/worlds_replay_before_role_pairs.json. LCK và hybrid ghi bên dưới là các mốc lịch sử trước sửa composition.

## Rà soát LCK và meta theo patch — 2026-11-23

VERIFIED: snapshot patch/thời gian chung trong draft_meta.py; presence/slot/player share có decay 21 ngày, cửa sổ 60 ngày; bỏ percentile, giảm cosine, matchup theo phân phối role một-một. Lineup lấy từ trận gần nhất, không là live roster. CLI có as-of/patch/freshness guard/used-champions. Phiên lịch sử bỏ dự báo model để tránh model fit sau cutoff. LCK local đến 2026-09-13, patch dataset16.16, 153 ván cửa sổ/80 ván patch; không có dữ liệu mới được tải. 31 unit tests và 6 CLI scenarios PASS (LCK/LPL/ALL, Red first, previous-game pool, stale-data rejection, missing-patch rejection); checks: reports/lck_meta_checks.json. Replay đóng băng trước 20 trận/200 lượt: Recall@5 policy28.5%, recent-presence27%, long-history24%; CI chênh [-1.5,+4.5] điểm phần trăm, chưa chứng minh ưu thế hoặc tăng thắng. Coverage84.5%, chưa replay đầy đủ Fearless series. Chi tiết docs/LCK_DRAFT_REVIEW.md; reports/lck_draft_policy_evaluation.json. Không sửa raw DB/schema hoặc huấn luyện ML.

## Bản hybrid trước sửa — lịch sử, đã thay policy bên dưới

## Giả lập hybrid ban/pick — 2026-11-23

VERIFIED: giả lập hybrid 20 lượt đã tích hợp historical + content-based/cosine; 24 tests PASS và 5 smoke scenarios hoàn tất 20 tướng khác nhau. Giữ lựa chọn đội/phe, lọc đường, why, chọn tay, swap, wishlist, auto và lưu JSON căn cứ. Pick tối đa điểm weighted rank aggregation; ban theo chênh top1/top2 đối thủ trên bảng hiện tại. Màu phe độc lập thứ tự draft qua --first-pick. Không tuyên bố tối ưu toàn cục/tăng thắng, không đổi benchmark cũ hay huấn luyện model mới. Hướng dẫn: docs/GIA_LAP_BAN_PICK.md; checks: reports/draft_simulator_checks.json.


## Cập nhật Chương 6 — 2026-11-23

VERIFIED: content-based filtering đã có item profile → user profile có trọng số → cosine similarity theo Chương 6. Notebook 02 đã chạy đủ 6 cell mã; 16 regression tests PASS, ba CLI (seed, player, cold-start) và tích hợp engine PASS. Benchmark validation: 299 trận, 2990 truy vấn; Precision@10=0.0494, Recall@5=0.2990; popularity Recall@5=0.4652. Chưa vượt baseline về truy hồi; không tuyên bố tăng thắng. Không huấn luyện lại ML hoặc thay schema/raw DB. Hướng: vận dụng kiến thức môn học, có phần mở rộng. Xem docs/CHUONG_6_CONTENT_BASED.md và reports/content_based_evaluation.md.

> **TRẠNG THÁI ƯU TIÊN — Integrity v2, 2026-11-23.** Dự án đang triển khai theo roadmap; API/web chưa triển khai là công việc kế hoạch. Các tuyên bố cũ bên dưới như “100% Zero-Hardcode”, “hoàn thành 85% về chất lượng”, kết quả model cũ và kết luận nhân quả không còn là trạng thái nghiệm thu. Nguồn hiện hành: [INTEGRITY_V2.md](../docs/INTEGRITY_V2.md), [đánh giá ML](../src/06_machine_learning/evaluation_report.md), [benchmark recommender](../reports/recommender_evaluation.json).

Đã triển khai shared domain cleaning; giữ 1.009 trận rank với dấu đúng, 6.000 dòng đội giải, 30.000 dòng tuyển thủ, 4.862 dòng phút 10 đủ phép đo. Models Draft/Snowball schema v2 đã huấn luyện CUDA; validation/calibration/test riêng và manifest/fingerprint. Draft: accuracy=0.5517, AUC=0.5628, logloss=0.6834; Snowball: accuracy=0.6718, AUC=0.7413, logloss=0.6004.

Recommender có counts/Wilson CI, không còn uplift gán sẵn; điểm quy tắc không là xác suất. Benchmark Recall@5=0.1425, baseline phổ biến=0.3952; chưa chứng minh ưu thế. Phân cụm/radar vẫn dùng quy tắc chuyên gia, chưa retrain. Model cũ schema v1 bị từ chối. Các việc API/web/bảo vệ tiếp tục kế hoạch.

Kiểm chứng Integrity v2 cuối lượt: {"rank_rows": 1009, "negative_blue_gold_rows": 525, "inconsistent_clean_gold_rows": 0, "notebook_executed_code_cells": 8, "notebook_png_outputs": 5, "unit_tests_passed": 11, "workflow_commands_passed": 12, "gpu_preflight": "passed"}. Raw DB không sửa; notebook có output thực; ML/ranking metrics xem báo cáo hiện hành.

---

NỘI DUNG LỊCH SỬ / KẾ HOẠCH TRƯỚC INTEGRITY V2:

# PROJECT STATE (TRẠNG THÁI DỰ ÁN THỰC TẾ)

*Thời điểm audit thực tế:* 2026-11-23
*Nguồn dữ liệu:* Khảo sát trực tiếp từ mã nguồn, CSDL SQLite (`data/database/lol_live_data.db`), các mô hình `.pkl` đã huấn luyện trên GPU NVIDIA RTX 4070 và kiểm thử thực tế.

---

## 1. TỔNG QUAN HIỆN TRẠNG
- **Tên dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Môn học:** Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT).
- **Giai đoạn hiện tại:** Đã hoàn thành 100% Giai đoạn 1 (Thu thập & CSDL), Giai đoạn 2 (Thống kê suy diễn & EDA), và Giai đoạn 3 (Machine Learning, Phân Cụm & Ban/Pick AI - Milestone 3). Sẵn sàng bước sang Giai đoạn 4 (REST API FastAPI & Web App).
- **Trạng thái thực thi hiện tại:** 🟢 **ACTIVE (ĐANG HOẠT ĐỘNG)** — Tập trung phát triển Giai đoạn 4 (Backend REST API FastAPI & Giao diện Web App tương tác).
- **Đánh giá tiến độ tổng:** ~85% (Hoàn thành trọn vẹn Milestone 1, Milestone 2, Milestone 3).

---

## 2. HIỆN TRẠNG MÃ NGUỒN (SOURCE CODE AUDIT)

| Thư mục / File | Trạng thái thực tế | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| `src/config/` | `VERIFIED - WORKING` | Package cấu hình trung tâm dự án (`settings.py`, `__init__.py`). Nạp `.env`, thẩm định API key, quản lý đường dẫn và metadata. |
| `.specify/` & `.gemini/commands/` | `VERIFIED - WORKING` | Bộ công cụ **GitHub SpecKit (`specify-cli v1.4.4`)** đã được cài đặt vào `.venv` và khởi tạo đầy đủ cấu trúc `.specify/` (`memory/constitution.md`, `scripts/powershell/`, `templates/`, `workflows/`) cùng 9 slash commands `/speckit.*` trong `.gemini/commands/`. |
| `src/01_data_pipeline/` | `VERIFIED - WORKING` | Gồm `crawl_riot_matches.py`, `sync_google_drive.py` (OAuth 2.0 2 tầng, bộ lọc giải đấu LCK/LCP/LPL/MSI/WLDS/EWC), `load_esports_to_db.py` (ETL nạp CSDL SQLite) và 3 file README đặc tả. |
| `.env` / `.env.example` | `VERIFIED - WORKING` | File cấu hình biến môi trường và file mẫu template an toàn. `.gitignore` đã chặn `.env`. |
| `src/02_preprocessing/` | `VERIFIED - WORKING` | Gồm `cleaner.py` (Domain Filtering Remake/AFK, 5 nhóm Missing Imputation, IQR/Z-Score Outlier Trimming & Winsorization), `__init__.py` và `README.md`. Hoàn thành Task 1.3. |
| `src/03_database_sql/` | `VERIFIED - WORKING` | Gồm `queries.sql` (5 câu truy vấn SQL nâng cao Chương 5 & 5x), `execute_queries.py` (CLI runner tự động xuất 5 file CSV kết quả), `__init__.py` và `README.md`. Hoàn thành Task 1.4. |
| `src/04_hypothesis_testing/` | `VERIFIED - WORKING` | Gồm `test_blue_side_advantage.py` & `.md` (Task 2.1: Z-test lợi thế Phe Xanh), `test_snowball_effect.py` & `.md` (Task 2.2: Two-sample Welch t-test & Z-test Lăn cầu tuyết Pro vs Rank), `test_voidgrubs_vs_dragon.py` & `.md` (Task 2.3: Chi-square & Odds Ratio 3 Sâu vs Rồng 1), `__init__.py` và `README.md`. **Hoàn thành trọn vẹn 3 bài toán Thống kê suy diễn (100% Chương 1)**. |
| `src/05_visualization/` | `VERIFIED - WORKING` | Gồm `plot_eda_figures.py` (Bộ 5 biểu đồ EDA 300 DPI theo Giáo trình Chương 3), `plot_eda_figures.md`, `__init__.py` và `README.md`. Xuất 5 tệp PNG 300 DPI vào `reports/figures/`. Hoàn thành Task 2.4. |
| `notebooks/` | `VERIFIED - WORKING` | Đã hoàn thành và đóng gói Notebook toàn diện `01_kham_pha_du_lieu_EDA.ipynb` (21 cells, thực thi và render 100% outputs hình ảnh & bảng thống kê). Hoàn thành Milestone 2. |
| `docs/figure_explain/` | `VERIFIED - WORKING` | Trọn bộ 11 tệp tài liệu giải thích học thuật và phản biện chi tiết cho Bộ biểu đồ Fig 1..11 (300 DPI). |
| `src/06_machine_learning/` | `VERIFIED - WORKING` | Gồm `draft_model.py` (Draft AI Phút 0 - 808 chiều có ngữ cảnh khu vực/giải đấu, GPU CUDA), `snowball_model.py` (Snowball AI Phút 10 - GPU CUDA), `evaluate_models.py` (Đánh giá & xuất Fig 6..9), `cluster_archetypes.py` (Phân cụm K-Means & PCA 4 Trường phái Đội hình & xuất Fig 10..11), các báo cáo `.md` và 3 file model `.pkl`. Hoàn thành Task 3.1, 3.2, 3.3, 3.4. |
| `src/07_recommender/` | `VERIFIED - WORKING` | Gồm `recommender_engine.py` (Phân tầng khu vực LCK/LPL/LCP/MSI/WLDS/EWC, Hybrid Target Ban Tuyển thủ, Universal Counter-Pick vs Blind-Pick Engine trên 3,098 cặp kèo 1v1, Punisher Engine, Win Condition Card ADR-014), `simulate_draft_match.py` (Giả lập tương tác 2 chiều), `recommender_engine.md`, `models/recommender_engine.pkl` và `data/pro_player_accounts.json`. Hoàn thành Task 3.5. |
| `src/api/` | `NOT CREATED (FACT)` | Chưa tạo thư mục mã nguồn Backend FastAPI. |
| `web/` | `NOT CREATED (FACT)` | Chưa tạo thư mục giao diện Web App. |
| `reports/figures/` | `VERIFIED - WORKING` | Lưu trữ 11 tệp hình ảnh 300 DPI (Bộ 5 biểu đồ EDA Fig 1..5 + Bộ 4 biểu đồ Model Diagnostics Fig 6..9 + Bộ 2 biểu đồ K-Means & PCA Fig 10..11) xuất bản từ pipeline. |

---

## 3. HIỆN TRẠNG DỮ LIỆU & CƠ SỞ DỮ LIỆU (DATABASE AUDIT)

### CSDL SQLite chính: `data/database/lol_live_data.db`
- **Số bảng hiện có:** 3 bảng đạt chuẩn 1NF/3NF (FACT / VERIFIED):
  1. `matches_10min`: 1,009 dòng (550 VN2, 459 KR), 42 cột đạt chuẩn 1NF & 3NF.
  2. `tournament_matches`: 6,000 dòng (3,000 trận $\times$ 2 đội Xanh/Đỏ), 155 cột. Khóa chính: `(gameid, side)`.
  3. `tournament_players`: 30,000 dòng (3,000 trận $\times$ 10 tuyển thủ), 129 cột. Khóa chính: `(gameid, participantid)`, Khóa ngoại: `(gameid, side) REFERENCES tournament_matches(gameid, side)`.
- **Tổng số dòng dữ liệu trong DB:** **37,009 dòng** (FACT / VERIFIED).
- **Hệ thống Index tối ưu truy vấn:** 12 indexes đã được tạo tự động cho các trường lọc/nhóm phổ biến (`league, year`, `teamname`, `date`, `patch`, `playername`, `champion`, `position`...).

### Các tệp dữ liệu sạch tại `data/processed/`:
1. `data/processed/clean_ranked_10min.csv`: Dữ liệu Solo Rank sạch mốc 10 phút (977 dòng khi áp dụng filter both IQR/Z-score, 1,009 dòng khi áp dụng capping).
2. `data/processed/clean_tournament_10min.csv`: Dữ liệu Đấu Giải sạch mốc 10 phút (4,636 dòng khi áp dụng filter both, 4,752 dòng khi áp dụng capping).
3. `data/processed/clean_tournament_draft.csv`: Toàn bộ 3,000 trận Đấu Giải sạch (6,000 dòng) phục vụ mô hình Cấm/Chọn.
4. `data/processed/clean_tournament_players.csv`: Dữ liệu 10 vị trí tuyển thủ sạch (28,880 dòng khi áp dụng filter both, 30,000 dòng khi áp dụng capping).
5. `data/processed/lol_live_ranked_10min.csv`: Dữ liệu Rank thô ban đầu (1,009 dòng $\times$ 42 cột).
2. `data/raw/2026_LoL_esports_match_data_from_OraclesElixir.csv`: 106,896 dòng, 165 cột dữ liệu đấu giải chuyên nghiệp năm 2026 (8,908 trận). Kích thước: 71.5 MB (FACT / VERIFIED).
3. `data/raw/2025_LoL_esports_match_data_from_OraclesElixir.csv`: Dữ liệu mùa giải 2025 dùng cho cơ chế bù đắp mẫu thích ứng (Adaptive Merging). Kích thước: 79.1 MB (FACT / VERIFIED).
4. `data/raw/esports_active_matches.csv`: Tệp dữ liệu hoạt động được tạo bởi `sync_google_drive.py` tích hợp bộ 6 giải đấu đỉnh cao (`LCK, LCP, LPL, MSI, WLDS, EWC`) kết hợp ghép đuôi thích ứng (ADR-013). Kích thước: 26.97 MB, 36,000 dòng, đúng **3,000 trận đấu đỉnh cao** (1,890 trận năm 2026 + 1,110 trận cuối 2025, cập nhật đến ngày `2026-11-14`): LPL (1,092), LCK (812), LCP (474), EWC (265), WLDS (206), MSI (151). Tỷ lệ có Timeline 10 phút đạt **81.23% (2,437 / 3,000 trận)** (FACT / VERIFIED).
5. `.drive_sync_manifest.json`: Lưu vết thời gian và kích thước file đồng bộ từ Google Drive.

---

## 4. HIỆN TRẠNG MÔI TRƯỜNG THỰC THI (ENVIRONMENT AUDIT)
- **Hệ điều hành:** Windows x64 (FACT).
- **Môi trường ảo cô lập (.venv):** Đã khởi tạo tại thư mục gốc dự án: `d:\Chivinh\2026_MonHoc\Nhập môn khoa học dữ liệu\Project\.venv` (VERIFIED - Python 3.13.14).
- **Cấu hình VS Code:** Đã tạo `.vscode/settings.json` trỏ tự động `python.defaultInterpreterPath` về `.venv`.
- **Các package ĐÃ CÀI ĐẶT ĐẦY ĐỦ TRONG `.venv`:**
  - `pandas == 3.0.6`
  - `numpy == 2.5.3`
  - `scipy == 1.18.1`
  - `scikit-learn == 1.9.1`
  - `matplotlib == 3.11.2`
  - `seaborn == 0.13.2`
  - `gdown == 6.4.0`
  - `requests == 2.34.2`
  - `python-docx == 1.2.0`
  - `jupyter == 1.1.1` & `ipykernel == 7.3.0`
  - `google-api-python-client == 2.200.0`
  - `google-auth-oauthlib == 1.4.1`
  - `google-auth-httplib2 == 0.4.2`
- **Kết nối Riot Games API:**
  - Trạng thái: `VERIFIED - HTTP 200` (Đang hoạt động tốt).
- **Xác thực Google Cloud Drive API v3:**
  - Trạng thái: `VERIFIED - WORKING` (`credentials.json` và `.gdrive_token.json` đã lưu an toàn trong `.gitignore`).

---

## 5. CÁC RỦI RO, TỐI ƯU HÓA & DANH MỤC CẢI THIỆN (IMPROVEMENT BACKLOG)
1. **Google Drive Quota Exceeded:** `[RESOLVED 100%]` Đã khắc phục triệt để bằng cơ chế tải 2 tầng tích hợp Google Drive API v3 (OAuth 2.0 Smart Copy).
2. **Dữ liệu đấu giải 2026 nạp vào CSDL:** `[RESOLVED 100%]` Đã nạp thành công 6,000 dòng `tournament_matches` và 30,000 dòng `tournament_players` vào `lol_live_data.db`.
3. **Hệ Thống Ma Trận Kèo Đấu & Gợi Ý Đối Đầu Toàn Diện (Universal Counter-Pick vs Blind-Pick Engine):** `[RESOLVED & VERIFIED ON ALL 5 LANES / 3,098 MATCHUPS]`
   - *Đã hoàn thành:*
     - Tăng tốc huấn luyện GPU NVIDIA CUDA (`device='cuda', tree_method='hist'`) trên RTX 4070 và tối ưu 14 SQLite Indexes (`idx_tp_game_pos_side`, `idx_tp_game_side_pos`).
     - Phân tầng Meta Cấm/Chọn theo từng Khu vực & Giải đấu Quốc tế (`LCK`, `LPL`, `LCP`, `WLDS`/CKTG, `MSI`, `EWC`, `INTERNATIONAL`, `ALL` - ADR-015).
     - Triển khai **Universal Counter-Pick vs Blind-Pick Engine (ADR-016)** 100% dựa trên thuật toán & dữ liệu (Zero-Hardcode) cho toàn bộ 5 vị trí và 3,098 cặp đối đầu 1v1: Nhận diện chính xác 1-1 tướng cùng đường, Ngưỡng loại bỏ cứng tổng quát (`WR < 47.5%` hoặc `GD@10 < -110g`), Khóa điểm tướng tủ (`player_bonus`) khi gặp kèo dưới, Làm mịn Bayes (`C=10.0`) & Smooth Sample Confidence (`n / (n + 8)`), và Bộ lọc độ tinh khiết vị trí (Role Purity Filter).
     - Tài liệu hóa toàn diện trong [`docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md`](../docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md).



---

IN PROGRESS: Khắc phục audit theo yêu cầu 4 mục. Đã thêm canonical domain cleaning và validation tách train/validation/calibration/test theo gameid. Models cũ không còn tương thích schema v2; đang chờ huấn luyện CUDA và kiểm chứng. Các tuyên bố hoàn tất/Zero-Hardcode và số liệu trước mục này là lịch sử, chưa phải nghiệm thu sau sửa.
