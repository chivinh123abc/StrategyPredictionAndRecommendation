# MODULE 05: TRỰC QUAN HÓA DỮ LIỆU EDA (DATA VISUALIZATION - CHƯƠNG 3)

> **Môn học:** Nhập môn Khoa học Dữ liệu (PTIT)  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Phụ trách:** Thành viên 2 (Task 2.4)  
> **Trạng thái:** `VERIFIED - WORKING` (100% Hoàn thành)

---

## 1. MỤC TIÊU & DANH MỤC BỘ 5 BIỂU ĐỒ 300 DPI

Module xuất bản bộ 5 biểu đồ trực quan hóa khám phá dữ liệu chuẩn khoa học (Publication-Ready, 300 DPI) lưu tại [`reports/figures/`](../../reports/figures/):

1. **Fig 1 (Pearson Heatmap):** Ma trận tương quan 9x9 giữa các chỉ số 10p và biến Thắng/Thua (thang đo `[-1.0, +1.0]`, tam giác dưới, căn thẳng hàng `make_axes_locatable`).
2. **Fig 2 (Histogram + KDE):** Phân phối chênh lệch vàng phút 10 theo Thắng (+1,250g) vs Thua (-1,250g) cho cả Đấu Giải và Solo Rank.
3. **Fig 3 (Boxplot & Outliers):** Phân bố chênh lệch kinh tế 10p theo 5 vị trí thi đấu (Top, Jungle, Mid, Bot, Support).
4. **Fig 4 (Scatter Plot + Regression):** Tương quan giữa Vàng dẫn trước 10p và Thời lượng kết thúc trận đấu (Mốc 20p Baron vs 15p FF15).
5. **Fig 5 (Grouped Bar Chart 2 Subplots):** Ma trận 8 tổ hợp mục tiêu lớn (Rồng 1 x 0, 1, 2, 3 Sâu) đối chiếu Đấu Giải vs Solo Rank.

---

## 2. HƯỚNG DẪN THỰC THI (CLI)

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Xuất toàn bộ 5 biểu đồ 300 DPI vào reports/figures/
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py

# Xuất riêng 1 biểu đồ cụ thể (ví dụ: Fig 1)
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py --fig 1
```

---

## 3. TÀI LIỆU LIÊN QUAN

* **Tài liệu phân tích tổng quan:** [`plot_eda_figures.md`](plot_eda_figures.md)
* **Bộ tài liệu giải thích chi tiết 5 biểu đồ:** [`docs/figure_explain/`](../../docs/figure_explain/)
  * [`fig1_correlation_heatmap.md`](../../docs/figure_explain/fig1_correlation_heatmap.md)
  * [`fig2_gold_diff_distribution.md`](../../docs/figure_explain/fig2_gold_diff_distribution.md)
  * [`fig3_lane_economy_boxplot.md`](../../docs/figure_explain/fig3_lane_economy_boxplot.md)
  * [`fig4_gold_lead_vs_duration.md`](../../docs/figure_explain/fig4_gold_lead_vs_duration.md)
  * [`fig5_neutral_objectives_scenarios.md`](../../docs/figure_explain/fig5_neutral_objectives_scenarios.md)

