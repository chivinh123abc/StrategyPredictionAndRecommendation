# Thu thập snapshot rank đủ10người

Server KR, Solo/Duo; ngưỡng MASTER+ tại lúc kiểm tra.
Tổng 5 trận: nhận 2, loại 3, thiếu 0.
Đã kiểm 46 participant duy nhất; đủ10người đạt ngưỡng tại snapshot: 5 trận.
Trạng thái collection: complete. Xem summary.json/guard issues nếu API dừng.

Chỉ nhận nhóm gần trận nếu snapshot sau kết thúc trận tối đa24giờ và10snapshot trải trong tối đa15phút. Đây là ngưỡng kỹ thuật tự thiết kế, chỉnh được, chưa tối ưu.
Snapshot được chụp nối tiếp, không đồng thời; không xác nhận rank lịch sử lúc trận. Không tự chuyển thành historical_interval hoặc bật tín hiệu cho Giải.
Không có Solo/Duo entry/lỗi API là thiếu thông tin, không suy thành tier thấp. Trận đã biết có người dưới ngưỡng được loại; có thể đồng thời còn thiếu participant khác.
Chỉ cohort snapshot đủ điều kiện được xuất accepted_observations nếu có timeline; gold/XP/CS gần10/15phút chỉ mô tả. Match acceptance và coverage timeline là hai điều kiện riêng.

| Match | Kết quả | Đạt tier | Dưới tier | Thiếu | Lý do |
|---|---|---:|---:|---:|---|
| KR_8463947440 | rejected | 10 | 0 | 0 | match_too_old_for_near_match_proxy |
| KR_8471152856 | accepted | 10 | 0 | 0 | đủ điều kiện snapshot proxy |
| KR_8471152777 | accepted | 10 | 0 | 0 | đủ điều kiện snapshot proxy |
| KR_8470100138 | rejected | 10 | 0 | 0 | match_too_old_for_near_match_proxy |
| KR_8467485073 | rejected | 10 | 0 | 0 | match_too_old_for_near_match_proxy |
