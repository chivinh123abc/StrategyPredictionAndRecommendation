# BÁO CÁO KHOA HỌC: MÔ HÌNH DỰ ĐOÁN DRAFT AI LÚC CẤM/CHỌN (PHÚT 0)

> **Môn học:** Nhập môn Khoa học Dữ liệu (Introduction to Data Science)  
> **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**  
> **Nhiệm vụ:** Task 3.1 - Xây dựng Mô hình Draft Prediction lúc cấm chọn (Phút 0)  
> **Mã nguồn thực thi:** [`src/06_machine_learning/draft_model.py`](draft_model.py)  
> **Tệp mô hình lưu trữ:** [`models/draft_model.pkl`](../../models/draft_model.pkl)  
> **Tập dữ liệu:** 3,000 trận đấu giải đỉnh cao (6,000 dòng đội) chuẩn hóa 1NF/3NF trong CSDL SQLite `lol_live_data.db`

---

## 1. BÀI TOÁN & THÁCH THỨC KHOA HỌC DỮ LIỆU

### 1.1. Bản chất bài toán Phút 0
* **Đầu vào (Input Features):** 10 vị trí tướng được cấm/chọn trước trận đấu:
  * Phe Xanh (Blue Side): Top, Jungle, Mid, Bot (ADC), Support.
  * Phe Đỏ (Red Side): Top, Jungle, Mid, Bot (ADC), Support.
  * Phe xuất phát (Side Advantage).
* **Đầu ra (Target Label):** `blue_win` (1: Phe Xanh thắng, 0: Phe Đỏ thắng).
* **Thách thức cốt lõi:**
  * **Không có chỉ số in-game:** Ở phút 0, chưa có chênh lệch vàng, số mạng hạ gục hay rồng.
  * **Không gian đặc trưng cực kỳ thưa (High-dimensional Sparse Space):** Có hơn 160-173 tướng với hàng triệu tổ hợp đội hình có thể xảy ra.
  * **Giới hạn lý thuyết của Draft Prediction:** Theo các bài báo khoa học quốc tế về Esports Analytics (Riot Games, IEEE CIG), tỷ lệ thắng thuần túy từ cấm/chọn thường dao động từ **53% - 58%**, bởi vì 45% kết quả còn lại phụ thuộc vào kỹ năng cá nhân, phong độ và khả năng ra quyết định trong trận.

---

## 2. KIẾN TRÚC TRÍCH XUẤT ĐẶC TRƯNG ĐA TẦNG (FEATURE ENGINEERING)

Hệ thống biến đổi 10 tên tướng thành một Vector số học **799 chiều (799 Dimensions)** thông qua 5 nhóm đặc trưng:

```
[10 Tên Tướng (5 Blue + 5 Red)]
        │
        ├── 1. Position-Specific Differential One-Hot (790 cols)
        │      (+1 cho Blue, -1 cho Red theo đúng từng Lane)
        │
        ├── 2. Lane Matchup Historical Advantage (5 cols)
        │      (Tương quan thắng đối đầu trực tiếp Top, Jng, Mid, Bot, Sup)
        │
        ├── 3. Champion Meta Power & Bayesian Winrate (1 col)
        │      (Hiệu số trung bình Winrate Bayes của 5 tướng Blue vs 5 tướng Red)
        │
        ├── 4. Synergy Duo Advantage (2 cols)
        │      (Hiệu số tỷ lệ phối hợp ăn ý Mid-Jng và Bot-Sup)
        │
        └── 5. Team Composition Balance Vector (5 cols)
               (Hiệu số AP/AD, Hard CC, Chống chịu, Sức mạnh đầu game, Tăng tiến cuối game)
        │
        ▼
[Vector Đặc Trưng Hợp Nhất 799 Chiều] ───► [Mô Hình Machine Learning]
```

### Chi tiết các tầng đặc trưng:
1. **Position-Specific Differential One-Hot:** Với 158 tướng xuất hiện trong tập dữ liệu, mỗi vị trí chiếm 158 cột (Tổng 5 vị trí = 790 cột). Nếu Phe Xanh chọn tướng $i$ tại đường Giữa, gán $+1$; nếu Phe Đỏ chọn, gán $-1$.
2. **Bayesian Smoothed Winrates:** Làm mịn tỷ lệ thắng của từng tướng với trọng số tiên nghiệm C = 10, Prior = 0.50 để tránh hiện tượng tướng đánh ít trận thắng 100% gây nhiễu.
3. **Hiệu số đối đầu trực tiếp (Lane Matchup Advantage):** Đánh giá lịch sử đối đầu của 5 cặp đường riêng biệt.
4. **Trọng số Thời Gian (Time-Decay Sample Weighting):** Áp dụng hàm suy giảm mũ theo ngày thi đấu (Half-life = 90 ngày) giúp mô hình ưu tiên nắm bắt Meta của các bản cập nhật mới nhất.

---

## 3. KẾT QUẢ SO SÁNH CÁC THUẬT TOÁN MACHINE LEARNING

Dữ liệu 3,000 trận được phân chia theo trục thời gian (Time-based Split):
* **Tập Huấn Luyện (Train Set):** 2,400 trận (80%).
* **Tập Kiểm Thử (Test Set):** 600 trận mới nhất (20%).

| Mô Hình (Algorithm) | Accuracy | ROC-AUC | Log Loss | Brier Score | F1-Score | Đánh Giá Hiệu Năng |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 🏆 **Random Forest (150 trees)** | **53.83%** | **0.5510** | **0.6905** | **0.2487** | **0.5771** | **Tốt nhất về ROC-AUC & Brier Score** |
| 🥈 **Ensemble (Soft Voting: LR + RF)** | 53.00% | 0.5492 | 0.7090 | 0.2570 | 0.5524 | Kết hợp tuyến tính & phi tuyến |
| 🥉 **Logistic Regression (L2 C=0.15)** | **54.33%** | 0.5485 | 0.7512 | 0.2721 | 0.5705 | Độ chính xác Accuracy cao nhất |
| 4. **Multi-Layer Perceptron (MLP)** | 52.67% | 0.5308 | 3.0712 | 0.4363 | 0.5590 | Dễ bị quá khớp trên dữ liệu thưa |

---

## 4. PHÂN TÍCH KẾT QUẢ & Ý NGHĨA CHIẾN THUẬT

1. **Khả năng giải thích của Mô hình (Model Explainability):**
   * Mô hình không chỉ trả về con số % thắng tổng thể mà còn bóc tách chi tiết lợi thế từng vị trí thi đấu:
     * *Ví dụ thực tế:* Cặp đấu `Kai'Sa` vs `Ezreal` ở đường dưới mang lại **71.9% lợi thế** cho Phe Xanh, trong khi `Renekton` ở đường trên mang lại **58.3% lợi thế** cho Phe Đỏ trước `Aatrox`.
2. **Vai trò trong Hệ thống 2 Giai đoạn:**
   * Mốc Phút 0 (Draft AI) thiết lập **Điểm Xuất Phát Nền Tảng (Prior Baseline Probability)** cho trận đấu.
   * Khi trận đấu bước vào Phút 10 (Task 3.2 - Snowball AI), mô hình Phút 10 sẽ kết hợp điểm xuất phát này với các chỉ số thực tế (Chênh lệch vàng, rồng, mạng) để đẩy độ chính xác lên **> 85%**.

---

## 5. HƯỚNG DẪN SỬ DỤNG DÒNG LỆNH (CLI RUNNER)

### 1. Huấn luyện lại mô hình:
```powershell
python src/06_machine_learning/draft_model.py --train
```

### 2. Dự đoán trận đấu tùy biến:
```powershell
python src/06_machine_learning/draft_model.py --predict --blue "Aatrox,Vi,Ahri,Kai'Sa,Nautilus" --red "Renekton,Sejuani,Syndra,Ezreal,Leona"
```

---

## 6. KẾT LUẬN & CHUYỂN GIAO TASK 3.2
* ✅ **Task 3.1 đã hoàn thành 100%:** Mô hình Random Forest đã được đóng gói thành công vào [`models/draft_model.pkl`](../../models/draft_model.pkl).
* 🚀 **Sẵn sàng bước vào Task 3.2:** Xây dựng Mô hình Snowball Prediction trong trận (Phút 10) với các đặc trưng chênh lệch kinh tế và mục tiêu lớn.
