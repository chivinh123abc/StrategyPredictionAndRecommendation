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
                                      ▼        [ TẦNG 1: gdown ]
                              [ Bỏ qua tải, ]  (Tải ẩn danh nhanh)
                              [  tiết kiệm  ]           │
                              [   băng thông ]  ┌───────┴───────┐
                                                ▼               ▼
                                           [Thành công]    [Quota Exceeded]
                                                │               │
                                                │               ▼
                                                │      [ TẦNG 2: Drive API ]
                                                │      (OAuth2 Desktop App)
                                                │      - Copy về My Drive
                                                │      - Stream tải 8MB/chunk
                                                │      - Tự động xóa copy
                                                │               │
                                                └───────┬───────┘
                                                        ▼
                                               [ Lưu data/raw/*.csv ]
                                                        │
                                                        ▼
                                       [ Ghi nhận lịch sử vào file ]
                                       [ data/raw/.drive_sync_manifest.json ]
```

---

## 3. GIẢI THÍCH CHI TIẾT CÁC PHƯƠNG THỨC TRONG MÃ NGUỒN

### 3.1. Khởi tạo & Cấu hình đường dẫn (`__init__`)
- **Vị trí:** Dòng 60 - 75.
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
  - Tuy nhiên, vào **đầu mùa giải mới**, số lượng trận đấu chuyên nghiệp thuộc các giải mục tiêu còn ít $\rightarrow$ cần kéo thêm nửa sau của mùa giải liền trước để bù đắp cỡ mẫu.
- **Quy tắc quyết định tự động của thuật toán:**
  1. Quét danh sách mùa giải thực tế trên Google Drive bằng Regex $\texttt{\^(\textbackslash d\{4\})\_...csv\$}$ $\rightarrow$ luôn xác định mùa giải **MỚI NHẤT** (ví dụ: 2026, hoặc 2027 sau này).
  2. Đồng bộ tệp của mùa giải mới nhất về `data/raw/`.
  3. Đếm số lượng trận đấu độc lập (`unique gameid`) trong file mùa giải mới nhất theo bộ lọc giải đấu:
     - **Nếu số trận $\ge$ `MIN_MATCHES_THRESHOLD` (mặc định 3,000 trận):** Đánh giá năm mới nhất **ĐÃ ĐỦ LỚN**. Thuật toán **CHỈ DÙNG DUY NHẤT NĂM NÀY**, tuyệt đối **KHÔNG kéo thêm năm trước** (2025) để giữ trọn vẹn Meta và tính đồng nhất dữ liệu.
     - **Nếu số trận $<$ 3,000 trận (giai đoạn đầu mùa giải):** Kích hoạt phương thức `build_adaptive_dataset(latest_year, previous_year)`:
       - Lấy **TOÀN BỘ** trận đấu của năm mới nhất.
       - Tính số trận còn thiếu: $\text{needed} = \text{min\_matches} - \text{current\_matches}$.
       - Sắp xếp các trận của năm trước theo ngày thi đấu lùi dần từ cuối năm về trước (CKTG / Mùa Hè) để trích xuất đúng $\text{needed}$ trận từ **PHẦN CUỐI NĂM** của năm trước đó cho đến khi đủ số lượng yêu cầu.
       - Ghép lại thành tệp dữ liệu hoạt động: [`data/raw/esports_active_matches.csv`](data/raw/esports_active_matches.csv).

### 3.5. Đồng bộ từng file (`sync_file`) — Cơ chế tải 2 tầng
- Kiểm tra file cục bộ tại `data/raw/{filename}`:
  - Nếu đã tồn tại và không bật cờ `--force`: In thông báo `[✓] Đã có sẵn`, dung lượng và ngày đồng bộ $\rightarrow$ **bỏ qua tải để tiết kiệm băng thông**.
  - Nếu chưa có hoặc có cờ `--force`: Tiến hành quy trình tải 2 tầng:
    - **Tầng 1 (gdown):** Tải trực tiếp ẩn danh qua `gdown.download(..., resume=True)`. Nhanh chóng, không cần xác thực tài khoản. Kiểm tra tính toàn vẹn file sau tải (> 100 KB và không phải trang HTML lỗi).
    - **Tầng 2 (Google Drive API v3 + OAuth2 Fallback):** Tự động kích hoạt khi Tầng 1 gặp lỗi Quota Exceeded (`Too many users have viewed or downloaded...`):
      1. Khởi tạo xác thực OAuth2 qua `credentials.json` (Desktop App), lưu token cache vào `.gdrive_token.json`.
      2. Tự động tạo bản sao tạm thời vào Google Drive cá nhân của người dùng (`service.files().copy()`) để xóa bỏ giới hạn Quota của file chia sẻ công khai.
      3. Tải nội dung stream từ bản copy (8 MB/chunk) về `data/raw/`.
      4. Tự động xóa bản copy tạm khỏi Google Drive ngay sau khi tải xong (`service.files().delete()`).

### 3.6. Bộ lọc giải đấu chuyên nghiệp (`filter_leagues` & `filter_esports_by_leagues`)
- Cung cấp phương thức lọc độc lập không cần tải lại dữ liệu từ Google Drive:
  - Lọc chính xác các giải đấu mục tiêu (khuyên dùng: `LCK, LCP, LPL, MSI, WLDS, EWC`).
  - Hỗ trợ gọi từ dòng lệnh qua cờ `--filter` và `--filter-leagues`.
  - Hỗ trợ gọi dưới dạng hàm Python độc lập từ bất kỳ module nào:
    ```python
    from src.01_data_pipeline.sync_google_drive import filter_esports_by_leagues
    df = filter_esports_by_leagues(leagues=["LCK", "LCP", "LPL", "MSI", "WLDS", "EWC"])
    ```

### 3.7. Thẩm định độ sạch & sức khỏe dữ liệu (`check_data_health` & `check_esports_data_health`)
- Kiểm tra tính toàn vẹn đa tầng theo cấu trúc chuyên nghiệp của Oracle's Elixir:
  - Kiểm tra quy mô: tổng số dòng, số trận độc lập, dải ngày thi đấu, tỷ lệ dòng tuyển thủ vs dòng đội tuyển.
  - Kiểm tra cấu trúc chuẩn: tỷ lệ trận đủ $12$ dòng ($10$ tuyển thủ + $2$ đội).
  - Phân bổ số trận theo từng giải đấu (LCK, LCP, LPL, MSI, WLDS, EWC).
  - Thẩm định tỷ lệ khuyết thiếu (Missing Value Audit) theo từng phân tầng: Cốt lõi, Mục tiêu Team, và Timeline mốc 10 phút.
  - Xuất ra Báo cáo Thẩm định Sức khỏe Dữ liệu (**Data Health Card**) trực quan.
  - Hỗ trợ gọi từ dòng lệnh qua `--check` hoặc import Python:
    ```python
    from src.01_data_pipeline.sync_google_drive import check_esports_data_health
    check_esports_data_health()
    ```

### 3.8. Đồng bộ toàn bộ lịch sử (`sync_all`)
- Duyệt qua toàn bộ danh sách tất cả các file (từ 2014 đến nay) theo thứ tự tăng dần và đồng bộ từng file một cách an toàn.

---

## 4. CHIẾN LƯỢC LỰA CHỌN DỮ LIỆU ĐỒ ÁN (DATA STRATEGY)

### 📌 Danh mục 6 Giải đấu Trọng tâm được tích hợp trong Đồ án:
Oracle's Elixir phân loại giải đấu qua cột `league`. Hệ thống đã tối ưu lọc trọn vẹn 6 giải đấu đỉnh cao nhất thế giới:

| Phân loại | Tên giải đấu | Ký hiệu cột `league` | Ý nghĩa trong đồ án |
| :--- | :--- | :---: | :--- |
| **Nội địa lớn** | Giải Hàn Quốc | `LCK` | Đại diện trường phái kiểm soát chặt chẽ, macro bài bản. |
| **Nội địa lớn** | Giải Trung Quốc | `LPL` | Đại diện trường phái khát máu, giao tranh liên tục. |
| **Nội địa khu vực** | Giải Châu Á - Thái Bình Dương (VCS/PCS) | `LCP` | Đại diện đấu trường khu vực có các đội tuyển Việt Nam tham dự. |
| **Quốc tế đỉnh cao** | Chung Kết Thế Giới (Worlds) | `WLDS` | Đỉnh cao danh vọng cuối năm, đối đầu trực tiếp liên khu vực LCK vs LPL. |
| **Quốc tế đỉnh cao** | Mid-Season Invitational | `MSI` | Đại chiến các nhà vô địch mùa xuân toàn cầu. |
| **Quốc tế mở rộng** | Esports World Cup | `EWC` | Cúp thế giới Ả Rập Xê Út quy tụ các đội tuyển mạnh nhất. |

### 📌 Quy mô mẫu tập dữ liệu hoạt động (`data/raw/esports_active_matches.csv`):
- **Tổng số trận:** Đúng **3.000 trận đấu đỉnh cao (36.000 dòng dữ liệu, dung lượng ~26.8 MB)**.
- **Tỷ lệ có Timeline 10 phút:** **2.369 / 3.000 trận (đạt 79.0%)** — Tăng mạnh nhờ bổ sung các giải quốc tế (100% có Timeline).
- **Phân bổ chi tiết:**
  - 🇨🇳 LPL: 1.160 trận (38.7%)
  - 🇰🇷 LCK: 850 trận (28.3%)
  - 🌏 LCP: 466 trận (15.5%)
  - 👑 EWC: 265 trận (8.8%)
  - 🌍 MSI: 151 trận (5.0%)
  - 🏆 WLDS: 108 trận (3.6%)

---

## 5. HƯỚNG DẪN VẬN HÀNH DÒNG LỆNH

```bash
# 1. Chế độ khuyến nghị đồ án: Đồng bộ trọn vẹn 6 giải đấu đỉnh cao (LCK, LCP, LPL, MSI, WLDS, EWC):
python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL,MSI,WLDS,EWC

# 2. Lọc trực tiếp từ file đã có sẵn trên máy mà không cần tải lại từ Google Drive:
python src/01_data_pipeline/sync_google_drive.py --filter --filter-leagues LCK,LCP,LPL,MSI,WLDS,EWC

# 3. Kiểm tra độ sạch và tính toàn vẹn (Data Health Card) của tập dữ liệu:
python src/01_data_pipeline/sync_google_drive.py --check

# 4. Điều chỉnh ngưỡng số trận tối thiểu (mặc định: 3000 trận):
python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL,MSI,WLDS,EWC --min-matches 5000

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
| **Google Drive Quota Exceeded ("Too many users have viewed or downloaded...")** | File công khai có quá nhiều lượt tải ẩn danh cùng lúc nên Google tạm khóa tải ẩn danh. | **Tự động 100% qua Tầng 2:** Script tự động kích hoạt Google Drive API v3 (OAuth 2.0 qua `credentials.json`), tạo bản sao tạm vào My Drive để vượt hạn ngạch, tải về và tự dọn dẹp file tạm. Không cần can thiệp thủ công. |
| **Google Drive Access Denied** | Link thư mục bị tắt quyền chia sẻ công khai. | Đảm bảo thư mục Google Drive được bật chế độ *"Bất kỳ ai có đường liên kết đều có thể xem"*. |
