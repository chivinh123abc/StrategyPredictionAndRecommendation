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

import re

# 6. Cấu hình Đồng bộ Google Drive & Mùa giải Esports
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH").strip()
GOOGLE_DRIVE_FOLDER_URL = f"https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}"
DRIVE_SYNC_MANIFEST = os.path.join(RAW_DATA_DIR, ".drive_sync_manifest.json")
MIN_MATCHES_THRESHOLD = int(os.getenv("MIN_MATCHES_THRESHOLD", "3000"))

# Danh sách giải đấu trọng tâm (tùy chọn, ví dụ: LCK, LCP, LPL). Mặc định None = lấy toàn bộ giải đấu.
raw_leagues = os.getenv("ESPORTS_TARGET_LEAGUES", "").strip()
ESPORTS_TARGET_LEAGUES = [l.strip().upper() for l in raw_leagues.split(",") if l.strip()] if raw_leagues else None

def get_active_esports_season():
    """Tự động xác định mùa giải Esports mới nhất có trong data/raw/ hoặc theo .env."""
    env_season = os.getenv("ESPORTS_SEASON", "").strip()
    if env_season:
        return env_season
    found_years = []
    if os.path.exists(RAW_DATA_DIR):
        for f in os.listdir(RAW_DATA_DIR):
            m = re.match(r"^(\d{4})_LoL_esports_match_data_from_OraclesElixir\.csv$", f)
            if m:
                found_years.append(int(m.group(1)))
    return str(max(found_years)) if found_years else "2026"

def get_active_esports_file():
    """
    Tự động xác định file dữ liệu giải đấu hoạt động:
    1. Nếu có cấu hình đường dẫn file trực tiếp trong .env -> dùng file đó.
    2. Nếu tồn tại tệp ghép thích ứng esports_active_matches.csv -> dùng tệp này.
    3. Ngược lại, trỏ đến tệp mùa giải mới nhất {ESPORTS_SEASON}_LoL_...csv trong data/raw/.
    """
    env_file = os.getenv("ESPORTS_RAW_CSV", "").strip()
    if env_file and os.path.exists(env_file):
        return env_file
    adaptive_file = os.path.join(RAW_DATA_DIR, "esports_active_matches.csv")
    if os.path.exists(adaptive_file):
        return adaptive_file
    return os.path.join(RAW_DATA_DIR, f"{ESPORTS_SEASON}_LoL_esports_match_data_from_OraclesElixir.csv")

ESPORTS_SEASON = get_active_esports_season()
ESPORTS_RAW_CSV = get_active_esports_file()

