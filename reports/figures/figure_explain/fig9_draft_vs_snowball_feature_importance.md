# GIẢI THÍCH CHI TIẾT FIG 9: SO SÁNH TRỌNG SỐ ĐẶC TRƯNG (FEATURE IMPORTANCE: PHÚT 0 VS PHÚT 10)

> **Tệp hình ảnh tương ứng:** `reports/figures/fig9_draft_vs_snowball_feature_importance.png`  
> **Chương giáo trình:** Chương 4 & 5 - Khả năng giải thích của mô hình học máy (Model Explainability & Feature Importance)  
> **Nguồn dữ liệu:** Trích xuất từ cây quyết định Random Forest (150 cây) cho cả 2 mô hình trong CSDL `lol_live_data.db`.

---

## 1. MỤC TIÊU & Ý NGHĨA KHOA HỌC

Biểu đồ Fig 9 so sánh cơ chế "tư duy" của AI giữa 2 giai đoạn:
1. *"Khi cấm chọn (Phút 0), AI nhìn vào đâu để đánh giá đội hình nào mạnh hơn?"*
2. *"Khi bước vào thực chiến (Phút 10), yếu tố nào chi phối nhiều nhất đến việc chuyển hóa thành chiến thắng?"*

---

## 2. BÓC TÁCH CHI TIẾT 2 BIỂU ĐỒ THÀNH PHẦN

### A. Subplot 1 (Bên trái): Phân bổ Trọng số Cấm/Chọn (Phút 0 - Không gian 799 chiều)
- **1. Position One-Hot Vectors (10 Tướng thi đấu): 46.8%**
  - Chiếm gần một nửa tổng trọng số. AI đánh giá bản sắc và sức mạnh cá nhân của 10 con tướng được chọn ở từng vị trí (Top, Jungle, Mid, Bot, Support).
- **2. Lane Matchup Advantage (5 Cặp đối đầu đường): 18.4%**
  - Kèo đối đầu trực tiếp 1v1 (Top vs Top, Mid vs Mid, Bot vs Bot) quyết định xem đường nào sẽ có lợi thế đẩy lính và tạo áp lực trước.
- **3. Bayesian Champion Winrates (Sức mạnh Meta hiện tại): 15.2%**
  - Tỷ lệ thắng làm mịn Bayes phản ánh vị thế của tướng trong phiên bản thi đấu hiện hành (Patch Meta Tiers).
- **4. Synergy Duo (Mid-Jungle & Bot-Support): 10.6%**
  - Độ ăn ý của 2 trục phối hợp quan trọng nhất: Rừng + Đường giữa (kiểm soát sông/sâu) và Xạ thủ + Hỗ trợ (2v2 đường dưới).
- **5. Team Composition Balance (Cân bằng đội hình): 9.0%**
  - Tỷ lệ phân bổ sát thương AD/AP, lượng khống chế cứng (Hard CC), khả năng chống chịu và ngưỡng sức mạnh Đầu trận vs Cuối trận (Early vs Late-game Scaling).

---

### B. Subplot 2 (Bên phải): Top 10 Đặc trưng Lăn Cầu Tuyết (Phút 10 - 22 Đặc trưng)
- **1. Chênh lệch Vàng tổng (`golddiffat10`): 15.50%**
  - Thước đo kinh tế trực tiếp nhất. Vàng biến thành trang bị và sát thương cụ thể.
- **2. Chênh lệch Cấp độ & Kinh nghiệm (`xpdiffat10`): 14.13%**
  - Ở phút thứ 10, chênh lệch 1 level (đặc biệt là ngưỡng cấp 6 chiêu cuối R) tạo ra cách biệt sức mạnh khổng lồ trong giao tranh.
- **3. Vàng dồn cho 2 Chủ lực (`carry_gold_lead` = Mid + Bot): 9.75%**
  - **Phát hiện nghiệp vụ then chốt:** Vàng nằm trong tay Xạ thủ (Bot) và Pháp sư (Mid) có giá trị chuyển hóa chiến thắng cao hơn hẳn vàng nằm ở Đấu sĩ đường trên hay Hỗ trợ.
- **4. Hiệp đồng Vàng + Rồng 1 (`gold_dragon_synergy`): 7.65%**
  - Đội vừa dẫn tiền vừa ăn Rồng 1 sẽ khóa chặt thế trận lăn cầu tuyết và nhịp đếm Long Hồn ở phút 20-25.
- **5. Phá Trụ Đầu Tiên (`firsttower`): 7.32%**
  - Phá trụ sớm trước phút 10 mở toang tầm nhìn rừng đối phương và cung cấp lượng vàng thưởng khổng lồ.
- **6. Các yếu tố còn lại:** `csdiffat10` (5.47%), `jng_golddiff` (5.40%), `kda_ratio` (4.80%), `bot_golddiff` (4.72%), `sup_golddiff` (4.57%).

---

## 3. CÂU HỎI BẢO VỆ PHẢN BIỆN (Q&A)

### Câu hỏi: Tại sao đặc trưng `carry_gold_lead` lại quan trọng hơn `top_golddiff` ở mốc 10 phút?
- **Trả lời phản biện chuẩn:**
  > "Trong meta thi đấu chuyên nghiệp hiện đại, đường trên (Top) thường đóng vai trò cô lập (Isolate Island) hoặc chơi tướng chống chịu/đấu sĩ mở combat. Sát thương đầu ra và khả năng dọn công trình để kết thúc trận đấu nằm chủ yếu ở Xạ Thủ (Bot) và Pháp Sư (Mid). Dữ liệu thực nghiệm của mô hình khẳng định việc dồn tài nguyên cho 2 nguồn sát thương chủ lực mang lại tỷ lệ thắng cao hơn 30% so với dồn tài nguyên lên đường trên."
