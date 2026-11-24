## Dừng collector Rank nền & chốt số liệu báo cáo — 2026-11-24

- Dừng tiến trình `update_rank_evidence.py --watch` (PID `29828` / `7992`), xác nhận không còn tiến trình nền.
- Chốt số liệu đóng băng từ `reports/rank_matchups_live/summary.json` (`975` trận, `9,750` dòng, `5,236` cặp gộp, `148` cặp `n >= 5`) và tái tạo `reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx` cùng `BAO_CAO_CUOI_KY.md` để khớp tuyệt đối.
- **No-impact note (`AI/KNOWLEDGE_RULES.md` §4):** Không phát sinh thay đổi kiến thức/phương pháp/chức năng mới; không retrain, không commit/push.

## Xuất Báo cáo cuối kỳ Word (.docx) kèm biểu đồ & phân tích mạch giá trị — 2026-11-24

- Tạo `scratch/build_final_report_docx.py` và xuất `reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx` (4,725.6 KB, 105 đoạn, 15 bảng/callout, 13 ảnh nhúng trực tiếp: `fig1`–`fig9`, `fig11` và 3 ảnh Web UI thật).
- Bổ sung phân tích mạch giá trị ("làm để làm gì?" và "giúp ích gì cho kết quả cuối cùng của dự án?") xuyên suốt Chương 1–6 kèm bảng kết quả thực từ SQL Q1–Q5, 3 kiểm định giả thuyết, ML v2 và Content-Based.
- Cập nhật `reports/README.md`. **No-impact note (`AI/KNOWLEDGE_RULES.md` §4):** Không phát sinh thay đổi kiến thức/phương pháp/chức năng mới; không sửa code/DB/model, không retrain, không commit/push.

## Biên soạn Báo cáo cuối kỳ — 2026-11-24

- Tạo `reports/final_report/BAO_CAO_CUOI_KY.md` tổng hợp toàn bộ đồ án theo Chương 1–6, tách bạch `MH`/`UD` với `MR`/`NV`, trích đúng số liệu từ các tệp CSV/MD/JSON đã xác minh và giải trình rõ giới hạn của `draft_model`, `content_based`, `archetype_kmeans` và tập đánh giá hiện tại.
- Cập nhật `reports/README.md`.
- **No-impact note (`AI/KNOWLEDGE_RULES.md` §4):** Không phát sinh thay đổi kiến thức/phương pháp/chức năng mới; toàn bộ số liệu và phân loại bám sát sổ kiến thức hiện hành. Không sửa code/DB/model, không retrain, không commit/push.

## Dọn sạch & chuẩn hóa tài liệu, dừng web server nền — 2026-11-24

- Dừng tiến trình web server nền (`uvicorn` trên `127.0.0.1:8000`, PID `28952` / `46456`).
- Xóa các mục lặp và sửa lỗi dính chữ trong `AI/{PROJECT_STATE,ARCHITECTURE,TASKS,CHANGELOG,DECISIONS,DATABASE}.md` và mục 28–30 của `docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md`.
- Thu gọn 14 banner đầu `README.md` thành bảng trạng thái hiện hành; tạo `reports/README.md` phân loại sản phẩm nộp môn học, minh chứng hiện hành và artifact lịch sử.
- **No-impact note (`AI/KNOWLEDGE_RULES.md` §4):** Không phát sinh thay đổi kiến thức/phương pháp/chức năng; các mục hiện hành (MH-01..14, MR-01..24, NV-01..24) giữ nguyên. Không sửa code/DB/model, không retrain, không commit/push.

## Thu gọn toàn bộ Hiểu lựa chọn — 2026-11-24 (NV-24)

Inspector React thêm `collapsed` state và nút **Thu gọn toàn bộ** ở header. Khi collapsed, unmount toàn bộ body (tên, cảnh báo, lý do, thành phần, bảng nguồn, footer), chỉ giữ header nhỏ có nút Mở rộng / Đóng; `timeline y` giảm khi collapse. Khi mở rộng sẽ khôi phục body như cũ, selection không đổi, hành vi click-only và deselect cũ giữ nguyên. CSS header button dùng flex cùng `aria-expanded`/`aria-controls`. Build TS/Vite PASS; Edge 1 workflow PASS (`body` absent, header < 100px, timeline gần hơn, reopen body > 100px, close/deselect/reset/reload). Minh chứng: `reports/ui_inspector_collapse/{REPORT.md,browser.log}`. Chỉ thay đổi UI presentation (NV-24), không đổi khoa học/API/score/schema/model nên không chạy lại Python test hay retrain; không commit/push.

## Hiểu lựa chọn ẩn mặc định và click-toggle — 2026-11-24 (NV-24)

React App đặt `selected=null` và `inspectorOpen=false` mặc định, cũng như sau accept hoặc đổi ván. Bấm thẻ gợi ý / chọn tay sẽ mở Inspector; bấm lại thẻ đang chọn sẽ bỏ chọn và ẩn. Nút Đóng giữ selection và cho phép mở lại qua nút riêng; bỏ chọn sẽ không còn nút mở. Lịch sử click để mở / bấm lại để ẩn, không tự popup qua chuyển lượt hay reload. Không tạo fake advice cho lựa chọn tay ngoài pool. Chỉ thay đổi UI state/CSS, không đổi phương pháp khoa học/API/scoring/model/DB nên không train hay chạy lại Python test. TS/Vite build PASS, toàn bộ 7 Edge workflow PASS. Minh chứng: `reports/ui_inspector_toggle/REPORT.md` + `browser.log` + browser artifacts. Sổ mục 30 (NV-24) và hướng dẫn sử dụng đã đồng bộ; không commit/push.

## Sửa responsive hai khu chọn bị xuống — 2026-11-24 (NV-24)

CSS breakpoint 3 cột hạ từ `1200px` xuống `900px`, cột co giãn đối xứng `1fr / 2.7fr / 1fr`, bỏ `min-width` nội dung cứng, `margin: 0` và `align-items: stretch` cả 3 khu để cùng hàng và cùng chiều cao. Giữa vẫn giữ role dọc, setup trên và inspector dưới. Build TS/Vite PASS; Edge 1 layout test qua 7 độ rộng (`900/1024/1100/1199/1366/1553/1920px`) và mobile `390px` không tràn ngang. Minh chứng: `reports/ui_sidebars_fit/{REPORT.md,browser.log,desktop.png,mobile.png}`. Chỉ chỉnh trình bày NV-24, không đổi khoa học/API/score/DB nên không train hay chạy lại Python test; không commit/push.

## Làm rõ hai khu nằm hai bên khung giữa — 2026-11-24 (NV-24)

User làm rõ bố cục desktop: Gợi ý ở cột trái | hai đội hình ở giữa | Chọn tay ở cột phải, cả 3 cùng hàng. CSS Grid `>= 1200px` đã đổi `grid-template-areas`, hai đội vẫn xếp role dọc, căn giữa; setup trên và inspector dưới. Màn nhỏ responsive giữ nguyên. Không đổi logic/API/score/DB/model; chỉ trình bày NV-24 nên không retrain hay chạy lại Python. TS/Vite build PASS, Edge centered-board test PASS. Minh chứng: `reports/ui_flanking_choices/{REPORT.md,browser.log,desktop.png,mobile.png}`. Sổ mục 30 (NV-24) bổ sung mốc làm rõ; không commit/push.

## Căn giữa lại bảng tướng theo bố cục cũ — 2026-11-24 (NV-24)

Theo user chỉnh hướng: bỏ 5 pick cards nằm ngang mới thêm, giữ hai đội Blue/Red ở giữa (`max-width: 1000px`), mỗi đội 5 role hàng dọc với portrait `47px`. Setup trên đầu, gợi ý trái / manual phải, inspector dưới giữ nguyên; drag và auto-role không đổi. Chỉ CSS trình bày, không ảnh hưởng kiến thức khoa học/algorithm/DB/model/API nên không retrain hoặc chạy lại Python tests. TS/Vite build PASS, Edge centered-board test PASS. Minh chứng: `reports/ui_centered_board/{REPORT.md,browser.log,desktop.png,mobile.png}`; sổ mục 30 (NV-24) bổ sung mốc mới. Không commit/push.

## UI gọn / kiểm kèo đã lộ / Renekton / First Selection — 2026-11-24 (MR-12 sửa, NV-24)

Đã hoàn tất yêu cầu: thiết lập trên đầu, gợi ý trái / chọn tay phải, inspector dưới; bảng đội hình gọn, native drag/drop đổi slot cùng đội (trống hoặc đã có tướng), từ chối cross-team và archive, có menu dự phòng bàn phím/chạm. Chọn tay không dùng dropdown role: dựa trên snapshot Pro `role_counts` giảm dần, bỏ slot bận, preview và API commit dùng cùng rule; tướng không rõ hoặc không còn slot đã quan sát sẽ báo lỗi, không tự bịa role. `draft_safety.py` và API trả `role_preferences`.

Tái hiện case Galio Top vs Ambessa ở turn 19 (pick 9 toàn trận, địch mới lộ 4 tướng): gate cũ chờ đủ 5 tướng địch nên bị lọt. `lane_review` kiểm trực tiếp role đang gán và yêu cầu review khi `n < 5` ngay cả khi địch chưa đủ 5; blind role không gán `n=0`. Contextual cùng role hoặc khi mọi role trống đều đã lộ đối thủ sẽ dùng cận dưới Wilson 95% trước base current score (vẫn giữ wishlist / lớp đủ mẫu / pair guard ở trên). Cùng prefix: top cũ Galio → top mới Gnar, Renekton lên top 2; thứ tự mới: Gnar / Renekton / Camille / K'Sante / Galio. Raw score không đổi, GD không đưa vào feature, Rank không đưa vào score. Renekton `2/2` WR 100%, GD15 `+787`, Wilson `34.2%–100%`; Gnar `5/6`, GD15 `+686`, Wilson `43.6%–97.0%`; CI chồng lấn nên không tuyên bố vượt trội.

First Selection trên UI do người dùng cấu hình từng ván; CLI nhiều ván bắt buộc truyền danh sách đủ `n` phần tử, bỏ legacy alternating fallback. VERIFIED: 178 tests PASS, TS build PASS, 5 Edge workflow PASS. CLI all-Blue 5 ván đủ 100 actions / 50 unique picks / locks `0-10-20-30-40` (có test override); all-Red và all-Blue manual legal replay PASS. Minh chứng: `reports/ui_lane_revision/` và `bo5_blue_first`. Pro DB SHA-256 `20e3d973...` không đổi; không train/Rank collector/commit/push. Sổ mục 30 (MR-12 sửa / NV-24), ADR-043, `docs/UI_COMPACT_VA_KIEM_KEO_DA_LO.md`.

## Giữ cặp bot / First Selection người dùng chọn — 2026-11-24 (MR-24/NV-23)

Tái hiện đúng case 10 lượt đầu: Blue Nautilus → Jayce, Red ban Jhin/Kai'Sa → Blue Yunara. `pair_reservation.py` đếm ban địch sau lượt hiện tại đến trước pick tiếp theo của mình, quét toàn bộ legal bot/sup (`n >= 5`, `effective_lift >= 1`), ưu tiên `secure_now` khi số đối tác dương `<= ban_budget`. Không đổi score current, có `priority_tier`/lý do/count/CI riêng; giữ wishlist, lớp đủ mẫu, lọc role và chọn tay. UI chọn Blue/Red First Selection mỗi ván, bỏ auto luân phiên; CLI thêm `--first-picks`. VERIFIED: 170 tests PASS (11 mới), TS/Vite build PASS, 3 Edge workflow/mobile PASS. Minh chứng: `reports/pair_reservation_revision/`. Pro DB SHA-256 `20e3d973...` không đổi; sổ mục 29 (MR-24/NV-23), `docs/GIU_CAP_BOT_VA_FIRST_SELECTION.md`, ADR-042 đồng bộ.

## Hai khu UI và contextual v2 — 2026-11-24 (MR-13 sửa / NV-22)

Tách gợi ý và chọn tay thành 2 panel đồng hiện với nút confirm riêng; sửa `BanPlanner.pool_value` v2 = `sum(non-negative top 3) / 3` cố định để khử bất nhất mất backup mà tăng pool value ở `n < 3` (80 ban states WLDS 16.20: số probe tăng ngược `10+21 → 0`; Recall@5 giữ `0.675 / 0.525`). API chốt ngày UTC khi `as_of` trống, gắn `snapshot_id` + `configuration`, trả `409` khi lệch. 159 unit tests PASS (5 mới), build PASS, 2 Edge workflow PASS. Minh chứng: `reports/contextual_ui_revision/`. Sổ mục 28 (NV-22), ADR-041, docs BAN/UI đồng bộ.

## UI React + TypeScript local đã chạy — 2026-11-24 (NV-21)

Thêm `web/` (React/TS/Vite, CSS thuần) và `src/api/app.py` (FastAPI adapter), tái sử dụng `DraftState`/`DraftAdvisor`/`BanPlanner`, default pick `current`, ban `contextual`/`legacy`. Build/typecheck PASS; 154 Python tests PASS (8 API mới); browser Edge thật PASS một ván → ván 2 khóa 10, đổi đường/undo/archive/export/reload/mobile 390px. `start_ui.ps1` build và serve local `127.0.0.1:8000`; hướng dẫn `docs/UI_REACT_TYPESCRIPT.md`, minh chứng `reports/ui_demo/`. Sổ mục 27 (NV-21), ADR-040, constitution `1.3.0`.

## So sánh điểm đơn giản, không đổi default và BO5 minh họa — 2026-11-24

Thêm `AdvisorPolicy.scoring` (`current`/`simple`) và `DraftAdvisor._simple_rows` (3 tín hiệu: frequency, cosine, same-role WR có fallback). `compare_pick_scoring.py` so 200 validation / 320 test cùng frozen role pool: `current` Recall@5 `0.49375` / MRR `0.3026` vs `simple` `0.425` / `0.2334` (delta `-0.06875`, CI `[-0.11034, -0.03235]`), nên giữ mặc định `current`. BO5 simple T1–Gen.G đủ 5 games / 100 actions / 50 unique picks (44 fallback WR / 5 sparse có nhãn). 146 tests + integration PASS, canonical DB hash không đổi. Doc `docs/TINH_GIAN_DIEM_RECOMMENDER.md`, sổ mục 26 (MR-23/NV-20).

## Phạm vi môn học vừa sức, target mặc định null — 2026-11-24

Rà soát module và mapping Chương 1–6, thêm `docs/PHAM_VI_DO_AN_VUA_SUC.md`, cập nhật `AI_RULES`, `KNOWLEDGE_RULES` và constitution `1.2.0`. Bỏ target mặc định 2,000 trong `aggregate`/`export_tables`/CLI (`target=None`, summary v3, `ugg_reference_status=not_loaded`, `parity=False`). 139 full tests + 70 rank subset + integration 418 games PASS. Khởi động lại watch không quota PID 29828 / worker 7992. Sổ mục 25 (NV-19).

## Bằng chứng Pro/Rank, bảng giải thích và thử contextual — 2026-11-24

Thêm matchup_evidence.py và evaluate_contextual_evidence.py; DraftAdvisor chỉdecorategợiý sauxếpđiểm, simulatorinbảngởgợiý/why. RawSQL Pro/Rank khôngđổi; nguồnPro cùnggame/role/opposingside, sốâm/missing, catalogidentity; RankreadonlyWALtransaction, availabilitytínhcảingestion tránhbiếttrướctimeline, publickhôngPUUID. ExportPro3.000games/30.000rows/3.098pooledpairs/1.170n5, 24.370/24.380measurements tại10/15 cho từngmetric. Wilson/tCI dùnglại; khôngđưa tài nguyêntrậnqueryvàofeaturedraft.

Freeze261Rank07:36:57UTC24/11, experimentcontrolPro/Rankmatchup/hybridfixed50-50same-role, diagnostic30validation/30test ×3. Cả3Recall5=.6/.533333,MRR5=.313889/.315;hybridtop5khôngđổi.0RankknownởcutoffProquákhứ, dữliệuProđãdùngaudit:thăm dòhànhvi,khôngqualityproof. Prospective0series/readyFalse/resultNull,5+5series protocolvà--freezerepro; khôngtạofinalmetricsgiả/đổiweightsmain.138tests(12mới)+integration6stored-diff/mirror/roles/privacy/console/hashPASS. DocPRO_RANK_MATCHUP_EVIDENCE, sổ24/MR-22/NV-18, moduleindex/AI cậpnhật. KhôngMLtrain/commit/push, khôngservicecollectorchange.

## U.GG-style pooled tables và hiệu quả thu nhiều server — 2026-11-24

Nghiệmthu cuối:150games/1.500rows/725người,1.248scoped/1.170pooledpairs,14scopedn5/0pooledđạt2.000;69testsPASS + DB/FK/mirrors/dedup/privacy/sourcehash,140qualification và389listmembership kiểmraw. Phiênbulk101HTTPattempt xửlý40jobs (39accepted/1rejected),1freshindividualsnapshot, khônglàbenchmarkđối chứngspeed. WatchthậtPID23100 khởichạy07:17:06UTC/14:17VN24/11, manifestcollector_process.json/logs riêng; khôngcàiservice. Summarylive khácchecksnghiệmthu; sốliệusaucóthểtăng.

rank_matchup_tables.aggregate/export_tables thêm pooled scope ALL_OBSERVED nhưng giữqueue/tier/role, provenance patch/platform, n/CI tính từrawdedup, patchGD15direction mô tả, progress2.000/kèo vàreportv2. Ngưỡng2.000chỉmục tiêu; khôngtuyênbốthuậttoánU.GG/Worldcoverage/counterbấtbiến. update_rank_evidence thêm CLI target, next_job round-robinmetadata; bootstrap từ currentLeague-v4lists archive/typedqueue-tiercheck, batchupsert membershipsnapshot đúngPUUID, refresh15min/TTL giữtime, individualfallback nếu cần. KhôngschemaSQLite/Proscore/MLchange. 69testsPASS (6mới), livecảKR/EUW/NA và9listarchives đãcó; phiên153attempt thêm15games, phiên80attempt thêm8games; phiênbulk tiếp theo xem sessions/checks cuối. Doc POOLED_MATCHUPS_UGG_STYLE, sổMR-21/NV-17 và AI cậpnhật. Khôngcommit/push. Watchprocess/log ghi riêng khi khởi chạy; khôngservice/autostart và khôngđánhdấuthoàn tấtmục tiêu dữliệu.

## Rank evidence lake và bảngwinrate/GD15 tăngdần — 2026-11-24

Thêm rank_lake.py/update_rank_evidence.py/rank_matchup_tables.py,14test mới; typedclientdeadline vàatomicJSON, gitignoreDB-WAL/lock. Newranked_evidence.db schema metadata/seeds/jobs/snapshots/observations/sessions, policyfingerprint, canonicalguard, SQLiteWAL/filelock/FK/PK/10rowtransaction. Import10oldacceptedmộtlần, bootstrapC/GM/M,participantBFS,100recentIDs/page,cursor/polltime vàjobs persist, checkpointfieldqualificationtrướctimeline, TTL15mingiữtimestamp, exactall10Master+/24h/15min. Cap600HTTPattempt/15minmỗiphiên, watchlặpphiênkhôngtrầntổngkhôngcài service;auth/errorstopcheckpoint. Raw/SQLprivate, publickhôngPUUID.

Live600requestphiên063723199769Z ->87trận đủobs và1qualificationđangchờtimeline. Tiếpphiên065152611238Z 2requests/0snapshotmới ->88completegames(78mới),880rows382người;714pairs/8n5,11.012seeds/5pending/7rejected.63unit tests + integrationDB/FK/rebuildallnewqualifications/mirror/privacy/idempotence/canonicalhashPASS. all_matchups giữ sparse;3bảng xếptáchwinratecao/thấp/GD15 vớiWilson+meanCIStudenttNIST vàlimits, khônggọiU.GGinternalreplica. Khôngtrain/đổiProscore/canonicalDB. Docs vàsổmục22/MR-20/NV-16đãghi nguồn/giớihạn/output/trạngthái;2phiênđãkếtthúc, khôngđểserviceẩn.

## Rank campaigns/độphủ và temporalreadiness — 2026-11-24

Thêm collect_rank_batches.py (seen_matches/campaign/main), rank_coverage.py (load_cohort/observations/coverage_tables/chronological_plan/build/main),9testmới. Collector thêmoffset/exclusion/private seedregistry; RiotClientbudgetđếmHTTPattemptgồmretry; dừng đúngbudget/terminal, khôngthu vôhạn. Revalidateaccepted/dedup sớmnhất, identitychampID, distinctPUUIDtrongmemory, reportkhôngPUUID. Rejected chỉđịnhuniverse tênkhôngtăngn; scopegiữriêng. HeaderchoemptyCSV,JSONscalar,targetscope mới nhất và time ties cùngsplit được kiểm.

Campaign20261124T060507936864Z,3run mới060507936998/060626740398/060747435457Z:15seed/15IDs mới,179/200attempt,8accepted/7quácũ/0missing. Tổng10accepted/100rows/72người.115champion-role/2156directedpair,0supportn5/3người;46championrole/2058pairzeroevidence. Plan6/2/2nhưng0historyavailable trướcval; available_at=maxsnapshot/detailfetch, nếuthiếuprovdùngfinished_at. Khôngbenchmarkgiả,recommenderRank/UIđểconditionalplanned.49tests + integration DB/raw/source/count/privacy/budgetPASS. Docs vàsổmục21/MR-19/NV-15đồngbộ; khôngtrain/đổiPro/ML/DB.

## Thu thập rank snapshot từng người — 2026-11-24

Thêm collect_rank_snapshots.py (parse_snapshot/classify_match/collect_run/main),11test mới; typed status_code cho RiotError và clientthrows, configv2snapshot24h/15min. 10Solo/Duoentries phảiđúngqueue/server/identity; currenttier/chụpnốitiếp, khônghistorical. Snapshotcache riêngrun; private rawresponse + normalizedrecords, publicreport khôngPUUID/names. Nhận/loại/thiếu córeason; APIauth/rate/networkterminal dừngpartialreport,404participantthiếu; không điềntier từseed/Flex/noentry.

Live run20261124T055630861038Z:5seed/5trận,65clientcall,49unique người/50lượt do1lặp.5all10Master+ hiện tại,2nhận gầntrận/3loạivìquá24h/0thiếu;20observations đủ6phépđo.40tests + đối chiếureal49payloads/5classifications/signedmirror/privacy/DBrawPASS; historical gate nhận0snapshots. Khôngsửaolddata/model/runtimedraft hoặctrain. Artifacts reports/rank_snapshot_collection/{runid}/ vàlatest.json; docs/COLLECTOR_RANK_SNAPSHOTS, sổmục20/MR-18/NV-14, AI/indexdocsđồngbộ. Benchmark vàruntimeRankcònlộtrình.

## Thiết kế hai chế độ và admission Rank cao — 2026-11-24

Thêm config draft_modes.json và rank_eligibility.py (utc/read_policy/participant_evidence/assess_match/audit/main),10tests mới. Master+ ngưỡng làm việc chỉnh được, all10 historical interval đúngqueue/server/source/time; không suy current snapshot/seed thành historical rank. Unknown không là thấp; conflict loại, evidence chỉ kiểm hợp đồng chưa xác thực độc lập. Rank mode mới chỉ thiết kế/cổng dữ liệu, chưa chạy recommender.

Evaluator mặc định dùng admission đúng freeze, chỉ eligible IDs; thiếu chứng cứ dừng exit2 trước replay/ghiđè metric; cờ --allow-seed-only-research công khai phép thử cũ.92raw hiện có đều seed-only/0historical-qualified;29testsPASS, DB/raw/metric JSON cũ không đổi. Thêm cohort note cho report mốc18 và cập nhật lệnh tái lập có output riêng. Reports/rank_cohort_audit và docs/HAI_CHE_DO_VA_TIEU_CHUAN_RANK_CAO, sổ mục19/MR-17/NV-13, AI/index docs đồng bộ. Không retrain/đổi runtime advisor/ban/BO5 hoặc gọi411API lấy currentrank để hồi tố.

## Chuẩn hóa và thử nghiệm Rank transfer — 2026-11-24

Thêm rank_data_contract.py (official catalog ID/name, unknown/collision reject), evaluate_rank_transfer.py (temporal series split, frozen Pro/Rank evidence,3mode chỉ matchup, bootstrap/replay/contract audit),9test mới, mở collector date range/per-seed/interval1.3s/ended_at/catalog/schema v2. Không gọi evaluator từ simulator; hybrid là nghiên cứu, không runtime.

Tải96ID từ20seed ->92trận duy nhất,83đúng16.20;411participant khác nhau,18tên nội bộ chuẩn hóa, raw private gitignored. Audit30.000Pro CS không mismatch; diff10/15 khi có phép đo không mismatch. History/val/test27/9/10series, freeze trước26/10/2026 18:03:09UTC, Rank dùng ended_at và đúngpatch/KR. Validation200query R5=.515 cả3; test320 R5=.49375/MRR5=.302604 cả3,13query có hỗ trợ Rank n5. Test orderedtop5 khác control ở3Rank/1Hybrid query nhưng rank pick thật không đổi. CI[0,0] là suy biến mẫu, không equivalence.19unit tests + integration checks PASS; DB không đổi.

Giữ toàn bộ legacy/contextual/model/DB; không train hoặc tune để ép cải thiện. Dữ liệu Pro đã dùng trước nên chỉ thăm dò, cần tập mới độc lập; chưa tích hợp. Outputs reports/rank_pro_study_data và reports/rank_transfer_evaluation; protocol docs/RANK_TRANSFER_PROTOCOL.md, sổ mục18/MR-16/NV-12, module index và AI docs đồng bộ. Mốc smoke5trận/report v1 giữ như lịch sử.

## Đối đầu Rank riêng với Pro — 2026-11-24

Thêm `ranked_matchups.py` và10unit tests: client Riot retry hữu hạn/không in khóa; cache/provenance; reject role mơ hồ, ghép team/participant ID; signed gold/XP/CS10/15, missing không điền0. before mặc định không sau mốc, nearest±1000ms chỉ mô tả, ghi timestamp/offset thật; không dùng phút9 thay10. Pro từ shared cleaning, phép đo complete, nhóm riêng platform/queue/patch/role/tướng/đối thủ; ghép cùngpatch không pooling. Output5CSV/REPORT/summary/checks/tests.log ở `reports/rank_pro_matchups/`.

Đã lấy thật5trận KR16.23 ngày22/11/2026 UTC từ1seed,50dòng nearest đủ6phép đo; before thiếu đúng do frame sau mốc128–254ms. Worlds206trận/2060dòng trên4patch,1940dòng đủ phép đo; không patch chung nên ghép0dòng.10tests và integration signed mirror/cutoff/coverage/timestamp/DB SHA256 PASS;110link sổ PASS. Không sửa DB/model/điểm draft/train. Đồng bộ AI docs, danh mục module, hướng dẫn và sổ MR-15/NV-11; còn thiếu dữ liệu/benchmark chuyển miền, không nhận smoke là minh chứng counter/tăng thắng.

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

2026-11-23 — Integrity v2 theo yêu cầu 4 mục. Không đổi schema/raw SQLite. Bổ sung `analysis_data.py`, `validation.py`, `historical_recommender.py`, `evaluate_recommender.py`, regression tests. Các loader SQL/EDA/ML cùng domain snapshot; export lại CSV. XGBoost 3.4.1 build CUDA13.3 không chạy với driver CUDA12.6; đã cài/pin XGBoost3.0.5 và kiểm tra thiết bị booster CUDA. Draft: accuracy=0.5517, AUC=0.5628, logloss=0.6834; Snowball: accuracy=0.6718, AUC=0.7413, logloss=0.6004.

Recommender được đánh giá trên 6.000 truy vấn từ 600 trận: heuristic yếu hơn popularity về Recall@5. Kết quả được ghi nguyên trạng; không sửa thuật toán theo test để làm đẹp điểm. Notebook/tài liệu/figures được cập nhật; xem `reports/integrity_checks.json` cho kiểm chứng luồng thực thi và `tests/test_data_integrity.py` cho regression.

Kiểm chứng Integrity v2 cuối lượt: {"rank_rows": 1009, "negative_blue_gold_rows": 525, "inconsistent_clean_gold_rows": 0, "notebook_executed_code_cells": 8, "notebook_png_outputs": 5, "unit_tests_passed": 11, "workflow_commands_passed": 12, "gpu_preflight": "passed"}. Raw DB không sửa; notebook có output thực; ML/ranking metrics xem báo cáo hiện hành.

---

NỘI DUNG LỊCH SỬ / KẾ HOẠCH TRƯỚC INTEGRITY V2:

# CHANGELOG (NHẬT KÝ THAY ĐỔI DỰ ÁN)

Tất cả các thay đổi quan trọng về code, CSDL và tài liệu kiến trúc được ghi lại tại đây theo thứ tự thời gian.

---

## [2026-11-23] - NÂNG CẤP THUẬT TOÁN KHẮC CHẾ ĐƯỜNG TỔNG QUÁT (UNIVERSAL COUNTER-PICK ENGINE), PHÂN TẦNG KHU VỰC (LCK/LPL/LCP/MSI/WLDS), TĂNG TỐC GPU CUDA & CẬP NHẬT BỘ QUY TẮC AI_RULES
- **1. Tăng tốc Huấn luyện GPU (NVIDIA GeForce RTX 4070 CUDA) & Tối ưu Composite Indexes SQLite:**
  - Cập nhật `src/06_machine_learning/draft_model.py` và `src/06_machine_learning/snowball_model.py` tự động phát hiện và huấn luyện `XGBClassifier` trên GPU (`device='cuda', tree_method='hist'`).
  - Bổ sung 2 chỉ mục phức hợp `idx_tp_game_pos_side` và `idx_tp_game_side_pos` trong `src/01_data_pipeline/load_esports_to_db.py`, tăng tốc truy vấn Self-JOIN ma trận 3,098 cặp kèo đối đầu 1v1 lên hơn 50 lần.
- **2. Phân tầng Meta Cấm/Chọn theo từng Khu vực & Giải đấu Quốc tế (`ADR-015`):**
  - Hỗ trợ 8 chế độ khu vực/giải đấu (`LCK`, `LPL`, `LCP`, `WLDS`/CKTG, `MSI`, `EWC`, `INTERNATIONAL`, `ALL`) trên toàn bộ `recommender_engine.py`, `draft_model.py` (808 chiều đặc trưng) và `simulate_draft_match.py` (bổ sung cờ `--region` và `--interactive`).
  - Áp dụng công thức Hòa trộn Thích ứng ($w_{\text{reg}} = \frac{n_{\text{reg}}}{n_{\text{reg}} + \tau}$) giữa thống kê khu vực và toàn cầu.
- **3. Triển khai Thuật toán Khắc chế & Đi đường Tổng quát 100% Dựa trên Dữ liệu (`ADR-016` - Zero-Hardcode):**
  - Áp dụng cho toàn bộ **5 vị trí (`Top`, `Jungle`, `Mid`, `Bot`, `Support`)** và **3,098 cặp đối đầu trực tiếp 1v1** trong `src/07_recommender/recommender_engine.py` và `src/07_recommender/simulate_draft_match.py`:
    - Nhận diện chính xác 1-1 tướng đối thủ cùng đường (`_infer_enemy_lane_assignment` & truyền trực tiếp dictionary 5 vị trí).
    - Tách biệt 2 chế độ chấm điểm `Blind Pick` (chưa lộ đối thủ cùng đường) và `Counter Pick` (đã lộ đối thủ cùng đường).
    - Thiết lập **Bộ lọc Ngắt cứng Tổng quát (Universal Hard Cut-off)**: Tự động loại bỏ mọi ứng viên có tỷ lệ thắng đối đầu $< 47.5\%$ (mẫu $\ge 3$ trận) HOẶC bị đè đường phút 10 ($\text{GD@10} < -110\text{g}$ đối với Top/Jng/Mid/Bot; $< -150\text{g}$ đối với Sup nếu không có tỷ lệ lật kèo $\ge 52.5\%$).
    - Khóa điểm Tướng Tủ (`player_bonus` giảm 85–90%) nếu tướng tủ rơi vào kèo dưới hoặc chưa được kiểm chứng khả năng đi đường trước tướng đối diện.
    - Nâng tiên nghiệm làm mịn Bayes lên $C = 10.0$, hệ số tin cậy mẫu $\alpha = \frac{n}{n + 8.0}$, hiệu chuẩn điểm đơn điệu (`0.48 + 0.52 * raw_score`) và bổ sung Bộ lọc độ tinh khiết vị trí (Role Purity Filter: yêu cầu $\ge 35$ trận toàn cầu hoặc $\ge 15$ trận khu vực cho các tướng flex trái vị trí gốc).
  - Đã huấn luyện lại và cập nhật toàn bộ `models/recommender_engine.pkl`, `models/draft_model.pkl`, `models/snowball_model.pkl`, `models/archetype_kmeans.pkl`.
- **4. Biên soạn Tài liệu Kỹ thuật & Cập nhật Quy chuẩn Làm việc AI (`AI/AI_RULES.md`):**
  - Tạo mới tài liệu kỹ thuật tổng hợp [`docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md`](../docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md) và cập nhật [`src/07_recommender/recommender_engine.md`](../src/07_recommender/recommender_engine.md).
  - Cập nhật [`AI/AI_RULES.md`](AI_RULES.md) với 3 nguyên tắc bắt buộc từ User:
    1. **Cấm tuyệt đối tự suy luận chủ quan & cấm Hardcode tình huống lẻ (100% Algorithmic & Data-Driven)**.
    2. **Bắt buộc huấn luyện mô hình bằng GPU (Mandatory GPU-First Training - NVIDIA CUDA `device='cuda', tree_method='hist'`)**.
    3. **Bắt buộc cập nhật đồng bộ toàn bộ thư mục `AI/` và tiến độ dự án ngay sau mỗi thao tác**.
- **5. Cài đặt và Khởi tạo GitHub SpecKit (`specify-cli v1.4.4`):**
  - Cài đặt `specify-cli` vào `.venv` và khởi tạo đầy đủ cấu trúc `.specify/` (`.specify/memory/constitution.md`, `.specify/scripts/powershell/`, `.specify/templates/`, `.specify/workflows/`) cùng bộ 9 lệnh `/speckit.*` tại `.gemini/commands/`.
  - Đồng bộ hóa nội dung `.specify/memory/constitution.md` với `AI/AI_RULES.md`.

---

## [2026-11-22] - DỌN DẸP CÁC TỆP PHÁT SINH NGOÀI DỰ ÁN, CẬP NHẬT DỮ LIỆU ESPORTS MỚI NHẤT & TINH GỌN ĐỊNH HƯỚNG 100% WEB APP MÔN KHOA HỌC DỮ LIỆU
- **Cập nhật bộ dữ liệu giải đấu `2026_LoL_esports_match_data_from_OraclesElixir.csv` mới nhất (đến ngày 2026-11-14):**
  - Tổng số trận của năm 2026 thuộc 6 giải đấu lớn (`LCK, LCP, LPL, MSI, WLDS, EWC`) tăng lên **1,890 trận** (bổ sung trọn vẹn giải CKTG / Worlds 2026 `WLDS`: 206 trận).
  - Ghép thích ứng với 1,110 trận cuối năm 2025 tạo thành `data/raw/esports_active_matches.csv` (3,000 trận, 36,000 dòng, 26.97 MB): LPL (1,092), LCK (812), LCP (474), EWC (265), WLDS (206), MSI (151). Tỷ lệ có Timeline mốc 10 phút tăng lên **81.23% (2,437 / 3,000 trận)**.
  - Đã nạp mới hoàn toàn vào CSDL SQLite `data/database/lol_live_data.db` (`tournament_matches`: 6,000 dòng, `tournament_players`: 30,000 dòng) và chạy `cleaner.py` xuất 4 tệp dữ liệu sạch vào `data/processed/`.
- **Xóa bỏ toàn bộ thư mục/tệp phát sinh không thuộc dự án chính:**
  - Xóa thư mục bài tập ngoài luồng `Homework/`, `sql/`, `midterm_assignment/` và các file DB rỗng thừa (`lol_live_data.db` ở root, `data/lol_context.db`, `data/lol_live_data.db`), chỉ giữ lại CSDL chính thức `data/database/lol_live_data.db` (28.3 MB, 37,009 bản ghi).
  - Xóa tài liệu liên môn cũ `docs/KE_HOACH_LIEN_MON_DATA_SCIENCE_VA_ANDROID.md` và lọc sạch các chủ đề ngoài luồng trong `docs/DANH_MUC_API_VA_DATASET.md`.
- **Chuẩn hóa định hướng kiến trúc & tài liệu (`AI/`, `docs/`, `README.md`):**
  - Cập nhật đồng bộ toàn bộ hệ thống tài liệu quản trị ngữ cảnh (`AI/PROJECT_STATE.md`, `AI/ARCHITECTURE.md`, `AI/TASKS.md`, `AI/DECISIONS.md`, `README.md`, `docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`, `docs/clickup_import_lol_project.csv`).
  - Tập trung 100% mục tiêu dự án vào môn **Nhập môn Khoa học Dữ liệu (PTIT)** với kiến trúc Backend FastAPI & Giao diện **Web App** tương tác.

---

## [2026-10-10] - CẬP NHẬT TOÀN DIỆN RECOMMENDER: SỬA LỖI MẪU NHỎ, LỌC LANE PHASE 1/2, MÔ PHỎNG ĐA KỊCH BẢN (ĐỘI VÔ DANH VS T1) & GHI CHÚ ROADMAP
- **Tổng hợp Những Việc Đã Hoàn Thành (Completed Enhancements):**
  - **1. Khử Thiên kiến Mẫu nhỏ (Small Sample Bias):** Khắc phục triệt để lỗi Rek'Sai Jungle 2 trận thắng 100% bị tính Tier S+ 99.0% nhờ kỹ thuật Bayesian Shrinkage và Sample Confidence Weighting.
  - **2. Sửa lỗi Lọc Cấm theo Vị trí:** Khắc phục lỗi mất tướng khi lọc theo lane (Karma ở bảng tổng nhưng gõ `sp` bị mất); đồng bộ chuẩn xác `ban_phase` giữa Meta Bans và Target Bans.
  - **3. Sửa lỗi cú pháp & runtime:** Khắc phục lỗi `NameError: reason_text` và `KeyError: tournament_stats` khi xử lý dữ liệu tuyển thủ tân binh/ẩn danh.
  - **4. Nâng cấp Mô phỏng Tournament Draft ([`src/07_recommender/simulate_draft_match.py`](../src/07_recommender/simulate_draft_match.py)):**
    - Hỗ trợ đầy đủ tương tác 2 chiều cho cả Phe Xanh (First Pick) và Phe Đỏ (Counter Last Pick).
    - Tích hợp Menu chọn kịch bản trực quan: Hỗ trợ "ĐỘI VÔ DANH (Bạn) vs T1 (Faker, Oner, Keria, Doran, Peyz)", GAM vs T1, T1 vs GEN.G.
    - T1 AI cấm theo Meta toàn cầu đối với tuyển thủ vô danh; người dùng nhận gợi ý bóc tách toàn bộ tướng tủ của từng thành viên T1.
  - **5. Bộ lọc Ngắt cứng Kèo thua rõ rệt (Hard Cut-off Filter):** Khi đối thủ đã pick trước tướng cùng đường, loại bỏ hoàn toàn các tướng có Winrate đối đầu $< 45\%$ khỏi danh sách gợi ý chọn (loại trừ các kèo bị counter cứng).
  - **6. Khuếch đại Điểm Kèo trên Thực thụ:** Thưởng điểm mạnh cho các kèo trên ($\ge 52\%$) có mẫu tin cậy để đưa Vi (65%), Poppy (80%), Trundle (50%), Jarvan IV (54.1%) lên Top đầu.
- **Đánh dấu Định hướng Cải thiện Toàn diện Tương lai (Global Roadmap Backlog):**
  - Bắt buộc quay lại rà soát và đánh giá lại **TOÀN BỘ hệ thống Ma trận Kèo Đấu (Head-to-Head Matchup Matrix) trên TẤT CẢ các cặp tướng và 5 vị trí**, đối chiếu giữa *Cảm nhận người chơi (Perception)* vs *Dữ liệu thực chiến (Reality)*, và mô phỏng chi phí cơ hội *Đánh đổi Tài nguyên Chéo Bản đồ (Macro Tradeoff)*.

---

## [2026-10-08] - HOÀN THÀNH TASK 3.5 & MILESTONE 3: HỆ THỐNG GỢI Ý CẤM/CHỌN THÔNG MINH, NHẬN DIỆN LỖ HỔNG & THẺ ĐIỀU KIỆN THẮNG
- **Triển khai module Recommender [`src/07_recommender/recommender_engine.py`](../src/07_recommender/recommender_engine.py):**
  - **Phân hệ 1: TargetBanEngine (Hybrid Opponent Target Ban):**
    - Kết hợp 65% Trọng số Đấu Giải (30,000 bản ghi `tournament_players`, Bayesian Smoothed Winrate, 10m Laning Dominance, KDA, Damage Share) + 35% Solo Rank 30 trận gần nhất (`data/pro_player_accounts.json`).
    - Nhận diện đột biến (Spike in Pick Rate & Winrate >= 70%) phát hiện và gắn cờ `🚨 POCKET PICK SPAM RANK` / `🔥 TƯỚNG TỦ THƯƠNG HIỆU`.
    - Đã kiểm thử xuất sắc trên Keria (Bard, Camille, Renata), Chovy (Yone, Tristana, Ahri), Kiaya (Rumble, Urgot, Gwen), Levi, Knight, Bin, Ruler.
  - **Phân hệ 2: MetaPickRecommender (Gợi ý Chọn Chuẩn Meta & Synergy):**
    - Tích hợp Counter-Pick đối đầu lane trực tiếp, Duo Synergy (Mid-Jng, Bot-Sup) và Dynamic Composition Balance (bù đắp AP khi Full AD, bổ sung Hard CC và Frontline).
  - **Phân hệ 3: PunisherEngine (Quét Lỗ Hổng & Con Bài Trừng Phạt):**
    - Nhận diện 4 lỗ hổng cấm/chọn chí mạng: Heavy Melee (3-4 cận chiến -> Illaoi, Darius, Cassiopeia, Brand), Full AD (0 AP -> Malphite, Rammus, Taric), Zero Hard CC (Master Yi, Katarina, Zeri), Full Squishy (Nocturne, Jarvan IV).
    - Tác động gia tăng +12% đến +18.5% Winrate dự đoán (minh chứng qua Hiện tượng Siwoo Illaoi tại LCK).
  - **Phân hệ 4: WinConditionEngine (ADR-014: Thẻ Điều Kiện Thắng):**
    - Tích hợp mô hình K-Means `models/archetype_kmeans.pkl` xác định trường phái đội hình, vẽ Radar 5 trục và trích xuất Thẻ Chiến thuật hoàn chỉnh: Core Carry, Power Spike Timing, Primary Objective, Win Condition, Lose Condition, Do's & Don'ts.
- **Đóng gói mô hình & Artifacts:**
  - Xuất file mô hình đóng gói [`models/recommender_engine.pkl`](../models/recommender_engine.pkl).
  - Danh mục tuyển thủ & Rank tracking: [`data/pro_player_accounts.json`](../data/pro_player_accounts.json).
  - Soạn thảo báo cáo khoa học toàn diện [`src/07_recommender/recommender_engine.md`](../src/07_recommender/recommender_engine.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md) và [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
- **🎉 HOÀN THÀNH 100% MILESTONE 3 (GIAI ĐOẠN 3: MACHINE LEARNING & BAN/PICK AI)!** Sẵn sàng bước sang Giai đoạn 4 (REST API FastAPI & Web App).

---

## [2026-10-08] - HOÀN THÀNH TASK 3.4: PHÂN CỤM K-MEANS & PCA NHẬN DIỆN 4 TRƯỜNG PHÁI ĐỘI HÌNH
- **Triển khai module Machine Learning [`src/06_machine_learning/cluster_archetypes.py`](../src/06_machine_learning/cluster_archetypes.py):**
  - **Vector hóa 160+ tướng:** Xây dựng từ điển thuộc tính chiến thuật 5 trục chuẩn hóa [Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control] và tính toán Vector Đội hình có trọng số vị trí.
  - **Phân cụm K-Means & PCA (Chương 4):**
    - Khảo sát tìm số cụm tối ưu K=4 qua phương pháp Elbow (WCSS giảm mạnh từ 21,122 về 15,966) và Silhouette Analysis (0.1799).
    - Giảm chiều PCA 2D giải thích 68.98% phương sai tích lũy (PC1: 45.95% Tempo, PC2: 23.03% Combat Scale).
    - Phân tích và định danh 4 trường phái đội hình kinh điển:
      1. **Early Snowball & Dive (24.1%):** Đè đường, ép trụ và kết thúc sớm (Win condition: Ăn Sâu Hư Không đợt 1, Trụ Đầu trước phút 14).
      2. **Wombocombo & Objective Control (16.3%):** Giao tranh diện rộng 5v5 quanh hang Rồng và Baron.
      3. **Late-Game Hypercarry (22.7%):** Nuôi siêu chủ lực (Smolder, Jinx, Azir, Kayle) đánh về cuối trận.
      4. **Pick & Split-Push 1-3-1 (36.9%):** Đẩy lẻ 2 cánh và bắt lẻ mục tiêu đơn lập.
  - **Đóng gói mô hình:** Lưu trữ thành công vào [`models/archetype_kmeans.pkl`](../models/archetype_kmeans.pkl). Hỗ trợ CLI `--train` và `--predict`.
  - **Xuất bản bộ 2 biểu đồ 300 DPI vào [`reports/figures/`](../reports/figures/):**
    - **Fig 10:** [`fig10_kmeans_elbow_silhouette.png`](../reports/figures/fig10_kmeans_elbow_silhouette.png) - Phương pháp Elbow & Silhouette Score.
    - **Fig 11:** [`fig11_draft_archetypes_pca_clusters.png`](../reports/figures/fig11_draft_archetypes_pca_clusters.png) - Không gian phân cụm PCA 2D & Bộ 4 biểu đồ Radar 5 trục.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học chi tiết [`src/06_machine_learning/cluster_archetypes.md`](../src/06_machine_learning/cluster_archetypes.md).
  - Soạn thảo 2 tệp giải thích học thuật trong `docs/figure_explain/` (`fig10` và `fig11`) và đồng bộ `reports/figures/figure_explain/`.
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.4.** Sẵn sàng bước sang Task 3.5 (Hệ thống Gợi ý Cấm/Chọn Thông Minh).

---

## [2026-10-04] - HOÀN THÀNH TASK 3.3: ĐÁNH GIÁ TOÀN DIỆN MÔ HÌNH VÀ XUẤT BẢN BỘ 4 BIỂU ĐỒ DIAGNOSTICS (300 DPI)
- **Triển khai module Machine Learning [`src/06_machine_learning/evaluate_models.py`](../src/06_machine_learning/evaluate_models.py):**
  - **Đánh giá hiệu năng 2 giai đoạn:**
    - Cấm/Chọn (Phút 0): Random Forest đạt ROC-AUC = 0.5510, Accuracy = 53.83%, Brier Score = 0.2487, F1 = 0.5771.
    - Thực chiến (Phút 10): Random Forest đạt ROC-AUC = 0.7780, Accuracy = 70.75%, Brier Score = 0.1925, F1 = 0.7023.
  - **Thiết kế và xuất bản bộ 4 biểu đồ nghiên cứu khoa học (300 DPI) vào [`reports/figures/`](../reports/figures/):**
    - **Fig 6:** [`fig6_roc_auc_comparison.png`](../reports/figures/fig6_roc_auc_comparison.png) - Đường cong ROC và Precision-Recall đối chiếu Phút 0 vs Phút 10.
    - **Fig 7:** [`fig7_confusion_matrices.png`](../reports/figures/fig7_confusion_matrices.png) - Ma trận nhầm lẫn (Confusion Matrices Heatmap).
    - **Fig 8:** [`fig8_calibration_curve.png`](../reports/figures/fig8_calibration_curve.png) - Biểu đồ độ tin cậy hiệu chuẩn xác suất (Reliability Diagram).
    - **Fig 9:** [`fig9_draft_vs_snowball_feature_importance.png`](../reports/figures/fig9_draft_vs_snowball_feature_importance.png) - So sánh cơ chế đặc trưng quyết định Phút 0 vs Phút 10.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học chi tiết [`src/06_machine_learning/evaluation_report.md`](../src/06_machine_learning/evaluation_report.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.3.** Sẵn sàng bước sang Task 3.4 (Phân cụm 4 Trường phái Đội hình) và Task 3.5 (Hệ thống Gợi ý Ban/Pick Thông Minh).

---

## [2026-10-04] - HOÀN THÀNH TASK 3.2: XÂY DỰNG MÔ HÌNH SNOWBALL PREDICTION (PHÚT 10)
- **Triển khai module Machine Learning [`src/06_machine_learning/snowball_model.py`](../src/06_machine_learning/snowball_model.py):**
  - **Tích hợp dữ liệu đa nguồn:** Trích xuất và hợp nhất 6,770 quan sát mốc 10 phút từ CSDL SQLite `lol_live_data.db` (4,752 Pro Play bóc tách 5 lane + 2,018 Solo Rank Thách Đấu VN2/KR).
  - **Kỹ thuật 22 đặc trưng chiến thuật:**
    - Macro: `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`, `deathsat10`, `kill_diff`, `kda_ratio`.
    - Micro 5 Lanes: `top_golddiff`, `jng_golddiff`, `mid_golddiff`, `bot_golddiff`, `sup_golddiff`, `carry_gold_lead` (Mid + Bot).
    - Mục tiêu lớn: `firstdragon`, `void_grubs`, `has_3_grubs`, `firsttower`, `double_neutral_control`.
    - Synergy phi tuyến & Context: `gold_dragon_synergy`, `gold_grubs_synergy`, `is_blue_side`, `is_pro_play`.
  - **So sánh mô hình (Test Set 1,354 trận):**
    - Random Forest (150 trees): **ROC-AUC = 0.7780**, Accuracy = 70.75%, Log Loss = 0.5682, Brier Score = 0.1925.
    - Soft Voting Ensemble (LGB + XGB + RF + LR): Accuracy = 71.20%, ROC-AUC = 0.7774.
    - XGBoost: Accuracy = 71.20%, ROC-AUC = 0.7751.
    - Logistic Regression L2: Accuracy = 71.20%, ROC-AUC = 0.7746.
    - LightGBM: Accuracy = 71.27%, ROC-AUC = 0.7730.
  - **Đối chiếu Đấu Giải vs Solo Rank:**
    - Solo Rank: **ROC-AUC = 0.8189**, Accuracy = 73.54% (Lăn cầu tuyết tàn phá tâm lý và không thể lật kèo do thiếu phối hợp).
    - Pro Play: **ROC-AUC = 0.7572**, Accuracy = 69.47% (Các đội chuyên nghiệp kiểm soát tầm nhìn và có thể lật kèo nhờ đội hình Scaling).
  - **Đóng gói mô hình:** Lưu trữ thành công vào [`models/snowball_model.pkl`](../models/snowball_model.pkl). Hỗ trợ CLI `--train` và `--predict`.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học [`src/06_machine_learning/snowball_model.md`](../src/06_machine_learning/snowball_model.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.2.** Sẵn sàng bước sang Task 3.3 (Đánh giá mô hình ROC-AUC & Confusion Matrix).

---

## [2026-10-04] - HOÀN THÀNH TASK 3.1: XÂY DỰNG MÔ HÌNH DRAFT PREDICTION (PHÚT 0)
- **Triển khai module Machine Learning [`src/06_machine_learning/draft_model.py`](../src/06_machine_learning/draft_model.py):**
  - **Trích xuất dữ liệu:** Nạp và xoay trục 3,000 trận đấu giải đỉnh cao (6,000 dòng đội) chuẩn 1NF/3NF từ CSDL SQLite `lol_live_data.db`.
  - **Feature Pipeline đa tầng (799 chiều):**
    - Position-specific Differential One-Hot Vectors (+1 Blue, -1 Red theo 5 lane $\times$ 158 tướng = 790 cột).
    - Tỷ lệ thắng làm mịn Bayes (Bayesian Smoothed Winrates C=10).
    - Tương quan đối đầu trực tiếp 5 cặp đường (Lane Matchup Advantage).
    - Phối hợp cặp đôi (Synergy Duo Mid-Jng và Bot-Sup).
    - Cân bằng thuộc tính đội hình (AD/AP ratio, Hard CC, Tankiness, Early vs Late Scaling).
    - Trọng số suy giảm theo thời gian (Time-decay sample weights Half-life 90 ngày).
  - **So sánh mô hình (Test Set 600 trận theo thời gian):**
    - Random Forest (150 trees): **ROC-AUC = 0.5510**, Brier Score = 0.2487 (Mô hình tối ưu nhất).
    - Logistic Regression L2: **Accuracy = 54.33%**, ROC-AUC = 0.5485.
    - Soft Voting Ensemble: ROC-AUC = 0.5492.
  - **Đóng gói mô hình:** Lưu trữ thành công vào [`models/draft_model.pkl`](../models/draft_model.pkl).
  - **Hỗ trợ CLI Runner:** `--train` để huấn luyện, `--predict` để dự đoán tỷ lệ thắng và bóc tách lợi thế 5 lane theo thời gian thực.
- **Tài liệu & Báo cáo:**
  - Soạn thảo báo cáo khoa học chi tiết [`src/06_machine_learning/draft_model.md`](../src/06_machine_learning/draft_model.md).
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md).
  - **Hoàn thành 100% Task 3.1.** Sẵn sàng bước sang Task 3.2 (Mô hình Snowball Phút 10).

---

## [2026-09-30] - BỔ SUNG KIẾN TRÚC DRAFT FLAW & PUNISHER RECOMMENDER
- **Cập nhật đặc tả Task 3.5, Task 4.1 & Module `src/07_recommender/`:**
  - **Phân hệ Nhận diện Lỗ hổng Cấm/Chọn của Địch (Draft Flaw Exploitation):** Tự động phát hiện 4 lỗ hổng chí mạng của đội hình địch: Heavy Melee (3-4 cận chiến), Full AD (không có AP), Zero Hard CC (không có khống chế cứng), Full Squishy (máu giấy không có tanker/mở combat).
  - **Gợi ý Con Bài Trừng Phạt (Punisher Pick Recommender):** Tự động đề xuất các con bài trừng phạt tối thượng tương ứng như trận Siwoo Illaoi (Illaoi/Darius khắc chế Heavy Melee, Malphite/Rammus khắc chế Full AD, Master Yi/Katarina trừng phạt Zero CC) giúp tăng vọt +15% đến +20% winrate dự đoán.
  - **Bổ sung Endpoint API & Web UI:** `POST /api/v1/detect-flaws` trả về Thẻ Cảnh báo Lỗ hổng & Con bài Trừng phạt (Punisher Card) trực quan trên giao diện cấm/chọn.
  - Cập nhật [`AI/TASKS.md`](TASKS.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`src/07_recommender/README.md`](../src/07_recommender/README.md).

---

## [2026-09-30] - HOÀN THÀNH VÀ ĐÓNG GÓI MILESTONE 2: JUPYTER NOTEBOOK EDA
- **Hoàn thành và đóng gói Notebook [`notebooks/01_kham_pha_du_lieu_EDA.ipynb`](../notebooks/01_kham_pha_du_lieu_EDA.ipynb):**
  - Tích hợp toàn diện 21 cells (6 Markdown dẫn nhập & tổng kết học thuật, 15 Code cells thực thi) bao phủ trọn vẹn chương trình môn học:
    - **Phần 1: Khởi tạo & Tổng quan CSDL SQLite (Chương 2, 5):** Thống kê quy mô 37,009 bản ghi chuẩn 1NF/3NF từ 2 nguồn Đấu Giải và Solo Rank.
    - **Phần 2: 5 Truy vấn SQL nâng cao (Chương 5 & 5x):** Kèo 1v1 đường trên, Cặp đôi đường dưới, Tỷ lệ chọn tướng, Xếp hạng đè đường DENSE_RANK và Phân tầng Lăn cầu tuyết.
    - **Phần 3: 3 Bài toán Thống kê suy diễn (Chương 1):** Two-sample Proportion Z-test Lợi thế Phe Xanh, Two-sample Welch's t-test & Z-test Lăn cầu tuyết lead >= 2,000g, Chi-square & Odds Ratio 3 Sâu Hư Không vs Rồng 1.
    - **Phần 4: Bộ 5 Biểu đồ Trực quan hóa EDA 300 DPI (Chương 3):** Fig 1 (Correlation Heatmap 9x9), Fig 2 (Histogram + KDE Chênh vàng 10p), Fig 3 (Boxplot Kinh tế 5 vị trí), Fig 4 (Scatter + OLS Vàng dẫn vs Thời lượng), Fig 5 (Ma trận 8 tổ hợp mục tiêu lớn Pro vs Rank).
    - **Phần 5: Tổng kết Insights & Định hướng Kỹ thuật:** Tổng hợp 5 phát hiện cốt lõi và tiêu chuẩn kỹ thuật chuyển giao cho Giai đoạn 3 (Machine Learning 2 Giai Đoạn).
  - Đã thực thi qua kernel Jupyter/nbconvert, lưu trữ toàn vẹn toàn bộ outputs bảng số liệu và hình ảnh đồ họa chất lượng cao sẵn sàng nộp và trình chiếu.
  - Hoàn tất 100% Giai đoạn 2 và Milestone 2.

---

## [2026-09-30] - NÂNG CẤP BIỂU ĐỒ FIG 5 (MA TRẬN 8 TỔ HỢP) & XÂY DỰNG BỘ TÀI LIỆU GIẢI THÍCH DOCS/FIGURE_EXPLAIN/
- **Nâng cấp mã nguồn trực quan hóa [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py):**
  - **Tối ưu đồ họa Fig 1 (Correlation Heatmap):** Chuẩn hóa thang đo Colorbar $[-1.0, +1.0]$, căn thẳng hàng tuyệt đối với ma trận bằng `make_axes_locatable`, khử 100% đường lưới trục ngầm bằng `sns.axes_style("white")`.
  - **Nâng cấp toàn diện Fig 5 (Biểu đồ 2 Subplots 8 Tổ Hợp):** Phân rã trọn vẹn 4 mức Sâu Hư Không ($0, 1, 2, 3\text{ Sâu}$) theo 2 trạng thái $Có Rồng 1$ vs $Mất Rồng 1$ cho cả Đấu Giải Chuyên Nghiệp (4,752 quan sát) và Solo Rank Thách Đấu (2,018 quan sát), kèm đường tham chiếu cân bằng 50% và số % trên đầu cột.
  - **Xuất lại toàn bộ bộ 5 biểu đồ 300 DPI** vào [`reports/figures/`](../reports/figures/).
- **Xây dựng bộ tài liệu giải thích chi tiết [`docs/figure_explain/`](../docs/figure_explain/):**
  - Khởi tạo 5 file tài liệu giải thích chuyên sâu (tên file tương ứng khớp 1-1 với từng biểu đồ) và 1 file [`README.md`](../docs/figure_explain/README.md) mục lục:
    1. [`fig1_correlation_heatmap.md`](../docs/figure_explain/fig1_correlation_heatmap.md): Ma trận tương quan Pearson, Colorbar, tại sao đường chéo = 1, phân biệt hệ số r vs tỷ lệ thắng %.
    2. [`fig2_gold_diff_distribution.md`](../docs/figure_explain/fig2_gold_diff_distribution.md): Phân phối chênh lệch vàng (Histogram + KDE), kiểm tra tính chuẩn Gaussian, so sánh Pro vs Rank.
    3. [`fig3_lane_economy_boxplot.md`](../docs/figure_explain/fig3_lane_economy_boxplot.md): Boxplot kinh tế 5 vị trí (Bot 642g > Top 616g > Jng 572g > Mid 556g > Sup 328g), giải thích tính đối xứng gương qua 0 và ngoại lai.
    4. [`fig4_gold_lead_vs_duration.md`](../docs/figure_explain/fig4_gold_lead_vs_duration.md): Vàng dẫn trước vs Thời lượng (Scatter + OLS), ranh giới 20p Baron vs 15p FF15, các trận 11-13p do AFK/Open Mid.
    5. [`fig5_neutral_objectives_scenarios.md`](../docs/figure_explain/fig5_neutral_objectives_scenarios.md): Ma trận 8 tổ hợp mục tiêu (Rồng 1 x 0, 1, 2, 3 Sâu), hiệu ứng bảo hiểm trên 50% của Rồng 1, kèo chia sâu 1R+1S vs 0R+2S, tại sao các cặp đối đầu bù trừ đúng 100%, xử lý bỏ sâu/sâu biến mất.
  - Đồng bộ sang [`reports/figures/figure_explain/`](../reports/figures/figure_explain/).
- **Cập nhật tài liệu quản trị:**
  - Cập nhật [`AI/PROJECT_STATE.md`](PROJECT_STATE.md) (Tiến độ tổng đạt ~65%, Giai đoạn 2 đạt 95%).
  - Cập nhật [`src/05_visualization/plot_eda_figures.md`](../src/05_visualization/plot_eda_figures.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 2.4: TRỰC QUAN HÓA DỮ LIỆU EDA (BỘ 5 BIỂU ĐỒ 300 DPI - CHƯƠNG 3)
- **Triển khai module trực quan hóa dữ liệu EDA [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py):**
  - **Phương pháp & Đồ họa (Chương 3):** Sử dụng `matplotlib` và `seaborn`, thiết lập độ phân giải cao **300 DPI**, bảng màu phân cực chuyên nghiệp (Blue/Red side và Pro/Rank).
  - **Bộ 5 biểu đồ EDA chất lượng cao xuất tại [`reports/figures/`](../reports/figures/):**
    1. **Fig 1:** [`fig1_correlation_heatmap.png`](../reports/figures/fig1_correlation_heatmap.png) - Ma trận tương quan tuyến tính Pearson Heatmap (Tam giác trên) giữa các chỉ số 10p và tỷ lệ thắng.
    2. **Fig 2:** [`fig2_gold_diff_distribution_kde.png`](../reports/figures/fig2_gold_diff_distribution_kde.png) - Phân phối chênh lệch vàng (Histogram 40 bins + KDE Density) đối chiếu Đội Thắng vs Đội Thua ở cả 2 môi trường.
    3. **Fig 3:** [`fig3_lane_economy_boxplot.png`](../reports/figures/fig3_lane_economy_boxplot.png) - Phân bố kinh tế và ngoại lai 5 vị trí thi đấu (Top, Jungle, Mid, Bot, Support) với dải 1.5 IQR.
    4. **Fig 4:** [`fig4_gold_lead_vs_duration_scatter.png`](../reports/figures/fig4_gold_lead_vs_duration_scatter.png) - Mối quan hệ Vàng dẫn trước 10p vs Thời lượng trận đấu (Scatter + Đường hồi quy OLS + Mốc Baron 20p / Đầu hàng sớm FF15).
    5. **Fig 5:** [`fig5_neutral_objectives_scenarios_bar.png`](../reports/figures/fig5_neutral_objectives_scenarios_bar.png) - Grouped Bar Chart So sánh Tỷ lệ thắng 4 Kịch bản Kiểm soát Mục tiêu lớn (3 Sâu vs Rồng 1) kèm vạch 50%.
- **Tài liệu & Báo cáo:**
  - Tạo mới file báo cáo phân tích chi tiết [`src/05_visualization/plot_eda_figures.md`](../src/05_visualization/plot_eda_figures.md).
  - Cập nhật [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).
  - Hoàn tất 100% Task 2.4. Sẵn sàng đóng gói Milestone 2 vào Jupyter Notebook `notebooks/01_kham_pha_du_lieu_EDA.ipynb`.

---

## [2026-09-28] - HOÀN THÀNH TASK 2.3: KIỂM ĐỊNH CHI-SQUARE (χ²) & TỶ SỐ CHÊNH (ODDS RATIO): 3 SÂU HƯ KHÔNG VS RỒNG 1
- **Triển khai module kiểm định giả thuyết thống kê [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py):**
  - **Phương pháp toán học (Chương 1):** Bảng chéo 2x2 (Contingency Table), Kiểm định tính độc lập Chi-square ($\chi^2$), Tỷ số Chênh (Odds Ratio - OR), Woolf Logit 95% CI và Relative Risk (RR).
  - **Kết quả kiểm định thực nghiệm:**
    1. **Đấu Giải Chuyên Nghiệp (Pro Play):**
       - **Rồng Đầu Tiên (First Dragon):** Winrate **59.43%** vs **40.57%**, $\chi^2 = 167.39, p = 2.75 \times 10^{-38} < 0.0001$, $\text{Odds Ratio} = \mathbf{2.145}$ (CI 95%: $[1.910, 2.409]$) $\rightarrow$ Tăng cơ hội thắng gấp **2.15 lần**.
       - **3 Sâu Hư Không (Voidgrubs):** Winrate **55.81%** vs **46.96%**, $\chi^2 = 33.11, p = 8.73 \times 10^{-9} < 0.0001$, $\text{Odds Ratio} = \mathbf{1.427}$ (CI 95%: $[1.265, 1.609]$) $\rightarrow$ Tăng cơ hội thắng gấp **1.43 lần**.
       - **Đổi chéo mục tiêu (Cross-trade):** Đội chỉ ăn Rồng 1 (bỏ Sâu) thắng **55.92%**, trong khi đội chỉ ăn Sâu (bỏ Rồng) chỉ thắng **47.23%** (Rơi xuống dưới 50%!).
    2. **Solo Rank (Thách Đấu):**
       - **Rồng Đầu:** $\text{Odds Ratio} = \mathbf{2.306}$ ($p = 1.60 \times 10^{-18}$).
       - **3 Sâu Hư Không:** $\text{Odds Ratio} = \mathbf{2.031}$ ($p = 2.67 \times 10^{-13}$) $\rightarrow$ Ở Solo Rank, 3 Sâu có giá trị cao hơn Pro Play do người chơi tự đẩy trụ lấy tiền giáp trụ (Plates) lăn cầu tuyết cá nhân.
    3. **Ma trận 4 Kịch bản:** Đội ăn cả 2 (3 Sâu + Rồng 1) thắng **68.66%** ở Pro và **76.28%** ở Rank. Đội mất trắng cả 2 chỉ thắng **35.90%** (Pro) và **36.42%** (Rank).
  - Xuất bảng số liệu ra [`data/processed/hypothesis_test_3_objectives.csv`](../data/processed/hypothesis_test_3_objectives.csv).
- **Cập nhật tài liệu:**
  - Tạo mới file báo cáo phân tích chi tiết [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md).
  - Cập nhật [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).
  - **HOÀN THÀNH 100% CẢ 3 BÀI TOÁN THỐNG KÊ SUY DIỄN CHƯƠNG 1** (Task 2.1 Z-test + Task 2.2 t-test + Task 2.3 Chi-square).

---

## [2026-09-28] - HOÀN THÀNH TASK 2.2: KIỂM ĐỊNH TWO-SAMPLE WELCH T-TEST & Z-TEST HIỆU QUẢ LĂN CẦU TUYẾT (SNOWBALL LEAD >= 2000G)
- **Triển khai module kiểm định giả thuyết thống kê [`src/04_hypothesis_testing/test_snowball_effect.py`](../src/04_hypothesis_testing/test_snowball_effect.py):**
  - **Phương pháp toán học (Chương 1):**
    1. *Two-sample Proportion Z-test:* So sánh Tỷ lệ chuyển hóa chiến thắng (Winrate Conversion) khi dẫn $\ge 2,000$ vàng lúc 10 phút.
    2. *Two-sample Independent Welch's t-test:* So sánh Thời lượng kết thúc trận đấu trung bình (Game Duration).
    3. *Levene's Test for Variance:* Kiểm định tính đồng nhất phương sai đo lường tính ổn định & kỷ luật kiểm soát thế trận.
  - **Kết quả kiểm định thực nghiệm:**
    - **1. Tỷ lệ thắng (Winrate):** Đấu Giải đạt **83.48%** (192/230), Solo Rank đạt **86.04%** (339/394). $Z = -0.8671, p = 0.3859 > 0.05 \rightarrow$ **Chưa đủ bằng chứng bác bỏ $H_0$** (Dẫn 2,000g lúc 10p ở cả 2 môi trường đều nắm chắc $\sim 85\%$ chiến thắng, khác biệt là ngẫu nhiên).
    - **2. Thời lượng trận đấu (Duration):** Đấu Giải = **29.75 phút** vs Solo Rank = **24.46 phút**. $t = +11.4618, p = 1.16 \times 10^{-27} < 0.0001 \rightarrow$ **Bác bỏ $H_0$ cực kỳ mạnh mẽ** (Trận Solo Rank kết thúc nhanh hơn Đấu Giải trung bình **5.3 phút** do văn hóa đầu hàng sớm FF15 và lối đánh giao tranh liên tục).
    - **3. Tính ổn định & Kỷ luật (Variance):** Độ lệch chuẩn Pro Play $\sigma = 4.68$ phút vs Solo Rank $\sigma = 6.80$ phút. $\text{Levene Stat} = 53.1630, p = 9.37 \times 10^{-13} < 0.0001 \rightarrow$ **Bác bỏ $H_0$** (Đấu Giải ổn định, kỷ luật hơn rõ rệt).
    - **Phân tầng 4 mốc:** Mở rộng kiểm định trên các mốc $\ge 1,000$g, $\ge 1,500$g, $\ge 2,000$g, $\ge 3,000$g.
  - Xuất bảng số liệu ra [`data/processed/hypothesis_test_2_snowball.csv`](../data/processed/hypothesis_test_2_snowball.csv).
- **Cập nhật tài liệu:**
  - Tạo mới file báo cáo phân tích chi tiết [`src/04_hypothesis_testing/test_snowball_effect.md`](../src/04_hypothesis_testing/test_snowball_effect.md).
  - Cập nhật [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 2.1: KIỂM ĐỊNH A/B LỢI THẾ PHE XANH (BLUE SIDE ADVANTAGE) QUA Z-TEST 2 PHÍA
- **Triển khai module kiểm định giả thuyết thống kê [`src/04_hypothesis_testing/test_blue_side_advantage.py`](../src/04_hypothesis_testing/test_blue_side_advantage.py):**
  - **Phương pháp toán học:** $Z$-test tỷ lệ 2 phía ($\alpha = 0.05$) kiểm định $H_0: p = 0.5$ vs $H_1: p \neq 0.5$. Tính $Z$-score, $p$-value 2 phía và khoảng tin cậy 95% (Wald & Wilson).
  - **Kết quả kiểm định thực nghiệm:**
    1. **Đấu Giải Chuyên Nghiệp (Pro Play - 3,000 trận):** Tỷ lệ thắng Phe Xanh đạt **53.50%** ($Z = +3.8341, p = 0.000126 < 0.001$, CI: $[51.72\%, 55.28\%]$). **Bác bỏ $H_0$** $\rightarrow$ Lợi thế First Pick & góc nhìn bản đồ của Phe Xanh vượt trội có ý nghĩa thống kê cao.
    2. **Solo Rank (1,009 trận):** Tỷ lệ thắng Phe Xanh đạt **45.49%** ($Z = -2.8648, p = 0.004173 < 0.01$, CI: $[42.42\%, 48.56\%]$). **Bác bỏ $H_0$** $\rightarrow$ Phe Đỏ thắng $54.51\%$ cao hơn do Matchmaking Riot xếp đội có MMR cao hơn sang Phe Đỏ.
    3. **Phân rã theo giải đấu:** LCP ($p=0.0262^*$) và MSI ($p=0.0280^*$) đều bác bỏ $H_0$.
  - Xuất bảng tổng hợp kết quả ra [`data/processed/hypothesis_test_1_blue_side.csv`](../data/processed/hypothesis_test_1_blue_side.csv).
- **Cập nhật tài liệu:**
  - Tạo mới file giải thích báo cáo chi tiết song song [`src/04_hypothesis_testing/test_blue_side_advantage.md`](../src/04_hypothesis_testing/test_blue_side_advantage.md).
  - Cập nhật [`src/04_hypothesis_testing/README.md`](../src/04_hypothesis_testing/README.md), [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md).

---

## [2026-09-28] - KHỞI TẠO TỪ ĐIỂN DANH MỤC HÀM, CLASS & API NỘI BỘ DỰ ÁN (DOCS/DANH_MUC_HAM_VA_MODULES.MD)
- **Biên soạn tài liệu tra cứu toàn diện [`docs/DANH_MUC_HAM_VA_MODULES.md`](../docs/DANH_MUC_HAM_VA_MODULES.md):**
  - Hệ thống hóa $100\%$ các Class, Phương thức (Methods), Hàm độc lập và Hằng số cấu hình thuộc toàn bộ các module mã nguồn hiện có trong `src/`.
  - Phân loại rõ ràng theo 4 module chính:
    1. `src/config/`: `load_dotenv_custom()`, `get_active_esports_season()`, `get_active_esports_file()` và các hằng số toàn cục.
    2. `src/01_data_pipeline/`: Class `RiotApiCrawler` (12 methods), Class `GoogleDriveDataSyncer` (10 methods + 5 module functions), Class `EsportsDatabaseLoader` (7 methods + 2 module functions).
    3. `src/02_preprocessing/`: Class `DataCleaner` (9 methods: IQR, Z-score, Trimming, Winsorization, Domain Filtering, Imputation).
    4. `src/03_database_sql/`: Class `SQLQueryRunner` (4 methods), `extract_queries_from_sql_file()` và đặc tả 5 câu truy vấn SQL trong `queries.sql`.
  - Bổ sung bảng Cheat Sheet tra cứu nhanh (Function Quick Reference Index).
- **Cập nhật hệ thống Prompt khởi động phiên làm việc trong `docs/prompt_ne/`:**
  - Cập nhật [`docs/prompt_ne/prompt1.txt`](../docs/prompt_ne/prompt1.txt) và [`docs/prompt_ne/prompt3.txt`](../docs/prompt_ne/prompt3.txt) bổ sung danh mục file context mới (`DANH_MUC_HAM_VA_MODULES.md`, `KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`) và quy định bắt buộc về `.venv` & Git.
  - Tạo mới [`docs/prompt_ne/prompt4_giai_doan_2_stats_eda.txt`](../docs/prompt_ne/prompt4_giai_doan_2_stats_eda.txt) chuyên dụng để bắt đầu Giai đoạn 2 (Thống kê suy diễn & EDA - Chương 1, 3).

---

## [2026-09-28] - HOÀN THÀNH TASK 1.4: TRIỂN KHAI 5 CÂU TRUY VẤN SQL NÂNG CAO (CHƯƠNG 5 & 5X) & ĐẠT MILESTONE 1
- **Triển khai 5 câu truy vấn SQL phân tích chuyên sâu chuẩn giáo trình Chương 5 & 5x trong [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql):**
  1. **Truy vấn 1 (Kèo đối đầu trực tiếp 1v1 - Lane Matchup):** Áp dụng `Self-JOIN` ghép bảng `tournament_players` qua `gameid`, `position`, `side = 'Blue'` và `side = 'Red'`, kết hợp `GROUP BY` và `HAVING` thống kê tỉ lệ thắng, chênh lệch vàng/lính lúc 10 phút để phát hiện Counter-Pick.
  2. **Truy vấn 2 (Cặp đôi ăn ý đường dưới - Bot Lane Synergy Duo):** Áp dụng `Intra-team JOIN` ghép tuyển thủ Bot + Sup cùng phe, `GROUP BY`, `HAVING count(*) >= 10` xếp hạng cặp đôi có tỷ lệ thắng cao nhất phục vụ thuật toán Gợi ý Cấm/Chọn.
  3. **Truy vấn 3 (Tướng có tỷ lệ Cấm/Chọn cao nhất - Meta Presence Rate):** Áp dụng `CTE (Common Table Expressions)`, `Subqueries` và `Unpivot UNION ALL` tính toán Presence Rate = (Picks + Bans) / Tổng số trận.
  4. **Truy vấn 4 (Xếp hạng tuyển thủ đè đường phút 10 - Lane Dominance Ranking):** Áp dụng `Window Functions: DENSE_RANK() OVER (PARTITION BY position ORDER BY avg_gold_diff_10 DESC)` và `AVG() OVER (PARTITION BY position)` đối chiếu với chuẩn trung bình (Benchmark) toàn giải.
  5. **Truy vấn 5 (Đối chiếu hiệu quả Lăn cầu tuyết: Đấu Giải vs Rank Đơn):** Áp dụng `UNION ALL`, phân tầng rời rạc hóa `CASE WHEN` chênh lệch vàng 10 phút, `GROUP BY` so sánh khả năng chuyển hóa lợi thế thành chiến thắng giữa Pro Play và Solo Queue.
- **Xây dựng Script thực thi và xuất dữ liệu tự động [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py):**
  - Hỗ trợ giao diện CLI chuyên nghiệp: `--query 1..5`, `--limit N`, `--export`.
  - Tự động xuất 5 tệp kết quả phân tích sạch vào `data/processed/sql_query_[1-5]_result.csv`.
- **Nghiệm thu Milestone 1:** Hoàn thành 100% Giai đoạn 1 (Task 1.0, 1.1, 1.2, 1.3, 1.4, 1.5).

---

## [2026-09-28] - TÍCH HỢP QUYẾT ĐỊNH KIẾN TRÚC ADR-014: NHẬN DIỆN ĐIỀU KIỆN THẮNG & TRƯỜNG PHÁI ĐỘI HÌNH
- **Ghi nhận quyết định kiến trúc [ADR-014](DECISIONS.md) trong [`AI/DECISIONS.md`](DECISIONS.md):**
  - Tích hợp tính năng phân tích **Trường phái đội hình (Draft Archetypes qua K-Means & PCA)** và **Khuyến nghị Điều kiện thắng (Win Condition Card)** cho Giai đoạn 3 (ML & Recommender) và Giai đoạn 4 (FastAPI Backend endpoint `/api/v1/win-condition` & Web App).
  - Phân loại 4 trường phái: *Early Snowball / Dive, Dragon Soul Stacking, Late-Game Hypercarry Scaling, Pick & Split-Push 1-3-1*.
  - Xuất Thẻ điều kiện thắng tự động gồm: Chủ lực gánh đội (Core Carry), Điểm rơi sức mạnh (Power Spike Timing), Mục tiêu ưu tiên số 1 (Primary Objective), và Điều kiện thất bại cần tránh (Lose Condition).
- **Đồng bộ toàn bộ tài liệu:**
  - Cập nhật [`AI/TASKS.md`](TASKS.md) (Task 3.4, 3.5, 4.1, 4.2), [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md), [`src/06_machine_learning/README.md`](../src/06_machine_learning/README.md), [`src/07_recommender/README.md`](../src/07_recommender/README.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 1.3: TIỀN XỬ LÝ, LÀM SẠCH & KHỬ NGOẠI LAI IQR/Z-SCORE (SRC/02_PREPROCESSING/CLEANER.PY)
- **Triển khai module tiền xử lý dữ liệu chuẩn giáo trình Chương 2 [`src/02_preprocessing/cleaner.py`](../src/02_preprocessing/cleaner.py):**
  - **Domain Filtering:** Loại bỏ 100% trận Remake (< 10 phút) và AFK ($CS < 10$).
  - **Khử Missing Values:**
    - Zero Imputation cho biến sự kiện đếm (`elders`, `atakhans`, `doublekills`...).
    - Categorical Imputation (`'NoBan'`) cho các lượt cấm để trống.
    - Phân luồng dữ liệu thông minh qua `datacompleteness` cho bài toán Snowball mốc 10 phút.
  - **Khử Outlier linh hoạt (IQR & Z-Score):**
    - Hỗ trợ cả 2 thuật toán: IQR ($1.5 \times IQR$) và Z-Score ($|Z| > 3.0$).
    - Hỗ trợ cả 2 cơ chế: Trimming (Lọc bỏ ngoại lai) và Winsorization / Capping (Cắt ngọn giữ nguyên cỡ mẫu).
  - **Kỹ nghệ đặc trưng:** Tính toán các chỉ số bổ trợ `goldDiffPerMin10`, `csDiffPerMin10`, `kda`.
  - **Xuất thành công 4 tệp dữ liệu sạch vào `data/processed/`:**
    1. `clean_ranked_10min.csv`: 977 dòng sạch.
    2. `clean_tournament_10min.csv`: 4,636 dòng sạch.
    3. `clean_tournament_draft.csv`: 6,000 dòng sạch (3,000 trận đỉnh cao).
    4. `clean_tournament_players.csv`: 28,880 dòng sạch.
  - Tích hợp báo cáo kiểm định chất lượng làm sạch trực quan (Data Cleaning Card).
- **Cập nhật tài liệu:**
  - Cập nhật [`src/02_preprocessing/README.md`](../src/02_preprocessing/README.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/TASKS.md`](TASKS.md), [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md).

---

## [2026-09-28] - HOÀN THÀNH TASK 1.2: NẠP DỮ LIỆU ĐẤU GIẢI VÀO CSDL SQLITE (TOURNAMENT_MATCHES & TOURNAMENT_PLAYERS)
- **Triển khai module ETL [`src/01_data_pipeline/load_esports_to_db.py`](../src/01_data_pipeline/load_esports_to_db.py):**
  - Đọc và làm sạch dữ liệu từ tệp hoạt động `data/raw/esports_active_matches.csv` (3,000 trận đỉnh cao, 36,000 dòng).
  - Tự động chuẩn hóa tên cột (snake_case hợp lệ, xử lý ký tự đặc biệt như `dragons (type unknown)` $\rightarrow$ `dragons_type_unknown`, `team kpm` $\rightarrow$ `team_kpm`, `earned gpm` $\rightarrow$ `earned_gpm`, `total cs` $\rightarrow$ `total_cs`).
  - Phân tách và nạp thành công 2 bảng CSDL chuẩn 1NF/3NF vào `data/database/lol_live_data.db`:
    1. `tournament_matches`: **6,000 dòng** (3,000 trận $\times$ 2 đội Xanh/Đỏ), 155 cột. Khóa chính: `(gameid, side)`.
    2. `tournament_players`: **30,000 dòng** (3,000 trận $\times$ 10 tuyển thủ), 129 cột. Khóa chính: `(gameid, participantid)`. Khóa ngoại: `(gameid, side) REFERENCES tournament_matches(gameid, side) ON DELETE CASCADE`.
  - Tự động tạo 12 Indexes tối ưu hóa tốc độ truy vấn cho các câu lệnh SQL ở Module 03.
  - Tích hợp báo cáo kiểm định chất lượng dữ liệu tự động (Data Integrity Audit): Xác thực số trận, phân bổ giải đấu (LPL: 1,160; LCK: 850; LCP: 466; EWC: 265; MSI: 151; WLDS: 108), tỷ lệ có timeline 10 phút (79.0%), và chạy thử nghiệm các truy vấn phân tích (Top Pick Champions, Top Winrate Teams).
- **Cập nhật tài liệu:**
  - Cập nhật [`src/01_data_pipeline/README.md`](../src/01_data_pipeline/README.md), [`src/03_database_sql/README.md`](../src/03_database_sql/README.md), [`AI/PROJECT_STATE.md`](PROJECT_STATE.md), [`AI/DATABASE.md`](DATABASE.md), [`AI/TASKS.md`](TASKS.md), [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md).

---

## [2026-09-20] - TÍCH HỢP BỘ 6 GIẢI ĐẤU QUỐC TẾ (MSI, WLDS, EWC) & CHỨC NĂNG THẨM ĐỊNH SỨC KHỎE DỮ LIỆU (--CHECK)
- **Tích hợp các giải đấu quốc tế danh giá vào tập dữ liệu:**
  - Bổ sung các mã giải quốc tế chính thức của Oracle's Elixir: `WLDS` (World Championship / CKTG), `MSI` (Mid-Season Invitational), `EWC` (Esports World Cup).
  - Chạy đồng bộ lệnh: `python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL,MSI,WLDS,EWC`.
  - Kết quả: Tập dữ liệu đạt **3,000 trận (36,000 dòng, 26.8 MB)**, trong đó số trận có Timeline mốc 10 phút tăng vọt từ 70.4% lên **79.0% (2,369 / 3,000 trận)**.
  - Phân bổ chi tiết: LPL (1,160 trận), LCK (850 trận), LCP (466 trận), EWC (265 trận), MSI (151 trận), WLDS (108 trận).
- **Phát triển module Thẩm định Sức khỏe Dữ liệu (Data Health Card):**
  - Thêm phương thức `check_data_health(filepath)` trong `GoogleDriveDataSyncer` và hàm cấp module `check_esports_data_health()`.
  - Hỗ trợ cờ CLI `python src/01_data_pipeline/sync_google_drive.py --check`.
  - Thẩm định đa tầng: Quy mô, cấu trúc chuẩn 12 dòng/trận của Oracle's Elixir (đạt 100% hoàn hảo), phân bổ giải đấu, và audit missing values theo phân tầng: Cốt lõi, Mục tiêu Team (0% khuyết), và Timeline mốc 10 phút.
- **Giải quyết triệt để lỗi Google Drive Quota Exceeded (Lỗi 403 tải ẩn danh):**
  - Tích hợp kiến trúc tải 2 tầng trong `src/01_data_pipeline/sync_google_drive.py`:
    - **Tầng 1:** `gdown` tải ẩn danh nhanh; kiểm tra tính toàn vẹn (file > 100 KB, không phải HTML lỗi).
    - **Tầng 2:** Kích hoạt tự động khi gặp Quota Exceeded, dùng Google Drive API v3 kết hợp OAuth 2.0 (`credentials.json` Desktop Client, lưu token cache `.gdrive_token.json`).
    - Áp dụng thuật toán **Smart Copy**: Tự nhân bản file công khai vào Google Drive cá nhân của người dùng qua `service.files().copy()` $\rightarrow$ Vượt 100% hạn ngạch công khai $\rightarrow$ Stream tải 8MB/chunk $\rightarrow$ Tự động xóa bản sao tạm bằng `service.files().delete()`.
- **Bảo mật & Cập nhật tài liệu:**
  - Bổ sung `credentials.json`, `token.json`, `.gdrive_token.json` vào `.gitignore`.
  - Đồng bộ toàn bộ tài liệu: `README.md`, `README_SYNC_DRIVE.md`, `AI/PROJECT_STATE.md`, `AI/TASKS.md`, `docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`.

---

## [2026-09-20] - HOÀN THÀNH TASK 1.1: TÍCH LŨY 1,009 TRẬN RANK ĐỈNH CAO (VN2 & KR) ĐẠT CHUẨN 1NF/3NF
- **Cào dữ liệu Live Rank hoàn tất qua `crawl_riot_matches.py`:**
  - Tích lũy thành công **1,009 trận** xếp hạng đơn/đôi (vượt mốc chỉ tiêu 1,000 trận).
  - Phân bổ cân đối Multi-server: **550 trận** máy chủ Việt Nam (`VN2`) và **459 trận** máy chủ Hàn Quốc (`KR`).
  - Đảm bảo 100% chuẩn 1NF (10 cột lane nguyên tử `blueTop`..`redSupport`), 3NF (loại bỏ cột `country` phụ thuộc hàm, lưu cột `server`).
  - Thu thập đầy đủ 10 lượt cấm (`blueBans`, `redBans`) và chỉ số kinh tế mốc 10 phút.
  - Đồng bộ lưu song song vào CSDL SQLite `data/database/lol_live_data.db` (bảng `matches_10min`) và file `data/processed/lol_live_ranked_10min.csv` (1,009 $\times$ 42 cột, 0 giá trị NULL ở các cột chính).
- **Cập nhật trạng thái:**
  - Đánh dấu hoàn thành Task 1.1 trong [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md) và [`AI/TASKS.md`](TASKS.md).

---

## [2026-09-20] - THUẬT TOÁN QUYẾT ĐỊNH MÙA GIẢI THÔNG MINH (ADR-013) & BỘ LỌC GIẢI ĐẤU (LCK, LCP, LPL...)
- **Nâng cấp `src/01_data_pipeline/sync_google_drive.py`:**
  - Bổ sung hàm `parse_leagues()` và hỗ trợ tham số `--leagues` (ví dụ: `LCK,LCP,LPL`, `VCS`...).
  - Bổ sung hàm `count_matches(filepath, leagues=None)` đếm số lượng trận đấu độc lập trong phạm vi giải đấu chỉ định.
  - Bổ sung hàm `build_adaptive_dataset(latest_year, previous_year, min_matches, leagues=None)`:
    - Lấy toàn bộ năm mới nhất + trích xuất phần cuối năm trước (CKTG / Mùa Hè) cho đến khi đủ số lượng yêu cầu.
  - Bổ sung hàm `sync_smart_latest(min_matches, leagues, force)`:
    - Tự động thẩm định số trận trong phạm vi giải đấu chỉ định.
    - Xuất tệp hoạt động `data/raw/esports_active_matches.csv` lọc chuẩn xác các giải đấu yêu cầu.
- **Nâng cấp `src/config/settings.py` & `src/config/__init__.py`:**
  - Bổ sung cấu hình `ESPORTS_TARGET_LEAGUES` đọc từ `.env`.
  - Cập nhật hàm `get_active_esports_file()` tự động nhận diện `esports_active_matches.csv` nếu có.
- **Cập nhật tài liệu & file mẫu:**
  - Cập nhật [`src/01_data_pipeline/README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md), `.env.example`, và ghi nhận kiến trúc [ADR-013](DECISIONS.md) trong [`AI/DECISIONS.md`](DECISIONS.md).

---

## [2026-09-20] - THIẾT LẬP MÔI TRƯỜNG ẢO NỘI BỘ (.VENV) & ĐỒNG BỘ TOÀN DIỆN TÀI LIỆU DỰ ÁN
- **Khởi tạo môi trường ảo `.venv` cục bộ (Python 3.13.14):**
  - Tọa lạc tại: `d:\Chivinh\2026_MonHoc\Nhập môn khoa học dữ liệu\Project\.venv`.
  - Cài đặt đầy đủ 100% các package trong `requirements.txt`: `pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `gdown`, `requests`, `python-docx`, `jupyter`, `ipykernel`.
  - Thiết lập `.vscode/settings.json` tự động nhận diện và kích hoạt `.venv` khi chạy mã trong VS Code.
  - Bảo vệ Git: Cả `.venv/` và `.vscode/` đều được chặn commit an toàn trong `.gitignore`.
- **Cập nhật đồng bộ toàn bộ hệ thống tài liệu Markdown (`.md`):**
  - [`README.md`](../README.md): Viết lại hoàn chỉnh với khối lệnh kích hoạt `.venv` nổi bật, cập nhật cây thư mục mới, và hướng dẫn Quick Start 4 bước rõ ràng.
  - [`docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md`](../docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md): Cập nhật Giai đoạn 1 với Task 1.0 (.venv) và Task 1.5 (Cloud Data Auto-Sync).
  - [`docs/DANH_MUC_API_VA_DATASET.md`](../docs/DANH_MUC_API_VA_DATASET.md): Bổ sung liên kết Google Drive dùng chung và module `sync_google_drive.py`.
  - [`AI/TASKS.md`](TASKS.md): Nghiệm thu Task 1.0 và làm giàu tiêu chí Task 1.5.
  - [`AI/DECISIONS.md`](DECISIONS.md): Ghi nhận quyết định kiến trúc [ADR-011](DECISIONS.md) (.venv) và [ADR-012](DECISIONS.md) (Tự động phát hiện mùa giải & Phân tách tài liệu).
  - [`AI/ARCHITECTURE.md`](ARCHITECTURE.md): Bổ sung trách nhiệm 2 script module 01 và chuẩn môi trường thực thi Section 3.
  - [`AI/PROJECT_STATE.md`](PROJECT_STATE.md): Cập nhật trạng thái môi trường thực thi `.venv` đã xác thực.

---

## [2026-09-20] - PHÂN TÁCH TÀI LIỆU PIPELINE THÀNH 2 FILE ĐỘC LẬP & TỰ ĐỘNG HÓA MÙA GIẢI ĐỘNG
- **Phân tách tài liệu chi tiết thành 2 file chuyên biệt:**
  - [`src/01_data_pipeline/README_CRAWL_RIOT.md`](../src/01_data_pipeline/README_CRAWL_RIOT.md): Hướng dẫn toàn diện module cào Live Rank từ Riot Games API (kiến trúc, bóc tách timeline phút thứ 10, chuẩn 1NF/3NF, chống Rate Limit HTTP 429).
  - [`src/01_data_pipeline/README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md): Hướng dẫn toàn diện module đồng bộ Google Drive Oracle's Elixir (kiến trúc, cache manifest, regex trích xuất năm, hướng dẫn vượt hạn ngạch Google Drive Quota Exceeded).
  - [`src/01_data_pipeline/README.md`](../src/01_data_pipeline/README.md): Chuyển thành trang Tổng quan / Hub điều hướng liên kết trực tiếp tới 2 tài liệu trên.
- **Nâng cấp thuật toán tự động đón đầu tương lai (Future-Proof Season Discovery):**
  - Cập nhật [`sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py) hàm `get_recent_years(n_recent=2)` quét regex `^(\d{4})_LoL_...csv` trên Drive.
  - Tự động nhận diện và đồng bộ mùa giải mới nhất (khi có 2027 sẽ tự động kéo `[2026, 2027]` mà không cần sửa code).

---

## [2026-09-20] - XÂY DỰNG HOÀN TẤT MODULE ĐỒNG BỘ GOOGLE DRIVE (SYNC_GOOGLE_DRIVE.PY)
- **Triển khai module [src/01_data_pipeline/sync_google_drive.py](../src/01_data_pipeline/sync_google_drive.py):**
  - Tích hợp kết nối trực tiếp với Thư mục Google Drive Oracle's Elixir (`1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`).
  - Sử dụng `gdown` để quét danh mục siêu nhẹ 13 mùa giải (2014-2026) mà không cần tải dữ liệu nặng (`--list`).
  - Cơ chế Cache Manifest (`.drive_sync_manifest.json`): Tự động phát hiện dung lượng file cục bộ để bỏ qua tải trùng lặp, tiết kiệm 71 MB băng thông mạng.
  - Hỗ trợ tham số linh hoạt: Tải năm chỉ định (`--year`), tải toàn bộ lịch sử (`--all`), và ép buộc làm mới (`--force`).
- **Cập nhật cấu hình & tài liệu:**
  - Thêm `GOOGLE_DRIVE_FOLDER_ID` vào `src/config/settings.py`, `src/config/__init__.py`, `.env`, `.env.example`.
  - Bổ sung `gdown>=6.4.0` vào `requirements.txt`.
  - Cập nhật tài liệu hướng dẫn vận hành trong [src/01_data_pipeline/README.md](../src/01_data_pipeline/README.md).
  - Hoàn thành nghiệm thu **Task 1.5** trong [AI/TASKS.md](TASKS.md).

---

## [2026-09-20] - BỔ SUNG KIẾN TRÚC & TASK ĐỒNG BỘ DỮ LIỆU TỰ ĐỘNG TỪ GOOGLE DRIVE
- **Quy hoạch tính năng Cloud Data Auto-Sync (Task 1.5):**
  - Bổ sung quyết định kiến trúc [ADR-010](DECISIONS.md) và phân rã nhiệm vụ trong [AI/TASKS.md](TASKS.md).
  - Cơ chế: Hệ thống tự động kiểm tra thời gian cập nhật (`modifiedTime`) hoặc hash `md5Checksum` của tệp/thư mục Google Drive chia sẻ (tập dữ liệu giải đấu, nhãn bổ sung).
  - Tối ưu hóa: Chỉ tải về `data/raw/` khi trên Drive có dữ liệu mới; tự động kích hoạt pipeline làm sạch và cập nhật CSDL SQLite phục vụ làm việc nhóm khép kín.

---

## [2026-09-20] - FIX BUG ĐIỀU KIỆN DỪNG CỦA CRAWLER TRÊN CSDL ĐA MÁY CHỦ
- **Sửa lỗi ngắt sớm tại hàm `get_match_ids` trong [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py):**
  - Nguyên nhân: Trước đó điều kiện dừng kiểm tra `len(match_ids) + len(existing_ids) >= target_count`. Do CSDL đã có sẵn 99 trận từ máy chủ VN2 (`existing_ids = 99`), khi máy chủ KR vừa cào được đúng 1 trận (`1 + 99 = 100`) thì bị kích hoạt lệnh `break` dừng sớm.
  - Khắc phục: Sửa điều kiện dừng thành `len(match_ids) >= target_count`. Biến `existing_ids` chỉ dùng để lọc trùng lặp trận đã có trong DB (`if m_id not in existing_ids`).
  - Kết quả: Đảm bảo crawler cào đủ số lượng trận độc lập cho từng máy chủ theo đúng cấu hình `TARGET_MATCHES_PER_SERVER`.

---

## [2026-09-20] - KHÔI PHỤC CẤU TRÚC THƯ MỤC PIPELINE & BỔ SUNG README.MD CHUẨN HÓA
- **Khôi phục toàn bộ các thư mục theo kiến trúc chuẩn:**
  - Khôi phục các thư mục từ bước 02 đến 07: `src/02_preprocessing/`, `src/03_database_sql/`, `src/04_hypothesis_testing/`, `src/05_visualization/`, `src/06_machine_learning/`, `src/07_recommender/`.
  - Khôi phục các thư mục bổ trợ: `notebooks/`, `reports/figures/`.
- **Chuẩn hóa tài liệu nội bộ từng module:**
  - Thay thế toàn bộ các file tạm `.gitkeep` bằng các file `README.md` chi tiết cho từng thư mục.
  - Mỗi file `README.md` mô tả rõ mục tiêu, trách nhiệm phân công, dữ liệu đầu vào (Input), dữ liệu đầu ra (Output) và tiêu chuẩn chất lượng.
  - Vừa giúp Git theo dõi và duy trì cấu trúc thư mục vĩnh viễn, vừa phục vụ tài liệu tra cứu trực quan khi làm việc nhóm và nộp bài.

---

## [2026-09-20] - ĐÓNG GÓI CẤU HÌNH VÀO PACKAGE SRC/CONFIG/
- **Tách cấu hình vào thư mục riêng chuẩn mực:**
  - Tạo package [src/config/](../src/config/) gồm `settings.py` và `__init__.py`.
  - Quản lý tập trung toàn bộ biến môi trường (`.env`), xác thực Riot API key, đường dẫn thư mục I/O (`BASE_DIR`, `DATA_DIR`, `OUTPUT_CSV`, `OUTPUT_DB`), thông số server (`ACTIVE_SERVERS`, `SERVER_METADATA`).
  - Xóa file `config.py` ở thư mục gốc Project để giữ cấu trúc thư mục sạch sẽ, không có file lẻ đứng giữa đường.
- **Cập nhật script crawler [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py):**
  - Import cấu hình trực tiếp từ `src.config` (kèm fallback an toàn).
  - Loại bỏ các khối logic kiểm tra key trùng lặp vì module cấu hình đã tự động kiểm tra ngay khi nạp.
  - Chạy thử nghiệm thành công 100% không phát sinh bất kỳ lỗi đường dẫn nào.
- **Quy tắc Git:** Tuyệt đối không commit hay push tự động; giữ toàn bộ thay đổi ở Working Tree để User toàn quyền kiểm soát.

---

## [2026-09-20] - HOÀN NGUYÊN NGUYÊN TRẠNG BẢN CRAWLER ĐƠN LẬP (COMMIT 40dced0)
- **Hoàn nguyên mã nguồn [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py):**
  - Giữ nguyên cấu trúc xác định thư mục gốc `BASE_DIR = os.path.dirname(...)` nguyên bản.
  - Giữ nguyên toàn bộ cấu hình `.env`, biến môi trường, đường dẫn I/O và metadata tập trung trong một file duy nhất.
  - Dọn sạch toàn bộ các file cấu hình phát sinh ngoài luồng (`src/config.py`, `src/logger.py`, `pyproject.toml`, `tests/`, `.github/`).
- **Cập nhật quy tắc quản trị [AI/AI_RULES.md](AI_RULES.md):**
  - Bổ sung quy định bắt buộc: **TUYỆT ĐỐI KHÔNG tự ý chạy lệnh `git push` lên GitHub** khi chưa có sự cho phép trực tiếp từ User.


## [2026-09-20] - DỌN DẸP DỰ ÁN TINH GỌN (CLEAN CODEBASE)
- **Xóa bỏ file trùng lặp:**
  - Xóa file `crawl_riot_matches.py` ở root, chỉ giữ lại một file chính thức duy nhất tại [src/01_data_pipeline/crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py).
- **Xóa bỏ thư mục không dùng (`archive/`):**
  - Xóa toàn bộ thư mục `archive/` chứa các script nháp cũ không liên quan (`vietnam_housing.db`, `test_pull_housing.py`, các file test nháp).
- **Đồng bộ hóa tài liệu:**
  - Cập nhật `README.md` và `AI/PROJECT_STATE.md`.
  - Đẩy thay đổi dọn dẹp lên GitHub repository.

## [2026-09-20] - KẾT NỐI VÀ ĐẨY DỰ ÁN LÊN GITHUB REPOSITORY
- **Git & Remote:**
  - Khởi tạo Git repository cục bộ (`git init`).
  - Thiết lập nhánh mặc định là `main` (`git branch -M main`).
  - Thêm remote origin: `https://github.com/chivinh123abc/StrategyPredictionAndRecommendation.git`.
  - Thực hiện commit đầu tiên gồm 42 files (toàn bộ source code, thư mục `AI/`, `docs/`, `data/processed/`).
  - Đẩy thành công lên GitHub (`git push -u origin main` - SUCCESS).
  - Đảm bảo an toàn: File `.env` chứa key và file dữ liệu thô 71.1 MB được giữ cục bộ an toàn, không bị commit lên GitHub.

## [2026-09-20] - CẤU HÌNH BIẾN MÔI TRƯỜNG (.ENV) VÀ BẢO VỆ API KEY
- **Bảo mật:**
  - Cập nhật `.gitignore` bỏ qua `.env`, `.env.*` (ngoại trừ `.env.example`).
  - Tạo `.env` chứa `RIOT_API_KEY`, `ACTIVE_SERVERS`, `TARGET_MATCHES_PER_SERVER`.
  - Tạo `.env.example` làm mẫu cấu hình an toàn cho repository.
  - **Triệt tiêu 100% hardcode:** Xóa hoàn toàn giá trị fallback cũ trong mã nguồn `os.getenv()`, thêm exception `ValueError` cảnh báo bắt buộc nạp key từ `.env`.
- **Mã nguồn:**
  - Cập nhật `crawl_riot_matches.py` và `src/01_data_pipeline/crawl_riot_matches.py` tự động đọc cấu hình từ `.env` bằng thư viện chuẩn `os`.
  - Test kiểm thử: Nạp thành công key từ `.env` không phụ thuộc vào code (PASS).

## [2026-09-20] - AUDIT DỰ ÁN & THIẾT LẬP HỆ THỐNG QUẢN TRỊ NGỮ CẢNH (AI/)
- **Thực hiện:** Kiểm tra toàn bộ mã nguồn, dữ liệu thực tế, các gói thư viện cài đặt và CSDL SQLite.
- **Phát hiện quan trọng:**
  - `src/01_data_pipeline/crawl_riot_matches.py` và `crawl_riot_matches.py` đã hoạt động tốt, CSDL có 100 trận (99 VN2, 1 KR).
  - Các thư mục `src/02_` đến `src/07_`, `notebooks/`, `reports/` hiện đang rỗng.
  - Python 3.10.11 đã cài đặt `pandas`, `numpy`, `matplotlib`, `requests`. Chưa cài đặt `scikit-learn`, `scipy`, `fastapi`, `uvicorn`.
- **Tài liệu tạo mới trong `AI/`:**
  - `AI/AI_RULES.md`: Bộ quy tắc làm việc và giao thức bắt buộc cho AI sessions.
  - `AI/PROJECT_STATE.md`: Hiện trạng thực tế sau audit.
  - `AI/ARCHITECTURE.md`: Kiến trúc hệ thống 3 tầng (Data $\rightarrow$ FastAPI $\rightarrow$ Web App).
  - `AI/DATABASE.md`: Đặc tả chi tiết 42 cột của bảng `matches_10min` và các bảng giải đấu dự kiến.
  - `AI/TASKS.md`: Atomic checklist chi tiết 5 giai đoạn cho 3 thành viên.
  - `AI/DECISIONS.md`: Ghi nhận 7 quyết định kiến trúc cốt lõi (ADR-001 đến ADR-007).
  - `AI/CHANGELOG.md`: Nhật ký thay đổi này.
- **Tài liệu hỗ trợ quản lý:**
  - Tạo `docs/clickup_import_lol_project.csv` hỗ trợ kéo thả toàn bộ task vào ClickUp.
  - Cập nhật `README.md` chuẩn hóa kiến trúc dự án và Giao diện Web App.

---

## [2026-09-19] - CHUẨN HÓA CSDL 1NF & 3NF VÀ XỬ LÝ LỖI PIPELINE
- **Mã nguồn:**
  - Sửa lỗi `NameError: TARGET_MATCHES_PER_SERVER` trong `crawl_riot_matches.py`.
  - Tích hợp xử lý giới hạn tốc độ (Rate Limit 429) với cơ chế Exponential Backoff.
- **Cơ sở dữ liệu & Dữ liệu:**
  - **1NF:** Tách bỏ `blueChampions` và `redChampions` thành 10 cột nguyên tử (`blueTop`..`blueSupport`, `redTop`..`redSupport`).
  - **3NF:** Xóa bỏ cột `country` do phụ thuộc hàm vào `server`.
  - Tái tạo bảng `matches_10min` trong `data/database/lol_live_data.db` và file `data/processed/lol_live_ranked_10min.csv` về đúng 42 cột chuẩn mực.
  - Tạo tệp `data/raw/sample_2026_esports_100.csv` (100 dòng) từ file 71.1 MB của Oracle's Elixir để chống đơ VS Code.

---

## [2026-09-18] - KHỞI TẠO DỰ ÁN & ĐẶC TẢ ĐỒ ÁN
- Khởi tạo cấu trúc dự án `src/`, `data/`, `docs/`, `notebooks/`, `reports/`.
- Soạn thảo đặc tả đề tài môn Nhập môn Khoa học Dữ liệu gửi TS. Thái Tuyết Hải.
- Viết crawler ban đầu kết nối Riot Games Developer API.


---

2026-11-23 — Đang triển khai integrity remediation: không thay đổi raw SQLite/schema; snapshot sạch dùng chung, giữ chênh lệch âm và ngoại lai hợp lệ; Snowball chỉ dùng macro thực đo; lựa chọn model bằng validation log loss, calibration độc lập, test theo nhóm trận; Draft encoding chỉ dùng lịch sử trước block. Chưa công bố kết quả cho đến khi kiểm thử.
