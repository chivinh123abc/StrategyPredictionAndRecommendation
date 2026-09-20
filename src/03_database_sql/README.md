# Module 03: Cơ Sở Dữ Liệu & Truy Vấn SQL (Database & SQL)

## Mục tiêu & Trách nhiệm
Module này phục vụ trực tiếp cho nội dung chấm điểm Chương 5 & 5x (Databases and SQL) của môn học:
- **Thiết kế CSDL quan hệ:** Đạt chuẩn 1NF và 3NF trên CSDL SQLite (`lol_live_data.db`).
- **5 Câu truy vấn phân tích nâng cao:**
  1. Thống kê tỉ lệ thắng và chênh lệch vàng phút 10 theo từng tướng/vị trí (`GROUP BY`, `HAVING`).
  2. Phân tích tác động của Rồng đầu / Sâu hư không đến kết quả trận đấu (`JOIN`, `Aggregations`).
  3. Xếp hạng tướng theo chỉ số Snowball bằng Window Functions (`DENSE_RANK()`, `ROW_NUMBER()`).
  4. Phân tích đối chiếu giữa Đấu giải chuyên nghiệp (Pro Play) và Rank Đơn (`Subquery`, `UNION ALL`).
  5. Phát hiện các cặp tướng phối hợp hiệu quả nhất (Synergy Duo Winrate).

## Dữ liệu vào (Input)
- `data/database/lol_live_data.db`
