# Chạy thử BO5 T1–Gen.G — 24/11/2026

Đã yêu cầu5draft Fearless trên Worlds, cutoff13/11/2026, patch dataset16.20. Đây là draft giả lập; không có kết quả thắng/thua. T1 ởBlue, Gen.G ởRed, first-pick luân phiênBlue/Red. Không dùng opponent-model hoặc statistical-auto override.

Kết quả: hoàn thành ván1, ván2 dừng trước lượt20 để xem lại chiến thuật; ván3–5 chưa chạy. Không được mô tả thành đã hoàn thànhBO5.

Snapshot: {"region": "WLDS", "dataset_patch": "16.20", "data_through": "2026-11-09T00:56:00+00:00", "requested_as_of": "2026-11-13T23:59:59.999999999+00:00", "staleness_days": 4, "history_games": 106, "patch_games": 94, "lookback_days": 60, "half_life_days": 21.0, "claim": "historical_snapshot_not_live_meta"}.

## Ván1 — hoàn thành

Bên chọn trước: T1. Fearless khóa0tướng.

| Đội | Cấm pha1 | Cấm pha2 |
|---|---|---|
| T1 | Nocturne, Renata Glasc, Olaf | Lulu, Seraphine |
| Gen.G | Vi, Cassiopeia, Qiyana | Orianna, Locke |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Jayce | Rumble |
| jng | Lee Sin | Jarvan IV |
| mid | Galio | Syndra |
| bot | Ezreal | Jhin |
| sup | Nautilus | Alistar |

| Lượt | Đội | Hành động | Tướng | Role |
|---:|---|---|---|---|
| 1 | T1 | ban | Nocturne | — |
| 2 | Gen.G | ban | Vi | — |
| 3 | T1 | ban | Renata Glasc | — |
| 4 | Gen.G | ban | Cassiopeia | — |
| 5 | T1 | ban | Olaf | — |
| 6 | Gen.G | ban | Qiyana | — |
| 7 | T1 | pick | Lee Sin | jng |
| 8 | Gen.G | pick | Syndra | mid |
| 9 | Gen.G | pick | Rumble | top |
| 10 | T1 | pick | Ezreal | bot |
| 11 | T1 | pick | Nautilus | sup |
| 12 | Gen.G | pick | Jarvan IV | jng |
| 13 | Gen.G | ban | Orianna | — |
| 14 | T1 | ban | Lulu | — |
| 15 | Gen.G | ban | Locke | — |
| 16 | T1 | ban | Seraphine | — |
| 17 | Gen.G | pick | Jhin | bot |
| 18 | T1 | pick | Jayce | top |
| 19 | T1 | pick | Galio | mid |
| 20 | Gen.G | pick | Alistar | sup |

## Ván2 — chờ xem lại chiến thuật

Bên chọn trước: Gen.G. Fearless khóa10tướng.

| Đội | Cấm pha1 | Cấm pha2 |
|---|---|---|
| T1 | Renata Glasc, Cassiopeia, Qiyana | Wukong, Pantheon |
| Gen.G | Nocturne, Vi, Olaf | K'Sante, Ambessa |

| Vị trí | T1 | Gen.G |
|---|---|---|
| top | Chưa chốt | Gnar |
| jng | Trundle | Xin Zhao |
| mid | Locke | Orianna |
| bot | Yunara | Ashe |
| sup | Lulu | Seraphine |

| Lượt | Đội | Hành động | Tướng | Role |
|---:|---|---|---|---|
| 1 | Gen.G | ban | Nocturne | — |
| 2 | T1 | ban | Renata Glasc | — |
| 3 | Gen.G | ban | Vi | — |
| 4 | T1 | ban | Cassiopeia | — |
| 5 | Gen.G | ban | Olaf | — |
| 6 | T1 | ban | Qiyana | — |
| 7 | Gen.G | pick | Orianna | mid |
| 8 | T1 | pick | Locke | mid |
| 9 | T1 | pick | Lulu | sup |
| 10 | Gen.G | pick | Gnar | top |
| 11 | Gen.G | pick | Seraphine | sup |
| 12 | T1 | pick | Yunara | bot |
| 13 | T1 | ban | Wukong | — |
| 14 | Gen.G | ban | K'Sante | — |
| 15 | T1 | ban | Pantheon | — |
| 16 | Gen.G | ban | Ambessa | — |
| 17 | T1 | pick | Trundle | jng |
| 18 | Gen.G | pick | Ashe | bot |
| 19 | Gen.G | pick | Xin Zhao | jng |

Lượt20 chưa áp dụng: ứng viênCamille top; không có đối đầu đủ mẫu. Phương án thống kê khác: Renekton, Jax, Ornn. Chưa xác nhận phương án nào mạnh hơn về cơ chế.

## Giới hạn bộc lộ qua lần chạy

Trundle vẫn được T1 chọn ở ván2lượt17, coverage đối đầu=0%. Lúc đó địch chưa đủ5tướng, nên gate hiện hành không chặn. Không có chứng minhTrundle làcounter; điều này cho thấy task trước mới xử lý việc tự chốt thiếu căn cứ khi địch đủ5, chưa giải quyết toàn bộchất lượng chọn tướng/counter trongdraft chưa hoàn tất.

Lượt này chỉ chạy/kiểm tra và ghi báo cáo, không sửa thuật toán, không tự nhập lựa chọn để vượtgate, không fitmodel hoặc chạy suiteML lại. Không có tỉ sốBO5.

Lệnh tái lập:

```powershell
.\.venv\Scripts\python.exe src/07_recommender/simulate_fearless_series.py --blue-team T1 --red-team Gen.G --region WLDS --as-of 2026-11-13 --patch 16.20 --games 5 --output-dir reports/t1_geng_bo5_20261124
```

Driver hiện báo ValueError để kết thúc series cầnreview; đó là dừng do kiểm tra chiến thuật, không phải đủ5ván. Đầu ra: series.json, game_1/2.json vàlog, checks.json.
