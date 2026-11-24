# Đối chiếu Rank / Pro — thống kê mô tả riêng

Rank: 5 trận / 50 dòng; Pro (WLDS): 206 trận / 2060 dòng.
Patch Rank: 16.23; Pro: 15.17, 15.20, 16.17, 16.20.
Cặp có cùng patch/role/tướng/đối thủ: 0 dòng (mỗi platform giữ riêng).

- Các CSV rank_matchups/pro_matchups ghi số trận, kết quả thắng cả đội, Wilson CI95 và n/mean/SD của chênh lệch vàng/XP/CS phút10/15.
- rank_pro_same_patch.csv chỉ ghép mã patch major.minor trùng chính xác; không cộng số mẫu hai miền hoặc tự đổi phiên bản.
- CS Rank = lính đường + quái rừng; CS Pro là total CS do nguồn cung cấp, cần kiểm tra tương thích trước khi dùng làm feature chung.
- Frame policy: nearest; chỉ nhận frame cách mốc tối đa1000ms. before: không sau mốc; nearest: có thể sau mốc, CHỈ thống kê mô tả, không dùng làm đầu vào dự báo đúng phút10/15. frame_ms ghi thời điểm thật; không nội suy.
- Missing để trống; không dùng frame phút9 thay phút10, không giả lập chỉ số theo đường.
- Role là phân loại sau trận của Riot, không xác nhận đi đường cả trận hay thứ tự draft. Pro cũng dùng role sau trận.
- Seed Thách Đấu là cách lấy mẫu hiện tại, không chứng minh rank lịch sử của10người. Chưa thu rank cá nhân; không có phân tầng rank.
- Hai hướng A→B/B→A trong cùng trận có liên hệ; Wilson giả định trận độc lập, cùng người chơi tái xuất làm CI lạc quan.
- Chưa cân bằng trình độ/người chơi, phe, jungle/support, patch drift hoặc sửa sai số chọn mẫu; chưa chứng minh counter/cơ chế hoặc tăng thắng.
- Contextual/legacy chưa đọc tín hiệu Rank. Chưa benchmark Pro-only/Rank-only/hybrid, chưa có quyết định trộn miền.

- Ghép tên tướng đúng chuỗi Riot/nguồn Pro; chưa chuẩn hóa mọi alias giữa nguồn, có thể bỏ sót cặp (không tự đoán tên).
Số cache bị loại: 0. Xem summary.json để biết coverage và lý do.

Nguồn kỹ thuật: [Riot LoL](https://developer.riotgames.com/docs/lol), [Match-v5](https://developer.riotgames.com/apis#match-v5/GET_getMatch), [HTTP/rate limits](https://developer.riotgames.com/docs/portal).
