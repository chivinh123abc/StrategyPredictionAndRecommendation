# HỆ THỐNG TRỢ LÝ PHÂN TÍCH CẤM/CHỌN (BAN/PICK AI), DỰ ĐOÁN THẮNG THUA SỚM 2 GIAI ĐOẠN & ĐỐI CHIẾU CHIẾN THUẬT ĐẤU GIẢI (PRO PLAY) VS ĐẤU XẾP HẠNG (SOLO QUEUE) TRONG ESPORTS LIÊN MINH HUYỀN THOẠI

**Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science) - Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
**Nhóm sinh viên thực hiện:** Nhóm 3 thành viên  

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT REPOSITORY LAYOUT)

```text
Project/
├── docs/                               # Tài liệu học tập, giáo trình & kế hoạch đồ án
│   ├── course_slides/                  # Slide bài giảng từ Chương 0 đến Chương 6
│   ├── Dac_Ta_De_Tai_Va_Ke_Hoach_Data_Science_PTIT.docx   # Bản đặc tả Word chính thức
│   ├── DANH_MUC_API_VA_DATASET.md                         # Danh mục API & Dataset tham chiếu
│   └── KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md                # Checklist phân công 3 người
│
├── data/                               # Quản lý dữ liệu phân tầng chuẩn mực
│   ├── raw/                            # Dữ liệu thô ban đầu (File 2026 Pro Play 71MB)
│   ├── processed/                      # Dữ liệu sạch đã qua tiền xử lý, lọc outlier, chuẩn hóa
│   │   └── lol_live_ranked_10min.csv   # Dữ liệu cào Live Rank VN & KR mốc 10 phút
│   └── database/                       # Cơ sở dữ liệu quan hệ SQLite
│       └── lol_live_data.db            # Database chính thức chứa các bảng dữ liệu
│
├── src/                                # Toàn bộ mã nguồn cốt lõi (Source code) chia theo module
│   ├── 01_data_pipeline/               # Module cào & nạp dữ liệu (Riot API & Oracle's Elixir)
│   │   └── crawl_riot_matches.py       # Crawler cào Live Rank VN & KR
│   ├── 02_preprocessing/               # Module làm sạch, lọc outlier, remakes (Chương 2)
│   ├── 03_database_sql/                # Module CSDL & Truy vấn SQL/Pandas (Chương 5, 5x)
│   ├── 04_hypothesis_testing/          # Module thống kê suy diễn & kiểm định A/B (Chương 1)
│   ├── 05_visualization/               # Module trực quan hóa EDA đa chiều (Chương 3)
│   ├── 06_machine_learning/            # Module ML 2 giai đoạn: Draft & Snowball (Chương 4)
│   ├── 07_recommender/                 # Module Trợ lý Cấm/Chọn Ban/Pick AI (Chương 6)
│   └── api/                            # Backend REST API (FastAPI) kết nối Model AI & CSDL
│
├── web/                                # GIAO DIỆN WEB APP TƯƠNG TÁC (GIAI ĐOẠN 1)
│   ├── index.html                      # Trang chủ Dashboard phân tích & dự đoán trận đấu
│   ├── css/                            # Giao diện phong cách Hextech / Dark mode cao cấp
│   └── js/                             # Logic tương tác, gọi API /predict & vẽ biểu đồ live
│
├── mobile_app/                         # ỨNG DỤNG ANDROID NATIVE (GIAI ĐOẠN 2 - CẮM SAU)
│   └── LoLHextechApp/                  # Dự án Android Studio (kết nối chung Backend FastAPI)
│
├── notebooks/                          # Jupyter Notebooks tương tác (dùng để báo cáo, demo)
├── reports/                            # Báo cáo, slide thuyết trình & biểu đồ xuất bản
│   ├── figures/                        # Hình ảnh biểu đồ PNG độ phân giải cao 300 DPI
│   ├── slides/                         # Slide PowerPoint bảo vệ đồ án
│   └── final_report/                   # Báo cáo tổng kết đồ án Word/PDF
│
├── requirements.txt                    # Danh sách thư viện Python cần cài đặt
├── .env.example                        # File mẫu cấu hình biến môi trường
└── .gitignore                          # Cấu hình bỏ qua file nặng & bí mật khi commit Git
```

---

## 🚀 HƯỚNG DẪN BẮT ĐẦU NHANH (QUICK START)

### 1. Cài đặt môi trường
Khuyên dùng Python 3.10 trở lên:
```bash
pip install -r requirements.txt
```

### 2. Chạy Pipeline Cào Dữ Liệu Sống (Riot API)
Mã nguồn hỗ trợ cào song song máy chủ Việt Nam (VN2) và Hàn Quốc (KR):
```bash
python src/01_data_pipeline/crawl_riot_matches.py
```
Dữ liệu sẽ tự động được ghi vào:
* CSDL SQLite: `data/database/lol_live_data.db`
* File CSV: `data/processed/lol_live_ranked_10min.csv`

### 3. Chạy Backend REST API (FastAPI) & Khởi chạy Web App
Khởi động máy chủ API để phục vụ Web App và kiểm thử Swagger UI:
```bash
uvicorn src.api.main:app --reload --port 8000
```
* **Swagger UI kiểm thử API:** Truy cập `http://localhost:8000/docs`
* **Giao diện Web App tương tác:** Mở file `web/index.html` hoặc chạy dev server tại cổng 3000.

---

## 🧠 CHIẾN LƯỢC KỸ THUẬT & QUẢN TRỊ DỮ LIỆU CỐT LÕI

1. **Chuẩn hóa CSDL đạt chuẩn 1NF & 3NF (Data Normalization):**
   * **Chuẩn 1NF:** Triệt tiêu hoàn toàn các cột gộp chuỗi (`blueChampions`, `redChampions`). Toàn bộ 10 tướng được lưu trữ tại 10 cột nguyên tử tách bạch theo vị trí thi đấu: `blueTop` $\rightarrow$ `blueSupport` và `redTop` $\rightarrow$ `redSupport`.
   * **Chuẩn 3NF (Khử phụ thuộc hàm):** Loại bỏ cột `country` vì phụ thuộc trực tiếp vào `server` (`VN2` $\rightarrow$ `Vietnam`, `KR` $\rightarrow$ `Korea`). Giữ lại duy nhất mã định danh `server` để triệt tiêu dư thừa dữ liệu (khi trực quan hóa EDA chỉ cần ánh xạ nhãn qua dictionary).
2. **Chiến lược dữ liệu Đa máy chủ (Multi-server):**
   * Hỗ trợ cào dữ liệu rank cao song song từ máy chủ Việt Nam (`vn2`) và Hàn Quốc (`kr`).
   * Máy chủ Hàn Quốc (`kr`) đóng vai trò đại diện cho đấu trường Solo Queue đỉnh cao của khu vực Đông Á (nơi các tuyển thủ Trung Quốc LPL và Hàn Quốc LCK cùng thi đấu xếp hạng).
   * Dữ liệu giải đấu chuyên nghiệp Trung Quốc (LPL) được phân tích độc lập thông qua bộ dữ liệu chuẩn 8,740 trận đấu từ **Oracle's Elixir** (`2026_LoL_esports_match_data_from_OraclesElixir.csv`).
3. **Cơ chế xử lý Concept Drift & Học liên tục (Continual Learning):**
   * Đối phó với việc Riot cập nhật bản vá 2 tuần/lần làm thay đổi meta: Áp dụng kỹ thuật kết hợp giữa **Sliding Window** (lọc theo `gameVersion`) và **Exponential Time-Decay Sample Weighting** ($w_i = e^{-\lambda \Delta t}$) khi huấn luyện mô hình Machine Learning.
   * Giúp mô hình luôn ưu tiên cập nhật sức mạnh tướng của meta mới nhất mà không làm giảm kích thước mẫu (sample size).

---

## 👥 PHÂN CÔNG VAI TRÒ NHÓM 3 NGƯỜI
* **Thành viên 1 (Data Engineer, Backend API & Web/App Lead):** Phụ trách `src/01_data_pipeline`, `src/02_preprocessing`, `src/03_database_sql` (Chương 2, 5, 5x), đóng gói Backend REST API (FastAPI) và phát triển giao diện Web App tương tác (sau này tích hợp thêm Mobile App).
* **Thành viên 2 (Data Analyst & Statistician):** Phụ trách `src/04_hypothesis_testing`, `src/05_visualization` (Chương 1, 3 Thống kê A/B & Biểu đồ EDA).
* **Thành viên 3 (AI / Machine Learning Lead):** Phụ trách `src/06_machine_learning`, `src/07_recommender` (Chương 4, 6 Mô hình ML 2 giai đoạn & Ban/Pick AI).

Chi tiết toàn bộ lộ trình 5 giai đoạn xem tại: [docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md](file:///d:/Chivinh/2026_MonHoc/Nh%E1%BA%ADp%20m%C3%B4n%20khoa%20h%E1%BB%8Dc%20d%E1%BB%AF%20li%E1%BB%87u/Project/docs/KE_HOACH_THUC_HIEN_DO_AN_3_NGUOI.md)  
Checklist liên môn kết hợp Môn Lập trình Di động xem tại: [docs/KE_HOACH_LIEN_MON_DATA_SCIENCE_VA_ANDROID.md](file:///d:/Chivinh/2026_MonHoc/Nh%E1%BA%ADp%20m%C3%B4n%20khoa%20h%E1%BB%8Dc%20d%E1%BB%AF%20li%E1%BB%87u/Project/docs/KE_HOACH_LIEN_MON_DATA_SCIENCE_VA_ANDROID.md)
