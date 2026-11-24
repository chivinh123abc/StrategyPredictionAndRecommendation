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
