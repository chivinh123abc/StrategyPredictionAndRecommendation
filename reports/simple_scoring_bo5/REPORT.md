# WLDS: 5 ván draft Fearless — T1 vs Gen.G

Đây là 5 phiên draft liên tiếp, không mô phỏng trận chiến hoặc gán tỉ số thắng/thua. Không dùng kết quả giả để ép BO5 đi đủ5ván.

Luật: [Fearless của Riot](https://lolesports.com/en-GB/news/fst-2025-primer). Tướng đã pick bởi bất kỳ đội nào bị khóa cho cả hai đội đến hết series; ban thường chỉ có hiệu lực trong ván đó. Ván5 không reset pool.

Snapshot: `{'region': 'WLDS', 'dataset_patch': '16.20', 'data_through': '2026-11-14T23:18:11+00:00', 'requested_as_of': '2026-11-24T23:59:59.999999999+00:00', 'staleness_days': 10, 'history_games': 110, 'patch_games': 98, 'lookback_days': 60, 'half_life_days': 21.0, 'claim': 'historical_snapshot_not_live_meta'}`.

Lịch thử nghiệm: giữ T1 ở Blue và Gen.G ở Red; bên pick trước luân phiên Blue/Red. Đây là lịch chỉ định cho demo, không phải mô phỏng quyền First Selection dựa vào thắng/thua.

Cho phép test chọn số1 khi thiếu tin cậy: True. Không nâng nhãn counter hoặc độ tin cậy khi bật chế độ này.

Chiến lược ban: contextual. Chỉ legacy/contextual; không tìm nhánh phản ứng hoặc tối ưu toàn BO5.

Ứng viên: ít nhất 1 lần quan sát đúng role; ngưỡng bằng chứng 5 trận. Ưu tiên ứng viên đủ mẫu trước; chỉ xét lớp ít mẫu khi không còn ứng viên đủ mẫu ở role đang xét. Khi so giữa các role mở cũng ưu tiên lớp đủ mẫu; người dùng wishlist vẫn là lựa chọn chủ đích riêng. Đây là pool gợi ý có dữ liệu, chưa là danh mục tướng hợp lệ chính thức của sự kiện.

Cách tính điểm pick: simple.

Simple: trung bình tần suất chọn, cosine nếu có và WR đối đầu cùng role; thiếu matchup dùng WR lịch sử có nhãn. Không dùng synergy/lift/odds để chấm điểm. Thống kê cặp ở dưới chỉ để tham khảo.

## Ván 1 — T1 chọn trước

Fearless khóa 0 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Pantheon, K'Sante | Gnar, Renekton |
| Gen.G | Lee Sin, Rumble, Ambessa | Jhin, Yunara |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Olaf | Camille |
| jng | Vi | Jarvan IV |
| mid | Orianna | Syndra |
| bot | Ashe | Ezreal |
| sup | Lulu | Nautilus |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Lee Sin | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Pantheon | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Rumble | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | K'Sante | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Ambessa | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Orianna | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Syndra | mid | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Nautilus | sup | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Olaf | top | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Lulu | sup | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Ezreal | bot | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Jhin | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Gnar | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Yunara | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Renekton | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Jarvan IV | jng | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Vi | jng | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Ashe | bot | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Camille | top | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Orianna | 99.06 | pick_frequency=1.000; content=0.981 | Chưa lộ/không suy được cùng role; chưa chấm tương tác khác role |
| 8 | Gen.G | Syndra | 85.68 | pick_frequency=1.000; content=0.955; matchup=0.615 | Orianna n=2; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 9 | Gen.G | Nautilus | 83.57 | pick_frequency=1.000; content=0.877; matchup=0.630 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 10 | T1 | Olaf | 80.83 | pick_frequency=0.750; content=0.961; matchup=0.714 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 11 | T1 | Lulu | 80.24 | pick_frequency=0.963; content=0.867; matchup=0.577 | Nautilus n=1; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 12 | Gen.G | Ezreal | 78.2 | pick_frequency=1.000; content=0.877; matchup=0.469 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 17 | Gen.G | Jarvan IV | 77.67 | pick_frequency=0.903; content=0.927; matchup=0.500 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 18 | T1 | Vi | 74.6 | pick_frequency=0.645; content=0.943; matchup=0.650 | Jarvan IV n=3; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 19 | T1 | Ashe | 71.52 | pick_frequency=0.531; content=0.967; matchup=0.647 | Ezreal n=4; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 20 | Gen.G | Camille | 63.73 | pick_frequency=0.429; content=0.983; matchup=0.500 | Olaf n=2; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
Cặp T1: đủ mẫu 0, ít mẫu 8, chưa thấy 2, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 9, chưa thấy 1, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0065; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Lee Sin | Mất pool địch 0.0146; chi phí tự cấm 0.0036; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Pantheon | Mất pool địch 0.0033; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Rumble | Mất pool địch 0.0103; chi phí tự cấm 0.0036; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | K'Sante | Mất pool địch 0.0053; chi phí tự cấm 0.0014; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Ambessa | Mất pool địch 0.0160; chi phí tự cấm 0.0085; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Jhin | Mất pool địch 0.0073; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Gnar | Mất pool địch 0.0099; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Yunara | Mất pool địch 0.0073; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Renekton | Mất pool địch 0.0048; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 2 — Gen.G chọn trước

Fearless khóa 10 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Viktor, Pantheon | Naafiri, Renata Glasc |
| Gen.G | Lee Sin, Wukong, Nocturne | Trundle, Xin Zhao |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Gnar | Ambessa |
| jng | Cho'Gath | Skarner |
| mid | Taliyah | Cassiopeia |
| bot | Jhin | Yunara |
| sup | Seraphine | Alistar |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Lee Sin | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Wukong | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Viktor | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Nocturne | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Pantheon | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Ambessa | top | Chưa lộ địch |
| 8 | T1 | Pick 1 | Gnar | top | Coverage 100%; chưa xác nhận counter |
| 9 | T1 | Pick 2 | Seraphine | sup | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Cassiopeia | mid | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Yunara | bot | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Jhin | bot | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Naafiri | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Trundle | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Renata Glasc | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Xin Zhao | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Taliyah | mid | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Alistar | sup | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Skarner | jng | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Cho'Gath | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | Gen.G | Ambessa | 96.23 | pick_frequency=0.964; content=0.960 | Chưa lộ/không suy được cùng role; chưa chấm tương tác khác role |
| 8 | T1 | Gnar | 80.57 | pick_frequency=0.607; content=0.977; matchup=0.833 | Ambessa n=6; chưa chấm tương tác khác role |
| 9 | T1 | Seraphine | 75.93 | pick_frequency=0.741; content=0.887; matchup=0.650 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 10 | Gen.G | Cassiopeia | 75.89 | pick_frequency=0.654; content=0.976; matchup=0.647 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 11 | Gen.G | Yunara | 74.95 | pick_frequency=0.688; content=0.970; matchup=0.591 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 12 | T1 | Jhin | 74.5 | pick_frequency=0.750; content=0.943; matchup=0.542 | Yunara n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 17 | T1 | Taliyah | 68.29 | pick_frequency=0.385; content=0.964; matchup=0.700 | Cassiopeia n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 18 | Gen.G | Alistar | 71.66 | pick_frequency=1.000; content=0.780; matchup=0.370 | Seraphine n=1; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 19 | Gen.G | Skarner | 42.87 | pick_frequency=0.258; content=0.528; matchup=0.500 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 20 | T1 | Cho'Gath | 31.71 | pick_frequency=0.194; content=0.591; matchup=0.167 | Skarner n=1; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
Cặp T1: đủ mẫu 0, ít mẫu 4, chưa thấy 6, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 7, chưa thấy 3, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Lee Sin | Mất pool địch 0.0149; chi phí tự cấm 0.0103; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Qiyana | Mất pool địch 0.0110; chi phí tự cấm 0.0030; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Wukong | Mất pool địch 0.0065; chi phí tự cấm 0.0039; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Viktor | Mất pool địch 0.0153; chi phí tự cấm 0.0075; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Nocturne | Mất pool địch 0.0123; chi phí tự cấm 0.0079; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Pantheon | Mất pool địch 0.0144; chi phí tự cấm 0.0063; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Naafiri | Mất pool địch 0.0099; chi phí tự cấm 0.0016; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Trundle | Mất pool địch 0.0222; chi phí tự cấm 0.0100; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Renata Glasc | Mất pool địch 0.0064; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Xin Zhao | Mất pool địch 0.0209; chi phí tự cấm 0.0114; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 3 — T1 chọn trước

Fearless khóa 20 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Lucian, Pantheon | Ahri, Twisted Fate |
| Gen.G | Rumble, Lee Sin, Wukong | Renekton, Jayce |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Zaahen | K'Sante |
| jng | Nocturne | Trundle |
| mid | Viktor | Galio |
| bot | Xayah | Kalista |
| sup | Karma | Renata Glasc |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Rumble | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Lucian | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Lee Sin | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Pantheon | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Wukong | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Viktor | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Renata Glasc | sup | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | K'Sante | top | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Nocturne | jng | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Karma | sup | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Trundle | jng | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Renekton | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Ahri | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Jayce | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Twisted Fate | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Kalista | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Xayah | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Zaahen | top | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Galio | mid | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Viktor | 91.64 | pick_frequency=0.885; content=0.948 | Chưa lộ/không suy được cùng role; chưa chấm tương tác khác role |
| 8 | Gen.G | Renata Glasc | 73.18 | pick_frequency=0.741; content=0.955; matchup=0.500 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 9 | Gen.G | K'Sante | 70.57 | pick_frequency=0.857; content=0.843; matchup=0.417 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 10 | T1 | Nocturne | 69.92 | pick_frequency=0.581; content=0.906; matchup=0.611 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 11 | T1 | Karma | 65.88 | pick_frequency=0.667; content=0.921; matchup=0.389 | Renata Glasc n=2; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 12 | Gen.G | Trundle | 66.12 | pick_frequency=0.387; content=0.930; matchup=0.667 | Nocturne n=1; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 17 | Gen.G | Kalista | 64.55 | pick_frequency=0.594; content=0.869; matchup=0.474 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 18 | T1 | Xayah | 61.74 | pick_frequency=0.406; content=0.984; matchup=0.462 | Kalista n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 19 | T1 | Zaahen | 55.43 | pick_frequency=0.179; content=0.884; matchup=0.600 | K'Sante n=1; Trundle n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 20 | Gen.G | Galio | 63.06 | pick_frequency=0.385; content=0.907; matchup=0.600 | Viktor n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
Cặp T1: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 3, chưa thấy 6, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0098; chi phí tự cấm 0.0036; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Rumble | Mất pool địch 0.0236; chi phí tự cấm 0.0101; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Lucian | Mất pool địch 0.0111; chi phí tự cấm 0.0057; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Lee Sin | Mất pool địch 0.0172; chi phí tự cấm 0.0058; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Pantheon | Mất pool địch 0.0084; chi phí tự cấm 0.0042; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Wukong | Mất pool địch 0.0121; chi phí tự cấm 0.0034; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Renekton | Mất pool địch 0.0060; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Ahri | Mất pool địch 0.0046; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Jayce | Mất pool địch 0.0058; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Twisted Fate | Mất pool địch 0.0060; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 4 — Gen.G chọn trước

Fearless khóa 30 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Rumble, Qiyana, Pantheon | Naafiri, Maokai |
| Gen.G | Lee Sin, Jayce, Wukong | Xin Zhao, Sejuani |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Renekton | Jax |
| jng | Lillia | Aatrox |
| mid | Ahri | Twisted Fate |
| bot | Kai'Sa | Lucian |
| sup | Rakan | Leona |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Lee Sin | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Rumble | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Qiyana | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Wukong | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Pantheon | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Lucian | bot | Chưa lộ địch |
| 8 | T1 | Pick 1 | Ahri | mid | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | Renekton | top | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Twisted Fate | mid | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Leona | sup | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Rakan | sup | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Naafiri | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Xin Zhao | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Maokai | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Sejuani | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Kai'Sa | bot | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Jax | top | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Aatrox | jng | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Lillia | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: Gen.G Aatrox (1 trận); T1 Lillia (1 trận).

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | Gen.G | Lucian | 79.01 | pick_frequency=0.625; content=0.955 | Chưa lộ/không suy được cùng role; chưa chấm tương tác khác role |
| 8 | T1 | Ahri | 66.66 | pick_frequency=0.385; content=0.915; matchup=0.700 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 9 | T1 | Renekton | 63.1 | pick_frequency=0.429; content=0.798; matchup=0.667 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 10 | Gen.G | Twisted Fate | 63.77 | pick_frequency=0.192; content=0.921; matchup=0.800 | Ahri n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 11 | Gen.G | Leona | 63.57 | pick_frequency=0.333; content=0.907; matchup=0.667 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 12 | T1 | Rakan | 62.79 | pick_frequency=0.593; content=0.979; matchup=0.312 | Leona n=1; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 17 | T1 | Kai'Sa | 60.64 | pick_frequency=0.375; content=0.944; matchup=0.500 | Lucian n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 18 | Gen.G | Jax | 54.14 | pick_frequency=0.321; content=0.858; matchup=0.444 | Renekton n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 19 | Gen.G | Aatrox | 1.61 | pick_frequency=0.032; matchup=0.000 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 20 | T1 | Lillia | 1.61 | pick_frequency=0.032; matchup=0.000 | Aatrox n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
Cặp T1: đủ mẫu 0, ít mẫu 4, chưa thấy 5, thiếu anchor 1.
Cặp Gen.G: đủ mẫu 0, ít mẫu 2, chưa thấy 7, thiếu anchor 1.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Lee Sin | Mất pool địch 0.0172; chi phí tự cấm 0.0115; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Rumble | Mất pool địch 0.0245; chi phí tự cấm 0.0131; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Jayce | Mất pool địch 0.0253; chi phí tự cấm 0.0180; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Qiyana | Mất pool địch 0.0177; chi phí tự cấm 0.0078; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Wukong | Mất pool địch 0.0150; chi phí tự cấm 0.0099; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Pantheon | Mất pool địch 0.0209; chi phí tự cấm 0.0110; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Naafiri | Mất pool địch 0.0223; chi phí tự cấm 0.0145; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Xin Zhao | Mất pool địch 0.0210; chi phí tự cấm 0.0105; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Maokai | Mất pool địch 0.0119; chi phí tự cấm 0.0004; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Sejuani | Mất pool địch 0.0585; chi phí tự cấm 0.0244; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 5 — T1 chọn trước

Fearless khóa 40 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Corki, Qiyana, Ornn | Milio, Rell |
| Gen.G | Rumble, Jayce, Lee Sin | Miss Fortune, Tristana |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Irelia | Gwen |
| jng | Wukong | Pantheon |
| mid | Ryze | Locke |
| bot | Caitlyn | Sivir |
| sup | Nami | Poppy |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Corki | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Rumble | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Qiyana | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Ornn | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Wukong | jng | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Pantheon | jng | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Locke | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Nami | sup | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Ryze | mid | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Sivir | bot | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Miss Fortune | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Milio | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Tristana | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Rell | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Gwen | top | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Caitlyn | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Irelia | top | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Poppy | sup | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: Gen.G Gwen (3 trận); T1 Irelia (1 trận); Gen.G Poppy (2 trận).

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Wukong | 73.94 | pick_frequency=0.516; content=0.963 | Chưa lộ/không suy được cùng role; chưa chấm tương tác khác role |
| 8 | Gen.G | Pantheon | 68.11 | pick_frequency=0.613; content=0.957; matchup=0.474 | Wukong n=1; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 9 | Gen.G | Locke | 58.8 | pick_frequency=0.577; content=0.720; matchup=0.467 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 10 | T1 | Nami | 57.13 | pick_frequency=0.185; content=0.729; matchup=0.800 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 11 | T1 | Ryze | 55.11 | pick_frequency=0.423; content=0.958; matchup=0.273 | Locke n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 12 | Gen.G | Sivir | 55.64 | pick_frequency=0.188; content=0.982; matchup=0.500 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 17 | Gen.G | Gwen | 55.36 | pick_frequency=0.107; matchup=1.000 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 18 | T1 | Caitlyn | 46.38 | pick_frequency=0.250; content=0.891; matchup=0.250 | Sivir n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 19 | T1 | Irelia | 51.79 | pick_frequency=0.036; matchup=1.000 | Gwen n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
| 20 | Gen.G | Poppy | 53.7 | pick_frequency=0.074; matchup=1.000 | Nami n=0; thiếu hỗ trợ, test chọn số1; chưa chấm tương tác khác role |
Cặp T1: đủ mẫu 0, ít mẫu 3, chưa thấy 7, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 2, chưa thấy 4, thiếu anchor 4.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Corki | Mất pool địch 0.0060; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Rumble | Mất pool địch 0.0287; chi phí tự cấm 0.0135; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Qiyana | Mất pool địch 0.0110; chi phí tự cấm 0.0059; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Jayce | Mất pool địch 0.0380; chi phí tự cấm 0.0135; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Ornn | Mất pool địch 0.0832; chi phí tự cấm 0.0696; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0270; chi phí tự cấm 0.0091; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Miss Fortune | Mất pool địch 0.0099; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Milio | Mất pool địch 0.0035; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Tristana | Mất pool địch 0.0037; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Rell | Mất pool địch 0.0979; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

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
