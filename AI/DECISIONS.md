## ADR-043 — Compact UI, observed free-role placement and exposed-lane review (2026-11-24)

Acceptedtheouser3yêucầuvàRenektonfollowup. UIsetupabove/choicesparallel/inspectorbelow,nativeDragDropcùngđội/menuaccessible,noframeworknew. Manualfree_role=countsinProscope/descending/skipoccupied/knownobservedonly,serverrecomputes. ContextualguardMR12reviewdirectassignedopponentalreadyrevealedn<5withoutwaiting5enemies. Same-role/allopenexposedrankbyexistingWilsonlowerboundbeforeunchangedscore,pairguard/wishlist/supportedtierprecedencepreserved;GDnotadded. Đây làpolicytựthiếtkếkhôngclaimcoursealgorithm/optimalcounter. Renekton2/2nlow,CIoverlap;Gnar6nfirst/Renektonsecond/Galio0lastsameprefix. CLIfirstselectionexplicitmulti-games,nolegacyalternatingfallback.178tests/5Edge/build/allBlueBO5PASS,sourceunchanged,knowledge30/NV24,outputsreports/ui_lane_revision;independentqualitynotproven.

## ADR-042 — Bot partner preservation and per-game First Selection (2026-11-24)

AcceptedtheouserbáoweaklinkBluepick vàluậtphiênRed/Bluefirstindependent. Reusecounts/lift/threshold/schedule,addpair_reservationconstraintMR24khôngcâysearch/newmodel. Fulllegalbot/supscan,n>=5/lift>=1,positivepartnercount<=enemybanbudgetbeforeownnextpick→securecompletiontier;scorecurrentunchanged,wishlist/adequateevidence/rolefilter/manualpreserved. Sparsepairsreview,testoverrideexplicit. Guardchỉkhiđịchđãlộbot/sup;khôngkhẳngđịnhmechanicalsynergy/optimalpair/winuplift. Banv2khôngđổi.

UIchọnfirstSideeachgame,noforcedalternation;CLIexplicitlistnphầntử,omitgiữlegacydemorepro.Labelnguồnrulengườidùngđộc lậplinkFearless,khôngclaimofficialleagueadoption. APIconfiguration/fingerprintthêmpair_safety;report/explainkhônggiấupolicytier.170tests/3Edge/build/mirrorcase/5draftlegalityPASS;sổ29 vàdocsGIU_CAP_BOT_VA_FIRST_SELECTION,outputsreports/pair_reservation_revision;khôngtrain/DBchange/commit/push.

## ADR-041 — Two simultaneous choice panels; fixed-capacity contextual utility (2026-11-24)

Accepted theo user. ChỉsửaMR-13poolutility v2 cốđịnhmẫu3 đểmấtbackupkhônglàmtăngpool, giữnguyênowncost/accessweights/currentpick. Khôngthêmchiếnlượcthứba/họcmodel/épbanđadạng. Baseline80statescùngpoolcho31monotonicityprobes→0,Recall5khôngtăng; promote làsửaquyướcutilitybất nhất, khôngclaimstrategyaccuracy. HaiUIpanel/nútriêng vàpindate/fingerprint làNV-22, hỗtrợsochínhxác snapshot/config. CacheDBchanged409đòirestart; snapshotconflict vẫnexport/newsession. KhôngsnapshotDBhistorical/codearchive.159tests/build/2EdgePASS; sổ28 vàreports/contextual_ui_revision. KhôngđổiProML/Rankcollector.

## ADR-040 — Small local React/TypeScript UI over existing Python engine (2026-11-24)

**Accepted theo user** hỏi TS và chốt triển khai. Chọn React+TypeScript/Vite và FastAPI adapter, CSS thuần; reuse engine thay vì port công thức sang JS. Một server local phục vụ API+bundle; browser giữ inputs, API validate/replay và derive Fearless. Không thêm models, new scoring, lookahead, cloud hoặc full production platform. UI đầu là Pro; Rank bảng evidence riêng, không giả recommender Rank đã xong. Giữ current vì simple giảm retrieval. NV-21 kỹ thuật ngoài môn được ghi ở sổ27 và hướng dẫn; constitution1.3.0 chuyển trạng thái API/Web planned→implemented local demo.154unit tests và Edge workflowPASS, không phải chứng minh chiến thuật tốt hơn. Cache snapshot cần restart khi nguồn đổi; không globalBO5 optimization.

## ADR-039 — Simple pick as a measured option, preserve default (2026-11-24)

Useryêucầutrial3tínhiệudễgiảithích thay8thànhphần, chỉthaybảnchínhsaukhiđánhgiá. Simplecốđịnhfrequency/cosine/same-roleWR/explicitfallback,meanavailable,equalweights; khôngtunedgridtừtest. Giữpool/cutoff/rules/flexđểfaircompare, khôngthêmbanstrategy hoặcglobalBO5planner.

520querysamepool choSimpleR5test.425vsCurrent.49375,CIΔ[-.11034,-.03235],nêngiữcurrentdefault. Datareusedaudits khôngfreshfinaltest vàpickretrievalkhôngtacticaloptimality. KhôngđượctuyênbốmọiMRđềucầnhoặclựachọnSimpletốtngangbaseline. Ablationlàdiagnostic, khôngdùngđểra8varianttìmthắngtest. BO5minhhoạsimplevẫnđủ5draftvớitesttop1overridecónhãnmissing,khônggiảwinners. ReproCLI/docs/outputsởMR-23/NV-20.

## ADR-038 — Phạm vi vừa sức, không chạy theo quota U.GG (2026-11-24)

User rút mốc2.000 và muốn Chương1–6 với một số mở rộng vừa sức. Mặc định khôngquota, báo n/nguồn/CI thực vàU.GGreferencechưa có; khôngđánhdấuparityhoặctựhạcohortMaster+. Chỉhọc cáchhiểnthịkhôngđồngnghĩalấyđượcdataset/thuậttoánU.GG. GiữCLIlegacyoptionđểrepro, khôngthêmadapterkhinguồnchưađọcđược.

Giữ corevàdemo hiệncó, prototype/transfer/search/globaloptimizer làphụ; khôngmọiranhgiớiđềxuấtđềuphảitrởthànhsảnphẩm. KhôngbắtbuộcFastAPI/Reactfullstack. Ràsoát vàrulesđãghi docs/PHAM_VI_DO_AN_VUA_SUC,AIrules,constitution1.2.0,sổ25/NV-19. Việcđơngiảnhóacôngthứcruntimechưalàm, cầnbaseline, khôngđổitronglúcsửametadataquota; khôngxoáhistory.

## ADR-037 — Tách bằng chứng khỏi điểm, thử Rank có freeze và cổng thời gian (2026-11-24)

Theo yêu cầu3phần: xuất Pro earlyresources thật và hiển thị hai nguồn riêng ngay, không đợi chứngminhquality mới cho xem thốngkê. Bảng giải thích không đổi mainranking. Rankgộp patch/server theo yêu cầu nhưng availabilityphải trướcas_of, canonicalnames/IDs, đủcohortnguồn và snapshotproxylabel. Prototypechỉđổi matchupsource same-role, fixedhybrid50/50 đểisolatedcomparison, khôngđổi banpolicy hoặc đưa tài nguyênquerytươnglai vào features.

Rank24/11 thu sauPro14/11: benchmarkcũ chỉdiagnostic cófuture/reusedflags, khôngđượcpromote. Freezeđộc lập,5+5seriesmới saufreeze vàkhôngoverlap cho prospective; chưacódata thìnullmetrics/readyFalse, khônggán“independenttest” cho dữliệu đãtừngaudit. Retrievalgatekhôngtựbậtruntime hoặc chứngminhcounter/tăngthắng. Xem docs/PRO_RANK_MATCHUP_EVIDENCE.md và MR-22/NV-18; khôngretrain/schemaDBchange.

## ADR-036 — Gộp patch có truy vết, mục tiêu mỗi kèo (2026-11-24)

Thêm bảng gộp các patch/server đã thu theo yêu cầu. Giữ bảng scope riêng, nguồn và flag meanGD15 trái dấu; không nhận counter bất biến hoặc sao chép thuật toán U.GG. Mục tiêu2.000/kèo là tiến độ, không ngừng thu hoặc chứng nhận chất lượng. Vẫn10Master+ snapshot, không tự hạ xuống Emerald+. Round-robin server có cursor trong metadata để tăng phạm vi; không đổi schemaDB hay Proscore. Xem docs/POOLED_MATCHUPS_UGG_STYLE.md và MR-21/NV-17.

## ADR-035 — Kho tăngdần khôngtrầntổng và descriptive matchup tables (2026-11-24)

User muốn thu nhiều nhất/cậpnhật dữliệu nhưpublicU.GG, khôngmốc1.000rồimớilàm. TạoSQLiteevidence mới, khôngschema-mutatecanonicalPro; seedC/GM/M vàBFS,pagingIDsrecent24h, dedupPK/cursor/TTLgiữtimestamp/qualiresume/filelock. Tăngcorpus qua phiêncóbudget/rate/deadline; --watchchạynhiềuphiênnhưngkhôngnéquota hoặcserviceẩn. Giữ10Master+/24h/15min, khôngnhậnhistoricaltier/mẫutrùng. Thốngkêngaymọin vàgiữsparse, xếpriêngwholegameWRvàGD15n5vớiCIs; khôngcopyU.GGalgorithmhoặcbịa countercausal. NISTtCI làMR vớiindependence/outlier/smalln/multiplecomparisonlimits. 600+2requests88completegames/63testsPASS; khôngRankranker/Prosignal/UI/MLfit. RawDBprivate/reportkhôngPUUID; source/outputs MR-20/NV-16 lưu sổ vàdoc.

## ADR-034 — Thu hữu hạn, báođộphủ và không lách snapshotavailability (2026-11-24)

User giao thuđađợt/coverage, xâyRankkhiđủmẫu vàevaluate trướcUI. Chọn3đợt5seed/200HTTPattemptgồmretry, khôngcron/unboundedcollection, giữMaster+/24h/15min. Đếm lại10accepted/72người sau8mới; khôngđếmtrậtlặp/ngườilặp nhưđộclập, rejectedchỉbổsunguniverse tên đểbáo0. Readiness5games/3players/2championsperrole và5/2/2partition làengineeringpolicy chưa poweranalysis; dữliệuthiếuphảighi thiếu, khônggiảrecommendermetrics. Temporalhistorycầnrankcohort/detailđãbiết trướcvalidationstart, khôngchỉgamestartcũ; hiện0historyqualify. Vìvậy đúngđiềukiệnuser, recommender/eval/UIchưađược triểnkhai, protocol vàbaselines chỉplanned. GiữPro/historicalgate, khôngnớiđểépmetric. XemMR-19/NV-15.

## ADR-033 — Chụp rank đủ10người, công khai snapshot proxy (2026-11-24)

User giao collector cá nhân vàreport nhận/loại/thiếu. Dùng currentSolo/DuotierquacAPI cho10PUUID thật; snapshotnốitiếp cóobserved_at, không inferMMR hoặchistoricaltier. Master+theoconfig, engineeringdefaults24hafterend/15minspread, khôngnớiđểépkếtquả. Cachechỉtrongrun, raw/privateidentitytáchpublicreport; typedAPIerrorđểauth/rate/networkdừng,404thiếu tiếp tục. Snapshotall10highnhưngtrậnquácũ vẫnbáoallhighatobservationnhưngloạikhỏinhómnearproxy; real5trậncó2nhận/3quácũ,0thiếu. Historicalgatevẫnkhôngnhậnsnapshot, khôngtíchhợpProsignal/Rankruntime. Cầnbenchmarkriêng/nguồnđộclậpsau; khôngnhậncollector làrankrecommenderđãxong. MR-18/NV-14 truyvếttrongsổ.

## ADR-032 — Rank/Giải riêng và không gọi seed-only là high elo toàn trận (2026-11-24)

User xác định2chế độ Rank và Giải; đồng ý chốt thiết kế và tiêu chuẩn dữ liệu Rank cao cho Giải. Config Master+ là working default chỉnh được, không ngưỡng tối ưu. Định nghĩa cả trận high historical yêu cầu10người đủ rank evidence đúngthờigian/queue/server; unknown không là below. Seed/chỉsnapshotcurrent không hồi tố, interval cần nguồn thật và available trước cutoff, toolkhôngxácthựcđộc lập source. Chặn evaluator default khi không đạt, explicitflag chỉ tái lập seed-only cũ. Không cố gọi currentrankAPI rồi nhận làhistorical;92trận hiệnchưađủchứngcứ, không có kếtluậnrankthấp. Runtime Rank cònplanned; Giải giữPro/legacy/contextual, không bật hybrid. Thiết kếluậtdraftRankriêng, không đồng nhấtmodevớistrategy.

## ADR-031 — Thử nguồn matchup, không bật hybrid khi chưa có bằng chứng (2026-11-24)

User giao cả4bước chuẩn hóa/thu thêm/evaluate/conditional integration. Dùng official pinned catalog, lấy mẫu lịch sử trước holdout thay vì rank hiện tại16.23; giữ patch/server và ended_at cutoff. Phép thử chỉ thay matchup, cùng pool/công thức/prior/threshold, hybrid residual50/50 ở Rank n5 và Pro fallback khi thiếu. Không pooling domains hoặc giảm điểm Pro do missing Rank. Split chronological series60/20/20 và freeze trước val; không tune test. Pro dataset cũ đã dùng nên chỉ thăm dò, không gọi final test mới. Kết quả test không tăng R5, coverageRank13/320query; CI[0,0] không chứng minh equivalence. Do đó không tích hợp runtime, không hạ ngưỡng/tune để ép kết quả. Cần tập giải mới độc lập và coverage/benefit rõ trước khi cân nhắc. Kiến thức MR-16/NV-12, protocol/report lưu để viết báo cáo.

## ADR-030 — Rank là miền tham khảo riêng (2026-11-24)

User đồng ý bước thu thập/đối chiếu sau khi nêu khác biệt rank và giải. Pipeline sidecar không pooling counts/winrate hoặc cộng điểm contextual. Reject role thiếu/trùng, dùng timestamp thật và signed differences. before không sau mốc trong1000ms; nearest±1000ms chỉ mô tả vì frame Riot hơi sau mốc, không nối vào Snowball. Ngưỡng là policy kỹ thuật tự thiết kế, chưa tối ưu. Seed hiện tại không xác nhận rank lịch sử của10người.5trận KR16.23 chưa có patch chung Worlds nên chưa kết luận chuyển miền. Benchmark Pro-only/Rank-only/hybrid còn dự kiến, chưa có output; phải đánh giá độc lập trước khi cân nhắc trọng số. Xem sổ MR-15/NV-11 và docs/RIOT_RANK_MATCHUPS.md.

## ADR-029 — Audit pick trước khi sửa chiến lược (2026-11-24)

Userđồngýbắtđầubước1. Dựnglạiđúngstate/pool/cutoffcủa50pickcontextual,scoretáilậpkhớp,loạipickcũkhỏitop5alternativevàkiểm248alternativehợplệ. Bỏtừngthànhphầnđiểmchỉđểchẩnđoánđộnhạy,khôngthaypolicy/PICKhoặctuneweight. Khôngdùngtop1cũlàgroundtruthquality,khôngsuyđồngchọnthànhsynergy/counter. Reviewkhôngdùngrole/futurepickđịchchưalộvàsẽrejectswaphistorychưađượcreplaythayvìngầmsai. Sourcehash/state/savedscorechecks làminhchứng,khôngcầnretrainchoaudit. Báocáo hiệnchỉra thiếuđốidầu/phốihợpítmẫu/backoffcuốiFearless;chưatựsửaflexhoặcmởsearch.

## ADR-028 — Loại lookahead, chỉ duy trì legacy và contextual (2026-11-24)

User yêu cầu bỏlookahead vàchỉquantâmlegacy/contextual. Gỡ mã tìmnhánh/opponent response tíchhợpban, flags vàcomparator3mode; khônggiữruntimelookahead dormant. BanPlanner giữcontextualone-step vàContextualBanPolicy; traceđổi contextual_trace. Legacydefaultkhôngđổi, contextualchủđộngbật. Kếtquảcũlookahead chỉlàlịchsửcóngày/nhãn; khôngxóaDB/model/artifactđãtạo. Opponentpredictorprototypeđộc lập giữnguyênnhưngngoàifocus, khôngđượccontextualgọi. So2series mới đúng5draft vàsamepick/banvớimốctrước,57testsPASS; oldlookahead CLIreject. Mappingchínhtrongsổmục15/NV-09 vàdocs/BAN_LEGACY_VA_CONTEXTUAL.md.

## ADR-027 — Ban ngữ cảnh và bounded response rollouts, không ép ban khác nhau (2026-11-24)

User đãgiao3mục mới sau trạngtháidừngtrước. Giữlegacy làmđốichứng/mặcđịnh, thêmcontextual/lookaheadopt-in. Contextual đánhloss top3poolroleđịch trừlosscủamình×accessfactor1nếulấypicktrước,.5nếusau,chia5; roster/Fearlessđềuảnhhưởng. Lookahead root6/response2, chỉrẽfirstopponentturn, còn lại contextual/pickgreedytheolịchthật đến3pick/max12plies. Leafsumnewsecured+remainingrolepriority mìnhtrừđịch /5; score expectedproxy+.25contextual. Khôngfullminimax/expectimax, khôngwinprobability/fullBO5. Predictor lưu sẵn cócutoff/regionguard, fallbacksoftmaxcónhãn; khôngtrainlại. Traceminimalpublicstate khôngcapturemutablehistory/circularrefs; lưutấtcảroot/branches/selected-omittedmass/sensitivitybounds. Preservetestoverride,theo100lượtBan/Pickcósố. 57testsPASS,3seriesđủ5draft và583branchreplay. Diversitytăngkhôngchứngminhchấtlượng;48/50boundschồnglấn,41/50pickthiếubằngchứng. Artifact/docmapping trong sổ mục14 vàBAN_NGU_CANH_VA_LOOKAHEAD.md.

## ADR-026 — Không tự chốt counter thiếu căn cứ; hoàn tất Trundle rồi dừng (2026-11-24)

Xét toàn đội địch từ cross-role observations, không suy nhãncounter từ meta/cosine/co-pick hoặc một skill. Khi địch đã lộ5và coverage đối đầu đủ mẫu bằng0, auto dừng trướcapply, lưu manual_review/alternatives; explicit statistical-demo override riêng, user manual vẫn được phép. Evidence>0 cũng chưa làmechanicalproof; không blacklistTrundle hay tự gọi tướng khác tốt hơn. Source/evidence/giới hạn lưu trong sổ mục11 và reportcase. Người dùng đã thu hẹp task: hoàn tất xử lýTrundle/case tương tự rồi dừng; các model/state/forecast đã làm trước đó giữ lại có status thật, không tiếp tục search/planner hoặc training. 51testsPASS.

## ADR-025 — Sổ kiến thức là điều kiện hoàn thành; project overrides giữ quy định trong SpecKit (2026-11-23)

Theo yêu cầu người dùng, mọi bổ sung/sửa kiến thức/phương pháp/chức năng/output phải cập nhật sổ tổng hợp trong cùng đợt làm việc. Quy định chuẩn ở AI/KNOWLEDGE_RULES.md, dẫn từAGENTS/GEMINI/AI_RULES vàconstitutionVI(version1.1.0). Dùng .specify/templates/overrides cho4template, không sửa manifest/hashes hoặc core installer commandprompts. Spec/plan mapping, tasks códoc+verify, checklist xemrequirementsquality, analyze chỉbáogap không sửa. Kiểm chứng phù hợp tác động; docs-only không đòi retrain. No-impact có lý do; planned!=executed. Đây là nghĩa vụ workflow, chưa làCI tự động. Kiểm tra resolver/lần nâng cấp để tránh mấtcustomization. MụcNV-06 trong sổ ghi nơi áp dụng và output.

## ADR-024 — Giữ hướng mở rộng BO5, tách minh chứng môn học và mục tiêu chưa hiện thực (2026-11-23)

Theo yêu cầu người dùng, tiếp tục hướng tính trước phản ứng đối thủ và để dành tướng/tối ưu BO5, không thu hẹp chỉ còn gợi ý thủ công. Tài liệu thống nhất: docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md. Mọi nội dung phải có phân loại MH/UD/MR/NV, source/function, chức năng và artifact; planned modules/output ghi rõ chưa tồn tại. Hiện tại greedy Fearless driver không được mô tả thành full-series planner. Opponent model khác model dự đoán kết quả đội hình. Planner phải có evaluator, giả định đối thủ, trace/budget và đánh giá theo thời gian/series; không hứa tối ưu toàn cục hoặc tăng thắng. Lượt này chỉ tạo/sync tài liệu, chưa chọn hoặc hiện thực thuật toán planner cuối cùng.

## ADR-023 — Driver series Fearless, tách pool ứng viên và ngưỡng bằng chứng (2026-11-23)

Carry union PICK của cả hai đội, không carry bans, không reset ván5. Lịch first-pick demo chỉ định độc lập màu; không gán kết quả game để giả lập quyền chọn hoặc BO5score. Series mặc định xét role đã quan sát>=1 nhưng lớp>=5 ưu tiên trước; counts/CI/label vẫn giữ và evidence threshold5. Giữ ngưỡng mặc định5cho one-game. Shrink positive association theo n_pair, negative theo n_anchor; không thưởng quá mức mẫu đơn lẻ. Kiểm chứng5ván100lượt50picks và38tests. Đây là greedy per-turn, chưa là full-series planner, không bảo đảm tối ưu/thắng trận. Báo cáo reports/worlds_fearless_bo5/REPORT.md.

## ADR-022 — Association mọi cặp role điều chỉnh điểm draft (2026-11-23)

Không vá riêng cặp tướng. Bổ sung co-pick theo đúng team và cả hai role cho mọi cặp; shrink conditional frequency về marginal để tướng phổ biến không mặc nhiên là partner tốt. Dùng geometric lift qua các đồng đội đủ lịch sử làm hệ số odds điểm nền, exponent1 công khai; không tune sau kết quả audit hoặc gọi là xác suất thắng. Pair winrate giữ riêng và không suy nhân quả; n=0, n<5 và thiếu anchor history có trạng thái riêng. Ma trận10cặp/đội phải xuất JSON. Mở CLI evaluate_draft_policy --region WLDS, audit có cutoff và baseline; dữ liệu 20trận phát triển đã xem không thành final test. Chưa có mô hình cơ chế tướng/tương tác3/5tướng hoặc full-series search. Không fit ML, đổi schema hoặc raw DB. Xem docs/WORLDS_ROLE_PAIR_REVIEW.md.

## ADR-021 — Meta theo snapshot và thứ tự draft (2026-11-23)

Thay policy ADR-020: dùng DraftMetaSnapshot chung cho historical/content và tất cả điểm, cutoff/patch/khu vực/window có provenance. Bỏ percentile phụ thuộc pool; meta và slot prior trọng số1, historical0.25, matchup0.5, synergy0.25, mastery0.5, cosine0.1. Đây là policy thủ công công khai, chưa fit/tune; không có case theo tên tướng hoặc tỷ lệ tăng thắng. Presence/slot/pick share decay21ngày; counts/Wilson/content trong cửa sổ60ngày không decay. Ban 0.6presence+0.25enemyPriority+0.15gap; flex enemy dựa phân phối gán role một-một. As-of không dùng dự báo model lưu sẵn. Không tự tạo meta trên patch thiếu dữ liệu. Replay20trận/200lượt chưa cho bằng chứng chắc vượt baseline. Fearless có nhập excluded pool, chưa có full-series planner. Không retrain/schema change. Xem docs/LCK_DRAFT_REVIEW.md và docs/GIA_LAP_BAN_PICK.md.

## ADR-020 — Giả lập hybrid có objective công khai (2026-11-23)

Dùng DraftAdvisor riêng; không thay thế historical/content benchmarks. Pick là weighted rank aggregation (meta/historical/mastery/content mỗi thành phần trọng số 1, matchup 2, synergy 1; chỉ kích hoạt khi có ngữ cảnh). Counts/Wilson CI, đối đầu cả trận và cosine được hiển thị riêng. Ban là heuristic chênh top1/top2 của đối thủ, không đổi điểm thành xác suất. State machine giữ đúng 20 lượt, không trùng tướng/vị trí; lượt A/B độc lập màu phe qua first-pick. Không ngầm chọn thay người chơi khi EOF; có complete=false nếu hủy. Wishlist là user intent tách khỏi điểm. Không huấn luyện thêm model hoặc tuyên bố hiệu năng chiến thuật đã được chứng minh. Xem docs/GIA_LAP_BAN_PICK.md.

## ADR-019 — Content-based filtering bám Chương 6 (2026-11-23)

Thêm phương pháp riêng dùng item profiles, user profiles và cosine (slide 11–20), Precision@10 (slide 47). Thuộc tính là mean DPM/CSPM/WPM/damage-taken-per-minute/earned-gold-share lịch sử tướng tại role. Pick count chỉ là implicit preference. Không huấn luyện model: tính tổng hợp và cosine trên CPU, không có bước fit ML mới. Giới hạn thời gian/role/khu vực và cold-start phải rõ; benchmark validation không phải test độc lập hoặc đo tăng thắng. Không đổi schema/raw DB, không thay thế historical ranker đang dùng.

> **TRẠNG THÁI ƯU TIÊN — Integrity v2, 2026-11-23.** Dự án đang triển khai theo roadmap; API/web chưa triển khai là công việc kế hoạch. Các tuyên bố cũ bên dưới như “100% Zero-Hardcode”, “hoàn thành 85% về chất lượng”, kết quả model cũ và kết luận nhân quả không còn là trạng thái nghiệm thu. Nguồn hiện hành: [INTEGRITY_V2.md](../docs/INTEGRITY_V2.md), [đánh giá ML](../src/06_machine_learning/evaluation_report.md), [benchmark recommender](../reports/recommender_evaluation.json).

ADR-018 — Phân tách kiến thức chuyên gia và bằng chứng dữ liệu. Hủy tuyên bố “zero-hardcode” toàn hệ thống: radar/thẻ chiến thuật còn expert metadata nhưng không tạo probability/uplift. Historical ranker dùng Beta(5,5), reliability n/(n+10), counts/Wilson CI và benchmark retrieval; không diễn giải team winrate thành lane counter nhân quả. Mục tiêu Pro trước phút 10 chưa có timeline thì unavailable. Không cam kết accuracy target. Giữ phân cụm cũ như artifact chuyên gia chưa retrain.

---

NỘI DUNG LỊCH SỬ / KẾ HOẠCH TRƯỚC INTEGRITY V2:

# ARCHITECTURE DECISION RECORDS (ADR)

Tài liệu ghi nhận tất cả các quyết định kiến trúc, công nghệ và dữ liệu mang tính cốt lõi của dự án. Không được đảo ngược các quyết định này nếu không có lý do và bằng chứng cụ thể.

---

### ADR-001: Lựa chọn SQLite3 làm CSDL chính cho đồ án
- **Ngày quyết định:** 2026-09-18
- **Bối cảnh:** Cần một hệ quản trị CSDL quan hệ để lưu trữ dữ liệu cào từ Riot API và dữ liệu giải đấu Oracle's Elixir, phục vụ cho việc chấm điểm môn CSDL & SQL của PTIT.
- **Quyết định:** Sử dụng **SQLite 3** (`lol_live_data.db`).
- **Lý do:** 
  - Không yêu cầu cài đặt máy chủ (MySQL/PostgreSQL) phức tạp trên máy cá nhân của các thành viên.
  - Tệp `.db` duy nhất có thể dễ dàng nén vào file zip nộp trực tiếp cho giảng viên chạy kiểm thử ngay lập tức.
  - Hỗ trợ đầy đủ cú pháp chuẩn SQL: `JOIN`, `GROUP BY`, `HAVING`, `Subquery`, Window Functions.
- **Hệ quả:** Thao tác ghi đồng thời (concurrency) bị giới hạn nhưng hoàn toàn đáp ứng tốt cho quy mô dữ liệu đồ án học phần (~100,000 - 200,000 dòng).

---

### ADR-002: Chuẩn hóa CSDL đạt Chuẩn 1NF và 3NF
- **Ngày quyết định:** 2026-09-19
- **Bối cảnh:** Dữ liệu cào ban đầu có các cột gộp chuỗi (`blueChampions`, `redChampions`) và cột quốc gia (`country`).
- **Quyết định:**
  - **1NF:** Tách hoàn toàn 10 vị trí tướng thành 10 cột nguyên tử: `blueTop`, `blueJungle`, `blueMid`, `blueAdc`, `blueSupport` và `redTop`, `redJungle`, `redMid`, `redAdc`, `redSupport`.
  - **3NF:** Xóa bỏ cột `country` vì $server \rightarrow country$ là phụ thuộc hàm hiển nhiên (`VN2` $\rightarrow$ Vietnam, `KR` $\rightarrow$ Korea).
- **Lý do:** Đáp ứng chuẩn chỉnh tiêu chí chấm điểm khắt khe của môn Cơ sở dữ liệu PTIT; triệt tiêu dư thừa dữ liệu.

---

### ADR-003: Chiến lược Đa Máy Chủ (Multi-Server) Solo Rank
- **Ngày quyết định:** 2026-09-19
- **Bối cảnh:** Riot API không hỗ trợ máy chủ Trung Quốc (Tencent vận hành độc lập).
- **Quyết định:** Cào song song dữ liệu từ máy chủ **Việt Nam (`vn2`)** và **Hàn Quốc (`kr`)**.
- **Lý do:** Máy chủ Hàn Quốc (`kr`) là đấu trường rank cao danh giá bậc nhất thế giới, nơi toàn bộ tuyển thủ LPL (Trung Quốc) và LCK (Hàn Quốc) luyện tập hàng ngày. Dữ liệu giải đấu chuyên nghiệp Trung Quốc (LPL) được bổ sung độc lập từ nguồn Oracle's Elixir.

---

### ADR-004: Cơ chế Xử lý Concept Drift trong LMHT
- **Ngày quyết định:** 2026-09-19
- **Bối cảnh:** Riot Games cập nhật bản vá 2 tuần/lần, làm sức mạnh tướng và meta thay đổi liên tục.
- **Quyết định:** Kết hợp giữa **Sliding Window** (lọc theo `gameVersion`) và **Exponential Time-Decay Sample Weighting** ($w_i = e^{-\lambda \Delta t}$) khi huấn luyện mô hình.
- **Lý do:** Giúp mô hình ưu tiên học meta mới nhất mà không phải xóa bỏ hoàn toàn dữ liệu của các bản vá trước đó.

---

### ADR-005: Tách rời Backend REST API (FastAPI) để phục vụ Giao diện Web App
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Đồ án Khoa học Dữ liệu cần một giao diện Web trực quan để demo mô hình dự đoán và hệ thống gợi ý cấm/chọn.
- **Quyết định:** Xây dựng cổng **FastAPI** trung gian độc lập kết nối với Web App.
- **Lý do:** Mô hình AI chỉ cần huấn luyện và đóng gói một lần duy nhất (`.pkl`). Giao diện Web App đóng vai trò Client gọi API nhận kết quả JSON nhanh chóng, tách biệt rõ ràng giữa tầng xử lý dữ liệu và tầng hiển thị.

---

### ADR-006: Giữ nguyên Python 3.10.11 / 3.13 làm môi trường chuẩn trong `.venv`
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Hệ thống cần môi trường ổn định với pre-built wheel trên Windows cho `scikit-learn`, `xgboost`, `pandas`, `numpy`.
- **Quyết định:** Sử dụng môi trường ảo `.venv` chuẩn hóa cho toàn dự án.
- **Lý do:** Tránh lỗi xung đột thư viện và đảm bảo khả năng tái lập trên máy của mọi thành viên.

---

### ADR-007: Tập trung 100% vào Nền tảng Web App cho Môn Nhập môn Khoa học Dữ liệu
- **Ngày quyết định:** 2026-11-22 (Cập nhật)
- **Bối cảnh:** Dự án tập trung hoàn toàn vào học phần Nhập môn Khoa học Dữ liệu.
- **Quyết định:** Chỉ phát triển giao diện **Web App** (kết hợp Backend FastAPI / Streamlit) làm sản phẩm trình diễn và báo cáo chính thức.

---

### ADR-008: Giữ Kiến trúc Script Cào Độc Lập & Kiểm Soát Git Push Nghiêm Ngặt
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Việc phân tách cấu hình ra nhiều file phụ thuộc ngoài luồng (pyproject.toml, logger, config module) làm phát sinh lỗi phân giải đường dẫn của Language Server (Pyrefly) và gây phức tạp hóa không cần thiết.
- **Quyết định:**
  - Giữ script [crawl_riot_matches.py](../src/01_data_pipeline/crawl_riot_matches.py) độc lập, tự xác định `BASE_DIR = os.path.dirname(...)` và tự nạp cấu hình `.env` nội bộ.
  - Áp dụng quy tắc Git nghiêm ngặt: **Không bao giờ tự ý push lên GitHub** khi chưa có sự xác nhận/lệnh trực tiếp từ User.

---

### ADR-009: Tập trung cấu hình dự án vào package chuẩn `src/config/`
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Việc đặt file `config.py` ở ngay thư mục gốc `Project/` khiến cấu trúc bị phân tán ("đứng giữa đường"), không thuộc package `src/` và làm rối không gian làm việc gốc.
- **Quyết định:** Chuyển toàn bộ cấu hình vào package chuẩn [src/config/](../src/config/) gồm `settings.py` và `__init__.py`. Xóa hoàn toàn `config.py` ở root.
- **Lý do:**
  - Gom toàn bộ code dự án vào bên trong `src/` theo đúng chuẩn thiết kế phần mềm sạch.
  - Cung cấp cơ chế import kép an toàn (`from src.config import ...` hoặc fallback `from config import ...`) đảm bảo script chạy mượt mà từ bất kỳ working directory nào mà không sợ lỗi ModuleNotFoundError.
  - Tự động xác thực Riot API Key ngay khi khởi động.

---

### ADR-010: Cơ chế Đồng bộ Hóa Dữ liệu Tự động từ Google Drive (Cloud Data Auto-Sync)
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Dữ liệu giải đấu chuyên nghiệp và các bộ dữ liệu nhãn/bổ sung do các thành viên nhóm cập nhật lên Google Drive dùng chung. Cần cơ chế để máy trạm tự động phát hiện và đồng bộ về local mà không cần tải thủ công.
- **Quyết định:** Tích hợp module kiểm tra thay đổi dựa trên siêu dữ liệu thời gian sửa đổi (`modifiedTime`) hoặc hash `md5Checksum` qua Google Drive API / `gdown`.
- **Lý do:**
  - Tối ưu hóa băng thông mạng: Chỉ tải dữ liệu khi trên đám mây thực sự có phiên bản mới hơn phiên bản cục bộ.
  - Tự động hóa khép kín quy trình làm việc nhóm (Collaborative Data Pipeline).
  - Tự động kích hoạt các bước tiền xử lý (Preprocessing) và cập nhật SQLite khi có dữ liệu mới.

---

### ADR-011: Khởi tạo & Tiêu chuẩn hóa Môi trường ảo Nội bộ (.venv) thay thế Python toàn cục
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Máy trạm người dùng có nhiều phiên bản Python (3.10, 3.13) dẫn đến xung đột đường dẫn thư viện (`pip install` vào Python này nhưng VS Code chạy bằng Python khác), gây lỗi `missing-import`.
- **Quyết định:**
  - Khởi tạo môi trường ảo `.venv` cô lập ngay tại thư mục gốc dự án (`Project/.venv`) bằng Python 3.13.
  - Cấu hình `.vscode/settings.json` trỏ trực tiếp `python.defaultInterpreterPath` về `.venv`.
  - Bổ sung lệnh kích hoạt `.\.venv\Scripts\Activate.ps1` vào đầu các tài liệu hướng dẫn.
- **Lý do:**
  - Cô lập 100% môi trường dependencies, không bị ảnh hưởng bởi môi trường Windows toàn cục.
  - Tái tạo môi trường nhất quán (reproducibility) cho tất cả các thành viên trong nhóm 3 người.
  - Tránh ô nhiễm mã nguồn do `.venv/` và `.vscode/` đã được chặn hoàn toàn trong `.gitignore`.

---

### ADR-012: Cơ chế Tự động phát hiện Mùa giải mới (Future-Proof Season Discovery) và Phân tách Tài liệu Module 01
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:**
  - Việc gán cứng các mùa giải trong mã nguồn `sync_google_drive.py` (như `[2025, 2026]`) sẽ khiến hệ thống không tự động kéo được dữ liệu khi Oracle's Elixir đẩy mùa giải mới (2027...) lên Drive chung.
  - File `README.md` của Module 01 ban đầu quá dài khi gộp cả Riot API và Google Drive, gây khó khăn cho việc tra cứu chuyên biệt theo từng phân công nhiệm vụ.
- **Quyết định:**
  - Triển khai thuật toán trích xuất năm qua biểu thức chính quy (Regex: `^(\d{4})_LoL_...csv`) trong hàm `get_recent_years(n_recent=2)`: Tự động sắp xếp và kéo $N$ mùa giải mới nhất có trên Drive (khi có 2027 sẽ tự động kéo `[2026, 2027]` mà không sửa code).
  - Tách tài liệu Module 01 thành 2 tệp chuyên biệt: [`README_CRAWL_RIOT.md`](../src/01_data_pipeline/README_CRAWL_RIOT.md) và [`README_SYNC_DRIVE.md`](../src/01_data_pipeline/README_SYNC_DRIVE.md); tinh gọn [`README.md`](../src/01_data_pipeline/README.md) làm trang Hub điều hướng.
- **Lý do:**
  - Đảm bảo tính mở rộng lâu dài (Open-Closed Principle / Future-Proofing).
  - Phân tách trách nhiệm tài liệu rõ ràng, minh bạch cho các thành viên trong nhóm.

---

### ADR-013: Thuật toán Quyết định Mùa giải Thông minh dựa trên Ngưỡng Quy mô Trận đấu (Adaptive Season Decision)
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:**
  - Trong Data Science và game eSports (LoL), giữa các mùa giải luôn có sự thay đổi lớn về bản đồ, mục tiêu (Sâu Hư Không, Atakhan...) và tướng/trang bị. Nếu gộp nhiều năm cũ sẽ gây hiện tượng trôi dạt khái niệm (**Concept Drift**) làm giảm sút chất lượng mô hình.
  - Tuy nhiên, ở giai đoạn **đầu mùa giải mới** (ví dụ đầu năm 2027), số lượng trận đấu chuyên nghiệp còn quá ít, không đủ cỡ mẫu thống kê để huấn luyện mô hình.
- **Quy tắc quyết định:**
  1. Luôn xác định và đồng bộ mùa giải **MỚI NHẤT** trên Google Drive (`latest_year`, ví dụ 2026).
  2. Đọc nhanh số trận đấu độc lập (`unique gameid`) trong tệp:
     - **Nếu số trận $\ge$ `MIN_MATCHES_THRESHOLD` (mặc định 3,000 trận):** Đánh giá năm mới nhất **ĐÃ ĐỦ LỚN** (năm 2026 hiện có 8,874 trận). Hệ thống **CHỈ DÙNG DUY NHẤT NĂM NÀY**, tuyệt đối **KHÔNG kéo thêm năm trước** (2025) để bảo toàn Meta trò chơi.
     - **Nếu số trận $<$ 3,000 trận (giai đoạn đầu mùa):** Tự động kích hoạt cơ chế ghép đuôi thích ứng (`build_adaptive_dataset`):
       - Lấy **toàn bộ** năm mới nhất.
       - Sắp xếp dữ liệu năm liền trước theo ngày thi đấu lùi dần từ cuối năm về trước, trích xuất đúng số trận còn thiếu từ **phần cuối năm** của năm trước đó cho đến khi đủ ngưỡng yêu cầu.
       - Xuất tệp hoạt động `data/raw/esports_active_matches.csv` để các bước tiếp theo phân tích.
  3. Cấu hình biến `ESPORTS_SEASON` và `ESPORTS_RAW_CSV` trong `src/config/settings.py` tự động phát hiện mùa giải kích hoạt thay vì gán cứng.
- **Lý do:**
  - Giải quyết triệt để bài toán cân bằng giữa: **Quy mô mẫu (Sample Size)** và **Tính thời sự của Meta (Recency & Homogeneity)**, tránh việc nạp dữ liệu đầu năm cũ đã quá lỗi thời.

---

### ADR-014: Hệ Thống Nhận Diện Trường Phái Đội Hình & Khuyến Nghị Điều Kiện Thắng (Draft Win Condition & Archetype Engine)
- **Ngày quyết định:** 2026-09-28
- **Bối cảnh:** Khi chọn xong đội hình cấm/chọn (Draft Phase lúc Phút 0), người dùng và ban huấn luyện không chỉ muốn biết tỷ lệ thắng tổng quan (% Winrate) mà còn cần chỉ dẫn chiến thuật cụ thể: Đội hình này thắng bằng cách nào? Cần đánh xoay quanh ai? Điểm rơi sức mạnh là khi nào? và Cần kiểm soát mục tiêu gì (Rồng hay Sâu Hư Không)?
- **Quyết định:**
  - Tích hợp module phân tích điều kiện thắng vào Giai đoạn 3 (Machine Learning & Recommender):
  - **1. Phân cụm Đội hình (Archetype Clustering qua K-Means & PCA - Chương 4):** Phân loại 159 tướng thành 5 trục sức mạnh `[Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control]` và nhận diện 4 trường phái đội hình:
    1. *Early Game Snowball / Dive* (Lăn cầu tuyết sớm).
    2. *Dragon Soul Stacking / Teamfight Control* (Kiểm soát chuỗi Rồng).
    3. *Late-Game Hypercarry Scaling* (Hậu kỳ tăng tiến sức mạnh).
    4. *Pick & Split-Push 1-3-1* (Bắt lẻ & Đẩy lẻ đường biên).
  - **2. Xuất Thẻ Điều Kiện Thắng (Win Condition Card):**
    - Trích xuất vị trí chủ lực gánh đội (Core Carry: Jinx, Smolder, Draven, Renekton...).
    - Xác định điểm rơi sức mạnh (Power Spike Timing: Trước phút 25 vs Sau phút 25).
    - Khuyến nghị mục tiêu ưu tiên số 1 (Primary Objective) và điều kiện thất bại cần tránh (Lose Condition).
  - **3. Đóng gói vào API & UI:** Trả về qua endpoint `POST /api/v1/recommend` và `POST /api/v1/predict`, hiển thị trực quan dưới dạng Radar Chart 5 trục trên giao diện Web App.
- **Lý do:** Nâng tầm đồ án từ một mô hình dự báo xác suất cơ bản thành một **Trợ lý Chiến thuật Toàn diện (AI Strategic Assistant)**, giúp đồ án đạt điểm số tối đa (A+) trước hội đồng giảng viên.

---

### ADR-015: Phân Tầng Meta Cấm/Chọn Theo Từng Khu Vực & Giải Đấu Quốc Tế (Regional & International Draft Meta Segmentation)
- **Ngày quyết định:** 2026-11-23
- **Bối cảnh:** Mỗi khu vực Esports lớn (`LCK`, `LPL`, `LCP`) có triết lý vận hành đội hình và bể tướng ưu tiên hoàn toàn khác nhau, và khi bước ra sân khấu quốc tế (`WLDS` / CKTG, `MSI`, `EWC`) sự giao thoa meta lại tạo nên đặc trưng riêng. Việc gộp chung toàn bộ 3,000 trận vào một bảng thống kê duy nhất sẽ làm mờ nhạt bản sắc khu vực.
- **Quyết định:**
  - Phân tách toàn bộ thống kê trong `RecommenderEngine` (`TargetBanEngine`, `MetaPickRecommender`) và `DraftPredictor` theo 8 chế độ khu vực (`LCK`, `LPL`, `LCP`, `WLDS`, `MSI`, `EWC`, `INTERNATIONAL`, `ALL`).
  - Áp dụng công thức **Hòa trộn Thích ứng (Adaptive Regional Blending)** với trọng số tin cậy $w_{\text{reg}} = \frac{n_{\text{reg}}}{n_{\text{reg}} + \tau}$ để vừa ưu tiên dữ liệu đặc thù của khu vực đang chọn, vừa tận dụng tri thức toàn cầu khi cỡ mẫu ở giải ngắn ngày còn nhỏ.
  - Bổ sung 8 đặc trưng One-Hot ngữ cảnh giải đấu vào `DraftPredictor` (`models/draft_model.pkl`, nâng tổng số chiều đặc trưng từ 799 lên **808 chiều**).
- **Lý do:** Đảm bảo mô phỏng Cấm/Chọn phản ánh đúng 100% thực tế chiến thuật của từng giải đấu chuyên nghiệp.

---

### ADR-016: Thuật Toán Khắc Chế & Đi Đường Tổng Quát 100% Dựa Trên Dữ Liệu (Universal Counter-Pick vs Blind-Pick Engine & Zero-Hardcode Principle)
- **Ngày quyết định:** 2026-11-23
- **Bối cảnh:** Khi đối thủ đã lộ tướng cùng đường, nếu thuật toán cộng gộp tuyến tính điểm phổ biến Meta (`eff_norm`) và điểm Tướng Tủ (`player_bonus`) quá cao, AI có thể gợi ý chọn một tướng phổ biến hoặc tướng tủ nhưng lại bị đối thủ khắc chế cứng trên đường (ví dụ: chọn `K'Sante` vào `Gnar` dù thua `-252 vàng` lúc 10 phút và chỉ thắng `42%`).
- **Quyết định:**
  - **1. Cấm tuyệt đối Hardcode tình huống lẻ:** Không bao giờ gán cứng kèo khắc chế bằng tay; áp dụng thuật toán tổng quát trên toàn bộ **3,098 cặp đối đầu 1v1** của cả **5 vị trí (`Top`, `Jungle`, `Mid`, `Bot`, `Support`)**.
  - **2. Nhận diện chính xác 1-1 tướng cùng đường (`_infer_enemy_lane_assignment`):** Ánh xạ chính xác vị trí của từng tướng địch để xác định đường nào đang chọn mù (`Blind Pick`) và đường nào đã biết đối thủ (`Counter Pick`).
  - **3. Ngưỡng Loại Bỏ Cứng Tổng Quát (Universal Hard Cut-off):** Trong chế độ `Counter Pick`, tự động loại bỏ mọi ứng viên có tỷ lệ thắng đối đầu $< 47.5\%$ (mẫu $\ge 3$ trận) HOẶC bị thua thiệt kinh tế phút 10 ($\text{GD@10} < -110\text{g}$ đối với Top/Jng/Mid/Bot; $< -150\text{g}$ đối với Sup nếu không có tỷ lệ thắng lật kèo $\ge 52.5\%$).
  - **4. Khóa điểm Tướng Tủ (`player_bonus`) khi gặp kèo dưới:** Cắt giảm 85–90% `player_bonus` nếu tướng tủ chưa được kiểm chứng thắng/hòa đường trước tướng đối diện.
  - **5. Làm mịn Bayes ($C=10.0$) & Độ tin cậy mẫu ($\alpha = \frac{n}{n+8}$) + Lọc độ tinh khiết vị trí (Role Purity Filter):** Ngăn các tướng trái vị trí có mẫu siêu nhỏ (2–5 trận) làm nhiễu kết quả gợi ý.
- **Lý do:** Triệt tiêu hoàn toàn hiện tượng gợi ý tướng tự hủy đường, đảm bảo tính khoa học, tổng quát và minh bạch (Explainable AI) cho toàn bộ hệ thống.

---

### ADR-017: Chuẩn Hóa Huấn Luyện Mô Hình Bằng GPU NVIDIA CUDA (Mandatory GPU-First Model Training)
- **Ngày quyết định:** 2026-11-23
- **Bối cảnh:** Máy trạm phát triển trang bị card đồ họa rời **NVIDIA GeForce RTX 4070 Laptop GPU** hỗ trợ đầy đủ tập lệnh CUDA. Khi tập đặc trưng mở rộng lên 808 chiều (`draft_model.py`) và 6,770 quan sát (`snowball_model.py`), việc huấn luyện bằng CPU đơn thuần gây lãng phí tài nguyên phần cứng và kéo dài thời gian thử nghiệm.
- **Quyết định:**
  - Thiết lập quy chuẩn **GPU-First Training**: Mọi quy trình huấn luyện mô hình học máy trong dự án bắt buộc ưu tiên chạy trên GPU (`device='cuda', tree_method='hist'` cho XGBoost), kết hợp đa luồng tối đa (`n_jobs=-1`) và Composite Indexes SQLite (`idx_tp_game_pos_side`, `idx_tp_game_side_pos`).
  - Duy trì hàm tự động phát hiện `_check_xgb_gpu_support()` để đảm bảo khả năng chạy tương thích an toàn trên cả các máy không có GPU rời.
- **Lý do:** Rút ngắn thời gian huấn luyện toàn bộ pipeline xuống chỉ còn vài giây mà vẫn giữ nguyên độ chính xác toán học.






---

ADR-017 (2026-11-23): Ưu tiên tính kiểm chứng. Điểm quy tắc không là xác suất; không công bố uplift nhân quả. Dùng shared domain cleaning, không fit outlier bounds trên toàn dữ liệu. Huấn luyện XGBoost CUDA; validation chọn model, calibration chọn shrinkage xác suất, test chỉ dùng đánh giá. Rank không có event time phải công khai grouped holdout.
