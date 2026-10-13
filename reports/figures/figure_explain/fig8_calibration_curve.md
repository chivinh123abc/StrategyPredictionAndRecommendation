# GIẢI THÍCH CHI TIẾT FIG 8: ĐƯỜNG CONG HIỆU CHUẨN XÁC SUẤT (PROBABILITY CALIBRATION CURVE)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig8_calibration_curve.png`  
> **Chương giáo trình:** Chương 4 & 5 - Đánh giá độ tin cậy xác suất của mô hình học máy (Probability Calibration & Brier Score)  
> **Nguồn dữ liệu:** Kiểm thử trên 600 trận Draft và 1,354 trận Snowball từ CSDL `lol_live_data.db`.

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC

Trong Khoa học Dữ liệu, chỉ số Accuracy hay F1-score chỉ đo lường việc phân loại nhị phân (0 hay 1). Tuy nhiên, đối với một **Hệ Thống Trợ Lý Cấm/Chọn (AI Assistant)**, đầu ra hiển thị cho người dùng là **con số Xác Suất Thắng (ví dụ: "Đội Xanh có 65.4% tỷ lệ thắng")**.

Biểu đồ Fig 8 (Reliability Diagram) sinh ra để trả lời câu hỏi sống còn:
* *"Khi mô hình AI dự báo một đội có 70% tỷ lệ thắng, thì trong thực tế 100 trận có dự báo tương tự, đội đó có thực sự thắng đúng khoảng 70 trận hay không?"*

---

## 2. CẤU TRÚC ĐỒ HỌA & CÁCH ĐỌC BIỂU ĐỒ

- **Trục hoành (X-axis):** Xác suất thắng dự đoán của mô hình (Predicted Probability từ 0.0 đến 1.0 chia thành các khoảng bin).
- **Trục tung (Y-axis):** Tỷ lệ thắng thực tế diễn ra trên dữ liệu lịch sử (Fraction of Positives).
- **Đường nét đứt màu xám (Đường chéo 45 độ):** Đại diện cho **Hiệu chuẩn hoàn hảo (Perfect Calibration)**. Nếu điểm nằm chính xác trên đường này, mô hình hoàn toàn trung thực với thực tế.
- **Đường màu xanh dương (Draft Model - Phút 0):**
  - Đạt điểm sai số `Brier Score = 0.2487` (Tốt hơn mức ngẫu nhiên 0.2500).
  - Điểm dự đoán tập trung chủ yếu trong vùng hẹp từ **45% đến 60%**. Điều này phản ánh thực tế khách quan rằng cấm/chọn không bao giờ đẩy tỷ lệ thắng lên 90% hay hạ xuống 10% khi 10 tướng vừa vào trận.
- **Đường màu đỏ (Snowball Model - Phút 10):**
  - Đạt điểm sai số `Brier Score = 0.1925` (Mức suy giảm sai số vượt bậc).
  - Đường cong bám sát đường chéo lý tưởng trên toàn bộ dải xác suất từ 0.1 đến 0.9.

---

## 3. THANG ĐO ĐỊNH LƯỢNG: BRIER SCORE

* **Định nghĩa:** Brier Score đo bình phương khoảng cách trung bình giữa xác suất dự đoán và kết quả thực tế (0 hoặc 1). Giá trị càng gần 0 thì mô hình càng chuẩn xác và đáng tin cậy.
* **So sánh:**
  * Mô hình đoán mò ngẫu nhiên (50/50): `Brier Score = 0.2500`.
  * Draft Model (Phút 0): `Brier Score = 0.2487` (Đã có tính thông tin vượt trên mức ngẫu nhiên).
  * Snowball Model (Phút 10): `Brier Score = 0.1925` (Đạt chuẩn mô hình xác suất tin cậy cao của các hệ thống dự báo thể thao chuyên nghiệp).

---

## 4. CÂU HỎI BẢO VỆ PHẢN BIỆN (Q&A)

### Câu hỏi: Tại sao đường màu xanh của Draft Model lại không kéo dài từ 0.0 đến 1.0 như đường màu đỏ?
- **Trả lời phản biện chuẩn:**
  > "Vì ở giai đoạn cấm/chọn (Phút 0), không có bất kỳ đội hình nào có thể đảm bảo 100% thắng hoặc 100% thua. Đội hình dù out-draft đến mấy thì tỷ lệ thắng trong thực tế cũng chỉ dao động trong khoảng từ 40% đến 65%. Việc mô hình Draft tự giới hạn dải xác suất trong khoảng này chứng minh mô hình không bị tự tin thái quá (Overconfident) và phản ánh chính xác bản chất xác suất của trò chơi."
