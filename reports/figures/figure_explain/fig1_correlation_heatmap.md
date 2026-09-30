# GIẢI THÍCH CHI TIẾT FIG 1: MA TRẬN TƯƠNG QUAN PEARSON (CORRELATION HEATMAP)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig1_correlation_heatmap.png`  
> **Chương giáo trình:** Chương 3 - Trực quan hóa dữ liệu khám phá (EDA)  
> **Nguồn dữ liệu:** 3,000 trận Đấu Giải Chuyên Nghiệp đỉnh cao (6,000 bản ghi đội từ bảng `tournament_matches` trong CSDL SQLite `lol_live_data.db`)

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC CỦA BIỂU ĐỒ

Biểu đồ Fig 1 sinh ra để trả lời câu hỏi cốt lõi:
* *"Trong số các chỉ số tích lũy được sau 10 phút đầu trận, chỉ số nào có mối liên hệ mạnh nhất tới việc thắng/thua trận đấu, và các chỉ số này tương tác qua lại với nhau như thế nào?"*
* **Ý nghĩa đối với Giai đoạn 3 (Machine Learning):** Đây là cơ sở thực nghiệm để thực hiện **Lựa chọn đặc trưng (Feature Selection)**. Biến nào có hệ số tương quan cao sẽ được ưu tiên đưa vào làm đầu vào chính cho các mô hình AI dự đoán (Random Forest / XGBoost).

---

## 2. CẤU TRÚC ĐỒ HỌA & THƯỚC ĐO MÀU SẮC (COLORBAR)

### A. Ma trận tam giác dưới (Lower Triangle Matrix)
* Trong thống kê, ma trận tương quan luôn đối xứng qua đường chéo chính (r giữa A và B bằng r giữa B và A).
* Biểu đồ chủ động ẩn nửa tam giác trên để loại bỏ 50% thông tin lặp lại thừa thãi, giúp người đọc tập trung vào các giao điểm quan trọng.

### B. Thước đo màu (Colorbar bên phải)
* Thang đo chạy từ **-1.0 đến +1.0** theo đúng định nghĩa toán học của Hệ số tương quan Pearson:
  * **Tông màu Đỏ / Cam (r > 0):** Tương quan thuận (Biến này tăng kéo theo biến kia tăng).
  * **Màu Trắng / Xám nhạt (r ≈ 0):** Không có tương quan tuyến tính (Hai biến độc lập).
  * **Tông màu Xanh Dương (r < 0):** Tương quan nghịch (Biến này tăng làm biến kia giảm).

---

## 3. GIẢI THÍCH TẠI SAO ĐƯỜNG CHÉO BẰNG 1.00 VÀ TẠI SAO KHÔNG CÓ -1.00

### Tại sao trên đường chéo chính luôn luôn bằng 1.00?
* Đường chéo chính là giao điểm của **chính một biến so với chính bản thân nó** (ví dụ: Chênh Vàng so với Chênh Vàng).
* Hai đại lượng giống hệt nhau thì mức độ đồng điệu là trùng khớp 100% tuyệt đối, theo công thức toán học tử số và mẫu số bằng nhau nên kết quả luôn bằng **1.00**.

### Tại sao không có chỉ số nào đạt -1.00?
* r = -1.00 chỉ xảy ra khi có một mối quan hệ hàm số ngặt nghèo: biến A tăng thì biến B chắc chắn 100% phải giảm, không có bất kỳ ngoại lệ nào.
* Trong thể thao điện tử LMHT, ở phút thứ 10 dù một đội có chết nhiều mạng (deathsat10 cao, r = -0.17) thì họ **vẫn còn cơ hội lật kèo (Comeback)** ở giao tranh Baron phút 25-30 hoặc đối thủ quăng game. Không có chỉ số nào ở phút thứ 10 đảm bảo 100% là thua trận.

---

## 4. CHI TIẾT TOÀN BỘ CÁC CẶP CHỈ SỐ GIAO NHAU (MA TRẬN 9x9)

### Nhóm 1: Các chỉ số giao với "Thắng Trận (Result)"
1. **Chênh Vàng vs Thắng Trận (r = +0.38):** Yếu tố dự đoán chiến thắng mạnh nhất mốc 10 phút. Dẫn tiền cho phép mua trang bị lớn sớm để ép giao tranh.
2. **Chênh XP vs Thắng Trận (r = +0.35):** Dẫn cấp độ giúp chủ lực đạt cấp 6 (Chiêu cuối) sớm hơn đối thủ, tạo ưu thế giao tranh mục tiêu.
3. **Chênh Lính vs Thắng Trận (r = +0.30):** Kỹ năng đè đường đẩy lính vào trụ tạo áp lực kiểm soát bản đồ.
4. **Ăn Rồng 1 vs Thắng Trận (r = +0.19):** Có tương quan thuận rõ rệt, tạo đà tích lũy Linh Hồn Rồng.
5. **Số Mạng Ăn vs Thắng Trận (r = +0.17):** Ăn mạng mang lại tiền thưởng và tâm lý tự tin.
6. **Số Mạng Chết vs Thắng Trận (r = -0.17):** Càng chết nhiều ở 10 phút đầu cơ hội thắng càng giảm.
7. **Sâu Hư Không vs Thắng Trận (r = +0.10):** Tương quan dương nhẹ (thấp hơn Rồng 1 ở Đấu Giải).
8. **Thời Lượng Trận Đấu vs Thắng Trận (r = -0.00):** Độc lập hoàn toàn, vì trận dài hay ngắn luôn có 1 đội thắng và 1 đội thua.

### Nhóm 2: Mối tương tác nội tại giữa các chỉ số kinh tế
9. **Chênh Vàng vs Chênh XP (r = +0.74):** Tương quan cực mạnh. Đè tiền gần như luôn đi kèm đè cấp độ do đối thủ mất lính khi biến về nhà.
10. **Chênh Vàng vs Chênh Lính (r = +0.57):** Lính là nguồn kinh tế ổn định nhất đầu trận.
11. **Chênh Vàng vs Số Mạng Ăn (r = +0.51) / Chết (r = -0.50):** Mạng hạ gục trực tiếp nới rộng khoảng cách tiền.
12. **Chênh XP vs Chênh Lính (r = +0.69):** Lính mang lại cả vàng lẫn kinh nghiệm.

### Nhóm 3: Mối quan hệ mục tiêu và thời lượng
13. **Ăn Rồng 1 vs Ăn Sâu Hư Không (r = -0.17):** Tương quan nghịch rõ rệt, minh chứng dữ liệu cho chiến thuật "Đổi chéo mục tiêu" (ăn Rồng 1 cánh dưới thì nhường Sâu cánh trên).
14. **Chênh Vàng vs Thời Lượng Trận Đấu (r = -0.00 trên ma trận chung, nhưng xét riêng đội dẫn tiền là r = -0.31):** Dẫn càng nhiều tiền trận kết thúc càng nhanh do Snowball hiệu quả.

---

## 5. LƯU Ý PHÂN BIỆT QUAN TRỌNG: "HỆ SỐ r" KHÔNG PHẢI LÀ "TỶ LỆ %"
* Con số **0.38** giữa Chênh Vàng và Thắng Trận là **hệ số đo độ dốc tương quan tuyến tính**, không phải là 0.38% tỷ lệ thắng.
* Trên thực tế dữ liệu dự án:
  * Dẫn >= 1,000 vàng lúc 10p: Tỷ lệ thắng đạt **72.5%**
  * Dẫn >= 2,000 vàng lúc 10p: Tỷ lệ thắng đạt **83.5% - 86.0%**
  * Dẫn >= 3,000 vàng lúc 10p: Tỷ lệ thắng đạt **93.0%**
