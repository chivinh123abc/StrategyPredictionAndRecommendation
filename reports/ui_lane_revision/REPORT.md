# UI gọn, auto-role và kèo đã lộ — 24/11/2026

[Hướng dẫn/phương pháp](../../docs/UI_COMPACT_VA_KIEM_KEO_DA_LO.md). UI local http://127.0.0.1:8000; cần tạo Phiên mới nếu fingerprint policy cũ không khớp.

## Thay đổi đã chạy

- Thiết lập phiên trên đầu; gợi ý trái, chọn tay phải; Hiểu lựa chọn phía dưới. Bảng đội hình gọn, kéo tướng sang slot trống hoặc đổi với tướng cùng đội. Có menu bàn phím/chạm dự phòng, không claim kéo bằng cảm ứng đã hỗ trợ.
- Chọn tay không cần dropdown role. Preview và API cùng dùng tần suất role trong snapshot Pro, bỏ role đã có tướng, chọn role tiếp theo đã quan sát. Không có role đã quan sát còn trống thì báo rõ, không bịa slot phù hợp.
- First Selection do người dùng chọn từngván; CLI nhiều ván bắt buộc --first-picks, không còn tự luân phiên.

## Galio / Renekton

Tái hiện đúng prefix18lượt: Ambessa Top đã lộ, địch có4tướng. Cũtop1Galio0mẫu vẫn được auto vì gate chờ đủ5địch. Bản mới kiểm lane đang gán ngay khi lộ, n<5 cần review; không nâng nhãn counter, vẫn cho xác nhận tay/testoverride.

Khi so cùngrole hoặc tất cả role còn mở đã có địch tương ứng, dùng cận dưới Wilson95% của WR cả trận trước điểm tổng. Wishlist/lớp ứng viên đủmẫu/giữcặp bot vẫn ưu tiên. Không coi role blind tốt hơn chỉ vì chưa có địch. Điểm current và weights giữ nguyên.

| Tướng vs Ambessa Top | n Pro | WR trận | Wilson95% | GD15 | Điểm gốc |
|---|---:|---:|---|---:|---:|
| Gnar | 6 | 83.3% | 43.6–97.0% | +686 | 22.85 |
| Renekton | 2 | 100% | 34.2–100% | +787 | 18.59 |
| Galio | 0 | — | — | — | 27.24 |

Thứ tự mới trong cùng trạng thái: **Gnar, Renekton, Camille, K’Sante, Galio**. Renekton không còn ở cuối nhưng2mẫu vẫn cần review. 100%=2/2 không chứng minh vượt trội; Wilson và meanGD15CI chồng lấn với Gnar. MeanGD15RenektonCI≈+520…+1054, Gnar≈+283…+1089. CompositionliftRenekton≈0.718 từng làm giảm điểm gốc; đó là association, không cơ chế phối hợp. Gold/XP/CS vẫn chỉ giải thích, chưa thêm vào score; Rank tách riêng không đổi điểm Pro.

[lane_audit.json](lane_audit.json) lưu prefix/scope/policy/scorecomponents/CI; [automatic_top_response.json](automatic_top_response.json) xác nhận autoGnar. Đây là regression cùngprefix, không independent final quality test, không chứng minh tăngthắng hoặc Gnar countercơchế.

## Kiểm chứng

- **178Python testsPASS**,8mới cho rolefallback/noinventedrole, gate địch chưađủ5, blind/supported, bắtbuộcfirstselection, realGalio/Renekton case. [tests.log](tests.log).
- **5Edge workflowsPASS**: bố cục hai khu theo tọa độ, manual/auto, ProRank, flex/undo/nextgame/archive/export/reload/mobile; mismatchsnapshot; Redfirst/giữcặp; autoGalioTopkhiMidbận và dragoccupied/cross-teamreject; sốmẫuGalio/Renekton vàGD15. [browser.log](browser.log).
- [desktop](desktop.png), [mobile](mobile.png), [kéo/auto-role](drag-and-auto-role.png), [kèo](lane-audit.png), [export thật](export.json).
- [BO5Bluechọntrướccả5ván](bo5_blue_first/REPORT.md), [series](bo5_blue_first/series.json), [log](bo5.log):5draft/100action/50pickunique/locks0-10-20-30-40, testoverridebật đểhoànthành, khônggamewinnergiả. [first_selection_checks.json](first_selection_checks.json) kiểm allBlue/allRed5ván bằng inputchọntayhợplệ; không gọi đó là2BO5auto.
- ProDBhash20e3d973...khôngđổi, khôngmodeltraining/Rankcollectorchange/commit/push, publicJSONkhôngplayerID/APIkey. [checks.json](checks.json). Servermanifest ở[process.json](process.json), cầnxácminhPIDtrướckhistop.

Tái lập: `.\.venv\Scripts\python.exe scratch/check_ui_lane_revision.py`; `npm --prefix web run build`; `.\.venv\Scripts\python.exe -m unittest discover -s tests`; `.\start_ui.ps1`; tạiweb`npm run test:e2e`khiAPIđãchạy/cóEdge. LệnhBO5vàgiới hạntronghướngdẫn.
