# GIẢI THÍCH CHI TIẾT FIG 7: MA TRẬN NHẦM LẪN (CONFUSION MATRICES)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig7_confusion_matrices.png`  
> **Chương giáo trình:** Chương 4 & 5 - Đánh giá mô hình học máy (Classification Metrics)  
> **Nguồn dữ liệu:** Kiểm thử trên 600 trận Cấm/Chọn (Phút 0) và 1,354 trận Thực chiến (Phút 10) từ CSDL `lol_live_data.db`.

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC

Ma trận nhầm lẫn (Confusion Matrix) giúp nhìn thấu bên trong con số Accuracy tổng thể, bóc tách cụ thể:
1. Mô hình dự đoán đúng bao nhiêu trận Thắng thật (True Positive) và Thua thật (True Negative)?
2. Mô hình có bị thiên kiến (Bias) nghiêng về dự đoán Thắng hay Thua nhiều hơn không?
3. Sai số dự đoán ở Phút 0 và Phút 10 xảy ra ở các trường hợp nào?

---

## 2. BÓC TÁCH CHI TIẾT 2 MA TRẬN

### A. Ma trận 1 (Bên trái): Draft Model - Phút 0 (Test Set N = 600 trận)
- **Cấu trúc 4 ô phân loại:**
  - **True Negative (Thực tế Thua, Đoán Thua):** 113 trận (38.8% số trận Thua).
  - **False Positive (Thực tế Thua, Đoán nhầm Thắng):** 178 trận (61.2% số trận Thua) $\rightarrow$ *Trường hợp đội ban/pick đẹp nhưng tuyển thủ thi đấu dưới sức hoặc quăng game.*
  - **False Negative (Thực tế Thắng, Đoán nhầm Thua):** 99 trận (32.0% số trận Thắng) $\rightarrow$ *Trường hợp đội ban/pick yếu hơn nhưng lật kèo nhờ kỹ năng cá nhân (Hands Diff vượt trội).*
  - **True Positive (Thực tế Thắng, Đoán Thắng):** 210 trận (68.0% số trận Thắng).
- **Tổng số trận đoán đúng:** 113 + 210 = **323 / 600 trận (Accuracy = 53.83%)**.
- **Nhận xét chuyên môn:** Mô hình Draft có xu hướng dự đoán nghiêng về Phe Xanh (Blue Side) do Phe Xanh có lợi thế First Pick và tỷ lệ thắng nền tảng cao hơn (53.5%).

---

### B. Ma trận 2 (Bên phải): Snowball Model - Phút 10 (Test Set N = 1,354 trận)
- **Cấu trúc 4 ô phân loại:**
  - **True Negative (Thực tế Thua, Đoán Thua):** 481 trận (71.0% số trận Thua).
  - **False Positive (Thực tế Thua, Đoán nhầm Thắng):** 196 trận (29.0% số trận Thua) $\rightarrow$ *Trường hợp dẫn tiền phút 10 nhưng quăng game ở giai đoạn sau (chủ yếu ở Đấu Xếp Hạng).*
  - **False Negative (Thực tế Thắng, Đoán nhầm Thua):** 200 trận (29.5% số trận Thắng) $\rightarrow$ *Trường hợp bị dẫn tiền phút 10 nhưng lật kèo thành công (Comeback ở Đấu Giải nhờ đội hình Scaling).*
  - **True Positive (Thực tế Thắng, Đoán Thắng):** 477 trận (70.5% số trận Thắng).
- **Tổng số trận đoán đúng:** 481 + 477 = **958 / 1,354 trận (Accuracy = 70.75%)**.
- **Nhận xét chuyên môn:** Ma trận có tính đối xứng và cân bằng rất cao giữa việc phát hiện đội thắng và đội thua, không bị lệch nhãn.

---

## 3. BẢNG TỔNG HỢP CHỈ SỐ PHÂN LOẠI CHI TIẾT (PRECISION, RECALL, F1)

| Mô Hình | Precision (Độ chuẩn xác) | Recall (Độ phủ) | F1-Score | Accuracy Tổng |
| :--- | :---: | :---: | :---: | :---: |
| **Draft Model (Phút 0)** | 54.12% | 67.96% | **57.71%** | **53.83%** |
| **Snowball Model (Phút 10)** | 70.88% | 70.46% | **70.23%** | **70.75%** |

---

## 4. CÂU HỎI BẢO VỆ PHẢN BIỆN (Q&A)

### Câu hỏi: False Positive và False Negative trong mô hình LMHT cái nào nguy hiểm hơn?
- **Trả lời phản biện chuẩn:**
  > "Trong bài toán Trợ lý Cấm/Chọn LMHT, cả 2 loại lỗi đều mang lại bài học chiến thuật giá trị:
  > - **False Positive (Đoán Thắng nhưng Thua):** Cho biết cấm chọn đã tốt nhưng thất bại do triển khai chiến thuật (In-game execution) hoặc gank lỗi đầu trận.
  > - **False Negative (Đoán Thua nhưng Thắng):** Cho biết đội hình cấm chọn bị lép vế nhưng đã lật kèo nhờ sự tỏa sáng cá nhân của một tuyển thủ hoặc bắt lẻ thành công ở hang Baron."
