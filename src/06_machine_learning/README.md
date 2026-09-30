# Module 06: Học Máy & Dự Đoán Thắng Thua (Machine Learning)

## Mục tiêu & Trách nhiệm
Module này chịu trách nhiệm xây dựng và đánh giá hệ thống mô hình dự đoán 2 giai đoạn và phân cụm đội hình:
- **Tầng 1 (Draft Prediction - Phút 0):** Dự đoán xác suất thắng dựa hoàn toàn vào đội hình cấm/chọn (10 tướng). Mô hình: Logistic Regression, Random Forest, LightGBM.
- **Tầng 2 (Snowball Prediction - Phút 10):** Dự đoán xác suất thắng dựa vào diễn biến trận đấu ở phút 10 (chênh lệch vàng, rồng, mạng hạ gục, trụ). Mô hình: XGBoost, LightGBM, Random Forest.
- **Phân cụm Đội hình (Archetype Clustering qua K-Means & PCA - Task 3.4):** Vector hóa tướng theo 5 trục sức mạnh `[Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control]` để nhận diện 4 trường phái đội hình chiến thuật (*Early Snowball / Dive, Dragon Soul Stacking, Late-Game Hypercarry, Pick & Split-Push 1-3-1*).

## Đánh giá & Tiêu chuẩn
- Đạt độ chính xác (Accuracy) > 75%, AUC-ROC > 0.82.
- Phân tích độ quan trọng của đặc trưng (Feature Importance / SHAP values).
- Xuất file mô hình huấn luyện: `models/draft_model.pkl`, `models/snowball_model.pkl`, `models/archetype_kmeans.pkl`.

