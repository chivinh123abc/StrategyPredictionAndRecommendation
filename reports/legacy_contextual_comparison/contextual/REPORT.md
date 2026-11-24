# WLDS: 5 ván draft Fearless — T1 vs Gen.G

Đây là 5 phiên draft liên tiếp, không mô phỏng trận chiến hoặc gán tỉ số thắng/thua. Không dùng kết quả giả để ép BO5 đi đủ5ván.

Luật: [Fearless của Riot](https://lolesports.com/en-GB/news/fst-2025-primer). Tướng đã pick bởi bất kỳ đội nào bị khóa cho cả hai đội đến hết series; ban thường chỉ có hiệu lực trong ván đó. Ván5 không reset pool.

Snapshot: `{'region': 'WLDS', 'dataset_patch': '16.20', 'data_through': '2026-11-09T00:56:00+00:00', 'requested_as_of': '2026-11-13T23:59:59.999999999+00:00', 'staleness_days': 4, 'history_games': 106, 'patch_games': 94, 'lookback_days': 60, 'half_life_days': 21.0, 'claim': 'historical_snapshot_not_live_meta'}`.

Lịch thử nghiệm: giữ T1 ở Blue và Gen.G ở Red; bên pick trước luân phiên Blue/Red. Đây là lịch chỉ định cho demo, không phải mô phỏng quyền First Selection dựa vào thắng/thua.

Cho phép test chọn số1 khi thiếu tin cậy: True. Không nâng nhãn counter hoặc độ tin cậy khi bật chế độ này.

Chiến lược ban: contextual. Chỉ legacy/contextual; không tìm nhánh phản ứng hoặc tối ưu toàn BO5.

Ứng viên: ít nhất 1 lần quan sát đúng role; ngưỡng bằng chứng 5 trận. Ưu tiên ứng viên đủ mẫu trước; chỉ xét lớp ít mẫu khi không còn ứng viên đủ mẫu ở role đang xét. Khi so giữa các role mở cũng ưu tiên lớp đủ mẫu; người dùng wishlist vẫn là lựa chọn chủ đích riêng. Đây là pool gợi ý có dữ liệu, chưa là danh mục tướng hợp lệ chính thức của sự kiện.

Association dương được shrink thêm theo số mẫu cặp; association âm theo số quan sát đồng đội. Không cho một cặp một-mẫu tạo bonus lift lớn như cặp có nhiều mẫu.

## Ván 1 — T1 chọn trước

Fearless khóa 0 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Seraphine, Ashe | Jhin, Wukong |
| Gen.G | Nocturne, Vi, Lee Sin | Orianna, Locke |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Ambessa | Olaf |
| jng | Jarvan IV | Pantheon |
| mid | Syndra | Cassiopeia |
| bot | Kalista | Ezreal |
| sup | Renata Glasc | Nautilus |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Seraphine | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Ashe | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Renata Glasc | sup | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Olaf | top | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Cassiopeia | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Kalista | bot | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Jarvan IV | jng | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Nautilus | sup | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Orianna | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Jhin | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Locke | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Wukong | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Ezreal | bot | Coverage 33%; chưa xác nhận counter |
| 18 | T1 | Pick 4 | Ambessa | top | Coverage 25%; chưa xác nhận counter |
| 19 | T1 | Pick 5 | Syndra | mid | Coverage 25%; chưa xác nhận counter |
| 20 | Gen.G | Pick 5 | Pantheon | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 1, ít mẫu 7, chưa thấy 2, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 9, chưa thấy 0, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0050; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0086; chi phí tự cấm 0.0036; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Seraphine | Mất pool địch 0.0022; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0131; chi phí tự cấm 0.0045; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Ashe | Mất pool địch 0.0021; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0093; chi phí tự cấm 0.0024; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Orianna | Mất pool địch 0.0035; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Jhin | Mất pool địch 0.0077; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Locke | Mất pool địch 0.0027; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Wukong | Mất pool địch 0.0075; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 2 — Gen.G chọn trước

Fearless khóa 10 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Nocturne, Vi | Alistar, Seraphine |
| Gen.G | Locke, Jayce, Orianna | Wukong, Trundle |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Galio | Rumble |
| jng | Skarner | Lee Sin |
| mid | Akali | Viktor |
| bot | Yunara | Jhin |
| sup | Lulu | Leona |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Locke | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Nocturne | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Orianna | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Vi | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Lee Sin | jng | Chưa lộ địch |
| 8 | T1 | Pick 1 | Lulu | sup | Coverage 100%; chưa xác nhận counter |
| 9 | T1 | Pick 2 | Yunara | bot | Coverage 100%; chưa xác nhận counter |
| 10 | Gen.G | Pick 2 | Jhin | bot | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Rumble | top | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Akali | mid | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Alistar | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Wukong | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Seraphine | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Trundle | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Galio | top | Coverage 32%; chưa xác nhận counter |
| 18 | Gen.G | Pick 4 | Viktor | mid | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Leona | sup | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Skarner | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 1, ít mẫu 6, chưa thấy 3, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 3, ít mẫu 7, chưa thấy 0, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Locke | Mất pool địch 0.0029; chi phí tự cấm 0.0003; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Qiyana | Mất pool địch 0.0055; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Jayce | Mất pool địch 0.0048; chi phí tự cấm 0.0025; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Nocturne | Mất pool địch 0.0147; chi phí tự cấm 0.0067; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Orianna | Mất pool địch 0.0057; chi phí tự cấm 0.0039; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Vi | Mất pool địch 0.0154; chi phí tự cấm 0.0068; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Alistar | Mất pool địch 0.0056; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Wukong | Mất pool địch 0.0087; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Seraphine | Mất pool địch 0.0053; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Trundle | Mất pool địch 0.0051; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 3 — T1 chọn trước

Fearless khóa 20 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Ashe, Qiyana, Seraphine | Naafiri, Trundle |
| Gen.G | Nocturne, Vi, Jayce | Karma, Rakan |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Gnar | K'Sante |
| jng | Wukong | Xin Zhao |
| mid | Orianna | Locke |
| bot | Lucian | Corki |
| sup | Milio | Alistar |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Ashe | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Qiyana | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Seraphine | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Jayce | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Orianna | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Locke | mid | Coverage 100%; chưa xác nhận counter |
| 9 | Gen.G | Pick 2 | K'Sante | top | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Gnar | top | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Wukong | jng | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Alistar | sup | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Karma | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Naafiri | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Rakan | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Trundle | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Corki | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Lucian | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Milio | sup | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Xin Zhao | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 2, ít mẫu 6, chưa thấy 2, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 7, chưa thấy 3, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Ashe | Mất pool địch 0.0061; chi phí tự cấm 0.0003; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0162; chi phí tự cấm 0.0060; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Qiyana | Mất pool địch 0.0147; chi phí tự cấm 0.0090; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0186; chi phí tự cấm 0.0075; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Seraphine | Mất pool địch 0.0091; chi phí tự cấm 0.0054; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Jayce | Mất pool địch 0.0074; chi phí tự cấm 0.0022; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Karma | Mất pool địch 0.0050; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Naafiri | Mất pool địch 0.0056; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Rakan | Mất pool địch 0.0022; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Trundle | Mất pool địch 0.0066; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 4 — Gen.G chọn trước

Fearless khóa 30 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Nocturne, Vi | Xayah, Kai'Sa |
| Gen.G | Karma, Jayce, Trundle | Taliyah, Naafiri |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Renekton | Camille |
| jng | Sejuani | Maokai |
| mid | Anivia | Ahri |
| bot | Ashe | Miss Fortune |
| sup | Rakan | Seraphine |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Karma | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Nocturne | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Trundle | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Vi | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Seraphine | sup | Chưa lộ địch |
| 8 | T1 | Pick 1 | Ashe | bot | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | Renekton | top | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Ahri | mid | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Camille | top | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Rakan | sup | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Xayah | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Taliyah | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Kai'Sa | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Naafiri | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Anivia | mid | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Miss Fortune | bot | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Maokai | jng | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Sejuani | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.
Cặp T1: đủ mẫu 0, ít mẫu 3, chưa thấy 7, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 6, chưa thấy 4, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Karma | Mất pool địch 0.0067; chi phí tự cấm 0.0043; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Qiyana | Mất pool địch 0.0155; chi phí tự cấm 0.0041; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Jayce | Mất pool địch 0.0099; chi phí tự cấm 0.0080; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Nocturne | Mất pool địch 0.0213; chi phí tự cấm 0.0103; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Trundle | Mất pool địch 0.0061; chi phí tự cấm 0.0046; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Vi | Mất pool địch 0.0227; chi phí tự cấm 0.0102; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Xayah | Mất pool địch 0.0023; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Taliyah | Mất pool địch 0.0026; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Kai'Sa | Mất pool địch 0.0028; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Naafiri | Mất pool địch 0.0026; chi phí tự cấm 0.0010; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 5 — T1 chọn trước

Fearless khóa 40 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Taliyah, Naafiri | Rell, Cho'Gath |
| Gen.G | Nocturne, Vi, Jayce | Jax, Zaahen |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Aurora | Ornn |
| jng | Trundle | Nasus |
| mid | Ryze | Annie |
| bot | Kai'Sa | Xayah |
| sup | Karma | Poppy |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Taliyah | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Naafiri | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Jayce | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Trundle | jng | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Xayah | bot | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Ornn | top | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Kai'Sa | bot | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Karma | sup | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Annie | mid | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Jax | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Rell | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Zaahen | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Cho'Gath | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Poppy | sup | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Ryze | mid | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Aurora | top | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Nasus | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: Gen.G Poppy (2 trận); T1 Aurora (2 trận); Gen.G Nasus (1 trận).
Cặp T1: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 3, chưa thấy 2, thiếu anchor 5.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0147; chi phí tự cấm 0.0090; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0232; chi phí tự cấm 0.0094; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Taliyah | Mất pool địch 0.0056; chi phí tự cấm 0.0043; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0241; chi phí tự cấm 0.0104; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Naafiri | Mất pool địch 0.0011; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Jayce | Mất pool địch 0.0134; chi phí tự cấm 0.0051; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Jax | Mất pool địch 0.0045; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Rell | Mất pool địch 0.0267; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Zaahen | Mất pool địch 0.0243; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Cho'Gath | Mất pool địch 0.0227; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

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
