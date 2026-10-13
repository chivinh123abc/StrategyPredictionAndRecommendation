# BÁO CÁO KHOA HỌC: ĐÁNH GIÁ TOÀN DIỆN MÔ HÌNH MACHINE LEARNING (TASK 3.3)

## THÔNG TIN TỔNG QUAN
- **Dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Học phần:** Nhập môn Khoa học Dữ liệu - PTIT (Giảng viên: TS. Thái Tuyết Hải).
- **Mã nguồn đánh giá:** [`src/06_machine_learning/evaluate_models.py`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/06_machine_learning/evaluate_models.py)
- **Thư mục biểu đồ xuất bản (300 DPI):** [`reports/figures/`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/reports/figures/)
  - Fig 6: `fig6_roc_auc_comparison.png`
  - Fig 7: `fig7_confusion_matrices.png`
  - Fig 8: `fig8_calibration_curve.png`
  - Fig 9: `fig9_draft_vs_snowball_feature_importance.png`

---

## 1. TỔNG HỢP HIỆU NĂNG MÔ HÌNH 2 GIAI ĐOẠN

| Giai Đoạn Dự Đoán | Mô Hình Tối Ưu | Số Quan Sát Test Set | Accuracy | ROC-AUC | F1-Score | Brier Score | Log Loss |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Cấm/Chọn (Phút 0 - Draft AI)** | Random Forest (150 trees) | 600 trận (Time-split) | **53.83%** | **0.5510** | **0.5771** | **0.2487** | **0.6905** |
| **Thực Chiến (Phút 10 - Snowball AI)** | Random Forest (150 trees) | 1,354 trận (Stratified) | **70.75%** | **0.7780** | **0.7023** | **0.1925** | **0.5682** |

---

## 2. PHÂN TÍCH CHI TIẾT BỘ 4 BIỂU ĐỒ NGHIÊN CỨU

### 2.1. Biểu đồ Fig 6: Đường cong ROC-AUC & Precision-Recall
- **Ý nghĩa:** Đo lường khả năng phân tách giữa 2 lớp (Thắng vs Thua) ở mọi ngưỡng xác suất (Thresholds từ 0.0 đến 1.0).
- **Kết quả quan sát:**
  - **Draft Model (Phút 0 - Đường màu xanh):** Đạt diện tích dưới đường cong **ROC-AUC = 0.5510**. Đường cong nằm phía trên đường ngẫu nhiên (Chance Baseline = 0.50), chứng minh giai đoạn cấm/chọn tạo ra một lợi thế nghiêng về phía đội ban/pick tốt hơn ~4-5%.
  - **Snowball Model (Phút 10 - Đường màu đỏ):** Đạt diện tích **ROC-AUC = 0.7780** (ở Solo Rank đạt **0.8189**). Đường cong vươn cao về góc trên bên trái, thể hiện năng lực phân loại vượt bậc khi trận đấu đã hình thành chênh lệch tài nguyên và mục tiêu lớn.

---

### 2.2. Biểu đồ Fig 7: Ma trận nhầm lẫn (Confusion Matrices)
- **Ý nghĩa:** Thống kê chi tiết tỷ lệ phân loại đúng và nhầm lẫn trên tập kiểm thử độc lập.
- **Phân tích:**
  - **Mô hình Draft (Phút 0 - N = 600):**
    - Phân loại đúng: 323 / 600 trận (Accuracy 53.83%).
    - Độ nhạy với Phe Xanh cao hơn do ưu thế sân nhà và thứ tự chọn trước.
  - **Mô hình Snowball (Phút 10 - N = 1,354):**
    - Phân loại đúng: 958 / 1,354 trận (Accuracy 70.75%).
    - Cân bằng xuất sắc giữa việc nhận diện đội dẫn trước thắng và đội bị dẫn thua.

---

### 2.3. Biểu đồ Fig 8: Hiệu chuẩn xác suất (Probability Calibration & Reliability Curve)
- **Ý nghĩa:** Kiểm định tính trung thực của xác suất dự đoán (Calibration). Một mô hình có độ tin cậy cao khi xác suất dự báo 70% tương ứng với tỷ lệ thắng thực tế 70%.
- **Phân tích Brier Score:**
  - **Draft Model:** `Brier Score = 0.2487` (Thấp hơn mức ngẫu nhiên 0.2500). Đường hiệu chuẩn bám sát trục đường chéo 45 độ trong khoảng xác suất từ 45% đến 60%.
  - **Snowball Model:** `Brier Score = 0.1925` (Mức suy giảm lỗi vượt bậc). Đường hiệu chuẩn mượt mà từ 0.1 đến 0.9, khẳng định đầu ra xác suất của mô hình hoàn toàn đủ độ tin cậy để làm thang đo định lượng trực quan cho giao diện Dashboard.

---

### 2.4. Biểu đồ Fig 9: So sánh Trọng số Đặc trưng (Feature Importance)
- **Cấm/Chọn (Phút 0 - Không gian 799 chiều):**
  1. *Position One-Hot (10 Tướng thi đấu):* Chiếm **46.8%** trọng số.
  2. *Lane Matchup Advantage (5 Cặp đối đầu đường):* Chiếm **18.4%**.
  3. *Bayesian Champion Winrates (Tỷ lệ thắng Meta):* Chiếm **15.2%**.
  4. *Synergy Duo (Mid-Jng, Bot-Sup):* Chiếm **10.6%**.
  5. *Team Comp Balance (AD/AP/CC/Scaling):* Chiếm **9.0%**.
- **Thực Chiến (Phút 10 - 22 Đặc trưng):**
  1. *Chênh lệch vàng tổng (`golddiffat10`):* **15.50%**
  2. *Chênh lệch cấp độ/kinh nghiệm (`xpdiffat10`):* **14.13%**
  3. *Vàng dồn cho 2 Chủ lực Mid + Bot (`carry_gold_lead`):* **9.75%**
  4. *Tương tác Vàng + Rồng 1 (`gold_dragon_synergy`):* **7.65%**
  5. *Trụ đầu tiên (`firsttower`):* **7.32%**

---

## 3. KẾT LUẬN NGHIỆP VỤ & HÀNH ĐỘNG TIẾP THEO

1. **Minh chứng khoa học chặt chẽ:** Việc đánh giá song song 2 mô hình đã chứng minh bằng số liệu thực nghiệm rằng Cấm/Chọn cung cấp nền tảng chiến thuật ban đầu, trong khi kỹ năng thực chiến (Hands Diff) và kiểm soát tài nguyên chuyển hóa thành chiến thắng ở giai đoạn sau.
2. **Sẵn sàng bước sang Task 3.4 & Task 3.5:** Hệ thống đã có đầy đủ bộ số liệu và các mô hình nền tảng để triển khai bộ công cụ Gợi ý Cấm/Chọn Thông Minh (Target Ban, Meta Recommender, Draft Flaw & Punisher Engine).
