# HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
## KHOA CÔNG NGHỆ THÔNG TIN
### BÀI TẬP LỚN GIỮA KỲ: NHẬP MÔN KHOA HỌC DỮ LIỆU
**Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
**Học kỳ:** II - Năm học 2025 - 2026  

---

# BÁO CÁO NGHIÊN CỨU & THỰC NGHIỆM KHOA HỌC DỮ LIỆU
## CHỦ ĐỀ 2: PHÁT HIỆN VÀ XỬ LÝ ĐIỂM NGOẠI LAI TRONG PHÂN TÍCH DỮ LIỆU (OUTLIER DETECTION & HANDLING)
### Nghiên cứu thực nghiệm trên 2,304 ván đấu Thể thao Điện tử Chuyên nghiệp LMHT 2026 (LCK, LPL, MSI, EWC)

---

## THÔNG TIN NHÓM THỰC HIỆN
- **Đề tài:** Phát hiện và Xử lý Điểm Ngoại Lai (Outlier Detection)
- **Tập dữ liệu ứng dụng:** Chênh lệch Tài nguyên Phút 10 (Early Game Metrics) trong Giải Đấu Chuyên Nghiệp Liên Minh Huyền Thoại 2026.
- **Sinh viên thực hiện:**
  - Họ và tên: [Điền họ và tên]
  - Mã sinh viên: [Điền MSSV]
  - Lớp: [Điền mã lớp sinh viên]

---

## TÓM TẮT NỘI DUNG (ABSTRACT)
Điểm ngoại lai (Outliers) là một trong những thách thức cốt lõi trong quy trình phân tích và khai phá dữ liệu (Data Mining & Data Science). Sự hiện diện của các giá trị cực trị không chỉ bóp méo các đại lượng đo lường vị trí trung tâm (Mean) và độ biến thiên (Standard Deviation) mà còn làm sai lệch giả định phân phối chuẩn của nhiều mô hình học máy. Báo cáo này trình bày cơ sở lý thuyết toàn diện về khái niệm ngoại lai, phân biệt rạch ròi giữa ngoại lai thực sự (True Outliers) và dữ liệu dị thường do sai sót thu thập (Erroneous Data), đồng thời phân tích các nguyên nhân hình thành. 

Về mặt thực nghiệm, báo cáo tiến hành một nghiên cứu đối sánh thực tế trên **2,304 ván đấu chuyên nghiệp đỉnh cao LMHT mùa giải 2026** (trích xuất từ các giải đấu LCK, LPL, LCP, EWC, MSI). Ba phương pháp phát hiện ngoại lai được triển khai và kiểm chứng: **Khoảng tứ phân vị (IQR)**, **Điểm số tiêu chuẩn (Z-Score)**, và **Mô hình học máy không giám sát Isolation Forest**. Kết quả chỉ ra rằng Z-Score (|Z| > 3.0) cực kỳ bảo thủ (chỉ gắn cờ 2 điểm - 0.09%) do chính các giá trị cực trị đã thổi phồng độ lệch chuẩn mẫu; trong khi IQR phát hiện 23 điểm (1.00%) và bảo vệ phân phối tốt hơn. Phân tích định lượng cũng chứng minh rằng việc loại bỏ thô bạo (Trimming) làm tổn thất thông tin của những trận đấu kinh điển "lăn cầu tuyết", và phương pháp **Cắt ngọn phân vị (Winsorization 1% - 99%)** là giải pháp tối ưu nhất khi vừa kiểm soát được phương sai vừa giữ nguyên 100% kích thước mẫu và tính trung thực của dữ liệu thể thao điện tử.

---

## 1. TỔNG QUAN VỀ ĐIỂM NGOẠI LAI (OUTLIERS)

### 1.1. Khái niệm Điểm ngoại lai
Theo định nghĩa kinh điển của Hawkins (1980), *một điểm ngoại lai (Outlier) là một quan sát sai lệch quá nhiều so với các quan sát khác trong cùng tập dữ liệu, đến mức làm nảy sinh nghi ngờ rằng nó được tạo ra bởi một cơ chế hoàn toàn khác biệt*. 

Trong khoa học dữ liệu, ngoại lai không đơn thuần là "nhiễu" (noise) cần phải xóa bỏ. Ngoại lai mang hai bản chất đối lập:
1. **Ngoại lai có giá trị phát hiện tri thức (Informative Outliers):** Phản ánh các hiện tượng đặc biệt, đột biến hiếm gặp nhưng hoàn toàn có thật trong thế giới thực (ví dụ: giao dịch gian lận ngân hàng, phát hiện hạt hạ nguyên tử mới, hoặc một trận đấu LMHT mà một đội out-play toàn diện dẫn trước hơn 3,500 vàng ở phút thứ 10).
2. **Ngoại lai phi giá trị (Harmful Noise):** Gây nhiễu tín hiệu thống kê, làm mô hình hồi quy bị lệch trọng số hoặc làm thuật toán phân cụm bị méo mó tâm cụm.

### 1.2. Phân biệt Ngoại lai (Outliers) và Dữ liệu Sai hỏng (Erroneous Data / Data Anomalies)
Đây là ranh giới sống còn trong tiền xử lý dữ liệu (Data Preprocessing):

| Tiêu chí | Điểm Ngoại Lai Thực Sự (True Outliers) | Dữ liệu Sai hỏng (Erroneous Data) |
| :--- | :--- | :--- |
| **Bản chất** | Giá trị cực trị nhưng **hợp lệ và có thực** trong không gian biến thiên của thực tế. | Giá trị **phi lý, sai lệch** do lỗi kỹ thuật hoặc quá trình ghi nhận. |
| **Nguồn gốc** | Tính biến động tự nhiên cực đoan (Natural Variability) hoặc sự kiện ngoại lệ. | Lỗi cảm biến, gõ nhầm (human error), lỗi trích xuất API, ván đấu bị lỗi mạng/AFK/Remake. |
| **Ví dụ trong LMHT** | Một đội dẫn trước +3,580 vàng lúc 10 phút do khai thác triệt để sai lầm đối phương và ăn trọn Trụ đầu. | Trận đấu kéo dài 2 phút do lỗi mạng (Remake) nhưng hệ thống vẫn ghi nhận chỉ số vàng 0. |
| **Chiến lược xử lý** | Giữ lại, biến đổi log, hoặc dùng phương pháp bền vững (Winsorization, Robust Scaling). | **Bắt buộc loại bỏ hoặc hiệu đính** ngay từ bước làm sạch dữ liệu ban đầu (Data Cleaning). |

---

## 2. NGUYÊN NHÂN PHÁT SINH NGOẠI LAI TRONG DỮ LIỆU

Các nguyên nhân phổ biến sinh ra điểm ngoại lai trong khoa học dữ liệu gồm:
1. **Lỗi con người trong quá trình nhập liệu (Data Entry Errors):** Gõ nhầm dấu phẩy, thêm chữ số 0 thừa (ví dụ nhập 100,000 thay vì 10,000).
2. **Lỗi thiết bị đo lường và hệ thống (Measurement / System Faults):** Cảm biến phần cứng bị chập, mạng rớt gói tin dẫn đến giá trị NULL hoặc đột biến vô lý.
3. **Lỗi tích hợp và chuyển đổi dữ liệu (Data Pipeline / ETL Pipeline Bugs):** Sai lệch đơn vị đo lường (ví dụ pha trộn giữa mét và feet, giây và mili-giây).
4. **Biến động tự nhiên từ bản chất hiện tượng (Natural Variation / Heavy-tailed Distributions):** Phổ biến trong kinh tế học, tài chính và thể thao điện tử, nơi dữ liệu tuân theo quy luật lũy thừa (Power Law) hoặc phân phối đuôi dày (Heavy-tailed) hơn là phân phối chuẩn Gauss thuần túy.

Trong dữ liệu thi đấu thể thao điện tử Liên Minh Huyền Thoại (LoL Esports), ngoại lai phút thứ 10 thường xuất phát từ:
- Đột biến cấp độ 1 (Level 1 Invade bẫy thành công) dẫn tới 3-4 mạng hạ gục ngay trước khi lính xuất hiện.
- Chiến thuật đảo đường (Lane Swap) khai thác thành công ăn trọn 5 lớp giáp trụ và sâu Hư Không (Voidgrubs).
- Đẳng cấp chênh lệch giữa hai đội tuyển tại các giải đấu quốc tế vòng khởi động (Play-in stage).

---

## 3. CÁC PHƯƠNG PHÁP PHÁT HIỆN NGOẠI LAI (OUTLIER DETECTION TECHNIQUES)

### 3.1. Phương pháp Khoảng Tứ Phân Vị (Interquartile Range - IQR)
IQR là kỹ thuật phi tham số (Non-parametric) dựa trên xếp hạng vị trí, được giới thiệu bởi nhà thống kê John Tukey:
- **Tứ phân vị thứ nhất (Q1):** Điểm phân vị thứ 25.
- **Tứ phân vị thứ ba (Q3):** Điểm phân vị thứ 75.
- **Khoảng tứ phân vị:** `IQR = Q3 - Q1`.
- **Ngưỡng chặn dưới (Lower Bound):** `Threshold_Low = Q1 - 1.5 * IQR`.
- **Ngưỡng chặn trên (Upper Bound):** `Threshold_High = Q3 + 1.5 * IQR`.

**Đánh giá:**
- *Ưu điểm:* Cực kỳ bền vững (Robust) trước các giá trị cực trị vì tứ phân vị không bị kéo lệch bởi đuôi phân phối. Không đòi hỏi dữ liệu phải tuân theo phân phối chuẩn.
- *Nhược điểm:* Ngưỡng hệ số 1.5 mang tính kinh nghiệm (Heuristic); có thể gắn cờ nhầm nếu dữ liệu có đuôi phân phối dài tự nhiên.

### 3.2. Phương pháp Điểm Tiêu Chuẩn (Z-Score)
Z-Score đo lường khoảng cách từ một điểm dữ liệu đến giá trị trung bình theo đơn vị độ lệch chuẩn:
- Công thức: `Z = (X - Mean) / Std`
- Quy tắc nhận diện ngoại lai: Một điểm bị coi là ngoại lai nếu `|Z| > 3.0` (ngưỡng 3-sigma).

**Đánh giá:**
- *Ưu điểm:* Dựa trên nền tảng toán học chặt chẽ của phân phối Gauss. Dễ tính toán và biểu diễn.
- *Nhược điểm:* **Rất dễ bị tổn thương bởi hiệu ứng che khuất (Masking Effect).** Bản thân giá trị trung bình (Mean) và độ lệch chuẩn (Std) bị bóp méo nghiêm trọng bởi chính các ngoại lai cực lớn, làm cho mẫu số `Std` bị phình to, dẫn đến điểm Z-Score bị co lại và bỏ sót nhiều ngoại lai rõ ràng.

### 3.3. Phương pháp Rừng Cô Lập (Isolation Forest) - Mở rộng nâng cao
Isolation Forest (Liu et al., 2008) là thuật toán học máy không giám sát dựa trên cấu trúc cây nhị phân:
- Giả thuyết cốt lõi: Ngoại lai là những điểm "ít và khác biệt" (few and different), do đó chúng rất dễ bị cô lập sâu trong không gian thuộc tính với số lần phân nhánh ngẫu nhiên ít hơn nhiều so với các điểm bình thường.
- *Ưu điểm:* Xử lý tốt dữ liệu đa chiều (Multivariate), không phụ thuộc giả định phân phối chuẩn, độ phức tạp tính toán tuyến tính `O(n)`.
- *Nhược điểm:* Cần xác định tham số tỷ lệ nhiễm bẩn (`contamination`) từ trước.

---

## 4. THIẾT KẾ THỰC NGHIỆM TRÊN DỮ LIỆU ĐẤU GIẢI LMHT 2026

### 4.1. Dữ liệu thực nghiệm
- **Nguồn trích xuất:** Cơ sở dữ liệu thi đấu giải đấu chuyên nghiệp 2026 (`clean_tournament_10min.csv`).
- **Phạm vi giải đấu:** Các giải đấu Tier-1 hàng đầu thế giới: LCK (Hàn Quốc), LPL (Trung Quốc), LCP (Châu Á - Thái Bình Dương), MSI (Mid-Season Invitational), EWC (Esports World Cup).
- **Cỡ mẫu nghiên cứu:** $N = 2,304$ ván đấu độc lập (quan sát phía Đội Xanh).
- **Biến số nghiên cứu chính (Univariate):** `golddiffat10` (Chênh lệch vàng giữa 2 đội tại phút thứ 10).
- **Biến phụ trợ phân tích đa chiều (Bivariate):** `xpdiffat10` (Chênh lệch điểm kinh nghiệm tại phút 10).

### 4.2. Thống kê mô tả tập dữ liệu ban đầu
- **Cỡ mẫu (N):** 2,304 ván đấu
- **Giá trị trung bình (Mean):** +98.37 vàng (Đội Xanh có lợi thế nhẹ)
- **Trung vị (Median):** +86.00 vàng
- **Độ lệch chuẩn (Std Dev):** 1,171.80 vàng
- **Khoảng giá trị (Range):** [-3,606.0 vàng, +3,580.0 vàng]
- **Độ lệch (Skewness):** 0.0616 (gần đối xứng)
- **Độ nhọn (Kurtosis):** -0.0220 (gần phân phối chuẩn chuẩn tắc)

---

## 5. KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH ĐỐI SÁNH

### 5.1. Kết quả nhận diện ngoại lai giữa các phương pháp
Triển khai mã nguồn độc lập trên bộ dữ liệu thu được kết quả:

| Thuật toán | Ngưỡng xác định | Số điểm ngoại lai phát hiện | Tỷ lệ ngoại lai (%) |
| :--- | :--- | :---: | :---: |
| **IQR (1.5 x IQR)** | [-2,961.2 vàng, +3,136.8 vàng] | **23** | **1.00%** |
| **Z-Score (|Z| > 3.0)** | [-3,417.0 vàng, +3,613.8 vàng] | **2** | **0.09%** |
| **Isolation Forest (Contam=0.03)** | Điểm bất thường (Anomaly Score) < 0 | **70** | **3.04%** |

### 5.2. Hiện tượng Che khuất (Masking Effect) của Z-Score
Đối chiếu chi tiết giữa IQR và Z-Score:
- Số điểm **cả 2 phương pháp cùng gắn cờ:** 2 điểm (ván đấu có chênh lệch vàng cực đại: -3,606 vàng và +3,580 vàng).
- Số điểm **chỉ có IQR gắn cờ nhưng Z-Score bỏ sót:** **21 điểm** (các ván có chênh lệch trong khoảng 2,960 đến 3,400 vàng).
- Số điểm chỉ có Z-Score gắn cờ: 0 điểm.

*Giải thích hiện tượng:* Các trận đấu dẫn trước hơn 3,000 vàng lúc 10 phút kéo giãn độ lệch chuẩn mẫu lên mức 1,171.80 vàng. Khi nhân hệ số $3 \times \text{Std}$, ngưỡng biên của Z-Score bị đẩy lên tới $\approx \pm 3,500$ vàng. Điều này khiến Z-Score trở nên "quá trơ" và bỏ sót hoàn toàn 21 ván đấu có mức chênh lệch tài nguyên áp đảo phi thường. Ngược lại, IQR dựa trên phân vị $Q_1$ và $Q_3$ hoàn toàn miễn nhiễm với sự thổi phồng này.

*(Xem Hình minh họa 1: `fig1_outlier_detection_iqr_zscore.png` và Hình 3: `fig3_scatter_multivariate_outliers.png`)*

---

## 6. ĐÁNH GIÁ TÁC ĐỘNG CỦA CÁC CHIẾN LƯỢC XỬ LÝ NGOẠI LAI

Nghiên cứu so sánh 4 kịch bản can thiệp lên tập dữ liệu:
1. **Gốc (Retaining / Raw Data):** Giữ nguyên toàn bộ 2,304 ván đấu.
2. **Loại bỏ theo IQR (Trimming IQR):** Xóa bỏ 23 quan sát vượt ngưỡng IQR.
3. **Loại bỏ theo Z-Score (Trimming Z-Score):** Xóa bỏ 2 quan sát vượt ngưỡng $|Z| > 3.0$.
4. **Cắt ngọn phân vị (Winsorization 1% - 99%):** Giữ nguyên kích thước mẫu, thay thế các giá trị $< 1\%$ và $> 99\%$ bằng giá trị tại phân vị thứ 1 và thứ 99.

### Bảng Tổng hợp Tác động Lên Các Thước Đo Thống Kê:

| Chiến lược xử lý | Cỡ mẫu (N) | Tỷ lệ giữ mẫu (%) | Mean (Trung bình) | Std (Độ lệch chuẩn) | Δ Std so với Gốc (%) | Skewness | Min (vàng) | Max (vàng) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gốc (Raw / Retaining)** | 2,304 | 100.00% | +98.37 | 1,171.80 | 0.00% | 0.0616 | -3,606.0 | +3,580.0 |
| **Loại bỏ IQR (Trimming)** | 2,281 | 99.00% | +97.43 | 1,130.64 | **-3.51%** | 0.0727 | -2,947.0 | +3,098.0 |
| **Loại bỏ Z-Score (Trimming)** | 2,302 | 99.91% | +101.58 | 1,167.24 | **-0.39%** | 0.0817 | -3,374.0 | +3,580.0 |
| **Cắt ngọn (Winsorization 1%-99%)** | **2,304** | **100.00%** | **+98.84** | **1,156.90** | **-1.27%** | **0.0727** | **-2,702.0** | **+2,921.0** |

### Nhận xét chuyên sâu:
1. **Tác động lên Độ lệch chuẩn (Std Dev):**
   - Loại bỏ theo IQR làm giảm độ lệch chuẩn tới 3.51% (từ 1,171.8 xuống 1,130.64), nén chặt không gian dữ liệu.
   - Loại bỏ theo Z-Score gần như không làm thay đổi biến thiên mẫu (-0.39%) vì chỉ loại vỏn vẹn 2 trận đấu.
   - Winsorization kéo giảm độ biến thiên ở mức vừa phải (-1.27%), giúp triệt tiêu rủi ro phương sai lớn mà không làm mất mẫu.
2. **Tác động lên Giá trị Trung bình (Mean):**
   - Do phân phối chênh lệch vàng khá cân bằng giữa hai phía thắng/thua, giá trị Mean chỉ dao động trong khoảng +97 đến +101 vàng. Tuy nhiên, nếu phân phối lệch hẳn về một phía (như tỷ lệ mạng hạ gục hay sát thương), việc loại bỏ thô bạo sẽ dịch chuyển Mean một cách nguy hiểm.

*(Xem Hình minh họa 2: `fig2_distribution_before_after.png` và Hình 4: `fig4_statistical_impact_comparison.png`)*

---

## 7. KHUYẾN NGHỊ CHIẾN LƯỢC XỬ LÝ NGOẠI LAI (RECOMMENDATIONS)

Dựa trên kết quả thực nghiệm, báo cáo đúc kết hướng dẫn hành động cho các nhà khoa học dữ liệu:

1. **Khi nào nên Giữ lại (Retaining):**
   - Áp dụng khi mục tiêu nghiên cứu là khám phá các sự kiện hiếm (Anomaly Detection, Fraud Detection, hoặc phân tích chiến thuật "lăn cầu tuyết" cực đại trong Esports). Các trận đấu ngoại lai phản ánh đỉnh cao chiến thuật thực sự, việc xóa bỏ chúng là hành vi phá hủy tri thức.
2. **Khi nào nên Loại bỏ (Trimming):**
   - Chỉ áp dụng khi ngoại lai được xác định rõ ràng là **Dữ liệu sai hỏng (Erroneous Data)** (ví dụ: ván đấu Remake $<10$ phút, trận đấu có người chơi mất kết nối, lỗi ghi nhận của API). Tuyệt đối không Trimming tùy tiện đối với True Outliers vì sẽ làm giảm sức mạnh thống kê (Statistical Power) và làm sai lệch cỡ mẫu $N$.
3. **Khi nào nên Cắt ngọn (Winsorizing):**
   - **Đây là giải pháp khuyến nghị hàng đầu trong bài toán hồi quy hoặc huấn luyện mô hình học máy (Machine Learning).** Winsorization giúp bảo toàn chính xác kích thước tập dữ liệu ($N = 2,304$), chặn đứng ảnh hưởng của các giá trị cực đoan lên hàm mất mát (Loss Function như MSE), đồng thời duy trì cấu trúc phân phối ổn định.
4. **Khi nào nên Biến đổi dữ liệu (Transforming):**
   - Khi dữ liệu có độ lệch lớn và mang tính chất nhân tính (Multiplicative), việc áp dụng Log-transform hoặc Box-Cox / Yeo-Johnson transform sẽ đưa phân phối về gần chuẩn tắc mà không cần phải loại bỏ bất kỳ quan sát nào.

---

## 8. KẾT LUẬN (CONCLUSION)
Thực nghiệm trên 2,304 trận đấu chuyên nghiệp LMHT mùa giải 2026 đã mang lại những bài học kinh nghiệm sâu sắc về bài toán phát hiện và xử lý ngoại lai:
- Không có một phương pháp phát hiện ngoại lai vạn năng; IQR vượt trội hơn Z-Score trong các tập dữ liệu có giá trị cực trị lớn nhờ tính chất bền vững.
- Rừng cô lập (Isolation Forest) là công cụ bổ trợ đắc lực khi phân tích mở rộng trên không gian đa chiều (Vàng kết hợp Kinh nghiệm và Mục tiêu lớn).
- Quyết định xử lý ngoại lai cần dựa trên sự am hiểu sâu sắc về ngữ cảnh nghiệp vụ (Domain Knowledge) thay vì mù quáng áp dụng các quy tắc toán học thô sơ. Chiến lược Winsorization thể hiện sự cân bằng hoàn hảo nhất giữa việc giữ trọn vẹn thông tin và ổn định hóa các mô hình phân tích định lượng.

---

## TÀI LIỆU THAM KHẢO (REFERENCES)
1. Hawkins, D. M. (1980). *Identification of Outliers*. Chapman and Hall, London.
2. Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
3. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). *Isolation Forest*. In 2008 Eighth IEEE International Conference on Data Mining (pp. 413-422). IEEE.
4. Rousseeuw, P. J., & Hubert, M. (2011). *Robust statistics for outlier detection*. Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery, 1(1), 73-79.
5. Oracle's Elixir (2026). *League of Legends Esports Match Data*. https://oracleselixir.com/
6. Riot Games API Documentation (2026). *LoL Match-v5 & Tournament Endpoints*. https://developer.riotgames.com/
