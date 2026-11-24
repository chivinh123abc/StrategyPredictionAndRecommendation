# Thống kê đối đầu Pro

3000 trận, 30000 observations; 3098 kèo gộp, 1170 kèo n>=5.

Ghép cùng game/role, khác side. GD/XPD/CSD = chỉ số người chọn trừ người đối diện; giữ số âm và missing.

all_matchups tách league/patch; pooled và ba bảng xếp gộp các league/patch thực có, giữ danh sách nguồn. Bảng giải thích runtime dùng đúng cửa sổ/region của advisor, không lấy cả corpus để chấm trận quá khứ.

Winrate là kết quả cả đội, Wilson95; mean resource CI dùng Student-t. Người chơi lặp, đội hình, gank và patch là confounding; không xác nhận counter nhân quả. N5 chỉ là ngưỡng hiển thị. Không có dữ liệu lane suy tạo.
