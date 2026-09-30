# Module 03: Cơ Sở Dữ Liệu & Truy Vấn SQL (Database & SQL)

## Mục tiêu & Trách nhiệm
Module này phục vụ trực tiếp cho nội dung chấm điểm Chương 5 & 5x (Databases and SQL) của môn học:
- **Thiết kế CSDL quan hệ:** Đạt chuẩn 1NF và 3NF trên CSDL SQLite (`data/database/lol_live_data.db`).
- **Hệ thống bảng hiện có trong `lol_live_data.db`:**
  1. `matches_10min` (1,009 dòng, 42 cột): Dữ liệu Rank Đơn/Đôi cao thủ VN2 & KR lúc 10 phút.
  2. `tournament_matches` (6,000 dòng, 155 cột): Dữ liệu cấp trận/đội tuyển 6 giải đấu đỉnh cao (`LCK, LCP, LPL, MSI, WLDS, EWC`). Khóa chính: `(gameid, side)`.
  3. `tournament_players` (30,000 dòng, 129 cột): Dữ liệu chi tiết 10 tuyển thủ theo 5 lane. Khóa chính: `(gameid, participantid)`, Khóa ngoại: `(gameid, side) -> tournament_matches(gameid, side)`.
- **5 Câu truy vấn phân tích nâng cao (Chương 5 & 5x):**
  1. Thống kê tỉ lệ thắng và chênh lệch vàng phút 10 theo từng tướng/vị trí (`GROUP BY`, `HAVING`).
  2. Phân tích tác động của Rồng đầu / Sâu hư không đến kết quả trận đấu (`JOIN`, `Aggregations`).
  3. Xếp hạng tướng theo chỉ số Snowball bằng Window Functions (`DENSE_RANK()`, `ROW_NUMBER()`).
  4. Phân tích đối chiếu giữa Đấu giải chuyên nghiệp (Pro Play) và Rank Đơn (`Subquery`, `UNION ALL`).
  5. Phát hiện các cặp tướng phối hợp hiệu quả nhất (Synergy Duo Winrate).

## Dữ liệu vào (Input)
- `data/database/lol_live_data.db`

