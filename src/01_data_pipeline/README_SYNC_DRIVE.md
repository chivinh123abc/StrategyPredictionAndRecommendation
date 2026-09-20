# HƯỚNG DẪN MODULE: ĐỒNG BỘ DỮ LIỆU ĐẤU GIẢI TỪ GOOGLE DRIVE

> **Tệp mã nguồn:** [`sync_google_drive.py`](sync_google_drive.py)  
> **Mục tiêu:** Tự động phát hiện, kiểm tra tính toàn vẹn và đồng bộ các mùa giải chuyên nghiệp (Oracle's Elixir) từ Google Drive về máy trạm cục bộ.

---

## 1. MỤC TIÊU VÀ VAI TRÒ CỦA PIPELINE

- **Nhiệm vụ cốt lõi:** Kết nối trực tiếp với Thư mục Google Drive dùng chung ([ID: `1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`](https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH)) lưu trữ toàn bộ dữ liệu các mùa giải chuyên nghiệp Oracle's Elixir (từ 2014 đến nay).
- **Tự động hóa cộng tác:** Khi một thành viên trong nhóm tải lên bản cập nhật dữ liệu mới hoặc file bổ sung lên Google Drive, các thành viên khác chỉ cần chạy một lệnh duy nhất để đồng bộ về máy trạm cục bộ mà không cần phải tải thủ công qua trình duyệt web.
- **Tối ưu hóa băng thông (Smart Caching):** Kiểm tra dung lượng và siêu dữ liệu cục bộ trước khi tải; tuyệt đối không tải lại tệp lớn (~70 MB - 100 MB) nếu nội dung trên máy đã trùng khớp với trên đám mây.
- **Đầu ra (Output):** Các tệp dữ liệu phẳng lưu trữ an toàn tại `data/raw/*.csv` phục vụ cho khâu nạp CSDL (Module 03) và tiền xử lý làm sạch (Module 02).

---

## 2. KIẾN TRÚC LUỒNG ĐỒNG BỘ ĐÁM MÂY (CLOUD DATA FLOW)

```
[ Google Drive Shared Folder: 1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH ]
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
     [ Chế độ quét --list ]        [ Chế độ tự động thông minh ]
  (gdown.download_folder với        (Tự trích xuất N năm mới nhất)
     skip_download=True)                       │
               │                               ▼
               ▼               [ Kiểm tra file trong data/raw/ ]
    [ Xuất danh mục file ]                     │
    (Tên file & Google File ID)       ┌────────┴────────┐
                                      ▼                 ▼
                              [ Đã tồn tại & ]   [ Chưa có hoặc ]
                              [  khớp dung   ]   [ dùng --force ]
                              [    lượng     ]          │
                                      │                 ▼
                                      ▼        [ gdown.download ]
                              [ Bỏ qua tải, ]  (Tải stream resume)
                              [  tiết kiệm  ]           │
                              [   băng thông ]          ▼
                                               [ Lưu data/raw/*.csv ]
                                                        │
                                                        ▼
                                       [ Ghi nhận lịch sử vào file ]
                                       [ data/raw/.drive_sync_manifest.json ]
```

---

## 3. GIẢI THÍCH CHI TIẾT CÁC PHƯƠNG THỨC TRONG MÃ NGUỒN

### 3.1. Khởi tạo & Cấu hình đường dẫn (`__init__`)
- **Vị trí:** Dòng 52 - 58.
- **Chức năng:** Nạp `folder_id` từ biến cấu hình tập trung `GOOGLE_DRIVE_FOLDER_ID` trong `src.config` (hoặc từ `.env`).
- Khởi tạo bộ nhớ đệm trong phiên `self._remote_files_cache = None` để tránh quét Drive lặp đi lặp lại.
- Đảm bảo thư mục đích `data/raw/` luôn được tự động khởi tạo (`os.makedirs(..., exist_ok=True)`).

### 3.2. Quản lý Cache kiểm soát đồng bộ (`load_manifest` & `save_manifest`)
- **Tệp lưu trữ:** `data/raw/.drive_sync_manifest.json`.
- **Cơ chế:** Lưu vết metadata của từng file đã tải thành công: `Google File ID`, `Dung lượng byte (size)`, và `Thời điểm đồng bộ (synced_at)`.
- **Lợi ích:** Tránh việc đọc lại toàn bộ file CSV nặng hàng trăm MB từ đĩa cứng khi kiểm tra trạng thái đồng bộ.

### 3.3. Quét siêu dữ liệu đám mây (`list_folder_files`)
- Sử dụng hàm `gdown.download_folder(..., skip_download=True)` để lấy toàn bộ danh sách file và ID tương ứng chỉ trong **2 - 3 giây** mà không tiêu tốn băng thông tải nội dung.
- Kết quả được lưu vào cache `self._remote_files_cache` để các lần gọi tiếp theo trong cùng phiên chạy được trả về ngay lập tức.

### 3.4. Thuật toán quyết định mùa giải thông minh (`sync_smart_latest` & `count_matches`)
- **Nguyên lý miền nghiệp vụ (Domain Knowledge):**
  - Mùa giải LoL thay đổi liên tục về bản đồ, mục tiêu lớn và trang bị. Việc gộp dữ liệu nhiều năm cũ sẽ gây hiện tượng **Trôi dạt khái niệm (Concept Drift)**.
  - Tuy nhiên, vào **đầu mùa giải mới** (ví dụ đầu năm 2027), số lượng trận đấu chuyên nghiệp còn ít $\rightarrow$ cần kéo thêm nửa sau của mùa giải liền trước để bù đắp cỡ mẫu.
- **Quy tắc quyết định tự động của thuật toán:**
  1. Quét danh sách mùa giải thực tế trên Google Drive bằng Regex $\texttt{\^(\textbackslash d\{4\})\_...csv\$}$ $\rightarrow$ luôn xác định mùa giải **MỚI NHẤT** (ví dụ: 2026, hoặc 2027 sau này).
  2. Đồng bộ tệp của mùa giải mới nhất về `data/raw/`.
  3. Đếm số lượng trận đấu độc lập (`unique gameid`) trong file mùa giải mới nhất:
     - **Nếu số trận $\ge$ `MIN_MATCHES_THRESHOLD` (mặc định 3,000 trận):** Đánh giá năm mới nhất **ĐÃ ĐỦ LỚN** (ví dụ 2026 hiện có tới **8,874 trận**). Thuật toán **CHỈ DÙNG DUY NHẤT NĂM NÀY**, tuyệt đối **KHÔNG kéo thêm năm trước** (2025) để giữ trọn vẹn Meta và tính đồng nhất dữ liệu.
     - **Nếu số trận $<$ 3,000 trận (giai đoạn đầu mùa giải):** Kích hoạt phương thức `build_adaptive_dataset(latest_year, previous_year)`:
       - Lấy **TOÀN BỘ** trận đấu của năm mới nhất.
       - Tính số trận còn thiếu: $\text{needed} = \text{min\_matches} - \text{current\_matches}$.
       - Sắp xếp các trận của năm trước theo ngày thi đấu lùi dần từ cuối năm về trước (CKTG / Mùa Hè) để trích xuất đúng $\text{needed}$ trận từ **PHẦN CUỐI NĂM** của năm trước đó cho đến khi đủ số lượng yêu cầu.
       - Ghép lại thành tệp dữ liệu hoạt động: [`data/raw/esports_active_matches.csv`](data/raw/esports_active_matches.csv).

### 3.5. Đồng bộ từng file (`sync_file`)
- Kiểm tra file cục bộ tại `data/raw/{filename}`:
  - Nếu đã tồn tại và không bật cờ `--force`: In thông báo `[✓] Đã có sẵn`, dung lượng và ngày đồng bộ $\rightarrow$ **bỏ qua tải để tiết kiệm băng thông**.
  - Nếu chưa có hoặc có cờ `--force`: Tiến hành tải file qua `gdown.download(..., resume=True)` hỗ trợ tiếp tục tải nếu mạng gián đoạn.
- **Xử lý ngoại lệ thông minh:** Nếu Google Drive trả về lỗi vượt hạn ngạch tải ẩn danh (`Quota exceeded`), script sẽ tự động xuất hướng dẫn người dùng cách tải qua mẹo "Tạo bản sao" chỉ trong 30 giây.

### 3.6. Đồng bộ toàn bộ lịch sử (`sync_all`)
- Duyệt qua toàn bộ danh sách tất cả các file (từ 2014 đến nay) theo thứ tự tăng dần và đồng bộ từng file một cách an toàn.

---

## 4. CHIẾN LƯỢC LỰA CHỌN DỮ LIỆU ĐỒ ÁN (DATA STRATEGY)

### 📌 Tại sao ưu tiên độc quyền mùa giải 2026 (hoặc tối đa 2025 + 2026)?
1. **Triệt tiêu 100% Hiện tượng Trôi Dạt Dữ Liệu (Concept Drift):**
   - Mùa giải 2026 áp dụng thể thức thi đấu mới **Fearless Draft (Cấm chọn không lặp tướng)**, bản đồ làm lại địa hình Summoner's Rift và cơ chế bùa lợi quái khủng mới (Sâu Hư Không / Voidgrubs, Atakhan).
   - Dữ liệu từ các năm cũ (2014 - 2023) không có các mục tiêu này (dẫn đến giá trị NULL hoặc 0), nếu đưa vào huấn luyện mô hình sẽ gây **nhiễu nghiêm trọng** và làm giảm độ chính xác dự đoán trận đấu hiện tại.
2. **Quy mô mẫu đã vượt ngưỡng hội tụ:**
   - Riêng tệp `2026_LoL_esports_match_data_from_OraclesElixir.csv` đã có tới **106,488 dòng** (với **8,874 trận đấu chuyên nghiệp** độc lập).
   - Cỡ mẫu này đã quá đủ lớn để thực hiện các phép kiểm định thống kê suy diễn ($Z$-test, $t$-test) đạt mức ý nghĩa cao ($p$-value < 0.001) và huấn luyện các mô hình Machine Learning (Random Forest, XGBoost) một cách mượt mà nhất.
3. **Áp dụng kỹ thuật Cửa Sổ Trượt Thời Gian (Adaptive Sliding Window):**
   - Khi bước sang mùa giải mới, hệ thống tự động trượt cửa sổ thời gian để luôn ưu tiên dữ liệu mang tính thời sự cao nhất.

---

## 5. HƯỚNG DẪN VẬN HÀNH DÒNG LỆNH

```bash
# 1. Chế độ mặc định: Tự động thẩm định mùa giải mới nhất và tự quyết định có lấy thêm năm trước hay không:
python src/01_data_pipeline/sync_google_drive.py

# 2. Lọc chỉ lấy các giải đấu trọng điểm (ví dụ: LCK, LCP, LPL):
python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL

# 3. Lọc giải đấu kết hợp ngưỡng tối thiểu số trận:
python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL --min-matches 2000

# 4. Điều chỉnh ngưỡng số trận tối thiểu (mặc định: 3000 trận):
python src/01_data_pipeline/sync_google_drive.py --min-matches 5000

# 5. Đồng bộ một năm chỉ định bất kỳ (ví dụ: 2025 hoặc 2024):
python src/01_data_pipeline/sync_google_drive.py --year 2025

# 6. Liệt kê toàn bộ danh mục file có trên Google Drive cùng File ID (không tải):
python src/01_data_pipeline/sync_google_drive.py --list

# 7. Bắt buộc tải lại bản mới nhất từ Drive dù file trên máy đã tồn tại:
python src/01_data_pipeline/sync_google_drive.py --force

# 8. Tải toàn bộ tất cả 13 mùa giải từ 2014 đến nay:
python src/01_data_pipeline/sync_google_drive.py --all
```

---

## 6. BẢNG MÃ LỖI THƯỜNG GẶP & CÁCH XỬ LÝ

| Mã lỗi / Cảnh báo | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **Cannot find module `gdown`** | Môi trường Python (hoặc venv) đang chạy chưa cài gói `gdown`. | Chạy lệnh: `pip install gdown` |
| **Google Drive Quota Exceeded ("Too many users have viewed or downloaded...")** | File công khai có quá nhiều lượt tải ẩn danh cùng lúc nên Google tạm khóa tải qua script. | **Mẹo khắc phục 100% trong 30 giây:**<br>1. Mở link Drive trực tiếp của file trên trình duyệt.<br>2. Nhấp chuột phải $\rightarrow$ Chọn **Tạo bản sao (Make a copy)** vào Google Drive cá nhân.<br>3. Tải bản sao đó về và bỏ vào thư mục `data/raw/`.<br>4. Chạy lại script, hệ thống sẽ tự nhận diện file hợp lệ. |
| **Google Drive Access Denied** | Link thư mục bị tắt quyền chia sẻ công khai. | Đảm bảo thư mục Google Drive được bật chế độ *"Bất kỳ ai có đường liên kết đều có thể xem"*. |
