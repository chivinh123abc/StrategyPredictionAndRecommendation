# Bảo vệ cặp bot và First Selection độc lập màu đội — 24/11/2026

[Phương pháp/giới hạn](../../docs/GIU_CAP_BOT_VA_FIRST_SELECTION.md). UI local: http://127.0.0.1:8000.

## Tái hiện chính xác prefix cũ

Cùng10lượtđầu, snapshotWLDS/patch16.20/ngày24/11/currentpick. Cũtop1Jayce(top), sauđóRedbanJhin/Kai’Sa, BluekếtthúcNautilus–Yunara. CặpNautilus–Jhin5mẫu/Kai’Sa6mẫu/Yunara1mẫu. Chưađủkếtluậncơchếphốihợptốt/xấu.

Bảnmớitop1Jhin(bot),Kai’Sa cũngđượcưu tiêngiữcặp; Jayce vẫnhợplệ nhưngcảnhbáo2đốitác/2banđịch. Khôngđổiscoregốccácứngviênchung. Phòngngừađượcdựatrênlịchbantrướclượtpicktiếp, khôngdựđoánchắcđịchbanhayduyệtcâyphảnứng.

Chạytiếptừcùngprefixvớitestoverride hoànthành20lượthợplệ,BlueNautilus–Jhin. KhôngnerfbanRed,khôngtạokếtquảtrận. [regression.json](regression.json), [same_prefix_completed.json](same_prefix_completed.json).

| Lượt | Đội | Hành động | Bản cũ | Chạy tiếp bản sửa |
|---:|---|---|---|---|
| 1 | blue | ban | Qiyana | Qiyana |
| 2 | red | ban | Nocturne | Nocturne |
| 3 | blue | ban | Olaf | Olaf |
| 4 | red | ban | Vi | Vi |
| 5 | blue | ban | Ezreal | Ezreal |
| 6 | red | ban | Lee Sin | Lee Sin |
| 7 | blue | pick | Cassiopeia (mid) | Cassiopeia (mid) |
| 8 | red | pick | Renata Glasc (sup) | Renata Glasc (sup) |
| 9 | red | pick | Kalista (bot) | Kalista (bot) |
| 10 | blue | pick | Nautilus (sup) | Nautilus (sup) |
| 11 | blue | pick | Jayce (top) | Jhin (bot) |
| 12 | red | pick | Orianna (mid) | Orianna (mid) |
| 13 | red | ban | Jhin | Jayce |
| 14 | blue | ban | Jarvan IV | Jarvan IV |
| 15 | red | ban | Kai'Sa | Rumble |
| 16 | blue | ban | Pantheon | Pantheon |
| 17 | red | pick | K'Sante (top) | Ambessa (top) |
| 18 | blue | pick | Wukong (jng) | Wukong (jng) |
| 19 | blue | pick | Yunara (bot) | Galio (top) |
| 20 | red | pick | Xin Zhao (jng) | Trundle (jng) |

## Kiểm tra5ván và quyền chọn trước

[BO5đầyđủBan1–5/Pick1–5vàlýdo](bo5/REPORT.md), [series.json](bo5/series.json), [log](bo5.log). T1Blue/Gen.GRedgiữnguyên;firstselectionuserconfiguredRed,Red,Blue,Blue,Red. Đủ5ván/100actions/50pickunique/locks0–10–20–30–40,khôngresetván5.

Đãbậttestoverrideđểđiđủ5ván; có4pickrequires_reviewvềcặp và1picksecure_now. Khôngnhậntấtcảcặpđủmẫu hoặc tốiưu chỉvìdraftchạyxong.

UIbắtbuộcchọnBlue/RedtrướckhiSangván, khôngtựluânphiên. API/CLIhỗtrợlặpfirstselection;CLI`--first-picks`đúngsốván,mặcthịchCLIcũgiữlegacyalternatingdemođểtáilập,khôngnhậnnólàluậtgiải. Đây làquyđịnhphiêndongườidùngyêucầu; nguồnFearlesskhôngđượcgánthànhnguồnxácnhậnFirstSelectionmới.

## Kiểm chứng

-170Python testsPASS(11mới:7lịch/đốitác/sparse/mirror/first-selection,4APIregression/rolefilter/Redfirst/repeatfirst). [tests.log](tests.log).
-TypeScript/VitebuildPASS;3EdgeworkflowsPASS:hailựachọn/manual/flex/undo/auto/archive/export/reload/mobile; snapshotconflict; vàRedchọntrước+đúngprefixgiữcặp/cảnhbáoTop. Khôngtrànngang/mobilehoặcpageerrorởworkflowchính. [browser.log](browser.log), [desktop](desktop.png), [mobile](mobile.png), [pair-window](pair-window.png), [export](export.json).
-ProDBhash20e3d973...giữnguyên,khôngretrain/đổiRankcollector/commit/push; exportkhôngplayerID/key. [checks.json](checks.json).

## Giới hạn

Đây làregression/thửluậtvàtínhhợplệ, khôngfreshholdout hoặcchứngminhtăngthắng. Cặpđượclịchsửhỗtrợkhôngbằngcặptốiưu;WR/CIcôngkhai,mẫuítkhôngđượcbịađộchắc. Guardchỉxétbot/supkhiđịchđãlộassignmenthairole, banbudgettrướcpicktiếp vàpartnerhợplệ; khônggiảibàitoántấtcảcặp/đốithủpickmất/độimìnhtựban/globalBO5. Chọn tay/lọcrole/vàwishlistđượctôntrọng, cócảnhbáo. Bancontextualv2vàbasepickcurrentgiữnguyên;Rankvẫnlàbằngchứngriêng.

Mãsnapshotcópair_safetyversionnênphiêncũcóthể409;exportinputscũvàtạoPhiênmớiđểdùngpolicyhiện tại. Processmanifesthiệnhành[process.json](process.json); PIDphảixácminhtrướckhistop. Táilập:`.\.venv\Scripts\python.exe scratch/check_pair_reservation_revision.py`vàlệnhBO5tronghướngdẫn.
