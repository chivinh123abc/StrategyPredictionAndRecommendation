# SYSTEM ARCHITECTURE (KIẾN TRÚC HỆ THỐNG)

Dự án áp dụng mô hình **Kiến trúc phân tầng hướng dịch vụ (Decoupled / API-First Architecture)** nhằm phục vụ đồng thời cho 2 môn học mà không bị phụ thuộc chéo.

---

## 1. SƠ ĐỒ TỔNG THỂ HỆ THỐNG

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TẦNG 1: DỮ LIỆU & TRÍ TUỆ NHÂN TẠO              │
│       (Data Engineering, Machine Learning & Ban/Pick Recommender)       │
│                                                                        │
│   [Dữ liệu Solo Rank (Riot API)]       [Dữ liệu Esports (Oracle's)]   │
│                 │                                    │                 │
│                 └──────────────┬─────────────────────┘                 │
│                                ▼                                       │
│                [Làm sạch & Chuẩn hóa 1NF / 3NF]                        │
│                                ▼                                       │
│                  [CSDL Quan hệ SQLite (.db)]                           │
│                                │                                       │
│                 ┌──────────────┴──────────────┐                        │
│                 ▼                             ▼                        │
│     [Kiểm định Thống kê & EDA]     [Huấn luyện AI (XGBoost/RF)]        │
│        (Chi-Square, T-Test)          (Acc > 75%, Xuất model .pkl)      │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         TẦNG 2: CỔNG GIAO TIẾP DỊCH VỤ                 │
│                     (Backend REST API - FastAPI & Uvicorn)             │
│                                                                        │
│   • POST /api/v1/predict      : Dự đoán tỉ lệ thắng (% Winrate)        │
│   • GET  /api/v1/champions    : Danh sách 173 tướng + Stats            │
│   • POST /api/v1/recommend    : Gợi ý cấm/chọn (Ban/Pick AI)           │
│   • GET  /api/v1/analytics    : Số liệu thống kê Meta giải đấu         │
│   • Tự động sinh giao diện kiểm thử Swagger UI (/docs)                 │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             ▼                                       ▼
┌───────────────────────────────┐     ┌──────────────────────────────────┐
│   TẦNG 3A: CLIENT BÁO CÁO     │     │     TẦNG 3B: CLIENT DI ĐỘNG      │
│   MÔN KHOA HỌC DỮ LIỆU        │     │     MÔN LẬP TRÌNH ANDROID        │
│   (Web Dashboard / Streamlit) │     │     (Android Native Java/Kotlin) │
│                               │     │                                  │
│ • Giao diện Web tương tác     │     │ • RecyclerView 173 tướng         │
│ • Trực quan hóa biểu đồ       │     │ • SQLite/SharedPreferences lưu   │
│ • Báo cáo Cô Thái Tuyết Hải   │     │ • Retrofit 2 gọi REST API        │
│ • Nộp đồ án Giai đoạn 1       │     │ • Nộp đồ án Thầy Nguyễn T. Hiếu  │
└───────────────────────────────┘     └──────────────────────────────────┘
```

---

## 2. PHÂN TRÁCH NHIỆM TỪNG MODULE (MODULE BOUNDARIES)

### `src/01_data_pipeline/`
- Chịu trách nhiệm: 
  - Gọi Riot API (Live Rank VN2, KR), xử lý rate limit, retry logic, trích xuất chỉ số phút thứ 10.
  - Tự động kiểm tra và đồng bộ hóa dữ liệu từ Google Drive (Cloud Data Auto-Sync via modifiedTime/hash).
- Đầu ra: Bảng `matches_10min` trong SQLite, file CSV `lol_live_ranked_10min.csv` và dữ liệu giải đấu mới nhất trong `data/raw/`.

### `src/02_preprocessing/`
- Chịu trách nhiệm: Đọc dữ liệu thô (cả Rank và Esports), lọc bỏ trận Remake/AFK, phát hiện và xử lý giá trị ngoại lai (IQR & Z-score).
- Đầu ra: Dữ liệu sạch đưa vào CSDL và các tập train/test.

### `src/03_database_sql/`
- Chịu trách nhiệm: Quản lý cấu trúc schema CSDL SQLite `lol_live_data.db`, thực thi 5 câu truy vấn SQL phân tích nâng cao (Chương 5, 5x).
- Đầu ra: Các bảng quan hệ và view dữ liệu phân tích.

### `src/04_hypothesis_testing/`
- Chịu trách nhiệm: Thực hiện các phép kiểm định thống kê suy diễn: $Z$-test (Lợi thế Phe Xanh), Two-sample $t$-test (Lăn Cầu Tuyết Đấu giải vs Rank), Chi-Square (Mục tiêu lớn Rồng vs Sâu Hư Không).

### `src/05_visualization/`
- Chịu trách nhiệm: Sinh bộ 5 biểu đồ phân tích EDA độ phân giải cao 300 DPI lưu vào `reports/figures/`.

### `src/06_machine_learning/`
- Chịu trách nhiệm: Huấn luyện mô hình 2 giai đoạn:
  - Tầng 1: Draft Prediction (Phút 0 - cấm chọn).
  - Tầng 2: Snowball Prediction (Phút 10 - kinh tế/mục tiêu).
- Đánh giá: ROC-AUC, Confusion Matrix, Feature Importance.
- Đầu ra: File mô hình `draft_model.pkl`, `snowball_model.pkl`.

### `src/07_recommender/`
- Chịu trách nhiệm: Thuật toán gợi ý tướng khắc chế (Counter Pick) và tương thích đồng đội (Synergy Pick).
- Đầu ra: File `recommender.pkl`.

### `src/api/` (Planned)
- Chịu trách nhiệm: Đóng gói các hàm của tầng ML và Database thành các endpoint RESTful HTTP bằng FastAPI.

### `web/` (Planned - Giai đoạn 1)
- Chịu trách nhiệm: Giao diện Web tương tác trình diễn trực tiếp cho giảng viên môn Khoa học Dữ liệu.

### `mobile_app/` (Planned - Giai đoạn 2)
- Chịu trách nhiệm: Ứng dụng Android độc lập gọi REST API từ máy tính, phục vụ nộp bài môn Lập trình Di động.
