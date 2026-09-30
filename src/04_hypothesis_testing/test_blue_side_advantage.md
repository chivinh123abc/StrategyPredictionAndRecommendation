# BÁO CÁO KIỂM ĐỊNH THỐNG KÊ: LỢI THẾ PHE XANH (BLUE SIDE ADVANTAGE)

> **Mã Task:** Task 2.1 [Thành viên 2]  
> **File code thực thi:** [`test_blue_side_advantage.py`](test_blue_side_advantage.py)  
> **Giáo trình:** Chương 1 - Thống kê suy diễn & Kiểm định giả thuyết (TS. Thái Tuyết Hải - PTIT)  
> **File kết quả xuất ra:** [`data/processed/hypothesis_test_1_blue_side.csv`](../../data/processed/hypothesis_test_1_blue_side.csv)  
> **Môi trường thực thi:** Python 3.13 (`.venv`)

---

## 📌 1. MỤC TIÊU & CƠ SỞ BÀI TOÁN

Trong bộ môn Thể thao điện tử Liên Minh Huyền Thoại (League of Legends), người chơi và giới chuyên môn thường cho rằng **Đội Xanh (Blue Side)** sở hữu nhiều ưu thế hơn **Đội Đỏ (Red Side)** nhờ:
1. **Góc nhìn bản đồ (Camera Angle):** Góc nhìn chéo từ góc dưới bên trái hướng lên góc trên bên phải thuận mắt tự nhiên với tư thế điều khiển chuột của người chơi.
2. **Quyền chọn tướng đầu tiên (First Pick):** Được quyền khóa ngay vị tướng mạnh nhất (Power Pick / Meta Pick) của phiên bản.

**Câu hỏi nghiên cứu:**
> *"Liệu tỷ lệ thắng của Đội Xanh có thực sự vượt trội hơn Đội Đỏ một cách có ý nghĩa thống kê hay sự chênh lệch này chỉ là do biến thiên ngẫu nhiên?"*

---

## 📐 2. BỘ GIẢ THUYẾT VÀ CÔNG THỨC TOÁN THỐNG KÊ

### A. Thiết Lập Giả Thuyết (Hypotheses)
* **Mức ý nghĩa:** `alpha = 0.05` (Tương đương Độ tin cậy `95%`).
* **Ngưỡng tới hạn chuẩn:** `Z_critical = ±1.96` (Tra bảng phân phối chuẩn tắc `Normal(0, 1)`).

```text
Giả thuyết H0 (Giả thuyết Không - Null Hypothesis):
  p = 0.5  --> Tỷ lệ thắng của Phe Xanh bằng đúng 50% (Không có lợi thế đặc biệt).

Giả thuyết H1 (Giả thuyết Đối - Alternative Hypothesis):
  p != 0.5 --> Tỷ lệ thắng của Phe Xanh khác 50% (Tồn tại sự chênh lệch có ý nghĩa thống kê).
```

---

### B. Các Công Thức Tính Toán Chi Tiết

```text
1. Tỷ lệ thắng thực tế của mẫu (Sample Proportion):
   p_hat = (Số trận thắng của Phe Xanh) / (Tổng số trận n)

2. Sai số chuẩn dưới giả thuyết H0 (Standard Error under H0):
   SE_0 = Căn_bậc_hai( p_0 * (1 - p_0) / n )
        = Căn_bậc_hai( 0.5 * 0.5 / n )
        = 0.5 / Căn_bậc_hai(n)

3. Giá trị thống kê kiểm định Z (Z-score):
   Z = (p_hat - 0.5) / SE_0

4. Giá trị p-value kiểm định 2 phía (Two-tailed p-value):
   p_value = 2 * ( 1 - Phi( |Z| ) )
   (Trong đó Phi là hàm phân phối tích lũy chuẩn tắc CDF)

5. Khoảng tin cậy 95% (95% Confidence Interval - Wald Method):
   CI_95% = [ p_hat - 1.96 * SE_sample ,  p_hat + 1.96 * SE_sample ]
   Với SE_sample = Căn_bậc_hai( p_hat * (1 - p_hat) / n )
```

---

### C. Quy Tắc Quyết Định (Decision Rule)
* **BÁC BỎ H0** nếu `p_value < 0.05` (hoặc `|Z| > 1.96`): Sự chênh lệch tỷ lệ thắng là **CÓ Ý NGHĨA THỐNG KÊ** (Statistically Significant).
* **CHƯA ĐỦ BẰNG CHỨNG BÁC BỎ H0** nếu `p_value >= 0.05` (hoặc `-1.96 <= Z <= +1.96`): Chưa thể khẳng định có lợi thế phe, chênh lệch có thể do ngẫu nhiên.

---

## 📊 3. BẢNG KẾT QUẢ KIỂM ĐỊNH THỰC NGHIỆM

Số liệu được tính toán trực tiếp từ CSDL [`lol_live_data.db`](../../data/database/lol_live_data.db):

| Tập Dữ Liệu Phân Tích | Cỡ Mẫu (n) | Blue Thắng | Tỷ Lệ Thắng | Điểm Z (Z-score) | Chỉ Số p-value | Khoảng Tin Cậy 95% | Kết Luận (alpha = 0.05) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Toàn Bộ Đấu Giải (Pro Play)** | **3,000** | **1,605** | **53.50%** | **+3.8341** | **0.000126 (***)** | **[51.72% đến 55.28%]** | ✅ **BÁC BỎ H0** (Lợi thế Blue rõ rệt) |
| **2. Toàn Bộ Solo Rank (VN2 & KR)**| **1,009** | **459** | **45.49%** | **-2.8648** | **0.004173 (**)** | **[42.42% đến 48.56%]** | ✅ **BÁC BỎ H0** (Phe Đỏ thắng 54.51%) |
| *2a. Solo Rank Việt Nam (VN2)* | 550 | 259 | 47.09% | -1.3645 | 0.1724 | [42.92% đến 51.26%] | ❌ Chưa đủ bằng chứng bác bỏ H0 |
| *2b. Solo Rank Hàn Quốc (KR)* | 459 | 200 | 43.57% | -2.7539 | 0.0059 (**) | [39.04% đến 48.11%] | ✅ **BÁC BỎ H0** (Phe Đỏ áp đảo tại KR) |
| *3. Giải Đấu LCP (Châu Á - TBD)* | 466 | 257 | 55.15% | +2.2236 | 0.0262 (*) | [50.63% đến 59.67%] | ✅ **BÁC BỎ H0** (Blue thắng áp đảo) |
| *3. Giải Quốc Tế MSI* | 151 | 89 | 58.94% | +2.1972 | 0.0280 (*) | [51.09% đến 66.79%] | ✅ **BÁC BỎ H0** (First Pick quá mạnh) |
| *3. Giải Đấu LPL (Trung Quốc)* | 1,160 | 612 | 52.76% | +1.8791 | 0.0602 | [49.89% đến 55.63%] | ⚖️ Tiệm cận ngưỡng (Ý nghĩa ở mức 10%) |
| *3. Giải Đấu LCK (Hàn Quốc)* | 850 | 449 | 52.82% | +1.6464 | 0.0997 | [49.47% đến 56.18%] | ⚖️ Tiệm cận ngưỡng (Ý nghĩa ở mức 10%) |
| *3. Giải Đấu EWC (Esports World Cup)*| 265 | 143 | 53.96% | +1.2900 | 0.1970 | [47.96% đến 59.96%] | ❌ Chưa đủ bằng chứng bác bỏ H0 |
| *3. Giải Vô Địch Thế Giới (Worlds)* | 108 | 55 | 50.93% | +0.1925 | 0.8474 | [41.50% đến 60.35%] | ❌ Chưa đủ bằng chứng bác bỏ H0 |

> 📌 **Quy ước mức ý nghĩa thống kê:**
> * `***` : `p < 0.001` (Bác bỏ cực kỳ rõ rệt / Highly Significant).
> * `**`  : `p < 0.01` (Bác bỏ mạnh).
> * `*`   : `p < 0.05` (Bác bỏ có ý nghĩa thống kê).

---

## 🧠 4. PHÂN TÍCH CHUYÊN SÂU THEO NGHIỆP VỤ LMHT (DOMAIN KNOWLEDGE)

### 🔹 1. Tại Đấu Giải Chuyên Nghiệp (Pro Play): Lợi Thế First Pick Quyết Định Trận Đấu
* Winrate Phe Xanh đạt **53.50%** với `p-value = 0.000126` (Xác suất xảy ra do ngẫu nhiên chỉ là 0.0126%).
* **Nguyên nhân cốt lõi:**
  1. **Quyền First Pick (Chọn 1):** Trong thi đấu chuyên nghiệp đỉnh cao, Meta luôn tồn tại 3 - 4 vị tướng có sức mạnh vượt trội (S-Tier như Varus, Orianna, Vi, Rumble). Đội Xanh luôn chắc chắn chọn được ít nhất 1 vị tướng lỗi nhất giải đấu.
  2. **Góc nhìn Camera chuẩn:** Góc nhìn từ góc dưới bên trái lên góc trên bên phải giúp tuyển thủ căn chỉnh kỹ năng định hướng (Skillshots) dễ dàng và quan sát thế lính tốt hơn.

---

### 🔹 2. Tại Đấu Solo Rank Thách Đấu: Thuật Toán Cân Bằng Của Riot Games (Matchmaking)
* Ngược lại, tại Rank Đơn, Winrate Phe Xanh chỉ đạt **45.49%**, trong khi Phe Đỏ lại thắng tới **54.51%** (`p-value = 0.004173 < 0.01`).
* **Nguyên nhân cốt lõi:**
  * **Cơ chế cân bằng điểm ẩn MMR (Matchmaking Rating):** Vì nhà phát hành Riot Games biết rõ Đội Xanh có lợi thế địa hình và góc nhìn, nên hệ thống ghép trận của Riot được lập trình để **luôn xếp đội có tổng điểm MMR/Elo trung bình cao hơn sang Phe Đỏ (Red Side)**.
  * Trong môi trường Solo Queue (nơi việc phối hợp chiến thuật đội hình không chặt chẽ bằng đấu giải), kỹ năng cá nhân và trình độ tay to (Elo cao hơn) của Phe Đỏ đã lấn át lợi thế bản đồ của Phe Xanh.

---

## 💻 5. GIẢI THÍCH MÃ NGUỒN (CODE ARCHITECTURE)

File code [`test_blue_side_advantage.py`](test_blue_side_advantage.py) được thiết kế theo hướng đối tượng (OOP) gồm Class `BlueSideHypothesisTester`:

1. **Khởi tạo (`__init__`):**
   * Nhận `db_path` trỏ đến SQLite và mức ý nghĩa `alpha = 0.05`.
   * Tính toán tự động giá trị `z_critical` qua hàm `scipy.stats.norm.ppf(1 - alpha/2)`.
2. **Hàm tính toán lõi (`compute_z_test`):**
   * Nhận `wins`, `total` và tính toán `p_hat`, `se_0`, `z_score`, `p_value` (dùng `scipy.stats.norm.cdf`), và khoảng tin cậy 95% `CI_95%`.
3. **Hàm chạy toàn bộ (`run_tests`):**
   * Kết nối SQLite, truy vấn bảng `tournament_matches` và `matches_10min`.
   * Thực hiện Z-test trên từng phân vùng dữ liệu và đóng gói kết quả vào `pd.DataFrame`.
4. **Hàm xuất báo cáo (`display_report`):**
   * In bảng kết quả định dạng terminal đẹp mắt kèm phân tích nghiệp vụ chuyên sâu.
   * Tự động xuất file CSV ra thư mục `data/processed/hypothesis_test_1_blue_side.csv`.

---

## 🚀 6. HƯỚNG DẪN CHẠY LỆNH (HOW TO RUN)

Chạy script từ thư mục gốc dự án qua môi trường ảo `.venv`:

```powershell
# Chạy kiểm định với mức ý nghĩa mặc định alpha = 0.05
.\.venv\Scripts\python.exe src/04_hypothesis_testing/test_blue_side_advantage.py

# Chạy với mức ý nghĩa tùy chọn (ví dụ: alpha = 0.01)
.\.venv\Scripts\python.exe src/04_hypothesis_testing/test_blue_side_advantage.py --alpha 0.01
```
