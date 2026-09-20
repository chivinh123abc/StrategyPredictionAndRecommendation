"""
Package cấu hình tập trung của dự án.
Cho phép import trực tiếp: from src.config import OUTPUT_CSV, OUTPUT_DB, ...
"""

from .settings import (
    ACTIVE_SERVERS,
    BASE_DIR,
    DATABASE_DIR,
    DATA_DIR,
    DRIVE_SYNC_MANIFEST,
    ESPORTS_RAW_CSV,
    GOOGLE_DRIVE_FOLDER_ID,
    GOOGLE_DRIVE_FOLDER_URL,
    OUTPUT_CSV,
    OUTPUT_DB,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    RIOT_API_KEY,
    SERVER_METADATA,
    TARGET_MATCHES_PER_SERVER,
)
