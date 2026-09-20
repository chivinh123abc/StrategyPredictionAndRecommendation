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
    ESPORTS_SEASON,
    ESPORTS_TARGET_LEAGUES,
    GOOGLE_DRIVE_FOLDER_ID,
    GOOGLE_DRIVE_FOLDER_URL,
    MIN_MATCHES_THRESHOLD,
    OUTPUT_CSV,
    OUTPUT_DB,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    RIOT_API_KEY,
    SERVER_METADATA,
    TARGET_MATCHES_PER_SERVER,
)
