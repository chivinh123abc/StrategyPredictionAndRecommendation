# AI WORKING RULES & PROJECT PROTOCOL

Tài liệu này là quy chuẩn bắt buộc đối với tất cả các AI session khi làm việc trên dự án.

**Quy định kiến thức bắt buộc:** đọc và áp dụng [KNOWLEDGE_RULES.md](KNOWLEDGE_RULES.md). Khi thêm/sửa/bỏ phương pháp, chức năng, dữ liệu đánh giá hoặc đầu ra, phải cập nhật [sổ kiến thức báo cáo](../docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md) trong cùng đợt thay đổi: chương/nguồn, nơi dùng, công dụng, output, trạng thái và minh chứng. Đây là một phần điều kiện hoàn thành, không phải ghi chú tùy chọn.

---

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
11. Suy luận của AI (**Tuyệt đối không bao giờ được biến suy luận chủ quan thành sự thật hoặc gán cứng vào code**)

---

## 2. CÁC NGUYÊN TẮC BẮT BUỘC TỪ USER (CORE MANDATORY REQUIREMENTS)

### Nguyên tắc 2.1: CẤM TUYỆT ĐỐI TỰ SUY LUẬN CHỦ QUAN & CẤM HARDCODE (100% ALGORITHMIC & DATA-DRIVEN)
- **Không tự suy diễn cảm tính:** AI tuyệt đối không được dùng cảm nhận cá nhân hay suy luận ngoài dữ liệu để bịa đặt thông số, tỷ lệ thắng, kèo khắc chế hay tier tướng.
- **Cấm Hardcode tình huống lẻ (No Case-Specific Hardcoding):** Khi sửa lỗi hoặc nâng cấp tính năng, **TUYỆT ĐỐI CẤM** viết câu lệnh `if/else` gán cứng cho riêng một vài trường hợp lẻ. Mọi bản sửa lỗi bắt buộc phải là **thuật toán tổng quát** áp dụng đồng nhất cho toàn bộ dữ liệu.
- **100% Vận hành bằng Thuật toán & Dữ liệu thực tế:** Mọi con số, gợi ý Cấm/Chọn, phân hạng Tier hay dự đoán thắng thua đều phải được tính toán trực tiếp từ thuật toán và mô hình học máy truy vấn trên CSDL SQLite `data/database/lol_live_data.db`.

### Nguyên tắc 2.2: BẮT BUỘC HUẤN LUYỆN MÔ HÌNH BẰNG GPU (MANDATORY GPU-FIRST TRAINING)
- **Mọi quá trình huấn luyện mô hình học máy (`--train` / Model Training) BẮT BUỘC phải chạy bằng GPU (NVIDIA CUDA)** để tối đa hóa tốc độ thực thi trên phần cứng của máy trạm (**NVIDIA GeForce RTX 4070 Laptop GPU**):
  - Với **XGBoost (`XGBClassifier` / `XGBRegressor`)**: Luôn cấu hình `device='cuda'`, `tree_method='hist'`.
  - Với **PyTorch / Deep Learning / Neural Networks** (nếu mở rộng): Luôn ưu tiên `.to('cuda')` khi `torch.cuda.is_available()`.
  - Với các thuật toán song song và truy vấn dữ liệu đi kèm: Khai thác tối đa đa luồng (`n_jobs=-1`) và Composite Indexes của SQLite (`idx_tp_game_pos_side`, `idx_tp_game_side_pos`), kèm cơ chế tự động kiểm tra GPU (`_check_xgb_gpu_support()`).

### Nguyên tắc 2.3: ĐỒNG BỘ TÀI LIỆU `AI/` & TIẾN ĐỘ NGAY SAU MỖI THAO TÁC (MANDATORY REAL-TIME PROGRESS SYNC)
- **Mỗi khi thực hiện bất kỳ thay đổi nào** (sửa code, cập nhật thuật toán, huấn luyện lại model `.pkl`, nạp dữ liệu mới, thêm cờ CLI, sửa bug), AI **BẮT BUỘC** phải cập nhật đồng bộ ngay lập tức vào các tệp quản trị trong thư mục `AI/`:
  1. `AI/PROJECT_STATE.md`: Cập nhật trạng thái thực tế của mã nguồn, CSDL, models và backlog.
  2. `AI/TASKS.md`: Cập nhật trạng thái checklist công việc và tổng kết kỹ thuật.
  3. `AI/CHANGELOG.md`: Ghi nhật ký thay đổi chi tiết kèm ngày tháng, công thức/hành vi thay đổi và kết quả kiểm chứng.
  4. `AI/DECISIONS.md` / `AI/ARCHITECTURE.md` / `AI/DATABASE.md`: Cập nhật ngay nếu có quyết định kiến trúc mới (ADR), thay đổi cấu trúc module hoặc thêm Index/Bảng CSDL.
- Không bao giờ kết thúc một task lớn mà để các file trong `AI/` bị lệch hoặc lỗi thời so với source code thực tế.

---

## 3. QUY TRÌNH BẮT ĐẦU SESSION MỚI
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
4. Dừng lại và chờ User xác nhận/giao task (trừ khi User đã giao task trực tiếp ngay trong câu lệnh mở đầu).

---

## 4. QUY TRÌNH TIẾP NHẬN & THỰC HIỆN TASK
1. Xác định mục tiêu và phạm vi (Scope).
2. Kiểm tra implementation hiện tại.
3. Xác định file cần thay đổi và side effect tiềm ẩn.
4. Kiểm tra xung đột với architecture và database.
5. Lập implementation plan ngắn gọn trước khi viết code.
6. Thực thi bằng thuật toán tổng quát (Zero-Hardcode), huấn luyện/kiểm thử thực tế trên `.venv` và cập nhật đồng bộ toàn bộ thư mục `AI/`.

---

## 5. KIỂM SOÁT PHẠM VI (SCOPE CONTROL)
- Chỉ sửa những gì nằm trong phạm vi task được giao.
- KHÔNG tự ý đổi database schema hoặc đổi tên cột/bảng/class đang ổn định trừ khi có yêu cầu.
- Nếu phát hiện vấn đề ngoài phạm vi: Ghi `OUT-OF-SCOPE ISSUE: [mô tả]` và báo cáo rõ ràng.

---

## 6. PHÂN LOẠI TRẠNG THÁI THÔNG TIN
- `FACT`: Đã xác minh trực tiếp từ code, database hoặc lệnh hệ thống.
- `VERIFIED`: Đã chạy test thực tế và có kết quả pass/fail cụ thể.
- `ASSUMPTION`: Giả định, chưa kiểm chứng.
- `UNVERIFIED`: Có dấu hiệu đúng nhưng chưa test.
- `BLOCKED`: Bị chặn do thiếu dữ liệu hoặc dependency.
- Tuyệt đối KHÔNG nói "đã hoạt động" nếu chưa chạy lệnh kiểm thử thực tế.

---

## 7. BÁO CÁO SAU IMPLEMENTATION
Sau khi xong task, báo cáo theo mẫu:
- Changed: [danh sách file]
- Behavior: [thay đổi hành vi / thuật toán tổng quát]
- Tests: [test đã chạy - PASS/FAIL kèm số liệu thực tế]
- AI Docs Updated: [danh sách các file trong `AI/` và `docs/` đã đồng bộ]
- Known issues / Out of scope: [nếu có]

---

## 8. QUY TẮC QUẢN LÝ GIT & GITHUB (GIT CONTROL PROTOCOL - STRICT)
- **TUYỆT ĐỐI KHÔNG tự động `git commit` hoặc `git push`**: Mọi thao tác commit và push hoàn toàn do User tự quyết định và quản lý.
- Mọi thay đổi mã nguồn, tài liệu chỉ được chỉnh sửa trực tiếp trên file (Working Directory).
- Chỉ thực hiện `git commit` hoặc `git push` khi User chỉ định đích danh câu lệnh (ví dụ: "commit cho tôi", "push lên git").

---

## 9. MỤC TIÊU CUỐI CÙNG
**ALGORITHMIC GENERALITY > STATISTICAL RIGOR > CORRECTNESS > CONSISTENCY > TRACEABILITY > SPEED.**
