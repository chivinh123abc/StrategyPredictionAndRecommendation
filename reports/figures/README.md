# THƯ MỤC LƯU TRỮ HÌNH ẢNH BIỂU ĐỒ (REPORTS/FIGURES)

> **Tiêu chuẩn đồ họa:** Xuất bản bài báo khoa học (Publication-Ready), độ phân giải cao **300 DPI**, không lỗi font.  
> **Module sinh đồ họa:** [`src/05_visualization/plot_eda_figures.py`](../../src/05_visualization/plot_eda_figures.py)  
> **Thư mục tài liệu giải thích chi tiết:** [`figure_explain/`](figure_explain/)

---

## 📊 DANH MỤC BỘ 5 BIỂU ĐỒ EDA (CHƯƠNG 3)

| Tên File Ảnh (300 DPI) | Tiêu Đề Biểu Đồ | Tài Liệu Giải Thích Chi Tiết |
| :--- | :--- | :--- |
| 🖼️ [`fig1_correlation_heatmap.png`](fig1_correlation_heatmap.png) | **Ma Trận Tương Quan Pearson (9x9):** Tương quan các chỉ số 10p vs Kết quả Thắng. | 📄 [`figure_explain/fig1_correlation_heatmap.md`](figure_explain/fig1_correlation_heatmap.md) |
| 🖼️ [`fig2_gold_diff_distribution_kde.png`](fig2_gold_diff_distribution_kde.png) | **Phân Phối Chênh Lệch Vàng 10p:** Histogram + KDE Thắng vs Thua (Pro vs Rank). | 📄 [`figure_explain/fig2_gold_diff_distribution.md`](figure_explain/fig2_gold_diff_distribution.md) |
| 🖼️ [`fig3_lane_economy_boxplot.png`](fig3_lane_economy_boxplot.png) | **Kinh Tế 5 Vị Trí:** Boxplot & Outliers chênh lệch vàng 10p (Top, Jng, Mid, Bot, Sup). | 📄 [`figure_explain/fig3_lane_economy_boxplot.md`](figure_explain/fig3_lane_economy_boxplot.md) |
| 🖼️ [`fig4_gold_lead_vs_duration_scatter.png`](fig4_gold_lead_vs_duration_scatter.png) | **Vàng Dẫn Trước vs Thời Lượng:** Scatter Plot + Đường Hồi Quy OLS (Baron vs FF15). | 📄 [`figure_explain/fig4_gold_lead_vs_duration.md`](figure_explain/fig4_gold_lead_vs_duration.md) |
| 🖼️ [`fig5_neutral_objectives_scenarios_bar.png`](fig5_neutral_objectives_scenarios_bar.png) | **Ma Trận 8 Tổ Hợp Mục Tiêu Lớn:** Grouped Bar 2 Subplots (Rồng 1 x 0, 1, 2, 3 Sâu). | 📄 [`figure_explain/fig5_neutral_objectives_scenarios.md`](figure_explain/fig5_neutral_objectives_scenarios.md) |

---

## ⚡ HƯỚNG DẪN TÁI TẠO LẠI BỘ ẢNH (POWERSHELL)

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Xuất toàn bộ 5 biểu đồ 300 DPI
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py
```

