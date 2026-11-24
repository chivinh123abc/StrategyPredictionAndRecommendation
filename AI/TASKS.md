## Dừng collector Rank nền & đóng băng số liệu báo cáo — 2026-11-24

- [x] Dừng `update_rank_evidence.py --watch` (PID `29828`, `7992`) và xác nhận không còn tiến trình chạy nền.
- [x] Đóng băng số liệu `ranked_evidence.db` ở mốc **975 trận / 9,750 dòng / 5,236 cặp gộp / 148 cặp `n >= 5`** và xuất lại `BAO_CAO_CUOI_KY_PTIT.docx` + cập nhật `BAO_CAO_CUOI_KY.md` khớp 100%.

## Xuất Báo cáo cuối kỳ Word (.docx) kèm biểu đồ & phân tích mạch giá trị — 2026-11-24

- [x] Viết `scratch/build_final_report_docx.py` và xuất [reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx](../reports/final_report/BAO_CAO_CUOI_KY_PTIT.docx) (4,725.6 KB, 13 biểu đồ/ảnh minh chứng, 15 bảng/khung phân tích mạch giá trị).
- [x] Kiểm chứng đọc lại file `.docx` bằng `python-docx` PASS; đồng bộ `reports/README.md` và `AI/`. Không thay đổi phương pháp/code/DB/model, không retrain/commit/push.

## Biên soạn Báo cáo cuối kỳ — 2026-11-24

- [x] Viết [reports/final_report/BAO_CAO_CUOI_KY.md](../reports/final_report/BAO_CAO_CUOI_KY.md) bám sát Chương 1–6, tách bạch `MH`/`UD` và `MR`/`NV`, trích đúng số liệu đã xác minh và giải trình rõ giới hạn của `draft_model` / `content_based`.
- [x] Cập nhật trạng thái trong `reports/README.md` và đồng bộ `AI/`; kiểm tra toàn bộ liên kết nội bộ PASS. Không thay đổi phương pháp/code/DB/model, không retrain/commit/push.

## Dọn sạch & chuẩn hóa tài liệu, dừng web server nền — 2026-11-24

- [x] Dừng tiến trình `uvicorn` nền trên `127.0.0.1:8000` (PID `28952`, `46456`) và xác nhận cổng `8000` không còn lắng nghe.
- [x] Xóa các đoạn lặp tiêu đề NV-24 và sửa lỗi dính chữ trong 6 file `AI/` và mục 28–30 của `docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md`.
- [x] Thu gọn `README.md` thành bảng trạng thái hiện hành và lập mục lục `reports/README.md`.
- [x] Không phát sinh thay đổi kiến thức/phương pháp/chức năng; các mục hiện hành giữ nguyên, không retrain/commit/push.

## Inspector whole-panel collapse — 2026-11-24

- [x] Thu gọn toàn bộ body Inspector → chỉ giữ header nhỏ, kéo gần timeline, mở rộng phục hồi nguyên trạng; build và Edge test PASS.

## Inspector click-toggle — 2026-11-24

- [x] Inspector ẩn mặc định, click-only mở/tắt, close giữ selection / deselect ẩn nút mở, reset/reload; build và 7 Edge workflow PASS.

## Sidebar responsive fit — 2026-11-24

- [x] Responsive 3 cột từ `900px`, cùng hàng và cùng chiều cao; kiểm tra 7 độ rộng desktop + mobile `390px` và build PASS.

## Hai khu hai bên — 2026-11-24

- [x] Desktop 3 cột: Gợi ý | Đội hình | Chọn tay cùng hàng; setup trên đầu, inspector dưới, giữ role dọc.
- [x] Build và Edge layout/mobile PASS; đồng bộ tài liệu NV-24, không đổi logic/DB.

## Điều chỉnh bảng đội hình — 2026-11-24

- [x] Khôi phục 2 bảng căn giữa, 5 role dọc, ảnh `47px`, giữ yêu cầu phần xung quanh.
- [x] Build TS/Vite và Edge kiểm layout/mobile PASS; không đổi logic nên không retrain/chạy lại Python test.
- [x] Đồng bộ sổ mục 30 (NV-24), hướng dẫn UI, AI state/tasks/changelog/architecture; không commit/push.

## UI compact / lane review — 2026-11-24

- [x] Setup trên đầu, gợi ý trái / manual phải, inspector dưới; auto-role preview + commit, native drag/swap cùng đội, keyboard fallback.
- [x] Tái hiện case Galio `n=0` vs Ambessa (địch 4 tướng), review ngay khi lane đã lộ; Wilson lower bound cho cùng role, Renekton `2/2` không nhận vượt trội.
- [x] CLI series bắt buộc `--first-picks`, bỏ auto luân phiên, hỗ trợ all-Blue/all-Red hợp lệ; UI chọn từng ván.
- [x] 178 tests, 5 Edge workflow, build, BO5 all-Blue (50 unique picks), hash/privacy/docs/sổ mục 30/ADR-043 PASS.
- [ ] Chất lượng chiến thuật độc lập và việc đưa GD/XP/CS vào score chưa được chứng minh; không đánh giá regression như win uplift.

## Giữ cặp bot và chọn trước từng ván — 2026-11-24

- [x] Tái hiện 10 lượt case Nautilus/Jayce → 2 AD bans → Yunara, công khai số mẫu `n=5/6/1`.
- [x] Guard theo lịch, full legal partner (`n >= 5`, `lift >= 1`), giữ score gốc, role filter/manual, review/test override; API/CLI/JSON/why/UI đồng bộ.
- [x] First Selection user chọn Blue/Red mỗi ván, không auto luân phiên trên UI; CLI `--first-picks` cho lặp side, validation và báo cáo nguồn luật đúng phạm vi.
- [x] 170 tests, build, 3 Edge workflow, mirror case, continued prefix và BO5 `red,red,blue,blue,red` (100 actions / 50 unique) PASS; hash/privacy/docs/sổ mục 29/ADR-042.
- [ ] Chứng minh cặp tối ưu, tăng thắng và đánh giá chiến thuật độc lập vẫn chưa đạt; không nằm trong kết luận regression này.

## Hai panel / contextual v2 — 2026-11-24

- [x] Gợi ý và chọn tay đồng hiện, nút xác nhận riêng; browser kiểm tra manual không ẩn gợi ý.
- [x] Fixed-capacity utility sửa pool `n < 3`, tính đơn điệu và baseline cùng pool trên 80 states.
- [x] Pin ngày và mã `snapshot_id`, hiện cấu hình/export, mismatch trả `409` và guard cache; khi conflict vẫn export/tạo phiên mới được.
- [x] 159 tests, build, 2 Edge workflow/mobile, Pro hash/outputs/privacy/documentation PASS; không train/commit/push.
- [ ] Chứng minh tăng chất lượng chiến thuật độc lập vẫn chưa đạt; phép so hiện tại không tăng Recall@5 ban lịch sử.

## UI local TS/API — 2026-11-24

- [x] React/TypeScript một trang, FastAPI mỏng, tái sử dụng engine và mặc định `current`.
- [x] Chọn tay/gợi ý, đánh số lượt, flex/undo/archive, auto có review/test override.
- [x] Chuỗi 5 ván Fearless, `localStorage`, export JSON; Rank chỉ là bảng bằng chứng trong Pro UI.
- [x] Build, 154 unit tests, browser Edge workflow một ván → ván 2 và mobile, export/hash/privacy.
- [x] Hướng dẫn chạy, sổ mục 27 (NV-21), AI/ADR-040/constitution `1.3.0` đồng bộ; không commit/push.
- [ ] Rank recommender UI riêng và đánh giá prospective chất lượng: còn phụ thuộc dữ liệu, không thuộc nghiệm thu UI Pro đầu tiên.

## Rà điểm / so sánh đơn giản / BO5 — 2026-11-24

- [x] Rà 8 thành phần, trọng số/công thức/chương/MR và bảng giữ-bỏ trong `docs/TINH_GIAN_DIEM_RECOMMENDER.md`.
- [x] Công thức `simple` 3 tín hiệu có fallback/missing rõ; selector `current`/`simple`, default `current` không đổi, không thêm framework/model.
- [x] Cùng frozen Pro history, eligible `(role, champion)` pool và rules; 200 val / 320 test × 3; xuất pool hash, split và ablation 8 thành phần.
- [x] `simple` test Recall@5 = `0.425` thấp hơn `current` = `0.49375`: giữ mặc định, không tune để ép metric.
- [x] BO5 T1–Gen.G 5 draft / 100 actions / 50 pick unique, ban contextual / pick simple, ghi đủ số Ban/Pick, lý do và missing; 44 fallback / 5 sparse có nhãn, không giả winner.
- [x] 146 unit tests + integration PASS; sổ mục 26 (MR-23/NV-20), docs/AI đồng bộ.

Không đánh dấu đã nâng chất lượng chiến thuật hay đã tinh giản mặc định; so sánh dùng Pro audit cũ và pick retrieval, không phải final test độc lập mới.

## Rà soát phạm vi vừa sức và rút quota — 2026-11-24

- [x] Đối chiếu nhóm chức năng với Chương 0–6, chỉ rõ phần cốt lõi / phụ / nghiên cứu và phần runtime vẫn còn MR trong `docs/PHAM_VI_DO_AN_VUA_SUC.md`.
- [x] Thêm giới hạn phát triển vào `AI_RULES`, `KNOWLEDGE_RULES` và constitution `1.2.0`; không bắt buộc Web/API đầy đủ hoặc theo đuổi quy mô U.GG.
- [x] Bỏ default 2,000, metadata `None`, summary v3, `ugg_reference_status=not_loaded`; không giảm tiêu chuẩn cohort hoặc đổi điểm Pro.
- [x] 139 full tests / 70 rank subset / integration 418 games PASS, Pro export chỉ đổi quota metadata; không đổi DB/model.
- [x] Nạp lại watch không quota PID 29828 / worker 7992, cùng kho và checkpoint, manifest/log đã lưu; sổ mục 25 (NV-19) và docs đồng bộ.
- [ ] Chưa có U.GG reference cùng bộ lọc để xác nhận ngang số mẫu/độ phủ; không phải điều kiện nghiệm thu đồ án.
- [ ] Nếu thực sự rút công thức xếp hạng hiện tại cần một thay đổi riêng có baseline; chưa tuyên bố đã đơn giản hóa thuật toán. Prototype/evaluator cũ giữ để truy vết, không xóa file.

## Pro matchup + source explanations + contextual experiment — 2026-11-24

- [x] Thống kê3.000trận Pro từ luồng sạch, đủrole/signed/missing/identity/độ dài trận; exportall/pooled/WRcao-thấp/GD15, khôngghiDB.
- [x] Giải thích từng gợi ý vàwhy: Pro/Rank riêng, n, metric10/15,CI, thiếu mẫu/trái chiều, flexroleprobability và provenance.
- [x] Score/thứ tự bản chính không đổi; test bật/tắt giải thích đạt.
- [x] FreezeRank riêng và contextual matchup source experiment, cùngpool/history/control; hybrid cố định, không bật main.
- [x] Diagnostic30val/30test từ261Rankfrozen: chưa cải thiệnRecall5/MRR5; công khaifutureRank/reusedPro, khôngdùng đểpromote.
- [x] 138unit tests + integration6stored-diff/mirror/roles/privacy/console/hashPASS; sổMR-22/NV-18 vàdocs/AI cậpnhật.
- [ ] Chưa có5validation+5testProseries độc lập saufreeze24/11:readyFalse/metricsNull, chờ dữliệu mới để kiểm chứng; prospective_queries.json chưa tồn tại.
- [ ] Chưa có bằng chứng nâng chất lượng để thay điểmPro chính; không gán counter/tăngthắng/BO5optimality từ retrieval.

## Bảng gộp và thu theo hướng U.GG — 2026-11-24

- [x] Integration cuốiPASS:150trận/725người/1.170pooledpairs/389rawbulkmemberships;69tests, nguồn/duplicate/CIprogress/DBProhash đạt. ĐãkhởiwatchPID23100 lúc14:17VN24/11, PID/log/cáchdừngtrongcollector_process.json; khôngnghĩađạt2.000/kèo.

- [x] Gộp patch/server thực có, giữ scope queue/tier/role và bảng riêng để kiểmtra; khônggán counter bấtbiến.
- [x] Bảng pooled wholegameWR/GD15 riêng, nguồn/dấuGD15; tiến độ mục tiêu2.000 mỗi kèo quan sát, không chặn thu/khôngbịamẫu.
- [x] Luân phiên server/cursor, live đủobservations KR/EUW/NA.
- [x] Bulkcurrentrank từ từngmembership League-v4lists archive, batchtransaction/refresh15min; individualfallback vàall10guard giữnguyên.
- [x] 69unit testsPASS, thêm6testtổngquát; xem checks.json cho integration mốc cuối và sessions/*.json cho thu thật.
- [x] Truyvết sổMR-21/NV-17/docs/AI; policyMaster+ khôngnới, khôngtrain/commit/push/đổiProscore.
- [ ] Chưa đạt mục tiêu2.000/kèo; tiếp tục qua --watch. Không phải thu xong khi code chạy được.
- [ ] Chưa chứngminh transferRank→Pro hoặc counterbềnqua patch; đánhgiá riêng sau.

## Kho tăngdần/thốngkê ngay, không trần1.000 — 2026-11-24

- [x] SQLiteevidence mới/persistentqueue/seedC-GM-M/paginationrecent100IDs/BFSparticipants, checkpoint/importraw10/idempotence, lock/rate/budget/watch.
- [x] Snapshotcache15mingiữtimegốc/afterend, qualificationresumequangày/atomic10roles/rawcheckpoint, khôngnớifloor24h/15minđểépdata.
- [x] Bảngrawsparse + winratecao/thấp vàGD15riêng, n/người/Wilson/mean-median-SD-tCI, cậpnhậtngaykhôngchờ1.000.
- [x] Live600+2HTTPrequest,88completegames/880rows/382người;714pairs,8n5.63tests+integrationPASS, canonicalDB/modelkhôngđổi.
- [x] Sổmục22/MR-20/NV-16, docsCONTINUOUS_RANK_EVIDENCE vàAI/indexđồngbộ; hai phiênđãdừng, watchlàlệnhtựchạytiếpcócheckpointkhôngtrầntổng.
- [ ] Recommender/UI/benchmarkindependent/Prosignal vẫnchưa triểnkhai; datasetstatskhôngxácnhậncounternhânquảhoặctốiưuBO5.

## Thu theođợt/coverage và điều kiện Rank — 2026-11-24

- [x]3batch/15seed/15candidate mới,179/200HTTPattempt gồmretry; giữngưỡng, tránhIDlặp, không thu vôhạn/nềntựđộng.
- [x] Gộp10accepted/100dòng/72người, CSVcoverage patch/role/championrole/lanepair kèm n/người/deficit/0evidenceuniverse.
- [x] Readiness/timeplan6/2/2,0historyavailabletrướcvalidation và0championrole n5; chặn việc nhận là đủ mẫu, metricsNull.
- [x]49tests + integrationPASS, docs/AI/sổ mục21/MR-19/NV-15 cậpnhật, DBrawkhôngđổi.
- [ ] Điều kiện chưađạt: recommenderRank/inputngữcảnh/pool, evaluation/baseline/CI vàUI cònchờdữliệuđủvàđợtởthờigiansau; khônghạthresholdhoặcdùngfuturetierđểépbenchmark. Prosignal/Rankruntime chưa bật.

## Collector snapshots đủ10người — 2026-11-24

- [x] Collector mới kiểm từng participant qua League-v4, lưu snapshot/tier/queue/server/time/raw riêngrun, báo nhận/loại/thiếu, typedHTTPstatus/terminal stop vàcache trongrun.
- [x] Live5trận KR/49người: cả5all10Master+ atobservation,2accepted/3quá24h/0missing,20observations.40tests + offline evidence/replay/privacy/DB checksPASS.
- [x] Snapshot-proxy tách historical gate, config recency/spread, docs/sổ mục20/MR-18/NV-14 và AI đồng bộ.
- [ ] RuntimeRank/benchmarkcohortmới/tíchhợpRankvàoGiải/finaltest vẫn chưa triển khai; không nâng currenttier thành historicalrank.

## Hai chế độ và tiêu chuẩn Rank cao — 2026-11-24

- [x] Thiết kế Rank/Giải riêng, config có ngưỡng làm việc Master+ chỉnh được, phân biệt legacy/contextual là chiến lược hiện có.
- [x] Admission audit: all10historical/unknown/snapshot/seed/below/conflict; private evidence và cutoff, không hồi tố current rank.
- [x] Audit92trận ->92seed-only,0đủ chứng cứ lịch sử;29tests + default evaluator exit2 và metric cũ giữ nguyên.
- [x] Output reports/rank_cohort_audit, sổ mục19/MR-17/NV-13, docs/HAI_CHE_DO_VA_TIEU_CHUAN_RANK_CAO và AI docs đồng bộ.
- [ ] Runtime/giao diện Rank, collector snapshot từng participant, cohort đạt chuẩn và final test mới vẫn chưa triển khai. Không bật Rank signal cho Giải.

## Kiểm chứng nguồn Rank/Pro — 2026-11-24

- [x] Chuẩn hóa theo catalog chính thức, audit CS/role/time; không fuzzy alias hoặc suy role.
- [x] Thu92trận lịch sử từ20seed,83trận16.20 trước freeze; raw/output riêng.
- [x] So Pro-only/Rank-only/hybrid offline, tách27/9/10series và giữ cùng pool/điểm khác;19unit tests + integration PASS.
- [x] Ghi kết quả không cải thiện: test Recall5=.49375 cả3, chỉ13/320query có bằng chứng Rank đủ mẫu. Giữ runtime contextual hiện tại.
- [x] Sổ mục18/MR-16/NV-12, protocol, AI docs và outputs reports/rank_transfer_evaluation đồng bộ.
- [ ] Chưa có final test bằng dữ liệu giải mới độc lập; còn thiếu độ phủ/kiểm soát selection-skill bias. Chưa tích hợp hybrid, chưa chứng minh counter/ban tốt/tăng thắng.

## Đối đầu Rank riêng với Pro — 2026-11-24

- [x] Thêm pipeline Riot sidecar, role/timestamp nghiêm ngặt và bảng thống kê Rank/Pro riêng; không cộng vào contextual.
- [x] Tải thật5trận KR16.23,50dòng; so phạm vi Worlds206trận/2060dòng, không có patch chung.
- [x]10unit tests và integration signed mirror/offset/missing/cutoff/DB hash PASS;110link sổ PASS. Minh chứng `reports/rank_pro_matchups/checks.json`.
- [x] Cập nhật sổ mục17/MR-15/NV-11 và hướng dẫn `docs/RIOT_RANK_MATCHUPS.md`. nearest±1000ms chỉ mô tả; before mặc định không sau mốc.
- [ ] Dự kiến sau: dữ liệu đủ/scope phù hợp và benchmark Pro-only/Rank-only/hybrid độc lập trước khi cân nhắc trọng số; chưa triển khai, chưa có output benchmark. Chưa chuẩn hóa hết alias/phân tầng rank.

## Rà soát50pick contextual, chưa sửa điểm chọn — 2026-11-24

VERIFIED AUDIT: user đã đồng ý bước1 trước, nên chỉ tái dựng50state của5draftcontextual và so248alternativecùngrole hợp lệ; khôngthêmsearch/flexhoặcsửapolicy. audit_draft_choices.py bổsungcompositionevidence/playerhistory/slot/sourcehash/scoregap vàdiagnosticablation; review_contextual_picks.py kiểmtra state/pool/score vàxuấtREVIEW/summary. 50score/top1táilậpkhớpphiênđãlưu, đây khônglàqualitylabel. 38/50pickcóđịchlộnhưngthiếumẫuđốidầu;5blind;7cóítmẫuđủngưỡng.3candidateítmẫuván5:Poppy2,Aurora2,Nasus1.100cặpphốihợp:8đủmẫu,59ítmẫu,32chưathấy,1thiếuanchor. Ablationbỏmetađổitop1ở13lượt,composition14,content1,mastery3,matchup3; khôngsuytướngthaythếtốthơnhoặcđếmsốpicksaibằngtổngnày.

Artifacts reports/contextual_pick_audit.json/md, reports/contextual_pick_review/REVIEW.md vàsummary.json. Sourcehash/state/248legalalternatives/savedscorechecksPASS, khôngthayđổiquyếtđịnhđãlưu/model/DB/train. PhươngphápkiểmđộnhạyMRmớighiởsổmục16; nềnChương1/5x, phầnablationngoàimônvớipolicychẩnđoántựthiếtkế. Phạmvihiệnhànhvẫnlegacy/contextual; bướcflex/đa-serieschưalàmtronglượtnày.

- [x] Bước1: audit50pickcontextual,248alternativevàđộnhạythànhphần, giữ nguyênpolicy.
- [ ] Chưa triểnkhai: xửlýflexownvàđánhgiánhiềuseries; cần dựa audit trước khi sửa điểm/dữ liệu.

## Hiện hành: chỉ legacy và contextual — 2026-11-24

Theo yêu cầu người dùng, đã BỎ lookahead khỏi mã ban và CLI; không chỉ ẩn menu. BanPlanner chỉ còn one-stepcontextual, ContextualBanPolicy(top3pool/owncost). Gỡ response_distribution/evaluate_root/rollout/leaf/predictor dependency và --ban-response-model; --ban-strategy chỉ legacy|contextual, legacygiữmặcđịnh. Contextual dùng pool_impact/contextual_trace, không xuất search_trace/branches/sensitivity. OpponentModelcũ giữ độc lập, không được contextual dùng đểban; không mởrộngchứcnăngkhác.

VERIFIED:57testsPASS;2seriesT1–Gen.GWorldscutoff13/11patchdataset16.20đều5draft/100actions/50uniquePicks,locks0/10/20/30/40, testtop1override. Pick/ban của cảlegacy/contextual giống phiêntrước (đã so cả100lượtmỗiseries); CLIonegame vàseries từchốilookahead(exit2), helpkhôngcònban-response-model. Newoutputs khôngsearchfields. Báocáohiệnhành reports/legacy_contextual_comparison/{COMPARISON.md,comparison.json,checks.json,legacy/,contextual/}; doc docs/BAN_LEGACY_VA_CONTEXTUAL.md. Khôngtrainmodel/đổiDB/raw. Tài liệu vàreportlookaheadcũđánh dấuLỊCHSỬ, khôngxóa artifact/minhchứng; cácmốcbêndướilàlịch sử trướcquyếtđịnhnày.

- [x] Gỡlookaheadkhỏiruntime/CLI/comparator, giữlegacy/contextual.
- [x] Rerun2×5draft,57tests vàCLIreject/lookaheadchecks; đánh dấuartifactcũlịchsử.
- Phạmvihiệnhành: chỉlegacy/contextual; search/plannerkhôngthuộcđợtlàmviệcnày.

## Bản chạy contextual riêng T1–Gen.G — 2026-11-24

VERIFIED RUN ONLY: đã chạy contextual riêng theo yêu cầu, xuất reports/t1_geng_contextual_20261124/{QUICK_VIEW.md,REPORT.md,series.json,game_1..5.json/log,checks.json}. Worlds cutoff13/11 patchdataset16.20, T1Blue/Gen.GRed,first-pickluânphiên, test chọn số1thiếutincậy.5draft/100actions/50uniquePicks,locks0/10/20/30/40; validate_game vàBan1–5/Pick1–5PASS.38pickreview_required giữnhãn. Không kiến thức/phương pháp mới, không đổi code/model/DB hoặctrain; MR-13/NV-08 vẫn áp dụng. Không gọi đây là tối ưu hoặc có tỉ số thắng/thua.

## Hoàn tất3mục ban ngữ cảnh, rollout phản ứng và đối chiếu5draft — 2026-11-24

VERIFIED: ban_planner.py/BanPlanner có contextual pool loss địch trừ self-denial theo thứ tựpick thật/roster/Fearless; lookahead shortlist6ban,2response ởfirstopponentturn rồigreedyđến3pick mới/max12plies. OpponentModelđãcó dùng inference, khôngfitmới; fallbacksoftmaxcónhãn. Không épdiversity, khôngcasechampion/team. Mặc địnhlegacy đểtáilập; bật --ban-strategy contextual|lookahead, --ban-response-model PATH. Trace lưu mọiroot/branch/leaf/coverage/omittedmass và sensitivitybounds (khôngCIthốngkê), why/REPORTgiảithích theo lượt.

57testsPASS; so3seriesT1–Gen.GWorlds cùngcutoff13/11patchdataset16.20/rosters/lịchfirstpick, testoverrideTrue theoủyquyền. Mỗi5draft100actions50uniquePicks, khóa0/10/20/30/40; 583branchpaths/295rootreplay hợp lệ, sâu tốiđa9<12. Tập6ban đầu:legacy1tập lặp5ván, contextual5,lookahead5; Jaccard1/.471/.145, khôngclaimđadạng=tốthơn. Lookahead~.471s/banmean,p95.787s,max1.371s trênlầnchạy;cócache. 23/50ban kháccontexttop1. Giữ2response chỉphủmean21.1%khốihỗtrợ,min5.8%;48/50sensitivityboundsoverlap. 41/50pickvẫnthiếucontextđủmẫu. Chưaindependentbanqualitybenchmark/counterevaluator/fullflex hoặcfullBO5plannerđểdànhtướng.

Artifacts: reports/ban_strategy_comparison/COMPARISON.md,comparison.json,checks.json và{legacy,contextual,lookahead}/{QUICK_VIEW.md,REPORT.md,series.json,game_1..5.json/log}. Sổkiếnthứcmục14/MR-13/KH-02 cậpnhật; docs/BAN_NGU_CANH_VA_LOOKAHEAD.md. KhôngđổiDB/schema/raw, khôngtrainmodel, khôngcommit/push. Trạngtháidừngtrướcđượcusergiaotiếprõ3mục; phạmvihoànthànhtạibảnrolloutgiớihạnnày.

- [x] Điểmbanngữcảnh theo2roster,firstpick vàFearlesspool.
- [x] Rolloutgiớihạn cócandidates/branches/leaf/latency/coverage vàsensitivity.
- [x] Chạy3chếđộ×5draftT1–Gen.G,57testsPASS,583branchreplay; ghi trước/sau vàsổkiếnthức.
- [ ] Cònbacklog: independentbanquality/evaluatorcơchế, mởrộngresponsecoverage, flex vàfullBO5resourceplanner.

## Test đủ5draft T1–Gen.G theo yêu cầu — 2026-11-24

VERIFIED: thêm --allow-statistical-auto cho series, defaultFalse không đổi. User yêu cầu test thiếu tin cậy vẫn chọn số1; toàn bộ5ván chạyTrue, không manualreviewstop nhưng vẫn giữreview_required/counterstatus/coverage. Worlds cutoff13/11 patchdataset16.20.100actions/50uniquePicks, locks0/10/20/30/40 vàvalidate_gamePASS; 38pick thiếu đối đầu đủ mẫu có nhãn. Report dùng đúng tên2đội vàBan1..5/Pick1..5mỗiđội kèmturn1..20. reports/t1_geng_bo5_test_20261124/REPORT.md,QUICK_VIEW.md,series.json,checks.json. Khôngtạo tỉsố hoặc chứngminhcounter/tốiưu. Khôngfitmodel/đổiDB hoặcphươngphápthốngkê. Lượt này chỉ mởtestoverride trongdriver vàđánh sốreport; khôngtiếptụcsearch/planner.

## Chạy lại BO5 T1–Gen.G — 2026-11-24

VERIFIED RUN ONLY: Worlds as-of2026-11-13 patchdataset16.20, 5draft được yêu cầu, mặc địnhtactical-reviewgate, khôngopponentmodel/override. Ván1hoàn thành20actions; ván2dừngtrước20(chỉ19actions) trướcCamille topT1, alternativesRenekton/Jax/Ornnđềucoverage0; ván3–5chưa chạy.39actions/19uniquePicks, khóa0rồi10, khônglặp hoặc dùngtướngbịkhóa. Reports:t1_geng_bo5_20261124/REPORT.md,series.json,game_1/2.json,checks.json.

Giới hạn xác nhận: Trundle vẫn được chọn ởván2trước khiđịch đủ5, coverage0; gatechỉkiểmtrađịchđủ5khônggiảiquyếthếtchấtlượngcounter/cáclựachọnkhác. Không đượcgọiBO5hoànthành hoặcfixcountertoàndiện. Lượtchỉchạyvàghiartifact, khôngđổiphươngpháp/code/model/DB, khôngretrain hoặc chạyregressionsuitekhôngliênquan. Userchỉyêucầuchạythử, khôngtựmởrộngfix/search/planner.

## Hoàn tất phạm vi Trundle/các lựa chọn tương tự, dừng phát triển tiếp — 2026-11-24

VERIFIED: enemy_evidence/evaluate_enemy_context xét mọi role địch, giữ n/CI/coverage và trạng thái mechanical_counter:not_evaluated. Audit50pick đúng state vàtop5, không blacklist tên. Actual Trundle ván2lượt20 vẫn topheuristic nhưng coverage0cũng như alternatives; không có căn cứ xác nhận counter/tướng thay thế tối ưu. Mặc định auto khi địch đủ5và pick thiếu mọi đối đầu đủ mẫu sẽ dừng trướcapply, lưu manual_review/completefalse vàCLIexit3; chọn tay được phép, demoonegame có --allow-statistical-auto rõ nghĩa. Exactcase giữ19actions/jungletrống; CLI casePantheon cũng dừng19actions. 51testsPASS, checks reports/tactical_review_checks.json; docs/RA_SOAT_LUA_CHON_THEO_DOI_HINH.md và sổ kiến thức mục11. Seriesdriver dừng khi cầnreview; các5draft trước đó là lịch sử trướcgate, không được gọicounterđãxác nhận.

Theo chỉ đạo mới, DỪNG sau khi hoàn tất phạm vi trên. Trước chỉ đạo dừng đã dựng4120draftstate/206ván/93seriesWorlds và fit OpponentModel CUDA, validation/time-series split train142/val22/holdout42ván; 840query phát triển R5=.3917 so slot=.2202. Cácmodel/dataset/forecastartifact được giữ, đã ghi sổ; không tiếp tục phát triển hoặc retrain sau thu hẹp phạm vi. Predictor mô phỏng hành vi, không là evaluator cơ chế hoặc planner. Opponent/search/BO5 và nguồn cơ chế patch-specific còn backlog. Không sửa rawDB/schema, không commit/push.

- [x] Rà soátTrundle và50pick, thêmcross-role context/alternatives, fail-closed khi đáp trả đội hình đủ5mà thiếu mẫu;51testsPASS.
- [x] Ghi đầy đủ kiến thức/artifacts đã làm trước chỉ đạo dừng; KH-01 có bảnđầu.
- [ ] Theo chỉ đạo người dùng: không tiếp tục opponent/search/planner/evaluator cơ chế trong đợt này.

## Quy định cập nhật kiến thức bắt buộc trong SpecKit/agent — 2026-11-23

VERIFIED CONFIGURATION: AI/KNOWLEDGE_RULES.md quy định mọi thay đổi kiến thức/phương pháp/chức năng/output phải cập nhật docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md trong cùng đợt: ID, MH/UD/MR/NV, chương/nguồn, hàm/module, công dụng/giả định, artifact/tái lập, trạng thái/minh chứng/giới hạn. No-impact có lý do; không tạo lý thuyết giả hoặc retrain model không đổi. Root AGENTS.md/GEMINI.md và AI/AI_RULES dẫn quy định; constitution thêmVI, version1.1.0. PrincipleV được làm rõ kiểm chứng theo tác động, không ép sửa tài liệu phải tái tạo.pkl.

SpecKit dùng4project overrides spec/plan/tasks/checklist với mapping và task cập nhật kiến thức bắt buộc; analyze giữread-only, checklist giữreviewownership. Đã kiểm tra actual Resolve-TemplateContent chọn đúng4override;70link sổ kiến thức PASS. Checker bền vững: .specify/scripts/powershell/check-knowledge-templates.ps1. Core templates,9Gemini commandprompts và manifest cài đặt giữ nguyên; không ghi policy vào installation metadata. Đây là policy/template enforcement qua agent và review, chưa là CI bảo đảm tự động mọi thay đổi. Không sửa code thuật toán/model/DB; không train hoặc chạy lại suite ML không liên quan.

- [x] Quy định truy vết kiến thức trong governance,constitution và4templateoverride; resolver/link checks PASS.
- [ ] Khi nâng cấp SpecKit, kiểm tra lại nguyên tắcVI/override và chạy check-knowledge-templates.ps1.

## Tổng hợp kiến thức và mục tiêu mở rộng BO5 — 2026-11-23

VERIFIED DOCUMENTATION: docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md là file tổng hợp dùng viết báo cáo: MH-01..14 đối chiếu Chương1..6/5x với hàm, chức năng và đầu ra; MR-01..11 ghi rõ các kỹ thuật ngoài nội dung cụ thể của slide; NV-01..05 ghi nghiệp vụ/Fearless/CLI; KH-01..06 ghi mục tiêu opponent modeling/search/để dành tướng/planner BO5 và đầu ra DỰ KIẾN. Giữ hướng người dùng yêu cầu: vận dụng môn học có mở rộng, có tính trước phản ứng và tối ưu phân bổ tướng cả series. Không ghi planner/opponent model như chức năng đã hiện thực: driver hiện tại vẫn greedy từng lượt.

Đã đối chiếu source, slide text, manifests và artifacts; 65liên kết nội bộ PASS, không link hỏng. Ghi rõ XGBoost CUDA là luồng fit hiện hành; RF/boosting/PCA/K-Means có nền trong bài nhưng import không chứng minh đãfit. Số liệu hiện hành lấy manifest/reports, không trộn mốc cũ. Đây là lượt tài liệu, không đổi thuật toán, DB/model/raw hoặc chạy lại training/benchmark.

- [x] Một file tổng hợp kiến thức/chương/module/đầu ra và phần mở rộng phục vụ báo cáo.
- [ ] KH-01/KH-04: opponent model và evaluator, đánh giá độc lập theo series/time.
- [ ] KH-02/KH-03: tìm kiếm phản ứng, phân bổ tướng qua BO5; trace và benchmark mới.
- [ ] KH-06: điều khiển2phe, kết quả và quyềnFirstSelection thực; MCTS KH-05 chỉ là phương án nếu cần.

## Hiện hành — 5 ván Fearless Worlds (2026-11-23)

VERIFIED: simulate_fearless_series.py chạy đủ5ván Gen.G–Bilibili Gaming, snapshotWLDS as-of2026-11-13 patch dataset16.20 (106ván/94ván patch), cố định Gen.G Blue/BLG Red và luân phiên first-pick B/R/B/R/B theo lịch demo. Không mô phỏng thắng/thua hoặc ép tỉ số2-2; đây là5draft liên tiếp. Fearless khóa mọi tướng PICK trước đó cho cả hai đội, không carry standard bans, không reset ván5. Validator kiểm tra20lượt/5role/5ban mỗi đội và pool dùng trước; 100actions,50uniquePicks, locks[0,10,20,30,40],38testsPASS. Lưu toàn bộ100lượt và căn cứ ở reports/worlds_fearless_bo5/REPORT.md, series.json và game_1..5.json/log.

Pilot min5 dừng ván5 vì pool support không đủ. Tách candidate_min_games khỏi min_games(evidence): series cho ứng viên từ1lần quan sát, giữ evidence5; luôn ưu tiên lớp>=5 trước lớp ít mẫu trong các role đang mở. Chỉ có Yuumi ván5 là sparse_candidate (4trận). Không invent role/tướng hoặc tự giảm ngưỡng tin cậy. Positive log-lift shrink theo weighted_pair/(weighted_pair+10), negative theo weighted_anchor/(weighted_anchor+10), trước geometric aggregation, để chặn bonus lớn từ cặp một-mẫu. Policy có công khai, chưa tối ưu cả series. Default one-game vẫn candidate/evidence5. CLI evaluate WLDS cập nhật audit: Recall@5=.36, Recall@1=.095,MRR5=.184, CI mô tả vsrecent[+.015,+.102625]; benchmark là phát triển nhỏ, chưa đánh giá fullFearless hoặc tăng thắng. Những số liệu36%/MRR.21225 bên dưới thuộc phiên trước shrink bổ sung.

Không đổi DB/schema/raw, tải dữ liệu mới, fit ML hoặc commit/push.

- [x] Chạy và validate100lượt/50picks cho5vánFearless.
- [ ] Lập kế hoạch bảo toàn pool cho toàn series, mô phỏng quyền First Selection theo kết quả thật; danh mục legal/event champion restrictions có nguồn.

## Hiện hành — phối hợp mọi cặp role, chạy Worlds (2026-11-23)

VERIFIED: DraftMetaSnapshot thống kê đủ 10 cặp role (20 chiều) trên gameid+side, giữ role của cả hai tướng, counts/Wilson cho tần suất ghép cặp và riêng kết quả cả trận. DraftAdvisor dùng conditional co-pick share shrink về marginal, geometric lift qua mọi đồng đội, điều chỉnh odds điểm nền; composition exponent1 là policy công khai chưa học/tune. Synergy WR cũng đã sửa giữ cả hai role. Không có case theo tên tướng, không biến association thành synergy cơ học/tăng thắng. JSON lưu formula/base/lift/evidence và ma trận10cặp/đội; why giải thích công thức.

35 tests PASS, gồm nhiều cặp role, tránh ghép đối thủ, flex role, thiếu mẫu/cutoff, đổi tên tướng không đổi điểm. Hai phiên Gen.G–Bilibili Gaming tại Worlds, Blue/Red first, hoàn thành20lượt/tướng khác nhau; snapshot trước chung kết as-of2026-11-13 patch dataset16.20, 106ván/94ván patch, không dùng4ván final14/11. Lucian–Milio đứng đầu truy vấn support khi đã có Lucian trong hai snapshot LCK/Worlds đã kiểm tra; không ép kết quả hoặc khóa cặp khác.

Audit Worlds200lượt: Recall@5 cũ30%, recent-presence30%, mới36%, MRR@5=0.21225; CI mô tả chênh với baseline[+1,+12]điểm phần trăm. Đây là tập phát triển nhỏ đã xem, chưa phải final test độc lập/đánh giá tăng thắng; chưa tái dựng Fearless series trong benchmark. Candidate coverage86%. Không tải dữ liệu mới, sửa schema/raw DB hoặc huấn luyện ML.

Nguồn hiện hành: docs/WORLDS_ROLE_PAIR_REVIEW.md, reports/worlds_draft_role_pairs.json, reports/worlds_role_pair_checks.json, reports/wlds_draft_policy_evaluation.json; baseline cũ được giữ trong reports/worlds_replay_before_role_pairs.json. LCK và hybrid ghi bên dưới là các mốc lịch sử trước sửa composition.

- [x] Thống kê và xếp hạng phối hợp cho toàn bộ cặp role, không vá riêng Lucian/Milio; chạy Worlds và lưu căn cứ.
- [ ] Xác nhận cơ chế phối hợp từ thuộc tính tướng có nguồn; mô hình tương tác3/5tướng; test nhiều patch theo series/time độc lập; full-series Fearless.

## Rà soát LCK và meta theo patch — 2026-11-23

VERIFIED: snapshot patch/thời gian chung trong draft_meta.py; presence/slot/player share có decay 21 ngày, cửa sổ 60 ngày; bỏ percentile, giảm cosine, matchup theo phân phối role một-một. Lineup lấy từ trận gần nhất, không là live roster. CLI có as-of/patch/freshness guard/used-champions. Phiên lịch sử bỏ dự báo model để tránh model fit sau cutoff. LCK local đến 2026-09-13, patch dataset16.16, 153 ván cửa sổ/80 ván patch; không có dữ liệu mới được tải. 31 unit tests và 6 CLI scenarios PASS (LCK/LPL/ALL, Red first, previous-game pool, stale-data rejection, missing-patch rejection); checks: reports/lck_meta_checks.json. Replay đóng băng trước 20 trận/200 lượt: Recall@5 policy28.5%, recent-presence27%, long-history24%; CI chênh [-1.5,+4.5] điểm phần trăm, chưa chứng minh ưu thế hoặc tăng thắng. Coverage84.5%, chưa replay đầy đủ Fearless series. Chi tiết docs/LCK_DRAFT_REVIEW.md; reports/lck_draft_policy_evaluation.json. Không sửa raw DB/schema hoặc huấn luyện ML.

## Bản hybrid trước sửa — lịch sử, đã thay policy bên dưới

## Giả lập hybrid ban/pick — 2026-11-23

VERIFIED: giả lập hybrid 20 lượt đã tích hợp historical + content-based/cosine; 24 tests PASS và 5 smoke scenarios hoàn tất 20 tướng khác nhau. Giữ lựa chọn đội/phe, lọc đường, why, chọn tay, swap, wishlist, auto và lưu JSON căn cứ. Pick tối đa điểm weighted rank aggregation; ban theo chênh top1/top2 đối thủ trên bảng hiện tại. Màu phe độc lập thứ tự draft qua --first-pick. Không tuyên bố tối ưu toàn cục/tăng thắng, không đổi benchmark cũ hay huấn luyện model mới. Hướng dẫn: docs/GIA_LAP_BAN_PICK.md; checks: reports/draft_simulator_checks.json.

- [x] Giả lập tương tác hybrid và kiểm soát trạng thái 20 lượt.
- [x] Audit replay lượt chọn với baseline, CI theo ván và cutoff chung.
- [ ] Tối ưu trọng số bằng validation riêng; final test theo thời gian/series; quản lý tự động toàn bộ series Fearless; cập nhật nguồn dữ liệu và kiểm tra provenance.


## Cập nhật Chương 6 — 2026-11-23

VERIFIED: content-based filtering đã có item profile → user profile có trọng số → cosine similarity theo Chương 6. Notebook 02 đã chạy đủ 6 cell mã; 16 regression tests PASS, ba CLI (seed, player, cold-start) và tích hợp engine PASS. Benchmark validation: 299 trận, 2990 truy vấn; Precision@10=0.0494, Recall@5=0.2990; popularity Recall@5=0.4652. Chưa vượt baseline về truy hồi; không tuyên bố tăng thắng. Không huấn luyện lại ML hoặc thay schema/raw DB. Hướng: vận dụng kiến thức môn học, có phần mở rộng. Xem docs/CHUONG_6_CONTENT_BASED.md và reports/content_based_evaluation.md.

- [x] Minh chứng Chương 6: item/user profiles, cosine, Precision@10, notebook và benchmark.
- [ ] Cải thiện chất lượng trên validation mới; đánh giá liên quan thực tế trước khi tuyên bố tối ưu.

> **TRẠNG THÁI ƯU TIÊN — Integrity v2, 2026-11-23.** Dự án đang triển khai theo roadmap; API/web chưa triển khai là công việc kế hoạch. Các tuyên bố cũ bên dưới như “100% Zero-Hardcode”, “hoàn thành 85% về chất lượng”, kết quả model cũ và kết luận nhân quả không còn là trạng thái nghiệm thu. Nguồn hiện hành: [INTEGRITY_V2.md](../docs/INTEGRITY_V2.md), [đánh giá ML](../src/06_machine_learning/evaluation_report.md), [benchmark recommender](../reports/recommender_evaluation.json).

- [x] Bỏ uplift cố định, synergy/counter riêng từng trường hợp và công thức radar tự tạo xác suất trong mô phỏng.
- [x] Dữ liệu chung: giữ signed differences, không tạo vàng theo đường, chỉ dùng macro đo tại phút 10; Pro objectives unavailable khi thiếu timeline.
- [x] Tách theo trận/thời gian; validation chọn model; calibration riêng; baseline; CI bootstrap; test manifest và fingerprint.
- [x] Gợi ý lịch sử có số mẫu/Wilson CI; công khai expert rules; benchmark retrieval so với popularity.
- [ ] Thu thập timestamps/timeline còn thiếu; đánh giá patch mới; cải thiện retrieval trên validation mới.
- [ ] Các hạng mục API/web và báo cáo cuối kỳ giữ theo roadmap.

Kiểm chứng Integrity v2 cuối lượt: {"rank_rows": 1009, "negative_blue_gold_rows": 525, "inconsistent_clean_gold_rows": 0, "notebook_executed_code_cells": 8, "notebook_png_outputs": 5, "unit_tests_passed": 11, "workflow_commands_passed": 12, "gpu_preflight": "passed"}. Raw DB không sửa; notebook có output thực; ML/ranking metrics xem báo cáo hiện hành.

---

NỘI DUNG LỊCH SỬ / KẾ HOẠCH TRƯỚC INTEGRITY V2:

# PROJECT TASKS & ATOMIC CHECKLIST

Trạng thái:
- `[x] DONE`: Đã hoàn thành và xác minh bằng kiểm thử/dữ liệu thực tế.
- `[-] IN PROGRESS`: Đang trong quá trình thực hiện.
- `[ ] NOT STARTED`: Chưa bắt đầu.
- `[!] BLOCKED`: Bị chặn bởi phụ thuộc kỹ thuật.

---

## 🟢 GIAI ĐOẠN 1: THU THẬP, LÀM SẠCH & THIẾT KẾ CSDL (CHƯƠNG 2, 5)

- [x] **Task 1.0 [Cả nhóm]: Thiết lập môi trường ảo `.venv`, cấu hình tập trung `src/config` & Cấu trúc thư mục Pipeline chuẩn**
  - *Mục tiêu:* Khởi tạo `.venv` nội bộ tại thư mục gốc dự án (Python 3.13), cài đầy đủ `requirements.txt` (`pandas`, `scipy`, `scikit-learn`, `gdown`, `jupyter`, `google-api-python-client`...), cấu hình `.vscode/settings.json` tự động trỏ interpreter. Tạo package cấu hình chuẩn `src/config/` (`settings.py`, `__init__.py`), bảo vệ Riot API key, nạp `.env`. Khởi tạo đầy đủ cây thư mục từ `02` đến `07`, `notebooks/`, `reports/figures/` đi kèm file tài liệu `README.md` chuẩn hóa.
  - *Kết quả:* Đã hoàn tất, kích hoạt thành công qua `.\.venv\Scripts\Activate.ps1` và kiểm thử 100% trơn tru.

- [x] **Task 1.1 [Thành viên 1]: Cào dữ liệu Live Rank VN & KR từ Riot Games API**
  - *Mục tiêu:* Tích lũy tối thiểu 1,000 - 3,000 trận rank cao (VN2 & KR) đạt chuẩn 1NF/3NF vào `data/database/lol_live_data.db`.
  - *Kết quả:* Đã tích lũy thành công **1,009 trận** thực tế (550 trận VN2, 459 trận KR), xuất song song ra `data/processed/lol_live_ranked_10min.csv` (1,009 dòng $\times$ 42 cột).
  - *Acceptance Criteria:* Bảng `matches_10min` có $\ge 1,000$ trận, 0 giá trị NULL ở các cột kinh tế và 10 tướng, tỷ lệ VN2 (54.5%) và KR (45.5%) cân đối hoàn hảo. Đạt chuẩn 1NF (10 cột lane nguyên tử) và 3NF (khử cột phụ thuộc hàm). Hoàn thành 100%.

- [x] **Task 1.2 [Thành viên 1]: Nạp dữ liệu giải đấu chuyên nghiệp vào SQLite**
  - *Mục tiêu:* Viết script ETL đọc tệp dữ liệu hoạt động (`get_active_esports_file()` / `data/raw/esports_active_matches.csv`) nạp vào 2 bảng `tournament_matches` và `tournament_players` trong `lol_live_data.db`.
  - *Kết quả:* Đã hoàn thành module [`src/01_data_pipeline/load_esports_to_db.py`](../src/01_data_pipeline/load_esports_to_db.py). Nạp thành công **6,000 dòng** vào `tournament_matches` (3,000 trận $\times$ 2 đội) và **30,000 dòng** vào `tournament_players` (3,000 trận $\times$ 10 tuyển thủ).
  - *Acceptance Criteria:* CSDL có 2 bảng mới chuẩn hóa 1NF/3NF, có composite Primary Key `(gameid, side)` cho matches, `(gameid, participantid)` cho players, và Foreign Key `(gameid, side) REFERENCES tournament_matches(gameid, side)`. Tự động tạo 12 Indexes tối ưu hóa truy vấn SQL. Chạy kiểm thử xác thực 100% trơn tru. Hoàn thành 100%.

- [x] **Task 1.3 [Thành viên 1]: Viết module làm sạch dữ liệu & khử ngoại lai (IQR/Z-Score)**
  - *Mục tiêu:* Viết hàm trong `src/02_preprocessing/cleaner.py` lọc bỏ 100% trận Remake (< 10 phút), AFK (CS < 10), xử lý missing values theo 5 nhóm chuẩn và lọc/cắt ngọn outlier chênh lệch vàng bất thường bằng IQR & Z-score.
  - *Kết quả:* Đã hoàn thành module [`src/02_preprocessing/cleaner.py`](../src/02_preprocessing/cleaner.py) và package `src/02_preprocessing/`.
    - Lọc bỏ 100% trận Remake và AFK.
    - Xử lý triệt để Missing Values: Impute `0` cho biến đếm mục tiêu, `'NoBan'` cho lượt cấm rỗng, phân luồng `datacompleteness` cho bài toán mốc 10 phút.
    - Khử ngoại lai linh hoạt qua 2 thuật toán: IQR ($1.5 \times IQR$) và Z-Score ($|Z| > 3.0$), hỗ trợ cả 2 chế độ Trimming (Lọc bỏ) và Winsorization (Cắt ngọn/Capping).
    - Xuất thành công 4 tập dữ liệu sạch vào `data/processed/`: `clean_ranked_10min.csv`, `clean_tournament_10min.csv`, `clean_tournament_draft.csv`, `clean_tournament_players.csv`.
  - *Acceptance Criteria:* Có thống kê số lượng bản ghi trước và sau khi lọc, tỷ lệ giữ lại đạt $> 96\%$ ở chế độ đồng thuận, không làm mất tính toàn vẹn dữ liệu. Hoàn thành 100%.

- [x] **Task 1.4 [Thành viên 1 + 2]: Viết 5 câu truy vấn SQL nâng cao theo Chương 5 & 5x**
  - *Mục tiêu:* Viết 5 câu truy vấn SQL phân tích nâng cao theo chuẩn giáo trình Chương 5 & 5x (Databases, SQL & Pandas) trên CSDL SQLite `data/database/lol_live_data.db`.
  - *Kết quả:* Đã hoàn thành [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql), [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py) và tài liệu [`src/03_database_sql/README.md`](../src/03_database_sql/README.md).
    - **Truy vấn 1:** Kèo đối đầu 1v1 (`Self-JOIN`, `GROUP BY`, `HAVING`) đánh giá tỷ lệ thắng và chênh lệch vàng/lính lúc 10 phút.
    - **Truy vấn 2:** Cặp đôi ăn ý đường dưới Xạ thủ + Hỗ trợ (`Intra-team JOIN`, `HAVING COUNT(*) >= 10`).
    - **Truy vấn 3:** Tướng có tỷ lệ Cấm/Chọn cao nhất (`Subqueries / CTE`, `Unpivot UNION ALL`).
    - **Truy vấn 4:** Xếp hạng tuyển thủ đè đường phút 10 (`Window Functions: DENSE_RANK()`, `PARTITION BY`, `AVG() OVER()`).
    - **Truy vấn 5:** Đối chiếu hiệu quả Lăn cầu tuyết Đấu Giải vs Solo Rank (`UNION ALL`, `CASE WHEN`).
    - Hỗ trợ CLI đa năng: `--query 1..5`, `--limit`, `--export`, xuất tự động 5 file CSV kết quả vào `data/processed/sql_query_*.csv`.
  - *Acceptance Criteria:* 100% truy vấn thực thi chính xác trên SQLite, trả về bảng dữ liệu phân tích nghiệp vụ rõ ràng, hỗ trợ xuất CSV. Hoàn thành 100%.

- [x] **Task 1.5 [Thành viên 1]: Xây dựng Module Đồng Bộ Dữ Liệu Tự Động từ Google Drive (Cloud Data Auto-Sync)**
  - *Mục tiêu:* Xây dựng module tự động kết nối thư mục Google Drive (`1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`) lưu trữ toàn bộ mùa giải Oracle's Elixir (2014-2026).
  - *Kết quả:* Đã hoàn thành module [`src/01_data_pipeline/sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py).
    - Hỗ trợ kiểm tra danh mục siêu nhẹ (`--list`), tự động bỏ qua nếu file cục bộ đã khớp dung lượng, hỗ trợ tải từng năm (`--year`), tải toàn bộ (`--all`) và ép buộc tải mới (`--force`).
    - Nâng cấp thuật toán quyết định mùa giải thông minh (ADR-013): Tự động phát hiện năm mới nhất; nếu chưa đủ số trận (`min_matches`), tự động ghép toàn bộ năm mới + trích xuất phần cuối năm trước (CKTG / Mùa Hè) cho đến khi đủ số lượng.
    - Hỗ trợ bộ lọc giải đấu linh hoạt (`--leagues LCK,LCP,LPL,MSI,WLDS,EWC`): Tự động trích xuất đúng các giải đấu chỉ định kết hợp các giải quốc tế danh giá (Worlds, MSI, EWC), xuất tệp hoạt động `data/raw/esports_active_matches.csv` (26.8 MB, 36,000 dòng, đúng 3,000 trận đỉnh cao: 1,774 trận từ 2026 + 1,226 trận từ cuối 2025). Tỷ lệ có Timeline 10 phút tăng vọt lên **79.0% (2,369 / 3,000 trận)**.
    - Bổ sung hàm chuyên dụng `filter_leagues()` và `filter_esports_by_leagues()` cùng cờ CLI `--filter --filter-leagues`.
    - Bổ sung hàm kiểm tra sức khỏe và độ sạch dữ liệu `check_data_health()` / `check_esports_data_health()` cùng cờ CLI `--check` xuất Data Health Card trực quan.
    - Cơ chế chống Quota Exceeded 2 tầng: Tầng 1 (gdown trực tiếp), Tầng 2 (Google Drive API v3 + OAuth 2.0 Desktop App qua cơ chế Smart Copy vào My Drive rồi tự dọn dẹp file tạm). Đã kiểm thử live thành công 100%.
    - Phân tách tài liệu chi tiết thành 2 file chuyên biệt [`README_CRAWL_RIOT.md`](../src/01_data_pipeline/README_CRAWL_RIOT.md) và [`README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md). Hoàn thành 100%.

- [x] **Milestone 1:** Nghiệm thu toàn bộ CSDL SQLite `lol_live_data.db` hoàn chỉnh cả 2 nguồn dữ liệu, module tiền xử lý dữ liệu sạch, bộ truy vấn SQL phân tích nâng cao và cơ chế đồng bộ tự động.

---

## 🔵 GIAI ĐOẠN 2: THỐNG KÊ SUY DIỄN & TRỰC QUAN HÓA EDA (CHƯƠNG 1, 3)

- [x] **Task 2.1 [Thành viên 2]: Kiểm định A/B Lợi thế Phe Xanh (Blue Side Advantage) qua $Z$-test 2 phía**
  - *Mục tiêu:* Thực hiện $Z$-test tỷ lệ 2 phía ($\alpha = 0.05$) để kiểm định giả thuyết: $H_0: p_{blue} = 0.5$ vs $H_1: p_{blue} \neq 0.5$.
  - *Kết quả:* Đã hoàn thành module [`src/04_hypothesis_testing/test_blue_side_advantage.py`](../src/04_hypothesis_testing/test_blue_side_advantage.py) và package `src/04_hypothesis_testing/`.
    - **Đấu Giải (Pro Play - 3,000 trận):** Tỷ lệ thắng Phe Xanh đạt **53.50%** (1,605 thắng), $Z = +3.8341$, $p\text{-value} = 0.000126 < 0.001$, CI 95%: $[51.72\%, 55.28\%]$ $\rightarrow$ **Bác bỏ $H_0$** (Phe Xanh có lợi thế First Pick và góc nhìn camera vượt trội có ý nghĩa thống kê cao).
    - **Solo Rank (1,009 trận):** Tỷ lệ thắng Phe Xanh đạt **45.49%**, Phe Đỏ đạt **54.51%**, $Z = -2.8648$, $p\text{-value} = 0.004173 < 0.01$ $\rightarrow$ **Bác bỏ $H_0$** (Phe Đỏ thắng cao hơn do thuật toán Matchmaking xếp đội có MMR cao hơn sang Phe Đỏ).
    - **Từng giải đấu:** LCP ($p=0.0262^*$), MSI ($p=0.0280^*$) đều bác bỏ $H_0$.
    - Xuất tệp kết quả: `data/processed/hypothesis_test_1_blue_side.csv`.
  - *Acceptance Criteria:* Chạy lệnh CLI không lỗi, xuất đầy đủ $Z$-score, $p$-value, khoảng tin cậy 95%, bảng số liệu và phân tích nghiệp vụ. Hoàn thành 100%.

- [x] **Task 2.2 [Thành viên 2]: Kiểm định Two-sample Welch's $t$-test & $Z$-test về Hiệu quả Lăn Cầu Tuyết (Snowball Lead $\ge 2,000$g lúc 10 phút)**
  - *Mục tiêu:* So sánh khả năng chuyển hóa chiến thắng, thời lượng trận đấu và tính ổn định khi dẫn $\ge 2,000$ vàng lúc 10 phút giữa Đấu Giải Chuyên Nghiệp (Pro Play) và Đấu Solo Rank Thách Đấu.
  - *Kết quả:* Đã hoàn thành module [`src/04_hypothesis_testing/test_snowball_effect.py`](../src/04_hypothesis_testing/test_snowball_effect.py), tài liệu phân tích chi tiết [`src/04_hypothesis_testing/test_snowball_effect.md`](../src/04_hypothesis_testing/test_snowball_effect.md) và xuất tệp số liệu [`data/processed/hypothesis_test_2_snowball.csv`](../data/processed/hypothesis_test_2_snowball.csv).
    - **1. Tỷ lệ thắng (Two-sample Proportion Z-test):** Pro Play thắng **83.48%** (192/230), Solo Rank thắng **86.04%** (339/394). $Z = -0.8671, p = 0.3859 > 0.05 \rightarrow$ **Chưa đủ bằng chứng bác bỏ $H_0$** (Cả 2 môi trường đều chuyển hóa thành thắng lợi $\sim 85-86\%$, sự chênh lệch là ngẫu nhiên).
    - **2. Thời lượng trận đấu (Welch's $t$-test):** Pro Play = **29.75 phút** vs Solo Rank = **24.46 phút**. $t = +11.4618, p = 1.16 \times 10^{-27} < 0.0001 \rightarrow$ **Bác bỏ $H_0$ cực kỳ mạnh mẽ** (Trận Solo Rank kết thúc nhanh hơn trung bình **5.3 phút** do cơ chế đầu hàng sớm FF15 và lối đánh giao tranh liên tục).
    - **3. Tính ổn định & Kỷ luật (Levene's Variance Test):** Độ lệch chuẩn Pro Play $\sigma = 4.68$ phút vs Solo Rank $\sigma = 6.80$ phút. $\text{Levene Stat} = 53.1630, p = 9.37 \times 10^{-13} < 0.0001 \rightarrow$ **Bác bỏ $H_0$** (Đấu Giải có tính kỷ luật, kiểm soát chặt chẽ và ít bị đột biến quăng game hơn).
    - **Phân tầng đa mốc:** Mở rộng kiểm định trên 4 mốc ($\ge 1,000$g, $\ge 1,500$g, $\ge 2,000$g, $\ge 3,000$g).
  - *Acceptance Criteria:* Chạy lệnh CLI hoàn hảo, xuất đủ 3 bài toán thống kê theo Giáo trình Chương 1, có bảng phân tầng và phân tích nghiệp vụ sâu sắc. Hoàn thành 100%.

- [x] **Task 2.3 [Thành viên 2]: Kiểm định Chi-square (χ²) & Tỷ Số Chênh (Odds Ratio): 3 Sâu Hư Không đầu vs Rồng 1**
  - *Mục tiêu:* Đánh giá mối quan hệ độc lập giữa việc kiểm soát mục tiêu trung lập (3 Sâu Hư Không đợt 1 vs Rồng Nguyên Tố đầu) và kết quả trận đấu; định lượng mức độ gia tăng cơ hội chiến thắng qua Odds Ratio (OR) và ma trận 4 kịch bản đối đầu.
  - *Kết quả:* Đã hoàn thành module [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.py), tài liệu phân tích chi tiết [`src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md`](../src/04_hypothesis_testing/test_voidgrubs_vs_dragon.md) và xuất tệp số liệu [`data/processed/hypothesis_test_3_objectives.csv`](../data/processed/hypothesis_test_3_objectives.csv).
    - **1. Đấu Giải (Pro Play):**
      - **Rồng Đầu Tiên (First Dragon):** Winrate **59.43%** vs **40.57%**, $\chi^2 = 167.39, p = 2.75 \times 10^{-38} < 0.0001$, $\text{Odds Ratio} = \mathbf{2.145}$ (CI 95%: $[1.910, 2.409]$) $\rightarrow$ Tăng cơ hội thắng gấp **2.15 lần**.
      - **3 Sâu Hư Không (Voidgrubs):** Winrate **55.81%** vs **46.96%**, $\chi^2 = 33.11, p = 8.73 \times 10^{-9} < 0.0001$, $\text{Odds Ratio} = \mathbf{1.427}$ (CI 95%: $[1.265, 1.609]$) $\rightarrow$ Tăng cơ hội thắng gấp **1.43 lần**.
      - **Đổi chéo mục tiêu (Cross-trade):** Đội chỉ ăn Rồng 1 (bỏ Sâu) thắng **55.92%**, đội chỉ ăn Sâu (bỏ Rồng) chỉ thắng **47.23%** (Rơi xuống dưới 50%!).
    - **2. Solo Rank (Thách Đấu):**
      - **Rồng Đầu:** $\text{Odds Ratio} = \mathbf{2.306}$ ($p = 1.60 \times 10^{-18}$).
      - **3 Sâu Hư Không:** $\text{Odds Ratio} = \mathbf{2.031}$ ($p = 2.67 \times 10^{-13}$) $\rightarrow$ Ở Solo Rank, 3 Sâu có giá trị cao hơn hẳn Pro Play do người chơi tự đẩy trụ lấy tiền giáp trụ (Plates) lăn cầu tuyết cá nhân.
    - **3. Kịch bản Double Neutral Control:** Đội ăn cả 2 (3 Sâu + Rồng 1) thắng **68.66%** ở Pro và **76.28%** ở Rank. Đội mất trắng cả 2 chỉ còn **35.90%** (Pro) và **36.42%** (Rank).
  - *Acceptance Criteria:* Chạy lệnh CLI hoàn hảo, tính đủ Chi-square, Odds Ratio, Woolf CI 95%, Relative Risk và ma trận 4 kịch bản. Hoàn thành 100%.

- [x] **Task 2.4 [Thành viên 2]: Trực quan hóa dữ liệu EDA (Bộ 5 biểu đồ 300 DPI - Chương 3)**
  - *Mục tiêu:* Thiết kế và xuất bản bộ 5 biểu đồ EDA theo chuẩn đồ họa nghiên cứu khoa học (Publication-Ready, 300 DPI) phân tích các đặc trưng kinh tế, mục tiêu và nhịp độ trận đấu mốc 10 phút.
  - *Kết quả:* Đã hoàn thành module [`src/05_visualization/plot_eda_figures.py`](../src/05_visualization/plot_eda_figures.py), tài liệu phân tích chuyên sâu [`src/05_visualization/plot_eda_figures.md`](../src/05_visualization/plot_eda_figures.md) và xuất 5 tệp hình ảnh 300 DPI vào thư mục [`reports/figures/`](../reports/figures/):
    - **Fig 1:** [`fig1_correlation_heatmap.png`](../reports/figures/fig1_correlation_heatmap.png) - Ma trận tương quan Pearson Heatmap (Tam giác trên).
    - **Fig 2:** [`fig2_gold_diff_distribution_kde.png`](../reports/figures/fig2_gold_diff_distribution_kde.png) - Phân phối chênh lệch vàng (Histogram + KDE Thắng vs Thua).
    - **Fig 3:** [`fig3_lane_economy_boxplot.png`](../reports/figures/fig3_lane_economy_boxplot.png) - Phân bố kinh tế & ngoại lai 5 vị trí thi đấu (Boxplot 1.5 IQR).
    - **Fig 4:** [`fig4_gold_lead_vs_duration_scatter.png`](../reports/figures/fig4_gold_lead_vs_duration_scatter.png) - Vàng dẫn trước 10p vs Thời lượng kết thúc trận (Scatter + Hồi quy OLS + Mốc Baron 20p/FF15).
    - **Fig 5:** [`fig5_neutral_objectives_scenarios_bar.png`](../reports/figures/fig5_neutral_objectives_scenarios_bar.png) - Ma trận 8 tổ hợp mục tiêu lớn (Rồng 1 x 0, 1, 2, 3 Sâu) đối chiếu Đấu Giải vs Solo Rank.
  - *Tài liệu giải thích chuyên sâu:* Đã xây dựng trọn bộ 6 tệp tài liệu trong thư mục [`docs/figure_explain/`](../docs/figure_explain/) (đồng bộ tại `reports/figures/figure_explain/`).
  - *Acceptance Criteria:* Chạy lệnh CLI trơn tru (hỗ trợ cả `--all` và `--fig 1..5`), xuất file ảnh 300 DPI sắc nét, có chú thích học thuật rõ ràng, không lỗi font Tiếng Việt. Hoàn thành 100%.

- [x] **Milestone 2:** Báo cáo Thống kê & EDA hoàn tất trong Notebook [`notebooks/01_kham_pha_du_lieu_EDA.ipynb`](../notebooks/01_kham_pha_du_lieu_EDA.ipynb). Tích hợp trọn vẹn 5 phần: Tổng quan CSDL SQLite (37,009 dòng), 5 Truy vấn SQL nâng cao, 3 Bài kiểm định Thống kê suy diễn (Z-test, Welch's t-test, Chi-square & Odds Ratio) và Bộ 5 biểu đồ EDA 300 DPI kèm diễn giải học thuật chuyên sâu. Đã thực thi và lưu trữ trọn vẹn kết quả bảng số liệu + hình ảnh render sẵn. Hoàn thành 100%.

---

- [x] **Task 3.1 [Thành viên 3]: Xây dựng Mô hình Draft Prediction lúc cấm chọn (Phút 0)**
  - *Mục tiêu:* Dự đoán xác suất thắng thua dựa hoàn toàn vào 10 tướng cấm/chọn trước khi trận đấu bắt đầu.
  - *Phương pháp & Kỹ thuật:*
    - Trích xuất 3,000 trận đấu giải đỉnh cao (6,000 dòng đội) từ CSDL SQLite `lol_live_data.db`.
    - Xây dựng Pipeline đặc trưng đa tầng 799 chiều (Position-specific One-hot 790 cột, Bayesian Champion Winrate, 5 cặp đối đầu Lane Matchup, 2 cặp phối hợp Synergy Duo Mid-Jng/Bot-Sup, Vector cân bằng đội hình AD/AP/CC/Scaling và Trọng số thời gian Half-life 90 ngày).
    - So sánh 4 mô hình: Random Forest (ROC-AUC: 0.5510, Brier: 0.2487), Logistic Regression L2 (Accuracy: 54.33%), Ensemble Soft Voting (ROC-AUC: 0.5492) và MLP.
  - *Kết quả & Artifacts:*
    - Module mã nguồn: [`src/06_machine_learning/draft_model.py`](../src/06_machine_learning/draft_model.py).
    - Báo cáo khoa học: [`src/06_machine_learning/draft_model.md`](../src/06_machine_learning/draft_model.md).
    - Đóng gói mô hình tối ưu: [`models/draft_model.pkl`](../models/draft_model.pkl). Hỗ trợ CLI `--train` và `--predict`. Hoàn thành 100%.
- [x] **Task 3.2 [Thành viên 3]: Xây dựng Mô hình Snowball Prediction trong trận (Phút 10)**
  - *Mục tiêu:* Dự đoán xác suất thắng thua dựa trên chỉ số kinh tế, mạng hạ gục và mục tiêu lớn đạt được ở mốc 10 phút.
  - *Phương pháp & Kỹ thuật:*
    - Tích hợp 6,770 quan sát trận đấu mốc 10 phút (4,752 Pro Play + 2,018 Solo Rank Thách Đấu).
    - Xây dựng 22 đặc trưng chiến thuật: Macro Economy (`golddiffat10`, `xpdiffat10`, `csdiffat10`), Combat (`killsat10`, `deathsat10`, `kill_diff`, `kda_ratio`), 5 Lanes (`top_golddiff`, `jng_golddiff`, `mid_golddiff`, `bot_golddiff`, `sup_golddiff`), `carry_gold_lead` (Mid + Bot), Mục tiêu trung lập (`firstdragon`, `void_grubs`, `has_3_grubs`, `firsttower`, `double_neutral_control`), Synergies (`gold_dragon_synergy`, `gold_grubs_synergy`) và Match Context (`is_blue_side`, `is_pro_play`).
    - So sánh và đánh giá đa thuật toán: Random Forest (150 trees), XGBoost Classifier, LightGBM Classifier, Logistic Regression (L2) và Soft Voting Ensemble.
    - Đánh giá phân tầng: Đấu Giải Pro Play (Accuracy: 69.47%, ROC-AUC: 0.7572) vs Đấu Xếp Hạng Solo Rank (Accuracy: 73.54%, ROC-AUC: 0.8189). Kịch bản lăn cầu tuyết dẫn >= 2,000 vàng + 1 Rồng + 3 Sâu đẩy tỷ lệ thắng dự đoán lên **83.23%**.
  - *Kết quả & Artifacts:*
    - Module mã nguồn: [`src/06_machine_learning/snowball_model.py`](../src/06_machine_learning/snowball_model.py).
    - Báo cáo khoa học: [`src/06_machine_learning/snowball_model.md`](../src/06_machine_learning/snowball_model.md).
    - Đóng gói mô hình tối ưu: [`models/snowball_model.pkl`](../models/snowball_model.pkl). Hỗ trợ CLI `--train` và `--predict`. Hoàn thành 100%.
- [x] **Task 3.3 [Thành viên 3]: Đánh giá mô hình & Xuất bản bộ biểu đồ chẩn đoán (ROC-AUC, Confusion Matrix, Feature Importance)**
  - *Mục tiêu:* Đánh giá toàn diện và trực quan hóa hiệu năng của cả 2 mô hình (Draft Phút 0 vs Snowball Phút 10) theo chuẩn đồ họa nghiên cứu khoa học 300 DPI.
  - *Phương pháp & Kỹ thuật:*
    - Đánh giá trên tập kiểm thử độc lập: ROC-AUC Curves, Precision-Recall Curves, Confusion Matrix Heatmaps, Probability Calibration Curves (Reliability Diagrams) và Brier Scores.
    - So sánh cấu trúc trọng số đóng góp của các nhóm đặc trưng (Feature Importance).
  - *Kết quả & Artifacts:*
    - Module mã nguồn: [`src/06_machine_learning/evaluate_models.py`](../src/06_machine_learning/evaluate_models.py).
    - Báo cáo khoa học: [`src/06_machine_learning/evaluation_report.md`](../src/06_machine_learning/evaluation_report.md).
    - Bộ 4 biểu đồ 300 DPI trong [`reports/figures/`](../reports/figures/): `fig6_roc_auc_comparison.png`, `fig7_confusion_matrices.png`, `fig8_calibration_curve.png`, `fig9_draft_vs_snowball_feature_importance.png`. Hoàn thành 100%.
- [x] **Task 3.4 [Thành viên 3]: Phân cụm K-Means & PCA Nhận diện 4 Trường phái Đội hình (Draft Archetypes - Chương 4)**
  - *Mục tiêu:* Vector hóa 159 tướng theo 5 trục sức mạnh `[Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control]`. Dùng K-Means + PCA gom cụm 6,000 đội hình giải đấu nhận diện 4 trường phái đội hình: Early Snowball / Dive, Wombocombo & Objective Control, Late-Game Hypercarry, Pick & Split-Push 1-3-1.
  - *Phương pháp & Kỹ thuật:*
    - Khảo sát tìm K tối ưu qua Elbow Method (WCSS giảm mạnh từ 21,122 về 15,966 tại K=4) và Silhouette Analysis (0.1799).
    - Giảm chiều PCA 2D giải thích 68.98% phương sai tích lũy (PC1: 45.95% Tempo, PC2: 23.03% Combat Scale).
    - Trích xuất Thẻ Điều kiện thắng (Win Condition) và Điểm yếu chí mạng (Critical Weakness) cho từng trường phái.
  - *Kết quả & Artifacts:*
    - Module mã nguồn: [`src/06_machine_learning/cluster_archetypes.py`](../src/06_machine_learning/cluster_archetypes.py).
    - Báo cáo khoa học: [`src/06_machine_learning/cluster_archetypes.md`](../src/06_machine_learning/cluster_archetypes.md).
    - Đóng gói mô hình: [`models/archetype_kmeans.pkl`](../models/archetype_kmeans.pkl). Hỗ trợ CLI `--train` và `--predict`.
    - Bộ 2 biểu đồ 300 DPI trong [`reports/figures/`](../reports/figures/): `fig10_kmeans_elbow_silhouette.png`, `fig11_draft_archetypes_pca_clusters.png` kèm tài liệu giải thích chi tiết trong `docs/figure_explain/`. Hoàn thành 100%.
- [x] **Task 3.5 [Thành viên 3 + 1]: Hệ thống Gợi ý Cấm/Chọn Thông Minh (Hybrid Opponent Target Ban, Meta Recommender & Punisher Engine) & Engine Phân tích Điều kiện thắng (Win Condition Card - ADR-014)**
  - *Mục tiêu & Cơ chế:*
    - **1. Phân hệ CẤM lai ghép mục tiêu theo Tuyển thủ Đối phương (Hybrid Opponent Target Ban):** 
      - *Trọng số Đấu Giải (60-70%):* Khai thác 30,000 dòng `tournament_players` trong SQLite, tính điểm nguy hiểm/tướng tủ ổn định (Bayesian Smoothed Winrate + 10m Laning Dominance) của tuyển thủ đối phương (ví dụ: Keria -> Bard/Renata, Kiaya -> Rumble/Renekton, Chovy -> Yone/Ahri). Tự động nhận diện hồ sơ tân binh ngay khi có trận đấu giải mới.
      - *Trọng số Solo Rank Gần Nhất (30-40% - Hidden Weapon / Pocket Pick Detector):* Tích hợp cơ chế Pro Player Registry (`data/pro_player_accounts.json`) và Riot Games Account API (PUUID) để cào 20-50 trận Rank Thách Đấu gần nhất của tuyển thủ đối phương, phát hiện bài dị đang bí mật spam luyện tập (Spike in Pick Rate & Winrate > 65%).
      - *Cơ chế Cập nhật & Tự học Tuyển thủ Mới:* Hỗ trợ CLI/API link tài khoản Rank mới (`--link-player "Player" --riot-id "Name#Tag"`) và cơ chế Fallback an toàn về dữ liệu giải đấu nếu chưa có Riot ID.
      - *Đầu ra:* Tự động xuất **Top 3-5 tướng bắt buộc phải CẤM (Target Ban & Pocket Pick Alert 🚨)**.
    - **2. Phân hệ CHỌN theo Chuẩn Meta & Khắc chế Đội hình (Meta-based Pick Recommender):** Gợi ý chọn tướng tối ưu dựa trên Counter-Pick đối đầu lane trực tiếp, Synergy Duo (Mid-Jungle, Bot-Sup) và bù đắp thuộc tính đội hình (AD/AP/CC/Engage). Độ thuận tay của phe mình sẽ để người chơi/tuyển thủ tự quyết định bên ngoài.
    - **3. Phân hệ NHẬN DIỆN LỖ HỔNG CẤM/CHỌN CỦA ĐỊCH & GỢI Ý CON BÀI TRỪNG PHẠT (Draft Flaw & Punisher Recommender):**
      - Tự động quét Vector thuộc tính đội hình địch để phát hiện 4 lỗ hổng chí mạng:
        - *Lỗ hổng 1 (Heavy Melee - Đối thủ pick 3-4 tướng cận chiến/tay ngắn):* Tự động bật cảnh báo đỏ và đẩy điểm gợi ý con bài trừng phạt chống càn diện rộng lên Top 1 (ví dụ: **Illaoi, Darius, Mordekaiser, Cassiopeia, Brand** - tăng vọt +15% đến +20% Winrate dự đoán như trận Siwoo Illaoi).
        - *Lỗ hổng 2 (Full AD - Thiếu sát thương phép):* Gợi ý siêu đỡ đòn giáp (**Malphite, Rammus, K'Sante, Taric**).
        - *Lỗ hổng 3 (Zero Hard CC - Thiếu khống chế cứng):* Gợi ý siêu sát thủ/quẩy giao tranh (**Master Yi, Katarina, Irelia, Zeri**).
        - *Lỗ hổng 4 (Full Squishy - Máu giấy/Thiếu mở combat):* Gợi ý càn quét mở giao tranh (**Nocturne, Jarvan IV, Hecarim, Akali**).
    - **4. Engine Phân tích Điều kiện thắng (Win Condition Card - ADR-014):** Tự động trích xuất Thẻ chiến thuật chỉ rõ: Chủ lực gánh đội (Core Carry), Điểm rơi sức mạnh (Power Spike Timing), Mục tiêu ưu tiên số 1 (Primary Objective) và Điều kiện thua cần tránh (Lose Condition).
  - *Kết quả & Artifacts:*
    - Module mã nguồn: [`src/07_recommender/recommender_engine.py`](../src/07_recommender/recommender_engine.py).
    - Báo cáo khoa học: [`src/07_recommender/recommender_engine.md`](../src/07_recommender/recommender_engine.md).
    - Danh mục tuyển thủ & Rank tracking: [`data/pro_player_accounts.json`](../data/pro_player_accounts.json).
    - Đóng gói mô hình: [`models/recommender_engine.pkl`](../models/recommender_engine.pkl). Hỗ trợ đầy đủ CLI và demo 4 phân hệ. Hoàn thành 100%.
- [x] **Milestone 3:** Toàn bộ Giai đoạn 3 (Machine Learning, Phân Cụm & Ban/Pick AI) hoàn thành 100%. Đã xuất các file mô hình `models/draft_model.pkl`, `models/snowball_model.pkl`, `models/archetype_kmeans.pkl`, `models/recommender_engine.pkl`, cùng hệ thống biểu đồ chẩn đoán Fig 6 - 11 (300 DPI) và báo cáo khoa học chi tiết. Sẵn sàng tiến sang Giai đoạn 4 (REST API FastAPI & Web App).

### 📝 TỔNG KẾT NHỮNG CẢI TIẾN ĐÃ THỰC HIỆN TRÊN HỆ THỐNG RECOMMENDER:
1. **Khử Thiên Kiến Mẫu Nhỏ (Small Sample Bias Removal):**
   - Triệt tiêu hoàn toàn lỗi "ảo điểm" (ví dụ: Rek'Sai Jungle 2 trận thắng 100% bị tính là Tier S+ 99.0%).
   - Tích hợp kỹ thuật Bayesian Shrinkage kéo tỷ lệ thắng về mốc tiên nghiệm 50% đối với mẫu nhỏ, kết hợp Sample Confidence Weighting để ưu tiên các kèo đấu có độ tin cậy thống kê cao.
2. **Đồng Bộ Bộ Lọc Cấm/Chọn Theo Vị Trí (`top`, `jng`, `mid`, `bot`, `sp`):**
   - Khắc phục lỗi lọc theo vị trí bị mất tướng (ví dụ: Karma ở bảng tổng hợp Phase 1 nhưng gõ `sp` lại biến mất).
   - Truyền tham số `ban_phase` (Phase 1 vs Phase 2) chuẩn xác, đồng bộ hóa giữa cấm theo Meta và cấm mục tiêu tướng tủ của đối phương.
3. **Nâng Cấp Hệ Thống Mô Phỏng Cấm/Chọn Đấu Giải ([`simulate_draft_match.py`](../src/07_recommender/simulate_draft_match.py)):**
   - Hỗ trợ người dùng điều khiển tương tác linh hoạt ở cả **Phe Xanh (Blue Side - First Pick)** lẫn **Phe Đỏ (Red Side - Counter Last Pick)**.
   - Thêm Menu chọn kịch bản trực quan: Hỗ trợ kịch bản đặc biệt **"ĐỘI VÔ DANH (Bạn) vs T1"**, GAM vs T1, T1 vs GEN.G và Tùy chỉnh tự do.
   - Cơ chế cấm/chọn thích ứng: Khi đối đầu Đội Vô Danh, AI tự động cấm theo chuẩn Meta toàn cầu; khi đối đầu T1, hệ thống bóc tách toàn bộ CSDL tướng tủ của Faker, Oner, Keria, Doran, Peyz để cấm và phản đòn.
4. **Hệ Thống Khắc Chế & Đi Đường Tổng Quát (Universal Counter-Pick vs Blind-Pick Engine - ADR-016) & Phân Tầng Khu Vực (ADR-015):**
   - **Phân tầng Meta Khu vực & Giải đấu Quốc tế (`LCK`, `LPL`, `LCP`, `WLDS`/CKTG, `MSI`, `EWC`, `INTERNATIONAL`, `ALL`):** Tách biệt thống kê cấm/chọn, kèo đối đầu 1v1, cặp đôi Synergy và hồ sơ tuyển thủ theo từng giải đấu, kết hợp công thức hòa trộn thích ứng ($w_{\text{reg}} = \frac{n_{\text{reg}}}{n_{\text{reg}} + \tau}$).
   - **Nhận diện 1-1 Tướng Đối Thủ Cùng Đường (`_infer_enemy_lane_assignment`):** Truyền trực tiếp `picks_dict` & `enemy_picks_dict` trong mô phỏng và tự động giải bài toán phân bổ 1-1 vị trí khi truyền danh sách tướng qua CLI.
   - **Bộ Lọc Ngắt Cứng Tổng Quát (Universal Hard Cut-off Filter cho cả 5 vị trí & 3,098 cặp kèo 1v1):** Khi đối thủ đã lộ tướng cùng đường (`Counter-Pick Mode`), tự động loại bỏ mọi ứng viên có Winrate đối đầu $< 47.5\%$ (mẫu $\ge 3$ trận) HOẶC bị thua thiệt kinh tế phút thứ 10 (`GD@10 < -110 vàng` đối với `Top/Jng/Mid/Bot`, `< -150 vàng` đối với `Sup` nếu không có tỷ lệ lật kèo giao tranh $\ge 52.5\%$).
   - **Khóa Điểm Tướng Tủ (`player_bonus`) Khi Gặp Kèo Dưới:** Cắt giảm 85% – 90% điểm cộng tướng tủ nếu tướng tủ rơi vào kèo thua hoặc chưa được kiểm chứng đối đầu với tướng địch cùng đường.
   - **Làm Mịn Bayes (`C = 10.0`), Độ Tin Cậy Mẫu (`n / (n + 8)`) & Lọc Độ Tinh Khiết Vị Trí (Role Purity Filter):** Ngăn các tướng trái vị trí có mẫu siêu nhỏ (2–5 trận) làm nhiễu gợi ý khắc chế.
   - **Tài liệu kỹ thuật chuyên sâu:** Đã ghi nhận đầy đủ tại [`docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md`](../docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md).

---

### 📌 ĐỊNH HƯỚNG BẮT BUỘC QUAY LẠI XEM XÉT & CẢI THIỆN TOÀN DIỆN (GLOBAL ROADMAP BACKLOG)
> **ĐÁNH DẤU:** Sau này bắt buộc phải rà soát và đánh giá lại **TOÀN BỘ hệ thống Ma trận Kèo Đấu (Head-to-Head Matchup Matrix)** trên tất cả các vị trí (Top, Jungle, Mid, Bot, Support) chứ không chỉ dừng lại ở một vài cặp tướng riêng lẻ:

1. **Rà soát Toàn bộ Ma trận Đối đầu Trực tiếp (Global Head-to-Head Matrix Review):**
   - Khảo sát lại tương tác giữa cả 173 vị tướng trên cả 5 vị trí để đối chiếu giữa **Cảm nhận người chơi (Perception / Lý thuyết kỹ năng 1v1)** và **Dữ liệu thực chiến (Reality / Pro Play + High Elo)**.
   - Xử lý các cặp đấu "bẫy" tương tự (nhìn lý thuyết thì tưởng kèo trên nhưng thực tế vận hành macro lại là kèo dưới do thua thiệt về tốc độ dọn quái, nhịp độ di chuyển hoặc khả năng đóng góp giao tranh).
2. **Nâng cấp Đánh giá Kèo Đấu Đa Biến Theo Ngữ Cảnh (Context-Aware Matchup Evaluation):**
   - Kèo đấu cùng đường không tồn tại cô lập: Cần tích hợp thêm yếu tố thế trận 2 cánh và rừng đồng minh.
   - Xem xét lại những vị tướng có kỹ năng đảo đường toàn bản đồ (Pantheon, Twisted Fate, Shen, Galio, Taliyah): Cần đánh giá bài toán **Đánh đổi Tài nguyên Chéo Bản đồ (Macro Cross-Map Tradeoff)** — chi phí cơ hội khi một tướng bỏ đường/bỏ rừng đi can thiệp so với lượng tài nguyên bị mất ở cánh đối diện.
3. **Phân Tách Rạch Ròi giữa "Kèo Đi Rừng (Jungle Tempo)" và "Kèo Đường Đơn (Lane 1v1)":**
   - Cùng một cặp tướng, khi gặp nhau ở Đường Trên/Đường Giữa có thể mang tính chất khác hoàn toàn so với khi cùng Đi Rừng (nơi tốc độ dọn quái và khả năng vượt địa hình quyết định toàn bộ ván đấu).
4. **Hệ Thống Giải Thích Minh Bạch Đa Chiều (Multi-Dimensional Explainability Engine):**
   - Nâng cấp giao diện hiển thị để không chỉ đưa ra một điểm số thuần túy, mà cung cấp bảng so sánh rõ ràng: *"Ưu thế về kỹ năng đối kháng vs Rủi ro về nhịp độ bản đồ / macro"*, giúp người chơi và ban huấn luyện hiểu sâu sắc bản chất chiến thuật đằng sau mỗi gợi ý.

---

## 🟣 GIAI ĐOẠN 4: ĐÓNG GÓI REST API (FASTAPI) & DỰNG WEB APP TƯƠNG TÁC

- [ ] **Task 4.1 [Thành viên 1]:** Xây dựng Backend REST API bằng **FastAPI** (`src/api/`):
  - `POST /api/v1/predict`: Dự đoán tỉ lệ thắng 2 giai đoạn (Phút 0 & Phút 10).
  - `GET /api/v1/champions`: Danh sách 173 tướng + Vector thuộc tính.
  - `POST /api/v1/target-ban`: Phân tích và gợi ý CẤM mục tiêu theo 5 tuyển thủ đối phương (kết hợp Đấu Giải + Solo Rank).
  - `POST /api/v1/players/link-account`: Thêm / Cập nhật tài khoản Riot ID Rank cho tuyển thủ mới.
  - `POST /api/v1/recommend`: Gợi ý chọn tướng cấm/chọn tối ưu theo Meta (Counter & Synergy).
  - `POST /api/v1/detect-flaws`: Quét đội hình địch và trả về Cảnh báo Lỗ hổng + Gợi ý Con bài Trừng phạt (Punisher Picks).
  - `POST /api/v1/win-condition`: Trích xuất Radar Chart 5 trục & Thẻ điều kiện thắng của đội hình (ADR-014).
  - `GET /api/v1/analytics`: Số liệu thống kê Meta giải đấu & Rank.
- [ ] **Task 4.2 [Thành viên 1 + 3]:** Xây dựng Giao diện Web App tương tác (`web/` hoặc Streamlit) tích hợp chọn Tuyển thủ đối phương, Thẻ cảnh báo Lỗ hổng & Con bài Trừng phạt (Punisher Card), Radar Chart 5 trục và Thẻ chiến thuật Win Condition trực quan.
- [ ] **Milestone 4:** Demo hoàn chỉnh Web App kết nối API phục vụ môn Nhập môn Khoa học Dữ liệu.

---

## 🔴 GIAI ĐOẠN 5: BÁO CÁO TỔNG KẾT & BẢO VỆ ĐỒ ÁN

- [ ] **Task 5.1 [Cả nhóm]:** Viết báo cáo tổng kết đồ án Word/PDF.
- [ ] **Task 5.2 [Cả nhóm]:** Thiết kế Slide thuyết trình PowerPoint.
- [ ] **Task 5.3 [Cả nhóm]:** Tổng duyệt demo Web App trực tiếp và bảo vệ đồ án trước hội đồng.
- [ ] **Milestone 5:** Hoàn thành bảo vệ đồ án môn Nhập môn Khoa học Dữ liệu với kết quả cao nhất.


---

[ ] Integrity remediation: kiểm chứng signed differences, loại thông tin sau phút 10, CUDA retrain, calibration, grouped bootstrap, historical recommender + ranking benchmark; cập nhật kết quả sau chạy.
