# Khôi phục bảng đội hình ở giữa — 24/11/2026

Theo chỉnh hướng của người dùng: hai bảng Blue/Red được căn giữa, giới hạn rộng1000px; mỗi đội có5vị trí xếp dọc và ảnh47px như trước. Bỏ kiểu5thẻpick nằm ngang vừa thêm. Phần thiết lập vẫn trên đầu, gợi ý trái/chọn tay phải và hiểu lựa chọn ở dưới; auto-role/drag/drop vẫn giữ.

Chỉ sửa CSS trình bày, không đổi Python/API, scoring, dữ liệu, mẫu số, rolepolicy hay luật draft. Không thêm kiến thức khoa học hoặc retrain; phân loại cập nhật NV-24. Không chạy lại Python tests vì không có thay đổi tác động tới logic Python.

TypeScript/Vite production build PASS. Edge layout test PASS: bảng ở giữa workspace, role xếp dọc, hai khu lựa chọn cùng hàng, inspector ở dưới và390px không tràn ngang. [Log](browser.log), [desktop](desktop.png), [mobile](mobile.png). Test: `web/e2e/centered-board.spec.ts`; chạy `npm --prefix web run test:e2e -- centered-board.spec.ts` khi APIlocalđangchạy.

Server vẫn http://127.0.0.1:8000; chỉ build lại bundle, không cần khởi động lại Python. PIDmanifest ở reports/ui_lane_revision/process.json là mốc khởi động trước đó, phải xác minh trước khi dừng. Không commit/push.
