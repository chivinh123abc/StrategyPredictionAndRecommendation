# WLDS: 5 ván draft Fearless — T1 vs Gen.G

Đây là 5 phiên draft liên tiếp, không mô phỏng trận chiến hoặc gán tỉ số thắng/thua. Không dùng kết quả giả để ép BO5 đi đủ5ván.

Luật: [Fearless của Riot](https://lolesports.com/en-GB/news/fst-2025-primer). Tướng đã pick bởi bất kỳ đội nào bị khóa cho cả hai đội đến hết series; ban thường chỉ có hiệu lực trong ván đó. Ván5 không reset pool.

Snapshot: `{'region': 'WLDS', 'dataset_patch': '16.20', 'data_through': '2026-11-14T23:18:11+00:00', 'requested_as_of': '2026-11-24T23:59:59.999999999+00:00', 'staleness_days': 10, 'history_games': 110, 'patch_games': 98, 'lookback_days': 60, 'half_life_days': 21.0, 'claim': 'historical_snapshot_not_live_meta'}`.

Lịch thử nghiệm: giữ T1 ở Blue và Gen.G ở Red; đội chọn trước từng ván: red, red, blue, blue, red. Quyền chọn trước độc lập màu đội, theo cấu hình người dùng; không suy từ thắng/thua. Nguồn luật Fearless bên trên không xác nhận một luật First Selection mới.

Cho phép test chọn số1 khi thiếu tin cậy: True. Không nâng nhãn counter hoặc độ tin cậy khi bật chế độ này.

Chiến lược ban: contextual. Chỉ legacy/contextual; không tìm nhánh phản ứng hoặc tối ưu toàn BO5.

Ứng viên: ít nhất 1 lần quan sát đúng role; ngưỡng bằng chứng 5 trận. Ưu tiên ứng viên đủ mẫu trước; chỉ xét lớp ít mẫu khi không còn ứng viên đủ mẫu ở role đang xét. Khi so giữa các role mở cũng ưu tiên lớp đủ mẫu; người dùng wishlist vẫn là lựa chọn chủ đích riêng. Đây là pool gợi ý có dữ liệu, chưa là danh mục tướng hợp lệ chính thức của sự kiện.

Cách tính điểm pick: current.

Association dương được shrink thêm theo số mẫu cặp; association âm theo số quan sát đồng đội. Không cho một cặp một-mẫu tạo bonus lift lớn như cặp có nhiều mẫu.

## Ván 1 — Gen.G chọn trước

Fearless khóa 0 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Ezreal, Renata Glasc, Seraphine | Ashe, Yunara |
| Gen.G | Nautilus, Jayce, Lucian | Alistar, Ambessa |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Rumble | Olaf |
| jng | Vi | Nocturne |
| mid | Cassiopeia | Syndra |
| bot | Jhin | Xayah |
| sup | Rakan | Lulu |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Nautilus | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Ezreal | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Renata Glasc | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Lucian | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Seraphine | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Nocturne | jng | Chưa lộ địch |
| 8 | T1 | Pick 1 | Vi | jng | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | Cassiopeia | mid | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Olaf | top | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Syndra | mid | Coverage 47%; chưa xác nhận counter |
| 12 | T1 | Pick 3 | Jhin | bot | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Ashe | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Alistar | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Yunara | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Ambessa | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Rumble | top | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Lulu | sup | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Xayah | bot | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Rakan | sup | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | Gen.G | Nocturne | 41.71 | meta=0.860; draft_order=0.120; historical=0.386; mastery=0.047; content=0.889 | Chưa lộ/không suy được cùng role |
| 8 | T1 | Vi | 38.54 | meta=0.761; draft_order=0.020; historical=0.433; matchup=0.500; mastery=0.114; content=0.943 | Nocturne n=2; thiếu hỗ trợ, test chọn số1 |
| 9 | T1 | Cassiopeia | 37.94 | meta=0.651; draft_order=0.021; historical=0.413; matchup=0.500; synergy=0.500; composition=0.631; mastery=0.085; content=0.956 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 10 | Gen.G | Olaf | 37.25 | meta=0.575; draft_order=0.049; historical=0.500; matchup=0.500; synergy=0.500; composition=0.517; mastery=0.227; content=0.980 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | Gen.G | Syndra | 30.83 | meta=0.541; draft_order=0.053; historical=0.425; matchup=0.476; synergy=0.500; composition=0.455; mastery=0.135; content=0.955 | Cassiopeia n=8 |
| 12 | T1 | Jhin | 28.89 | meta=0.329; draft_order=0.024; historical=0.351; matchup=0.500; synergy=0.500; composition=0.510; mastery=0.267; content=0.943 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 17 | T1 | Rumble | 27.19 | meta=0.475; draft_order=0.046; historical=0.102; matchup=0.500; synergy=0.500; composition=0.448; mastery=0.091; content=0.935 | Olaf n=1; thiếu hỗ trợ, test chọn số1 |
| 18 | Gen.G | Lulu | 29.01 | meta=0.477; draft_order=0.017; historical=0.389; matchup=0.500; synergy=0.500; composition=0.472; mastery=0.090; content=0.846 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 19 | Gen.G | Xayah | 21.04 | meta=0.169; draft_order=0.009; historical=0.232; matchup=0.500; synergy=0.500; composition=0.513; mastery=0.156; content=0.981 | Jhin n=2; thiếu hỗ trợ, test chọn số1 |
| 20 | T1 | Rakan | 20.3 | meta=0.174; draft_order=0.018; historical=0.142; matchup=0.500; synergy=0.500; composition=0.503; mastery=0.150; content=0.979 | Lulu n=1; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 0, ít mẫu 8, chưa thấy 2, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 9, chưa thấy 1, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Nautilus | Mất pool địch 0.0030; chi phí tự cấm 0.0005; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Ezreal | Mất pool địch 0.0091; chi phí tự cấm 0.0029; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Jayce | Mất pool địch 0.0030; chi phí tự cấm 0.0015; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Renata Glasc | Mất pool địch 0.0105; chi phí tự cấm 0.0051; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Lucian | Mất pool địch 0.0012; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Seraphine | Mất pool địch 0.0074; chi phí tự cấm 0.0021; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Ashe | Mất pool địch 0.0009; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Alistar | Mất pool địch 0.0050; chi phí tự cấm 0.0011; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Yunara | Mất pool địch 0.0019; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Ambessa | Mất pool địch 0.0038; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 2 — Gen.G chọn trước

Fearless khóa 10 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Ezreal, Qiyana, Lee Sin | Pantheon, Xin Zhao |
| Gen.G | Jarvan IV, Jayce, Locke | Trundle, Naafiri |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Ambessa | K'Sante |
| jng | Skarner | Wukong |
| mid | Orianna | Akali |
| bot | Kai'Sa | Kalista |
| sup | Nautilus | Renata Glasc |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Jarvan IV | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Ezreal | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Qiyana | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Locke | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Renata Glasc | sup | Chưa lộ địch |
| 8 | T1 | Pick 1 | Orianna | mid | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | Nautilus | sup | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Kalista | bot | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Akali | mid | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Kai'Sa | bot | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Pantheon | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Trundle | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Xin Zhao | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Naafiri | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Ambessa | top | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Wukong | jng | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | K'Sante | top | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Skarner | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | Gen.G | Renata Glasc | 32.79 | meta=0.743; draft_order=0.021; historical=0.299; mastery=0.000; content=0.955 | Chưa lộ/không suy được cùng role |
| 8 | T1 | Orianna | 31.24 | meta=0.504; draft_order=0.056; historical=0.425; matchup=0.500; mastery=0.063; content=0.981 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | T1 | Nautilus | 36.44 | meta=0.446; draft_order=0.053; historical=0.442; matchup=0.500; synergy=0.594; composition=0.641; mastery=0.148; content=0.878 | Renata Glasc n=0; thiếu hỗ trợ, test chọn số1 |
| 10 | Gen.G | Kalista | 39.55 | meta=0.185; draft_order=0.037; historical=0.273; matchup=0.500; synergy=0.500; composition=0.865; mastery=0.000; content=0.869 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | Gen.G | Akali | 27.38 | meta=0.509; draft_order=0.032; historical=0.066; matchup=0.500; synergy=0.500; composition=0.434; mastery=0.134; content=0.824 | Orianna n=3; thiếu hỗ trợ, test chọn số1 |
| 12 | T1 | Kai'Sa | 24.56 | meta=0.204; draft_order=0.030; historical=0.254; matchup=0.500; synergy=0.625; composition=0.590; mastery=0.085; content=0.944 | Kalista n=0; thiếu hỗ trợ, test chọn số1 |
| 17 | T1 | Ambessa | 29.75 | meta=0.335; draft_order=0.042; historical=0.276; matchup=0.500; synergy=0.552; composition=0.552; mastery=0.213; content=0.971 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 18 | Gen.G | Wukong | 27.42 | meta=0.356; draft_order=0.018; historical=0.185; matchup=0.500; synergy=0.500; composition=0.549; mastery=0.162; content=0.918 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 19 | Gen.G | K'Sante | 25.82 | meta=0.399; draft_order=0.056; historical=0.245; matchup=0.500; synergy=0.500; composition=0.495; mastery=0.000; content=0.843 | Ambessa n=3; thiếu hỗ trợ, test chọn số1 |
| 20 | T1 | Skarner | 16.22 | meta=0.169; draft_order=0.012; historical=0.215; matchup=0.500; synergy=0.500; composition=0.435; mastery=0.000; content=0.697 | Wukong n=1; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 4, ít mẫu 4, chưa thấy 2, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 8, chưa thấy 1, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Jarvan IV | Mất pool địch 0.0071; chi phí tự cấm 0.0044; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Ezreal | Mất pool địch 0.0100; chi phí tự cấm 0.0035; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Jayce | Mất pool địch 0.0050; chi phí tự cấm 0.0028; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Qiyana | Mất pool địch 0.0099; chi phí tự cấm 0.0037; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Locke | Mất pool địch 0.0020; chi phí tự cấm 0.0004; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Lee Sin | Mất pool địch 0.0108; chi phí tự cấm 0.0047; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Pantheon | Mất pool địch 0.0066; chi phí tự cấm 0.0009; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Trundle | Mất pool địch 0.0046; chi phí tự cấm 0.0003; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Xin Zhao | Mất pool địch 0.0027; chi phí tự cấm 0.0010; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Naafiri | Mất pool địch 0.0055; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 3 — T1 chọn trước

Fearless khóa 20 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Ashe, Qiyana, Ezreal | Trundle, Xin Zhao |
| Gen.G | Lee Sin, Jarvan IV, Jayce | Gnar, Camille |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Jax | Renekton |
| jng | Pantheon | Naafiri |
| mid | Locke | Viktor |
| bot | Lucian | Yunara |
| sup | Alistar | Seraphine |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Ashe | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Lee Sin | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Qiyana | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Jarvan IV | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Ezreal | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Jayce | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Locke | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Seraphine | sup | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Viktor | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Alistar | sup | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Pantheon | jng | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Renekton | top | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Gnar | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Trundle | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Camille | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Xin Zhao | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Yunara | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Jax | top | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Lucian | bot | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Naafiri | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Locke | 23.51 | meta=0.475; draft_order=0.010; historical=0.248; mastery=0.091; content=0.769 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Seraphine | 29.32 | meta=0.418; draft_order=0.025; historical=0.433; matchup=0.500; mastery=0.183; content=0.893 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Viktor | 27.62 | meta=0.326; draft_order=0.015; historical=0.408; matchup=0.500; synergy=0.500; composition=0.599; mastery=0.065; content=0.945 | Locke n=2; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Alistar | 24.99 | meta=0.312; draft_order=0.047; historical=0.215; matchup=0.500; synergy=0.500; composition=0.527; mastery=0.054; content=0.766 | Seraphine n=1; thiếu hỗ trợ, test chọn số1 |
| 11 | T1 | Pantheon | 24.51 | meta=0.330; draft_order=0.038; historical=0.273; matchup=0.500; synergy=0.500; composition=0.498; mastery=0.000; content=0.797 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Renekton | 24.95 | meta=0.287; draft_order=0.016; historical=0.391; matchup=0.500; synergy=0.500; composition=0.613; mastery=0.000; content=0.877 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | Yunara | 21.8 | meta=0.227; draft_order=0.015; historical=0.387; matchup=0.500; synergy=0.503; composition=0.474; mastery=0.072; content=0.970 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 18 | T1 | Jax | 20.87 | meta=0.205; draft_order=0.022; historical=0.189; matchup=0.500; synergy=0.500; composition=0.579; mastery=0.000; content=0.827 | Renekton n=0; thiếu hỗ trợ, test chọn số1 |
| 19 | T1 | Lucian | 18.29 | meta=0.250; draft_order=0.013; historical=0.219; matchup=0.500; synergy=0.500; composition=0.389; mastery=0.091; content=0.866 | Yunara n=4; thiếu hỗ trợ, test chọn số1 |
| 20 | Gen.G | Naafiri | 15.71 | meta=0.154; draft_order=0.007; historical=0.237; matchup=0.500; synergy=0.500; composition=0.398; mastery=0.000; content=0.910 | Pantheon n=0; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 0, ít mẫu 8, chưa thấy 2, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 6, chưa thấy 3, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Ashe | Mất pool địch 0.0018; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Lee Sin | Mất pool địch 0.0094; chi phí tự cấm 0.0023; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Qiyana | Mất pool địch 0.0136; chi phí tự cấm 0.0099; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Jarvan IV | Mất pool địch 0.0128; chi phí tự cấm 0.0053; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Ezreal | Mất pool địch 0.0112; chi phí tự cấm 0.0092; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Jayce | Mất pool địch 0.0071; chi phí tự cấm 0.0020; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Gnar | Mất pool địch 0.0037; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Trundle | Mất pool địch 0.0045; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Camille | Mất pool địch 0.0069; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Xin Zhao | Mất pool địch 0.0049; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 4 — T1 chọn trước

Fearless khóa 30 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Ashe, Ezreal | Nami, Leona |
| Gen.G | Lee Sin, Jarvan IV, Jayce | Gnar, Ornn |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Zaahen | Camille |
| jng | Trundle | Xin Zhao |
| mid | Galio | Taliyah |
| bot | Caitlyn | Corki |
| sup | Karma | Milio |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Lee Sin | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Ashe | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Jarvan IV | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Ezreal | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Jayce | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Galio | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Camille | top | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Taliyah | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Trundle | jng | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Karma | sup | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Corki | bot | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Gnar | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Nami | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Ornn | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Leona | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Xin Zhao | jng | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Caitlyn | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Zaahen | top | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Milio | sup | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Galio | 20.07 | meta=0.369; draft_order=0.007; historical=0.313; mastery=0.059; content=0.882 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Camille | 22.43 | meta=0.272; draft_order=0.008; historical=0.254; matchup=0.500; mastery=0.119; content=0.983 | Galio n=0; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Taliyah | 23.55 | meta=0.182; draft_order=0.008; historical=0.397; matchup=0.500; synergy=0.500; composition=0.592; mastery=0.137; content=0.975 | Galio n=0; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Trundle | 23.53 | meta=0.203; draft_order=0.007; historical=0.391; matchup=0.500; synergy=0.500; composition=0.645; mastery=0.085; content=0.897 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | T1 | Karma | 24.09 | meta=0.211; draft_order=0.058; historical=0.203; matchup=0.500; synergy=0.500; composition=0.518; mastery=0.154; content=0.921 | Camille n=1; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Corki | 19.69 | meta=0.138; draft_order=0.018; historical=0.313; matchup=0.500; synergy=0.500; composition=0.466; mastery=0.133; content=0.892 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | Xin Zhao | 17.29 | meta=0.143; draft_order=0.030; historical=0.359; matchup=0.500; synergy=0.500; composition=0.378; mastery=0.000; content=0.911 | Trundle n=1; thiếu hỗ trợ, test chọn số1 |
| 18 | T1 | Caitlyn | 21.15 | meta=0.225; draft_order=0.006; historical=0.071; matchup=0.500; synergy=0.500; composition=0.607; mastery=0.056; content=0.891 | Taliyah n=0; Corki n=0; thiếu hỗ trợ, test chọn số1 |
| 19 | T1 | Zaahen | 13.06 | meta=0.036; draft_order=0.003; historical=0.231; matchup=0.500; synergy=0.500; composition=0.378; mastery=0.000; content=0.884 | Camille n=1; thiếu hỗ trợ, test chọn số1 |
| 20 | Gen.G | Milio | 16.98 | meta=0.150; draft_order=0.011; historical=0.173; matchup=0.500; synergy=0.500; composition=0.482; mastery=0.000; content=0.590 | Karma n=0; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0136; chi phí tự cấm 0.0099; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Lee Sin | Mất pool địch 0.0135; chi phí tự cấm 0.0056; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Ashe | Mất pool địch 0.0051; chi phí tự cấm 0.0021; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Jarvan IV | Mất pool địch 0.0161; chi phí tự cấm 0.0068; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Ezreal | Mất pool địch 0.0141; chi phí tự cấm 0.0109; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Jayce | Mất pool địch 0.0075; chi phí tự cấm 0.0023; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Gnar | Mất pool địch 0.0143; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Nami | Mất pool địch 0.0032; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Ornn | Mất pool địch 0.0114; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Leona | Mất pool địch 0.0121; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 5 — Gen.G chọn trước

Fearless khóa 40 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Ezreal, Lee Sin | Nami, Ornn |
| Gen.G | Jarvan IV, Jayce, Sejuani | Cho'Gath, Sivir |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Gnar | Gwen |
| jng | Aatrox | Maokai |
| mid | Sylas | Ahri |
| bot | Ziggs | Ashe |
| sup | Leona | Rell |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | Gen.G | Ban 1 | Jarvan IV | — | Điểm cấm thống kê |
| 2 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 3 | Gen.G | Ban 2 | Jayce | — | Điểm cấm thống kê |
| 4 | T1 | Ban 2 | Ezreal | — | Điểm cấm thống kê |
| 5 | Gen.G | Ban 3 | Sejuani | — | Điểm cấm thống kê |
| 6 | T1 | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | Gen.G | Pick 1 | Ashe | bot | Chưa lộ địch |
| 8 | T1 | Pick 1 | Gnar | top | Thiếu mẫu — test chọn số1 |
| 9 | T1 | Pick 2 | Leona | sup | Thiếu mẫu — test chọn số1 |
| 10 | Gen.G | Pick 2 | Ahri | mid | Thiếu mẫu — test chọn số1 |
| 11 | Gen.G | Pick 3 | Maokai | jng | Thiếu mẫu — test chọn số1 |
| 12 | T1 | Pick 3 | Sylas | mid | Thiếu mẫu — test chọn số1 |
| 13 | T1 | Ban 4 | Nami | — | Điểm cấm thống kê |
| 14 | Gen.G | Ban 4 | Cho'Gath | — | Điểm cấm thống kê |
| 15 | T1 | Ban 5 | Ornn | — | Điểm cấm thống kê |
| 16 | Gen.G | Ban 5 | Sivir | — | Điểm cấm thống kê |
| 17 | T1 | Pick 4 | Ziggs | bot | Thiếu mẫu — test chọn số1 |
| 18 | Gen.G | Pick 4 | Rell | sup | Thiếu mẫu — test chọn số1 |
| 19 | Gen.G | Pick 5 | Gwen | top | Thiếu mẫu — test chọn số1 |
| 20 | T1 | Pick 5 | Aatrox | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: Gen.G Gwen (3 trận); T1 Aatrox (1 trận).

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | Gen.G | Ashe | 16.86 | meta=0.180; draft_order=0.012; historical=0.413; mastery=0.183; content=0.936 | Chưa lộ/không suy được cùng role |
| 8 | T1 | Gnar | 20.99 | meta=0.226; draft_order=0.012; historical=0.469; matchup=0.500; mastery=0.000; content=0.977 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | T1 | Leona | 18.91 | meta=0.110; draft_order=0.006; historical=0.354; matchup=0.500; synergy=0.500; composition=0.590; mastery=0.000; content=0.879 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 10 | Gen.G | Ahri | 22.03 | meta=0.144; draft_order=0.009; historical=0.397; matchup=0.500; synergy=0.500; composition=0.658; mastery=0.072; content=0.886 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | Gen.G | Maokai | 15.64 | meta=0.122; draft_order=0.014; historical=0.026; matchup=0.500; synergy=0.500; composition=0.485; mastery=0.000; content=0.718 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 12 | T1 | Sylas | 15.8 | meta=0.173; draft_order=0.010; historical=0.082; matchup=0.500; synergy=0.500; composition=0.425; mastery=0.000; content=0.512 | Ahri n=1; thiếu hỗ trợ, test chọn số1 |
| 17 | T1 | Ziggs | 15.62 | meta=0.070; draft_order=0.004; historical=0.097; matchup=0.500; synergy=0.500; composition=0.677; mastery=0.000; content=0.646 | Ashe n=1; thiếu hỗ trợ, test chọn số1 |
| 18 | Gen.G | Rell | 13.46 | meta=0.054; draft_order=0.006; historical=0.097; matchup=0.500; synergy=0.500; composition=0.452; mastery=0.000; content=0.912 | Leona n=1; thiếu hỗ trợ, test chọn số1 |
| 19 | Gen.G | Gwen | 17.21 | meta=0.064; draft_order=0.003; historical=0.439; matchup=0.500; synergy=0.500; composition=0.632; mastery=0.072 | Gnar n=0; thiếu hỗ trợ, test chọn số1 |
| 20 | T1 | Aatrox | 10.18 | meta=0.036; draft_order=0.006; historical=0.000; matchup=0.500; synergy=0.500; composition=0.390; mastery=0.000 | Maokai n=0; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 0, ít mẫu 5, chưa thấy 4, thiếu anchor 1.
Cặp Gen.G: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | Gen.G | Jarvan IV | Mất pool địch 0.0161; chi phí tự cấm 0.0135; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | T1 | Qiyana | Mất pool địch 0.0205; chi phí tự cấm 0.0078; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | Gen.G | Jayce | Mất pool địch 0.0176; chi phí tự cấm 0.0157; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | T1 | Ezreal | Mất pool địch 0.0154; chi phí tự cấm 0.0061; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | Gen.G | Sejuani | Mất pool địch 0.0011; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | T1 | Lee Sin | Mất pool địch 0.0203; chi phí tự cấm 0.0099; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | T1 | Nami | Mất pool địch 0.0104; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | Gen.G | Cho'Gath | Mất pool địch 0.0077; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | T1 | Ornn | Mất pool địch 0.0103; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | Gen.G | Sivir | Mất pool địch 0.0012; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

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
