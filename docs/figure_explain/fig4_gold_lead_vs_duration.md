# GIẢI THÍCH CHI TIẾT FIG 4: VÀNG DẪN TRƯỚC VS THỜI LƯỢNG TRẬN ĐẤU (SCATTER + REGRESSION)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig4_gold_lead_vs_duration_scatter.png`  
> **Chương giáo trình:** Chương 3 - Trực quan hóa dữ liệu khám phá (EDA)  
> **Nguồn dữ liệu:** Đấu Giải Chuyên Nghiệp (Pro Play) vs Solo Rank Thách Đấu (VN & KR) từ CSDL SQLite `lol_live_data.db`

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC

Biểu đồ Fig 4 trả lời câu hỏi:
* *"Khi một đội dẫn trước nhiều tiền ở phút thứ 10, thời lượng trận đấu sẽ bị rút ngắn bao nhiêu phút và có sự khác biệt gì giữa Đấu Giải Chuyên Nghiệp vs Solo Rank?"*

---

## 2. CẤU TRÚC VÀ CÁC THÀNH PHẦN TRÊN BIỂU ĐỒ

Biểu đồ gồm 2 đồ thị con đối chiếu song song:
* **Bên Trái (Màu Xanh Dương):** Đấu Giải Chuyên Nghiệp (Pro Play).
* **Bên Phải (Màu Xanh Lá):** Solo Rank Thách Đấu.

### Các yếu tố trên biểu đồ:
* **Trục hoành (Trục X):** Lượng vàng đội dẫn trước lúc 10 phút (từ 0 đến 5,000 vàng).
* **Trục tung (Trục Y):** Thời lượng trận đấu thực tế (tính bằng phút).
* **Mỗi chấm tròn:** Đại diện cho **1 trận đấu thực tế**.
* **Đường nét liền màu Đỏ (Đường hồi quy OLS):** Xu hướng biến thiên trung bình của thời lượng theo lượng vàng dẫn trước.
* **Đường nét chấm màu Cam (Mốc 20 phút):** Thời điểm Bùa Lợi Baron xuất hiện trên bản đồ.
* **Đường nét đứt màu Đỏ (Mốc 15 phút - ở đồ thị Solo Rank):** Mốc biểu quyết Đầu Hàng Sớm (FF15).

---

## 3. CÁC PHÁT HIỆN KHOA HỌC & CHIẾN THUẬT TRỌNG TÂM

### A. Độ dốc âm rõ rệt: Minh chứng cho hiệu ứng "Lăn Cầu Tuyết" (Snowball)
* Ở cả 2 môi trường, đường màu đỏ đều dốc xuống từ trái qua phải:
  * Khi chỉ dẫn nhẹ **+500 vàng**: Trận đấu kéo dài trung bình **33 - 35 phút**.
  * Khi dẫn đậm **+3,500 vàng**: Thời lượng trận đấu bị kéo tụt xuống chỉ còn **24 - 26 phút**.
* **Ý nghĩa:** Lượng tiền dẫn trước được chuyển hóa thành trang bị, giúp đội dẫn tiền đẩy trụ nhanh hơn, kiểm soát hoàn toàn bản đồ và bóp nghẹt đối thủ để kết liễu trận đấu sớm hơn gần **10 phút**.

### B. Đối chiếu Đấu Giải (Trái) vs Solo Rank (Phải): Ranh giới 20 phút (Baron) và 15 phút (FF15)

| Đặc điểm | Đấu Giải Chuyên Nghiệp (Trái) | Solo Rank Thách Đấu (Phải) |
| :--- | :--- | :--- |
| **"Vùng chặn đáy" của thời lượng** | Hầu hết các chấm tròn đều nằm **trên mốc 20 phút** (rất hiếm trận dưới 20p). | Rất nhiều chấm tròn rơi sát xuống **mốc 15 - 18 phút**. |
| **Lý do chiến thuật** | Tuyển thủ chuyên nghiệp **không bao giờ đầu hàng sớm** và phòng ngự rất kỷ luật. Đội dẫn tiền bắt buộc phải chờ **Baron xuất hiện lúc 20 phút** mới đủ sức công phá nhà lính để kết thúc trận. | Solo Rank có cơ chế **Đầu Hàng Sớm (FF15)**. Khi bị dẫn quá 2,500g lúc 10 phút, người chơi dễ nản lòng và bấm /ff để chuyển sang trận mới. |
| **Độ gom cụm của dữ liệu** | Các chấm tròn gom sát đường màu đỏ (ít trận bị lệch quá xa). | Các chấm tròn phân tán lung tung (nhiều trận dẫn 3,000g nhưng vẫn bị kéo dài tới 40p do quăng game/bắt lẻ). |

---

## 4. TẠI SAO Ở SOLO RANK VẪN CÓ TRẬN KẾT THÚC DƯỚI CẢ MỐC 15 PHÚT (11 - 13 PHÚT)?

Trong dữ liệu thực tế có một số ít trận kết thúc ở phút 11 - 13 do 2 cơ chế đặc thù:
1. **Cơ chế Đầu Hàng Sớm Do AFK (AFK Early Surrender):**
   * Nếu có người chơi mất kết nối/AFK từ phút thứ 3 đến phút thứ 8, hệ thống cho phép biểu quyết đầu hàng ngay từ phút 10:00 - 10:30, trận đấu kết thúc ở phút 11 - 12.
2. **Văn hóa "Open Mid" ở Rank Cao (Hàn Quốc & Thách Đấu VN):**
   * Khi bị dẫn quá nặng lúc 10 phút, cả đội đồng lòng đứng trong hồ máu mở đường giữa cho đối thủ đẩy thẳng phá nát Nhà Chính lúc phút 12 - 13.
3. **Tính toàn vẹn dữ liệu:**
   * Các trận này đã được chơi đầy đủ qua mốc 10 phút (có chỉ số kinh tế thực tế), nên được giữ lại để phản ánh đúng tính chất khốc liệt của Solo Rank.

---

## 5. Ý NGHĨA BỔ TRỢ CHO KIỂM ĐỊNH THỐNG KÊ (TASK 2.2)

* Biểu đồ Fig 4 là minh chứng trực quan hoàn hảo cho kết quả kiểm định **Welch's t-test ở Task 2.2**: Chứng minh trận Solo Rank kết thúc nhanh hơn Đấu Giải trung bình **5.3 phút** với độ tin cậy tuyệt đối (p-value < 10^-26).
