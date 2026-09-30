# BÁO CÁO TRỰC QUAN HÓA DỮ LIỆU EDA (EXPLORATORY DATA ANALYSIS)

> **Môn học:** Nhập môn Khoa học Dữ liệu (PTIT)  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Chương trình:** Khoa học Dữ liệu & Trực quan hóa Khám phá (Chương 3)  
> **Mã Task:** Task 2.4 [Thành viên 2]  
> **Module thực thi:** [`plot_eda_figures.py`](plot_eda_figures.py)  
> **Thư mục ảnh xuất 300 DPI:** [`reports/figures/`](../../reports/figures/)

---

## 1. MỤC TIÊU & DANH MỤC BỘ 5 BIỂU ĐỒ EDA

Bộ 5 biểu đồ EDA được thiết kế theo chuẩn đồ họa xuất bản (Publication-Ready, độ phân giải cao **300 DPI**, bảng màu phân cực chuyên nghiệp) nhằm giải mã toàn diện các đặc trưng kinh tế, mục tiêu và nhịp độ trận đấu mốc 10 phút:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ FIG 1: Ma trận tương quan Pearson Heatmap (Chỉ số 10p vs Tỷ lệ thắng).                   │
│ FIG 2: Phân phối chênh lệch vàng Histogram + KDE (Đấu Giải vs Solo Rank).                │
│ FIG 3: Boxplot & Ngoại lai phân bố kinh tế 5 vị trí thi đấu (Top, Jng, Mid, Bot, Sup).   │
│ FIG 4: Scatter Plot & Đường hồi quy: Vàng dẫn trước 10p vs Thời lượng kết thúc trận.    │
│ FIG 5: Grouped Bar Chart So sánh 4 Kịch bản Mục tiêu lớn (3 Sâu vs Rồng 1).             │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. CHI TIẾT & Ý NGHĨA KHOA HỌC CỦA TỪNG BIỂU ĐỒ

### 📊 FIG 1: BẢN ĐỒ NHIỆT MA TRẬN TƯƠNG QUAN PEARSON (CORRELATION HEATMAP)
* **Tệp ảnh:** [`reports/figures/fig1_correlation_heatmap.png`](../../reports/figures/fig1_correlation_heatmap.png)
* **Phương pháp:** Tính toán hệ số tương quan tuyến tính Pearson ($r \in [-1, 1]$) giữa các chỉ số mốc 10 phút và biến mục tiêu `result` (Thắng/Thua). Áp dụng mặt nạ (mask) tam giác trên để tối ưu không gian thị giác.
* **Phát hiện quan trọng:**
  1. **Chênh lệch Vàng (`golddiffat10`)** có hệ số tương quan dương mạnh nhất với chiến thắng ($r = +0.61$), tiếp theo là **Chênh lệch Kinh nghiệm (`xpdiffat10`)** ($r = +0.52$) và **Mạng hạ gục (`killsat10`)** ($r = +0.48$).
  2. **Rồng Đầu Tiên (`firstdragon`)** có tương quan $r = +0.38$, trong khi **Sâu Hư Không (`void_grubs`)** đạt $r = +0.22$.
  3. **Thời lượng trận đấu (`duration_min`)** có tương quan âm ($r = -0.31$) với chênh lệch vàng $\rightarrow$ Càng dẫn nhiều tiền ở phút 10 thì trận đấu càng kết thúc sớm.

---

### 📈 FIG 2: PHÂN PHỐI CHÊNH LỆCH VÀNG LÚC 10 PHÚT (HISTOGRAM + KDE DENSITY)
* **Tệp ảnh:** [`reports/figures/fig2_gold_diff_distribution_kde.png`](../../reports/figures/fig2_gold_diff_distribution_kde.png)
* **Phương pháp:** Kết hợp biểu đồ cột tần suất (Histogram 40 bins) và đường ước lượng mật độ hạt nhân Gaussian KDE, phân tầng theo 2 nhóm màu (Xanh: Đội Thắng, Đỏ: Đội Thua).
* **Phát hiện quan trọng:**
  1. **Tính đối xứng chuông chuẩn:** Phân phối chênh lệch vàng của cả 2 môi trường đều tập trung cao nhất ở khoảng `[-1,500g, +1,500g]`.
  2. **Độ lệch của tâm phân phối:**
     - Đội Thắng tại Đấu Giải có mức chênh lệch vàng trung bình là **+1,250g** lúc 10 phút.
     - Đội Thua có mức chênh lệch vàng trung bình là **-1,250g**.
  3. **Độ phân tán ở Solo Rank rộng hơn:** Solo Rank xuất hiện nhiều trận đấu có chênh lệch vàng cực đoan (vượt qua mốc $\pm 4,000$g lúc 10 phút) do kỹ năng cá nhân chênh lệch và bắt lẻ đẫm máu.

---

### 📦 FIG 3: PHÂN BỐ KINH TẾ 5 VỊ TRÍ THI ĐẤU LÚC 10 PHÚT (BOXPLOT & OUTLIERS)
* **Tệp ảnh:** [`reports/figures/fig3_lane_economy_boxplot.png`](../../reports/figures/fig3_lane_economy_boxplot.png)
* **Phương pháp:** Biểu đồ hộp biểu diễn 5 giá trị then chốt (Min, Q1, Median, Q3, Max) và lọc các điểm ngoại lai ($1.5 \times \text{IQR}$) cho 5 vị trí: Đường Trên (Top), Đi Rừng (Jungle), Đường Giữa (Mid), Xạ Thủ (Bot), Hỗ Trợ (Support).
* **Phát hiện quan trọng:**
  1. **Vị trí Đường Giữa (Mid) & Đường Trên (Top)** có biên độ dao động và độ trải giữa (IQR) lớn nhất (~1,200g - 1,400g) $\rightarrow$ Đây là 2 khu vực đường đơn xảy ra nhiều pha solo-kill và đè đường triệt để nhất.
  2. **Vị trí Hỗ Trợ (Support)** có độ trải hẹp nhất (IQR ~450g) do nguồn thu nhập chủ yếu phụ thuộc vào trang bị hỗ trợ cố định và ít farm lính.
  3. **Điểm ngoại lai (Outliers):** Xuất hiện các trường hợp tuyển thủ out trình đè đường tới hơn $+2,500$g chỉ trong 10 phút đầu trận (chủ yếu ở kèo Counter-Pick đường trên và đường giữa).

---

### 📉 FIG 4: MỐI QUAN HỆ GIỮA VÀNG DẪN TRƯỚC VÀ THỜI LƯỢNG TRẬN ĐẤU (SCATTER + REGRESSION)
* **Tệp ảnh:** [`reports/figures/fig4_gold_lead_vs_duration_scatter.png`](../../reports/figures/fig4_gold_lead_vs_duration_scatter.png)
* **Phương pháp:** Biểu đồ phân tán (Scatter Plot) với độ trong suốt alpha kết hợp đường hồi quy tuyến tính (Linear Regression Trendline với dải tin cậy 95%).
* **Phát hiện quan trọng:**
  1. **Độ dốc âm rõ rệt:** Cả 2 đồ thị đều có độ dốc đi xuống (Negative Slope). Khi lượng vàng dẫn trước tăng từ $500$g lên $3,500$g, thời gian kết thúc trận đấu bị kéo tụt trung bình từ $33$ phút xuống còn $25$ phút ở Đấu Giải.
  2. **Mốc chặn Baron (20 phút):** Ở Đấu Giải, hầu hết các trận đấu có độ dẫn tiền cực lớn đều hội tụ quanh mốc 22 - 25 phút (ngay sau khi ăn bùa lợi Baron đầu tiên).
  3. **Mốc Đầu Hàng Sớm (FF15) ở Solo Rank:** Rất nhiều chấm tròn ở Solo Rank rơi xuống sát mốc 15 - 18 phút do cơ chế biểu quyết đầu hàng sớm.

---

### 📊 FIG 5: MA TRẬN TOÀN DIỆN 8 TỔ HỢP MỤC TIÊU LỚN (RỒNG 1 x 0, 1, 2, 3 SÂU HƯ KHÔNG)
* **Tệp ảnh:** [`reports/figures/fig5_neutral_objectives_scenarios_bar.png`](../../reports/figures/fig5_neutral_objectives_scenarios_bar.png)
* **Phương pháp:** Biểu đồ 2 đồ thị con (Subplots) so sánh song song giữa Đấu Giải (Pro Play) và Solo Rank (Thách Đấu). Mỗi đồ thị phân rã toàn bộ 4 mức Sâu (0, 1, 2, 3 Sâu) theo 2 trạng thái: **Có Rồng 1** (Cột Xanh) vs **Mất Rồng 1** (Cột Đỏ), kèm đường mốc cân bằng 50%.
* **Phát hiện quan trọng:**
  1. **Hiệu ứng "Bảo hiểm trên 50%" của Rồng 1 ở Đấu Giải:** Bất kể ăn 0, 1, 2 hay 3 Sâu, hễ có Rồng 1 là tỷ lệ thắng đều vượt trên 50% (53.6% -> 68.4%). Ngược lại, nếu mất Rồng 1 thì dù ăn đủ 3 Sâu vẫn không vượt qua mốc 50% (đạt tối đa 47.2%).
  2. **Kèo chia sâu (1 Rồng + 1 Sâu) vs (0 Rồng + 2 Sâu):** Đội ăn Rồng + 1 Sâu thắng **54.7% (Pro)** và **62.6% (Rank)**, áp đảo hoàn toàn đội ăn 2 Sâu mất Rồng (43.8% Pro và 47.6% Rank).
  3. **Solo Rank đề cao 3 Sâu hơn Đấu Giải:** Ở Rank Đơn, đội mất Rồng nhưng ăn trọn 3 Sâu vẫn đạt tỷ lệ thắng **54.7%** (vượt 50%) nhờ khả năng tự đẩy trụ lăn cầu tuyết cá nhân.
  4. **Thâu tóm cả hai (Có Rồng + 3 Sâu):** Tỷ lệ thắng vọt lên **68.4% (Pro)** và **76.3% (Rank)**. Mất trắng cả hai tụt xuống **31.4% (Pro)** và **31.9% (Rank)**.

---

## 3. HƯỚNG DẪN TÁI TẠO BIỂU ĐỒ (HOW TO RUN)

Chạy script từ thư mục gốc qua môi trường ảo `.venv`:

```powershell
# Xuất toàn bộ 5 biểu đồ 300 DPI vào reports/figures/
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py

# Xuất riêng 1 biểu đồ cụ thể (ví dụ: Fig 1)
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py --fig 1
```
