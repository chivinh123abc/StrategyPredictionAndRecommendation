# Giữ cặp bot trước pha ban và chọn trước độc lập màu đội

Ngày24/11/2026. Thay đổi theo tình huống người dùng chỉ ra; **MR-24/NV-23**, không thêm model hoặc tìm kiếm cây phản ứng.

## Vấn đề đã tái hiện

Trong bản lưu `reports/contextual_ui_revision/export.json`, Blue đã có Cassiopeia và Nautilus, Red đã lộ Renata–Kalista. Blue chọn Jayce ở lượt11, sau đó Red ban Jhin/Kai’Sa ở lượt13/15; Blue kết thúc với Nautilus–Yunara. Lúc đó snapshotWLDS có Nautilus–Jhin5mẫu, Nautilus–Kai’Sa6mẫu, Nautilus–Yunara1mẫu. Đây là bằng chứng độ phủ lịch sử hẹp, **không đủ kết luận Yunara không phối hợp được hoặc Jhin/Kai’Sa là đáp án tối ưu**.

Pick scorer cũ có association với đồng đội đã lộ nhưng không bảo vệ các đối tác chưa pick trước pha ban tiếp theo. Vấn đề nằm ở thứ tự pick của Blue; không cần làm yếu contextual ban của Red để sửa.

## Cách xử lý có giới hạn

`pair_reservation.py` dùng lại `DraftMetaSnapshot.pair_evidence`, ngưỡng bằng chứng hiện hànhn5 và associationlift đã có:

1. Chỉ kích hoạt kiểm tra này khi đối thủ đã có cả bot/sup trong assignment hiện tại. Role là assignment draft, có thể thay đổi bằng flex/swap.
2. Đếm **số ban của đối thủ sau pick hiện tại đến trước lượt pick tiếp theo của mình**, theo `DraftState.schedule`. Không giả định Blue đi trước; nếu mình còn một pick liền thì budgetban=0.
3. Đối tác phải nằm trong pool đúng role, chưa pick/ban/khóaFearless, có cặp n≥5 và effectiveassociationlift≥1. Quét đầy đủ pool bot/sup, không suy chỉ từ5gợiý đầu. Lift≥1 là mốc độc lập lịch sử, không phải kiểm định ý nghĩa thống kê hoặc cơ chế synergy.
4. Nếu đã lộ một nửa cặp và số đối tác được hỗ trợ dương nhưng ≤budgetban, các pick hoàn tất cặp được đưa lên trước các pick vị trí khác. Giữ điểm `current` nguyên; lưu `priority_tier`, lý do và số mẫu riêng. Wishlist rõ của người dùng và lớp ứng viên đủmẫu vẫn có ưu tiên như cũ.
5. Khi chưa chọn cả hai role bot, tránh một cam kết mới có quá ít đối tác trước pha ban nếu còn lựa chọn khác cùng mức bằng chứng. Không gọi lựa chọn thiếu mẫu là yếu. Chọn tay và lọc role vẫn được tôn trọng; lọcTop chỉ trảTop với cảnh báo, không trảADC dưới tênTop.
6. Cặp đã hoàn tất nhưng thiếu hỗ trợ hoặc không còn đối tác đủ mẫu trước pha ban sẽ yêu cầu review khi tự chọn. `--allow-statistical-auto`/ôtest có thể bỏ qua để thử đủván nhưng giữ nhãn; chọn tay vẫn là quyết định người dùng.

`budgetban=2, đối tác=2` chỉ có nghĩa đối thủ **có thể** loại cả hai nếu dùng hai lượt ban đó. Không mô phỏng hoặc khẳng định họ sẽ ban thế; không tính xác suất tương lai, không có lookahead/search/đặt tướng cho toànBO5. Pool đối tác sống sót cũng không bảo đảm kèo đi đường hoặc chất lượng toànđội; chưa xét đầy đủ nguy cơ bị đối thủ pick mất hoặc ban từ đội mình.

## First Selection theo cấu hình phiên

Giữ màuBlue/Red của hai đội, người dùng chọn bên đi trước độc lập cho **từngván**, có thể Red–Red hoặcBlue–Blue liên tiếp. Engine đã có `first_side` và lịch ban/pick tương ứng; UI bỏ tự luân phiên và yêu cầu chọn rõ bên đi trước trước khi bấm Sangván. Khi chưa đi lượt nào có thể đổi lựa chọn; khi có lịch sử thì khóa để tránh làm sai thứ tự.

Đây là **luật phiên do người dùng yêu cầu**. Không khẳng định mọi giải/Worlds dùng luật này hoặc gán nguồnFearless2025 thành nguồn xác nhận luật mới. `first_side` điều khiển FirstSelection của cả lịch cấm/chọn trong simulator; không đổi màu đội theo bên chọn trước.

CLI:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-24 --patch 16.20 --games 5 --ban-strategy contextual --first-picks red,red,blue,blue,red --allow-statistical-auto --output-dir reports/pair_reservation_revision/bo5
```

Mỗi phần tửblue/red tương ứng mộtván, số phần tử phải đúng `--games`. **Cập nhật mới hơn cùng ngày:** series nhiều ván bắt buộc có `--first-picks`; đã bỏ fallback luânphiên cả trongCLI. Có thể `blue,blue,blue,blue,blue` hoặc `red,red,red,red,red`. [Luồng hiện hành](UI_COMPACT_VA_KIEM_KEO_DA_LO.md). Những report có legacy_alternating_demo là lịch sử trước cập nhật này. UI luôn cho người dùng chọn từngván.

## Nơi dùng, kiến thức, minh chứng

- `pair_reservation.reserve_pairs/enemy_bans_before_next_pick`: constraint tự thiết kếMR-24; tái sử dụng association/n/Wilson củaMR cũ. Chương1 tần suất, Chương5/5x lọc/nhóm là nền; Chương6 profile/cosine vẫn thuộc scorer hiện có. Quy tắc giữ đối tác trướcban **không phải thuật toán đã học trong Chương6**.
- `simulate_draft_match.pick_candidates`: bật guard cho contextual, mở fullbot/sup rồi xếp theo lớp bằng chứng/ưu tiên và score gốc. Legacy không bật. `needs_tactical_review` xét thêm cặp thiếu hỗ trợ. JSON/history/explain giữ `pair_reservation` để không giấu lý do đổi thứ tự.
- `src/api/app.py`: dùng cùng guard, whitelist metadata, fingerprint thêm `pair_safety` để không âm thầm trộn phiên trước/sau. Phiên cũ có thể409 và vẫn xuấtinput/tạoPhiênmới được.
- `simulate_fearless_series.first_selection_order/run_series`: nhận lịchuserconfigured; report ghi lịch thực từngván và phân biệt nguồn luật phiên với nguồnFearless.
- UI `App.tsx`: lý do giữ cặp/cảnh báo, n/WR/CI và đối tác còn lại; quyền chọn trước ở mỗi ván. React/TS/API làNV kỹthuật ngoài môn, không thêm framework.
- [Report và kiểm tra](../reports/pair_reservation_revision/REPORT.md), [tái hiện cùngprefix](../reports/pair_reservation_revision/regression.json), [draft tiếp tục cùngprefix](../reports/pair_reservation_revision/same_prefix_completed.json), [BO5](../reports/pair_reservation_revision/bo5/REPORT.md). So sánh regression và độhợplệ, không là kiểm chứng tăng thắng hoặc nhãn chiếnthuật độc lập.

Tái lập tình huống: `.\.venv\Scripts\python.exe scratch/check_pair_reservation_revision.py`; kiểmthử: `.\.venv\Scripts\python.exe -m unittest discover -s tests`, tạiweb`npm run test:e2e` vớiAPIđangchạy/Edge. Sổkiếnthức tập trungmục29 ghi trạng thái/output/kếtquả thực tế.
