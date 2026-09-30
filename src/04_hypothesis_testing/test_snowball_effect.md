# BÁO CÁO KIỂM ĐỊNH THỐNG KÊ: HIỆU QUẢ LĂN CẦU TUYẾT (SNOWBALL EFFECT)

> **Môn học:** Nhập môn Khoa học Dữ liệu (PTIT)  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Chương trình:** Khoa học Dữ liệu & Phân tích Thống kê Thực nghiệm  
> **Module thực thi:** [`test_snowball_effect.py`](test_snowball_effect.py)  
> **Dữ liệu xuất:** [`data/processed/hypothesis_test_2_snowball.csv`](../../data/processed/hypothesis_test_2_snowball.csv)

---

## 1. ĐẶT VẤN ĐỀ VÀ MỤC TIÊU NGHIÊN CỨU

### 1.1. Hiện tượng "Lăn Cầu Tuyết" (Snowball Effect) trong LMHT là gì?
Trong tựa game Liên Minh Huyền Thoại (LMHT), **lăn cầu tuyết (snowball)** là khái niệm chỉ việc một đội giành được lợi thế sớm ở giai đoạn đi đường (10 phút đầu), sau đó liên tục tận dụng lượng trang bị, chỉ số vượt trội để kiểm soát bản đồ, ăn các mục tiêu lớn và bóp nghẹt đối thủ cho đến khi giành chiến thắng.

*Mốc dẫn trước **2,000 vàng lúc 10 phút** là một lợi thế khổng lồ:*
- Tương đương chênh lệch từ 6 đến 7 mạng hạ gục, hoặc 2 trụ đầu, hoặc hơn 60 chỉ số lính (CS).
- Đội dẫn đầu có từ 1 đến 1.5 trang bị lớn hoàn chỉnh trước đối thủ, tạo ra sự vượt trội hoàn toàn trong mọi pha giao tranh mục tiêu.

### 1.2. Câu hỏi nghiên cứu (Research Question)
> *"Hiệu quả Lăn Cầu Tuyết (khi dẫn từ 2,000 vàng trở lên lúc 10 phút) ở Đấu Giải Chuyên Nghiệp (Pro Play) có vượt trội, kết thúc trận nhanh hơn và ổn định hơn so với Đấu Xếp Hạng Đỉnh Cao (Solo Rank Thách Đấu) có ý nghĩa thống kê hay không?"*

### 1.3. Tại sao phải thực hiện kiểm định này?
1. **Về mặt Khoa học Dữ liệu & Học thuật:**
   - Ứng dụng trọn vẹn bộ công cụ Thống kê suy diễn thuộc **Chương 1 (Kiểm định giả thuyết)**:
     - **Two-sample Proportion Z-test**: So sánh 2 tỷ lệ độc lập (Tỷ lệ thắng).
     - **Two-sample Welch's t-test**: So sánh 2 trung bình độc lập khi phương sai không đồng nhất (Thời lượng trận đấu).
     - **Levene's Test**: Kiểm định độ đồng nhất của phương sai (Đo lường tính biến động, kỷ luật và phân tán dữ liệu).
2. **Về mặt Thực tiễn & eSports Analytics:**
   - Đánh giá sự khác biệt giữa **lối chơi kỷ luật đồng đội (Team Macro)** ở tuyển thủ chuyên nghiệp và **kỹ năng cá nhân hỗn loạn (Micro / Solo Play)** ở bậc rank Thách Đấu.
   - Cung cấp cơ sở định lượng để các huấn luyện viên (HLV) và nhà phân tích chiến thuật đưa ra quyết định: *Nên đánh nhịp độ nhanh (Early-game Aggression) hay đánh kiểm soát kéo dài (Late-game Scaling)?*

---

## 2. PHƯƠNG PHÁP THỐNG KÊ VÀ THIẾT LẬP GIẢ THUYẾT

Để đánh giá toàn diện hiện tượng Lăn Cầu Tuyết trên 3 khía cạnh: **Tỷ lệ thắng**, **Tốc độ trận đấu**, và **Độ ổn định**, nhóm thực hiện 3 bài toán kiểm định thống kê với mức ý nghĩa chung là **alpha = 0.05**:

```text
                                  KIỂM ĐỊNH LĂN CẦU TUYẾT (DẪN >= 2,000 VÀNG PHÚT 10)
                                                          │
          ┌───────────────────────────────────────────────┼──────────────────────────────────────────────┐
          ▼                                               ▼                                              ▼
[1. TỶ LỆ THẮNG (WINRATE)]                     [2. THỜI LƯỢNG TRẬN (DURATION)]                [3. TÍNH ỔN ĐỊNH (VARIANCE)]
   Two-sample Z-test                              Two-sample Welch's t-test                      Levene's Test for Variance
   H0: p_Pro = p_Rank                             H0: mu_Pro = mu_Rank                           H0: sigma^2_Pro = sigma^2_Rank
   H1: p_Pro != p_Rank                            H1: mu_Pro != mu_Rank                          H1: sigma^2_Pro != sigma^2_Rank
```

---

## 3. KẾT QUẢ VÀ Ý NGHĨA CHI TIẾT CỦA 3 PHÉP KIỂM ĐỊNH

Dữ liệu được trích xuất từ CSDL SQLite chuẩn hóa `data/database/lol_live_data.db`:
- **Đấu Giải Chuyên Nghiệp (Pro Play):** 230 trận đấu có đội dẫn từ 2,000 vàng trở lên lúc 10 phút.
- **Solo Rank Thách Đấu (Solo Queue):** 394 trận đấu có đội dẫn từ 2,000 vàng trở lên lúc 10 phút.

---

### 🔹 Phép Kiểm Định 1: So sánh Tỷ lệ chuyển hóa thành chiến thắng (Winrate Conversion Rate)
* **Tên phương pháp:** Two-sample Independent Proportion Z-test.
* **Mục đích làm phép này để làm gì?**
  - Trả lời câu hỏi: *"Khi đã vươn lên dẫn trước từ 2,000 vàng lúc 10 phút, liệu Tuyển thủ Chuyên nghiệp (Đấu Giải) có khả năng 'kết liễu' trận đấu và giành chiến thắng chắc chắn hơn người chơi Solo Rank hay không?"*
* **Tại sao phải làm?**
  - Người xem thường nghĩ Đấu Giải thi đấu kỷ luật hơn thì khi dẫn 2,000 vàng phải thắng gần như tuyệt đối (95% - 99%), còn Rank Đơn hay đánh ẩu nên tỷ lệ thắng sẽ thấp hơn.
  - Cần phép kiểm định Z-test để xác minh xem chênh lệch giữa `83.48%` và `86.04%` là sự khác biệt thực sự về bản chất hay chỉ do ngẫu nhiên của mẫu dữ liệu.
* **Thiết lập giả thuyết:**
  - H0: `p_Pro = p_Rank` (Tỷ lệ thắng khi dẫn 2,000 vàng ở Đấu Giải và Solo Rank là như nhau).
  - H1: `p_Pro != p_Rank` (Có sự khác biệt về tỷ lệ thắng giữa 2 môi trường).
* **Số liệu thực tế:**
  - Đấu Giải (Pro Play): Thắng **192 / 230** trận (đạt **83.48%**).
  - Solo Rank: Thắng **339 / 394** trận (đạt **86.04%**).
  - Tỷ lệ gộp (Pooled Proportion): **85.10%**.
* **Kết quả thống kê:**
  - `Z-score = -0.8671`
  - `p-value = 0.3859` (lớn hơn ngưỡng 0.05)
* **Quyết định & Kết luận:**
  - **CHƯA ĐỦ BẰNG CHỨNG BÁC BỎ H0.**
  - **Ý nghĩa:** Chênh lệch tỷ lệ thắng chỉ là ngẫu nhiên. Khi đã dẫn trước 2,000 vàng tại phút 10 (tương đương hơn 1 trang bị lớn hoàn chỉnh), cả tuyển thủ chuyên nghiệp lẫn cao thủ Thách Đấu đều có khả năng chuyển hóa thành chiến thắng cực kỳ khủng khiếp (**gần 85% - 86%**).

---

### 🔹 Phép Kiểm Định 2: So sánh Thời lượng kết thúc trận đấu (Game Duration)
* **Tên phương pháp:** Two-sample Independent Welch's t-test (không giả định bằng nhau về phương sai).
* **Mục đích làm phép này để làm gì?**
  - Trả lời câu hỏi: *"Khi một đội đã dẫn từ 2,000 vàng lúc 10 phút, liệu trận đấu ở Solo Rank có kết thúc NHANH HƠN Đấu Giải Chuyên Nghiệp một cách có ý nghĩa thống kê hay không?"*
* **Tại sao phải làm?**
  - Dù tỷ lệ thắng ở phép 1 là tương đương nhau (~85%), nhưng *nhịp độ đi đến chiến thắng* lại rất khác nhau: Solo Rank thường kết thúc chóng vánh trong khi Đấu Giải lại kéo dài thêm rất lâu.
  - Cần Welch's t-test để đo lường chính xác mức độ chênh lệch thời gian trung bình giữa 2 môi trường.
* **Thiết lập giả thuyết:**
  - H0: `mu_Pro = mu_Rank` (Thời gian kết thúc trận đấu trung bình là như nhau).
  - H1: `mu_Pro != mu_Rank` (Thời gian kết thúc trận đấu có sự chênh lệch có ý nghĩa thống kê).
* **Số liệu thực tế:**
  - Đấu Giải (Pro Play): Thời lượng trung bình = **29.75 phút** (cỡ mẫu n = 230).
  - Solo Rank: Thời lượng trung bình = **24.46 phút** (cỡ mẫu n = 394).
  - Chênh lệch: Trận Đấu Giải kéo dài hơn Solo Rank trung bình **5.29 phút** (hơn 21.6% thời lượng).
* **Kết quả thống kê:**
  - `t-statistic = +11.4618`
  - `p-value = 1.16 x 10^(-27) < 0.0001` (nhỏ hơn 0.05 rất nhiều)
* **Quyết định & Kết luận:**
  - **BÁC BỎ H0 CỰC KỲ MẠNH MẼ.**
  - **Ý nghĩa:** Trận Solo Rank kết thúc nhanh hơn Đấu Giải trung bình **5.3 phút** mang tính quy luật hệ thống: do cơ chế đầu hàng sớm (FF15) trong Rank Đơn và kỹ năng phối hợp co cụm phòng thủ trụ bậc cao (Turtle Defense) của các đội tuyển chuyên nghiệp.

---

### 🔹 Phép Kiểm Định 3: So sánh Tính Ổn Định và Kỷ Luật Thế Trận (Stability & Variance)
* **Tên phương pháp:** Levene's Test kiểm định tính đồng nhất phương sai giữa hai tổng thể.
* **Mục đích làm phép này để làm gì?**
  - Trả lời câu hỏi: *"Độ biến động / phân tán về thời gian kết thúc trận đấu của Tuyển thủ Chuyên nghiệp có ỔN ĐỊNH VÀ KỶ LUẬT HƠN người chơi Solo Rank hay không?"*
* **Tại sao phải làm?**
  - Phép số 2 chỉ đo giá trị *trung bình* (Mean), chưa phản ánh được mức độ *ổn định / hỗn loạn* (Variance).
  - Cần Levene's Test để kiểm chứng xem lối chơi kỷ luật của Đấu Giải có giúp trận đấu ít bị đột biến quăng game hơn Solo Rank hay không.
* **Thiết lập giả thuyết:**
  - H0: `sigma^2_Pro = sigma^2_Rank` (Độ phân tán thời gian kết thúc trận là đồng nhất).
  - H1: `sigma^2_Pro != sigma^2_Rank` (Độ phân tán giữa Đấu Giải và Solo Rank có sự khác biệt).
* **Số liệu thực tế:**
  - Độ lệch chuẩn Đấu Giải: `sigma_Pro = 4.68 phút`.
  - Độ lệch chuẩn Solo Rank: `sigma_Rank = 6.80 phút` (dao động lớn hơn gần 45%).
* **Kết quả thống kê:**
  - `Levene Statistic = +53.1630`
  - `p-value = 9.37 x 10^(-13) < 0.0001` (nhỏ hơn 0.05 rất nhiều)
* **Quyết định & Kết luận:**
  - **BÁC BỎ H0.**
  - **Ý nghĩa:** Đấu Giải có tính kỷ luật, bám sát các mốc Baron (phút 20) và Rồng Ngàn Tuổi (phút 35) nên thời gian trận đấu luôn dao động trong khung kiểm soát rất hẹp (~4.7 phút). Solo Rank biến động cực lớn (từ 15 phút đầu hàng đến hơn 40 phút quăng game).

---

### 📌 TỔNG HỢP NHANH BỘ 3 PHÉP KIỂM ĐỊNH:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Phép 1 (Tỷ lệ thắng - Z-test)  : Dẫn 2,000g lúc 10p đều nắm ~85% chiến thắng (Như nhau)│
│ Phép 2 (Thời lượng - t-test)  : Solo Rank kết thúc NHANH HƠN 5.3 phút (Do FF15 & Ép sân)│
│ Phép 3 (Độ ổn định - Levene)  : Đấu Giải ỔN ĐỊNH VÀ KỶ LUẬT HƠN (Ít bị quăng game)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. PHÂN TÍCH PHÂN TẦNG (MULTI-TIER ANALYSIS)

Để hiểu rõ hơn động lực của Lăn Cầu Tuyết, nhóm mở rộng kiểm định trên 4 mốc chênh lệch vàng lúc 10 phút:

| Mốc Dẫn Vàng (10p) | Số trận Pro | Pro Tỷ Lệ Thắng (%) | Pro Thời Lượng (phút) | Số trận Rank | Rank Tỷ Lệ Thắng (%) | Rank Thời Lượng (phút) | Chênh Lệch Thời Lượng | p-value Thời Lượng (t-test) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dẫn >= 1,000g** | 925 | 77.51% | 31.5p | 657 | 80.37% | 25.0p | **+6.5 phút** | `p < 10^(-50)` |
| **Dẫn >= 1,500g** | 486 | 81.89% | 30.7p | 517 | 84.53% | 24.5p | **+6.1 phút** | `p < 10^(-35)` |
| **Dẫn >= 2,000g** | 230 | 83.48% | 29.8p | 394 | 86.04% | 24.5p | **+5.3 phút** | `p < 10^(-26)` |
| **Dẫn >= 3,000g** | 49 | **91.84%** | 28.9p | 208 | **89.90%** | 23.1p | **+5.7 phút** | `p < 10^(-12)` |

```text
                       TỶ LỆ THẮNG THEO MỐC VÀNG DẪN TRƯỚC (10 PHÚT)
  100% ┼                                                  ┌──── 91.8% (Pro)
       │                                       ┌──────────┴──── 89.9% (Rank)
   90% ┼                            ┌──────────┴──── 86.0% (Rank)
       │                 ┌──────────┴──── 84.5% (Rank)
   80% ┼      ┌──────────┴──── 80.4% (Rank) / 83.5% (Pro)
       │      └────────── 77.5% (Pro)
   70% ┼───────────────────────────────────────────────────────────────────
           Dẫn >= 1,000g        Dẫn >= 1,500g        Dẫn >= 2,000g        Dẫn >= 3,000g
```

---

## 5. GIẢI THÍCH NGUYÊN NHÂN NGHIỆP VỤ & BẢN CHẤT GAME LMHT

Từ 3 kết quả kiểm định trên, Khoa học Dữ liệu làm sáng tỏ các cơ chế vận hành trong LMHT:

### 5.1. Tại sao Tỷ lệ thắng (Winrate) ở cả 2 môi trường đều cao xấp xỉ nhau (~85%)?
* **Sức mạnh ngưỡng trang bị sớm:** Ở phút thứ 10, người chơi trung bình chỉ tích lũy được khoảng 3,000 - 3,500 vàng. Một đội dẫn 2,000 vàng đồng nghĩa với việc họ sở hữu sức mạnh trang bị vượt trội gần **30% - 40%** so với đối phương.
* **Khóa chặt mục tiêu lớn:** Đội dẫn vàng dễ dàng kiểm soát tầm nhìn khu vực Sâu Hư Không (Voidgrubs) và Rồng Nguyên Tố đầu tiên, tạo đà đẩy nhanh tốc độ phá hủy công trình.

### 5.2. Tại sao trận Solo Rank kết thúc NHANH HƠN 5.3 phút so với Đấu Giải?
1. **Cơ chế Đầu Hàng Sớm (Early Surrender / FF15):**
   - Trong Solo Rank, Riot Games cho phép biểu quyết đầu hàng từ **phút 15**. Khi bị dẫn cách biệt từ 2,000 vàng ở phút 10, tâm lý người chơi rank đơn rất dễ nản lòng và đồng thuận bỏ cuộc sớm.
   - Ngược lại, trong Đấu Giải Chuyên Nghiệp, luật thi đấu **nghiêm cấm đầu hàng**. Mọi tuyển thủ bắt buộc phải thi đấu cho đến khi nhà chính Nexus nổ.
2. **Chiến thuật Phòng thủ Nhà chính (High Ground Turtle Defense):**
   - Ở Đấu Giải, các đội bị dẫn có kỹ năng phối hợp macro xuất sắc: họ chủ động nhường mục tiêu phụ, co cụm thủ trụ bậc cao (Inhibitor Turrets) và dọn lính an toàn để kéo dài trận đấu chờ cơ hội đối phương mắc sai lầm giao tranh.
3. **Lối chơi Giao tranh Liên Tục (Agressiveness):**
   - Trong rank Thách Đấu, người chơi có xu hướng liên tục tổ chức bắt lẻ và ép giao tranh đẫm máu (brawl), khiến khoảng cách chênh lệch bị đẩy lên cực đại trong thời gian rất ngắn.

### 5.3. Tại sao Đấu Giải có tính Kỷ luật & Ổn định cao hơn Solo Rank?
* Độ lệch chuẩn thời gian ở Đấu Giải chỉ là **4.7 phút** (so với **6.8 phút** của Solo Rank).
* Tuyển thủ chuyên nghiệp tuân thủ chặt chẽ thời gian hồi sinh của Baron Nashor (phút 20) và Rồng Ngàn Tuổi (phút 35) để dứt điểm trận đấu theo bài bản, ít xảy ra tình trạng "quăng game" (throw lead) hay bị lật kèo bất thường như trong môi trường Solo Rank cá nhân.

---

## 6. KẾT LUẬN & ĐỀ XUẤT CHO MILESTONE TIẾP THEO

1. **Kết luận chính:**
   - Dẫn >= 2,000 vàng lúc 10 phút đem lại tỷ lệ chiến thắng gần như tuyệt đối (**khoảng 85%**) ở cả Pro Play lẫn Solo Rank.
   - Sự khác biệt căn bản không nằm ở tỷ lệ thắng, mà nằm ở **Thời lượng kết thúc trận đấu** (`t = +11.46, p < 10^(-26)`) và **Tính ổn định kiểm soát trận đấu** (`Levene = 53.16, p < 10^(-12)`).
2. **Bước triển khai tiếp theo:**
   - Chuyển sang **Task 2.3**: Kiểm định Chi-square và Tỷ số Chênh (Odds Ratio) giữa Đội ăn **3 Sâu Hư Không đầu** so với Đội ăn **Rồng Nguyên Tố đầu**.
