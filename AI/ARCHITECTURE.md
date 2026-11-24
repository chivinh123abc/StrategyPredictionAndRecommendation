## Hiện hành: chỉ legacy và contextual — 2026-11-24

Theo yêu cầu người dùng, đã BỎ lookahead khỏi mã ban và CLI; không chỉ ẩn menu. BanPlanner chỉ còn one-stepcontextual, ContextualBanPolicy(top3pool/owncost). Gỡ response_distribution/evaluate_root/rollout/leaf/predictor dependency và --ban-response-model; --ban-strategy chỉ legacy|contextual, legacygiữmặcđịnh. Contextual dùng pool_impact/contextual_trace, không xuất search_trace/branches/sensitivity. OpponentModelcũ giữ độc lập, không được contextual dùng đểban; không mởrộngchứcnăngkhác.

VERIFIED:57testsPASS;2seriesT1–Gen.GWorldscutoff13/11patchdataset16.20đều5draft/100actions/50uniquePicks,locks0/10/20/30/40, testtop1override. Pick/ban của cảlegacy/contextual giống phiêntrước (đã so cả100lượtmỗiseries); CLIonegame vàseries từchốilookahead(exit2), helpkhôngcònban-response-model. Newoutputs khôngsearchfields. Báocáohiệnhành reports/legacy_contextual_comparison/{COMPARISON.md,comparison.json,checks.json,legacy/,contextual/}; doc docs/BAN_LEGACY_VA_CONTEXTUAL.md. Khôngtrainmodel/đổiDB/raw. Tài liệu vàreportlookaheadcũđánh dấuLỊCHSỬ, khôngxóa artifact/minhchứng; cácmốcbêndướilàlịch sử trướcquyếtđịnhnày.

## Hoàn tất3mục ban ngữ cảnh, rollout phản ứng và đối chiếu5draft — 2026-11-24

VERIFIED: ban_planner.py/BanPlanner có contextual pool loss địch trừ self-denial theo thứ tựpick thật/roster/Fearless; lookahead shortlist6ban,2response ởfirstopponentturn rồigreedyđến3pick mới/max12plies. OpponentModelđãcó dùng inference, khôngfitmới; fallbacksoftmaxcónhãn. Không épdiversity, khôngcasechampion/team. Mặc địnhlegacy đểtáilập; bật --ban-strategy contextual|lookahead, --ban-response-model PATH. Trace lưu mọiroot/branch/leaf/coverage/omittedmass và sensitivitybounds (khôngCIthốngkê), why/REPORTgiảithích theo lượt.

57testsPASS; so3seriesT1–Gen.GWorlds cùngcutoff13/11patchdataset16.20/rosters/lịchfirstpick, testoverrideTrue theoủyquyền. Mỗi5draft100actions50uniquePicks, khóa0/10/20/30/40; 583branchpaths/295rootreplay hợp lệ, sâu tốiđa9<12. Tập6ban đầu:legacy1tập lặp5ván, contextual5,lookahead5; Jaccard1/.471/.145, khôngclaimđadạng=tốthơn. Lookahead~.471s/banmean,p95.787s,max1.371s trênlầnchạy;cócache. 23/50ban kháccontexttop1. Giữ2response chỉphủmean21.1%khốihỗtrợ,min5.8%;48/50sensitivityboundsoverlap. 41/50pickvẫnthiếucontextđủmẫu. Chưaindependentbanqualitybenchmark/counterevaluator/fullflex hoặcfullBO5plannerđểdànhtướng.

Artifacts: reports/ban_strategy_comparison/COMPARISON.md,comparison.json,checks.json và{legacy,contextual,lookahead}/{QUICK_VIEW.md,REPORT.md,series.json,game_1..5.json/log}. Sổkiếnthứcmục14/MR-13/KH-02 cậpnhật; docs/BAN_NGU_CANH_VA_LOOKAHEAD.md. KhôngđổiDB/schema/raw, khôngtrainmodel, khôngcommit/push. Trạngtháidừngtrướcđượcusergiaotiếprõ3mục; phạmvihoànthànhtạibảnrolloutgiớihạnnày.

## Test đủ5draft T1–Gen.G theo yêu cầu — 2026-11-24

VERIFIED: thêm --allow-statistical-auto cho series, defaultFalse không đổi. User yêu cầu test thiếu tin cậy vẫn chọn số1; toàn bộ5ván chạyTrue, không manualreviewstop nhưng vẫn giữreview_required/counterstatus/coverage. Worlds cutoff13/11 patchdataset16.20.100actions/50uniquePicks, locks0/10/20/30/40 vàvalidate_gamePASS; 38pick thiếu đối đầu đủ mẫu có nhãn. Report dùng đúng tên2đội vàBan1..5/Pick1..5mỗiđội kèmturn1..20. reports/t1_geng_bo5_test_20261124/REPORT.md,QUICK_VIEW.md,series.json,checks.json. Khôngtạo tỉsố hoặc chứngminhcounter/tốiưu. Khôngfitmodel/đổiDB hoặcphươngphápthốngkê. Lượt này chỉ mởtestoverride trongdriver vàđánh sốreport; khôngtiếptụcsearch/planner.

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

Luồng hiện hành: raw SQLite (read-only) → `src/analysis_data.py` → canonical snapshots/CSV → SQL, EDA, statistics, Draft/Snowball và historical recommender. `validation.py` điều phối partitions, expanding historical encoding, CUDA model selection, calibration, CI và provenance. `evaluate_models.py` dùng test manifest đã lưu; không tạo lại test theo số dòng mới. Rank grouped random do thiếu event time; Pro chronological. REST API/web vẫn Planned.

---

NỘI DUNG LỊCH SỬ / KẾ HOẠCH TRƯỚC INTEGRITY V2:

# SYSTEM ARCHITECTURE (KIẾN TRÚC HỆ THỐNG)

Dự án áp dụng mô hình **Kiến trúc phân tầng hướng dịch vụ (Decoupled / API-First Architecture)** kết nối trực tiếp tầng Khoa học Dữ liệu & Học máy với Giao diện Web App tương tác.

---

## 1. SƠ ĐỒ TỔNG THỂ HỆ THỐNG

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TẦNG 1: DỮ LIỆU & TRÍ TUỆ NHÂN TẠO              │
│       (Data Engineering, Machine Learning & Ban/Pick Recommender)       │
│                                                                        │
│   [Dữ liệu Solo Rank (Riot API)]       [Dữ liệu Esports (Oracle's)]   │
│                 │                                    │                 │
│                 └──────────────┬─────────────────────┘                 │
│                                ▼                                       │
│                [Làm sạch & Chuẩn hóa 1NF / 3NF]                        │
│                                ▼                                       │
│                  [CSDL Quan hệ SQLite (.db)]                           │
│                                │                                       │
│                 ┌──────────────┴──────────────┐                        │
│                 ▼                             ▼                        │
│     [Kiểm định Thống kê & EDA]     [Huấn luyện AI (XGBoost/RF)]        │
│        (Chi-Square, T-Test)          (Acc > 75%, Xuất model .pkl)      │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         TẦNG 2: CỔNG GIAO TIẾP DỊCH VỤ                 │
│                     (Backend REST API - FastAPI & Uvicorn)             │
│                                                                        │
│   • POST /api/v1/predict      : Dự đoán tỉ lệ thắng (% Winrate)        │
│   • GET  /api/v1/champions    : Danh sách 173 tướng + Stats            │
│   • POST /api/v1/recommend    : Gợi ý cấm/chọn (Ban/Pick AI)           │
│   • GET  /api/v1/analytics    : Số liệu thống kê Meta giải đấu         │
│   • Tự động sinh giao diện kiểm thử Swagger UI (/docs)                 │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│               TẦNG 3: GIAO DIỆN WEB APP TƯƠNG TÁC                      │
│          (Web Dashboard / Streamlit - Môn Khoa Học Dữ Liệu)            │
│                                                                        │
│   • Giao diện Web tương tác mô phỏng Cấm/Chọn & Dự đoán 2 giai đoạn    │
│   • Trực quan hóa biểu đồ EDA, Radar Chart 5 trục & Win Condition Card │
│   • Phục vụ báo cáo & demo trực tiếp môn Nhập môn Khoa học Dữ liệu     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. PHÂN TRÁCH NHIỆM TỪNG MODULE (MODULE BOUNDARIES)

### `src/01_data_pipeline/`
- Chịu trách nhiệm: 
  - [`crawl_riot_matches.py`](../src/01_data_pipeline/crawl_riot_matches.py): Gọi Riot Games API (Live Rank VN2, KR), xử lý rate limit HTTP 429 qua Exponential Backoff, trích xuất chỉ số mốc phút thứ 10, chuẩn hóa 1NF & 3NF (Xem [`README_CRAWL_RIOT.md`](../src/01_data_pipeline/README_CRAWL_RIOT.md)).
  - [`sync_google_drive.py`](../src/01_data_pipeline/sync_google_drive.py): Tự động quét và đồng bộ dữ liệu giải đấu từ Google Drive dùng chung; áp dụng Smart Caching manifest và thuật toán regex tự động đón đầu mùa giải mới nhất (2026, 2027...) (Xem [`README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md)).
- Đầu ra: Bảng `matches_10min` trong SQLite `lol_live_data.db`, file CSV `lol_live_ranked_10min.csv` và dữ liệu thô các mùa giải tại `data/raw/*.csv`.

### `src/02_preprocessing/`
- Chịu trách nhiệm: Đọc dữ liệu thô (cả Rank và Esports), lọc bỏ trận Remake/AFK, phát hiện và xử lý giá trị ngoại lai (IQR & Z-score).
- Đầu ra: Dữ liệu sạch đưa vào CSDL và các tập train/test.

### `src/03_database_sql/`
- Chịu trách nhiệm: Quản lý cấu trúc schema CSDL SQLite `lol_live_data.db`, thực thi 5 câu truy vấn SQL phân tích nâng cao (Chương 5, 5x).
- Đầu ra: Các bảng quan hệ và view dữ liệu phân tích.

### `src/04_hypothesis_testing/`
- Chịu trách nhiệm: Thực hiện các phép kiểm định thống kê suy diễn: $Z$-test (Lợi thế Phe Xanh), Two-sample $t$-test (Lăn Cầu Tuyết Đấu giải vs Rank), Chi-Square (Mục tiêu lớn Rồng vs Sâu Hư Không).

### `src/05_visualization/`
- Chịu trách nhiệm: Sinh bộ 5 biểu đồ phân tích EDA độ phân giải cao 300 DPI lưu vào `reports/figures/`.

### `src/06_machine_learning/`
- Chịu trách nhiệm: Huấn luyện mô hình 2 giai đoạn:
  - Tầng 1: Draft Prediction (Phút 0 - cấm chọn).
  - Tầng 2: Snowball Prediction (Phút 10 - kinh tế/mục tiêu).
- Đánh giá: ROC-AUC, Confusion Matrix, Feature Importance.
- Đầu ra: File mô hình `draft_model.pkl`, `snowball_model.pkl`.

### `src/07_recommender/`
- Chịu trách nhiệm: Thuật toán gợi ý tướng khắc chế (Counter Pick) và tương thích đồng đội (Synergy Pick).
- Đầu ra: File `recommender.pkl`.

### `src/api/` (Planned)
- Chịu trách nhiệm: Đóng gói các hàm của tầng ML và Database thành các endpoint RESTful HTTP bằng FastAPI.

### `web/` (Planned)
- Chịu trách nhiệm: Giao diện Web tương tác trình diễn trực tiếp cho giảng viên môn Nhập môn Khoa học Dữ liệu.

---

## 3. TIÊU CHUẨN MÔI TRƯỜNG THỰC THI (RUNTIME ENVIRONMENT STANDARD)

- **Môi trường ảo nội bộ (.venv):** Tọa lạc tại `d:\Chivinh\2026_MonHoc\Nhập môn khoa học dữ liệu\Project\.venv` sử dụng **Python 3.13.14**.
- **Cấu hình IDE:** Tự động nhận diện qua `.vscode/settings.json` (`python.defaultInterpreterPath`).
- **Lệnh kích hoạt nhanh:**
  - PowerShell: `.\.venv\Scripts\Activate.ps1`
  - Command Prompt: `.\.venv\Scripts\activate.bat`
  - Git Bash / Linux: `source .venv/Scripts/activate`
- **Bộ thư viện cốt lõi:** Đã cài đặt hoàn chỉnh `pandas==3.0.6`, `numpy==2.5.3`, `scipy==1.18.1`, `scikit-learn==1.9.1`, `matplotlib==3.11.2`, `seaborn==0.13.2`, `gdown==6.4.0`, `jupyter==1.1.1`.


---

Integrity v2: src/analysis_data.py là chính sách domain cleaning chung; src/06_machine_learning/validation.py quản lý split/manifest/fingerprint/calibration/CI. Pro chia theo thời gian sự kiện; rank grouped random vì CSDL cũ không lưu timestamp trận (không dùng crawled_at làm ngày trận). Schema model v2 bắt buộc retrain.
