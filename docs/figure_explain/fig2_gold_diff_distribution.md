# GIẢI THÍCH CHI TIẾT FIG 2: PHÂN PHỐI CHÊNH LỆCH VÀNG LÚC 10 PHÚT (HISTOGRAM + KDE)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig2_gold_diff_distribution_kde.png`  
> **Chương giáo trình:** Chương 3 - Trực quan hóa dữ liệu khám phá (EDA)  
> **Nguồn dữ liệu:** Đấu Giải Chuyên Nghiệp (4,752 quan sát đội) vs Solo Rank Thách Đấu (2,018 quan sát đội) từ CSDL SQLite `lol_live_data.db`

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC

Biểu đồ Fig 2 trả lời 2 câu hỏi trọng tâm:
1. *"Hình dáng phân phối chênh lệch tiền giữa Đội Thắng và Đội Thua lúc 10 phút phân tách nhau rõ ràng như thế nào?"*
2. *"Có sự khác biệt gì về độ biến động và tính ổn định kiểm soát thế trận giữa Đấu Giải Chuyên Nghiệp (Pro Play) và Đấu Xếp Hạng Đơn (Solo Rank)?"*

---

## 2. CẤU TRÚC VÀ CÁC THÀNH PHẦN TRÊN BIỂU ĐỒ

Biểu đồ gồm 2 đồ thị con (Subplots) đặt cạnh nhau:
* **Bên Trái:** Đấu Giải Chuyên Nghiệp (Pro Play - 4,752 quan sát).
* **Bên Phải:** Solo Rank Thách Đấu (2,018 quan sát).

### Các yếu tố đồ họa:
1. **Trục hoành (Trục X):** Mức chênh lệch vàng lúc 10 phút (từ -6,000 vàng đến +6,000 vàng).
   * Giá trị Dương (+): Đang dẫn trước tiền đối thủ.
   * Giá trị Âm (-): Đang bị đối thủ dẫn tiền.
2. **Trục tung (Trục Y):** Mật độ / Tần suất số lượng trận đấu rơi vào mức chênh lệch đó.
3. **Màu sắc:**
   * **Màu Xanh Dương:** Phân phối của **Đội Thắng** chung cuộc.
   * **Màu Đỏ:** Phân phối của **Đội Thua** chung cuộc.
4. **Các đường kẻ dọc:**
   * **Đường nét đứt màu xám (ở giữa 0g):** Trận đấu đang cân bằng tuyệt đối về tiền lúc 10 phút.
   * **Đường nét liền Xanh:** Mức chênh lệch vàng trung bình của Đội Thắng (`+1,250g`).
   * **Đường nét liền Đỏ:** Mức chênh lệch vàng trung bình của Đội Thua (`-1,250g`).

---

## 3. CÁC PHÁT HIỆN KHOA HỌC & CHIẾN THUẬT QUAN TRỌNG

### A. Sự phân tách rõ rệt của tâm phân phối (+1,250g vs -1,250g)
* Tâm phân phối của Đội Thắng lệch hẳn sang bên phải (trung bình **+1,250 vàng**).
* Tâm phân phối của Đội Thua lệch hẳn sang bên trái (trung bình **-1,250 vàng**).
* **Ý nghĩa thực tế:** Mức dẫn trước từ **1,000 đến 1,500 vàng** ở phút thứ 10 (tương đương 1 trang bị thành phần lớn như Cuốc Chim, Kiếm B.F, Gậy Bùng Nổ) đã tạo ra ranh giới phân hóa cực kỳ rõ ràng giữa kẻ thắng và người thua.

### B. Đối chiếu Đấu Giải (Pro Play) vs Solo Rank (Thách Đấu)

| Đặc điểm | Đấu Giải Chuyên Nghiệp (Trái) | Solo Rank Thách Đấu (Phải) |
| :--- | :--- | :--- |
| **Hình dáng quả chuông** | Nhọn hơn, hẹp hơn, tập trung cao quanh mốc -1,500g đến +1,500g. | Bè ngang hơn, trải rộng sang 2 bên sườn. |
| **Hiện tượng cực đoan (Outliers)** | Rất hiếm khi có trận bị dẫn quá 4,000g ở phút thứ 10. | Xuất hiện nhiều trận bị dẫn cực lớn (vượt quá 4,000g đến 5,000g lúc 10 phút). |
| **Giải thích nguyên nhân** | Tuyển thủ chuyên nghiệp đánh kỷ luật, cắm mắt kiểm soát, khi thua đường biết ôm trụ thủ hòa chờ giao tranh tổng. | Người chơi Solo Rank đánh giao tranh liên tục, bắt lẻ nhiều, dễ bị "vỡ trận" do chênh lệch kỹ năng cá nhân. |

---

## 4. Ý NGHĨA ĐỐI VỚI BÁO CÁO MÔN HỌC (CHƯƠNG 1, 2, 3)

1. **Kiểm tra tính chuẩn của dữ liệu (Normality Check):**
   * Đường cong KDE (Kernel Density Estimation) cho thấy dữ liệu chênh lệch vàng ở cả 2 môi trường đều tuân theo **Phân phối Chuẩn (Gaussian Normal Distribution)** dạng hình chuông đối xứng.
   * Đây là tiền đề toán học hợp lệ để áp dụng các phép kiểm định tham số như **Z-test** và **Welch's t-test** ở Chương 1 (Task 2.1 & 2.2).
2. **Khẳng định tính phổ quát của ngưỡng Snowball:**
   * Dù là Đấu Giải kỷ luật hay Solo Rank tự do, ngưỡng chênh lệch **+1,250 vàng** lúc 10 phút đều là "điểm rơi sức mạnh" mang tính bước ngoặt đưa đội tuyển chạm tay vào chiến thắng.
