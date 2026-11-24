# WLDS: 5 ván draft Fearless — T1 vs Gen.G

Đây là 5 phiên draft liên tiếp, không mô phỏng trận chiến hoặc gán tỉ số thắng/thua. Không dùng kết quả giả để ép BO5 đi đủ5ván.

Luật: [Fearless của Riot](https://lolesports.com/en-GB/news/fst-2025-primer). Tướng đã pick bởi bất kỳ đội nào bị khóa cho cả hai đội đến hết series; ban thường chỉ có hiệu lực trong ván đó. Ván5 không reset pool.

Snapshot: `{'region': 'WLDS', 'dataset_patch': '16.20', 'data_through': '2026-11-14T23:18:11+00:00', 'requested_as_of': '2026-11-24T23:59:59.999999999+00:00', 'staleness_days': 10, 'history_games': 110, 'patch_games': 98, 'lookback_days': 60, 'half_life_days': 21.0, 'claim': 'historical_snapshot_not_live_meta'}`.

Lịch thử nghiệm: giữ T1 ở Blue và Gen.G ở Red; đội chọn trước từng ván: blue, blue, blue, blue, blue. Quyền chọn trước độc lập màu đội, theo cấu hình người dùng; không suy từ thắng/thua. Nguồn luật Fearless bên trên không xác nhận một luật First Selection mới.

Cho phép test chọn số1 khi thiếu tin cậy: True. Không nâng nhãn counter hoặc độ tin cậy khi bật chế độ này.

Chiến lược ban: contextual. Chỉ legacy/contextual; không tìm nhánh phản ứng hoặc tối ưu toàn BO5.

Ứng viên: ít nhất 1 lần quan sát đúng role; ngưỡng bằng chứng 5 trận. Ưu tiên ứng viên đủ mẫu trước; chỉ xét lớp ít mẫu khi không còn ứng viên đủ mẫu ở role đang xét. Khi so giữa các role mở cũng ưu tiên lớp đủ mẫu; người dùng wishlist vẫn là lựa chọn chủ đích riêng. Đây là pool gợi ý có dữ liệu, chưa là danh mục tướng hợp lệ chính thức của sự kiện.

Cách tính điểm pick: current.

Association dương được shrink thêm theo số mẫu cặp; association âm theo số quan sát đồng đội. Không cho một cặp một-mẫu tạo bonus lift lớn như cặp có nhiều mẫu.

## Ván 1 — T1 chọn trước

Fearless khóa 0 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Olaf, Ezreal | Jarvan IV, Pantheon |
| Gen.G | Nocturne, Vi, Lee Sin | Jayce, Rumble |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Gnar | Ambessa |
| jng | Wukong | Xin Zhao |
| mid | Cassiopeia | Orianna |
| bot | Jhin | Kalista |
| sup | Nautilus | Renata Glasc |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Olaf | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Ezreal | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Cassiopeia | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Renata Glasc | sup | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Kalista | bot | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Nautilus | sup | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Jhin | bot | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Orianna | mid | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Jayce | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Jarvan IV | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Rumble | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Pantheon | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Ambessa | top | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Wukong | jng | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Gnar | top | Coverage 25%; chưa xác nhận counter |
| 20 | Gen.G | Pick 5 | Xin Zhao | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Cassiopeia | 34.21 | meta=0.651; draft_order=0.083; historical=0.413; mastery=0.085; content=0.956 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Renata Glasc | 35.6 | meta=0.743; draft_order=0.029; historical=0.299; matchup=0.500; mastery=0.000; content=0.955 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Kalista | 39.13 | meta=0.185; draft_order=0.027; historical=0.273; matchup=0.500; synergy=0.500; composition=0.865; mastery=0.000; content=0.869 | Cassiopeia n=0; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Nautilus | 34.34 | meta=0.446; draft_order=0.027; historical=0.442; matchup=0.500; synergy=0.557; composition=0.630; mastery=0.148; content=0.878 | Renata Glasc n=0; thiếu hỗ trợ, test chọn số1 |
| 11 | T1 | Jhin | 29.51 | meta=0.329; draft_order=0.056; historical=0.351; matchup=0.500; synergy=0.386; composition=0.534; mastery=0.267; content=0.943 | Kalista n=1; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Orianna | 34.17 | meta=0.504; draft_order=0.052; historical=0.425; matchup=0.500; synergy=0.500; composition=0.585; mastery=0.090; content=0.975 | Cassiopeia n=3; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | Ambessa | 27.79 | meta=0.335; draft_order=0.042; historical=0.276; matchup=0.500; synergy=0.485; composition=0.538; mastery=0.137; content=0.960 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 18 | T1 | Wukong | 26.19 | meta=0.356; draft_order=0.018; historical=0.185; matchup=0.500; synergy=0.500; composition=0.523; mastery=0.091; content=0.963 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 19 | T1 | Gnar | 22.85 | meta=0.226; draft_order=0.040; historical=0.469; matchup=0.512; synergy=0.500; composition=0.492; mastery=0.000; content=0.977 | Ambessa n=6 |
| 20 | Gen.G | Xin Zhao | 18.33 | meta=0.143; draft_order=0.005; historical=0.359; matchup=0.500; synergy=0.500; composition=0.574; mastery=0.000; content=0.911 | Wukong n=1; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 2, ít mẫu 8, chưa thấy 0, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 2, ít mẫu 7, chưa thấy 1, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0042; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0089; chi phí tự cấm 0.0038; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Olaf | Mất pool địch 0.0082; chi phí tự cấm 0.0068; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0133; chi phí tự cấm 0.0044; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Ezreal | Mất pool địch 0.0080; chi phí tự cấm 0.0067; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0094; chi phí tự cấm 0.0024; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Jayce | Mất pool địch 0.0035; chi phí tự cấm 0.0022; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Jarvan IV | Mất pool địch 0.0074; chi phí tự cấm 0.0033; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Rumble | Mất pool địch 0.0019; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Pantheon | Mất pool địch 0.0046; chi phí tự cấm 0.0009; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 0; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 2 — T1 chọn trước

Fearless khóa 10 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Seraphine, Pantheon | Rumble, Jarvan IV |
| Gen.G | Nocturne, Vi, Lee Sin | Akali, Viktor |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Olaf | K'Sante |
| jng | Trundle | Naafiri |
| mid | Locke | Syndra |
| bot | Yunara | Ezreal |
| sup | Lulu | Alistar |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Seraphine | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Pantheon | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Olaf | top | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Ezreal | bot | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Syndra | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Lulu | sup | Coverage 50%; chưa xác nhận counter |
| 11 | T1 | Pick 3 | Yunara | bot | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Alistar | sup | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Akali | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Rumble | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Viktor | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Jarvan IV | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | K'Sante | top | Coverage 33%; chưa xác nhận counter |
| 18 | T1 | Pick 4 | Locke | mid | Coverage 25%; chưa xác nhận counter |
| 19 | T1 | Pick 5 | Trundle | jng | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Naafiri | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Olaf | 32.82 | meta=0.575; draft_order=0.051; historical=0.500; mastery=0.176; content=0.961 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Ezreal | 33.11 | meta=0.523; draft_order=0.080; historical=0.309; matchup=0.500; mastery=0.182; content=0.877 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Syndra | 32.62 | meta=0.541; draft_order=0.018; historical=0.425; matchup=0.500; synergy=0.500; composition=0.486; mastery=0.135; content=0.955 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Lulu | 30.69 | meta=0.477; draft_order=0.017; historical=0.389; matchup=0.504; synergy=0.500; composition=0.519; mastery=0.085; content=0.867 | Chưa lộ/không suy được cùng role |
| 11 | T1 | Yunara | 31.27 | meta=0.227; draft_order=0.029; historical=0.387; matchup=0.500; synergy=0.492; composition=0.658; mastery=0.085; content=0.942 | Ezreal n=4; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Alistar | 25.37 | meta=0.312; draft_order=0.065; historical=0.215; matchup=0.500; synergy=0.424; composition=0.538; mastery=0.047; content=0.780 | Lulu n=0; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | K'Sante | 27.78 | meta=0.399; draft_order=0.061; historical=0.245; matchup=0.476; synergy=0.561; composition=0.532; mastery=0.000; content=0.843 | Olaf n=5 |
| 18 | T1 | Locke | 28.04 | meta=0.475; draft_order=0.032; historical=0.248; matchup=0.511; synergy=0.500; composition=0.462; mastery=0.091; content=0.769 | Syndra n=3 |
| 19 | T1 | Trundle | 22.58 | meta=0.203; draft_order=0.024; historical=0.391; matchup=0.500; synergy=0.500; composition=0.495; mastery=0.085; content=0.897 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 20 | Gen.G | Naafiri | 18.21 | meta=0.154; draft_order=0.007; historical=0.237; matchup=0.500; synergy=0.500; composition=0.561; mastery=0.000; content=0.910 | Trundle n=1; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 1, ít mẫu 9, chưa thấy 0, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 2, ít mẫu 7, chưa thấy 1, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0042; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0089; chi phí tự cấm 0.0038; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Seraphine | Mất pool địch 0.0070; chi phí tự cấm 0.0045; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0147; chi phí tự cấm 0.0044; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Pantheon | Mất pool địch 0.0048; chi phí tự cấm 0.0014; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0142; chi phí tự cấm 0.0058; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Akali | Mất pool địch 0.0040; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Rumble | Mất pool địch 0.0060; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Viktor | Mất pool địch 0.0053; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Jarvan IV | Mất pool địch 0.0106; chi phí tự cấm 0.0049; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 10; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 3 — T1 chọn trước

Fearless khóa 20 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Ashe, Pantheon | Skarner, Maokai |
| Gen.G | Nocturne, Vi, Lee Sin | Karma, Rakan |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Rumble | Jayce |
| jng | Jarvan IV | Sejuani |
| mid | Viktor | Akali |
| bot | Lucian | Xayah |
| sup | Milio | Seraphine |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Ashe | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Pantheon | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Jarvan IV | jng | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Seraphine | sup | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Akali | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Rumble | top | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Viktor | mid | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Jayce | top | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Karma | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Skarner | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Rakan | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Maokai | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Xayah | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Lucian | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Milio | sup | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Sejuani | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Jarvan IV | 30.7 | meta=0.520; draft_order=0.058; historical=0.326; mastery=0.239; content=0.955 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Seraphine | 29.32 | meta=0.418; draft_order=0.025; historical=0.433; matchup=0.500; mastery=0.183; content=0.893 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Akali | 29.69 | meta=0.509; draft_order=0.013; historical=0.066; matchup=0.500; synergy=0.500; composition=0.523; mastery=0.134; content=0.824 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Rumble | 30.03 | meta=0.475; draft_order=0.033; historical=0.102; matchup=0.500; synergy=0.420; composition=0.578; mastery=0.091; content=0.935 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | T1 | Viktor | 28.35 | meta=0.326; draft_order=0.026; historical=0.408; matchup=0.500; synergy=0.509; composition=0.584; mastery=0.085; content=0.948 | Akali n=1; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Jayce | 25.85 | meta=0.499; draft_order=0.011; historical=0.214; matchup=0.500; synergy=0.500; composition=0.431; mastery=0.000; content=0.873 | Rumble n=0; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | Xayah | 19.17 | meta=0.169; draft_order=0.009; historical=0.232; matchup=0.500; synergy=0.500; composition=0.450; mastery=0.156; content=0.981 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 18 | T1 | Lucian | 22.43 | meta=0.250; draft_order=0.020; historical=0.219; matchup=0.500; synergy=0.500; composition=0.517; mastery=0.091; content=0.866 | Xayah n=3; thiếu hỗ trợ, test chọn số1 |
| 19 | T1 | Milio | 22.39 | meta=0.150; draft_order=0.018; historical=0.173; matchup=0.500; synergy=0.508; composition=0.612; mastery=0.091; content=0.650 | Seraphine n=3; thiếu hỗ trợ, test chọn số1 |
| 20 | Gen.G | Sejuani | 11.86 | meta=0.054; draft_order=0.009; historical=0.030; matchup=0.500; synergy=0.500; composition=0.481; mastery=0.000; content=0.371 | Jarvan IV n=1; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 6, ít mẫu 4, chưa thấy 0, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 5, chưa thấy 5, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0042; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0089; chi phí tự cấm 0.0038; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Ashe | Mất pool địch 0.0040; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0147; chi phí tự cấm 0.0044; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Pantheon | Mất pool địch 0.0076; chi phí tự cấm 0.0048; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0168; chi phí tự cấm 0.0070; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Karma | Mất pool địch 0.0042; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Skarner | Mất pool địch 0.0034; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Rakan | Mất pool địch 0.0042; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Maokai | Mất pool địch 0.0092; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 20; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 4 — T1 chọn trước

Fearless khóa 30 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Qiyana, Ashe, Corki | Karma, Nami |
| Gen.G | Nocturne, Vi, Lee Sin | Skarner, Maokai |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Camille | Renekton |
| jng | Cho'Gath | Pantheon |
| mid | Galio | Taliyah |
| bot | Kai'Sa | Sivir |
| sup | Rakan | Leona |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Qiyana | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Ashe | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Corki | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Galio | mid | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Pantheon | jng | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Taliyah | mid | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Camille | top | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Rakan | sup | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Renekton | top | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Skarner | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Karma | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Maokai | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Nami | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Sivir | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Kai'Sa | bot | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Cho'Gath | jng | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Leona | sup | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: không có dưới ngưỡng5trận.

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Galio | 20.07 | meta=0.369; draft_order=0.007; historical=0.313; mastery=0.059; content=0.882 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Pantheon | 25.56 | meta=0.330; draft_order=0.034; historical=0.273; matchup=0.500; mastery=0.156; content=0.957 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Taliyah | 27.75 | meta=0.182; draft_order=0.008; historical=0.397; matchup=0.500; synergy=0.467; composition=0.754; mastery=0.137; content=0.975 | Galio n=0; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Camille | 26.65 | meta=0.272; draft_order=0.023; historical=0.254; matchup=0.500; synergy=0.500; composition=0.718; mastery=0.085; content=0.927 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | T1 | Rakan | 22.5 | meta=0.174; draft_order=0.036; historical=0.142; matchup=0.500; synergy=0.500; composition=0.570; mastery=0.150; content=0.979 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Renekton | 22.57 | meta=0.287; draft_order=0.016; historical=0.391; matchup=0.500; synergy=0.500; composition=0.470; mastery=0.000; content=0.877 | Camille n=2; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | Sivir | 17.82 | meta=0.103; draft_order=0.021; historical=0.188; matchup=0.500; synergy=0.500; composition=0.601; mastery=0.000; content=0.982 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 18 | T1 | Kai'Sa | 20.04 | meta=0.204; draft_order=0.027; historical=0.254; matchup=0.500; synergy=0.500; composition=0.442; mastery=0.085; content=0.944 | Sivir n=0; thiếu hỗ trợ, test chọn số1 |
| 19 | T1 | Cho'Gath | 11.28 | meta=0.042; draft_order=0.007; historical=0.030; matchup=0.500; synergy=0.500; composition=0.372; mastery=0.000; content=0.591 | Pantheon n=0; thiếu hỗ trợ, test chọn số1 |
| 20 | Gen.G | Leona | 18.04 | meta=0.110; draft_order=0.031; historical=0.354; matchup=0.500; synergy=0.500; composition=0.369; mastery=0.182; content=0.907 | Rakan n=1; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 0, ít mẫu 4, chưa thấy 6, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 1, ít mẫu 3, chưa thấy 6, thiếu anchor 0.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Qiyana | Mất pool địch 0.0042; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0176; chi phí tự cấm 0.0058; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Ashe | Mất pool địch 0.0051; chi phí tự cấm 0.0021; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0195; chi phí tự cấm 0.0082; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Corki | Mất pool địch 0.0029; chi phí tự cấm 0.0002; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0168; chi phí tự cấm 0.0070; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Skarner | Mất pool địch 0.0107; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Karma | Mất pool địch 0.0026; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Maokai | Mất pool địch 0.0091; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Nami | Mất pool địch 0.0120; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 30; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

## Ván 5 — T1 chọn trước

Fearless khóa 40 tướng từ các ván trước.

| Đội | Cấm pha1 (theo thứ tự) | Cấm pha2 (theo thứ tự) |
|---|---|---|
| T1 | Ashe, Qiyana, Corki | Miss Fortune, Maokai |
| Gen.G | Nocturne, Vi, Lee Sin | Ornn, Zaahen |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Gwen | Jax |
| jng | Skarner | Aatrox |
| mid | Annie | Ahri |
| bot | Caitlyn | Tristana |
| sup | Karma | Nami |

### Toàn bộ20lượt

| Lượt | Đội | Ban/Pick số | Tướng | Role | Độ tin cậy đối đầu |
|---:|---|---|---|---|---|
| 1 | T1 | Ban 1 | Ashe | — | Điểm cấm thống kê |
| 2 | Gen.G | Ban 1 | Nocturne | — | Điểm cấm thống kê |
| 3 | T1 | Ban 2 | Qiyana | — | Điểm cấm thống kê |
| 4 | Gen.G | Ban 2 | Vi | — | Điểm cấm thống kê |
| 5 | T1 | Ban 3 | Corki | — | Điểm cấm thống kê |
| 6 | Gen.G | Ban 3 | Lee Sin | — | Điểm cấm thống kê |
| 7 | T1 | Pick 1 | Karma | sup | Chưa lộ địch |
| 8 | Gen.G | Pick 1 | Ahri | mid | Thiếu mẫu — test chọn số1 |
| 9 | Gen.G | Pick 2 | Jax | top | Thiếu mẫu — test chọn số1 |
| 10 | T1 | Pick 2 | Caitlyn | bot | Thiếu mẫu — test chọn số1 |
| 11 | T1 | Pick 3 | Skarner | jng | Thiếu mẫu — test chọn số1 |
| 12 | Gen.G | Pick 3 | Nami | sup | Thiếu mẫu — test chọn số1 |
| 13 | Gen.G | Ban 4 | Ornn | — | Điểm cấm thống kê |
| 14 | T1 | Ban 4 | Miss Fortune | — | Điểm cấm thống kê |
| 15 | Gen.G | Ban 5 | Zaahen | — | Điểm cấm thống kê |
| 16 | T1 | Ban 5 | Maokai | — | Điểm cấm thống kê |
| 17 | Gen.G | Pick 4 | Tristana | bot | Thiếu mẫu — test chọn số1 |
| 18 | T1 | Pick 4 | Annie | mid | Thiếu mẫu — test chọn số1 |
| 19 | T1 | Pick 5 | Gwen | top | Thiếu mẫu — test chọn số1 |
| 20 | Gen.G | Pick 5 | Aatrox | jng | Thiếu mẫu — test chọn số1 |

Lựa chọn ít mẫu: T1 Gwen (3 trận); Gen.G Aatrox (1 trận).

### Căn cứ từng lượt pick

| Lượt | Đội | Pick | Điểm | Thành phần | Đối đầu / thiếu bằng chứng |
|---:|---|---|---:|---|---|
| 7 | T1 | Karma | 15.75 | meta=0.211; draft_order=0.018; historical=0.203; mastery=0.154; content=0.921 | Chưa lộ/không suy được cùng role |
| 8 | Gen.G | Ahri | 18.63 | meta=0.144; draft_order=0.006; historical=0.397; matchup=0.500; mastery=0.072; content=0.886 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 9 | Gen.G | Jax | 20.68 | meta=0.205; draft_order=0.006; historical=0.189; matchup=0.500; synergy=0.500; composition=0.650; mastery=0.000; content=0.858 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 10 | T1 | Caitlyn | 24.85 | meta=0.225; draft_order=0.049; historical=0.071; matchup=0.500; synergy=0.500; composition=0.752; mastery=0.056; content=0.891 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 11 | T1 | Skarner | 19.2 | meta=0.169; draft_order=0.004; historical=0.215; matchup=0.500; synergy=0.500; composition=0.638; mastery=0.000; content=0.697 | Chưa lộ/không suy được cùng role; thiếu hỗ trợ, test chọn số1 |
| 12 | Gen.G | Nami | 16.21 | meta=0.057; draft_order=0.004; historical=0.376; matchup=0.500; synergy=0.500; composition=0.401; mastery=0.090; content=0.758 | Karma n=2; thiếu hỗ trợ, test chọn số1 |
| 17 | Gen.G | Tristana | 14.75 | meta=0.079; draft_order=0.012; historical=0.158; matchup=0.500; synergy=0.500; composition=0.409; mastery=0.000; content=0.806 | Caitlyn n=0; thiếu hỗ trợ, test chọn số1 |
| 18 | T1 | Annie | 16.95 | meta=0.133; draft_order=0.033; historical=0.267; matchup=0.500; synergy=0.500; composition=0.380; mastery=0.085; content=0.708 | Ahri n=1; thiếu hỗ trợ, test chọn số1 |
| 19 | T1 | Gwen | 15.91 | meta=0.064; draft_order=0.003; historical=0.439; matchup=0.500; synergy=0.500; composition=0.500; mastery=0.063 | Jax n=0; thiếu hỗ trợ, test chọn số1 |
| 20 | Gen.G | Aatrox | 10.84 | meta=0.036; draft_order=0.006; historical=0.000; matchup=0.500; synergy=0.500; composition=0.413; mastery=0.000 | Skarner n=0; thiếu hỗ trợ, test chọn số1 |
Cặp T1: đủ mẫu 0, ít mẫu 4, chưa thấy 6, thiếu anchor 0.
Cặp Gen.G: đủ mẫu 0, ít mẫu 1, chưa thấy 8, thiếu anchor 1.

### Căn cứ từng lượt ban

| Lượt | Đội | Ban | Lý do | Ghi chú |
|---:|---|---|---|---|
| 1 | T1 | Ashe | Mất pool địch 0.0080; chi phí tự cấm 0.0036; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 2 | Gen.G | Nocturne | Mất pool địch 0.0091; chi phí tự cấm 0.0035; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 3 | T1 | Qiyana | Mất pool địch 0.0164; chi phí tự cấm 0.0133; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 4 | Gen.G | Vi | Mất pool địch 0.0221; chi phí tự cấm 0.0091; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 5 | T1 | Corki | Mất pool địch 0.0046; chi phí tự cấm 0.0023; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 6 | Gen.G | Lee Sin | Mất pool địch 0.0211; chi phí tự cấm 0.0094; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 13 | Gen.G | Ornn | Mất pool địch 0.0119; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 14 | T1 | Miss Fortune | Mất pool địch 0.0100; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 15 | Gen.G | Zaahen | Mất pool địch 0.0087; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=True; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |
| 16 | T1 | Maokai | Mất pool địch 0.0099; chi phí tự cấm 0.0000; đội mình lấy lượt pick tới trước địch=False; Fearless khóa 40; chấm theo pool ngữ cảnh | Không tìm nhánh phản ứng |

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
