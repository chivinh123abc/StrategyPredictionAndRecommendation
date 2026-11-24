# Rà soát50lượt pick contextual — T1/Gen.G

Đầu vào: 5draftWorlds cutoff13/11/2026 patchdataset16.20, contextual và chếđộtest chọn gợi ý1 khi thiếu tin cậy. Không sửa công thức/đổi lựa chọn, không train model trong audit này.

## Kết quả chính

- Đã tái dựng và đối chiếu50trạng thái trước lượt; score/top1 khớp phiên đã lưu. Đây là tính tái lập, không chứng minh chọn đúng chiến thuật.
- 38/50pick có địch đã lộ nhưng không có đối đầu đủ mẫu; 5/50pick chưa thấy địch; 7/50có ít nhất một đối đầu đủ mẫu. Có mẫu vẫn chưa chứng minh counter.
- Đã kiểm tra248phương án cùng role, hợp lệ tại đúng thời điểm. Nếu còn ít hơn3lựa chọn thì không bịa thêm cho đủ3–5.
- 3pick dưới5trận; xem bảng riêng. Tướng ít mẫu là giới hạn bằng chứng, không tự động là lựa chọn yếu.

| Bỏ thành phần để kiểm tra độ nhạy | Số lượt đổi top1 |
|---|---:|
| meta | 13/50 |
| content | 1/50 |
| composition | 14/50 |
| mastery | 3/50 |
| matchup | 3/50 |

Các lượt có thể nhạy với nhiều thành phần nên không cộng các số trên thành số pick sai. Bỏ thành phần là chẩn đoán công thức, không là đề xuất thay đổi policy.

## Các lựa chọn ít mẫu

| Ván | Lượt | Đội | Role | Pick | Số trận |
|---:|---:|---|---|---|---:|
| 5 | 17 | Gen.G | sup | Poppy | 2 |
| 5 | 19 | T1 | top | Aurora | 2 |
| 5 | 20 | Gen.G | jng | Nasus | 1 |

## Các vấn đề cần xử lý tiếp, chưa sửa trong lượt này

1. Thiếu bằng chứng đối đầu là vấn đề lớn nhất. Không dùng điểmmeta/cosine thay thế bằng chứng counter; cần phân biệt blindpick với cóđịch nhưng thiếu mẫu.
2. Phối hợp làm đổi nhiều lựa chọn khi bỏ thành phần; cần kiểm chứng cặp ít mẫu và các giả định về tần suất đồngchọn, không coi top1 là đáp án chuẩn.
3. Pool cuốiFearless buộc backoff tướng ít mẫu; báo cáo coverage và độ tin cậy trước khi kết luận chất lượng.
4. Audit chỉ so tướng cùng role đang gán. Galio top/mid hoặc tướngflex khác chưa được so như nhiều cách phânvai; đây là phần cần thiết kế sau, không được kết luận Galio top sai chỉ vì hiếm.

## Toàn bộ50lượt

| Ván | Lượt | Đội | Role | Pick | n | Địch lộ | Coverage | Chênh điểm với phương án2 | Phương án khác |
|---:|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | 7 | T1 | sup | Renata Glasc | 19 | 0 | 0% | 8.788 | Nautilus, Lulu, Alistar |
| 1 | 8 | Gen.G | top | Olaf | 20 | 1 | 0% | 6.731 | Rumble, Jayce, K'Sante |
| 1 | 9 | Gen.G | mid | Cassiopeia | 16 | 1 | 0% | 7.399 | Syndra, Akali, Galio |
| 1 | 10 | T1 | bot | Kalista | 18 | 2 | 0% | 17.598 | Ezreal, Jhin, Lucian |
| 1 | 11 | T1 | jng | Jarvan IV | 27 | 2 | 0% | 9.325 | Wukong, Pantheon, Xin Zhao |
| 1 | 12 | Gen.G | sup | Nautilus | 27 | 3 | 0% | 8.219 | Lulu, Leona, Alistar |
| 1 | 17 | Gen.G | bot | Ezreal | 31 | 3 | 33% | 5.304 | Kai'Sa, Yunara, Corki |
| 1 | 18 | T1 | top | Ambessa | 26 | 4 | 25% | 1.890 | Rumble, K'Sante, Jayce |
| 1 | 19 | T1 | mid | Syndra | 25 | 4 | 25% | 2.257 | Viktor, Akali, Galio |
| 1 | 20 | Gen.G | jng | Pantheon | 18 | 5 | 0% | 3.360 | Trundle, Naafiri, Xin Zhao |
| 2 | 7 | Gen.G | jng | Lee Sin | 30 | 0 | 0% | 9.237 | Wukong, Trundle, Xin Zhao |
| 2 | 8 | T1 | sup | Lulu | 25 | 1 | 100% | 3.563 | Seraphine, Alistar, Karma |
| 2 | 9 | T1 | bot | Yunara | 21 | 1 | 100% | 24.787 | Jhin, Sivir, Tristana |
| 2 | 10 | Gen.G | bot | Jhin | 23 | 2 | 0% | 7.339 | Ashe, Caitlyn, Kai'Sa |
| 2 | 11 | Gen.G | top | Rumble | 28 | 2 | 0% | 5.425 | Galio, K'Sante, Camille |
| 2 | 12 | T1 | mid | Akali | 15 | 3 | 0% | 0.083 | Viktor, Galio, Ryze |
| 2 | 17 | T1 | top | Galio | 6 | 3 | 32% | 0.748 | Gnar, Camille, Ornn |
| 2 | 18 | Gen.G | mid | Viktor | 22 | 4 | 0% | 6.483 | Anivia, Ryze, Taliyah |
| 2 | 19 | Gen.G | sup | Leona | 9 | 4 | 0% | 3.872 | Rakan, Karma, Milio |
| 2 | 20 | T1 | jng | Skarner | 8 | 5 | 0% | 1.414 | Sejuani, Xin Zhao, Maokai |
| 3 | 7 | T1 | mid | Orianna | 25 | 0 | 0% | 3.615 | Locke, Taliyah, Ahri |
| 3 | 8 | Gen.G | mid | Locke | 14 | 1 | 100% | 4.501 | Taliyah, Ahri, Anivia |
| 3 | 9 | Gen.G | top | K'Sante | 23 | 1 | 0% | 3.158 | Gnar, Camille, Jax |
| 3 | 10 | T1 | top | Gnar | 16 | 2 | 0% | 3.763 | Renekton, Jax, Camille |
| 3 | 11 | T1 | jng | Wukong | 15 | 2 | 0% | 2.374 | Xin Zhao, Trundle, Naafiri |
| 3 | 12 | Gen.G | sup | Alistar | 26 | 3 | 0% | 4.391 | Karma, Rakan, Milio |
| 3 | 17 | Gen.G | bot | Corki | 9 | 3 | 0% | 0.266 | Kai'Sa, Lucian, Caitlyn |
| 3 | 18 | T1 | bot | Lucian | 20 | 4 | 0% | 2.085 | Kai'Sa, Xayah, Caitlyn |
| 3 | 19 | T1 | sup | Milio | 17 | 4 | 0% | 8.856 | Rell, Nami, Camille |
| 3 | 20 | Gen.G | jng | Xin Zhao | 7 | 5 | 0% | 3.993 | Maokai, Cho'Gath, Sejuani |
| 4 | 7 | Gen.G | sup | Seraphine | 20 | 0 | 0% | 13.756 | Rakan, Rell, Camille |
| 4 | 8 | T1 | bot | Ashe | 17 | 1 | 0% | 1.682 | Xayah, Kai'Sa, Caitlyn |
| 4 | 9 | T1 | top | Renekton | 12 | 1 | 0% | 5.579 | Camille, Jax, Ornn |
| 4 | 10 | Gen.G | mid | Ahri | 10 | 2 | 0% | 4.386 | Anivia, Taliyah, LeBlanc |
| 4 | 11 | Gen.G | top | Camille | 12 | 2 | 0% | 2.977 | Ornn, Jax, Zaahen |
| 4 | 12 | T1 | sup | Rakan | 15 | 3 | 0% | 6.591 | Rell, Poppy, Neeko |
| 4 | 17 | T1 | mid | Anivia | 8 | 3 | 0% | 0.991 | Annie, Ryze, LeBlanc |
| 4 | 18 | Gen.G | bot | Miss Fortune | 6 | 4 | 0% | 0.445 | Caitlyn, Sivir, Tristana |
| 4 | 19 | Gen.G | jng | Maokai | 7 | 4 | 0% | 3.633 | Sejuani, Cho'Gath, Aatrox |
| 4 | 20 | T1 | jng | Sejuani | 6 | 5 | 0% | 0.835 | Cho'Gath, Nasus, Aatrox |
| 5 | 7 | T1 | jng | Trundle | 12 | 0 | 0% | 12.444 | Cho'Gath, Aatrox, Malphite |
| 5 | 8 | Gen.G | bot | Xayah | 12 | 1 | 0% | 1.084 | Kai'Sa, Caitlyn, Sivir |
| 5 | 9 | Gen.G | top | Ornn | 9 | 1 | 0% | 3.019 | Jax, Zaahen, Aurora |
| 5 | 10 | T1 | bot | Kai'Sa | 12 | 2 | 0% | 0.610 | Caitlyn, Sivir, Ziggs |
| 5 | 11 | T1 | sup | Karma | 17 | 2 | 0% | 5.715 | Rell, Poppy, Yuumi |
| 5 | 12 | Gen.G | mid | Annie | 8 | 3 | 0% | 1.158 | Ryze, Aurora, Sylas |
| 5 | 17 | Gen.G | sup | Poppy | 2 | 3 | 0% | 0.179 | Nami, Yuumi, Shen |
| 5 | 18 | T1 | mid | Ryze | 11 | 4 | 0% | 1.914 | LeBlanc, Sylas, Aurora |
| 5 | 19 | T1 | top | Aurora | 2 | 4 | 0% | 0.379 | Gwen, Vayne, Kennen |
| 5 | 20 | Gen.G | jng | Nasus | 1 | 5 | 0% | 0.277 | Aatrox, Lillia, Malphite |

Chênh điểm tính trên thang100; không phải chênh xác suất thắng. Các alternative không được mô tả là tốt hơn về cơ chế.

## Căn cứ từng lượt và top5phương án khác

### Ván1 lượt7: T1 — Renata Glasc (sup, F1)

Đồng đội đã lộ: {}. Địch đã lộ: {}.
Pool hợp lệ tại role:22ứngviên. Pick:19trận; score:34.178điểm, baseline:0.34178, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.77956 | 1.000 |
| draft_order | 0.02017 | 1.000 |
| historical | 0.31708 | 0.250 |
| mastery | 0.00000 | 0.500 |
| content | 0.95052 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Nautilus | 25.389 | 27 | 0% | observed_candidate |
| Lulu | 24.367 | 25 | 0% | observed_candidate |
| Alistar | 16.688 | 26 | 0% | observed_candidate |
| Karma | 15.696 | 17 | 0% | observed_candidate |
| Rakan | 13.624 | 15 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Nautilus.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt8: Gen.G — Olaf (top, S1)

Đồng đội đã lộ: {}. Địch đã lộ: {"sup": "Renata Glasc"}.
Pool hợp lệ tại role:28ứngviên. Pick:20trận; score:35.782điểm, baseline:0.35782, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.59905 | 1.000 |
| draft_order | 0.02556 | 1.000 |
| historical | 0.48103 | 0.250 |
| matchup | 0.50000 | 0.500 |
| mastery | 0.21384 | 0.500 |
| content | 0.96902 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rumble | 29.050 | 28 | 0% | observed_candidate |
| Jayce | 26.240 | 14 | 0% | observed_candidate |
| K'Sante | 24.753 | 23 | 0% | observed_candidate |
| Ambessa | 24.213 | 26 | 0% | observed_candidate |
| Galio | 23.724 | 6 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt9: Gen.G — Cassiopeia (mid, S2)

Đồng đội đã lộ: {"top": "Olaf"}. Địch đã lộ: {"sup": "Renata Glasc"}.
Pool hợp lệ tại role:27ứngviên. Pick:16trận; score:40.364điểm, baseline:0.36354, geometriclift:1.18493.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.66216 | 1.000 |
| draft_order | 0.02057 | 1.000 |
| historical | 0.38641 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.67231 | 1.000 |
| mastery | 0.11221 | 0.500 |
| content | 0.98324 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Cassiopeia–Olaf (mid/top) | 4/20 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Syndra | 32.965 | 25 | 0% | observed_candidate |
| Akali | 29.788 | 15 | 0% | observed_candidate |
| Galio | 28.263 | 10 | 0% | observed_candidate |
| Locke | 27.620 | 14 | 0% | observed_candidate |
| Viktor | 24.165 | 22 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt10: T1 — Kalista (bot, F2)

Đồng đội đã lộ: {"sup": "Renata Glasc"}. Địch đã lộ: {"top": "Olaf", "mid": "Cassiopeia"}.
Pool hợp lệ tại role:20ứngviên. Pick:18trận; score:41.412điểm, baseline:0.20912, geometriclift:2.67321.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.17993 | 1.000 |
| draft_order | 0.03789 | 1.000 |
| historical | 0.29031 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.87270 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.87431 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Kalista–Renata Glasc (bot/sup) | 18/19 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Ezreal | 23.814 | 31 | 0% | observed_candidate |
| Jhin | 22.439 | 23 | 0% | observed_candidate |
| Lucian | 18.697 | 20 | 0% | observed_candidate |
| Xayah | 18.249 | 12 | 0% | observed_candidate |
| Yunara | 18.020 | 21 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏcomposition→Ezreal.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt11: T1 — Jarvan IV (jng, F3)

Đồng đội đã lộ: {"sup": "Renata Glasc", "bot": "Kalista"}. Địch đã lộ: {"top": "Olaf", "mid": "Cassiopeia"}.
Pool hợp lệ tại role:15ứngviên. Pick:27trận; score:35.745điểm, baseline:0.34494, geometriclift:1.05643.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.54025 | 1.000 |
| draft_order | 0.02654 | 1.000 |
| historical | 0.33986 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.57426 | 1.000 |
| mastery | 0.23948 | 0.500 |
| content | 0.95295 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Jarvan IV–Renata Glasc (jng/sup) | 4/19 | sparse_pair |
| Jarvan IV–Kalista (jng/bot) | 4/18 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Wukong | 26.420 | 15 | 0% | observed_candidate |
| Pantheon | 24.263 | 18 | 0% | observed_candidate |
| Xin Zhao | 21.892 | 7 | 0% | observed_candidate |
| Trundle | 17.169 | 12 | 0% | observed_candidate |
| Maokai | 16.769 | 7 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt12: Gen.G — Nautilus (sup, S3)

Đồng đội đã lộ: {"top": "Olaf", "mid": "Cassiopeia"}. Địch đã lộ: {"sup": "Renata Glasc", "bot": "Kalista", "jng": "Jarvan IV"}.
Pool hợp lệ tại role:21ứngviên. Pick:27trận; score:34.080điểm, baseline:0.32541, geometriclift:1.07177.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.42390 | 1.000 |
| draft_order | 0.03323 | 1.000 |
| historical | 0.44229 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.55679 | 0.250 |
| composition | 0.56468 | 1.000 |
| mastery | 0.25353 | 0.500 |
| content | 0.87796 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Nautilus–Olaf (sup/top) | 2/20 | sparse_pair |
| Nautilus–Cassiopeia (sup/mid) | 5/16 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Lulu | 25.861 | 25 | 67% | observed_candidate |
| Leona | 24.765 | 9 | 0% | observed_candidate |
| Alistar | 23.300 | 26 | 0% | observed_candidate |
| Karma | 15.417 | 17 | 0% | observed_candidate |
| Rakan | 14.411 | 15 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt17: Gen.G — Ezreal (bot, S4)

Đồng đội đã lộ: {"top": "Olaf", "mid": "Cassiopeia", "sup": "Nautilus"}. Địch đã lộ: {"sup": "Renata Glasc", "bot": "Kalista", "jng": "Jarvan IV"}.
Pool hợp lệ tại role:18ứngviên. Pick:31trận; score:29.883điểm, baseline:0.32919, geometriclift:0.86848.
Đối đầu: coverage33%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.52507 | 1.000 |
| draft_order | 0.04021 | 1.000 |
| historical | 0.31970 | 0.250 |
| matchup | 0.51290 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.44257 | 1.000 |
| mastery | 0.14381 | 0.500 |
| content | 0.86511 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Ezreal–Olaf (bot/top) | 1/20 | sparse_pair |
| Ezreal–Cassiopeia (bot/mid) | 2/16 | sparse_pair |
| Ezreal–Nautilus (bot/sup) | 4/27 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Kai'Sa | 24.579 | 12 | 0% | observed_candidate |
| Yunara | 20.294 | 21 | 0% | observed_candidate |
| Corki | 19.661 | 9 | 0% | observed_candidate |
| Tristana | 16.666 | 7 | 0% | observed_candidate |
| Xayah | 16.300 | 12 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Kai'Sa.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt18: T1 — Ambessa (top, F4)

Đồng đội đã lộ: {"sup": "Renata Glasc", "bot": "Kalista", "jng": "Jarvan IV"}. Địch đã lộ: {"top": "Olaf", "mid": "Cassiopeia", "sup": "Nautilus", "bot": "Ezreal"}.
Pool hợp lệ tại role:27ứngviên. Pick:26trận; score:29.738điểm, baseline:0.28990, geometriclift:1.03671.
Đối đầu: coverage25%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.34157 | 1.000 |
| draft_order | 0.05415 | 1.000 |
| historical | 0.28756 | 0.250 |
| matchup | 0.49487 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.54945 | 1.000 |
| mastery | 0.21306 | 0.500 |
| content | 0.97066 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Ambessa–Renata Glasc (top/sup) | 3/19 | sparse_pair |
| Ambessa–Kalista (top/bot) | 3/18 | sparse_pair |
| Ambessa–Jarvan IV (top/jng) | 4/27 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rumble | 27.848 | 28 | 50% | observed_candidate |
| K'Sante | 26.324 | 23 | 0% | observed_candidate |
| Jayce | 26.089 | 14 | 0% | observed_candidate |
| Renekton | 22.990 | 12 | 0% | observed_candidate |
| Camille | 19.693 | 12 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏcomposition→Jayce.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt19: T1 — Syndra (mid, F5)

Đồng đội đã lộ: {"sup": "Renata Glasc", "bot": "Kalista", "jng": "Jarvan IV", "top": "Ambessa"}. Địch đã lộ: {"top": "Olaf", "mid": "Cassiopeia", "sup": "Nautilus", "bot": "Ezreal"}.
Pool hợp lệ tại role:24ứngviên. Pick:25trận; score:28.241điểm, baseline:0.34515, geometriclift:0.74667.
Đối đầu: coverage25%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.56247 | 1.000 |
| draft_order | 0.03532 | 1.000 |
| historical | 0.40739 | 0.250 |
| matchup | 0.48889 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.37218 | 1.000 |
| mastery | 0.15414 | 0.500 |
| content | 0.96386 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Syndra–Renata Glasc (mid/sup) | 0/19 | unobserved_pair |
| Syndra–Kalista (mid/bot) | 0/18 | unobserved_pair |
| Syndra–Jarvan IV (mid/jng) | 2/27 | sparse_pair |
| Syndra–Ambessa (mid/top) | 1/26 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Viktor | 25.983 | 22 | 0% | observed_candidate |
| Akali | 25.688 | 15 | 0% | observed_candidate |
| Galio | 24.032 | 10 | 0% | observed_candidate |
| Ahri | 22.583 | 10 | 0% | observed_candidate |
| Taliyah | 19.895 | 10 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Ahri.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván1 lượt20: Gen.G — Pantheon (jng, S5)

Đồng đội đã lộ: {"top": "Olaf", "mid": "Cassiopeia", "sup": "Nautilus", "bot": "Ezreal"}. Địch đã lộ: {"sup": "Renata Glasc", "bot": "Kalista", "jng": "Jarvan IV", "top": "Ambessa", "mid": "Syndra"}.
Pool hợp lệ tại role:13ứngviên. Pick:18trận; score:24.708điểm, baseline:0.26191, geometriclift:0.92478.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.33594 | 1.000 |
| draft_order | 0.01226 | 1.000 |
| historical | 0.29031 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.48685 | 1.000 |
| mastery | 0.10186 | 0.500 |
| content | 0.96163 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Pantheon–Olaf (jng/top) | 3/20 | sparse_pair |
| Pantheon–Cassiopeia (jng/mid) | 1/16 | sparse_pair |
| Pantheon–Nautilus (jng/sup) | 1/27 | sparse_pair |
| Pantheon–Ezreal (jng/bot) | 2/31 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Trundle | 21.347 | 12 | 0% | observed_candidate |
| Naafiri | 16.649 | 9 | 0% | observed_candidate |
| Xin Zhao | 16.000 | 7 | 0% | observed_candidate |
| Skarner | 11.055 | 8 | 0% | observed_candidate |
| Maokai | 9.973 | 7 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt7: Gen.G — Lee Sin (jng, F1)

Đồng đội đã lộ: {}. Địch đã lộ: {}.
Pool hợp lệ tại role:13ứngviên. Pick:30trận; score:29.508điểm, baseline:0.29508, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.52449 | 1.000 |
| draft_order | 0.09674 | 1.000 |
| historical | 0.36142 | 0.250 |
| mastery | 0.11235 | 0.500 |
| content | 0.73230 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Wukong | 20.271 | 15 | 0% | observed_candidate |
| Trundle | 14.521 | 12 | 0% | observed_candidate |
| Xin Zhao | 11.739 | 7 | 0% | observed_candidate |
| Naafiri | 10.324 | 9 | 0% | observed_candidate |
| Skarner | 9.331 | 8 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt8: T1 — Lulu (sup, S1)

Đồng đội đã lộ: {}. Địch đã lộ: {"jng": "Lee Sin"}.
Pool hợp lệ tại role:21ứngviên. Pick:25trận; score:29.417điểm, baseline:0.29417, geometriclift:1.00000.
Đối đầu: coverage100%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.43798 | 1.000 |
| draft_order | 0.05027 | 1.000 |
| historical | 0.40739 | 0.250 |
| matchup | 0.54706 | 0.500 |
| mastery | 0.08514 | 0.500 |
| content | 0.79264 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Seraphine | 25.854 | 20 | 0% | observed_candidate |
| Alistar | 23.247 | 26 | 100% | observed_candidate |
| Karma | 21.305 | 17 | 0% | observed_candidate |
| Rakan | 19.053 | 15 | 0% | observed_candidate |
| Milio | 16.828 | 17 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt9: T1 — Yunara (bot, S2)

Đồng đội đã lộ: {"sup": "Lulu"}. Địch đã lộ: {"jng": "Lee Sin"}.
Pool hợp lệ tại role:19ứngviên. Pick:21trận; score:44.250điểm, baseline:0.24597, geometriclift:2.43319.
Đối đầu: coverage100%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.22476 | 1.000 |
| draft_order | 0.03836 | 1.000 |
| historical | 0.36547 | 0.250 |
| matchup | 0.53571 | 0.500 |
| synergy | 0.50493 | 0.250 |
| composition | 0.83869 | 1.000 |
| mastery | 0.08514 | 0.500 |
| content | 0.94342 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Yunara–Lulu (bot/sup) | 19/25 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Jhin | 19.463 | 23 | 0% | observed_candidate |
| Sivir | 18.792 | 6 | 0% | observed_candidate |
| Tristana | 18.748 | 7 | 0% | observed_candidate |
| Lucian | 15.154 | 20 | 0% | observed_candidate |
| Ashe | 14.258 | 17 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏcomposition→Jhin.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt10: Gen.G — Jhin (bot, F2)

Đồng đội đã lộ: {"jng": "Lee Sin"}. Địch đã lộ: {"sup": "Lulu", "bot": "Yunara"}.
Pool hợp lệ tại role:18ứngviên. Pick:23trận; score:32.704điểm, baseline:0.29578, geometriclift:1.15704.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.33513 | 1.000 |
| draft_order | 0.03601 | 1.000 |
| historical | 0.36811 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.47554 | 0.250 |
| composition | 0.62242 | 1.000 |
| mastery | 0.28677 | 0.500 |
| content | 0.89370 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Jhin–Lee Sin (bot/jng) | 6/30 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Ashe | 25.365 | 17 | 0% | observed_candidate |
| Caitlyn | 22.639 | 8 | 100% | observed_candidate |
| Kai'Sa | 20.594 | 12 | 0% | observed_candidate |
| Lucian | 19.974 | 20 | 50% | observed_candidate |
| Xayah | 17.967 | 12 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt11: Gen.G — Rumble (top, F3)

Đồng đội đã lộ: {"jng": "Lee Sin", "bot": "Jhin"}. Địch đã lộ: {"sup": "Lulu", "bot": "Yunara"}.
Pool hợp lệ tại role:25ứngviên. Pick:28trận; score:31.775điểm, baseline:0.30943, geometriclift:1.03942.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.49169 | 1.000 |
| draft_order | 0.06238 | 1.000 |
| historical | 0.10212 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.48214 | 0.250 |
| composition | 0.53828 | 1.000 |
| mastery | 0.14364 | 0.500 |
| content | 0.91991 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Rumble–Lee Sin (top/jng) | 6/30 | observed_pair |
| Rumble–Jhin (top/bot) | 4/23 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Galio | 26.350 | 6 | 0% | observed_candidate |
| K'Sante | 25.224 | 23 | 0% | observed_candidate |
| Camille | 23.903 | 12 | 0% | observed_candidate |
| Gnar | 21.844 | 16 | 0% | observed_candidate |
| Zaahen | 16.744 | 5 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt12: T1 — Akali (mid, S3)

Đồng đội đã lộ: {"sup": "Lulu", "bot": "Yunara"}. Địch đã lộ: {"jng": "Lee Sin", "bot": "Jhin", "top": "Rumble"}.
Pool hợp lệ tại role:22ứngviên. Pick:15trận; score:30.256điểm, baseline:0.29625, geometriclift:1.03056.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.51016 | 1.000 |
| draft_order | 0.03654 | 1.000 |
| historical | 0.07048 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.55615 | 1.000 |
| mastery | 0.09129 | 0.500 |
| content | 0.81533 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Akali–Lulu (mid/sup) | 3/25 | sparse_pair |
| Akali–Yunara (mid/bot) | 2/21 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Viktor | 30.174 | 22 | 33% | observed_candidate |
| Galio | 24.253 | 10 | 0% | observed_candidate |
| Ryze | 19.554 | 11 | 0% | observed_candidate |
| Annie | 19.351 | 8 | 0% | observed_candidate |
| Taliyah | 17.765 | 10 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Viktor.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt17: T1 — Galio (top, S4)

Đồng đội đã lộ: {"sup": "Lulu", "bot": "Yunara", "mid": "Akali"}. Địch đã lộ: {"jng": "Lee Sin", "bot": "Jhin", "top": "Rumble"}.
Pool hợp lệ tại role:23ứngviên. Pick:6trận; score:24.564điểm, baseline:0.25085, geometriclift:0.97246.
Đối đầu: coverage32%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.35979 | 1.000 |
| draft_order | 0.00307 | 1.000 |
| historical | 0.43650 | 0.250 |
| matchup | 0.49639 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.60070 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.57882 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Galio–Lulu (top/sup) | 2/25 | sparse_pair |
| Galio–Yunara (top/bot) | 2/21 | sparse_pair |
| Galio–Akali (top/mid) | 0/15 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Gnar | 23.815 | 16 | 0% | observed_candidate |
| Camille | 22.881 | 12 | 0% | observed_candidate |
| Ornn | 19.613 | 9 | 32% | observed_candidate |
| K'Sante | 18.856 | 23 | 33% | observed_candidate |
| Jax | 18.376 | 8 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Gnar; bỏcomposition→K'Sante.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt18: Gen.G — Viktor (mid, F4)

Đồng đội đã lộ: {"jng": "Lee Sin", "bot": "Jhin", "top": "Rumble"}. Địch đã lộ: {"sup": "Lulu", "bot": "Yunara", "mid": "Akali", "top": "Galio"}.
Pool hợp lệ tại role:20ứngviên. Pick:22trận; score:25.256điểm, baseline:0.26630, geometriclift:0.93098.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.31270 | 1.000 |
| draft_order | 0.02888 | 1.000 |
| historical | 0.38735 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50303 | 0.250 |
| composition | 0.48784 | 1.000 |
| mastery | 0.10175 | 0.500 |
| content | 0.93631 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Viktor–Lee Sin (mid/jng) | 2/30 | sparse_pair |
| Viktor–Jhin (mid/bot) | 2/23 | sparse_pair |
| Viktor–Rumble (mid/top) | 5/28 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Anivia | 18.773 | 8 | 0% | observed_candidate |
| Ryze | 17.465 | 11 | 0% | observed_candidate |
| Taliyah | 16.854 | 10 | 0% | observed_candidate |
| Ahri | 16.290 | 10 | 0% | observed_candidate |
| Annie | 15.982 | 8 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt19: Gen.G — Leona (sup, F5)

Đồng đội đã lộ: {"jng": "Lee Sin", "bot": "Jhin", "top": "Rumble", "mid": "Viktor"}. Địch đã lộ: {"sup": "Lulu", "bot": "Yunara", "mid": "Akali", "top": "Galio"}.
Pool hợp lệ tại role:18ứngviên. Pick:9trận; score:24.029điểm, baseline:0.22993, geometriclift:1.05928.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.11768 | 1.000 |
| draft_order | 0.01394 | 1.000 |
| historical | 0.35420 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.60640 | 1.000 |
| mastery | 0.28454 | 0.500 |
| content | 0.90305 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Leona–Lee Sin (sup/jng) | 2/30 | sparse_pair |
| Leona–Jhin (sup/bot) | 3/23 | sparse_pair |
| Leona–Rumble (sup/top) | 2/28 | sparse_pair |
| Leona–Viktor (sup/mid) | 1/22 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rakan | 20.156 | 15 | 0% | observed_candidate |
| Karma | 18.838 | 17 | 25% | observed_candidate |
| Milio | 14.332 | 17 | 0% | observed_candidate |
| Rell | 11.601 | 6 | 0% | observed_candidate |
| Camille | 12.638 | 2 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván2 lượt20: T1 — Skarner (jng, S5)

Đồng đội đã lộ: {"sup": "Lulu", "bot": "Yunara", "mid": "Akali", "top": "Galio"}. Địch đã lộ: {"jng": "Lee Sin", "bot": "Jhin", "top": "Rumble", "mid": "Viktor", "sup": "Leona"}.
Pool hợp lệ tại role:10ứngviên. Pick:8trận; score:17.753điểm, baseline:0.18766, geometriclift:0.93436.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.16348 | 1.000 |
| draft_order | 0.01287 | 1.000 |
| historical | 0.21522 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.51137 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.70422 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Skarner–Lulu (jng/sup) | 2/25 | sparse_pair |
| Skarner–Yunara (jng/bot) | 2/21 | sparse_pair |
| Skarner–Akali (jng/mid) | 0/15 | unobserved_pair |
| Skarner–Galio (jng/top) | 0/6 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Sejuani | 16.339 | 6 | 0% | observed_candidate |
| Xin Zhao | 14.183 | 7 | 0% | observed_candidate |
| Maokai | 13.153 | 7 | 0% | observed_candidate |
| Naafiri | 12.838 | 9 | 0% | observed_candidate |
| Cho'Gath | 10.554 | 5 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Sejuani; bỏcomposition→Xin Zhao.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt7: T1 — Orianna (mid, F1)

Đồng đội đã lộ: {}. Địch đã lộ: {}.
Pool hợp lệ tại role:21ứngviên. Pick:25trận; score:27.813điểm, baseline:0.27813, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.50478 | 1.000 |
| draft_order | 0.04709 | 1.000 |
| historical | 0.44518 | 0.250 |
| mastery | 0.06317 | 0.500 |
| content | 0.97925 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Locke | 24.199 | 14 | 0% | observed_candidate |
| Taliyah | 14.842 | 10 | 0% | observed_candidate |
| Ahri | 13.942 | 10 | 0% | observed_candidate |
| Annie | 11.188 | 8 | 0% | observed_candidate |
| Anivia | 9.752 | 8 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt8: Gen.G — Locke (mid, S1)

Đồng đội đã lộ: {}. Địch đã lộ: {"mid": "Orianna"}.
Pool hợp lệ tại role:20ứngviên. Pick:14trận; score:26.523điểm, baseline:0.26523, geometriclift:1.00000.
Đối đầu: coverage100%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.49204 | 1.000 |
| draft_order | 0.00874 | 1.000 |
| historical | 0.26799 | 0.250 |
| matchup | 0.50000 | 0.500 |
| mastery | 0.00000 | 0.500 |
| content | 0.70762 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Taliyah | 22.023 | 10 | 0% | observed_candidate |
| Ahri | 19.541 | 10 | 0% | observed_candidate |
| Anivia | 16.151 | 8 | 0% | observed_candidate |
| Annie | 15.620 | 8 | 0% | observed_candidate |
| Ryze | 15.485 | 11 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Taliyah.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt9: Gen.G — K'Sante (top, S2)

Đồng đội đã lộ: {"mid": "Locke"}. Địch đã lộ: {"mid": "Orianna"}.
Pool hợp lệ tại role:23ứngviên. Pick:23trận; score:26.618điểm, baseline:0.26341, geometriclift:1.01435.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.41057 | 1.000 |
| draft_order | 0.01417 | 1.000 |
| historical | 0.25635 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.53286 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.84431 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| K'Sante–Locke (top/mid) | 2/14 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Gnar | 23.460 | 16 | 0% | observed_candidate |
| Camille | 20.100 | 12 | 0% | observed_candidate |
| Jax | 19.474 | 8 | 0% | observed_candidate |
| Renekton | 18.038 | 12 | 0% | observed_candidate |
| Ornn | 14.424 | 9 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Gnar.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt10: T1 — Gnar (top, F2)

Đồng đội đã lộ: {"mid": "Orianna"}. Địch đã lộ: {"mid": "Locke", "top": "K'Sante"}.
Pool hợp lệ tại role:22ứngviên. Pick:16trận; score:27.663điểm, baseline:0.23440, geometriclift:1.24905.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.22467 | 1.000 |
| draft_order | 0.01019 | 1.000 |
| historical | 0.44404 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.60417 | 0.250 |
| composition | 0.69181 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.96937 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Gnar–Orianna (top/mid) | 5/25 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Renekton | 23.900 | 12 | 0% | observed_candidate |
| Jax | 20.298 | 8 | 0% | observed_candidate |
| Camille | 20.275 | 12 | 0% | observed_candidate |
| Ornn | 18.071 | 9 | 0% | observed_candidate |
| Zaahen | 9.220 | 5 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt11: T1 — Wukong (jng, F3)

Đồng đội đã lộ: {"mid": "Orianna", "top": "Gnar"}. Địch đã lộ: {"mid": "Locke", "top": "K'Sante"}.
Pool hợp lệ tại role:11ứngviên. Pick:15trận; score:23.280điểm, baseline:0.26149, geometriclift:0.85698.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.36418 | 1.000 |
| draft_order | 0.01060 | 1.000 |
| historical | 0.19824 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.43615 | 1.000 |
| mastery | 0.09129 | 0.500 |
| content | 0.96380 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Wukong–Orianna (jng/mid) | 1/25 | sparse_pair |
| Wukong–Gnar (jng/top) | 1/16 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Xin Zhao | 20.906 | 7 | 0% | observed_candidate |
| Trundle | 19.577 | 12 | 0% | observed_candidate |
| Naafiri | 19.003 | 9 | 0% | observed_candidate |
| Maokai | 11.847 | 7 | 0% | observed_candidate |
| Cho'Gath | 11.635 | 5 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Xin Zhao.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt12: Gen.G — Alistar (sup, S3)

Đồng đội đã lộ: {"mid": "Locke", "top": "K'Sante"}. Địch đã lộ: {"mid": "Orianna", "top": "Gnar", "jng": "Wukong"}.
Pool hợp lệ tại role:18ứngviên. Pick:26trận; score:26.384điểm, baseline:0.25523, geometriclift:1.04582.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.31698 | 1.000 |
| draft_order | 0.06727 | 1.000 |
| historical | 0.19412 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.55896 | 1.000 |
| mastery | 0.07293 | 0.500 |
| content | 0.74590 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Alistar–Locke (sup/mid) | 2/14 | sparse_pair |
| Alistar–K'Sante (sup/top) | 4/23 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Karma | 21.993 | 17 | 33% | observed_candidate |
| Rakan | 19.286 | 15 | 0% | observed_candidate |
| Milio | 18.346 | 17 | 0% | observed_candidate |
| Rell | 10.736 | 6 | 0% | observed_candidate |
| Camille | 15.061 | 2 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt17: Gen.G — Corki (bot, S4)

Đồng đội đã lộ: {"mid": "Locke", "top": "K'Sante", "sup": "Alistar"}. Địch đã lộ: {"mid": "Orianna", "top": "Gnar", "jng": "Wukong"}.
Pool hợp lệ tại role:16ứngviên. Pick:9trận; score:19.709điểm, baseline:0.19016, geometriclift:1.04540.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.12996 | 1.000 |
| draft_order | 0.00625 | 1.000 |
| historical | 0.26665 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.60259 | 1.000 |
| mastery | 0.06793 | 0.500 |
| content | 0.72727 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Corki–Locke (bot/mid) | 0/14 | unobserved_pair |
| Corki–K'Sante (bot/top) | 2/23 | sparse_pair |
| Corki–Alistar (bot/sup) | 4/26 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Kai'Sa | 19.443 | 12 | 0% | observed_candidate |
| Lucian | 18.877 | 20 | 0% | observed_candidate |
| Caitlyn | 15.703 | 8 | 0% | observed_candidate |
| Xayah | 14.792 | 12 | 0% | observed_candidate |
| Sivir | 14.247 | 6 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏcomposition→Lucian; bỏmastery→Kai'Sa; bỏmatchup→Lucian.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):3. Không là đo tác động nhân quả.

### Ván3 lượt18: T1 — Lucian (bot, F4)

Đồng đội đã lộ: {"mid": "Orianna", "top": "Gnar", "jng": "Wukong"}. Địch đã lộ: {"mid": "Locke", "top": "K'Sante", "sup": "Alistar", "bot": "Corki"}.
Pool hợp lệ tại role:15ứngviên. Pick:20trận; score:21.835điểm, baseline:0.23633, geometriclift:0.90267.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.26812 | 1.000 |
| draft_order | 0.02046 | 1.000 |
| historical | 0.21881 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.46407 | 1.000 |
| mastery | 0.09129 | 0.500 |
| content | 0.86866 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Lucian–Orianna (bot/mid) | 3/25 | sparse_pair |
| Lucian–Gnar (bot/top) | 0/16 | unobserved_pair |
| Lucian–Wukong (bot/jng) | 2/15 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Kai'Sa | 19.750 | 12 | 0% | observed_candidate |
| Xayah | 19.174 | 12 | 0% | observed_candidate |
| Caitlyn | 17.539 | 8 | 0% | observed_candidate |
| Tristana | 16.043 | 7 | 0% | observed_candidate |
| Sivir | 12.469 | 6 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmeta→Xayah.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt19: T1 — Milio (sup, F5)

Đồng đội đã lộ: {"mid": "Orianna", "top": "Gnar", "jng": "Wukong", "bot": "Lucian"}. Địch đã lộ: {"mid": "Locke", "top": "K'Sante", "sup": "Alistar", "bot": "Corki"}.
Pool hợp lệ tại role:15ứngviên. Pick:17trận; score:21.235điểm, baseline:0.19353, geometriclift:1.12351.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.16112 | 1.000 |
| draft_order | 0.01861 | 1.000 |
| historical | 0.17310 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.55096 | 1.000 |
| mastery | 0.09129 | 0.500 |
| content | 0.53041 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Milio–Orianna (sup/mid) | 2/25 | sparse_pair |
| Milio–Gnar (sup/top) | 0/16 | unobserved_pair |
| Milio–Wukong (sup/jng) | 2/15 | sparse_pair |
| Milio–Lucian (sup/bot) | 17/20 | observed_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rell | 12.380 | 6 | 0% | observed_candidate |
| Nami | 13.804 | 4 | 0% | sparse_candidate |
| Camille | 12.786 | 2 | 0% | sparse_candidate |
| Poppy | 11.206 | 2 | 0% | sparse_candidate |
| Shen | 10.595 | 3 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván3 lượt20: Gen.G — Xin Zhao (jng, S5)

Đồng đội đã lộ: {"mid": "Locke", "top": "K'Sante", "sup": "Alistar", "bot": "Corki"}. Địch đã lộ: {"mid": "Orianna", "top": "Gnar", "jng": "Wukong", "bot": "Lucian", "sup": "Milio"}.
Pool hợp lệ tại role:8ứngviên. Pick:7trận; score:16.919điểm, baseline:0.19710, geometriclift:0.82955.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.15368 | 1.000 |
| draft_order | 0.00501 | 1.000 |
| historical | 0.35893 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.47116 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.86128 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Xin Zhao–Locke (jng/mid) | 1/14 | sparse_pair |
| Xin Zhao–K'Sante (jng/top) | 2/23 | sparse_pair |
| Xin Zhao–Alistar (jng/sup) | 0/26 | unobserved_pair |
| Xin Zhao–Corki (jng/bot) | 0/9 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Maokai | 12.926 | 7 | 0% | observed_candidate |
| Cho'Gath | 9.822 | 5 | 0% | observed_candidate |
| Sejuani | 9.086 | 6 | 0% | observed_candidate |
| Aatrox | 8.563 | 1 | 0% | sparse_candidate |
| Lillia | 8.498 | 1 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt7: Gen.G — Seraphine (sup, F1)

Đồng đội đã lộ: {}. Địch đã lộ: {}.
Pool hợp lệ tại role:16ứngviên. Pick:20trận; score:26.516điểm, baseline:0.26516, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.39372 | 1.000 |
| draft_order | 0.02658 | 1.000 |
| historical | 0.43285 | 0.250 |
| mastery | 0.28713 | 0.500 |
| content | 0.83622 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rakan | 12.760 | 15 | 0% | observed_candidate |
| Rell | 6.309 | 6 | 0% | observed_candidate |
| Camille | 10.046 | 2 | 0% | sparse_candidate |
| Poppy | 5.858 | 2 | 0% | sparse_candidate |
| Shen | 4.797 | 3 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt8: T1 — Ashe (bot, S1)

Đồng đội đã lộ: {}. Địch đã lộ: {"sup": "Seraphine"}.
Pool hợp lệ tại role:15ứngviên. Pick:17trận; score:21.807điểm, baseline:0.21807, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.19379 | 1.000 |
| draft_order | 0.08750 | 1.000 |
| historical | 0.41300 | 0.250 |
| matchup | 0.50000 | 0.500 |
| mastery | 0.00000 | 0.500 |
| content | 0.96009 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Xayah | 20.125 | 12 | 0% | observed_candidate |
| Kai'Sa | 19.699 | 12 | 0% | observed_candidate |
| Caitlyn | 19.024 | 8 | 0% | observed_candidate |
| Sivir | 16.036 | 6 | 0% | observed_candidate |
| Miss Fortune | 14.621 | 6 | 0% | observed_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt9: T1 — Renekton (top, S2)

Đồng đội đã lộ: {"bot": "Ashe"}. Địch đã lộ: {"sup": "Seraphine"}.
Pool hợp lệ tại role:20ứngviên. Pick:12trận; score:24.839điểm, baseline:0.22540, geometriclift:1.13566.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.25223 | 1.000 |
| draft_order | 0.00711 | 1.000 |
| historical | 0.39062 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.68616 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.79451 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Renekton–Ashe (top/bot) | 3/17 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Camille | 19.260 | 12 | 0% | observed_candidate |
| Jax | 13.645 | 8 | 0% | observed_candidate |
| Ornn | 13.088 | 9 | 0% | observed_candidate |
| Zaahen | 11.134 | 5 | 0% | observed_candidate |
| Gwen | 16.786 | 2 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏcomposition→Camille.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt10: Gen.G — Ahri (mid, F2)

Đồng đội đã lộ: {"sup": "Seraphine"}. Địch đã lộ: {"bot": "Ashe", "top": "Renekton"}.
Pool hợp lệ tại role:17ứngviên. Pick:10trận; score:23.368điểm, baseline:0.21723, geometriclift:1.09881.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.15466 | 1.000 |
| draft_order | 0.00862 | 1.000 |
| historical | 0.39678 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.66353 | 1.000 |
| mastery | 0.11235 | 0.500 |
| content | 0.88384 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Ahri–Seraphine (mid/sup) | 3/20 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Anivia | 18.983 | 8 | 0% | observed_candidate |
| Taliyah | 16.766 | 10 | 0% | observed_candidate |
| LeBlanc | 16.152 | 5 | 0% | observed_candidate |
| Annie | 12.308 | 8 | 0% | observed_candidate |
| Ryze | 12.164 | 11 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏcomposition→Taliyah.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt11: Gen.G — Camille (top, F3)

Đồng đội đã lộ: {"sup": "Seraphine", "mid": "Ahri"}. Địch đã lộ: {"bot": "Ashe", "top": "Renekton"}.
Pool hợp lệ tại role:19ứngviên. Pick:12trận; score:20.318điểm, baseline:0.24809, geometriclift:0.77282.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.25518 | 1.000 |
| draft_order | 0.00815 | 1.000 |
| historical | 0.25378 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.37149 | 1.000 |
| mastery | 0.18559 | 0.500 |
| content | 0.98567 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Camille–Seraphine (top/sup) | 1/20 | sparse_pair |
| Camille–Ahri (top/mid) | 0/10 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Ornn | 17.341 | 9 | 0% | observed_candidate |
| Jax | 15.667 | 8 | 0% | observed_candidate |
| Zaahen | 11.823 | 5 | 0% | observed_candidate |
| Gwen | 17.619 | 2 | 0% | sparse_candidate |
| Sion | 13.010 | 2 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏmeta→Ornn.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt12: T1 — Rakan (sup, S3)

Đồng đội đã lộ: {"bot": "Ashe", "top": "Renekton"}. Địch đã lộ: {"sup": "Seraphine", "mid": "Ahri", "top": "Camille"}.
Pool hợp lệ tại role:14ứngviên. Pick:15trận; score:18.215điểm, baseline:0.21203, geometriclift:0.82773.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.16824 | 1.000 |
| draft_order | 0.00925 | 1.000 |
| historical | 0.15176 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.46024 | 1.000 |
| mastery | 0.14976 | 0.500 |
| content | 0.97980 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Rakan–Ashe (sup/bot) | 0/17 | unobserved_pair |
| Rakan–Renekton (sup/top) | 2/12 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rell | 11.625 | 6 | 0% | observed_candidate |
| Poppy | 12.440 | 2 | 0% | sparse_candidate |
| Neeko | 10.816 | 3 | 0% | sparse_candidate |
| Shen | 10.772 | 3 | 0% | sparse_candidate |
| Yuumi | 10.613 | 4 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt17: T1 — Anivia (mid, S4)

Đồng đội đã lộ: {"bot": "Ashe", "top": "Renekton", "sup": "Rakan"}. Địch đã lộ: {"sup": "Seraphine", "mid": "Ahri", "top": "Camille"}.
Pool hợp lệ tại role:15ứngviên. Pick:8trận; score:16.871điểm, baseline:0.19183, geometriclift:0.85504.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.13836 | 1.000 |
| draft_order | 0.04314 | 1.000 |
| historical | 0.07148 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.44803 | 1.000 |
| mastery | 0.05552 | 0.500 |
| content | 0.88450 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Anivia–Ashe (mid/bot) | 1/17 | sparse_pair |
| Anivia–Renekton (mid/top) | 0/12 | unobserved_pair |
| Anivia–Rakan (mid/sup) | 0/15 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Annie | 15.880 | 8 | 0% | observed_candidate |
| Ryze | 15.238 | 11 | 0% | observed_candidate |
| LeBlanc | 14.590 | 5 | 0% | observed_candidate |
| Sylas | 14.175 | 7 | 0% | observed_candidate |
| Aurora | 12.550 | 5 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏcomposition→Annie.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt18: Gen.G — Miss Fortune (bot, F4)

Đồng đội đã lộ: {"sup": "Seraphine", "mid": "Ahri", "top": "Camille"}. Địch đã lộ: {"bot": "Ashe", "top": "Renekton", "sup": "Rakan", "mid": "Anivia"}.
Pool hợp lệ tại role:12ứngviên. Pick:6trận; score:15.785điểm, baseline:0.16080, geometriclift:0.97825.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.05428 | 1.000 |
| draft_order | 0.01987 | 1.000 |
| historical | 0.18762 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.55665 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.82819 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Miss Fortune–Seraphine (bot/sup) | 1/20 | sparse_pair |
| Miss Fortune–Ahri (bot/mid) | 0/10 | unobserved_pair |
| Miss Fortune–Camille (bot/top) | 1/12 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Caitlyn | 15.340 | 8 | 0% | observed_candidate |
| Sivir | 14.152 | 6 | 0% | observed_candidate |
| Tristana | 12.370 | 7 | 0% | observed_candidate |
| Ziggs | 10.774 | 5 | 0% | observed_candidate |
| Zeri | 11.886 | 4 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏcontent→Caitlyn; bỏcomposition→Caitlyn; bỏmatchup→Caitlyn.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):2. Không là đo tác động nhân quả.

### Ván4 lượt19: Gen.G — Maokai (jng, F5)

Đồng đội đã lộ: {"sup": "Seraphine", "mid": "Ahri", "top": "Camille", "bot": "Miss Fortune"}. Địch đã lộ: {"bot": "Ashe", "top": "Renekton", "sup": "Rakan", "mid": "Anivia"}.
Pool hợp lệ tại role:7ứngviên. Pick:7trận; score:15.181điểm, baseline:0.16665, geometriclift:0.89500.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.13140 | 1.000 |
| draft_order | 0.01272 | 1.000 |
| historical | 0.02568 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.43498 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.74414 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Maokai–Seraphine (jng/sup) | 1/20 | sparse_pair |
| Maokai–Ahri (jng/mid) | 0/10 | unobserved_pair |
| Maokai–Camille (jng/top) | 1/12 | sparse_pair |
| Maokai–Miss Fortune (jng/bot) | 0/6 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Sejuani | 11.548 | 6 | 0% | observed_candidate |
| Cho'Gath | 11.478 | 5 | 0% | observed_candidate |
| Aatrox | 9.314 | 1 | 0% | sparse_candidate |
| Malphite | 8.268 | 1 | 0% | sparse_candidate |
| Nasus | 8.263 | 1 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván4 lượt20: T1 — Sejuani (jng, S5)

Đồng đội đã lộ: {"bot": "Ashe", "top": "Renekton", "sup": "Rakan", "mid": "Anivia"}. Địch đã lộ: {"sup": "Seraphine", "mid": "Ahri", "top": "Camille", "bot": "Miss Fortune", "jng": "Maokai"}.
Pool hợp lệ tại role:6ứngviên. Pick:6trận; score:11.891điểm, baseline:0.15192, geometriclift:0.75338.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.05832 | 1.000 |
| draft_order | 0.00981 | 1.000 |
| historical | 0.03005 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.35264 | 1.000 |
| mastery | 0.08535 | 0.500 |
| content | 0.53607 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Sejuani–Ashe (jng/bot) | 0/17 | unobserved_pair |
| Sejuani–Renekton (jng/top) | 0/12 | unobserved_pair |
| Sejuani–Rakan (jng/sup) | 0/15 | unobserved_pair |
| Sejuani–Anivia (jng/mid) | 0/8 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Cho'Gath | 11.056 | 5 | 0% | observed_candidate |
| Nasus | 9.090 | 1 | 0% | sparse_candidate |
| Aatrox | 9.054 | 1 | 0% | sparse_candidate |
| Lillia | 8.348 | 1 | 0% | sparse_candidate |
| Malphite | 8.232 | 1 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏmastery→Cho'Gath.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt7: T1 — Trundle (jng, F1)

Đồng đội đã lộ: {}. Địch đã lộ: {}.
Pool hợp lệ tại role:6ứngviên. Pick:12trận; score:16.064điểm, baseline:0.16064, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.21791 | 1.000 |
| draft_order | 0.00969 | 1.000 |
| historical | 0.39062 | 0.250 |
| mastery | 0.08526 | 0.500 |
| content | 0.89943 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Cho'Gath | 3.620 | 5 | 0% | observed_candidate |
| Aatrox | 1.369 | 1 | 0% | sparse_candidate |
| Malphite | 0.282 | 1 | 0% | sparse_candidate |
| Nasus | 0.273 | 1 | 0% | sparse_candidate |
| Lillia | 0.257 | 1 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt8: Gen.G — Xayah (bot, S1)

Đồng đội đã lộ: {}. Địch đã lộ: {"jng": "Trundle"}.
Pool hợp lệ tại role:13ứngviên. Pick:12trận; score:19.341điểm, baseline:0.19341, geometriclift:1.00000.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.14420 | 1.000 |
| draft_order | 0.04118 | 1.000 |
| historical | 0.25378 | 0.250 |
| matchup | 0.50000 | 0.500 |
| mastery | 0.10186 | 0.500 |
| content | 0.98149 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Chưa có đồng đội đã chọn | — | Không chấm phối hợp |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Kai'Sa | 18.257 | 12 | 0% | observed_candidate |
| Caitlyn | 17.845 | 8 | 0% | observed_candidate |
| Sivir | 14.791 | 6 | 0% | observed_candidate |
| Tristana | 13.885 | 7 | 0% | observed_candidate |
| Ziggs | 11.680 | 5 | 0% | observed_candidate |

Kiểm tra độ nhạy: bỏmastery→Kai'Sa.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt9: Gen.G — Ornn (top, S2)

Đồng đội đã lộ: {"bot": "Xayah"}. Địch đã lộ: {"jng": "Trundle"}.
Pool hợp lệ tại role:18ứngviên. Pick:9trận; score:18.448điểm, baseline:0.18396, geometriclift:1.00352.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.10547 | 1.000 |
| draft_order | 0.00636 | 1.000 |
| historical | 0.35420 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.52028 | 1.000 |
| mastery | 0.06793 | 0.500 |
| content | 0.52893 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Ornn–Xayah (top/bot) | 1/12 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Jax | 15.430 | 8 | 0% | observed_candidate |
| Zaahen | 12.725 | 5 | 0% | observed_candidate |
| Aurora | 18.479 | 2 | 0% | sparse_candidate |
| Kled | 15.635 | 4 | 0% | sparse_candidate |
| Kennen | 13.257 | 3 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏcomposition→Jax.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt10: T1 — Kai'Sa (bot, F2)

Đồng đội đã lộ: {"jng": "Trundle"}. Địch đã lộ: {"bot": "Xayah", "top": "Ornn"}.
Pool hợp lệ tại role:12ứngviên. Pick:12trận; score:23.456điểm, baseline:0.22135, geometriclift:1.07792.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.20085 | 1.000 |
| draft_order | 0.02034 | 1.000 |
| historical | 0.25378 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.64948 | 1.000 |
| mastery | 0.08526 | 0.500 |
| content | 0.94601 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Kai'Sa–Trundle (bot/jng) | 2/12 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Caitlyn | 22.845 | 8 | 0% | observed_candidate |
| Sivir | 15.103 | 6 | 0% | observed_candidate |
| Ziggs | 14.825 | 5 | 0% | observed_candidate |
| Tristana | 13.405 | 7 | 0% | observed_candidate |
| Zeri | 13.377 | 4 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏcomposition→Caitlyn.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt11: T1 — Karma (sup, F3)

Đồng đội đã lộ: {"jng": "Trundle", "bot": "Kai'Sa"}. Địch đã lộ: {"bot": "Xayah", "top": "Ornn"}.
Pool hợp lệ tại role:14ứngviên. Pick:17trận; score:21.557điểm, baseline:0.24073, geometriclift:0.86675.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.20846 | 1.000 |
| draft_order | 0.06074 | 1.000 |
| historical | 0.21611 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.42792 | 1.000 |
| mastery | 0.15434 | 0.500 |
| content | 0.91229 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Karma–Trundle (sup/jng) | 1/12 | sparse_pair |
| Karma–Kai'Sa (sup/bot) | 0/12 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Rell | 15.842 | 6 | 0% | observed_candidate |
| Poppy | 13.164 | 2 | 0% | sparse_candidate |
| Yuumi | 12.018 | 4 | 0% | sparse_candidate |
| Lux | 11.589 | 1 | 0% | sparse_candidate |
| Shen | 11.557 | 3 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt12: Gen.G — Annie (mid, S3)

Đồng đội đã lộ: {"bot": "Xayah", "top": "Ornn"}. Địch đã lộ: {"jng": "Trundle", "bot": "Kai'Sa", "sup": "Karma"}.
Pool hợp lệ tại role:14ứngviên. Pick:8trận; score:16.452điểm, baseline:0.18007, geometriclift:0.89662.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.12396 | 1.000 |
| draft_order | 0.00458 | 1.000 |
| historical | 0.30574 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.50817 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.68273 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Annie–Xayah (mid/bot) | 0/12 | unobserved_pair |
| Annie–Ornn (mid/top) | 1/9 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Ryze | 15.294 | 11 | 0% | observed_candidate |
| Aurora | 15.261 | 5 | 0% | observed_candidate |
| Sylas | 14.448 | 7 | 0% | observed_candidate |
| LeBlanc | 13.205 | 5 | 0% | observed_candidate |
| Twisted Fate | 13.597 | 4 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏcomposition→Ryze.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt17: Gen.G — Poppy (sup, S4)

Đồng đội đã lộ: {"bot": "Xayah", "top": "Ornn", "mid": "Annie"}. Địch đã lộ: {"jng": "Trundle", "bot": "Kai'Sa", "sup": "Karma"}.
Pool hợp lệ tại role:12ứngviên. Pick:2trận; score:13.093điểm, baseline:0.15484, geometriclift:0.82228.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.07977 | 1.000 |
| draft_order | 0.00159 | 1.000 |
| historical | 0.34238 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.37917 | 1.000 |
| mastery | 0.00000 | 0.500 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Poppy–Xayah (sup/bot) | 0/12 | unobserved_pair |
| Poppy–Ornn (sup/top) | 0/9 | unobserved_pair |
| Poppy–Annie (sup/mid) | 0/8 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Nami | 12.913 | 4 | 0% | sparse_candidate |
| Yuumi | 12.674 | 4 | 0% | sparse_candidate |
| Shen | 12.491 | 3 | 0% | sparse_candidate |
| Bard | 11.833 | 3 | 0% | sparse_candidate |
| Neeko | 11.322 | 3 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏmeta→Nami.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt18: T1 — Ryze (mid, F4)

Đồng đội đã lộ: {"jng": "Trundle", "bot": "Kai'Sa", "sup": "Karma"}. Địch đã lộ: {"bot": "Xayah", "top": "Ornn", "mid": "Annie", "sup": "Poppy"}.
Pool hợp lệ tại role:13ứngviên. Pick:11trận; score:18.222điểm, baseline:0.18345, geometriclift:0.99182.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.13844 | 1.000 |
| draft_order | 0.02701 | 1.000 |
| historical | 0.09746 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.57359 | 1.000 |
| mastery | 0.00000 | 0.500 |
| content | 0.95613 | 0.100 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Ryze–Trundle (mid/jng) | 0/12 | unobserved_pair |
| Ryze–Kai'Sa (mid/bot) | 3/12 | sparse_pair |
| Ryze–Karma (mid/sup) | 2/17 | sparse_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| LeBlanc | 16.309 | 5 | 0% | observed_candidate |
| Sylas | 16.038 | 7 | 0% | observed_candidate |
| Aurora | 14.594 | 5 | 0% | observed_candidate |
| Twisted Fate | 11.319 | 4 | 0% | sparse_candidate |
| Yone | 10.572 | 4 | 0% | sparse_candidate |

Kiểm tra độ nhạy: Không đổi top1 với các ablation đã thử.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt19: T1 — Aurora (top, F5)

Đồng đội đã lộ: {"jng": "Trundle", "bot": "Kai'Sa", "sup": "Karma", "mid": "Ryze"}. Địch đã lộ: {"bot": "Xayah", "top": "Ornn", "mid": "Annie", "sup": "Poppy"}.
Pool hợp lệ tại role:15ứngviên. Pick:2trận; score:14.216điểm, baseline:0.16404, geometriclift:0.84450.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.08905 | 1.000 |
| draft_order | 0.02451 | 1.000 |
| historical | 0.34238 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.47263 | 1.000 |
| mastery | 0.00000 | 0.500 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Aurora–Trundle (top/jng) | 0/12 | unobserved_pair |
| Aurora–Kai'Sa (top/bot) | 1/12 | sparse_pair |
| Aurora–Karma (top/sup) | 0/17 | unobserved_pair |
| Aurora–Ryze (top/mid) | 0/11 | unobserved_pair |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Gwen | 13.837 | 2 | 0% | sparse_candidate |
| Vayne | 12.358 | 2 | 0% | sparse_candidate |
| Kennen | 12.177 | 3 | 0% | sparse_candidate |
| Shen | 11.801 | 4 | 0% | sparse_candidate |
| Tristana | 11.613 | 1 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏmeta→Gwen.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):1. Không là đo tác động nhân quả.

### Ván5 lượt20: Gen.G — Nasus (jng, S5)

Đồng đội đã lộ: {"bot": "Xayah", "top": "Ornn", "mid": "Annie", "sup": "Poppy"}. Địch đã lộ: {"jng": "Trundle", "bot": "Kai'Sa", "sup": "Karma", "mid": "Ryze", "top": "Aurora"}.
Pool hợp lệ tại role:4ứngviên. Pick:1trận; score:10.365điểm, baseline:0.10937, geometriclift:0.94163.
Đối đầu: coverage0%, mechanical_counter_status=not_evaluated. Chưa có evaluatorcơchế.

| Thành phần | Giá trị | Trọng số |
|---|---:|---:|
| meta | 0.00731 | 1.000 |
| draft_order | 0.00048 | 1.000 |
| historical | 0.00000 | 0.250 |
| matchup | 0.50000 | 0.500 |
| synergy | 0.50000 | 0.250 |
| composition | 0.58351 | 1.000 |
| mastery | 0.00000 | 0.500 |

Composition điều chỉnh odds điểm nền bằng geometriclift, không cộng tuyến tính như các thành phần nền. Giá trị composition trong bảng là tóm tắtassociation, không thay cho hệ sốlift.

| Cặp với đồng đội | Mẫu cặp / mẫu đồng đội | Trạng thái |
|---|---:|---|
| Nasus–Xayah (jng/bot) | 1/12 | sparse_pair |
| Nasus–Ornn (jng/top) | 0/9 | unobserved_pair |
| Nasus–Annie (jng/mid) | 0/8 | unobserved_pair |
| Nasus–Poppy (jng/sup) | 0/2 | insufficient_anchor_history |

| Phương án khác | Điểm | n | Coverage địch | Nhãn mẫu |
|---|---:|---:|---:|---|
| Aatrox | 10.087 | 1 | 0% | sparse_candidate |
| Lillia | 9.306 | 1 | 0% | sparse_candidate |
| Malphite | 9.178 | 1 | 0% | sparse_candidate |

Kiểm tra độ nhạy: bỏcomposition→Aatrox; bỏmatchup→Aatrox.
Rank pick cũ khi che ngữ cảnh địch (giữ pool loại trừ):2. Không là đo tác động nhân quả.


## Nguồn và tái lập

Audit JSON: `D:\Chivinh\2026_MonHoc\Nhập môn khoa học dữ liệu\Project\reports\contextual_pick_audit.json`; sourceSHA256:`aab391f1e0705470cf5c3cbeea5eb14c520b3a72c1d703620984030efb86d70b`. File summary.json cùng thư mục lưu tổng hợp/checks; top_candidates/alternatives vàdiagnostic_ablations nằm trong auditJSON.

```powershell
.\.venv\Scripts\python.exe src/07_recommender/audit_draft_choices.py --session reports/legacy_contextual_comparison/contextual/series.json --output reports/contextual_pick_audit
.\.venv\Scripts\python.exe src/07_recommender/review_contextual_picks.py
```
