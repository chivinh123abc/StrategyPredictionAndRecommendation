# BÁO CÁO KIỂM ĐỊNH THỐNG KÊ: 3 SÂU HƯ KHÔNG ĐẦU (VOIDGRUBS) VS RỒNG NGUYÊN TỐ ĐẦU (FIRST DRAGON)

> **Môn học:** Nhập môn Khoa học Dữ liệu (PTIT)  
> **Giảng viên hướng dẫn:** TS. Thái Tuyết Hải  
> **Chương trình:** Khoa học Dữ liệu & Phân tích Thống kê Thực nghiệm  
> **Mã Task:** Task 2.3 [Thành viên 2]  
> **Module thực thi:** [`test_voidgrubs_vs_dragon.py`](test_voidgrubs_vs_dragon.py)  
> **Dữ liệu xuất:** [`data/processed/hypothesis_test_3_objectives.csv`](../../data/processed/hypothesis_test_3_objectives.csv)

---

## 1. ĐẶT VẤN ĐỀ VÀ MỤC TIÊU NGHIÊN CỨU

### 1.1. Bối cảnh tranh chấp mục tiêu trung lập (5 - 10 phút đầu trận)
Trong các phiên bản LMHT gần đây (Mùa 2024 - 2026), Riot Games bổ sung bãi quái **Sâu Hư Không (Voidgrubs)** xuất hiện tại hang Baron ở phút thứ 5, song song với **Rồng Nguyên Tố đầu tiên (First Dragon)** tại hang Rồng. Điều này tạo ra một bài toán chiến thuật kinh điển cho người đi rừng và người kêu gọi giao tranh (Shotcaller):

> *"Khi hai mục tiêu lớn xuất hiện cùng lúc, đội nên dồn tài nguyên kiểm soát 3 Sâu Hư Không (để lấy sát thương chuẩn đẩy công trình) hay ăn Rồng Nguyên Tố đầu tiên (để tích lũy điều kiện thắng Linh Hồn Rồng)?"*

### 1.2. Câu hỏi nghiên cứu (Research Question)
> *"Giữa việc ăn 3 Sâu Hư Không đầu và ăn Rồng Nguyên Tố đầu, mục tiêu nào có mối liên hệ mật thiết và gia tăng khả năng chiến thắng cao hơn? Khi hai đội đổi mục tiêu chéo (Cross-trade), bên nào nắm giữ lợi thế thực sự?"*

### 1.3. Tại sao phải làm kiểm định này?
1. **Về mặt Khoa học Dữ liệu (Chương 1 - Biến định danh):**
   - Hoàn thiện mảnh ghép cuối cùng trong bộ công cụ Thống kê suy diễn: **Kiểm định tính độc lập Chi-square (χ²)** và phân tích **Tỷ số Chênh (Odds Ratio - OR)** trên bảng chéo 2x2.
2. **Về mặt Chiến thuật LMHT:**
   - Cung cấp cơ sở định lượng chính xác để các đội tuyển và người chơi giải tỏa tranh cãi: *Nên bỏ Rồng lấy Sâu hay bỏ Sâu lấy Rồng?*

---

## 2. PHƯƠNG PHÁP TOÁN THỐNG KÊ VÀ BẢNG CHÉO 2X2

Ta xây dựng bảng chéo phân loại 2x2 (Contingency Table) giữa việc **Có kiểm soát mục tiêu** và **Kết quả thắng/thua**:

```text
                  Thắng (1)    Thua (0)    Tổng
Có mục tiêu (1)       a           b       n_has = a + b
Không có (0)          c           d       n_no  = c + d
Tổng               a + c       b + d         n
```

### Các công thức tính toán:
1. **Kiểm định Chi-square độc lập (Chi-square test with Yates correction):**
   `χ² = Tổng [ (O - E)² / E ]` với bậc tự do `df = (2-1) * (2-1) = 1`.
2. **Tỷ số Chênh (Odds Ratio - OR):**
   `Odds Ratio = (a / b) / (c / d) = (a * d) / (b * c)`
   - `OR > 1`: Có mục tiêu làm tăng cơ hội chiến thắng.
   - `OR = 1`: Mục tiêu không ảnh hưởng gì đến kết quả.
   - `OR < 1`: Có mục tiêu làm giảm cơ hội chiến thắng.
3. **Sai số chuẩn logarit và Khoảng tin cậy 95% (Woolf Logit Method):**
   - `SE(ln OR) = Căn_bậc_hai( 1/a + 1/b + 1/c + 1/d )`
   - `CI_95% = [ exp(ln OR - 1.96 * SE) , exp(ln OR + 1.96 * SE) ]`

---

## 3. BẢNG KẾT QUẢ KIỂM ĐỊNH CHI-SQUARE VÀ ODDS RATIO

Dữ liệu được trích xuất từ CSDL chuẩn hóa `lol_live_data.db` (gồm 4,732 quan sát đội Đấu Giải và 2,018 quan sát đội Solo Rank):

| Môi Trường | Mục Tiêu Phân Tích | Thắng Khi Có | Thắng Khi Mất | Chi-square (χ²) | Chỉ Số p-value | Odds Ratio (OR) [CI 95%] | Tăng Cơ Hội (Relative Risk) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Đấu Giải (Pro Play)** | **3 Sâu Hư Không (>=3 Grubs)** | **55.81%** *(908/1627)* | **46.96%** *(1458/3105)* | `33.11` | `8.73 x 10^(-9)***` | **1.427** [1.265 - 1.609] | **1.19x** (Tă## 4. PHÂN TÍCH MA TRẬN KỊCH BẢN ĐỐI ĐẦU VÀ CHIA SÂU

### 4.1. Ma Trận 4 Kịch Bản Đối Đầu Tổng Quát (Decision Matrix)

| Môi Trường | Kịch Bản Tranh Chấp (Phút 5 - 10) | Tổng Đội (n) | Thắng | Thua | Tỷ Lệ Thắng (%) | Đánh Giá Chiến Thuật |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Đấu Giải (Pro Play)** | **1. Cả Hai (3 Sâu + Rồng 1)** | 651 | 447 | 204 | **68.66%** | 🏆 **Áp đảo hoàn toàn** (Làm chủ 3 đường) |
| **Đấu Giải (Pro Play)** | **2. Chỉ 3 Sâu (Bỏ Rồng 1)** | 976 | 461 | 515 | **47.23%** | ⚠️ **Lỗ vốn** (Tỷ lệ thắng rơi dưới 50%) |
| **Đấu Giải (Pro Play)** | **3. Chỉ Rồng 1 (Bỏ 3 Sâu)** | 1,715 | 959 | 756 | **55.92%** | ✅ **Có lời** (Chiến thuật đổi mục tiêu tối ưu) |
| **Đấu Giải (Pro Play)** | **4. Mất Cả Hai (0 Sâu + Mất Rồng)**| 1,390 | 499 | 891 | **35.90%** | ❌ **Khủng hoảng** (Nguy cơ thua rất cao) |
| **Solo Rank (Thách Đấu)**| **1. Cả Hai (3 Sâu + Rồng 1)** | 215 | 164 | 51 | **76.28%** | 🏆 **Hủy diệt trận đấu** (Thắng hơn 3/4 số trận) |
| **Solo Rank (Thách Đấu)**| **2. Chỉ 3 Sâu (Bỏ Rồng 1)** | 444 | 243 | 201 | **54.73%** | ✅ **Có lời** (Tự đẩy trụ lấy tiền giáp trụ) |
| **Solo Rank (Thách Đấu)**| **3. Chỉ Rồng 1 (Bỏ 3 Sâu)** | 505 | 291 | 214 | **57.62%** | ✅ **Có lời** (Tích lũy linh hồn rồng) |
| **Solo Rank (Thách Đấu)**| **4. Mất Cả Hai (0 Sâu + Mất Rồng)**| 854 | 311 | 543 | **36.42%** | ❌ **Khủng hoảng** |

---

### 4.2. Ma Trận 8 Tổ Hợp Chi Tiết (Rồng 1 x Số Lượng Sâu 0, 1, 2, 3)

| Trạng Thái Rồng 1 | Số Con Sâu Ăn Được | Tổng Trận (n) | Thắng | Thua | Tỷ Lệ Thắng (%) | Ý Nghĩa Thực Tế |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Mất Rồng 1** | **0 Sâu** | 668 | 210 | 458 | **31.44%** | ❌ Mất trắng toàn bộ mục tiêu |
| **Mất Rồng 1** | **1 Sâu** | 338 | 121 | 217 | **35.80%** | ❌ Bị ép sâu, chỉ vét được 1 con |
| **Mất Rồng 1** | **2 Sâu** | 384 | 168 | 216 | **43.75%** | ⚠️ Ăn 2 sâu nhưng vẫn lỗ vì mất Rồng |
| **Mất Rồng 1** | **3 Sâu** | 965 | 455 | 510 | **47.15%** | ⚠️ Đổi ngang 3 sâu lấy Rồng (Vẫn < 50%) |
| **Có Rồng 1** | **0 Sâu** | 1,000 | 536 | 464 | **53.60%** | ✅ Bỏ trắng Sâu để ăn chắc Rồng |
| **Có Rồng 1** | **1 Sâu** | 384 | 210 | 174 | **54.69%** | ✅ Ăn Rồng + Cử người vét 1 sâu phá bùa |
| **Có Rồng 1** | **2 Sâu** | 331 | 213 | 118 | **64.35%** | 🏆 Thắng giao tranh lớn cả 2 cánh |
| **Có Rồng 1** | **3 Sâu** | 646 | 442 | 204 | **68.42%** | 🏆 Làm chủ hoàn toàn bản đồ |

---

### 4.3. Kèo Đối Đầu Trực Tiếp: (1 Rồng + 1 Sâu) vs (0 Rồng + 2 Sâu)

Khảo sát đối đầu trực tiếp trên **370 trận đấu chuyên nghiệp** đúng kịch bản chia sâu:
* **Đội A: Ăn (1 Rồng + 1 Sâu)** $\rightarrow$ Thắng **206 / 370 trận (55.68%)**.
* **Đội B: Ăn (0 Rồng + 2 Sâu)** $\rightarrow$ Thắng **164 / 370 trận (44.32%)**.
* 👉 **Chênh lệch:** Đội ăn **1 Rồng + 1 Sâu** nắm ưu thế vượt trội **+11.36% Winrate** so với đội ăn 2 Sâu (nhưng mất Rồng).

---

## 5. PHÂN TÍCH CHUYÊN SÂU THEO NGHIỆP VỤ LMHT (DOMAIN KNOWLEDGE)

### 5.1. Tại sao Rồng Đầu Tiên lại có giá trị cao hơn 3 Sâu Hư Không ở Đấu Giải (OR 2.15 vs 1.43)?
1. **Tạo áp lực thời gian (Dragon Soul Clock):**
   - Trong Đấu Giải Chuyên Nghiệp, Rồng đầu tiên không chỉ là một chỉ số nguyên tố đơn lẻ, mà nó **kích hoạt đồng hồ đếm ngược Linh Hồn Rồng**. Đội ăn được Rồng 1 sẽ luôn nắm quyền chủ động kiểm soát tầm nhìn ở các hang Rồng tiếp theo (Rồng 2, Rồng 3, Rồng 4).
   - Đội đối phương sẽ luôn bị đặt vào thế bị động: bắt buộc phải giao tranh ở các mốc Rồng Linh Hồn dù đội hình chưa đạt ngưỡng trang bị.
2. **Khả năng phòng ngự trụ ở Đấu Giải quá tốt:**
   - Bùa lợi Sâu Hư Không giúp tăng sát thương lên trụ. Tuy nhiên, ở Đấu Giải, các tuyển thủ bọc lót trụ và dọn lính (Wave Clear) rất nhanh, khiến đội ăn 3 Sâu rất khó tận dụng bùa lợi để đục sập trụ 1 sớm.
   - Kết quả: Khi đổi chéo mục tiêu, đội **Chỉ ăn Sâu (bỏ Rồng)** chỉ đạt tỷ lệ thắng **47.23%** (thua thiệt rõ rệt so với đội **Chỉ ăn Rồng** đạt **55.92%**).

### 5.2. Tại sao chiến thuật "Ăn 1 Rồng + Vét 1 Sâu" lại tối ưu?
* Khi đội bạn quyết định tập trung ăn Rồng 1, người đi đường trên (Top) hoặc đường giữa (Mid) chỉ cần tranh cướp được **đúng 1 con Sâu Hư Không**:
  - Đối phương sẽ bị chặn đứng ở mốc **2 Sâu** (không thể kích hoạt bùa 3 sâu đợt 1 và mất đi cơ hội triệu hồi bọ đợt 2).
  - Đội bạn vừa có Rồng 1 (tích lũy linh hồn), vừa phá vỡ chiến thuật của đối thủ, đẩy tỷ lệ thắng của đối phương xuống chỉ còn **44.32%**.

### 5.3. Tại sao 3 Sâu Hư Không ở Solo Rank lại có giá trị cao hơn hẳn Pro Play (OR 2.03 vs 1.43)?
* **Khả năng tự lăn cầu tuyết cá nhân (Solo Carry):**
  - Trong rank Thách Đấu, người chơi không có sự bọc lót bảo vệ trụ từ đồng đội. Khi người đi đường trên (Top) hoặc đường giữa (Mid) có bùa 3 Sâu, họ có thể tự tay bào sạch **5 lớp giáp trụ (125 vàng/lớp = 625 vàng)** và lấy luôn 250 vàng Trụ Đầu.
  - Lượng tiền này đổ thẳng vào túi của 1 cá nhân carry, giúp họ lập tức vượt ngưỡng sức mạnh để snowball cả trận đấu.

---

## 6. KẾT LUẬN & ỨNG DỤNG CHO DỰ ÁN

1. **Kết luận khoa học:**
   - Mối quan hệ giữa mục tiêu lớn lúc 10 phút và kết quả trận đấu có ý nghĩa thống kê cực kỳ mạnh mẽ (`p < 10^(-8)` ở cả 4 phép kiểm định Chi-square).
   - Rồng Nguyên Tố đầu tiên có sức nặng chuyển hóa chiến thắng cao hơn 3 Sâu Hư Không (Odds Ratio 2.15 vs 1.43 ở Pro Play).
2. **Ứng dụng cho Giai đoạn 3 (Machine Learning):**
   - Đưa cả 2 biến tương tác `has_first_dragon` và `has_3_grubs` cùng biến kết hợp `double_neutral_control = has_first_dragon * has_3_grubs` vào bộ đặc trưng (Feature Engineering) của Mô hình Snowball Phút 10.g rank Thách Đấu, người chơi không có sự bọc lót bảo vệ trụ từ đồng đội. Khi người đi đường trên (Top) hoặc đường giữa (Mid) có bùa 3 Sâu, họ có thể tự tay bào sạch **5 lớp giáp trụ (125 vàng/lớp = 625 vàng)** và lấy luôn 250 vàng Trụ Đầu.
  - Lượng tiền này đổ thẳng vào túi của 1 cá nhân carry, giúp họ lập tức vượt ngưỡng sức mạnh để snowball cả trận đấu.

### 5.3. Sức mạnh của kịch bản "Ăn Trọn Cả Hai" (Double Neutral Control)
* Nếu một đội kiểm soát được cả 3 Sâu + Rồng 1, tỷ lệ thắng vọt lên tới **68.66%** ở Đấu Giải và **76.28%** ở Solo Rank.
* Điều này chứng minh: Đội ăn được cả 2 mục tiêu ở phút 10 chắc chắn là đội đã làm chủ hoàn toàn thế trận đi đường ở cả 3 khu vực đường (Priroty Top, Mid, Bot).

---

## 6. KẾT LUẬN & ỨNG DỤNG CHO DỰ ÁN

1. **Kết luận khoa học:**
   - Mối quan hệ giữa mục tiêu lớn lúc 10 phút và kết quả trận đấu có ý nghĩa thống kê cực kỳ mạnh mẽ (`p < 10^(-8)` ở cả 4 phép kiểm định Chi-square).
   - Rồng Nguyên Tố đầu tiên có sức nặng chuyển hóa chiến thắng cao hơn 3 Sâu Hư Không (Odds Ratio 2.15 vs 1.43 ở Pro Play).
2. **Ứng dụng cho Giai đoạn 3 (Machine Learning):**
   - Đưa cả 2 biến tương tác `has_first_dragon` và `has_3_grubs` cùng biến kết hợp `double_neutral_control = has_first_dragon * has_3_grubs` vào bộ đặc trưng (Feature Engineering) của Mô hình Snowball Phút 10.
