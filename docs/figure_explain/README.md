# BỘ TÀI LIỆU GIẢI THÍCH TOÀN DIỆN 5 BIỂU ĐỒ EDA (FIGURE EXPLAIN)

> **Môn học:** Nhập môn Khoa học Dữ liệu (PTIT)  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Thư mục ảnh 300 DPI:** [`reports/figures/`](../../reports/figures/)  
> **Script tạo biểu đồ:** [`src/05_visualization/plot_eda_figures.py`](../../src/05_visualization/plot_eda_figures.py)

---

## 📚 DANH MỤC CÁC TÀI LIỆU GIẢI THÍCH CHI TIẾT

Hệ thống tài liệu giải thích chi tiết từng biểu đồ, bao gồm mục tiêu khoa học, công thức toán học, phân tích chuyên sâu các cặp chỉ số, giải đáp các câu hỏi hóc búa của Hội đồng và lưu ý nghiệp vụ:

| Tên File Giải Thích | Biểu Đồ Hình Ảnh Tương Ứng | Nội Dung Trọng Tâm & Phát Hiện Khoa Học |
| :--- | :--- | :--- |
| 📄 [`fig1_correlation_heatmap.md`](fig1_correlation_heatmap.md) | `reports/figures/fig1_correlation_heatmap.png` | **Ma trận tương quan Pearson Heatmap (9x9):** Giải thích Colorbar [-1, +1], tại sao đường chéo = 1, tại sao không có -1, phân biệt hệ số r vs tỷ lệ thắng %, Feature Selection. |
| 📄 [`fig2_gold_diff_distribution.md`](fig2_gold_diff_distribution.md) | `reports/figures/fig2_gold_diff_distribution_kde.png` | **Phân phối chênh lệch vàng (Histogram + KDE):** Phân tách tâm phân phối (+1,250g Thắng vs -1,250g Thua), kiểm tra tính chuẩn Gaussian, so sánh độ phân tán Pro vs Rank. |
| 📄 [`fig3_lane_economy_boxplot.md`](fig3_lane_economy_boxplot.md) | `reports/figures/fig3_lane_economy_boxplot.png` | **Kinh tế 5 vị trí (Boxplot & Outliers):** Giải thích Median = 0, IQR từng vị trí (Bot 642g > Top 616g > Jng 572g > Mid 556g > Sup 328g), giải thích tính đối xứng gương và ngoại lai. |
| 📄 [`fig4_gold_lead_vs_duration.md`](fig4_gold_lead_vs_duration.md) | `reports/figures/fig4_gold_lead_vs_duration_scatter.png` | **Vàng dẫn trước vs Thời lượng (Scatter + OLS):** Độ dốc âm Snowball, ranh giới 20p (Baron ở Pro) vs 15p (FF15 ở Rank), giải thích các trận 11-13p do AFK/Open Mid. |
| 📄 [`fig5_neutral_objectives_scenarios.md`](fig5_neutral_objectives_scenarios.md) | `reports/figures/fig5_neutral_objectives_scenarios_bar.png` | **Ma trận 8 tổ hợp mục tiêu (Rồng 1 x 0, 1, 2, 3 Sâu):** Hiệu ứng bảo hiểm trên 50% của Rồng 1, giải mã kèo chia sâu 1R+1S vs 0R+2S, xử lý bỏ sâu/sâu biến mất. |

---

## 🎯 CÁCH CHẠY LẠI MÃ NGUỒN XUẤT ẢNH 300 DPI

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Xuất toàn bộ 5 biểu đồ 300 DPI vào reports/figures/
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py

# Xuất riêng 1 biểu đồ cụ thể (ví dụ: Fig 1)
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py --fig 1
```
