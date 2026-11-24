> **LỊCH SỬ — đã ngừng sử dụng24/11/2026.** Lookahead đã được gỡ theo yêu cầu người dùng; tài liệu/đầu ra này chỉ giữ minh chứng phiên cũ, không phải chức năng hiện hành. Xem `reports/legacy_contextual_comparison/COMPARISON.md` và `docs/BAN_LEGACY_VA_CONTEXTUAL.md` cho phạm vi mới.

# Ban có định hướng: so sánh T1–Gen.G5draft

Cùng dữ liệu Worlds cutoff13/11/2026 patch dataset16.20, cùng roster và lịch first-pickT1/Gen.G/T1/Gen.G/T1. Cả3chếđộ bật test chọn số1 dù thiếu tin cậy; không mô phỏng thắng/thua.

| Chế độ | Draft hoàn thành | Pick không lặp | Tập6ban đầu khác nhau | Jaccard6ban đầu trung bình |
|---|---:|---:|---:|---:|
| legacy | 5 | 50 | 1/5 | 1.000 |
| contextual | 5 | 50 | 5/5 | 0.471 |
| lookahead | 5 | 50 | 5/5 | 0.145 |

## Sáu lượt ban đầu trước/sau

| Ván | Cũ:T1Ban1–3 | Cũ:Gen.GBan1–3 | Lookahead:T1Ban1–3 | Lookahead:Gen.GBan1–3 |
|---:|---|---|---|---|
| 1 | Nocturne, Renata Glasc, Olaf | Vi, Cassiopeia, Qiyana | Nautilus, Alistar, Olaf | Renata Glasc, Nocturne, Jayce |
| 2 | Renata Glasc, Cassiopeia, Qiyana | Nocturne, Vi, Olaf | Nocturne, Pantheon, Nautilus | Jayce, Jarvan IV, Ambessa |
| 3 | Nocturne, Vi, Olaf | Renata Glasc, Cassiopeia, Qiyana | Pantheon, Yunara, Xayah | Akali, Nocturne, Jarvan IV |
| 4 | Renata Glasc, Cassiopeia, Qiyana | Nocturne, Vi, Olaf | Camille, Viktor, Akali | Milio, Karma, Xayah |
| 5 | Nocturne, Vi, Olaf | Renata Glasc, Cassiopeia, Qiyana | Pantheon, Yunara, Naafiri | Camille, Viktor, Trundle |

## Ban/Pick đủ100lượt mỗi chế độ

- [Legacy — bảng từng Ban/Pick](legacy/QUICK_VIEW.md)
- [Contextual — bảng từng Ban/Pick](contextual/QUICK_VIEW.md)
- [Lookahead — bảng từng Ban/Pick](lookahead/QUICK_VIEW.md)
- [Lookahead — báo cáo lý do/nhánh](lookahead/REPORT.md)

JSON từnggame chứa `advice.pool_impact`, `search_trace.candidate_summary`, `search_trace.root_evaluations` và từngbranch trace/leaf/weight. So sánh lựa chọn bị loại với lựa chọn được chốt; không gọi score là xác suất thắng.

## Hiệu năng và độ bất định

50quyếtđịnhban: trungbình 0.471s, p95 0.787s, max 1.371s theo đồnghồ nội bộtrên lầnchạynày. Khôngphải benchmarkmáyđộc lập; cócache.
Đã replay 583đườngnhánh từ 295rootcandidate qua đúnglịchcấm/chọn, không trùngtướng/vi phạmFearless; sâu tốiđa9plies.
Tỷtrọng phảnứngđượcgiữ (điềukiệntrongpoolcóhỗtrợ): trungbình 21.1%, nhỏnhất 5.8%. Phầnbịcắtlớn; 48/50quyếtđịnh có khoảngđộnhạytruncationchồnglấn ứngviênkhác. Đây KHÔNG là CIthốngkê hoặc bảochứngrootđượcchọntốtnhất.

## Kết luận có thể rút ra

Đã có tínhngữcảnh và xétnhánh, lượtban khôngcònbịtáitạobởichỉsốpresencecốđịnh. Khôngcóbonusépdiversity. Độđa dạng tăngkhôngchứngminhdrafttốthơn: vẫn cần evaluatorchiếnthuật/đánhgiáđộclập, mởrộngđộphủresponse và kiểmtrachọn/phốihợptướng. Greedycontinuation khácvớithựctếvìrealpolicytínhtoánlạiởlượtsau; tracechỉlàkịchbản.

Khôngfitmodelmới/đổiDB, khôngtựđộngchuyểnlegacythànhlookaheadcho tấtcả phiên. Dùng `--ban-strategy lookahead --ban-response-model models/opponent_model.pkl` đểchạy chếđộmới.
