# PROJECT STATE (TRẠNG THÁI DỰ ÁN THỰC TẾ)

*Thời điểm audit thực tế:* 2026-09-20  
*Nguồn dữ liệu:* Khảo sát trực tiếp từ mã nguồn, CSDL SQLite, file hệ thống và lệnh `pip list`.

---

## 1. TỔNG QUAN HIỆN TRẠNG
- **Tên dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Môn học chính:** Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT).
- **Môn học mở rộng:** Lập trình trên thiết bị di động (ThS. Nguyễn Trung Hiếu, PTITHCM).
- **Giai đoạn hiện tại:** Giai đoạn 1 (Thu thập, Làm sạch Dữ liệu & Thiết kế CSDL).
- **Đánh giá tiến độ tổng:** ~15% (Đã xong phần thiết kế schema chuẩn hóa, cào mẫu ban đầu; chưa bắt đầu EDA, ML và Backend).

---

## 2. HIỆN TRẠNG MÃ NGUỒN (SOURCE CODE AUDIT)

| Thư mục / File | Trạng thái thực tế | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| `src/config/` | `VERIFIED - WORKING` | Package cấu hình trung tâm dự án (`settings.py`, `__init__.py`). Nạp `.env`, thẩm định API key, quản lý đường dẫn và metadata. |
| `src/01_data_pipeline/` | `VERIFIED - WORKING` | Chứa script cào chính thức `crawl_riot_matches.py` và tài liệu `README.md`. |
| `.env` / `.env.example` | `VERIFIED - WORKING` | File cấu hình biến môi trường và file mẫu template an toàn. `.gitignore` đã chặn `.env`. |
| `src/02_preprocessing/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` quy định luồng xử lý outlier IQR. Sẵn sàng viết code. |
| `src/03_database_sql/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` đặc tả schema và 5 câu query SQL. Sẵn sàng viết code. |
| `src/04_hypothesis_testing/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` quy định 3 bài kiểm định Z/t/Chi-square. Sẵn sàng viết code. |
| `src/05_visualization/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` đặc tả 5 biểu đồ EDA 300 DPI. Sẵn sàng viết code. |
| `src/06_machine_learning/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` đặc tả mô hình 2 tầng. Sẵn sàng viết code. |
| `src/07_recommender/` | `INITIALIZED` | Đã khởi tạo cấu trúc thư mục kèm tài liệu `README.md` thuật toán gợi ý cấm/chọn. Sẵn sàng viết code. |
| `src/api/` | `NOT CREATED (FACT)` | Chưa tạo thư mục mã nguồn Backend FastAPI. |
| `web/` | `NOT CREATED (FACT)` | Chưa tạo thư mục giao diện Web App. |
| `mobile_app/` | `NOT CREATED (FACT)` | Chưa tạo thư mục ứng dụng Android (theo kế hoạch là Giai đoạn 2). |
| `notebooks/` | `INITIALIZED` | Đã khởi tạo thư mục kèm tài liệu `README.md` phục vụ thử nghiệm `.ipynb`. |
| `reports/figures/` | `INITIALIZED` | Đã khởi tạo thư mục kèm tài liệu `README.md` sẵn sàng nhận ảnh xuất 300 DPI từ bước EDA. |

---

## 3. HIỆN TRẠNG DỮ LIỆU & CƠ SỞ DỮ LIỆU (DATABASE AUDIT)

### CSDL SQLite chính: `data/database/lol_live_data.db`
- **Số bảng hiện có:** 1 bảng duy nhất: `matches_10min` (FACT).
- **Tổng số dòng dữ liệu:** 100 dòng (FACT / VERIFIED).
- **Phân bổ máy chủ:** 
  - `VN2` (Việt Nam): 99 trận.
  - `KR` (Hàn Quốc): 1 trận.
- **Số lượng cột:** Đúng 42 cột đạt chuẩn 1NF (10 cột tướng nguyên tử `blueTop`..`blueSupport`, `redTop`..`redSupport`) và 3NF (không có cột `country`, có cột `server`).
- **Các bảng còn thiếu theo đặc tả:** `tournament_matches`, `tournament_players` (chưa được tạo/nạp từ dữ liệu Oracle's Elixir).

### Các tệp dữ liệu phẳng (CSV):
1. `data/processed/lol_live_ranked_10min.csv`: 100 dòng dữ liệu tương ứng bảng `matches_10min`. Kích thước: ~72 KB (FACT).
2. `data/raw/2026_LoL_esports_match_data_from_OraclesElixir.csv`: 106,488 dòng, 165 cột dữ liệu đấu giải chuyên nghiệp năm 2026. Kích thước: 71.1 MB (FACT).
3. `data/raw/sample_2026_esports_100.csv`: Bản trích mẫu 100 dòng đầu tiên phục vụ phát triển nhanh và chống crash bộ nhớ. Kích thước: ~90 KB (FACT).

---

## 4. HIỆN TRẠNG MÔI TRƯỜNG THỰC THI (ENVIRONMENT AUDIT)
- **Hệ điều hành:** Windows x64 (FACT).
- **Phiên bản Python:** `Python 3.10.11` (VERIFIED).
- **Các package ĐÃ CÀI ĐẶT:**
  - `pandas == 2.3.3`
  - `numpy == 2.2.6`
  - `matplotlib == 3.10.9`
  - `requests == 2.34.2`
  - `python-docx == 1.2.0`
  - `beautifulsoup4 == 4.15.0`
  - `pillow == 12.3.0`
- **Các package CHƯA CÀI ĐẶT (cần cài khi thực hiện các task tương ứng):**
  - `scikit-learn` (Cần cho Machine Learning - Giai đoạn 3)
  - `scipy` (Cần cho Kiểm định thống kê - Giai đoạn 2)
  - `seaborn` (Cần cho EDA Heatmap - Giai đoạn 2)
  - `fastapi`, `uvicorn` (Cần cho Backend API - Giai đoạn 4)
  - `jupyter`, `ipykernel` (Cần khi chạy Notebook `.ipynb`)
- **Kết nối Riot Games API:**
  - Key hiện tại: `RGAPI-c806266a-1220-4211-bf42-3e437f3ff378`
  - Trạng thái: `VERIFIED - HTTP 200` (Đang hoạt động tốt).

---

## 5. CÁC RỦI RO & VẤN ĐỀ ĐANG TỒN TẠI (KNOWN RISKS)
1. **Lệch phân bổ mẫu Solo Rank:** 99 trận VN2 nhưng chỉ mới có 1 trận KR $\rightarrow$ Cần bổ sung thêm trận từ máy chủ Hàn Quốc trong Task 1.1.
2. **Dữ liệu đấu giải 2026 chưa vào CSDL:** File 71.1 MB từ Oracle's Elixir vẫn đang ở dạng CSV thô, chưa được ETL vào bảng SQLite trong `lol_live_data.db` (Task 1.2).
3. **Các thư mục code phân tầng hiện đang trống:** Code mẫu trong `archive/` cần được chuẩn hóa và đưa vào các module chính thức trong `src/` khi thực hiện từng task.
