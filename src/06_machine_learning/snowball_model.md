# BÁO CÁO KHOA HỌC: MÔ HÌNH DỰ ĐOÁN LĂN CẦU TUYẾT TRONG TRẬN (SNOWBALL PREDICTION MODEL - PHÚT 10)

## THÔNG TIN TỔNG QUAN
- **Dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Học phần:** Nhập môn Khoa học Dữ liệu - PTIT (Giảng viên: TS. Thái Tuyết Hải).
- **Mã nguồn thực thi:** [`src/06_machine_learning/snowball_model.py`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/06_machine_learning/snowball_model.py)
- **Tệp đóng gói mô hình:** [`models/snowball_model.pkl`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/models/snowball_model.pkl)

---

## 1. MỤC TIÊU & BỐI CẢNH CHIẾN THUẬT (PHÚT 10)

Trong Liên Minh Huyền Thoại, **mốc 10 phút (Early-Game Milestone)** là thời điểm bản lề chuyển dịch từ giai đoạn đi đường (Laning Phase) sang giai đoạn kiểm soát mục tiêu lớn (Mid-Game Transitions):
1. **Hoàn tất nhịp gank đầu & vòng rừng:** Các vị trí đã có từ 1 đến 2 lần về nhà mua trang bị thành phần/thần thoại đầu tiên.
2. **Xuất hiện mục tiêu lớn đầu tiên:**
   - **Rồng nguyên tố 1 (Spawn 5:00):** Cung cấp bùa lợi nguyên tố vĩnh viễn và tiến trình Long Hồn.
   - **Đợt 1 Sâu Hư Không (Voidgrubs - Spawn 5:00):** Cung cấp sát thương đốt lên công trình và tạo bọ hư không đẩy lén.
   - **Giáp trụ (Turret Plates) chuẩn bị biến mất ở phút 14:** Đội nào có lợi thế đẩy đường sớm có thể bào rụng giáp trụ để thu về lượng tiền thưởng khổng lồ (125 vàng/khiên).
3. **Hiện thực hóa chênh lệch kỹ năng (Hands Diff):** Nếu ở Phút 0 (Task 3.1) yếu tố trình độ cá nhân chưa thể hiện qua chỉ số thực tế, thì ở Phút 10 toàn bộ "Hands Diff", "Gank Execution", "Wave Control" đã được lượng hóa chuẩn xác thành `golddiffat10`, `xpdiffat10`, `csdiffat10`, `killsat10`.

---

## 2. DỮ LIỆU & KỸ THUẬT KHAI PHÁ ĐẶC TRƯNG (FEATURE ENGINEERING)

Hệ thống tích hợp dữ liệu đa nguồn từ CSDL `lol_live_data.db` với tổng cộng **6,770 quan sát trận đấu mốc 10 phút**:
- **Đấu Giải Chuyên Nghiệp (Pro Play 2024 - 2025):** 4,752 quan sát (bóc tách chi tiết 5 vị trí Top, Jungle, Mid, Bot, Support).
- **Đấu Xếp Hạng Cao Thủ/Thách Đấu (Solo Rank VN2 & KR):** 2,018 quan sát (1,009 trận đấu 2 góc nhìn Blue & Red).

### Danh mục 22 Đặc trưng Chiến thuật (Feature Set):
1. **Kinh tế vĩ mô (Macro Economy):**
   - `golddiffat10`: Chênh lệch tổng lượng vàng giữa 2 đội lúc 10 phút.
   - `xpdiffat10`: Chênh lệch tổng điểm kinh nghiệm (Level advantage).
   - `csdiffat10`: Chênh lệch chỉ số lính + quái rừng (Creep Score).
2. **Giao tranh & Mạng hạ gục (Combat & Kill Differential):**
   - `killsat10`, `deathsat10`: Số mạng hạ gục và số lần nằm xuống.
   - `kill_diff`: Hiệu số mạng (Kills - Deaths).
   - `kda_ratio`: Tỷ số KDA chuẩn hóa.
3. **Phân bổ kinh tế 5 vị trí (Micro Lane Economy):**
   - `top_golddiff`, `jng_golddiff`, `mid_golddiff`, `bot_golddiff`, `sup_golddiff`.
   - `carry_gold_lead`: Tổng chênh lệch vàng của 2 vị trí gánh sát thương chủ lực (Mid Gold Lead + Bot Gold Lead).
4. **Mục tiêu trung lập & Công trình (Neutral Objectives & Structures):**
   - `firstdragon`: Chiếm lĩnh Rồng nguyên tố đầu tiên (1: Có, 0: Không).
   - `void_grubs`: Số lượng Sâu Hư Không ăn được (0 đến 6 con).
   - `has_3_grubs`: Đạt mốc kích hoạt 3 Sâu Hư Không đầu tiên.
   - `firsttower`: Phá hủy được trụ đầu tiên trước phút 10 (First Tower).
   - `double_neutral_control`: Kiểm soát đồng thời cả Rồng 1 và >= 3 Sâu Hư Không.
5. **Đặc trưng phi tuyến & Hiệu ứng Cầu tuyết (Synergy Multipliers):**
   - `gold_dragon_synergy`: Tương tác nhân giữa dẫn vàng và kiểm soát Rồng.
   - `gold_grubs_synergy`: Tương tác nhân giữa dẫn vàng và bùa lợi Sâu bào trụ.
6. **Bối cảnh thi đấu (Match Context):**
   - `is_blue_side`: Lợi thế xuất phát Phe Xanh (Bản đồ Summoner's Rift).
   - `is_pro_play`: Đấu giải chuyên nghiệp (Macro chặt chẽ) vs Đấu xếp hạng (Solo Queue biến động cao).

---

## 3. KẾT QUẢ HUẤN LUYỆN & SO SÁNH CÁC THUẬT TOÁN (BENCHMARK)

Mô hình được huấn luyện và đánh giá trên tập Kiểm Thử độc lập (**Test Set gồm 1,354 trận đấu**, Stratified Split 80/20):

| Thuật Toán (Algorithm) | Accuracy | ROC-AUC | Log Loss | Brier Score | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (150 trees)** | **70.75%** | **0.7780** | **0.5682** | **0.1925** | **0.7023** |
| **Ensemble (Soft Voting: LGB + XGB + RF + LR)** | **71.20%** | **0.7774** | **0.5694** | **0.1925** | **0.7045** |
| **XGBoost Classifier** | **71.20%** | **0.7751** | **0.5727** | **0.1935** | **0.7059** |
| **Logistic Regression (L2 Regularized)** | **71.20%** | **0.7746** | **0.5727** | **0.1937** | **0.7036** |
| **LightGBM Classifier** | **71.27%** | **0.7730** | **0.5768** | **0.1946** | **0.7028** |

---

## 4. ĐỐI CHIẾU CHIẾN THUẬT: ĐẤU GIẢI CHUYÊN NGHIỆP (PRO) VS SOLO RANK

Khi phân tách kiểm thử trên từng phân khúc môi trường thi đấu:

```
===============================================================================================
⚔️ ĐỐI CHIẾU ĐỘ CHÍNH XÁC SNOWBALL: ĐẤU GIẢI CHUYÊN NGHIỆP (PRO) VS ĐẤU XẾP HẠNG (SOLO RANK)
===============================================================================================
🏟️  Đấu Giải Pro Play (N = 927 trận)     : Accuracy = 69.47% | ROC-AUC = 0.7572
🔥 Đấu Xếp Hạng Solo Rank (N = 427 trận) : Accuracy = 73.54% | ROC-AUC = 0.8189
```

### Phân tích Ý nghĩa Khoa học:
1. **Tại Solo Rank (ROC-AUC = 0.8189, Accuracy = 73.54%):**
   - Lợi thế sớm ở phút 10 (Kills, Gold Lead) có tính chất tàn phá tâm lý đối phương rất mạnh (tâm lý buông xuôi, "FF 15", chat all trách móc).
   - Khả năng phối hợp phòng ngự thụ động kém khiến đội bị dẫn không thể kéo dài trận đấu để chờ ngưỡng sức mạnh Late-game.
2. **Tại Pro Play (ROC-AUC = 0.7572, Accuracy = 69.47%):**
   - Đội tuyển chuyên nghiệp có khả năng kiểm soát tầm nhìn (Vision Control), chia lane nhường tài nguyên (Wave Management) và phản gank chặt chẽ.
   - Các đội hình giao tranh tổng về sau (Teamfight Scaling) như Azir, Orianna, Jinx, Smolder có thể chấp nhận thua 1,000 - 1,500 vàng ở phút 10 nhưng vẫn lật kèo thành công ở phút 25 - 30 khi đạt ngưỡng 3 món trang bị.

---

## 5. TOP 10 ĐẶC TRƯNG QUYẾT ĐỊNH (FEATURE IMPORTANCE)

```
============================================================
📊 TOP 10 ĐẶC TRƯNG QUYẾT ĐỊNH THẮNG THUA MỐC 10 PHÚT
============================================================
 1. golddiffat10          : 15.50% ███████████████████████
 2. xpdiffat10            : 14.13% █████████████████████
 3. carry_gold_lead       :  9.75% ██████████████
 4. gold_dragon_synergy   :  7.65% ███████████
 5. firsttower            :  7.32% ██████████
 6. csdiffat10            :  5.47% ████████
 7. jng_golddiff          :  5.40% ████████
 8. kda_ratio             :  4.80% ███████
 9. bot_golddiff          :  4.72% ███████
10. sup_golddiff          :  4.57% ██████
```

### Phát hiện cốt lõi:
- **Kinh tế & Cấp độ (`golddiffat10` + `xpdiffat10` = 29.63%):** Chiếm gần 1/3 toàn bộ trọng số quyết định. Ở phút 10, cách biệt 1 level chiêu thức (đặc biệt là chiêu cuối R) tạo ra lợi thế giao tranh tuyệt đối.
- **Tiền của Chủ lực (`carry_gold_lead` = 9.75%):** Vàng rơi vào tay Xạ Thủ (Bot) và Pháp Sư (Mid) có sức nặng chuyển hóa thành chiến thắng cao gấp đôi so với vàng nằm ở Đấu Sĩ đường trên hay Hỗ Trợ.
- **Tương tác Vàng + Rồng (`gold_dragon_synergy` = 7.65%):** Dẫn vàng kết hợp sở hữu Rồng 1 sớm khóa chặt điều kiện thắng tích lũy Long Hồn từ phút 20.

---

## 6. KỊCH BẢN THỰC CHIẾN MẪU (INFERENCE EXAMPLES)

### Kịch bản 1: Blue Side dẫn áp đảo (+2,000 Vàng, 1 Rồng, 3 Sâu Hư Không)
- **Lệnh thực thi:** `python src/06_machine_learning/snowball_model.py --predict --gold-diff 2000 --dragon 1 --grubs 3 --side Blue`
- **Kết quả:**
  - **Tỷ lệ thắng dự đoán:** **83.23%**
  - **Tỷ lệ thua dự đoán:** **16.77%**
  - **Trạng thái:** *LĂN CẦU TUYẾT ÁP ĐẢO (Lead >= +2,000g)*

### Kịch bản 2: Bị dẫn sâu (-2,000 Vàng, Mất Rồng, Mất Sâu)
- **Lệnh thực thi:** `python src/06_machine_learning/snowball_model.py --predict --gold-diff -2000 --dragon 0 --grubs 0`
- **Kết quả:**
  - **Tỷ lệ thắng dự đoán:** **32.86%**
  - **Tỷ lệ thua dự đoán:** **67.14%**
  - **Trạng thái:** *BỊ DẪN RẤT LỚN (Nguy cơ vỡ trận)*

---

## 7. KẾT LUẬN & ĐÓNG GÓI
- **Task 3.2 đã hoàn thành 100% mục tiêu đề ra**: Xây dựng thành công mô hình Snowball Prediction 10 phút, tích hợp Gradient Boosting (XGBoost, LightGBM), Random Forest, Logistic Regression; đạt ROC-AUC 0.7780 - 0.8189 và độ chính xác phân loại vượt trội so với Phút 0.
- Tệp mô hình nhị phân [`models/snowball_model.pkl`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/models/snowball_model.pkl) sẵn sàng tích hợp vào Giao diện Web / Dashboard ở Giai đoạn 4.
