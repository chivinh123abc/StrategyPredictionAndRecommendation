# AI WORKING RULES & PROJECT PROTOCOL

Tài liệu này là quy chuẩn bắt buộc đối với tất cả các AI session khi làm việc trên dự án.

## 1. NGUỒN SỰ THẬT (TRUTH HIERARCHY)
Mọi thông tin phải được ưu tiên theo thứ tự giảm dần:
1. Source code hiện tại trong thư mục dự án
2. Kết quả test/build/chạy thực tế
3. Database/schema thực tế (`data/database/lol_live_data.db`)
4. `AI/PROJECT_STATE.md`
5. `AI/ARCHITECTURE.md`
6. `AI/DATABASE.md`
7. `AI/TASKS.md`
8. `AI/DECISIONS.md`
9. `AI/CHANGELOG.md`
10. Nội dung hội thoại hiện tại
11. Suy luận của AI (Không bao giờ được biến suy luận thành sự thật)

## 2. QUY TRÌNH BẮT ĐẦU SESSION MỚI
Trước khi code hoặc phân tích:
1. Đọc toàn bộ các file trong thư mục `AI/`.
2. Kiểm tra source code thực tế liên quan.
3. Xuất báo cáo `### PROJECT CONTEXT CHECK` đúng mẫu:
   - Project:
   - Current state:
   - Current task:
   - Completed:
   - In progress:
   - Not started:
   - Relevant files:
   - Important constraints:
   - Known problems:
   - Conflicts:
   - Missing information:
4. Dừng lại và chờ User xác nhận/giao task.

## 3. QUY TRÌNH TIẾP NHẬN & THỰC HIỆN TASK
1. Xác định mục tiêu và phạm vi (Scope).
2. Kiểm tra implementation hiện tại.
3. Xác định file cần thay đổi và side effect tiềm ẩn.
4. Kiểm tra xung đột với architecture và database.
5. Lập implementation plan ngắn gọn trước khi viết code.

## 4. KIỂM SOÁT PHẠM VI (SCOPE CONTROL)
- Chỉ sửa những gì nằm trong phạm vi task được giao.
- KHÔNG tự ý refactor, đổi database schema, đổi tên cột/bảng/class.
- KHÔNG thêm tính năng ngoài yêu cầu.
- Nếu phát hiện vấn đề ngoài phạm vi: Ghi `OUT-OF-SCOPE ISSUE: [mô tả]` và không tự ý sửa.

## 5. PHÂN LOẠI TRẠNG THÁI THÔNG TIN
- `FACT`: Đã xác minh trực tiếp từ code, database hoặc lệnh hệ thống.
- `VERIFIED`: Đã chạy test thực tế và có kết quả pass/fail cụ thể.
- `ASSUMPTION`: Giả định, chưa kiểm chứng.
- `UNVERIFIED`: Có dấu hiệu đúng nhưng chưa test.
- `BLOCKED`: Bị chặn do thiếu dữ liệu hoặc dependency.
- Tuyệt đối KHÔNG nói "đã hoạt động" nếu chưa chạy lệnh kiểm thử thực tế.

## 6. BÁO CÁO SAU IMPLEMENTATION
Sau khi xong task, báo cáo theo mẫu:
- Changed: [danh sách file]
- Behavior: [thay đổi hành vi]
- Tests: [test đã chạy - PASS/FAIL]
- Not tested: [những phần chưa test]
- Known issues: [vấn đề còn lại]
- Out of scope: [vấn đề phát hiện thêm]
- Cập nhật các file trong `AI/` tương ứng (`PROJECT_STATE.md`, `TASKS.md`, `CHANGELOG.md`).

## 7. MỤC TIÊU CUỐI CÙNG
CORRECTNESS > CONSISTENCY > TRACEABILITY > MAINTAINABILITY > SPEED.
