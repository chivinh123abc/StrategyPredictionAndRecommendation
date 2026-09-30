# GIẢI THÍCH CHI TIẾT FIG 3: PHÂN BỐ KINH TẾ 5 VỊ TRÍ THI ĐẤU (BOXPLOT & OUTLIERS)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig3_lane_economy_boxplot.png`  
> **Chương giáo trình:** Chương 3 - Trực quan hóa dữ liệu khám phá (EDA)  
> **Nguồn dữ liệu:** 23,690 quan sát tuyển thủ đối đầu 1v1 từ 3,000 trận Đấu Giải Chuyên Nghiệp (bảng `tournament_players` trong CSDL SQLite `lol_live_data.db`)

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC

Biểu đồ Fig 3 sinh ra để giải mã câu hỏi:
* *"Vị trí thi đấu nào trên bản đồ (Top, Jungle, Mid, Bot, Support) có mức độ chênh lệch tiền đối đầu 1v1 khốc liệt và rủi ro ngoại lai cao nhất lúc 10 phút đầu trận?"*

---

## 2. CẤU TRÚC VÀ CÁCH ĐỌC MỘT "CHIẾC HỘP" (BOXPLOT)

Biểu đồ so sánh 5 vị trí:
1. **Đường Trên (Top)** - Màu Đỏ
2. **Đi Rừng (Jungle)** - Màu Xanh Lá
3. **Đường Giữa (Mid)** - Màu Xanh Dương
4. **Xạ Thủ (Bot / ADC)** - Màu Vàng Cam
5. **Hỗ Trợ (Support)** - Màu Tím

### Ý nghĩa của các thành phần trong 1 hình hộp:
* **Đường gạch ngang ở giữa hộp (Median):** Giá trị Trung vị = **0 vàng** (vì mỗi trận đều có 1 người bên Xanh và 1 người bên Đỏ đối đầu trực tiếp, nên tâm phân phối luôn cân bằng ở 0g).
* **Chiều cao thân hộp (Độ trải giữa IQR = Q3 - Q1):** Chứa **50% số trận đấu phổ biến nhất** ở vị trí đó.
  * **Hộp càng cao** -> Vị trí đó có chênh lệch tiền giữa 2 tuyển thủ càng lớn, biến động cực mạnh.
  * **Hộp càng lùn / hẹp** -> Vị trí đó ít bị chênh lệch tiền, thu nhập tương đối ổn định.
* **Hai râu hộp (Whiskers):** Giới hạn biến thiên thông thường (trong phạm vi 1.5 lần IQR).
* **Các chấm tròn màu xám (Outliers):** Những trận đấu có chênh lệch tiền **bất thường, cực đoan** (đè nát đường hoặc bị thọt nặng nề).

---

## 3. BẢNG SỐ LIỆU THỰC TẾ 5 VỊ TRÍ

| Vị Trí Thi Đấu | Độ Trải Giữa (IQR) | Độ Lệch Chuẩn (Std) | Mức Độ Biến Động |
| :--- | :---: | :---: | :--- |
| **Xạ Thủ (Bot / ADC)** | **642 vàng** | 547 vàng | **Cao nhất toàn bản đồ** |
| **Đường Trên (Top)** | **616 vàng** | 471 vàng | Rất cao |
| **Đi Rừng (Jungle)** | **572 vàng** | 461 vàng | Mức độ trung bình - khá |
| **Đường Giữa (Mid)** | **556 vàng** | 465 vàng | Khá ổn định |
| **Hỗ Trợ (Support)** | **328 vàng** | 295 vàng | **Thấp nhất / Ổn định nhất** |

---

## 4. GIẢI THÍCH VẤN ĐỀ ĐỐI XỨNG GƯƠNG QUA 0 VÀ 2 ĐẦU NGOẠI LAI (+/-)

### Tại sao biểu đồ lại đối xứng hoàn hảo qua mốc 0?
* Trong mỗi trận đấu, nếu Tuyển thủ Phe Xanh dẫn trước **+500 vàng**, thì Tuyển thủ Phe Đỏ đối đầu trực tiếp sẽ bị ghi nhận là **-500 vàng** (golddiff_Red = -golddiff_Blue).
* Do đó, tập dữ liệu chứa cả 2 góc nhìn (Perspective của Phe Xanh và Phe Đỏ), tạo nên phân phối đối xứng gương qua 0 (Median = 0, Q1 = -Q3).

### Tại sao 1 trận đấu có thể sinh ra 2 chấm ngoại lai (+5,000g và -5,000g)? Có vấn đề gì về bản chất không?
* **HOÀN TOÀN KHÔNG CÓ VẤN ĐỀ**, vì đơn vị quan sát ở đây là **Từng Tuyển Thủ (Player-Level)**:
  * Tuyển thủ Phe Xanh trải qua trận đấu **thăng hoa cực độ** (+5,000 vàng) -> 1 quan sát ngoại lai dương (Stomp Outlier).
  * Tuyển thủ Phe Đỏ trải qua trận đấu **thảm họa cực độ** (-5,000 vàng) -> 1 quan sát ngoại lai âm (Be Stomped Outlier).
* Cả 2 con số này đều là trải nghiệm thi đấu thực tế của 2 con người khác nhau trong trận đấu đó. Cả 5 vị trí đều được áp dụng cấu trúc dữ liệu đối xứng như nhau nên so sánh hoàn toàn công bằng.

---

## 5. CÁC PHÁT HIỆN CHIẾN THUẬT QUAN TRỌNG

1. **Xạ Thủ (Bot: IQR = 642g) và Đường Trên (Top: IQR = 616g) có mức độ phân hóa cao nhất:**
   * Bot là giao tranh 2v2 kết hợp gank, có mạng sớm sẽ bào sạch Giáp Trụ (Plates) khiến tiền giãn ra rất nhanh.
   * Top là hòn đảo solo 1v1 dài hơi, khi bị solo-kill hoặc counter-pick rất dễ bị đóng băng lính và thọt nặng nề.
2. **Đường Giữa (Mid: IQR = 556g) an toàn hơn Đường Trên:**
   * Đường giữa rất ngắn, trụ ở sát lưng. Tuyển thủ khi gặp kèo khó có thể lùi sâu ôm trụ dùng kỹ năng dọn lính từ xa để tránh bị đè tiền quá mức.
3. **Hỗ Trợ (Support: IQR = 328g) ổn định nhất:**
   * Hỗ trợ không farm lính mà thu nhập chủ yếu đến từ Trang bị Hỗ Trợ khởi đầu với lượng vàng thụ động cố định theo thời gian.
