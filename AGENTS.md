# Hướng dẫn cho agent làm việc trong dự án

Trước khi làm việc, đọc [AI/AI_RULES.md](AI/AI_RULES.md), trạng thái hiện hành ở [AI/PROJECT_STATE.md](AI/PROJECT_STATE.md), và [quy định cập nhật kiến thức](AI/KNOWLEDGE_RULES.md). Khi dùng SpecKit, đọc thêm [.specify/memory/constitution.md](.specify/memory/constitution.md).

Mọi bổ sung/thay đổi phương pháp hoặc chức năng phải cập nhật [sổ kiến thức dùng viết báo cáo](docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md) trong cùng đợt làm việc: chương/trang hoặc nguồn mở rộng, nơi dùng, chức năng, output, trạng thái, minh chứng và giới hạn. Không chỉ ghi ở hội thoại hoặc spec. Planned output phải ghi rõ chưa tồn tại. Với thay đổi không ảnh hưởng kiến thức, ghi lý do theo `AI/KNOWLEDGE_RULES.md`.

Không tự commit/push; dùng `.venv` cho Python. Kiểm tra theo tác động thay đổi; sửa tài liệu không đòi retrain model không đổi. Quy định truy vết không tạo thêm bước xin phép thường lệ trong phạm vi người dùng đã giao.
