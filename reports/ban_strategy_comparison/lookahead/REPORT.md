> **LỊCH SỬ — đã ngừng sử dụng24/11/2026.** Lookahead đã được gỡ theo yêu cầu người dùng; tài liệu/đầu ra này chỉ giữ minh chứng phiên cũ, không phải chức năng hiện hành. Xem `reports/legacy_contextual_comparison/COMPARISON.md` và `docs/BAN_LEGACY_VA_CONTEXTUAL.md` cho phạm vi mới.

# WLDS: 5 ván draft Fearless — T1 vs Gen.G

Đây là 5 phiên draft liên tiếp, không mô phỏng trận chiến hoặc gán tỉ số thắng/thua. Không dùng kết quả giả để ép BO5 đi đủ5ván.

Luật: [Fearless của Riot](https://lolesports.com/en-GB/news/fst-2025-primer). Tướng đã pick bởi bất kỳ đội nào bị khóa cho cả hai đội đến hết series; ban thường chỉ có hiệu lực trong ván đó. Ván5 không reset pool.

Snapshot: `{'region': 'WLDS', 'dataset_patch': '16.20', 'data_through': '2026-11-09T00:56:00+00:00', 'requested_as_of': '2026-11-13T23:59:59.999999999+00:00', 'staleness_days': 4, 'history_games': 106, 'patch_games': 94, 'lookback_days': 60, 'half_life_days': 21.0, 'claim': 'historical_snapshot_not_live_meta'}`.

Lịch thử nghiệm: giữ T1 ở Blue và Gen.G ở Red; bên pick trước luân phiên Blue/Red. Đây là lịch chỉ định cho demo, không phải mô phỏng quyền First Selection dựa vào thắng/thua.

Cho phép test chọn số1 khi thiếu tin cậy: True. Không nâng nhãn counter hoặc độ tin cậy khi bật chế độ này.

Chiến lược ban: lookahead. Chế độ lookahead chỉ xét nhánh giới hạn trong ván; chưa tối ưu phân bổ tướng qua toàn BO5.

Ứng viên: ít nhất 1 lần quan sát đúng role; ngưỡng bằng chứng 5 trận. Ưu tiên ứng viên đủ mẫu trước; chỉ xét lớp ít mẫu khi không còn ứng viên đủ mẫu ở role đang xét. Khi so giữa các role mở cũng ưu tiên lớp đủ mẫu; người dùng wishlist vẫn là lựa chọn chủ đích riêng. Đây là pool gợi ý có dữ liệu, chưa là danh mục tướng hợp lệ chính thức của sự kiện.

Association dương được shrink thêm theo số mẫu cặp; association âm theo số quan sát đồng đội. Không cho một cặp một-mẫu tạo bonus lift lớn như cặp có nhiều mẫu.

## Ván 1 — T1 chọn trước

Fearless khóa 0 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Nautilus, Alistar, Olaf | Jhin, Ashe |
| Gen.G | Renata Glasc, Nocturne, Jayce | Karma, Lulu |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Gnar | Rumble |
| jng | Vi | Qiyana |
| mid | Syndra | Cassiopeia |
| bot | Ezreal | Kai'Sa |
| sup | Leona | Seraphine |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Nautilus | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Renata Glasc | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Alistar | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Nocturne | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Olaf | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Jayce | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Vi | jng | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Qiyana | jng | Coverage 100%; chưa xác nhận counter |
| 9 | Gen.G | Pick 2 | Cassiopeia | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Syndra | mid | Coverage 46%; chưa xác nhận counter |
| 11 | T1 | Pick 3 | Ezreal | bot | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Rumble | top | Coverage 33%; chưa xác nhận counter |
| 13 | Gen.G | Ban 4 | Karma | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Jhin | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Lulu | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Ashe | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Seraphine | sup | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Gnar | top | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Leona | sup | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Kai'Sa | bot | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 1, ít mẫu 8, chưa thấy 1, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 7, chưa thấy 2, thiếu anchor 0.

### Căn cứ và nhánh từng lượt ban

| Lượt | Đội | Ban | Lý do | Nhánh đáp trả được xét |
|---:|---|---|---|---|
| 1 | T1 | Nautilus | Mất pool địch 0.0033; chi phí tự cấm 0.0025; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; 2 nhánh, giá trị dự kiến -0.0086 | ban Nocturne (56% trong nhánh xét); ban Qiyana (44% trong nhánh xét) |
| 2 | Gen.G | Renata Glasc | Mất pool địch 0.0117; chi phí tự cấm 0.0052; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0241 | ban Nocturne (58% trong nhánh xét); ban Qiyana (42% trong nhánh xét) |
| 3 | T1 | Alistar | Mất pool địch 0.0017; chi phí tự cấm 0.0007; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; 2 nhánh, giá trị dự kiến -0.0107 | ban Nocturne (58% trong nhánh xét); ban Qiyana (42% trong nhánh xét) |
| 4 | Gen.G | Nocturne | Mất pool địch 0.0086; chi phí tự cấm 0.0032; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0295 | ban Qiyana (54% trong nhánh xét); ban Vi (46% trong nhánh xét) |
| 5 | T1 | Olaf | Mất pool địch 0.0086; chi phí tự cấm 0.0074; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; 2 nhánh, giá trị dự kiến -0.0022 | ban Qiyana (54% trong nhánh xét); ban Vi (46% trong nhánh xét) |
| 6 | Gen.G | Jayce | Mất pool địch 0.0045; chi phí tự cấm 0.0008; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0194 | pick Qiyana (53% trong nhánh xét); pick Vi (47% trong nhánh xét) |
| 13 | Gen.G | Karma | Mất pool địch 0.0026; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0044 | ban Seraphine (50% trong nhánh xét); ban Lulu (50% trong nhánh xét) |
| 14 | T1 | Jhin | Mất pool địch 0.0075; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0094 | ban Lulu (50% trong nhánh xét); ban Seraphine (50% trong nhánh xét) |
| 15 | Gen.G | Lulu | Mất pool địch 0.0052; chi phí tự cấm 0.0028; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0041 | ban Seraphine (51% trong nhánh xét); ban Rakan (49% trong nhánh xét) |
| 16 | T1 | Ashe | Mất pool địch 0.0006; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; 2 nhánh, giá trị dự kiến 0.0108 | pick Rakan (52% trong nhánh xét); pick Seraphine (48% trong nhánh xét) |

## Ván 2 — Gen.G chọn trước

Fearless khóa 10 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Nocturne, Pantheon, Nautilus | Alistar, Lulu |
| Gen.G | Jayce, Jarvan IV, Ambessa | Wukong, K'Sante |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Renekton | Olaf |
| jng | Xin Zhao | Lee Sin |
| mid | Orianna | Galio |
| bot | Kalista | Jhin |
| sup | Renata Glasc | Rakan |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Jayce | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jarvan IV | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Pantheon | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Ambessa | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Nautilus | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Olaf | top | Chưa lộ địch |
| 8 | T1 | Pick 1 | Renata Glasc | sup | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | Kalista | bot | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Jhin | bot | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Lee Sin | jng | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Orianna | mid | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Alistar | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Wukong | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Lulu | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | K'Sante | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Renekton | top | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Galio | mid | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Rakan | sup | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Xin Zhao | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 1, ít mẫu 9, chưa thấy 0, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 2, ít mẫu 7, chưa thấy 1, thiếu anchor 0.

### Căn cứ và nhánh từng lượt ban

| Lượt | Đội | Ban | Lý do | Nhánh đáp trả được xét |
|---:|---|---|---|---|
| 1 | Gen.G | Jayce | Mất pool địch 0.0038; chi phí tự cấm 0.0020; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; 2 nhánh, giá trị dự kiến -0.0123 | ban Nocturne (69% trong nhánh xét); ban Olaf (31% trong nhánh xét) |
| 2 | T1 | Nocturne | Mất pool địch 0.0147; chi phí tự cấm 0.0067; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; 2 nhánh, giá trị dự kiến 0.0155 | ban Olaf (53% trong nhánh xét); ban Jarvan IV (47% trong nhánh xét) |
| 3 | Gen.G | Jarvan IV | Mất pool địch 0.0088; chi phí tự cấm 0.0058; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; 2 nhánh, giá trị dự kiến -0.0098 | ban Olaf (52% trong nhánh xét); ban Orianna (48% trong nhánh xét) |
| 4 | T1 | Pantheon | Mất pool địch 0.0039; chi phí tự cấm 0.0008; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; 2 nhánh, giá trị dự kiến 0.0166 | ban Olaf (52% trong nhánh xét); ban Orianna (48% trong nhánh xét) |
| 5 | Gen.G | Ambessa | Mất pool địch 0.0024; chi phí tự cấm 0.0005; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; 2 nhánh, giá trị dự kiến -0.0207 | ban Olaf (52% trong nhánh xét); ban Orianna (48% trong nhánh xét) |
| 6 | T1 | Nautilus | Mất pool địch 0.0067; chi phí tự cấm 0.0029; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; 2 nhánh, giá trị dự kiến 0.0551 | pick Orianna (52% trong nhánh xét); pick Olaf (48% trong nhánh xét) |
| 13 | T1 | Alistar | Mất pool địch 0.0063; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; 2 nhánh, giá trị dự kiến -0.0027 | ban Renekton (53% trong nhánh xét); ban K'Sante (47% trong nhánh xét) |
| 14 | Gen.G | Wukong | Mất pool địch 0.0059; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; 2 nhánh, giá trị dự kiến 0.0140 | ban Akali (50% trong nhánh xét); ban Rakan (50% trong nhánh xét) |
| 15 | T1 | Lulu | Mất pool địch 0.0074; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; 2 nhánh, giá trị dự kiến -0.0018 | ban Renekton (52% trong nhánh xét); ban K'Sante (48% trong nhánh xét) |
| 16 | Gen.G | K'Sante | Mất pool địch 0.0047; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; 2 nhánh, giá trị dự kiến 0.0058 | pick Renekton (60% trong nhánh xét); pick Trundle (40% trong nhánh xét) |

## Ván 3 — T1 chọn trước

Fearless khóa 20 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Pantheon, Yunara, Xayah | Trundle, Naafiri |
| Gen.G | Akali, Nocturne, Jarvan IV | Viktor, Taliyah |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Jayce | Ambessa |
| jng | Wukong | Skarner |
| mid | Ahri | Locke |
| bot | Lucian | Ashe |
| sup | Lulu | Nautilus |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Pantheon | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Akali | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Yunara | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Nocturne | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Xayah | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Jarvan IV | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Jayce | top | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Nautilus | sup | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Ambessa | top | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Wukong | jng | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Lulu | sup | Coverage 50%; chưa xác nhận counter |
| 12 | Gen.G | Pick 3 | Locke | mid | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Viktor | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Trundle | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Taliyah | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Naafiri | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Ashe | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Lucian | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Ahri | mid | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Skarner | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 0, ít mẫu 6, chưa thấy 4, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 5, chưa thấy 4, thiếu anchor 0.

### Căn cứ và nhánh từng lượt ban

| Lượt | Đội | Ban | Lý do | Nhánh đáp trả được xét |
|---:|---|---|---|---|
| 1 | T1 | Pantheon | Mất pool địch 0.0001; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; 2 nhánh, giá trị dự kiến -0.0037 | ban Nocturne (71% trong nhánh xét); ban Jarvan IV (29% trong nhánh xét) |
| 2 | Gen.G | Akali | Mất pool địch 0.0056; chi phí tự cấm 0.0020; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0526 | ban Nocturne (71% trong nhánh xét); ban Jarvan IV (29% trong nhánh xét) |
| 3 | T1 | Yunara | Mất pool địch 0.0031; chi phí tự cấm 0.0018; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; 2 nhánh, giá trị dự kiến -0.0044 | ban Nocturne (71% trong nhánh xét); ban Jarvan IV (29% trong nhánh xét) |
| 4 | Gen.G | Nocturne | Mất pool địch 0.0189; chi phí tự cấm 0.0080; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0083 | ban Jarvan IV (54% trong nhánh xét); ban Caitlyn (46% trong nhánh xét) |
| 5 | T1 | Xayah | Mất pool địch 0.0012; chi phí tự cấm 0.0002; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0075 | ban Jarvan IV (55% trong nhánh xét); ban Caitlyn (45% trong nhánh xét) |
| 6 | Gen.G | Jarvan IV | Mất pool địch 0.0142; chi phí tự cấm 0.0062; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0224 | pick Lucian (50% trong nhánh xét); pick Ryze (50% trong nhánh xét) |
| 13 | Gen.G | Viktor | Mất pool địch 0.0069; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0006 | ban Caitlyn (62% trong nhánh xét); ban Ziggs (38% trong nhánh xét) |
| 14 | T1 | Trundle | Mất pool địch 0.0063; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0160 | ban Caitlyn (61% trong nhánh xét); ban Ziggs (39% trong nhánh xét) |
| 15 | Gen.G | Taliyah | Mất pool địch 0.0014; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0006 | ban Caitlyn (58% trong nhánh xét); ban Ziggs (42% trong nhánh xét) |
| 16 | T1 | Naafiri | Mất pool địch 0.0070; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; 2 nhánh, giá trị dự kiến 0.0224 | pick Ziggs (51% trong nhánh xét); pick Sivir (49% trong nhánh xét) |

## Ván 4 — Gen.G chọn trước

Fearless khóa 30 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Camille, Viktor, Akali | Ornn, Jax |
| Gen.G | Milio, Karma, Xayah | Rell, Bard |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | K'Sante | Zaahen |
| jng | Jarvan IV | Nocturne |
| mid | Ryze | Taliyah |
| bot | Caitlyn | Corki |
| sup | Shen | Alistar |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Milio | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Camille | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Karma | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Viktor | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Xayah | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Akali | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Nocturne | jng | Chưa lộ địch |
| 8 | T1 | Pick 1 | Jarvan IV | jng | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | K'Sante | top | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Taliyah | mid | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Alistar | sup | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Caitlyn | bot | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Ornn | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Rell | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Jax | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Bard | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Ryze | mid | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Corki | bot | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Zaahen | top | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Shen | sup | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: T1 Shen (3 trận).
Cặp T1: đủ mẫu 0, ít mẫu 6, chưa thấy 0, thiếu anchor 4.
Cặp Gen.G: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.

### Căn cứ và nhánh từng lượt ban

| Lượt | Đội | Ban | Lý do | Nhánh đáp trả được xét |
|---:|---|---|---|---|
| 1 | Gen.G | Milio | Mất pool địch 0.0032; chi phí tự cấm 0.0017; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; 2 nhánh, giá trị dự kiến -0.0004 | ban Nocturne (71% trong nhánh xét); ban Jarvan IV (29% trong nhánh xét) |
| 2 | T1 | Camille | Mất pool địch 0.0056; chi phí tự cấm 0.0021; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; 2 nhánh, giá trị dự kiến 0.0027 | ban Nocturne (71% trong nhánh xét); ban Jarvan IV (29% trong nhánh xét) |
| 3 | Gen.G | Karma | Mất pool địch 0.0029; chi phí tự cấm 0.0007; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; 2 nhánh, giá trị dự kiến -0.0049 | ban Nocturne (71% trong nhánh xét); ban Jarvan IV (29% trong nhánh xét) |
| 4 | T1 | Viktor | Mất pool địch 0.0071; chi phí tự cấm 0.0029; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; 2 nhánh, giá trị dự kiến 0.0189 | ban Nocturne (56% trong nhánh xét); ban Jarvan IV (44% trong nhánh xét) |
| 5 | Gen.G | Xayah | Mất pool địch 0.0032; chi phí tự cấm 0.0013; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; 2 nhánh, giá trị dự kiến -0.0006 | ban Nocturne (56% trong nhánh xét); ban Jarvan IV (44% trong nhánh xét) |
| 6 | T1 | Akali | Mất pool địch 0.0088; chi phí tự cấm 0.0046; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; 2 nhánh, giá trị dự kiến 0.0254 | pick Jarvan IV (57% trong nhánh xét); pick Nocturne (43% trong nhánh xét) |
| 13 | T1 | Ornn | Mất pool địch 0.0000; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; 2 nhánh, giá trị dự kiến -0.0014 | ban Sylas (58% trong nhánh xét); ban LeBlanc (42% trong nhánh xét) |
| 14 | Gen.G | Rell | Mất pool địch 0.0231; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; 2 nhánh, giá trị dự kiến 0.0151 | ban Ziggs (51% trong nhánh xét); ban Sivir (49% trong nhánh xét) |
| 15 | T1 | Jax | Mất pool địch 0.0064; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; 2 nhánh, giá trị dự kiến -0.0026 | ban Bard (50% trong nhánh xét); ban Sylas (50% trong nhánh xét) |
| 16 | Gen.G | Bard | Mất pool địch 0.0031; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; 2 nhánh, giá trị dự kiến 0.0114 | pick Sylas (52% trong nhánh xét); pick Yone (48% trong nhánh xét) |

## Ván 5 — T1 chọn trước

Fearless khóa 40 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Pantheon, Yunara, Naafiri | Maokai, Cho'Gath |
| Gen.G | Camille, Viktor, Trundle | Jax, Gwen |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Vayne | Ornn |
| jng | Sejuani | Malphite |
| mid | Akali | Anivia |
| bot | Sivir | Xayah |
| sup | Karma | Milio |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Pantheon | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Camille | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Yunara | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Viktor | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Naafiri | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Trundle | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Akali | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Xayah | bot | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Ornn | top | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Karma | sup | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Sivir | bot | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Anivia | mid | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Jax | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Maokai | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Gwen | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Cho'Gath | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Milio | sup | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Sejuani | jng | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Vayne | top | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Malphite | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: T1 Vayne (2 trận); Gen.G Malphite (1 trận).
Cặp T1: đủ mẫu 0, ít mẫu 4, chưa thấy 6, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 3, chưa thấy 6, thiếu anchor 1.

### Căn cứ và nhánh từng lượt ban

| Lượt | Đội | Ban | Lý do | Nhánh đáp trả được xét |
|---:|---|---|---|---|
| 1 | T1 | Pantheon | Mất pool địch 0.0088; chi phí tự cấm 0.0073; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; 2 nhánh, giá trị dự kiến -0.0058 | ban Yunara (52% trong nhánh xét); ban Trundle (48% trong nhánh xét) |
| 2 | Gen.G | Camille | Mất pool địch 0.0041; chi phí tự cấm 0.0025; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; 2 nhánh, giá trị dự kiến 0.0096 | ban Yunara (56% trong nhánh xét); ban Trundle (44% trong nhánh xét) |
| 3 | T1 | Yunara | Mất pool địch 0.0074; chi phí tự cấm 0.0053; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; 2 nhánh, giá trị dự kiến -0.0095 | ban Trundle (51% trong nhánh xét); ban Akali (49% trong nhánh xét) |
| 4 | Gen.G | Viktor | Mất pool địch 0.0072; chi phí tự cấm 0.0035; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; 2 nhánh, giá trị dự kiến 0.0098 | ban Trundle (51% trong nhánh xét); ban Akali (49% trong nhánh xét) |
| 5 | T1 | Naafiri | Mất pool địch 0.0046; chi phí tự cấm 0.0025; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; 2 nhánh, giá trị dự kiến 0.0150 | ban Trundle (51% trong nhánh xét); ban Akali (49% trong nhánh xét) |
| 6 | Gen.G | Trundle | Mất pool địch 0.0083; chi phí tự cấm 0.0038; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; 2 nhánh, giá trị dự kiến 0.0106 | pick Akali (52% trong nhánh xét); pick Rell (48% trong nhánh xét) |
| 13 | Gen.G | Jax | Mất pool địch 0.0333; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; 2 nhánh, giá trị dự kiến -0.0039 | ban Rell (61% trong nhánh xét); ban Maokai (39% trong nhánh xét) |
| 14 | T1 | Maokai | Mất pool địch 0.0021; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; 2 nhánh, giá trị dự kiến 0.0073 | ban Yorick (51% trong nhánh xét); ban Yone (49% trong nhánh xét) |
| 15 | Gen.G | Gwen | Mất pool địch 0.0015; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; 1 nhánh, giá trị dự kiến -0.0031 | ban Rell (100% trong nhánh xét) |
| 16 | T1 | Cho'Gath | Mất pool địch 0.0000; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; 2 nhánh, giá trị dự kiến 0.0110 | pick Rell (57% trong nhánh xét); pick Bard (43% trong nhánh xét) |

## Kiểm chứng

{
  "completed_games": 5,
  "total_actions": 100,
  "unique_picks_across_series": 50,
  "no_repeated_pick": true,
  "prior_lock_counts": [
    0,
    10,
    20,
    30,
    40
  ],
  "draft_order_legal": true,
  "no_locked_champion_picked_or_banned": true,
  "only_picks_carry_over_not_standard_bans": true
}

Giới hạn: chọn tham lam theo từng lượt; chưa tối ưu phân bổ champion pool cho cả series, chưa có mô hình tương tác3/5tướng hoặc combat simulator. Chưa chứng minh tăng thắng.
