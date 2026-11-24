# UI DraftLab — React + TypeScript

Bản đầu ngày 24/11/2026, chạy tại máy cá nhân. Giao diện một trang phục vụ **draft giải** bằng engine hiện có. Rank xuất hiện ở bảng bằng chứng đối đầu; chế độ recommender Rank riêng chưa được đưa lên UI.

## Chạy ứng dụng

Cần Python với `.venv`, Node.js tương thích Vite 8 (máy kiểm tra dùng Node 24.16.0), npm. Tại thư mục gốc dự án, cài lần đầu:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix web ci
```

Chạy:

```powershell
.\start_ui.ps1
```

Mở **http://127.0.0.1:8000**. Giữ cửa sổ chạy mở; Ctrl+C để dừng. Script build TypeScript rồi dùng Python phục vụ cả UI và API, không cần hai dịch vụ khi sử dụng. Có thể đổi cổng bằng `-Port 8001`. Không cần Riot API key để xem bằng chứng đã thu; không dán khóa vào trình duyệt.

Để phát triển UI với cập nhật tức thì, chạy riêng Python API ở cổng 8000 và `npm --prefix web run dev` ở cửa sổ khác. Vite chuyển `/api` về API local. Sau khi sửa Python phải khởi động lại API; sau khi sửa UI ở chế độ sử dụng phải build lại.

## Cách dùng

1. Chọn giải/khu vực, hai đội, đội chọn trước và cách ban **contextual hoặc legacy** trước lượt đầu. Mặc định minh họa Worlds, T1–Gen.G; không gán sẵn tướng hay kết quả cho hai đội.
2. Mỗi lượt hiện rõ đội nào **Ban 1–5 / Pick 1–5**. Thiết lập ở đầu; **Gợi ý trái, Chọn tay phải**, mỗi khu có nút xác nhận riêng; Hiểu lựa chọn ở dưới. Chọn tay chỉ tìm tướng và xác nhận: hệ thống tự xếp vào đường phổ biến nhất còn trống theo snapshot. Không có dropdown role cho lượt chọn tay. Sau một lượt cả hai khu cập nhật theo trạng thái mới.
3. Bảng lý do hiển thị số mẫu và các thành phần điểm. Khi có đối thủ phù hợp, bảng **Pro / Rank riêng** cho winrate lịch sử, CI95 và chênh vàng/XP/CS phút 10/15 với số mẫu từng chỉ số. “—” là thiếu dữ liệu.
4. **Kéo thả tướng trên bảng đội hình** sang đường trống hoặc sang một tướng cùng đội để đổi chỗ; có menu dự phòng cho bàn phím/chạm. Không đổi giữa hai đội hoặc sửa ván lưu cũ. Đây là quyết định flex của người dùng, không phải xác nhận mọi tướng đều phù hợp mọi đường. **Hoàn tác** bỏ lượt ban/pick cuối và các đổi đường phát sinh sau lượt đó.
5. **Tự draft ván** lần lượt chọn gợi ý số 1. Có thể dừng sau lượt đang xử lý. Khi engine yêu cầu review, auto dừng; ô **Cho phép chọn thiếu bằng chứng (chỉ test)** cho phép tiếp tục nhưng giữ cảnh báo. Việc người dùng xác nhận chọn tay không cần bật ô này.
6. Hoàn thành 20 lượt mới **Sang ván tiếp theo**. Các tướng đã pick bị khóa ở cả hai đội cho những ván sau; ban đặt lại. Tối đa5ván; **chọn rõ Blue hoặc Red đi trước cho từngván**, không tự luân phiên. Có thể cùng một bên chọn trước nhiều ván liên tiếp; màu đội giữ nguyên. Có thể đổi khi ván chưa đi lượt nào. Đây là luật phiên do người dùng thiết lập, không là xác nhận luật của mọi giải. Không giả lập thắng/thua hay tỷ sốBO5.
7. Bấm số ván đã xong và từng lượt trong lịch sử để xem lại. Bằng chứng được tính lại từ trạng thái **trước lượt đó**, không lấy điểm do trình duyệt gửi lên. Phiên tự lưu input trong localStorage của trình duyệt; **Xuất JSON** tải lịch sử và phạm vi dữ liệu về máy.

## Phạm vi và kiến thức

- `web/src/App.tsx`, `types.ts`, `api.ts`: React state, TypeScript, fetch, localStorage và CSS; **NV-21, kỹ thuật ngoài môn để làm giao diện**, không là thuật toán khoa học dữ liệu mới.
- `src/api/app.py`: FastAPI/Pydantic kiểm input, dựng lại state hợp lệ, gọi advisor/BanPlanner, trả JSON; cache advisor có giới hạn và khóa tuần tự bảo vệ cache dùng chung. Server không ghi vào SQLite hoặc giữ phiên của từng người dùng.
- Engine vẫn dùng kiến thức/thống kê/content-based ở sổ hiện hành, đặc biệt Chương 6; **pick scoring mặc định `current`**. Không tự chuyển sang công thức simple đã giảm chất lượng trong phép so trước. Không thêm lookahead, mô hình hoặc tối ưu toàn BO5.
- UI dùng pool ứng viên tối thiểu 1 trận để hỗ trợ demo nhiều ván; ngưỡng bằng chứng vẫn 5 và ứng viên ít mẫu có nhãn. Điểm ưu tiên không phải xác suất thắng, tần suất suy vị trí không phải độ chắc chắn cơ chế counter.
- Metadata thể hiện patch/cửa sổ và thời điểm dữ liệu thật. Advisor cache theo khu vực/cutoff trong vòng đời server; khi cập nhật dữ liệu cần khởi động lại để lấy snapshot mới. Không gọi đây là meta trực tiếp hiện tại.
- **Bổ sung NV-22:** thanh cấu hình hiện `Ban contextual/legacy`, `Pick current`, ngày cutoff cố định và mã snapshot. Lần tải đầu nếu ngày trống, API chốt ngày UTC hiện tại; localStorage/export giữ ngày đó. Snapshot SHA256 gắn nguồn Pro, scope, đội/roster, scoring/ngưỡng và version contextual. Nếu mã phiên không khớp, API409 thay vì lặng lẽ trộn kết quả; vẫn có thể xuất inputs cũ và bấm Phiên mới. Nếu chính file Pro đổi trong vòng đời cache, phải restart API trước khi tiếp tục. Đây là fingerprint kiểm tra nguồn/cấu hình, không lưu bản sao DB lịch sử hay toàn bộ code/dependencies, không tự khôi phục engine cũ.
- Contextual ban hiện là **v2 fixed-capacity pool**; sửa cách chấm pool dưới3lựa chọn, không thay công thức pick `current`. [Công thức và so sánh với bản cũ](BAN_LEGACY_VA_CONTEXTUAL.md). Không tuyên bố đã tăng accuracy chiến thuật từ một sửa lỗi số học.
- **Cập nhật MR-24/NV-23:** contextual pick dùng `current + giữ cặp bot`. Khi địch đã lộ cặp bot, kiểm số đối tác đủmẫu và số ban địch trước lượt pick tiếp theo; có thể ưu tiên hoàn tất cặp thay vì đi vị trí khác. Điểm gốc không bị tăng giả, lý do/nhãn/CI riêng. Đây là ràng buộc theo lịch và lịch sử đồngchọn, không bảo đảm cặp tối ưu. [Phương pháp, giới hạn và FirstSelection](GIU_CAP_BOT_VA_FIRST_SELECTION.md).
- Rank là snapshot đạt chuẩn 10 người Master+ lúc kiểm tra, không phải chứng nhận rank lịch sử. Patch khác/thiếu mẫu phải đọc riêng. Bằng chứng Rank chưa đổi điểm Pro.
- Ảnh tướng từ Riot Data Dragon theo catalog 16.20.1, font từ Google Fonts; cần mạng để tải các tài nguyên này, có fallback chữ/font hệ thống. Các quyết định và thống kê dựa trên dữ liệu local.
- Chưa có tài khoản, đồng bộ nhiều máy, server production, chế độ Rank riêng hoặc chứng minh tăng tỷ lệ thắng. Đó không phải điều kiện hoàn tất UI minh họa này.

## Kiểm chứng và file kết quả

```powershell
npm --prefix web run build
.\.venv\Scripts\python.exe -m unittest discover -s tests
# Cần API đã chạy và Microsoft Edge; chạy tại thư mục web:
npm run test:e2e
```

`web/dist/` là bundle build được, đã bỏ qua trong Git. Kiểm tra API ở `tests/test_ui_api.py`; browser workflow ở `web/e2e/draft.spec.ts` dùng Playwright + Edge thật. [Báo cáo kiểm tra](../reports/ui_demo/REPORT.md), [desktop](../reports/ui_demo/desktop.png), [mobile](../reports/ui_demo/mobile.png), [JSON xuất thử](../reports/ui_demo/export.json). File tải về của người dùng nằm tại thư mục download do trình duyệt chọn; API không tự tạo file cho mỗi phiên.

**Minh chứng mới nhất sau sửa hai khu/contextual v2:** [report](../reports/contextual_ui_revision/REPORT.md), [desktop](../reports/contextual_ui_revision/desktop.png), [mobile](../reports/contextual_ui_revision/mobile.png), [export](../reports/contextual_ui_revision/export.json), [comparison](../reports/contextual_ui_revision/comparison.json). Thư mục ui_demo là mốc UI v1, không được đọc như ảnh của bản hiện hành. Process manifest hiện hành ở reports/contextual_ui_revision/process.json; PID cần xác minh trước khi dừng.

**Mốc mới hơn — giữ cặp và chọn trước từngván:** [report](../reports/pair_reservation_revision/REPORT.md), [tình huốngbot](../reports/pair_reservation_revision/pair-window.png), [export](../reports/pair_reservation_revision/export.json), [BO5đầyđủ](../reports/pair_reservation_revision/bo5/REPORT.md). Servermanifest hiện hành chuyển sang reports/pair_reservation_revision/process.json; các foldertrước giữ là lịch sử. Có thể cần Phiênmới do fingerprint thay đổi khi bật guard.

**Hiện hành mới nhất — UI gọn/auto-role/drag/kèo đã lộ:** [hướng dẫn và lý do Renekton](UI_COMPACT_VA_KIEM_KEO_DA_LO.md), [report](../reports/ui_lane_revision/REPORT.md), [ảnh](../reports/ui_lane_revision/desktop.png), [audit](../reports/ui_lane_revision/lane_audit.json). Kèo cùng role đã lộ được kiểm tra ngay, không chờ đủ5địch. Khi so cùng role dùng cận dưới Wilson của WR trận trước điểm tổng; dưới5mẫu vẫn cần review. Vàng/XP/CS chưa cộng vào điểm gốc. CLI nhiềuván bắt buộc `--first-picks`, không còn fallback luânphiên. Processmanifest hiện tại ở reports/ui_lane_revision/process.json; các mốc trên giữ lịch sử.

Đối chiếu kỹ thuật: [React](https://react.dev/learn), [TypeScript](https://www.typescriptlang.org/docs/), [Vite](https://vite.dev/guide/), [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/), [Playwright](https://playwright.dev/docs/intro). Mapping báo cáo tập trung ở [sổ kiến thức, mục 27](TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md).

**Hiểu lựa chọn — thao tác hiện hành:** ẩn mặc định. Bấm một tướng ở gợiý/chọntay để mở; bấm lại đúng tướng để bỏchọn vàẩn. NútĐóng thu phầngiảithích nhưnggiữlựachọn, cóthểMởlại; khi bỏchọn thì khôngcònnútmở. Sanglượt/đổiván/reloadkhôngtựmở. [Minhchứng7Edge tests](../reports/ui_inspector_toggle/REPORT.md). Khôngđổiđiểmgợiý.

**Thu gọn toàn bộ phần giải thích:** bấm “Thu gọn toàn bộ” trên tiêu đề để ẩn cả nội dung/bảng nguồn, chỉ giữ một thanh nhỏ; phần Diễn biến lập tức dịch lên. Bấm “Mở rộng” để xem lại, không mất tướng đang chọn. [Kiểm tra](../reports/ui_inspector_collapse/REPORT.md).

**Thu gọn toàn bộ phần giải thích:** bấm “Thu gọn toàn bộ” trên tiêu đề để ẩn cả nội dung/bảng nguồn, chỉ giữ một thanh nhỏ; phần Diễn biến lập tức dịch lên. Bấm “Mở rộng” để xem lại, không mất tướng đang chọn. [Kiểm tra](../reports/ui_inspector_collapse/REPORT.md).
