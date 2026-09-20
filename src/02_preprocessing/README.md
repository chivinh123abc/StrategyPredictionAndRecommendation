# Module 02: Tiền Xử Lý Dữ Liệu (Data Preprocessing)

## Mục tiêu & Trách nhiệm
Module này chịu trách nhiệm làm sạch và chuẩn hóa dữ liệu thô từ hai nguồn (Riot API và Oracle's Elixir) trước khi đưa vào CSDL hoặc mô hình học máy:
- **Lọc bỏ trận đấu bất thường:** Loại bỏ các trận Remake, trận đấu có người AFK/thoát game sớm.
- **Xử lý giá trị ngoại lai (Outliers):** Áp dụng phương pháp IQR (Interquartile Range) và Z-Score đối với các chỉ số kinh tế, sát thương ở phút thứ 10.
- **Xử lý giá trị thiếu (Missing values):** Kiểm tra và bù đắp hoặc loại bỏ các bản ghi không hoàn chỉnh.

## Dữ liệu vào (Input)
- `data/database/lol_live_data.db` (bảng thô `matches_10min`)
- `data/raw/2026_LoL_esports_match_data_from_OraclesElixir.csv`

## Dữ liệu ra (Output)
- Dữ liệu sạch được chuẩn hóa lưu trữ vào CSDL và các tập train/test.
