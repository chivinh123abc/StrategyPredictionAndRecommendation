# BÀI THUYẾT TRÌNH GIỮA KỲ: NHẬP MÔN KHOA HỌC DỮ LIỆU
## CHỦ ĐỀ 2: PHÁT HIỆN VÀ XỬ LÝ ĐIỂM NGOẠI LAI (OUTLIER DETECTION & HANDLING)
**Giảng viên:** TS. Thái Tuyết Hải  
**Thực hiện:** [Họ và tên sinh viên] - [MSSV]  
**Quy mô thực nghiệm:** 2,304 Ván Đấu Đỉnh Cao LMHT Pro Play 2026 (LCK, LPL, MSI, EWC)

---

## SLIDE 1: TRANG TIÊU ĐỀ
- **Tên đề tài:** Nghiên cứu & Thực nghiệm Các Phương pháp Phát hiện Ngoại lai trong Dữ liệu Thể thao Điện tử.
- **Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science)
- **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**
- **Nhóm sinh viên thực hiện:** [Điền họ tên & MSSV]

---

## SLIDE 2: MỤC TIÊU NGHIÊN CỨU & CÂU HỎI CỐT LÕI
- **Mục tiêu chính:**
  1. Thấu hiểu bản chất toán học và ý nghĩa thống kê của Điểm Ngoại Lai (Outliers).
  2. Phân biệt ranh giới giữa *Ngoại lai thực sự* (True Outliers) và *Dữ liệu sai hỏng* (Erroneous Data).
  3. Đánh giá ưu - nhược điểm của các thuật toán: IQR, Z-Score, Isolation Forest.
  4. Thực nghiệm định lượng trên tập dữ liệu thực tế 2,304 trận đấu LMHT Pro Play 2026.
  5. Đưa ra cẩm nang chiến lược: Khi nào Giữ lại, Loại bỏ hay Cắt ngọn (Winsorize)?

---

## SLIDE 3: BẢN CHẤT NGOẠI LAI & PHÂN BIỆT VỚI DỮ LIỆU SAI HỎNG
- **Định nghĩa (Hawkins, 1980):** Một quan sát sai lệch quá xa so với phần còn lại, gợi ý cơ chế phát sinh khác biệt.
- **Ngoại lai thực sự (True Outliers):**
  - Hiện tượng cực đoan nhưng hoàn toàn hợp lệ trong thực tế.
  - *Ví dụ:* Một đội out-play áp đảo, dẫn trước 3,580 vàng lúc 10 phút.
  - *Ý nghĩa:* Mang giá trị tri thức cao, phản ánh đỉnh cao chiến thuật lăn cầu tuyết.
- **Dữ liệu sai hỏng (Erroneous Data):**
  - Giá trị phi lý do lỗi hệ thống, mất mạng, thiết bị đo hỏng hoặc ván đấu Remake.
  - *Hành động bắt buộc:* Phải lọc bỏ triệt để ở pha Data Cleaning, không được xem là Outlier để phân tích.

---

## SLIDE 4: NGUYÊN NHÂN PHÁT SINH NGOẠI LAI
- **Nhóm 1 - Lỗi kỹ thuật & Quy trình:** Lỗi nhập liệu, lỗi API, lỗi kết nối mạng.
- **Nhóm 2 - Bản chất của hệ thống phân tán & phức tạp:**
  - Quy luật đuôi dày (Heavy-tailed distribution) và hiệu ứng mạng (Network effects).
  - Trong Esports: Các pha bẫy Level 1 cướp rừng thành công, chiến thuật đảo đường (Lane Swap) phá hủy trụ sớm.
  - Sự chênh lệch trình độ giữa các khu vực thi đấu tại các kỳ CKTG / MSI.

---

## SLIDE 5: PHƯƠNG PHÁP 1: KHOẢNG TỨ PHÂN VỊ (IQR)
- **Cơ chế:** Dựa trên thứ bậc xếp hạng vị trí (Non-parametric):
  - $Q_1$ (Phân vị 25%), $Q_3$ (Phân vị 75%).
  - $IQR = Q_3 - Q_1$.
  - Ngưỡng an toàn: $[Q_1 - 1.5 \times IQR, \; Q_3 + 1.5 \times IQR]$.
- **Ưu điểm vượt trội:**
  - Cực kỳ bền vững (Robust), không bị méo mó bởi các giá trị cực trị.
  - Không cần giả định dữ liệu tuân theo phân phối chuẩn.
- **Nhược điểm:** Hệ số 1.5 mang tính kinh nghiệm (Rule of thumb).

---

## SLIDE 6: PHƯƠNG PHÁP 2: ĐIỂM SỐ TIÊU CHUẨN (Z-SCORE)
- **Cơ chế:** Dựa trên khoảng cách độ lệch chuẩn từ trung bình mẫu:
  - $Z = \frac{X - \mu}{\sigma}$.
  - Gắn cờ ngoại lai khi $|Z| > 3.0$ (Quy tắc 3-Sigma).
- **Điểm yếu chí mạng - Hiệu ứng Che khuất (Masking Effect):**
  - Bản thân $\mu$ và $\sigma$ bị chính các ngoại lai kéo lệch và phình to.
  - Mẫu số $\sigma$ quá lớn làm giá trị Z bị co lại, khiến Z-Score trở nên "quá trơ" và bỏ sót nhiều ngoại lai nghiêm trọng.

---

## SLIDE 7: PHƯƠNG PHÁP 3: RỪNG CÔ LẬP (ISOLATION FOREST - BONUS ML)
- **Cơ chế học máy không giám sát (Liu et al., 2008):**
  - Ngoại lai là những điểm "ít và khác biệt" trong không gian thuộc tính.
  - Dễ bị cô lập ở các tầng nông của cây nhị phân (Path length ngắn).
- **Lợi thế:**
  - Áp dụng xuất sắc cho dữ liệu đa chiều (Multivariate: Vàng + Kinh nghiệm + Mạng hạ gục).
  - Tốc độ tính toán tuyến tính $O(n)$, bắt trọn các điểm bất thường phức tạp.

---

## SLIDE 8: THIẾT KẾ THỰC NGHIỆM TRÊN 2,304 TRẬN LMHT PRO PLAY 2026
- **Tập dữ liệu:** 2,304 ván đấu Đội Xanh từ các giải đấu số 1 thế giới (LCK, LPL, LCP, EWC, MSI 2026).
- **Biến phân tích trọng tâm:** `golddiffat10` (Chênh lệch vàng phút 10).
- **Thống kê mô tả ban đầu:**
  - Trung bình (Mean): **+98.37 vàng**
  - Trung vị (Median): **+86.00 vàng**
  - Độ lệch chuẩn (Std): **1,171.80 vàng**
  - Khoảng giá trị: **[-3,606 vàng đến +3,580 vàng]**
  - Độ lệch (Skewness): **0.0616** | Độ nhọn (Kurtosis): **-0.0220** (tiệm cận phân phối chuẩn)

---

## SLIDE 9: KẾT QUẢ ĐỐI SÁNH: IQR vs Z-SCORE vs ISOLATION FOREST
*(Tham chiếu Biểu đồ Fig 1 & Fig 3)*

| Tiêu chí | IQR (1.5 x IQR) | Z-Score (|Z| > 3.0) | Isolation Forest |
| :--- | :---: | :---: | :---: |
| **Ngưỡng biên** | [-2,961g, +3,137g] | [-3,417g, +3,614g] | Anomaly Score < 0 |
| **Số lượng ngoại lai** | **23 ván (1.00%)** | **2 ván (0.09%)** | **70 ván (3.04%)** |
| **Độ nhạy (Sensitivity)** | Cao, bao quát tốt | Quá thấp (bị che khuất) | Rất nhạy trên đa chiều |

- **Phát hiện thú vị:** Z-Score bỏ sót tới 21 ván đấu lăn cầu tuyết cực lớn do độ lệch chuẩn bị đội lên 1,171.80 vàng. IQR chứng minh tính ưu việt vượt trội trong thực tế.

---

## SLIDE 10: TÁC ĐỘNG LÊN CÁC THƯỚC ĐO THỐNG KÊ (MEAN, STD, SKEWNESS)
*(Tham chiếu Biểu đồ Fig 2 & Fig 4)*

| Kịch bản xử lý | Cỡ mẫu (N) | Mean (vàng) | Std Dev (vàng) | Δ Std (%) | Skewness |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Dữ liệu Gốc (Retaining)** | 2,304 (100%) | +98.37 | 1,171.80 | 0.00% | 0.0616 |
| **2. Xóa bỏ IQR (Trimming)** | 2,281 (99.0%) | +97.43 | 1,130.64 | **-3.51%** | 0.0727 |
| **3. Xóa bỏ Z-Score (Trimming)**| 2,302 (99.9%) | +101.58 | 1,167.24 | **-0.39%** | 0.0817 |
| **4. Cắt ngọn (Winsorization 1%-99%)** | **2,304 (100%)**| **+98.84** | **1,156.90** | **-1.27%** | **0.0727** |

- **Kết luận định lượng:** Xóa bỏ (Trimming) làm mất 23 ván đấu giá trị; Cắt ngọn (Winsorization) giữ nguyên 100% cỡ mẫu và kiểm soát phương sai tối ưu nhất.

---

## SLIDE 11: BẢN ĐỒ CHIẾN LƯỢC XỬ LÝ NGOẠI LAI (DECISION FRAMEWORK)
1. **GIỮ NGUYÊN (RETAINING):**
   - Khi nghiên cứu chiến thuật lăn cầu tuyết, phát hiện gian lận hoặc phân tích tình huống hiếm.
2. **LOẠI BỎ (TRIMMING):**
   - Chỉ dùng khi chắc chắn là **Dữ liệu sai hỏng / Lỗi hệ thống (Erroneous Data)**. Tuyệt đối không xóa bừa bãi dữ liệu thật.
3. **CẮT NGỌN PHÂN VỊ (WINSORIZING - Khuyến nghị hàng đầu):**
   - Dùng khi chuẩn bị dữ liệu huấn luyện mô hình học máy (Hồi quy, Deep Learning) để tránh gradient bị bùng nổ mà vẫn giữ nguyên kích thước mẫu.
4. **BIẾN ĐỔI HÀM SỐ (TRANSFORMING):**
   - Dùng hàm Log, Box-Cox khi dữ liệu có độ lệch quá lớn và mang tính chất nhân tính.

---

## SLIDE 12: TỔNG KẾT & BÀI HỌC KINH NGHIỆM
- **Bài học 1:** Không có thuật toán ngoại lai vạn năng; IQR bền vững hơn Z-Score khi dữ liệu có biến thiên lớn.
- **Bài học 2:** Đừng bao giờ vội vàng "xóa" ngoại lai; ngoại lai thường chứa đựng những tri thức đột phá nhất.
- **Bài học 3:** Kết hợp kiến thức toán học thống kê với hiểu biết sâu sắc về nghiệp vụ (Domain Knowledge) là chìa khóa thành công của một nhà Khoa học Dữ liệu.
- **Lời cảm ơn:** Chân thành cảm ơn TS. Thái Tuyết Hải và các bạn đã lắng nghe bài thuyết trình!
