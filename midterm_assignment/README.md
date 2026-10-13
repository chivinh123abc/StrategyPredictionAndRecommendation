# BÀI TẬP LỚN GIỮA KỲ: NHẬP MÔN KHOA HỌC DỮ LIỆU
## TOPIC 2: PHÁT HIỆN VÀ XỬ LÝ ĐIỂM NGOẠI LAI (OUTLIER DETECTION & HANDLING)
**Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
**Đơn vị:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  

---

## 📁 CẤU TRÚC THƯ MỤC `midterm_assignment/`

```text
midterm_assignment/
├── README.md                                  # Hướng dẫn tổng quan & nộp bài
├── REQUIREMENTS.md                            # ĐẶC TẢ CHI TIẾT ĐỀ BÀI & CÁC YÊU CẦU ĐẶT RA
├── TASKS.md                                   # DANH SÁCH TÁC VỤ & ATOMIC CHECKLIST CỦA MIDTERM
├── data/
│   ├── outlier_experiment_data.csv            # 2,304 ván đấu Đấu Giải Chuyên Nghiệp LMHT 2026
│   └── outlier_comparison_summary.csv         # Bảng tổng hợp so sánh các chỉ số thống kê
├── figures/                                   # Bộ 4 biểu đồ độ phân giải cao 300 DPI
│   ├── fig1_outlier_detection_iqr_zscore.png  # Phân phối & Ngưỡng IQR vs Z-Score
│   ├── fig2_distribution_before_after.png     # So sánh hàm mật độ KDE trước & sau xử lý
│   ├── fig3_scatter_multivariate_outliers.png # Tương quan 2D Vàng vs Kinh nghiệm & Độ đồng thuận
│   └── fig4_statistical_impact_comparison.png# Đo lường định lượng thay đổi Mean, Std, Range
├── report/                                    # Báo cáo học thuật chi tiết (Deliverable 1)
│   ├── MIDTERM_REPORT_TOPIC2.docx             # File Word nộp bài chính thức (đã chèn hình & bảng chuẩn)
│   └── MIDTERM_REPORT_TOPIC2.md               # Bản Markdown lưu trữ
├── slides/                                    # Slide thuyết trình (Deliverable 2)
│   ├── MIDTERM_SLIDES_TOPIC2.pptx             # File PowerPoint 16:9 hiện đại (12 slides có hình ảnh)
│   └── MIDTERM_SLIDES_TOPIC2.md               # Kịch bản thuyết trình Markdown
└── src/                                       # Toàn bộ mã nguồn thực thi
    ├── outlier_experiment.py                  # Script chạy thí nghiệm, tính toán & xuất 4 biểu đồ
    └── build_deliverables.py                  # Script tự động tạo file Word .docx và PowerPoint .pptx
```

---

## 📋 CÁC YÊU CẦU ĐƯỢC ĐẶT RA (REQUIREMENTS SUMMARY)

*Chi tiết toàn văn đề bài, barem điểm (Rubrics) và Ma trận đối chiếu xem tại [REQUIREMENTS.md](file:///d:/Chivinh/2026_MonHoc/Nh%E1%BA%ADp%20m%C3%B4n%20khoa%20h%E1%BB%8Dc%20d%E1%BB%AF%20li%E1%BB%87u/Project/midterm_assignment/REQUIREMENTS.md).*

1. **Khái niệm:** Định nghĩa Outlier; phân biệt rạch ròi với Dữ liệu sai hỏng (Erroneous Data).
2. **Nguyên nhân:** Làm rõ 4 nguyên nhân sinh ra ngoại lai trong dữ liệu thực tế.
3. **Phương pháp:** Trình bày lý thuyết IQR, Z-Score (và mở rộng Isolation Forest), so sánh ưu/nhược điểm.
4. **Thực nghiệm:** Thiết kế thí nghiệm trên dữ liệu tự chọn (2,304 ván đấu Pro Play LMHT 2026).
5. **Đánh giá tác động:** Đo lường sự thay đổi của Mean, Std Dev, Skewness, Min, Max qua các phương pháp.
6. **Chiến lược can thiệp:** Thảo luận khi nào Retain, Trim, Winsorize, Transform; đề xuất Winsorization tối ưu cho ML.
7. **Quy chuẩn sản phẩm:**
   - Báo cáo văn bản: 6 - 15 trang (đã hoàn thành bản Word `.docx` và `.md`).
   - Slide thuyết trình: 8 - 15 slides (đã hoàn thành bản PowerPoint `.pptx` 12 slides).
   - Đính kèm mã nguồn và tập dữ liệu thí nghiệm.

---

## 🚀 HƯỚNG DẪN CHẠY LẠI THÍ NGHIỆM TỪ ĐẦU (REPRODUCIBILITY)

Nếu muốn tái tạo lại kết quả hoặc chỉnh sửa tham số:
1. **Kích hoạt môi trường Python:**
   ```powershell
   .venv\Scripts\activate
   ```
2. **Chạy thí nghiệm phát hiện ngoại lai:**
   ```powershell
   python midterm_assignment/src/outlier_experiment.py
   ```
3. **Biên tập và xuất bản lại Word `.docx` và PowerPoint `.pptx`:**
   ```powershell
   python midterm_assignment/src/build_deliverables.py
   ```

---

## 📊 KẾT QUẢ CỐT LÕI CỦA THÍ NGHIỆM

- **Tập dữ liệu:** 2,304 ván đấu Đội Xanh tại LCK, LPL, LCP, EWC, MSI 2026 (`golddiffat10`).
- **Phát hiện theo IQR (1.5 x IQR):** Gắn cờ **23 ván (1.00%)**, ngưỡng `[-2,961.2g, +3,136.8g]`.
- **Phát hiện theo Z-Score (|Z| > 3.0):** Chỉ gắn cờ **2 ván (0.09%)**, ngưỡng `[-3,417.0g, +3,613.8g]`.
- **Hiện tượng Che khuất (Masking Effect):** Z-Score bỏ sót tới 21 ván đấu lăn cầu tuyết cực lớn do độ lệch chuẩn bị đội lên 1,171.80 vàng. IQR chứng minh tính ưu việt vượt trội trong thực tế.
- **Chiến lược tối ưu:** **Winsorization (Cắt ngọn 1%-99%)** giữ nguyên 100% kích thước mẫu ($N = 2,304$), kiểm soát phương sai (giảm nhẹ 1.27%) và bảo vệ hàm mất mát khi huấn luyện mô hình học máy.
