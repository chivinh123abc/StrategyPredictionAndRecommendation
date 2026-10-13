# BỘ TÀI LIỆU GIẢI THÍCH TOÀN DIỆN 11 BIỂU ĐỒ NGHIÊN CỨU KHOA HỌC (FIGURE EXPLAIN)

> **Môn học:** Nhập môn Khoa học Dữ liệu (PTIT)  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Thư mục ảnh 300 DPI:** [`reports/figures/`](../../reports/figures/)  
> **Scripts tạo biểu đồ:**  
> - EDA (Fig 1 - 5): [`src/05_visualization/plot_eda_figures.py`](../../src/05_visualization/plot_eda_figures.py)  
> - Machine Learning Diagnostics (Fig 6 - 9): [`src/06_machine_learning/evaluate_models.py`](../../src/06_machine_learning/evaluate_models.py)  
> - Clustering & PCA (Fig 10 - 11): [`src/06_machine_learning/cluster_archetypes.py`](../../src/06_machine_learning/cluster_archetypes.py)

---

## 📚 DANH MỤC CÁC TÀI LIỆU GIẢI THÍCH CHI TIẾT

Hệ thống tài liệu giải thích chi tiết từng biểu đồ, bao gồm mục tiêu khoa học, công thức toán học, phân tích chuyên sâu các chỉ số, giải đáp các câu hỏi hóc búa của Hội đồng chấm điểm và lưu ý nghiệp vụ:

### Phân hệ 1: Trực Quan Hóa Khám Phá Dữ Liệu EDA (Chương 3)

| Tên File Giải Thích | Biểu Đồ Hình Ảnh Tương Ứng | Nội Dung Trọng Tâm & Phát Hiện Khoa Học |
| :--- | :--- | :--- |
| 📄 [`fig1_correlation_heatmap.md`](fig1_correlation_heatmap.md) | `reports/figures/fig1_correlation_heatmap.png` | **Ma trận tương quan Pearson Heatmap (9x9):** Giải thích Colorbar [-1, +1], tại sao đường chéo = 1, tại sao không có -1, phân biệt hệ số r vs tỷ lệ thắng %, Feature Selection. |
| 📄 [`fig2_gold_diff_distribution.md`](fig2_gold_diff_distribution.md) | `reports/figures/fig2_gold_diff_distribution_kde.png` | **Phân phối chênh lệch vàng (Histogram + KDE):** Phân tách tâm phân phối (+1,250g Thắng vs -1,250g Thua), kiểm tra tính chuẩn Gaussian, so sánh độ phân tán Pro vs Rank. |
| 📄 [`fig3_lane_economy_boxplot.md`](fig3_lane_economy_boxplot.md) | `reports/figures/fig3_lane_economy_boxplot.png` | **Kinh tế 5 vị trí (Boxplot & Outliers):** Giải thích Median = 0, IQR từng vị trí (Bot 642g > Top 616g > Jng 572g > Mid 556g > Sup 328g), giải thích tính đối xứng gương và ngoại lai. |
| 📄 [`fig4_gold_lead_vs_duration.md`](fig4_gold_lead_vs_duration.md) | `reports/figures/fig4_gold_lead_vs_duration_scatter.png` | **Vàng dẫn trước vs Thời lượng (Scatter + OLS):** Độ dốc âm Snowball, ranh giới 20p (Baron ở Pro) vs 15p (FF15 ở Rank), giải thích các trận 11-13p do AFK/Open Mid. |
| 📄 [`fig5_neutral_objectives_scenarios.md`](fig5_neutral_objectives_scenarios.md) | `reports/figures/fig5_neutral_objectives_scenarios_bar.png` | **Ma trận 8 tổ hợp mục tiêu (Rồng 1 x 0, 1, 2, 3 Sâu):** Hiệu ứng bảo hiểm trên 50% của Rồng 1, giải mã kèo chia sâu 1R+1S vs 0R+2S, xử lý bỏ sâu/sâu biến mất. |

### Phân hệ 2: Đánh Giá Chẩn Đoán Mô Hình Machine Learning (Chương 4 & 5)

| Tên File Giải Thích | Biểu Đồ Hình Ảnh Tương Ứng | Nội Dung Trọng Tâm & Phát Hiện Khoa Học |
| :--- | :--- | :--- |
| 📄 [`fig6_roc_auc_comparison.md`](fig6_roc_auc_comparison.md) | `reports/figures/fig6_roc_auc_comparison.png` | **Đường cong ROC-AUC & Precision-Recall (Phút 0 vs Phút 10):** Đối chiếu AUC 0.5510 (Cấm/Chọn) vs 0.7780 (Thực chiến). Minh chứng khoa học về giới hạn tự nhiên của cấm chọn trước trận và vai trò của Hands Diff. |
| 📄 [`fig7_confusion_matrices.md`](fig7_confusion_matrices.md) | `reports/figures/fig7_confusion_matrices.png` | **Ma trận nhầm lẫn (Confusion Matrices Heatmap):** Bóc tách True/False Positives và Negatives. Giải thích các ca ngoại lệ: Đội hình out-draft nhưng thua do macro lỗi, và đội hình yếu hơn nhưng thắng nhờ kỹ năng cá nhân. |
| 📄 [`fig8_calibration_curve.md`](fig8_calibration_curve.md) | `reports/figures/fig8_calibration_curve.png` | **Đường cong hiệu chuẩn xác suất (Reliability Diagram & Brier Score):** Đánh giá độ tin cậy của xác suất dự báo hiển thị trên giao diện người dùng. Phân tích Brier Score 0.2487 (Phút 0) vs 0.1925 (Phút 10). |
| 📄 [`fig9_draft_vs_snowball_feature_importance.md`](fig9_draft_vs_snowball_feature_importance.md) | `reports/figures/fig9_draft_vs_snowball_feature_importance.png` | **So sánh cơ chế đặc trưng quyết định:** Phân tích 799 chiều Cấm/Chọn (One-hot 10 tướng, Kèo lane, Bayesian winrate, Synergy) vs 22 đặc trưng Thực chiến (Vàng tổng, Cấp độ, Vàng dồn chủ lực Mid+Bot, Rồng 1). |

### Phân hệ 3: Phân Cụm K-Means & Giảm Chiều PCA Nhận Diện Trường Phái (Chương 4)

| Tên File Giải Thích | Biểu Đồ Hình Ảnh Tương Ứng | Nội Dung Trọng Tâm & Phát Hiện Khoa Học |
| :--- | :--- | :--- |
| 📄 [`fig10_kmeans_elbow_silhouette.md`](fig10_kmeans_elbow_silhouette.md) | `reports/figures/fig10_kmeans_elbow_silhouette.png` | **Phương pháp Khuỷu tay (Elbow) & Hệ số Silhouette:** Khảo sát K=2..8 trên 6,000 đội hình. Giải thích lý do chọn K=4 tối ưu toán học (WCSS Elbow Point) và phù hợp 4 trường phái chiến thuật. |
| 📄 [`fig11_draft_archetypes_pca_clusters.md`](fig11_draft_archetypes_pca_clusters.md) | `reports/figures/fig11_draft_archetypes_pca_clusters.png` | **Không gian phân cụm PCA 2D & Bộ 4 biểu đồ Radar 5 trục:** Chiếu 6,000 đội hình lên 2 trục PC1 (Tempo) & PC2 (Scale) với 68.98% phương sai giải thích. Hiển thị tâm cụm Centroids và ADN chiến thuật 4 trường phái. |

---

## 🎯 CÁCH CHẠY LẠI TOÀN BỘ PIPELINE XUẤT 11 BIỂU ĐỒ 300 DPI

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# 1. Xuất bộ 5 biểu đồ EDA (Fig 1 - 5)
.\.venv\Scripts\python.exe src/05_visualization/plot_eda_figures.py

# 2. Xuất bộ 4 biểu đồ Machine Learning Diagnostics (Fig 6 - 9)
.\.venv\Scripts\python.exe src/06_machine_learning/evaluate_models.py

# 3. Xuất bộ 2 biểu đồ K-Means & PCA Archetypes (Fig 10 - 11)
.\.venv\Scripts\python.exe src/06_machine_learning/cluster_archetypes.py --train
```
