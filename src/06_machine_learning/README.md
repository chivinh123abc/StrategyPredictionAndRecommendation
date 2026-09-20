# Module 06: Học Máy & Dự Đoán Thắng Thua (Machine Learning)

## Mục tiêu & Trách nhiệm
Xây dựng và đánh giá hệ thống mô hình dự đoán 2 giai đoạn:
- **Tầng 1 (Draft Prediction - Phút 0):** Dự đoán xác suất thắng dựa hoàn toàn vào đội hình cấm/chọn (10 tướng). Mô hình: Logistic Regression, Random Forest.
- **Tầng 2 (Snowball Prediction - Phút 10):** Dự đoán xác suất thắng dựa vào diễn biến trận đấu ở phút 10 (chênh lệch vàng, rồng, mạng hạ gục, trụ). Mô hình: XGBoost, LightGBM, Random Forest.

## Đánh giá & Tiêu chuẩn
- Đạt độ chính xác (Accuracy) > 75%, AUC-ROC > 0.82.
- Phân tích độ quan trọng của đặc trưng (Feature Importance / SHAP values).
- Xuất file mô hình huấn luyện: `models/draft_model.pkl`, `models/snowball_model.pkl`.
