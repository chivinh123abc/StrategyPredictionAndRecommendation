## Role preferences and lane-review JSON — 2026-11-24

SQL/schema/Prohashunchanged. Viewrole_preferences={champion:[{role,games}]}descendingobservedProcountinscope. Actionrole:nullonmanualpick→infernextobservedfreerole;persistactualassignedroleinMove. Swapsexistingrecordafter_turn,historyorderunchanged. Rowlane_review={role,opponent,games,winrate,ci95_wilson,status,requires_review,ranking_confidence_bound,ranking_basis,assignment_source,version,reason};blindgamesnull,unobservedknownkèongames0/metricsnull,noimputation. APIconfig/fingerprintnewlane_review_policy/manual_role_policy. Outputsreports/ui_lane_revision,publicnoplayerIDs/APIkeys.

## Pair reservation and first-selection JSON — 2026-11-24

NoSQLschema/sourcechange. Pickrow/advice thêm pair_reservation={version,status,priority_tier,enemy_bans_before_next_own_pick,opponent_bot_revealed,requires_review,reason,pair_evidenceorsupported_partners/count/worst_case_partners_remaining}. n/WR/Wilson/effectiveliftlấytừProscope;khôngfakepairtỉlệ/missing,khôngnạpRankvàoscore. Firstselectiongame.first_sideđãcó,UIexplicitmỗiván;seriesfirst_picks/first_selection_policy/user_rule_sourcemớiđểtáilậplịchthực. APIconfiguration/fingerprintthêmpair_safety,guardtraceđượclưutronghistory/why/exportmetadata. Reports/pair_reservation_revision,bo5/seriesJSON0-10-20-30-40locks;Prohash20e3d973...unchanged,noprivateplayerIDs/key.

## Session snapshot and contextual output v2 — 2026-11-24

SQL/schema/ProDBSHA20e3d973...khôngđổi. Session thêmoptional snapshot_id64hex; API tựđiềnngàyas_ofthiếuvàIDresponse, khôngghiSQL. View thêmconfiguration={pick_scoring,ban_strategy,contextual_version,snapshot_id}; exportlưucấuhình/IDscopeđểđốichiếu. Source/configkhôngkhớp409, sourceDBđổiđòirestart; fingerprintkhônglàbackupDB/code. Banpool_impactthêm before_slots/after_slots, contextual_policy.version=fixed_capacity_v2. Missingmetricvẫnnull; số0làutilitycủaslotkhôngcóbackup, khôngGD/XP/CSsuytạo. Reports80querycomparison vàexport/screenshot/tests ởreports/contextual_ui_revision; khôngplayerID/APIkey.

## UI JSON contracts, không đổi DB — 2026-11-24

Canonical SQLite readonly/schema/hash không đổi20e3d973...; không nhập thêm Rank vào Pro. Request Session={settings,completed<=4,current}; Game={first_side,history<=20,swaps}; swap={side,champion,to,after_turn}; input extra fields bị từ chối, server derive picks/bans/locks. View trả session,states,turn numbered,schedule,recommendations,scope,rosters,thresholds và series_complete. Browser `draft-lab-session-v1`={version:1,session} chỉ lưu inputs, được replay/validate khi load. Export `draft-lab-bo5.json`={version,session,scope,boards,interpretation}; test export thật ở reports/ui_demo/export.json. Không server-side persistence mới. Public advice whitelist không PUUUID/APIkey; floatNaN/Inf thànhnull, không giả số0. API chỉ phục vụ static web/dist, không mở projectroot/DB/.env. Đây là NV-21 output contract, không thêm kiến thức thống kê.

## Scoring selector and demo report fields, no DB change — 2026-11-24

KhôngđổiSQLitetables/schema hoặcmodeldata. Advisorrowsimple cóscore_components tốiđa frequency/content/matchup, nguồnfallback vàmatchup_scope same_role_only; shapehistoricalevidencevẫnCounts/Wilson. SessionJSONthêmpick_scoringvàeffectivepolicyweights, lưu scope/supportedmass/sourcecomparisonđểkhôngmấtmetadata. SeriesJSONgiữmodefive_drafts_no_game_results, khôngwinner/scorematchgiả. Comparatorqueries lưurole-poolSHA256mỗiquey và3formula,cùngDBhash20e3d973...; ProSQLitereadonlygiữnguyên. Outputsreports/pick_scoring_comparison vàsimple_scoring_bo5,khôngnạpRankvàocanonicalDB.

## Report schema v3: quota null, SQL không đổi — 2026-11-24

DB/schema/khóa/cohort/measurements khôngđổi. rank-matchup-tables-v3 giữtarget_games/games_remaining/target_reached nhưngdefaultnull, progressreference_status=not_loaded; summarytargetnull/parityFalse/collection_goal actualcoverage. Oldmanualtarget làcompatibilityrepro, khôngU.GGdata. ProCSVxuấtlạinhưngn/mean/CIkhôngđổi. Rank418completegamesởmốcreload;watchtiếptụctăng. KhôngsửacanonicalDB, khôngfakecount/CI. collector_process.json giờghiworker_pids+stop_commandchoPythonfamily,khôngxemPIDcũ23100làtiếntrìnhhiệnhành.

## Pro/Rank explanation outputs, không đổi schema — 2026-11-24

CanonicalProSQLite vàrank-lake-v1 khôngđổi, mainDBhash20e3d973... giữnguyên. matchup_evidence chỉđọc Proclean vàRankWALtransaction. RankqueryJOINobservations/jobs lấyupdated_at đểchốtavailability=maxqualification,ingestion, đóngconnection sauđọc. Proobservations/aggregateCSV riêng reports/pro_matchups, publickhôngpersonIDs. PrivatefrozenRank records ở data/raw/contextual_evidence_experiments/{timestamp}/freeze.json; publiceval/diagnostic chỉcounts/query/champion/report, khôngPUUID. KhôngnạpxuôiRankvàoPro hoặc sửaSQL. Reportschemaexplainer mới ở trường matchup_source_comparison củaadvisoryrow; score/bảngmodels khôngđổi.

## Bổ sung export pooled — 2026-11-24

Snapshots.record_json có thể thêm source_kind=league_list_membership, source_ref tới raw league_lists. Seeds vẫn trỏ current list; snapshot từng PUUID được suy xuất từ chính membership của người đó, tier/queue/observed_at và raw response được giữ. Metadata bootstrap_rank_lists:platform:tier refresh15min, khác bootstrap seed-only6h cũ. Batchtransaction cho seeds/snapshots, không đổi bảng/cột hoặc làm mất snapshot qualification đã đóng.

Schema rank-lake-v1 không đổi. metadata thêm key scheduler:last_platform cho round-robin server. Observations vẫn giữ patch/platform gốc; ALL_OBSERVED chỉ nằm ở bảng CSV tổng hợp, không sửa raw/DB để mất nguồn. Report schema v2 thêm pooled counts/target progress, pooled_*.csv và matchup_collection_progress.csv. Chi tiết docs/POOLED_MATCHUPS_UGG_STYLE.md, MR-21/NV-17.

## ranked_evidence.db — kho mới thật, không mutate canonical — 2026-11-24

Schema rank-lake-v1 tại data/database/ranked_evidence.db (private/gitignored), khôngđổi lol_live_data.db. metadata(key,value) giữschema_version/cohort_policy/bootstraptime; seeds PK(platform,puuid) lưu tier/source/observed_at/last_polled/page_start; jobs PKmatch_id lưu platform/routing/status/detail_path/timeline_path/detail_fetched_at/classification_json/evidence_json/available_at/updated_at/next_attempt. evidence_json cất10snapshot/time/source vàclassification đểresumeaccepted-chưatimelinequa ngày. snapshots PK(platform,puuid) lưu latestrecord/time; rawarchivegiữpayloadcũ. observations PK(match_id,team_id,role), FKjobs, scope/champion_id/opponent_id/privatePUUID/opponentPUUID/row_json; đủ10rowsmộttransaction. sessions PKsession_id lưu start/end/status/http_attempts/detail_json. Indexjobs_status,seeds_poll,observations_matchup; WAL+OSwriterlock, schema/policyfingerprintguard vàtừchốicanonicaldestination.

Import10accepted cũidempotent; mới78qualified ->tổng88completegames880rows382người. 11.012seed/5pending/7rejected là trạngtháimốcnghiệmthu, khôngphải11kmatch. Rawdata/raw/rank_lake/matches vàsnapshots/{hashedPUUID}/{timestamp}.json, nocredentials/header. Newpublic reports/rank_matchups_live all_matchups/best_full_game_matchups/unfavorable_full_game_matchups/early_gold_advantages/observations.csv +summary/REPORT/checks/tests/sessions; khôngPUUID. Scopeplatform/queue/patch/tierfloor/role/champID/opponentID, n/wins/Wilson/người +6metricn/mean/median/SD/tCI, giữsparse. Sourceactualframe gần10/15 chỉmôtả. Nghiệmthu600+2HTTPrequest,63tests+integrity/FK/rebuild/mirror/privacy/idempotence/canonicalhashPASS. --watchtăngcorpusnhiềuphiênkhôngtrần1.000, khônggộpRankProhoặchistoricalclaim; hai phiênhiệnđãkếtthúc.

## Campaign và coverage sidecars — 2026-11-24

KhôngschemaSQLite mới. Mỗi newrun thêmprivate seed_selection.json(seedindex/PUUID/tierselection) đểtruyvết seedregistry, raw/snapshot khácgiữmục20. Publiccampaignmanifest ở reports/rank_snapshot_collection/campaigns/{id}.json chứaactualbudget/attempts/seedcount/runs, khôngPUUID.

reports/rank_coverage: games.csv khóa match_id, chọnlầnaccepted sớmnhất, available_at=maxsnapshot/detailfetch; observations.csv khóa(match_id,team_id,role), có champion_id/opponent_id/tier/scope/time vàmeasurements cóthật, khôngPUUID. patch/role/champion_role/lane_matchup_coverageCSVscope(platform,queue,patch,tierfloor), sốtrận/ngườikhácnhau/deficit; pairlàcóhướng. Rejected chỉ thêmIDs/labels vàouniverse đểtạo0, khôngsamples. summary/readiness/checks JSON/REPORT/tests.logcósourcehash,policykind,splitIDvàmetricsNull. Tổng10trận100rows72người,115champrole/2156pair,0support. Privateevidence chỉtrongmemoryđếmngười, khôngmergeDB hoặcđầuvàomodel. Đồnghồavailabilityphảitrướctargetquery; prototyperanker/baselinereportschưatồntại.

## Tier snapshot sidecar v1 — 2026-11-24

KhôngđổiSQLite/schema/model. data/raw/riot_rank_snapshots/{runid}/private: detail/timeline/provenance, snapshots/{sha256puuid}.json(rawAPI +observed_at/platform), rank_snapshots.json(puuid/platform/queue/kind=snapshot/tier/division/league_points/observed_at/source_ref/status),manifest. Rawchứacá nhân vẫnprivate/gitignored, hashfilenamekhônglàanonymization.

Public reports/rank_snapshot_collection/{runid}/summary/matches/accepted_match_ids/checks.json/REPORT.md/tests.log khôngPUUID/names; participant_idchỉ1..10trongtrận. accepted_observations.csv thêm tier_at_observation/rank_observed_at/cohort/historical_rank_verifiedFalse vàoCOLUMNS hiệncó, signedgold/XP/CS10/15 chỉmôtả. acceptedIDscònphụthuộctimelineđểcóobservations;missingkhôngfill0. latest.jsonpointer. Live5trận49snapshots/2accepted/3quá24h/0missing/20observations; DB/rawkhôngđổiquachecks. Khôngmergecohortmớivàocachehistorical92trận hoặccanonicalDB.

## Rank cohort evidence/audit sidecar — 2026-11-24

Không migrationSQLite/raw. Config src/config/draft_modes.json; private evidence JSON list puuid/platform/queue/tier/kind/observed_at/source_ref + valid_from/valid_until nếu historical_interval. Snapshot không thành interval, không tự suy historicaltier; interval có source cũng chỉ contract-validated chưa xác thực độc lập. Audit reports/rank_cohort_audit/{summary,matches,checks}.json/REPORT.md/tests.log chỉ xuất match ID/nhãn/counts/reasons và hash, không PUUID/playername.92trận đều seed-only/0all10historical-high, không rank thấp. Evalcohortaudit tại reports/rank_transfer_evaluation/cohort_audit dừng0eligible, metric JSON trước giữ nguyên. Lệnh tái lập cũ cần --allow-seed-only-research; raw cache/mẫu cũ không sửa/xóa. Snapshot collector mới chưa triển khai, không invent bảng hoặc output.

## Rank study schema v2 và contract — 2026-11-24

Không đổi SQLite hoặc snapshot canonical. Raw92trận/catalog/manifest riêng data/raw/riot_matchups_study, gitignored;411participant chỉ báo số đếm, không xuất định danh. Observation CSV mới thêm ended_at (maxstart+duration/gameEndTimestamp) và chuẩn tên official ID/alias; schema rank-matchups-v2-ended-catalog, output reports/rank_pro_study_data. Smoke5trận v1 không ghi đè.

Eval từ raw độc lập vớiCSV đọcpatchdạngfloat, giữ patchstring16.20; lọc đúngKR/patch/trước freeze/đãkếtthúc,83trận. Pro cũng loại trận chưa kết thúc trước freeze. Outputs reports/rank_transfer_evaluation gồm contract/names/splits/querytraces/evaluation/checks, không nạp vào DB hoặc model. Contract audit CS Pro30.000dòng và đủdiff10/15 không mismatch; timestamps Rank cóoffset104–407ms, CS10/15 chỉ mô tả. Xem docs/RANK_TRANSFER_PROTOCOL.md và sổ MR-16/NV-12.

## Sidecar đối đầu Rank, không đổi schema SQLite — 2026-11-24

`ranked_matchups.py` không gọi init_db crawler cũ; dữ liệu mới chưa nạp vào matches_10min hoặc snapshot canonical. Raw/provenance/manifest ở `data/raw/riot_matchups/` chứa định danh Riot, gitignored. CSV phân tích `reports/rank_pro_matchups/rank_observations.csv` khóa (match_id,team_id,role), mỗi trận10dòng có hướng, không PUUID/playername. Lưu ngày trận/patch/queue/platform/result/signed gold-xp-cs10/15 và frame_ms thật; CS Rank cộng lính+quái. Pro observations chỉ dùng phép đo complete; missing không điền0.

Aggregate khóa platform/queue/patch/role/champion/opponent, ghi n/mean/SD và team-result winrate/Wilson; bảng ghép hai miền cùngpatch không cộng counts. before/nearest và ngưỡng1000ms phải đọc cùngsummary; nearest có thể sau mốc nên không dùng cho dự báo đúng10phút. Kiểm hash DB trước/sau pipeline PASS tại reports/rank_pro_matchups/checks.json. Không thay đổi ba bảng raw/index.

## 24/11 — Chỉ legacy/contextual

Không thay đổi dữ liệu/schema/index hoặc model khi bỏ lookahead. Chỉ gỡ code/CLI search, giữ snapshot sạch chung; kết quả so2chếđộở reports/legacy_contextual_comparison. Report3chếđộ/searchtrướclàartifactlịchsử, khôngdùnglàmtrạngtháihiệnhành.

## 24/11/2026 — BanPlanner không đổi dữ liệu/schema

Ban ngữ cảnh/rollout tái sử dụng DraftMetaSnapshot sạch trong bộ nhớ và model hành động đã lưu; không tạo bảng, không đổi rawSQLite/index, không tải dữ liệu hoặc fitmodelmới. Thêm JSONtrace/Markdowncomparison trong reports/ban_strategy_comparison, không là bảng dữ liệu mới. CutoffWorlds13/11patchdataset16.20 giữ nguyên trong cả3chếđộ.

> **TRẠNG THÁI ƯU TIÊN — Integrity v2, 2026-11-23.** Dự án đang triển khai theo roadmap; API/web chưa triển khai là công việc kế hoạch. Các tuyên bố cũ bên dưới như “100% Zero-Hardcode”, “hoàn thành 85% về chất lượng”, kết quả model cũ và kết luận nhân quả không còn là trạng thái nghiệm thu. Nguồn hiện hành: [INTEGRITY_V2.md](../docs/INTEGRITY_V2.md), [đánh giá ML](../src/06_machine_learning/evaluation_report.md), [benchmark recommender](../reports/recommender_evaluation.json).

Không thay đổi ba bảng raw hoặc khóa/index. Snapshot sạch trong bộ nhớ bổ sung `tournament_matches_10min` cho các truy vấn phút 10, không tạo bảng vật lý mới. CSV canonical giữ signed differences; snapshot/exports dùng cùng policy `domain-v2-signed-no-trimming`. Rank hiện thiếu event time và JSON timeline; `crawled_at` không được dùng thay ngày trận. Missing không đồng nghĩa 0.

---

NỘI DUNG LỊCH SỬ / KẾ HOẠCH TRƯỚC INTEGRITY V2:

# DATABASE SPECIFICATION & SCHEMA DICTIONARY

*Công nghệ:* SQLite 3  
*Đường dẫn tệp:* `data/database/lol_live_data.db`  
*Tiêu chuẩn thiết kế:* Chuẩn hóa dữ liệu 1NF và 3NF.

---

## 1. BẢNG HIỆN HỮU: `matches_10min`
Bảng lưu trữ thông số các trận đấu Solo Rank cao (Thách Đấu / Kim Cương) được cào từ Riot Games API mốc 10 phút.

### Cấu trúc 42 Cột Chi Tiết:

| Nhóm | Tên Cột | Kiểu dữ liệu | Ràng buộc | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- | :--- |
| **Định danh** | `gameId` | TEXT | PRIMARY KEY | Mã định danh trận đấu duy nhất của Riot (vd: `VN2_12345678`) |
| | `gameVersion` | TEXT | NOT NULL | Phiên bản bản vá của game (vd: `14.5.1`) |
| | `gameDuration` | INTEGER | NOT NULL | Tổng thời lượng trận đấu thực tế (tính bằng giây) |
| | `crawled_at` | TEXT | NOT NULL | Dấu thời gian cào dữ liệu (ISO format) |
| | `server` | TEXT | NOT NULL | Mã máy chủ cào (`VN2` hoặc `KR`) |
| **Mục tiêu chính**| `blueWins` | INTEGER | NOT NULL | Kết quả chung cuộc: `1` = Đội Xanh thắng, `0` = Đội Đỏ thắng |
| **Kinh tế Đội Xanh**| `blueTotalGold` | INTEGER | NOT NULL | Tổng lượng vàng Đội Xanh kiếm được tại phút thứ 10 |
| | `blueTotalExperience` | INTEGER | NOT NULL | Tổng kinh nghiệm Đội Xanh tích lũy tại phút 10 |
| | `blueTotalMinionsKilled`| INTEGER | NOT NULL | Tổng số lính thường Đội Xanh tiêu diệt tại phút 10 |
| | `blueTotalJungleMinionsKilled` | INTEGER | NOT NULL | Tổng số quái rừng Đội Xanh tiêu diệt tại phút 10 |
| | `blueKills` | INTEGER | NOT NULL | Tổng số mạng hạ gục của Đội Xanh lúc 10 phút |
| | `blueDeaths` | INTEGER | NOT NULL | Tổng số lần nằm xuống của Đội Xanh lúc 10 phút |
| | `blueDragons` | INTEGER | NOT NULL | Số Rồng Nguyên Tố Đội Xanh ăn được trước phút 10 |
| | `blueHeralds` | INTEGER | NOT NULL | Số Sứ Giả Khe Nứt Đội Xanh ăn được trước phút 10 |
| | `blueVoidgrubs`| INTEGER | NOT NULL | Số Sâu Hư Không Đội Xanh ăn được trước phút 10 |
| | `blueTowersDestroyed` | INTEGER | NOT NULL | Số trụ Đội Xanh phá được trước phút 10 |
| | `blueGoldDiff` | INTEGER | NOT NULL | Chênh lệch vàng (`blueTotalGold - redTotalGold`) |
| | `blueExperienceDiff` | INTEGER | NOT NULL | Chênh lệch kinh nghiệm (`blueTotalExp - redTotalExp`) |
| **Kinh tế Đội Đỏ** | `redTotalGold` | INTEGER | NOT NULL | Tổng lượng vàng Đội Đỏ kiếm được tại phút 10 |
| | `redTotalExperience` | INTEGER | NOT NULL | Tổng kinh nghiệm Đội Đỏ tích lũy tại phút 10 |
| | `redTotalMinionsKilled` | INTEGER | NOT NULL | Tổng số lính thường Đội Đỏ tiêu diệt tại phút 10 |
| | `redTotalJungleMinionsKilled` | INTEGER | NOT NULL | Tổng số quái rừng Đội Đỏ tiêu diệt tại phút 10 |
| | `redKills` | INTEGER | NOT NULL | Tổng số mạng hạ gục của Đội Đỏ lúc 10 phút |
| | `redDeaths` | INTEGER | NOT NULL | Tổng số lần nằm xuống của Đội Đỏ lúc 10 phút |
| | `redDragons` | INTEGER | NOT NULL | Số Rồng Nguyên Tố Đội Đỏ ăn được trước phút 10 |
| | `redHeralds` | INTEGER | NOT NULL | Số Sứ Giả Khe Nứt Đội Đỏ ăn được trước phút 10 |
| | `redVoidgrubs` | INTEGER | NOT NULL | Số Sâu Hư Không Đội Đỏ ăn được trước phút 10 |
| | `redTowersDestroyed` | INTEGER | NOT NULL | Số trụ Đội Đỏ phá được trước phút 10 |
| | `redGoldDiff` | INTEGER | NOT NULL | Chênh lệch vàng (`redTotalGold - blueTotalGold`) |
| | `redExperienceDiff` | INTEGER | NOT NULL | Chênh lệch kinh nghiệm (`redTotalExp - blueTotalExp`) |
| **Cấm / Chọn (1NF)**| `blueTop` | TEXT | | Tên tướng Đội Xanh đi đường Trên |
| | `blueJungle` | TEXT | | Tên tướng Đội Xanh đi Rừng |
| | `blueMid` | TEXT | | Tên tướng Đội Xanh đi đường Giữa |
| | `blueAdc` | TEXT | | Tên tướng Đội Xanh Xạ Thủ |
| | `blueSupport` | TEXT | | Tên tướng Đội Xanh Hỗ Trợ |
| | `redTop` | TEXT | | Tên tướng Đội Đỏ đi đường Trên |
| | `redJungle` | TEXT | | Tên tướng Đội Đỏ đi Rừng |
| | `redMid` | TEXT | | Tên tướng Đội Đỏ đi đường Giữa |
| | `redAdc` | TEXT | | Tên tướng Đội Đỏ Xạ Thủ |
| | `redSupport` | TEXT | | Tên tướng Đội Đỏ Hỗ Trợ |
| | `blueBans` | TEXT | | Chuỗi danh sách các tướng Đội Xanh cấm |
| | `redBans` | TEXT | | Chuỗi danh sách các tướng Đội Đỏ cấm |

---

---

## 2. BẢNG HIỆN HỮU: `tournament_matches`
Bảng lưu trữ thông số cấp độ trận đấu và đội tuyển (Team Level) từ dữ liệu giải đấu chuyên nghiệp (Oracle's Elixir), gồm 6 giải đấu hàng đầu (`LCK, LCP, LPL, MSI, WLDS, EWC`).
- **Quy mô thực tế:** 6,000 dòng (3,000 trận đấu độc lập $\times$ 2 phe Xanh / Đỏ).
- **Khóa chính (Primary Key):** `(gameid, side)`
- **Số lượng cột:** 155 cột (đã loại bỏ các cột rỗng cấp cá nhân và chuẩn hóa snake_case).
- **Các nhóm chỉ số chính:**
  - *Định danh & Bối cảnh:* `gameid`, `league`, `year`, `split`, `playoffs`, `date`, `game`, `patch`, `participantid` (100=Blue, 200=Red), `side`, `teamname`, `teamid`.
  - *Cấm / Chọn (Draft Phase):* `firstPick`, `ban1`..`ban5`, `pick1`..`pick5`.
  - *Kết quả & Giao tranh:* `gamelength`, `result` (1=Win, 0=Loss), `kills`, `deaths`, `assists`, `teamkills`, `teamdeaths`, `doublekills`..`pentakills`, `firstblood`, `team_kpm`, `ckpm`.
  - *Mục tiêu lớn:* `firstdragon`, `dragons`, `opp_dragons`, `elementaldrakes`, `elders`, `firstherald`, `heralds`, `void_grubs`, `opp_void_grubs`, `firstbaron`, `barons`, `atakhans`, `firsttower`, `towers`, `turretplates`, `inhibitors`.
  - *Sát thương & Tầm nhìn:* `damagetochampions`, `dpm`, `damagetakenperminute`, `damagemitigatedperminute`, `damagetotowers`, `wardsplaced`, `wpm`, `wardskilled`, `wcpm`, `controlwardsbought`, `visionscore`, `vspm`.
  - *Kinh tế & Lính:* `totalgold`, `earnedgold`, `earned_gpm`, `goldspent`, `minionkills`, `monsterkills`, `cspm`.
  - *Chỉ số Timeline mốc 10 phút:* `goldat10`, `xpat10`, `csat10`, `opp_goldat10`, `opp_xpat10`, `opp_csat10`, `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`, `assistsat10`, `deathsat10`, `opp_killsat10`, `opp_assistsat10`, `opp_deathsat10`.
  - *Chỉ số Timeline mốc 15, 20, 25 phút:* `goldat15`..`goldat25`, `golddiffat15`..`golddiffat25`,...

---

## 3. BẢNG HIỆN HỮU: `tournament_players`
Bảng lưu trữ thông số chi tiết của từng tuyển thủ chuyên nghiệp thi đấu ở 5 vị trí (`top`, `jng`, `mid`, `bot`, `sup`).
- **Quy mô thực tế:** 30,000 dòng (3,000 trận đấu độc lập $\times$ 10 tuyển thủ).
- **Khóa chính (Primary Key):** `(gameid, participantid)` (với `participantid` từ 1..10).
- **Khóa ngoại (Foreign Key):** `FOREIGN KEY (gameid, side) REFERENCES tournament_matches(gameid, side) ON DELETE CASCADE`.
- **Số lượng cột:** 129 cột.
- **Các nhóm chỉ số chính:**
  - *Định danh tuyển thủ:* `gameid`, `participantid`, `side`, `position`, `playername`, `playerid`, `teamname`, `teamid`, `champion`.
  - *Hiệu suất cá nhân:* `kills`, `deaths`, `assists`, `firstbloodkill`, `firstbloodassist`, `damagetochampions`, `dpm`, `damageshare`, `earnedgoldshare`, `total_cs`, `cspm`.
  - *Chỉ số đối đầu cá nhân mốc 10 phút:* `goldat10`, `xpat10`, `csat10`, `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`, `deathsat10`, `assistsat10`.

---

## 4. QUY TẮC CHUẨN HÓA ĐÃ ĐƯỢC CHỨNG MINH
1. **Chuẩn 1NF (Tính nguyên tử):**
   - Không dùng mảng ghép hay chuỗi ghép tướng cho đội hình. Toàn bộ 10 vị trí thi đấu trong Rank được tách thành 10 cột nguyên tử độc lập (`blueTop`..`blueSupport`, `redTop`..`redSupport`).
   - Trong dữ liệu giải đấu, mỗi tuyển thủ là 1 dòng độc lập trong `tournament_players`, liên kết với cấp trận qua `gameid`.
2. **Chuẩn 3NF (Khử phụ thuộc hàm bắc cầu):**
   - Loại bỏ cột `country` trong `matches_10min` vì $server \rightarrow country$ là phụ thuộc hàm hiển nhiên.
   - Phân tách rạch ròi cấp độ đội tuyển (`tournament_matches`) và cấp độ cá nhân (`tournament_players`), loại bỏ các cột thừa ở từng cấp.

---

## 5. BỘ TRUY VẤN SQL PHÂN TÍCH NÂNG CAO (CHƯƠNG 5 & 5x)
Tệp triển khai: [`src/03_database_sql/queries.sql`](../src/03_database_sql/queries.sql) & [`src/03_database_sql/execute_queries.py`](../src/03_database_sql/execute_queries.py).

| Mã Query | Kỹ thuật SQL | Bảng sử dụng | Đầu ra phân tích | File xuất CSV |
| :---: | :--- | :--- | :--- | :--- |
| **Q1** | `Self-JOIN`, `GROUP BY`, `HAVING` | `tournament_players` | Thống kê kèo đối đầu 1v1 theo từng đường (Top/Mid/Bot), winrate Đội Xanh, chênh lệch vàng & CS lúc 10 phút. | `data/processed/sql_query_1_result.csv` |
| **Q2** | `Intra-team JOIN`, `HAVING COUNT(*) >= 10` | `tournament_players` | Thống kê 125 cặp đôi Xạ thủ + Hỗ trợ (Bot + Sup) ăn ý nhất giải đấu, winrate, vàng chung phút 10. | `data/processed/sql_query_2_result.csv` |
| **Q3** | `CTE / Subquery`, `Unpivot UNION ALL`, `FULL JOIN` | `tournament_players`, `tournament_matches` | Top 20 tướng có Tỷ lệ Cấm/Chọn (Presence Rate) cao nhất giải đấu. | `data/processed/sql_query_3_result.csv` |
| **Q4** | `Window Functions: DENSE_RANK()`, `AVG() OVER()` | `tournament_players` | Xếp hạng top 3 tuyển thủ đè đường phút 10 theo từng vị trí (Top/Jng/Mid/Bot/Sup) và so với Benchmark toàn giải. | `data/processed/sql_query_4_result.csv` |
| **Q5** | `UNION ALL`, `CASE WHEN`, `GROUP BY` | `tournament_matches`, `matches_10min` | Đối chiếu hiệu quả lăn cầu tuyết (Snowball Lead) giữa Đấu Giải vs Solo Rank theo 5 phân tầng chênh lệch vàng phút 10. | `data/processed/sql_query_5_result.csv` |

---

## 6. HỆ THỐNG INDEXES TỐI ƯU TRUY VẤN (14 INDEXES)
- `idx_tm_league_year`: `tournament_matches(league, year)`
- `idx_tm_team`: `tournament_matches(teamname)`
- `idx_tm_date`: `tournament_matches(date)`
- `idx_tm_patch`: `tournament_matches(patch)`
- `idx_tm_playoffs`: `tournament_matches(playoffs)`
- `idx_tp_player`: `tournament_players(playername)`
- `idx_tp_champ`: `tournament_players(champion)`
- `idx_tp_pos`: `tournament_players(position)`
- `idx_tp_team`: `tournament_players(teamname)`
- `idx_tp_league`: `tournament_players(league)`
- `idx_tp_patch`: `tournament_players(patch)`
- `idx_tp_champ_pos`: `tournament_players(champion, position)`
- `idx_tp_game_pos_side`: `tournament_players(gameid, position, side)` *(Tối ưu hóa Q1 Self-JOIN)*
- `idx_tp_game_side_pos`: `tournament_players(gameid, side, position)` *(Tối ưu hóa Q2 Duo JOIN)*


