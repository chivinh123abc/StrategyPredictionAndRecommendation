"""
================================================================================
CẤU HÌNH HỆ THỐNG DỰ ÁN (PROJECT SETTINGS)
Dự án: Nhập môn Khoa học Dữ liệu - PTIT
Mô tả: Quản lý tập trung toàn bộ đường dẫn Input/Output, biến môi trường .env,
       và các thông số Riot API dùng chung cho toàn bộ dự án.
================================================================================
"""

import os

# 1. Định vị thư mục gốc dự án (Project)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# CURRENT_DIR là .../Project/src/config -> lùi 2 cấp về .../Project
if os.path.basename(os.path.dirname(CURRENT_DIR)) == "src":
    BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
else:
    BASE_DIR = os.path.dirname(CURRENT_DIR)

# 2. Hệ thống thư mục dữ liệu
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
DATABASE_DIR = os.path.join(DATA_DIR, "database")

# 3. File Input / Output chính của toàn bộ dự án
OUTPUT_CSV = os.path.join(PROCESSED_DATA_DIR, "lol_live_ranked_10min.csv")
OUTPUT_DB = os.path.join(DATABASE_DIR, "lol_live_data.db")

# Tự động tạo thư mục nếu chưa tồn tại
for folder in [RAW_DATA_DIR, PROCESSED_DATA_DIR, DATABASE_DIR]:
    os.makedirs(folder, exist_ok=True)

# 4. Nạp biến môi trường từ file .env
def load_dotenv_custom(env_path):
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

load_dotenv_custom(os.path.join(BASE_DIR, ".env"))

# 5. Biến Riot API & Cấu hình máy chủ
RIOT_API_KEY = os.getenv("RIOT_API_KEY", "").strip()
if not RIOT_API_KEY or "xxx" in RIOT_API_KEY:
    raise ValueError("LỖI BẢO MẬT: Chưa cấu hình RIOT_API_KEY hợp lệ trong file .env!\nHãy mở file .env và dán key của bạn vào: RIOT_API_KEY=\"RGAPI-...\"")

raw_servers = os.getenv("ACTIVE_SERVERS", "vn2,kr")
ACTIVE_SERVERS = [s.strip() for s in raw_servers.split(",") if s.strip()]

TARGET_MATCHES_PER_SERVER = int(os.getenv("TARGET_MATCHES_PER_SERVER", "50"))

SERVER_METADATA = {
    "vn2": {"platform": "vn2", "region": "sea", "country": "Vietnam", "label": "Việt Nam (VN2)"},
    "kr":  {"platform": "kr",  "region": "asia", "country": "Korea", "label": "Hàn Quốc (KR - Đấu trường Hàn & Trung)"},
    "tw2": {"platform": "tw2", "region": "sea", "country": "Taiwan", "label": "Đài Loan (TW2)"},
    "na1": {"platform": "na1", "region": "americas", "country": "North America", "label": "Bắc Mỹ (NA1)"},
    "euw1":{"platform": "euw1", "region": "europe", "country": "Europe", "label": "Tây Âu (EUW1)"}
}

# 6. Cấu hình Đồng bộ Google Drive
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH").strip()
GOOGLE_DRIVE_FOLDER_URL = f"https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}"
ESPORTS_RAW_CSV = os.path.join(RAW_DATA_DIR, "2026_LoL_esports_match_data_from_OraclesElixir.csv")
DRIVE_SYNC_MANIFEST = os.path.join(RAW_DATA_DIR, ".drive_sync_manifest.json")

