# BÀI TẬP LỚN GIỮA KỲ: DANH SÁCH TÁC VỤ & CHECKLIST (ATOMIC TASKS)
## CHỦ ĐỀ 2: PHÁT HIỆN VÀ XỬ LÝ ĐIỂM NGOẠI LAI (OUTLIER DETECTION & HANDLING)
**Học phần:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science)  
**Giảng viên hướng dẫn:** TS. Thái Tuyết Hải (PTIT)  
**Phạm vi:** Thư mục độc lập `midterm_assignment/`  

---

### 🚦 Trạng Thái Tác Vụ
- `[x] DONE`: Đã hoàn thành và kiểm chứng định lượng bằng dữ liệu thực tế.
- `[-] IN PROGRESS`: Đang thực hiện.
- `[ ] NOT STARTED`: Chưa bắt đầu.

---

## 📋 CHECKLIST CÁC TÁC VỤ ĐỘC LẬP (MIDTERM ASSIGNMENT TASKS)

### 📌 Nhóm Tác vụ 1: Thu thập & Chuẩn bị Dữ liệu Thực nghiệm
- [x] **Task M1.1: Trích xuất tập dữ liệu thực tế 2,304 ván đấu Đấu Giải Chuyên Nghiệp LMHT 2026**
  - *Mục tiêu:* Trích xuất các trận đấu sạch từ LCK, LPL, LCP, EWC, MSI 2026 phục vụ riêng bài toán ngoại lai mốc 10 phút.
  - *Kết quả:* Đã xuất bản tệp [`data/outlier_experiment_data.csv`](data/outlier_experiment_data.csv) gồm đúng **2,304 ván đấu Đội Xanh độc lập** (không bị trùng lặp đối xứng).
  - *Biến số trọng tâm:* `golddiffat10` (Chênh lệch vàng phút 10), `xpdiffat10` (Chênh lệch kinh nghiệm phút 10).

---

### 📌 Nhóm Tác vụ 2: Thiết kế & Thực thi Thí nghiệm Độc lập
- [x] **Task M2.1: Xây dựng mã nguồn thực nghiệm phát hiện ngoại lai đa phương pháp**
  - *Mục tiêu:* Viết script độc lập [`src/outlier_experiment.py`](src/outlier_experiment.py) cài đặt 3 thuật toán:
    1. Phương pháp Khoảng tứ phân vị IQR ($1.5 \times \text{IQR}$).
    2. Phương pháp Điểm số tiêu chuẩn Z-Score ($|Z| > 3.0$).
    3. Phương pháp Học máy không giám sát Isolation Forest (`contamination = 0.03`).
  - *Kết quả:*
    - IQR phát hiện **23 ván (1.00%)**, ngưỡng `[-2,961.2g, +3,136.8g]`.
    - Z-Score chỉ phát hiện **2 ván (0.09%)**, ngưỡng `[-3,417.0g, +3,613.8g]`.
    - Isolation Forest phát hiện **70 ván (3.04%)**.
    - Chứng minh rõ hiện tượng **Masking Effect (Che khuất)**: Z-Score bỏ sót 21 ván đấu lăn cầu tuyết cực lớn do độ lệch chuẩn bị đội lên 1,171.80 vàng.
  - *Acceptance Criteria:* Xuất file kết quả định lượng [`data/outlier_comparison_summary.csv`](data/outlier_comparison_summary.csv).

- [x] **Task M2.2: Đánh giá định lượng tác động lên các thước đo thống kê**
  - *Mục tiêu:* So sánh 4 kịch bản can thiệp:
    1. Gốc (Retaining): Giữ nguyên toàn bộ $N = 2,304$ ván.
    2. Loại bỏ theo IQR (Trimming): Loại bỏ 23 ván, giảm 3.51% phương sai mẫu.
    3. Loại bỏ theo Z-Score (Trimming): Loại bỏ 2 ván, giảm 0.39% phương sai.
    4. Cắt ngọn phân vị (Winsorization 1%-99%): Giữ nguyên 100% cỡ mẫu, giảm 1.27% phương sai, kiểm soát hoàn hảo giá trị cực trị.
  - *Kết luận đề xuất:* Winsorization là chiến lược tối ưu nhất cho Machine Learning.

---

### 📌 Nhóm Tác vụ 3: Trực quan hóa Dữ liệu Học thuật (Data Visualization)
- [x] **Task M3.1: Xuất bản bộ 4 biểu đồ 300 DPI đạt chuẩn công bố khoa học**
  - *Kết quả lưu tại [`figures/`](figures/):*
    1. [`fig1_outlier_detection_iqr_zscore.png`](figures/fig1_outlier_detection_iqr_zscore.png): Histogram phân phối vàng phút 10 & các đường ngưỡng IQR vs Z-Score.
    2. [`fig2_distribution_before_after.png`](figures/fig2_distribution_before_after.png): Đường cong mật độ xác suất (KDE) trước và sau 4 kịch bản xử lý.
    3. [`fig3_scatter_multivariate_outliers.png`](figures/fig3_scatter_multivariate_outliers.png): Scatter plot tương quan 2D Vàng vs Kinh nghiệm & Bản đồ đồng thuận nhãn giữa các thuật toán.
    4. [`fig4_statistical_impact_comparison.png`](figures/fig4_statistical_impact_comparison.png): Biểu đồ cột đo lường định lượng thay đổi của Mean, Std Dev và Biên độ giá trị.

---

### 📌 Nhóm Tác vụ 4: Biên tập Bài Báo Cáo Học Thuật (Deliverable 1)
- [x] **Task M4.1: Soạn thảo toàn văn Báo cáo Markdown & Xuất bản Word `.docx`**
  - *Cấu trúc:*
    - Trang bìa chuẩn mẫu PTIT (Môn học, Giảng viên TS. Thái Tuyết Hải, Sinh viên).
    - Tóm tắt nội dung (Abstract).
    - Mục 1: Khái niệm & Phân biệt True Outliers vs Erroneous Data.
    - Mục 2: Nguyên nhân phát sinh ngoại lai.
    - Mục 3: Phân tích kỹ thuật (IQR, Z-Score, Isolation Forest).
    - Mục 4: Thực nghiệm 2,304 trận Pro Play 2026.
    - Mục 5: Đánh giá tác động định lượng lên Mean, Std, Skewness.
    - Mục 6: Khuyến nghị chiến lược xử lý (Bản đồ quyết định).
    - Danh mục tài liệu tham khảo (References).
  - *Tệp sản phẩm:*
    - Bản Word hoàn chỉnh: [`report/MIDTERM_REPORT_TOPIC2.docx`](report/MIDTERM_REPORT_TOPIC2.docx) (đầy đủ bảng biểu và chèn 4 hình minh họa).
    - Bản Markdown: [`report/MIDTERM_REPORT_TOPIC2.md`](report/MIDTERM_REPORT_TOPIC2.md).
  - *Độ dài:* Đạt chuẩn 6 – 15 trang theo quy định.

---

### 📌 Nhóm Tác vụ 5: Thiết kế Bộ Slide Thuyết Trình (Deliverable 2)
- [x] **Task M5.1: Thiết kế Slide PowerPoint Widescreen 16:9 `.pptx`**
  - *Quy mô:* Đúng **12 slides** (trong khung 8 – 15 slides của Giảng viên).
  - *Phong cách:* Bảng màu Dark Slate / Cyan / Gold chuyên nghiệp, bố cục thẻ, có bảng số liệu và hình ảnh biểu đồ chèn sẵn.
  - *Tệp sản phẩm:*
    - File PowerPoint: [`slides/MIDTERM_SLIDES_TOPIC2.pptx`](slides/MIDTERM_SLIDES_TOPIC2.pptx).
    - Kịch bản thuyết trình: [`slides/MIDTERM_SLIDES_TOPIC2.md`](slides/MIDTERM_SLIDES_TOPIC2.md).

---

### 📌 Nhóm Tác vụ 6: Tự động hóa & Đặc tả Yêu cầu (Automation & Docs)
- [x] **Task M6.1: Viết script build deliverables tự động một chạm**
  - Tệp [`src/build_deliverables.py`](src/build_deliverables.py) tự động biên tập và xuất lại đồng thời `.docx` và `.pptx`.
- [x] **Task M6.2: Tổng hợp toàn văn Đề bài & Ma trận đối chiếu (Compliance Matrix)**
  - Tệp [`REQUIREMENTS.md`](REQUIREMENTS.md) lưu nguyên văn đề bài tiếng Anh, diễn giải tiếng Việt và bảng đối soát 11 tiêu chí đánh giá.
- [x] **Task M6.3: Hướng dẫn tổng thể tại README**
  - Tệp [`README.md`](README.md) hướng dẫn cách chạy lại thí nghiệm và nộp bài.
