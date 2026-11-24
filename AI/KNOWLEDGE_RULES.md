# Quy định cập nhật kiến thức và minh chứng báo cáo

**Giới hạn phạm vi24/11/2026:** vận dụng bài học với một số mở rộng vừa sức, theo [phạm vi hiện hành](../docs/PHAM_VI_DO_AN_VUA_SUC.md). Trước khi thêm phương pháp, ưu tiên cách trong môn hoặc module sẵn có; ghi vì sao phần mở rộng cần thiết, giải thích được và dùng ở đâu. Không nhóm/đổi nhãn để nhận một công thức MR đang chạy thành MH. Không biến mỗi ý tưởng nghiên cứu thành chức năng bắt buộc; thay đổi không thêm lý thuyết thì ghi NV/chính sách, không tạo MR giả.

Có hiệu lực từ23/11/2026, theo yêu cầu người dùng. Áp dụng cho người phát triển, AI và mọi bước SpecKit. Các đường dẫn dưới đây tính từ gốc dự án.

## 1. Tài liệu tổng hợp bắt buộc

Nguồn tra cứu tập trung: [docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md](../docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md), gọi là **sổ kiến thức**. Tài liệu phương pháp chi tiết có thể tách riêng, nhưng phải được dẫn và tóm tắt trong sổ này; không chỉ ghi trong hội thoại, notebook, spec hoặc changelog.

Phải cập nhật sổ kiến thức trong cùng đợt thay đổi khi thêm/sửa/bỏ:

- Tính năng, thuật toán, công thức, đặc trưng, ngưỡng, trọng số, giả định, thư viện có ảnh hưởng đến phương pháp.
- Nguồn dữ liệu, phạm vi patch/thời gian, tiền xử lý, cách chia tập, mô hình, evaluator hoặc chính sách cấm/chọn.
- Phép đánh giá, baseline, metric, diễn giải kết quả, output schema, vị trí file kết quả, cách tái lập.
- Luật nghiệp vụ, giao diện hoặc luồng thao tác làm đổi chức năng đã mô tả; phân loại NV khi phù hợp.
- Trạng thái từ dự kiến → hiện thực → đã chạy → thay thế/ngừng dùng. Ghi phiên bản/mốc áp dụng, không xóa lịch sử quan trọng để làm đẹp kết quả.

## 2. Nội dung tối thiểu của mỗi mục

| Trường bắt buộc | Phải ghi gì? |
|---|---|
| ID và tên | Tái sử dụng ID hiện có khi sửa cùng nội dung; thêm ID ổn định khi có phương pháp/chức năng mới. |
| Phân loại | MH: trong môn; UD: vận dụng; MR: mở rộng; NV: nghiệp vụ/kỹ thuật. Có thể kết hợp nhưng phải chỉ rõ ranh giới. |
| Căn cứ | MH phải có chương và trang/mục slide đã đối chiếu. MR phải có nguồn phù hợp hoặc ghi rõ “policy do nhóm tự thiết kế, chưa được kiểm chứng/tối ưu”. Không bịa nguồn, trang hoặc khẳng định nằm trong môn chỉ vì có nền toán liên quan. |
| Nơi sử dụng | Module/file/hàm hoặc notebook/cell tương ứng; đổi tên/chuyển file thì cập nhật liên kết. |
| Chức năng và lý do | Nhận đầu vào gì, giải quyết vấn đề nào, đầu ra có ý nghĩa gì; MR phải giải thích chức năng bổ sung và giả định. |
| File kết quả | Đường dẫn, loại file (data/model/report/log/trace), trường quan trọng, lệnh tạo/tái lập. Nếu chưa có đầu ra bền vững thì ghi console/API và “chưa xuất file”, không invent artifact. |
| Trạng thái và bằng chứng | Dự kiến/đã hiện thực/đã chạy/đã thay thế; ngày/phiên bản, kiểm tra đã thực thi. File dự kiến ghi rõ chưa tồn tại. |
| Đánh giá và giới hạn | Số mẫu/cutoff/policy/fingerprint khi phù hợp, baseline/metric, bất định, hạn chế và điều gì chưa được chứng minh. Nếu chưa benchmark phải nói rõ. |

Khung bổ sung vào sổ kiến thức:

```markdown
### [ID] Tên kiến thức/chức năng — cập nhật YYYY-MM-DD

- Phân loại: MH / UD / MR / NV.
- Chương/trang hoặc nguồn mở rộng/chính sách tự thiết kế:
- Trạng thái và mốc áp dụng:
- Nơi dùng: file/module/hàm.
- Đầu vào, chức năng, lý do và giả định:
- Kết quả: đường dẫn và ý nghĩa; hoặc ghi rõ chưa có/dự kiến.
- Lệnh tái lập và minh chứng đã chạy:
- Đánh giá, giới hạn, mục cũ được thay thế (nếu có):
```

## 3. Tích hợp quy trình SpecKit

| Bước | Yêu cầu |
|---|---|
| specify / clarify | Ghi yêu cầu truy vết vào sổ kiến thức; chỉ rõ phần mới, phần thay đổi và trạng thái dự kiến. Không bịa thiết kế/thuật toán để hoàn thành spec. |
| plan | Đối chiếu slide/source; lập bảng kiến thức → chức năng → module → output → cách đánh giá. Tách nền môn học với phần mở rộng. |
| tasks | Có task cập nhật sổ kiến thức gắn với tính năng/phương pháp và task kiểm tra đường dẫn/nhãn trạng thái/đầu ra; không để thành việc tùy chọn sau khi nghiệm thu. |
| implement | Cập nhật sổ cùng code/dữ liệu/model/output; hoàn thành minh chứng thích hợp trước khi đánh dấu task DONE. Dự kiến chỉ chuyển thành đã chạy sau khi thực thi thật. |
| checklist | Kiểm tra yêu cầu đã quy định đủ nội dung truy vết; checkbox vẫn thuộc người review, không tự sửa marker để vượt gate. |
| analyze | Chỉ đọc: báo thiếu mapping, sai chương, output không tồn tại nhưng được gọi là đã có, hoặc số liệu lệch như lỗi nhất quán; không sửa sổ trong lệnh read-only. |
| converge | Theo phạm vi cho phép của lệnh: tạo remediation task cho chỗ thiếu/lệch; không nâng trạng thái dự kiến thành hoàn thành để làm hết lỗi. |
| constitution | Khi sửa nguyên tắc vẫn giữ nghĩa vụ này, cập nhật version và ghi tác động. Không sửa manifest cài đặt thành nơi chứa quy định. |

Sử dụng `.specify/templates/overrides/` để giữ phần tùy biến dự án. Sau nâng cấp/tái cài SpecKit phải kiểm tra lại constitution, các override và resolver; không coi manifest hash là bằng chứng rule đang có hiệu lực.

## 4. Điều kiện hoàn thành và ngoại lệ hợp lý

- Một thay đổi liên quan kiến thức/chức năng **chưa DONE về tài liệu** nếu sổ kiến thức còn sai/thiếu mapping, trạng thái hoặc đầu ra. Chủ động hoàn thiện trong phạm vi đã được giao, không biến yêu cầu này thành bước xin phép thường lệ.
- Với sửa chính tả/format hoặc hạ tầng không đổi kiến thức/chức năng, có thể ghi trong changelog/task: “Không phát sinh thay đổi kiến thức/phương pháp/chức năng; các mục [ID] vẫn đúng”, kèm lý do. Không tạo mục lý thuyết giả và không yêu cầu retrain.
- Kiểm tra phù hợp thay đổi: tài liệu kiểm tra link/nội dung; code chạy kiểm tra liên quan; model/dataset thay đổi mới tái tạo artifact và đánh giá cần thiết. Không fit model không đổi chỉ để sửa tài liệu.
- Giữ số liệu cũ theo mốc/phiên bản; khi chạy đè report phải cập nhật số liệu hiện hành và ghi thay đổi. Không trộn benchmark của hai phiên bản thành một kết luận.
- Không đánh đồng điểm heuristic, cosine, tần suất ghép cặp, độ hợp lệ của draft với xác suất thắng hay chứng minh tối ưu BO5.
- Vẫn cập nhật `AI/PROJECT_STATE.md`, `AI/TASKS.md`, `AI/CHANGELOG.md` và tài liệu kiến trúc/quyết định/schema khi có tác động; sổ kiến thức không thay thế quản lý tiến độ.

Phạm vi người dùng chọn gần nhất (24/11/2026) là legacy/contextual, đã bỏlookahead. Các mục tiêu opponent/search/BO5 khác chỉ lưu lộ trình/lịch sử với trạng thái thật, không tự triển khai hoặc coi là tính năng đang duy trì. Quy định truy vết này không tự mở rộng phạm vi hay tự hiện thực planner.
