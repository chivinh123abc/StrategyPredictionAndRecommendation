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

### ADR-005: Tách rời Backend REST API (FastAPI) để phục vụ cả Web và Mobile
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Dự án kết hợp 2 môn học: Khoa học Dữ liệu (cần Web báo cáo) và Lập trình Di động (cần App Android).
- **Quyết định:** Xây dựng một cổng **FastAPI** trung gian độc lập.
- **Lý do:** Mô hình AI chỉ cần huấn luyện và đóng gói một lần duy nhất. Web App và Mobile App chỉ đóng vai trò là Client gọi API nhận kết quả JSON.

---

### ADR-006: Giữ nguyên Python 3.10.11 làm môi trường chuẩn
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Hệ thống đang cài Python 3.10.11. Cân nhắc nâng cấp lên Python 3.12/3.13.
- **Quyết định:** Giữ nguyên **Python 3.10.11**.
- **Lý do:** Python 3.10 là phiên bản ổn định nhất (sweet spot) với 100% pre-built wheel trên Windows cho `scikit-learn`, `xgboost`, `pandas`, `numpy`, tránh lỗi xung đột build tools C++.

---

### ADR-007: Ưu tiên hoàn thành Web App trước, Mobile App sau
- **Ngày quyết định:** 2026-09-20
- **Bối cảnh:** Môn Lập trình Di động chưa học xong các chương nâng cao (Networking, SQLite).
- **Quyết định:** Tập trung toàn bộ nguồn lực hoàn thành Web App phục vụ môn Khoa học Dữ liệu (Giai đoạn 1). Mobile App sẽ triển khai ở Giai đoạn 2 khi sinh viên đã học đủ bài giảng.
