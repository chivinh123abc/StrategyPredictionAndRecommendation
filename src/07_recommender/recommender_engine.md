> **Giả lập cấm/chọn hybrid:** chạy `.\.venv\Scripts\python.exe src/07_recommender/simulate_draft_match.py` tại thư mục gốc để mở menu. Có historical + content-based/cosine, gợi ý theo lượt, chọn tay/why/swap và lưu phiên. [Hướng dẫn](../../docs/GIA_LAP_BAN_PICK.md). Đã kiểm chứng 24 tests và 5 kịch bản; chưa có bằng chứng tối ưu toàn cục/tăng thắng.

> **Content-based Chương 6 đã kiểm chứng:** xem [minh chứng và lệnh chạy](../../docs/CHUONG_6_CONTENT_BASED.md); hỗ trợ `--content-based --seed-champion` và `--content-player`.

> **Integrity v2:** Nội dung dưới đây là thiết kế/lịch sử trước đợt sửa. Hành vi hiện hành, các giới hạn và lệnh chạy được mô tả tại [INTEGRITY_V2.md](../../docs/INTEGRITY_V2.md). Không dùng các tỷ lệ/kết luận cũ làm bằng chứng kết quả hiện tại.

# BÁO CÁO KHOA HỌC: HỆ THỐNG GỢI Ý CẤM/CHỌN THÔNG MINH, NHẬN DIỆN LỖ HỔNG & THẺ ĐIỀU KIỆN THẮNG (TASK 3.5)

## THÔNG TIN TỔNG QUAN
- **Dự án:** Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI), Dự Đoán Thắng Thua Sớm 2 Giai Đoạn & Đối Chiếu Chiến Thuật Đấu Giải (Pro Play) vs Đấu Xếp Hạng (Solo Queue) - LMHT.
- **Học phần:** Nhập môn Khoa học Dữ liệu - PTIT (Giảng viên: TS. Thái Tuyết Hải).
- **Mã nguồn thực thi:** [`src/07_recommender/recommender_engine.py`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/src/07_recommender/recommender_engine.py)
- **Tệp đóng gói mô hình:** [`models/recommender_engine.pkl`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/models/recommender_engine.pkl)
- **Danh mục tài khoản tuyển thủ:** [`data/pro_player_accounts.json`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/data/pro_player_accounts.json)

---

## 1. ĐẶT VẤN ĐỀ & Ý NGHĨA KHOA HỌC (CHƯƠNG 6: HỆ THỐNG GỢI Ý)

Trong thể thao điện tử đỉnh cao (Pro Play), giai đoạn Cấm/Chọn (Draft Phase) quyết định tới **40-50% kết quả trận đấu**. Một lượt cấm chính xác vào "tướng tủ" của tuyển thủ đối phương, hoặc một lượt chọn "con bài trừng phạt" (Punisher Pick) có thể bóp nghẹt hoàn toàn ý đồ chiến thuật của đối thủ ngay từ phút 0.

Hệ thống Gợi ý Cấm/Chọn Thông minh (Task 3.5) giải quyết 4 bài toán lớn:
1. **Target Ban cá nhân hóa:** *"Cần cấm những con tướng nào khi đối đầu với Keria, Chovy, Faker, Kiaya hay Levi?"*
2. **Meta Pick & Synergy:** *"Ở vị trí Bot/Mid, con tướng nào vừa khắc chế đối thủ cùng đường, vừa tương thích với đồng đội và cân bằng lượng sát thương AD/AP/CC?"*
3. **Draft Flaw & Punisher:** *"Khi đối thủ lộ sơ hở (chọn 4 tướng cận chiến Heavy Melee hoặc Full AD), con bài nào sẽ trừng phạt nặng nề nhất?"*
4. **Win Condition Card (ADR-014):** *"Sau khi hoàn tất 5 tướng, đội hình này đánh theo trường phái nào, ai là chủ lực, điểm rơi sức mạnh ở đâu và điều kiện thua cần tránh là gì?"*

---

## 2. KIẾN TRÚC 4 PHÂN HỆ CHIẾN THUẬT CỐT LÕI

```
                                  [ DỮ LIỆU ĐẦU VÀO ]
           ┌───────────────────────────────┴───────────────────────────────┐
           ▼                                                               ▼
   CSDL Đấu Giải (30,000 dòng)                                Solo Rank 30 trận gần nhất
   `tournament_players` (SQLite)                              `pro_player_accounts.json`
           │                                                               │
           ▼                                                               ▼
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                       PHÂN HỆ 1: TARGET BAN LAI GHÉP                            │
 │  - Đấu giải (65%): Tần suất + Winrate Bayes + Laning Dominance (GD10/CSD10)    │
 │  - Solo Rank (35%): Nhận diện Đột biến Spam Rank (Spike Pick Rate + WR > 70%)  │
 │  -> Xuất Top 3-5 Lượt CẤM Bắt Buộc (🚨 Pocket Pick Alert / 🔥 Tướng Tủ)         │
 └─────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                   PHÂN HỆ 2: GỢI Ý CHỌN TƯỚNG CHUẨN META                        │
 │  - Counter-Pick: Khắc chế trực tiếp tướng địch cùng đường                       │
 │  - Duo Synergy: Luật kết hợp cặp đôi (Lucian-Nami, Orianna-J4, Xayah-Rakan)     │
 │  - Team Composition Balance: Bù trừ sát thương AP, Khống chế CC, Chống chịu Tank│
 └─────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                 PHÂN HỆ 3: QUÉT LỖ HỔNG & CON BÀI TRỪNG PHẠT                    │
 │  - Quét 4 Lỗ Hổng: Heavy Melee (3-4 cận chiến), Full AD, Zero Hard CC, Squishy  │
 │  - Con bài trừng phạt: Illaoi, Darius, Malphite, Rammus, Master Yi, Nocturne    │
 │  -> Tăng vọt +12% đến +18.5% Winrate dự đoán (Hiện tượng Siwoo Illaoi LCK)      │
 └─────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │               PHÂN HỆ 4: THẺ ĐIỀU KIỆN THẮNG CHIẾN THUẬT (ADR-014)              │
 │  - Tích hợp K-Means models/archetype_kmeans.pkl (4 Trường phái Đội hình)       │
 │  - Trích xuất: Core Carry, Power Spike Timing, Primary Objective, Win/Lose Con  │
 └─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. PHÂN HỆ 1: CẤM LAI GHÉP THEO TUYỂN THỦ (HYBRID OPPONENT TARGET BAN)

### A. Phương pháp Toán học & Công thức
Hệ thống sử dụng cơ chế lai ghép 2 tầng:

1. **Chỉ số Đe Dọa Đấu Giải (Tournament Threat Index - TTI, Trọng số 65%):**
   - **Tỷ lệ thắng làm mịn Bayes (Bayesian Smoothed Winrate):**
     $$WR_{bayes} = \frac{\text{Wins} + C \cdot WR_{global}}{\text{Games} + C}$$
     *(với hằng số làm mịn $C = 5$, $WR_{global} = 0.50$ để tránh sai lệch khi mẫu nhỏ).*
   - **Chỉ số Đè Đường 10 phút (Laning Dominance Score):**
     $$LD_{10} = \frac{\overline{\text{golddiffat10}}}{500} + \frac{\overline{\text{csdiffat10}}}{15}$$
   - **Chỉ số Đe dọa Đấu giải tổng hợp:**
     $$TTI = 0.35 \times \text{PickShare} + 0.35 \times WR_{bayes} + 0.20 \times \text{Norm}(LD_{10}) + 0.10 \times \text{Norm}(KDA)$$

2. **Chỉ số Đột Biến Solo Rank (Solo Rank Threat Index - STI, Trọng số 35%):**
   - Đọc 30-50 trận gần nhất từ `pro_player_accounts.json`.
   - Phát hiện đột biến (Spike): Tần suất chọn tăng vọt và Tỷ lệ thắng $\ge 70\%$.
   - **Chỉ số Đe dọa Rank:**
     $$STI = 0.50 \times WR_{rank} + 0.35 \times \left(\frac{\text{Games}_{rank}}{15}\right) + (0.15 \text{ nếu có Spike})$$

3. **Điểm Đe Dọa Lai Ghép (Hybrid Threat Score):**
   $$HTS = 0.65 \times TTI + 0.35 \times STI + (0.08 \text{ nếu là Pocket Pick})$$

### B. Kết quả Thực nghiệm trên các Tuyển thủ Tiêu biểu:

#### 1. Keria (Hỗ Trợ - T1)
- **Top 1 [🚨 POCKET PICK SPAM RANK] BARD (0.7382):** Đấu giải 23 trận (WR 78.3%, KDA 6.17) + Solo Rank 18 trận (WR 77.8%, Spike liên tục).
- **Top 2 [🚨 POCKET PICK SPAM RANK] CAMILLE (0.6154):** Đấu giải 12 trận (WR 66.7%, GD10: +223g) + Solo Rank 8 trận (WR 75.0%, Bài dị Support).
- **Top 3 [🔥 TƯỚNG TỦ THƯƠNG HIỆU] RENATA GLASC (0.5249):** Đấu giải 20 trận (WR 65.0%, KDA 4.51).

#### 2. Chovy (Đường Giữa - Gen.G)
- **Top 1 [🚨 POCKET PICK SPAM RANK] YONE (0.7127):** Đấu giải 6 trận (WR 83.3%, KDA 7.67) + Solo Rank 20 trận (WR 80.0%).
- **Top 2 [🚨 POCKET PICK SPAM RANK] TRISTANA (0.5967):** Solo Rank 10 trận (WR 70.0%, Đè đường Mid).
- **Top 3 [🔥 TƯỚNG TỦ THƯƠNG HIỆU] AHRI (0.5866):** Đấu giải 12 trận (WR 66.7%, GD10: +302g, KDA 6.05).
- **Top 4 [🔥 TƯỚNG TỦ THƯƠNG HIỆU] GALIO (0.5721):** Đấu giải 29 trận (WR 93.1%, KDA 8.49).

#### 3. Kiaya (Đường Trên - GAM Esports)
- **Top 1 [🚨 POCKET PICK SPAM RANK] RUMBLE (0.8211):** Đấu giải 22 trận (WR 72.7%, GD10: +285g) + Solo Rank 15 trận (WR 80.0%).
- **Top 2 [🚨 POCKET PICK SPAM RANK] URGOT (0.5733):** Solo Rank 5 trận (WR 80.0%, Đè tướng cận chiến).
- **Top 3 [🔥 TƯỚNG TỦ THƯƠNG HIỆU] GWEN (0.5084):** Đấu giải 15 trận (WR 66.7%, GD10: +89g).

---

## 4. PHÂN HỆ 2: GỢI Ý CHỌN TƯỚNG CHUẨN META, PHÂN TẦNG KHU VỰC & KHẮC CHẾ ĐƯỜNG TỔNG QUÁT (UNIVERSAL COUNTER-PICK & SYNERGY ENGINE)

> Xem tài liệu đặc tả toán học đầy đủ tại: [`docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md`](../../docs/CO_CHE_BAN_PICK_COUNTER_VA_PHAN_TANG_KHU_VUC.md).

Hệ thống hoạt động 100% bằng thuật toán tổng quát trên dữ liệu thực nghiệm (Zero-Hardcode), hỗ trợ 8 chế độ khu vực (`LCK`, `LPL`, `LCP`, `WLDS`/CKTG, `MSI`, `EWC`, `INTERNATIONAL`, `ALL`) và tự động chuyển đổi giữa 2 chế độ:
1. **Chế độ `BLIND PICK` (Đối thủ CHƯA lộ tướng cùng đường):**
   - Ưu tiên Điểm Hiệu quả Meta (`0.36 * eff_norm`), Điểm Tương thích Cặp đôi (`0.24 * synergy_score`), Điểm Cân bằng Đội hình (`0.24 * balance_score`) và Điểm Tướng Tủ tuyển thủ (`player_bonus`).
2. **Chế độ `COUNTER PICK` (Đối thủ ĐÃ lộ tướng cùng đường - Áp dụng trên toàn bộ 5 vị trí & 3,098 cặp đối đầu 1v1):**
   - **Nhận diện 1-1 tướng cùng đường (`_infer_enemy_lane_assignment`):** Xác định chính xác tướng địch đang đứng ở đường nào.
   - **Ngưỡng Loại Bỏ Cứng Tổng Quát (Universal Hard Cut-off):** Loại bỏ hoàn toàn mọi ứng viên có tỷ lệ thắng đối đầu $< 47.5\%$ (mẫu $\ge 3$ trận) HOẶC bị đè đường phút 10 ($\text{GD@10} < -110\text{g}$ đối với `Top/Jng/Mid/Bot`, $< -150\text{g}$ đối với `Sup` nếu không có tỷ lệ lật kèo giao tranh $\ge 52.5\%$).
   - **Khóa Điểm Tướng Tủ (`player_bonus`) khi gặp kèo dưới:** Cắt giảm 85–90% `player_bonus` nếu tướng tủ chưa được kiểm chứng thắng/hòa đường trước tướng đối diện.
   - **Làm mịn Bayes ($C=10.0$), Độ tin cậy mẫu ($\alpha = \frac{n}{n+8}$) & Lọc độ tinh khiết vị trí (Role Purity Filter):** Ngăn các tướng trái vị trí có mẫu siêu nhỏ (2–5 trận) làm nhiễu gợi ý.
3. **Điểm Tương thích Cặp đôi (Duo Synergy Score) & Cân bằng Đội hình (Composition Balance Bonus):**
   - Kết hợp dữ liệu thực chiến từ CSDL (hàng nghìn cặp `Bot-Sup`, `Mid-Jng`, `Top-Jng`) với bù đắp sát thương AP/AD, khống chế cứng (Hard CC) và chống chịu (Tank/Frontline).

---

## 5. PHÂN HỆ 3: QUÉT LỖ HỔNG CẤM/CHỌN & CON BÀI TRỪNG PHẠT (PUNISHER ENGINE)

Quét và phát hiện 4 lỗ hổng cấm/chọn chí mạng:

| Lỗ Hổng Chiến Thuật | Điều Kiện Kích Hoạt | Mức Độ | Con Bài Trừng Phạt (Punisher Picks) | Tác Động Tỷ Lệ Thắng Dự Đoán |
| :--- | :--- | :---: | :--- | :---: |
| **1. Heavy Melee** | Địch chọn $\ge 3$ tướng Cận chiến | **CRITICAL** | **Illaoi** (Top), **Cassiopeia** (Mid), **Brand** (Jng/Sup), **Darius** (Top) | **+15.0% đến +18.5%** *(Chiến thuật Siwoo LCK)* |
| **2. Full AD** | 100% Sát thương vật lý (0 AP) | **CRITICAL** | **Malphite** (Top), **Rammus** (Jng), **Taric** (Sup), **K'Sante** (Top) | **+16.0% đến +17.0%** |
| **3. Zero Hard CC** | Chỉ số CC trung bình $< 0.40$ | **HIGH** | **Master Yi** (Jng), **Katarina** (Mid), **Zeri** (Bot), **Samira** (Bot) | **+13.0% đến +15.5%** |
| **4. Full Squishy** | 0 Tướng đỡ đòn / chống chịu | **HIGH** | **Nocturne** (Jng), **Jarvan IV** (Jng), **Hecarim** (Jng), **Akali** (Mid) | **+12.5% đến +13.5%** |

---

## 6. PHÂN HỆ 4: ENGINE TRÍCH XUẤT THẺ ĐIỀU KIỆN THẮNG (WIN CONDITION CARD - ADR-014)

Tích hợp mô hình K-Means `models/archetype_kmeans.pkl` để xuất Thẻ Chiến thuật hoàn chỉnh:

```
==========================================================================================
🏆 TRƯỜNG PHÁI ĐỘI HÌNH: [EARLY SNOWBALL & DIVE]
📊 Radar 5 trục: Early: 0.945 | Scaling: 0.488 | Combat: 0.52 | Pick: 0.927 | Obj: 0.63
==========================================================================================
🎯 THẺ CHIẾN THUẬT (WIN CONDITION CARD):
   1. Chủ lực gánh đội (Core Carry): ⭐ LeBlanc
   2. Điểm rơi sức mạnh: ⏱️ Đầu trận (Phút 1 đến Phút 20 - Trước mốc Baron xuất hiện)
   3. Mục tiêu số 1: 🐉 Sâu Hư Không đợt 1 + Trụ Đầu (First Tower) trước phút 14
   4. Điều kiện thắng: ✅ Tạo chênh lệch >= 2,000 vàng lúc 10 phút, băng trụ 2 cánh liên tục, ép đối thủ vỡ trận trước 25 phút.
   5. Điều kiện thua cần tránh: ❌ Bị đối thủ phòng ngự kéo dài trận đấu qua phút 30 khi chất tướng hết thời gian lăn cầu tuyết.
   6. Việc NÊN làm: Xâm lăng rừng đối phương sớm, Gank tập trung đường Bot lấy giáp trụ, Ăn trọn 3 Sâu Hư Không đợt 1
   7. Việc KHÔNG ĐƯỢC làm: Đánh chậm chờ đồ, Bỏ mục tiêu lớn giai đoạn đầu, Để đối thủ kéo late
```

---

## 7. ĐÓNG GÓI & SẴN SÀNG TÍCH HỢP REST API (GIAI ĐOẠN 4)

- Toàn bộ 4 phân hệ đã được đóng gói thành một đối tượng hợp nhất trong [`models/recommender_engine.pkl`](file:///d:/Chivinh/2026_MonHoc/Nhập%20môn%20khoa%20học%20dữ%20liệu/Project/models/recommender_engine.pkl).
- Sẵn sàng cung cấp các Endpoints cho FastAPI Backend (Giai đoạn 4):
  - `POST /api/v1/target-ban`: Cấm mục tiêu theo tuyển thủ.
  - `POST /api/v1/recommend-pick`: Gợi ý chọn tướng theo meta.
  - `POST /api/v1/detect-flaws`: Quét lỗ hổng & gợi ý con bài trừng phạt.
  - `POST /api/v1/win-condition`: Trích xuất Radar & Thẻ điều kiện thắng.
  - `POST /api/v1/players/link-account`: Đăng ký tài khoản Riot ID cho tuyển thủ mới.
