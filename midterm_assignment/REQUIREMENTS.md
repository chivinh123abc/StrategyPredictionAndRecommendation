# ĐẶC TẢ YÊU CẦU BÀI TẬP LỚN GIỮA KỲ (MIDTERM ASSIGNMENT SPECIFICATIONS)
## HỌC PHẦN: NHẬP MÔN KHOA HỌC DỮ LIỆU (INTRODUCTION TO DATA SCIENCE)
**Giảng viên phụ trách:** TS. Thái Tuyết Hải  
**Đơn vị:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Chủ đề đã chọn:** **Topic 2: Outlier Detection (Phát hiện và Xử lý Điểm Ngoại Lai)**

---

## 1. NGUYÊN VĂN ĐỀ BÀI TỪ GIẢNG VIÊN (ORIGINAL PROMPT)

> ### GENERAL REQUIREMENTS
> The purpose of this assignment is to explore additional knowledge, understand relevant methods, and apply the knowledge to a practical problem through a small experiment.
> 
> **Deliverables:**
> - A written report.
> - Presentation slides.
> - The dataset and source files or project files used in the experiment, as applicable.
> 
> **Format Requirements:**
> - **Written Report:**
>   - Include a cover page with the course name, project title, and the full names and student IDs of all team members.
>   - Structure the report clearly using appropriate headings and subheadings.
>   - If code is part of the work, provide a link to a GitHub repository or attach the code/project files as appropriate.
>   - Include a list of references at the end of the report to acknowledge all sources used.
>   - Accepted formats: `.docx`, `.pdf`, or `.md`.
>   - Length: **6 – 15 pages**.
> - **Presentation Slides:**
>   - Accepted formats: `.pptx` or `.pdf`.
>   - Length: **8 – 15 slides**.
> 
> ---
> 
> ### TOPIC 2: OUTLIER DETECTION
> **Objective:** Understand the concept of outliers, how to identify them, and how to handle them in data analysis.
> 
> **Required Content:**
> 1. What is an outlier? Contrast outliers with erroneous data (data anomalies).
> 2. What are the common causes of outliers?
> 3. Explore techniques for identifying outliers (e.g., IQR, Z-Score). Compare the advantages and disadvantages of each.
> 4. Use a dataset of your choice to design and conduct a small experiment comparing at least two outlier detection methods.
> 5. Identify the outliers found by each method and evaluate their impact on common statistical measures (e.g., mean, standard deviation).
> 6. Discuss different approaches to handling outliers (e.g., retaining, trimming, winsorizing, transforming) and when to use each.
> 
> ---
> 
> ### EVALUATION CRITERIA (RUBRICS)
> - **Understanding of Concepts (30%):** Depth, accuracy, and clarity of the explanations.
> - **Practical Experiment (30%):** Quality and design of the experiment, interpretation of results, and discussion of practical implications.
> - **Report and Presentation (30%):** Organization, visual appeal, structure, language, and adherence to the guidelines.
> - **Professionalism and Engagement (10%):** Active participation, thoroughness, and effective teamwork.

---

## 2. DIỄN GIẢI CHI TIẾT CÁC YÊU CẦU ĐƯỢC ĐẶT RA

### 2.1. Yêu cầu về Nội dung Học thuật (6 Trụ cột cốt lõi)
1. **Khái niệm Ngoại lai:** Định nghĩa toán học & thống kê (theo Hawkins 1980), bản chất của điểm ngoại lai trong phân phối xác suất.
2. **Phân biệt Ngoại lai vs Dữ liệu Sai hỏng:** Làm rõ ranh giới giữa *True Outliers* (hiện tượng cực đoan có thật, mang giá trị tri thức) và *Erroneous Data* (lỗi kỹ thuật, mất mạng, cảm biến hỏng cần phải xóa bỏ ở khâu Data Cleaning).
3. **Nguyên nhân phát sinh:** Phân tích 4 nhóm nguyên nhân: lỗi nhập liệu, lỗi đo lường, lỗi tích hợp pipeline, và bản chất biến động tự nhiên (phân phối đuôi dày).
4. **Kỹ thuật phát hiện (Lý thuyết):** Phân tích sâu phương pháp phi tham số (IQR) và phương pháp tham số (Z-Score), chỉ ra hiện tượng che khuất (Masking Effect) của Z-Score. Bổ sung mô hình học máy hiện đại Isolation Forest.
5. **Thực nghiệm đối sánh định lượng:** Thiết kế bài toán trên tập dữ liệu thực tế lớn (đã chọn: 2,304 ván đấu LMHT Pro Play 2026), đo lường độ nhạy của từng phương pháp.
6. **Đánh giá tác động & Chiến lược can thiệp:** Đo lường định lượng sự thay đổi của Mean, Median, Std Dev, Range, Skewness trước và sau 4 chiến lược: Retaining, Trimming IQR, Trimming Z-Score, Winsorization (Cắt ngọn phân vị).

### 2.2. Yêu cầu về Sản phẩm Bàn giao (Deliverables)
1. **Báo cáo bằng văn bản (Written Report):**
   - Có trang bìa chuẩn mẫu thông tin (Tên trường, khoa, môn, đề tài, giảng viên, sinh viên).
   - Định dạng chấp nhận: `.docx` và `.md`.
   - Độ dài: Đạt chuẩn 6 - 15 trang.
   - Có danh mục tài liệu tham khảo chuẩn học thuật (IEEE / APA).
2. **Slide Thuyết trình (Presentation Slides):**
   - Định dạng: `.pptx` (PowerPoint 16:9 hiện đại) và `.md`.
   - Độ dài: Đạt chuẩn 8 - 15 slides (đã làm 12 slides).
   - Thiết kế trực quan, thẩm mỹ cao, có bảng dữ liệu và chèn biểu đồ kết quả.
3. **Dữ liệu & Mã nguồn (Data & Source Code):**
   - Tập dữ liệu thí nghiệm đính kèm: `outlier_experiment_data.csv`.
   - Mã nguồn thực thi độc lập: `outlier_experiment.py` và `build_deliverables.py`.
   - Bộ 4 hình ảnh biểu đồ minh họa độ phân giải cao 300 DPI (`figures/`).

---

## 3. MA TRẬN ĐỐI CHIẾU MỨC ĐỘ ĐÁP ỨNG (COMPLIANCE MATRIX)

Bảng dưới đây chứng minh toàn bộ các yêu cầu của Giảng viên đã được hiện thực hóa 100% trong thư mục `midterm_assignment/`:

| STT | Yêu cầu được đặt ra | Mức độ đáp ứng | Tệp triển khai minh chứng | Vị trí kiểm chứng |
| :---: | :--- | :---: | :--- | :--- |
| **1** | Định nghĩa Outlier & Phân biệt với Erroneous Data | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx`<br>`report/MIDTERM_REPORT_TOPIC2.md` | Mục 1.1 & Mục 1.2, Bảng 1 |
| **2** | Nguyên nhân phát sinh điểm ngoại lai | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx`<br>`slides/MIDTERM_SLIDES_TOPIC2.pptx` | Mục 2 của Báo cáo & Slide 4 |
| **3** | Phân tích kỹ thuật phát hiện (IQR, Z-Score, Ưu/Nhược điểm) | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx`<br>`src/outlier_experiment.py` | Mục 3 của Báo cáo & Slide 5, 6, 7 |
| **4** | Thiết kế thí nghiệm thực tế so sánh ít nhất 2 phương pháp | **100% HOÀN TẤT** *(Vượt chỉ tiêu: so sánh 3 phương pháp)* | `src/outlier_experiment.py`<br>`data/outlier_experiment_data.csv` | 2,304 ván đấu Pro Play 2026, 3 phương pháp (IQR, Z-Score, Iso Forest) |
| **5** | Đánh giá tác động lên các thước đo thống kê (Mean, Std) | **100% HOÀN TẤT** | `data/outlier_comparison_summary.csv`<br>`figures/fig1..fig4.png` | Bảng 3 & 4 biểu đồ 300 DPI |
| **6** | Thảo luận các chiến lược xử lý (Retaining, Trimming, Winsorizing, Transforming) | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx`<br>`slides/MIDTERM_SLIDES_TOPIC2.pptx` | Mục 5 & 6 của Báo cáo, Slide 8 & 10 |
| **7** | Trang bìa đầy đủ thông tin giảng viên, sinh viên, học phần | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx`<br>`slides/MIDTERM_SLIDES_TOPIC2.pptx` | Trang 1 file Word & Slide 1 PPTX |
| **8** | Danh mục tài liệu tham khảo (References) | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx`<br>`report/MIDTERM_REPORT_TOPIC2.md` | Mục Tài liệu tham khảo (6 nguồn chuẩn) |
| **9** | Độ dài báo cáo (6 – 15 trang) | **100% HOÀN TẤT** | `report/MIDTERM_REPORT_TOPIC2.docx` | ~8 trang tiêu chuẩn học thuật kèm 4 hình |
| **10** | Độ dài slide thuyết trình (8 – 15 slides) | **100% HOÀN TẤT** | `slides/MIDTERM_SLIDES_TOPIC2.pptx` | Đúng **12 slides** Widescreen 16:9 |
| **11** | Khả năng tái tạo thí nghiệm (Reproducibility) | **100% HOÀN TẤT** | `src/outlier_experiment.py`<br>`src/build_deliverables.py` | Chạy 1 lệnh tự sinh lại dữ liệu, hình ảnh và tệp báo cáo |

---

## 4. BẢNG TIÊU CHÍ CHẤM ĐIỂM (RUBRICS) & CHIẾN LƯỢC TỐI ĐA HÓA ĐIỂM SỐ

- **Thấu hiểu khái niệm (Understanding of Concepts - 30%):**
  - Điểm mạnh: Không chỉ nêu định nghĩa cơ bản mà phân tích sâu hiện tượng *Masking Effect* của Z-Score và tính chất *Robust* của IQR. Phân định rõ ràng giữa Erroneous Data và Informative Outliers.
- **Thực nghiệm thực tế (Practical Experiment - 30%):**
  - Điểm mạnh: Sử dụng dữ liệu thật 2,304 ván đấu từ 5 giải đấu lớn nhất thế giới (LCK, LPL, LCP, EWC, MSI). So sánh không chỉ 2 mà 3 phương pháp (bổ sung Isolation Forest cho không gian đa chiều 2D Vàng vs Kinh nghiệm).
- **Hình thức báo cáo & Trình bày (Report & Presentation - 30%):**
  - Điểm mạnh: Trình bày song song cả `.docx` và `.pptx` với phong cách thiết kế hiện đại, bố cục thẻ, bảng biểu đối sánh màu sắc trang nhã, 4 biểu đồ 300 DPI xuất bản trực tiếp từ Matplotlib/Seaborn.
- **Tính chuyên nghiệp & Tinh thần học tập (Professionalism - 10%):**
  - Điểm mạnh: Cấu trúc thư mục độc lập, mã nguồn sạch sẽ, chú thích rõ ràng, cung cấp sẵn file chạy tự động một chạm.
