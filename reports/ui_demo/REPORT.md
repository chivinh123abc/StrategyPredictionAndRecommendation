# Kiểm tra UI DraftLab — 24/11/2026

Đã hiện thực một trang React + TypeScript và API FastAPI dùng lại engine. Bản local: http://127.0.0.1:8000. Hướng dẫn bền vững: [UI_REACT_TYPESCRIPT](../../docs/UI_REACT_TYPESCRIPT.md).

- TypeScript typecheck và Vite production build PASS; bundle `web/dist` thực có, không đưa node_modules/dist vào Git.
- 154 Python unit tests PASS, trong đó 8 API tests mới. [Log](tests.log). PowerShell có thể ghi NativeCommandError quanh progress stderr của unittest; kết luận của unittest là `Ran 154 tests ... OK`, không có failed test.
- Browser thật Playwright + Edge PASS: 6 ban đầu, pick có bảng hai nguồn, đổi đường, hoàn tác, tự hoàn thành một draft 20 lượt, sang ván 2 khóa 10 tướng, xem ván cũ, xuất JSON và reload. Viewport 1512px và 390px; không tràn ngang mobile, không pageerror. [Browser log](browser.log), [desktop](desktop.png), [mobile](mobile.png), [export thật](export.json).
- API tests còn kiểm chuỗi **5 ván bằng input chọn tay** với khóa được suy ra từ lịch sử, từ chối tái sử dụng và ván trước chưa hoàn tất. Đây không phải 5 ván auto chạy trên browser.
- Không đổi thuật toán/weights, không retrain, không ghi canonical SQLite; SHA256 trước/sau giữ nguyên. Export không có khóa định danh người chơi/API key được kiểm. Static chỉ phục vụ bundle, `.env` và đường dẫn DB trả 404.

Máy thử Node 24.16.0, React 19.3.1, TypeScript 7.0.2, Vite 8.3.8, FastAPI 0.165.0. Dependencies cụ thể được khóa trong `web/package-lock.json` và Python runtime lock. [Checks máy đọc](checks.json). PID của server tạm ở [process manifest](process.json); manifest chỉ là mốc khởi động, phải kiểm tra tiến trình trước khi dùng để dừng.

Giới hạn: UI hiện phục vụ Pro draft, Rank chỉ là bằng chứng; current score là heuristic, không phải xác suất. Cho phép auto thiếu bằng chứng chỉ để test và vẫn gắn nhãn. Chưa chứng minh counter cơ chế, tăng thắng hoặc tối ưu toàn BO5. Metadata dữ liệu cũ/khác patch được giữ; cache server không phải cập nhật live. Không thêm tài khoản, cloud hoặc cơ sở dữ liệu phiên mới. Kết quả test tính hợp lệ không là đánh giá chiến thuật độc lập.
