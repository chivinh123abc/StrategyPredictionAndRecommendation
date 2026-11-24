"""
Module 07: Recommender Engine & Win Condition Analyzer (Task 3.5)
Hệ Thống Gợi Ý Cấm/Chọn Thông Minh, Nhận Diện Lỗ Hổng & Thẻ Điều Kiện Thắng (ADR-014)

Bao gồm 4 Phân hệ Chiến thuật Cốt lõi:
1. TargetBanEngine: Phân hệ CẤM Lai Ghép theo Tuyển thủ Đối phương (60-70% Đấu giải + 30-40% Solo Rank gần nhất)
2. MetaPickRecommender: Phân hệ CHỌN Tướng Chuẩn Meta (Counter-Pick + Duo Synergy + Cân bằng Đội hình AD/AP/CC/Tank)
3. PunisherEngine: Phân hệ Quét Lỗ Hổng Cấm/Chọn Của Địch & Gợi Ý Con Bài Trừng Phạt (Heavy Melee, Full AD, Zero Hard CC, Full Squishy)
4. WinConditionEngine: Engine Trích Xuất Thẻ Điều Kiện Thắng (Chủ lực, Điểm rơi sức mạnh, Mục tiêu ưu tiên, Điều kiện thua cần tránh)

Học phần: Nhập môn Khoa học Dữ liệu - PTIT (TS. Thái Tuyết Hải)
"""

import sys
import os
import json
import argparse
import pickle
import sqlite3
import warnings
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

import numpy as np
import pandas as pd

# Paths configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "06_machine_learning"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "07_recommender"))

DB_PATH = PROJECT_ROOT / "data" / "database" / "lol_live_data.db"
KMEANS_MODEL_PATH = PROJECT_ROOT / "models" / "archetype_kmeans.pkl"
RECOMMENDER_MODEL_PATH = PROJECT_ROOT / "models" / "recommender_engine.pkl"
PRO_ACCOUNTS_PATH = PROJECT_ROOT / "data" / "pro_player_accounts.json"

sys.path.insert(0, str(PROJECT_ROOT / 'src'))
from analysis_data import open_clean_connection
from historical_recommender import HistoricalRecommender, evidence

warnings.filterwarnings('ignore')


# =========================================================================
# SAFE UNPICKLER PATTERN (Để nạp model K-Means xuyên module)
# =========================================================================
class _SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'DraftArchetypeClusterer':
            import cluster_archetypes
            return getattr(cluster_archetypes, 'DraftArchetypeClusterer')
        if name in ('RecommenderEngine', 'TargetBanEngine', 'MetaPickRecommender', 'PunisherEngine', 'WinConditionEngine'):
            return globals()[name]
        return super().find_class(module, name)


def safe_load_pickle(filepath: Path) -> Any:
    with open(filepath, 'rb') as f:
        return _SafeUnpickler(f).load()


# =========================================================================
# 1. TỪ ĐIỂN THUỘC TÍNH CHIẾN THUẬT & PHÂN LOẠI TƯỚNG TOÀN DIỆN (160+ TƯỚNG)
# =========================================================================
CHAMPION_METADATA = {
    # Đường Trên (Top)
    'Aatrox': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.75, 'engage': 0.65, 'anti_melee': 0.70},
    'Ambessa': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.60, 'durability': 0.65, 'engage': 0.75, 'anti_melee': 0.60},
    'Camille': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.65, 'engage': 0.90, 'anti_melee': 0.50},
    'Cho\'Gath': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.95, 'engage': 0.60, 'anti_melee': 0.65},
    'Darius': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.55, 'durability': 0.80, 'engage': 0.40, 'anti_melee': 0.95},
    'Dr. Mundo': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.95, 'engage': 0.35, 'anti_melee': 0.65},
    'Fiora': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.60, 'engage': 0.30, 'anti_melee': 0.80},
    'Gangplank': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.35, 'durability': 0.50, 'engage': 0.50, 'anti_melee': 0.65},
    'Garen': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.80, 'engage': 0.40, 'anti_melee': 0.70},
    'Gnar': {'lane': 'top', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.70, 'engage': 0.85, 'anti_melee': 0.65},
    'Gragas': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.75, 'engage': 0.85, 'anti_melee': 0.75},
    'Gwen': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.20, 'durability': 0.65, 'engage': 0.40, 'anti_melee': 0.90},
    'Illaoi': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.30, 'durability': 0.85, 'engage': 0.25, 'anti_melee': 1.00},
    'Irelia': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.60, 'durability': 0.65, 'engage': 0.75, 'anti_melee': 0.60},
    'Jax': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.75, 'durability': 0.75, 'engage': 0.70, 'anti_melee': 0.85},
    'Jayce': {'lane': 'top', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.45, 'engage': 0.40, 'anti_melee': 0.40},
    'K\'Sante': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.90, 'durability': 0.95, 'engage': 0.85, 'anti_melee': 0.85},
    'Kayle': {'lane': 'top', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.20, 'durability': 0.40, 'engage': 0.20, 'anti_melee': 0.50},
    'Kennen': {'lane': 'top', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.45, 'engage': 0.95, 'anti_melee': 0.75},
    'Kled': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.65, 'durability': 0.75, 'engage': 0.90, 'anti_melee': 0.65},
    'Malphite': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.95, 'engage': 1.00, 'anti_melee': 0.90},
    'Mordekaiser': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.85, 'engage': 0.60, 'anti_melee': 0.95},
    'Nasus': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.85, 'engage': 0.30, 'anti_melee': 0.80},
    'Olaf': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.75, 'engage': 0.65, 'anti_melee': 0.85},
    'Ornn': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.95, 'engage': 0.95, 'anti_melee': 0.80},
    'Poppy': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.90, 'durability': 0.85, 'engage': 0.75, 'anti_melee': 0.90},
    'Quinn': {'lane': 'top', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.35, 'engage': 0.40, 'anti_melee': 0.35},
    'Renekton': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.80, 'engage': 0.70, 'anti_melee': 0.75},
    'Riven': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.65, 'engage': 0.70, 'anti_melee': 0.70},
    'Rumble': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.40, 'durability': 0.60, 'engage': 0.75, 'anti_melee': 0.80},
    'Sett': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.80, 'durability': 0.85, 'engage': 0.80, 'anti_melee': 0.90},
    'Shen': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.85, 'engage': 0.75, 'anti_melee': 0.80},
    'Sion': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.95, 'engage': 0.80, 'anti_melee': 0.75},
    'Tahm Kench': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.95, 'engage': 0.65, 'anti_melee': 0.80},
    'Urgot': {'lane': 'top', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.80, 'engage': 0.60, 'anti_melee': 0.85},
    'Volibear': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.85, 'engage': 0.75, 'anti_melee': 0.85},
    'Yone': {'lane': 'top', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.80, 'durability': 0.55, 'engage': 0.85, 'anti_melee': 0.65},

    # Đi Rừng (Jungle)
    'Amumu': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.85, 'engage': 0.95, 'anti_melee': 0.75},
    'Bel\'Veth': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.65, 'durability': 0.65, 'engage': 0.70, 'anti_melee': 0.65},
    'Brand': {'lane': 'jungle', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.60, 'durability': 0.40, 'engage': 0.45, 'anti_melee': 0.95},
    'Elise': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.45, 'engage': 0.65, 'anti_melee': 0.50},
    'Graves': {'lane': 'jungle', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.25, 'durability': 0.60, 'engage': 0.40, 'anti_melee': 0.70},
    'Hecarim': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.75, 'durability': 0.75, 'engage': 0.90, 'anti_melee': 0.70},
    'Jarvan IV': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.75, 'engage': 0.95, 'anti_melee': 0.65},
    'Karthus': {'lane': 'jungle', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.15, 'durability': 0.35, 'engage': 0.25, 'anti_melee': 0.85},
    'Kayn': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.60, 'durability': 0.65, 'engage': 0.70, 'anti_melee': 0.65},
    'Kindred': {'lane': 'jungle', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.30, 'durability': 0.45, 'engage': 0.35, 'anti_melee': 0.50},
    'Lee Sin': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.75, 'durability': 0.65, 'engage': 0.85, 'anti_melee': 0.60},
    'Lillia': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.55, 'engage': 0.80, 'anti_melee': 0.80},
    'Master Yi': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.00, 'durability': 0.45, 'engage': 0.30, 'anti_melee': 0.60},
    'Maokai': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.85, 'engage': 0.90, 'anti_melee': 0.80},
    'Naafiri': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.50, 'engage': 0.70, 'anti_melee': 0.50},
    'Nidalee': {'lane': 'jungle', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.10, 'durability': 0.40, 'engage': 0.35, 'anti_melee': 0.30},
    'Nocturne': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.60, 'engage': 0.95, 'anti_melee': 0.55},
    'Nunu & Willump': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.85, 'engage': 0.85, 'anti_melee': 0.70},
    'Pantheon': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.70, 'engage': 0.85, 'anti_melee': 0.70},
    'Rammus': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.95, 'engage': 0.90, 'anti_melee': 0.95},
    'Rek\'Sai': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.75, 'durability': 0.70, 'engage': 0.80, 'anti_melee': 0.60},
    'Rengar': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.45, 'durability': 0.50, 'engage': 0.75, 'anti_melee': 0.45},
    'Sejuani': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.95, 'engage': 0.95, 'anti_melee': 0.80},
    'Skarner': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.95, 'durability': 0.90, 'engage': 0.90, 'anti_melee': 0.80},
    'Trundle': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.60, 'durability': 0.85, 'engage': 0.50, 'anti_melee': 0.95},
    'Vi': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.95, 'durability': 0.75, 'engage': 0.95, 'anti_melee': 0.70},
    'Volibear': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.85, 'engage': 0.75, 'anti_melee': 0.85},
    'Warwick': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.80, 'durability': 0.75, 'engage': 0.85, 'anti_melee': 0.80},
    'Wukong': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.90, 'durability': 0.70, 'engage': 0.90, 'anti_melee': 0.65},
    'Xin Zhao': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.75, 'engage': 0.85, 'anti_melee': 0.75},
    'Zac': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.90, 'engage': 0.95, 'anti_melee': 0.80},

    # Đường Giữa (Mid)
    'Ahri': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.45, 'engage': 0.80, 'anti_melee': 0.85},
    'Akali': {'lane': 'mid', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.30, 'durability': 0.50, 'engage': 0.80, 'anti_melee': 0.80},
    'Akshan': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.45, 'engage': 0.50, 'anti_melee': 0.45},
    'Anivia': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.45, 'engage': 0.40, 'anti_melee': 0.95},
    'Annie': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.40, 'engage': 0.85, 'anti_melee': 0.80},
    'Aurelion Sol': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.45, 'engage': 0.60, 'anti_melee': 0.70},
    'Aurora': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.45, 'engage': 0.80, 'anti_melee': 0.75},
    'Azir': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.45, 'engage': 0.75, 'anti_melee': 0.90},
    'Cassiopeia': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.45, 'engage': 0.70, 'anti_melee': 0.95},
    'Galio': {'lane': 'mid', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.85, 'engage': 0.90, 'anti_melee': 0.80},
    'Hwei': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.40, 'engage': 0.60, 'anti_melee': 0.85},
    'LeBlanc': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.65, 'durability': 0.35, 'engage': 0.80, 'anti_melee': 0.65},
    'Lissandra': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.50, 'engage': 0.90, 'anti_melee': 0.95},
    'Malzahar': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.40, 'engage': 0.65, 'anti_melee': 0.90},
    'Mel': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.70, 'durability': 0.40, 'engage': 0.60, 'anti_melee': 0.70},
    'Neeko': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.40, 'engage': 0.90, 'anti_melee': 0.80},
    'Orianna': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.40, 'engage': 0.85, 'anti_melee': 0.75},
    'Ryze': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.55, 'engage': 0.65, 'anti_melee': 0.75},
    'Sylas': {'lane': 'mid', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.70, 'durability': 0.60, 'engage': 0.80, 'anti_melee': 0.70},
    'Syndra': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.35, 'engage': 0.70, 'anti_melee': 0.85},
    'Taliyah': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.40, 'engage': 0.65, 'anti_melee': 0.85},
    'Twisted Fate': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.40, 'engage': 0.75, 'anti_melee': 0.50},
    'Veigar': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.40, 'engage': 0.50, 'anti_melee': 0.85},
    'Vex': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.50, 'engage': 0.85, 'anti_melee': 0.90},
    'Viktor': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.65, 'durability': 0.45, 'engage': 0.55, 'anti_melee': 0.70},
    'Vladmir': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.20, 'durability': 0.65, 'engage': 0.45, 'anti_melee': 0.75},
    'Xerath': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.30, 'engage': 0.50, 'anti_melee': 0.60},
    'Yasuo': {'lane': 'mid', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.55, 'engage': 0.75, 'anti_melee': 0.65},
    'Yone': {'lane': 'mid', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.80, 'durability': 0.55, 'engage': 0.85, 'anti_melee': 0.65},
    'Zed': {'lane': 'mid', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.45, 'engage': 0.60, 'anti_melee': 0.40},
    'Zoe': {'lane': 'mid', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.75, 'durability': 0.35, 'engage': 0.50, 'anti_melee': 0.40},

    # Đường Dưới / Xạ Thủ (Bot)
    'Aphelios': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.50, 'durability': 0.40, 'engage': 0.45, 'anti_melee': 0.55},
    'Ashe': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.35, 'engage': 0.85, 'anti_melee': 0.50},
    'Caitlyn': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.45, 'durability': 0.35, 'engage': 0.30, 'anti_melee': 0.45},
    'Draven': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.45, 'engage': 0.35, 'anti_melee': 0.50},
    'Ezreal': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.10, 'durability': 0.45, 'engage': 0.20, 'anti_melee': 0.35},
    'Jhin': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.35, 'engage': 0.65, 'anti_melee': 0.40},
    'Jinx': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.50, 'durability': 0.35, 'engage': 0.30, 'anti_melee': 0.45},
    'Kai\'Sa': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.15, 'durability': 0.45, 'engage': 0.70, 'anti_melee': 0.50},
    'Kalista': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.40, 'engage': 0.80, 'anti_melee': 0.55},
    'Kog\'Maw': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.35, 'engage': 0.20, 'anti_melee': 0.60},
    'Lucian': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.10, 'durability': 0.45, 'engage': 0.40, 'anti_melee': 0.45},
    'Miss Fortune': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.35, 'durability': 0.35, 'engage': 0.60, 'anti_melee': 0.50},
    'Samira': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.50, 'durability': 0.50, 'engage': 0.75, 'anti_melee': 0.60},
    'Senna': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.65, 'durability': 0.35, 'engage': 0.50, 'anti_melee': 0.45},
    'Sivir': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.10, 'durability': 0.40, 'engage': 0.45, 'anti_melee': 0.50},
    'Smolder': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.40, 'engage': 0.30, 'anti_melee': 0.50},
    'Tristana': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.40, 'durability': 0.45, 'engage': 0.50, 'anti_melee': 0.45},
    'Twitch': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.30, 'engage': 0.40, 'anti_melee': 0.40},
    'Varus': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.80, 'durability': 0.35, 'engage': 0.75, 'anti_melee': 0.50},
    'Vayne': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.60, 'durability': 0.40, 'engage': 0.30, 'anti_melee': 0.65},
    'Xayah': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.70, 'durability': 0.45, 'engage': 0.40, 'anti_melee': 0.75},
    'Zeri': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AD', 'hard_cc': 0.20, 'durability': 0.45, 'engage': 0.65, 'anti_melee': 0.50},
    'Ziggs': {'lane': 'bot', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.55, 'durability': 0.35, 'engage': 0.40, 'anti_melee': 0.65},

    # Hỗ Trợ (Support) & Tướng Đa Năng
    'Alistar': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.95, 'engage': 0.95, 'anti_melee': 0.85},
    'Bard': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.50, 'engage': 0.85, 'anti_melee': 0.60},
    'Blitzcrank': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.75, 'engage': 0.95, 'anti_melee': 0.65},
    'Braum': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.95, 'engage': 0.75, 'anti_melee': 0.95},
    'Janna': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.40, 'engage': 0.40, 'anti_melee': 0.95},
    'Karma': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.60, 'durability': 0.50, 'engage': 0.55, 'anti_melee': 0.65},
    'Leona': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 1.00, 'durability': 0.95, 'engage': 1.00, 'anti_melee': 0.80},
    'Lulu': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.45, 'engage': 0.45, 'anti_melee': 0.90},
    'Milio': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.60, 'durability': 0.40, 'engage': 0.40, 'anti_melee': 0.85},
    'Nami': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.40, 'engage': 0.75, 'anti_melee': 0.75},
    'Nautilus': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 1.00, 'durability': 0.90, 'engage': 1.00, 'anti_melee': 0.80},
    'Pyke': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.85, 'durability': 0.45, 'engage': 0.90, 'anti_melee': 0.45},
    'Rakan': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.65, 'engage': 1.00, 'anti_melee': 0.70},
    'Rell': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.90, 'engage': 1.00, 'anti_melee': 0.80},
    'Renata Glasc': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.90, 'durability': 0.50, 'engage': 0.75, 'anti_melee': 0.95},
    'Seraphine': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.45, 'engage': 0.85, 'anti_melee': 0.80},
    'Tahm Kench': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.80, 'durability': 0.95, 'engage': 0.70, 'anti_melee': 0.90},
    'Taric': {'lane': 'support', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.85, 'durability': 0.90, 'engage': 0.65, 'anti_melee': 0.95},
    'Thresh': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.70, 'engage': 0.90, 'anti_melee': 0.80},
    'Yuumi': {'lane': 'support', 'is_melee': False, 'dmg_type': 'AP', 'hard_cc': 0.65, 'durability': 0.35, 'engage': 0.50, 'anti_melee': 0.60},
    'Maokai': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AP', 'hard_cc': 0.95, 'durability': 0.90, 'engage': 0.95, 'anti_melee': 0.85},
    'Skarner': {'lane': 'jungle', 'is_melee': True, 'dmg_type': 'AD', 'hard_cc': 0.95, 'durability': 0.95, 'engage': 0.95, 'anti_melee': 0.85}
}

# Lane synergy pairs (Cặp đôi tương thích kinh điển Pro Play & Solo Rank)
# Synergy is estimated from observed teammate pairs in HistoricalRecommender.
DUO_SYNERGIES = {}


# =========================================================================
# ĐỊNH NGHĨA BỐI CẢNH KHU VỰC & GIẢI ĐẤU QUỐC TẾ (REGIONAL & INTERNATIONAL CONTEXT)
# =========================================================================
REGIONAL_PROFILES = {
    'ALL': {
        'label': 'Toàn Cầu (All Leagues)',
        'leagues': ['LCK', 'LPL', 'LCP', 'WLDS', 'MSI', 'EWC'],
        'style_dna': 'Tổng hợp toàn bộ Meta Đấu Giải Chuyên Nghiệp Đỉnh Cao 2026',
        'blend_weight': 1.0
    },
    'LCK': {
        'label': 'LCK (Hàn Quốc)',
        'leagues': ['LCK'],
        'style_dna': 'Kiểm soát Vĩ mô, Cấu rỉa & Giao tranh Mục tiêu Chuẩn chỉ (Macro Control & Objective Setup)',
        'blend_weight': 0.78
    },
    'LPL': {
        'label': 'LPL (Trung Quốc)',
        'leagues': ['LPL'],
        'style_dna': 'Giao tranh Cường độ cao, Băng trụ sớm & Đè đường Áp lực (High-Tempo Skirmish & Dive)',
        'blend_weight': 0.80
    },
    'LCP': {
        'label': 'LCP (Châu Á - Thái Bình Dương / VCS-PCS)',
        'leagues': ['LCP'],
        'style_dna': 'Giao tranh Rừng Sớm & Đột biến Tướng Tủ Thuận Tay (Jungle Tempo & Pocket Aggression)',
        'blend_weight': 0.72
    },
    'INTERNATIONAL': {
        'label': 'Giải Quốc Tế (CKTG WLDS + MSI + EWC)',
        'leagues': ['WLDS', 'MSI', 'EWC'],
        'style_dna': 'Va chạm Meta Đa Khu vực & Cấm Tôn Trọng Xuyên Quốc Gia (Cross-Region Clash & Respect Bans)',
        'blend_weight': 0.78
    },
    'WLDS': {
        'label': 'CKTG / Worlds (WLDS)',
        'leagues': ['WLDS'],
        'style_dna': 'Đỉnh cao Chung Kết Thế Giới - Meta Hội tụ, Bản lĩnh Bo5 & Cấm Tôn Trọng Tuyệt Đối',
        'blend_weight': 0.75
    },
    'MSI': {
        'label': 'Mid-Season Invitational (MSI)',
        'leagues': ['MSI'],
        'style_dna': 'Giao tranh Giữa Mùa Giải - Đấu trí Fearless/Bo5 Xuyên Khu vực LCK vs LPL',
        'blend_weight': 0.72
    },
    'EWC': {
        'label': 'Esports World Cup (EWC)',
        'leagues': ['EWC'],
        'style_dna': 'Giải Quốc Tế Nhịp Độ Nhanh - Đột biến Cấm/Chọn & Giao tranh Sớm',
        'blend_weight': 0.72
    }
}


def normalize_region_code(region: str = 'ALL') -> str:
    if not region:
        return 'ALL'
    r = str(region).strip().upper()
    alias_map = {
        'WORLDS': 'WLDS', 'CKTG': 'WLDS', 'WORLD': 'WLDS', 'WLDS': 'WLDS',
        'INT': 'INTERNATIONAL', 'INTER': 'INTERNATIONAL', 'QUOCTE': 'INTERNATIONAL',
        'VCS': 'LCP', 'PCS': 'LCP', 'APAC': 'LCP',
        'KR': 'LCK', 'CN': 'LPL', 'GLOBAL': 'ALL'
    }
    r = alias_map.get(r, r)
    return r if r in REGIONAL_PROFILES else 'ALL'


# =========================================================================
# 2. PHÂN HỆ 1: TARGET BAN ENGINE (CẤM LAI GHÉP THEO TUYỂN THỦ & KHU VỰC)
# =========================================================================
class TargetBanEngine:
    """
    Phân hệ CẤM Lai Ghép mục tiêu theo Tuyển thủ Đối phương & Đặc thù Khu vực / Giải đấu:
    - Phân tầng theo khu vực: LCK, LPL, LCP, và Giải Quốc Tế (MSI, CKTG/WLDS, EWC)
    - 60-70% Trọng số Đấu Giải: Lịch sử 30,000 bản ghi tournament_players (Bayesian Winrate + Laning Dominance)
    - 30-40% Trọng số Solo Rank Gần Nhất: Quét pro_player_accounts.json phát hiện Pocket Pick spam rank
    """
    def __init__(self, db_path: Path = DB_PATH, accounts_path: Path = PRO_ACCOUNTS_PATH):
        self.db_path = db_path
        self.accounts_path = accounts_path
        self.pro_accounts = self._load_pro_accounts()
        self.player_stats_cache = {}
        self.regional_bans_cache = {}
        self._build_player_stats_cache()

    def _load_pro_accounts(self) -> Dict[str, Any]:
        if self.accounts_path.exists():
            with open(self.accounts_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('players', {})
        return {}

    def _build_player_stats_cache(self):
        """Khai thác CSDL SQLite tính toán Bayesian Winrate, Dominance và Tần suất Cấm theo từng Khu vực / Giải đấu"""
        if not self.db_path.exists():
            return
        conn = open_clean_connection(self.db_path)
        query = """
        SELECT playername, champion, position,
               COUNT(*) as games,
               SUM(CASE WHEN result = 1 THEN 1 ELSE 0 END) as wins,
               AVG(COALESCE(golddiffat10, 0)) as avg_gd10,
               AVG(COALESCE(csdiffat10, 0)) as avg_csd10,
               AVG(COALESCE(kills, 0)) as avg_kills,
               AVG(COALESCE(deaths, 0)) as avg_deaths,
               AVG(COALESCE(assists, 0)) as avg_assists,
               AVG(COALESCE(dpm, 500)) as avg_dpm
        FROM tournament_players
        WHERE playername IS NOT NULL AND champion IS NOT NULL
          AND 1=1
        GROUP BY playername, champion
        """
        df = pd.read_sql(query, conn)
        conn.close()

        # Tính tổng số trận của mỗi tuyển thủ
        player_totals = df.groupby('playername')['games'].sum().to_dict()

        for _, row in df.iterrows():
            player = row['playername']
            champ = row['champion']
            games = row['games']
            wins = row['wins']
            total_player_games = player_totals.get(player, games)

            # 1. Tần suất chọn của tuyển thủ (Pick Share)
            pick_share = games / max(1, total_player_games)

            # 2. Bayesian Smoothed Winrate: (Wins + C * Global_WR) / (Games + C)
            C = 5.0
            global_wr = 0.50
            bayes_winrate = (wins + C * global_wr) / (games + C)

            # 3. Laning Dominance Score 10m
            gd10 = row['avg_gd10']
            csd10 = row['avg_csd10']
            dominance_score = (gd10 / 500.0) + (csd10 / 15.0)  # Chuẩn hóa về tầm -1.0 đến +1.0
            dominance_score = np.clip(dominance_score, -1.0, 1.5)

            # 4. KDA Score
            deaths = max(1.0, row['avg_deaths'])
            kda = (row['avg_kills'] + row['avg_assists']) / deaths

            # Tournament Threat Index (TTI)
            tti = (0.35 * min(1.0, pick_share * 3.5)) + (0.35 * bayes_winrate) + (0.20 * max(0.0, (dominance_score + 1.0) / 2.5)) + (0.10 * min(1.0, kda / 6.0))

            if player not in self.player_stats_cache:
                self.player_stats_cache[player] = {}

            self.player_stats_cache[player][champ] = {
                'games': int(games),
                'wins': int(wins),
                'winrate': round(wins / games, 3),
                'bayes_winrate': round(bayes_winrate, 3),
                'pick_share': round(pick_share, 3),
                'avg_gd10': round(gd10, 1),
                'avg_csd10': round(csd10, 1),
                'kda': round(kda, 2),
                'tti': round(float(tti), 4)
            }

        # 5. Khai thác Tần suất Bị Cấm Thực Tế Phân Chia Theo Đúng Phase 1 vs Phase 2 VÀ THEO TỪNG KHU VỰC / GIẢI ĐẤU
        conn = open_clean_connection(self.db_path)
        phase_ban_query = """
        SELECT 
            UPPER(b.league) as league,
            b.ban_champ,
            SUM(CASE WHEN b.slot IN ('ban1','ban2','ban3') THEN 1 ELSE 0 END) as p1_bans,
            SUM(CASE WHEN b.slot IN ('ban4','ban5') THEN 1 ELSE 0 END) as p2_bans,
            COUNT(*) as total_bans
        FROM (
            SELECT league, ban1 as ban_champ, 'ban1' as slot FROM tournament_matches WHERE 1=1 AND ban1 IS NOT NULL AND ban1 != ''
            UNION ALL SELECT league, ban2, 'ban2' FROM tournament_matches WHERE 1=1 AND ban2 IS NOT NULL AND ban2 != ''
            UNION ALL SELECT league, ban3, 'ban3' FROM tournament_matches WHERE 1=1 AND ban3 IS NOT NULL AND ban3 != ''
            UNION ALL SELECT league, ban4, 'ban4' FROM tournament_matches WHERE 1=1 AND ban4 IS NOT NULL AND ban4 != ''
            UNION ALL SELECT league, ban5, 'ban5' FROM tournament_matches WHERE 1=1 AND ban5 IS NOT NULL AND ban5 != ''
        ) b
        GROUP BY UPPER(b.league), b.ban_champ
        """
        phase_df = pd.read_sql(phase_ban_query, conn)
        league_counts_df = pd.read_sql(
            "SELECT UPPER(league) as league, COUNT(*) as cnt FROM tournament_matches WHERE 1=1 GROUP BY UPPER(league)",
            conn
        )
        conn.close()

        league_team_rows = dict(zip(league_counts_df['league'], league_counts_df['cnt']))

        # Xây dựng cache cấm cho từng khu vực trong REGIONAL_PROFILES
        self.regional_bans_cache = {}
        for reg_code, reg_info in REGIONAL_PROFILES.items():
            target_lgs = [lg.upper() for lg in reg_info['leagues']]
            sub_df = phase_df[phase_df['league'].isin(target_lgs)]
            if not sub_df.empty:
                agg_df = sub_df.groupby('ban_champ', as_index=False).agg(
                    p1_bans=('p1_bans', 'sum'),
                    p2_bans=('p2_bans', 'sum'),
                    total_bans=('total_bans', 'sum')
                )
                p1_dict = dict(zip(agg_df['ban_champ'], agg_df['p1_bans']))
                p2_dict = dict(zip(agg_df['ban_champ'], agg_df['p2_bans']))
                tot_dict = dict(zip(agg_df['ban_champ'], agg_df['total_bans']))
            else:
                p1_dict, p2_dict, tot_dict = {}, {}, {}

            tot_rows = sum(league_team_rows.get(lg, 0) for lg in target_lgs)
            self.regional_bans_cache[reg_code] = {
                'p1_bans': p1_dict,
                'p2_bans': p2_dict,
                'total_bans': tot_dict,
                'max_p1': max(p1_dict.values()) if p1_dict else 1,
                'max_p2': max(p2_dict.values()) if p2_dict else 1,
                'max_total': max(tot_dict.values()) if tot_dict else 1,
                'total_matches': max(1, tot_rows)
            }

        # Giữ tương thích ngược cho thuộc tính cấp ALL
        all_cache = self.regional_bans_cache['ALL']
        self.tournament_phase1_bans = all_cache['p1_bans']
        self.tournament_phase2_bans = all_cache['p2_bans']
        self.tournament_ban_counts = all_cache['total_bans']
        self.max_phase1_bans = all_cache['max_p1']
        self.max_phase2_bans = all_cache['max_p2']
        self.max_ban_count = all_cache['max_total']
        self.total_matches = all_cache['total_matches']

    def _get_region_ban_data(self, region: str = 'ALL') -> Dict[str, Any]:
        reg_code = normalize_region_code(region)
        if not hasattr(self, 'regional_bans_cache') or not self.regional_bans_cache:
            self._build_player_stats_cache()
        return self.regional_bans_cache.get(reg_code, self.regional_bans_cache.get('ALL'))

    def get_pro_tournament_meta_bans(self, top_k: int = 10, ban_phase: int = 1, region: str = 'ALL') -> List[Dict[str, Any]]:
        """Lấy danh sách Top tướng bị cấm nhiều nhất phân chia theo đúng Phase 1 vs Phase 2 và theo Khu vực / Giải đấu"""
        reg_code = normalize_region_code(region)
        reg_cache = self._get_region_ban_data(reg_code)
        reg_label = REGIONAL_PROFILES[reg_code]['label']

        ban_dict = reg_cache['p1_bans'] if ban_phase == 1 else reg_cache['p2_bans']
        tot_matches = reg_cache['total_matches']

        sorted_bans = sorted(ban_dict.items(), key=lambda x: x[1], reverse=True)
        results = []
        for champ, count in sorted_bans:
            if not champ or champ.lower() in ["none", "null", "locke", "noban"]:
                continue
            ban_rate = (count / max(1, tot_matches // 2)) * 100.0
            p1_c = reg_cache['p1_bans'].get(champ, 0)
            p2_c = reg_cache['p2_bans'].get(champ, 0)
            phase_label = f"Phase {ban_phase} ({count} lượt cấm - {round(ban_rate, 1)}%)"
            results.append({
                'champion': champ,
                'region': reg_code,
                'ban_count': count,
                'phase1_bans': p1_c,
                'phase2_bans': p2_c,
                'ban_rate': round(ban_rate, 1),
                'historical_ban': evidence(count, max(1, tot_matches // 2)),
                'score_kind': 'historical_ban_frequency',
                'reason': f"Top cấm [{reg_label}] {phase_label}"
            })
            if len(results) >= top_k:
                break
        return results

    def link_player_account(self, player_name: str, riot_id: str, server: str = "KR", tier: str = "Challenger") -> bool:
        """Đăng ký / Cập nhật Riot ID cho tuyển thủ mới"""
        self.pro_accounts[player_name] = {
            "riot_id": riot_id,
            "server": server,
            "tier": tier,
            "team": "Registered",
            "position": "All",
            "recent_rank_matches": 30,
            "recent_rank_picks": {}
        }
        with open(self.accounts_path, 'w', encoding='utf-8') as f:
            json.dump({"version": "1.0", "players": self.pro_accounts}, f, indent=2, ensure_ascii=False)
        return True

    def recommend_target_bans(self, player_name, top_k=5, tournament_weight=.65, ban_phase=1, region='ALL'):
        hist=HistoricalRecommender(self.db_path)
        players=hist.region_players(normalize_region_code(region))
        players=players[players.playername.eq(player_name)]
        total=len(players)
        result=[]
        for champ,g in players.groupby('champion'):
            n=len(g);w=int(g.result.sum())
            ev=evidence(w,n)
            score=(n/max(total,1))*((w+5)/(n+10))
            result.append({'champion':champ,'threat_score':score,'ranking_score':100*score,
                           'score_kind':'historical_heuristic_points','historical':ev,
                           'badge':'LỊCH SỬ TUYỂN THỦ','tournament_stats':f'{w}/{n} thắng; CI95 {ev["ci95_wilson"]}',
                           'rank_stats':'Chưa có lịch sử rank được kiểm chứng cho tài khoản liên kết',
                           'reason':f'{player_name}: đã chọn {n}/{total} trận; không ước lượng lợi ích của lượt cấm'})
        return sorted(result,key=lambda x:(-x['threat_score'],x['champion']))[:top_k]


    def recommend_team_bans(self, enemy_roster, top_k=5, ban_phase=1, already_banned=None, region='ALL'):
        excluded=set(already_banned or [])
        result={}
        for role,player in (enemy_roster or {}).items():
            for item in self.recommend_target_bans(player,top_k=100,region=region):
                champ=item['champion']
                if champ in excluded: continue
                candidate={**item,'priority_pct':item['threat_score']*100,
                           'player_target':player,'player_role':role,'region':normalize_region_code(region)}
                if champ not in result or candidate['threat_score']>result[champ]['threat_score']:
                    result[champ]=candidate
        if not result:
            for item in self.get_pro_tournament_meta_bans(top_k=100,ban_phase=ban_phase,region=region):
                if item['champion'] not in excluded:
                    result[item['champion']]={**item,'priority_pct':item['ban_rate'],
                                             'score_kind':'historical_ban_frequency_points',
                                             'player_target':None,'player_role':None}
        return sorted(result.values(),key=lambda x:(-x['priority_pct'],x['champion']))[:top_k]


    def recommend_enabling_bans(self, intended_pick, enemy_roster=None, top_k=4, already_banned=None, region='ALL'):
        hist=HistoricalRecommender(self.db_path)
        rows=hist.counters(intended_pick,top_k=100,region=normalize_region_code(region))['counters']
        excluded=set(already_banned or [])
        return [{**r,'priority_pct':r['score']*100,'counter_for':intended_pick,
                 'reason':f"Lịch sử đối đầu {intended_pick}: {r['games']} trận; chưa chứng minh lợi ích nhân quả của lượt cấm",
                 'ban_count':self.tournament_ban_counts.get(r['champion'],0),
                 'ban_rate':100*self.tournament_ban_counts.get(r['champion'],0)/max(1,self.total_matches//2)}
                for r in rows if r['champion'] not in excluded][:top_k]


    def get_solo_queue_meta_bans(self, top_k: int = 10) -> List[Dict[str, Any]]:
        """Lấy danh sách Top tướng bị cấm nhiều nhất 100% từ CSDL Solo Queue Rank (matches_10min)"""
        if not self.db_path.exists():
            return []
        try:
            conn = open_clean_connection(self.db_path)
            df = pd.read_sql("SELECT blueBans, redBans FROM matches_10min", conn)
            conn.close()

            ban_counter = Counter()
            for col in ['blueBans', 'redBans']:
                for bans_str in df[col].dropna():
                    champs = [c.strip() for c in str(bans_str).split(',') if c.strip()]
                    ban_counter.update(champs)

            total_matches = len(df)
            results = []
            for champ, count in ban_counter.most_common(top_k * 2):
                if champ and champ.lower() not in ["none", "null", "locke"]:
                    ban_rate = (count / max(1, total_matches)) * 100.0
                    results.append({
                        'champion': champ,
                        'ban_count': count,
                        'ban_rate': round(ban_rate, 1),
                        'reason': f"Top cấm Solo Queue ({count} lượt cấm - {round(ban_rate, 1)}%)"
                    })
                if len(results) >= top_k:
                    break
            return results
        except Exception as e:
            return []



# =========================================================================
# 2. PHÂN HỆ 2: META PICK & SYNERGY RECOMMENDER (CHỌN THEO META & ĐỘI HÌNH)
# =========================================================================
class MetaPickRecommender:
    """
    Phân hệ CHỌN Tướng Chuẩn Meta & Tương Thích Đội Hình:
    - Meta Presence: Khai thác tần suất xuất hiện và độ ưu tiên trong 30,000 trận Đấu Giải
    - Duo Synergy: Tương thích cặp đôi Bot-Support (Ashe-Seraphine, Lucian-Nami, Kalista-Renata), Mid-Jungle (Ahri-Vi, Orianna-J4)
    - Counter-Pick: Khắc chế trực tiếp tướng đối phương cùng lane
    - Composition Balance: Bù đắp thiếu hụt Sát thương phép (AP), Khống chế cứng (Hard CC), Chống chịu (Frontline)
    """
    def __init__(self, db_path: Path = DB_PATH, accounts_path: Path = PRO_ACCOUNTS_PATH):
        self.metadata = CHAMPION_METADATA
        self.duo_synergies = {}  # HistoricalRecommender computes observed pairs
        self.db_path = db_path
        self.accounts_path = accounts_path
        self.tournament_meta_picks = {}
        self.player_stats_cache = {}
        self.matchup_cache = {}
        self._load_tournament_meta_popularity()
        self._load_head_to_head_matchups()

    def _normalize_champion_name(self, raw_name: str) -> str:
        """Chuẩn hóa tên tướng giữa Solo Queue và Pro Play"""
        if not raw_name or not isinstance(raw_name, str):
            return ""
        raw_str = raw_name.strip()
        if raw_str in self.metadata:
            return raw_str
        clean_k = re.sub(r'[^a-zA-Z0-9]', '', raw_str).lower()
        for meta_name in self.metadata:
            if re.sub(r'[^a-zA-Z0-9]', '', meta_name).lower() == clean_k:
                return meta_name
        aliases = {
            'monkeyking': 'Wukong',
            'nunu': 'Nunu & Willump',
            'renata': 'Renata Glasc',
            'chogath': "Cho'Gath",
            'drmundo': "Dr. Mundo",
            'kaisa': "Kai'Sa",
            'ksante': "K'Sante",
            'kogmaw': "Kog'Maw",
            'reksai': "Rek'Sai",
            'velkoz': "Vel'Koz",
            'masteryi': 'Master Yi',
            'jarvaniv': 'Jarvan IV',
            'leesin': 'Lee Sin',
            'xinzhao': 'Xin Zhao',
            'missfortune': 'Miss Fortune',
            'twistedfate': 'Twisted Fate',
            'aurelionsol': 'Aurelion Sol',
            'tahmkench': 'Tahm Kench'
        }
        return aliases.get(clean_k, raw_str)

    def _load_tournament_meta_popularity(self):
        """Khai thác tần suất cấm chọn thực tế từ CSDL SQLite (Đấu Giải theo từng Khu Vực + Solo Rank) để xác định Meta Tier theo từng vị trí & Khu vực"""
        self.regional_meta_picks = {reg: {} for reg in REGIONAL_PROFILES}
        self.regional_macro_stats = {}
        if not self.db_path.exists():
            return
        try:
            conn = open_clean_connection(self.db_path)
            # 1. Đấu Giải Pro Play theo từng Giải đấu (LCK, LPL, LCP, WLDS, MSI, EWC)
            query_tour = """
            SELECT UPPER(league) as league, position, champion, COUNT(*) as picks, AVG(result) as winrate
            FROM tournament_players
            WHERE position IS NOT NULL AND champion IS NOT NULL
              AND 1=1
            GROUP BY UPPER(league), position, champion
            """
            df_tour = pd.read_sql(query_tour, conn)

            # Macro stats per league
            query_macro = """
            SELECT UPPER(league) as league,
                   COUNT(DISTINCT gameid) as games,
                   ROUND(AVG(gamelength)/60.0, 2) as avg_duration_min,
                   ROUND(AVG(ckpm), 2) as avg_ckpm,
                   ROUND(AVG(CASE WHEN side = 'Blue' THEN result END)*100.0, 1) as blue_winrate_pct
            FROM tournament_matches
            GROUP BY UPPER(league)
            """
            df_macro = pd.read_sql(query_macro, conn)

            # 2. Solo Queue Rank (matches_10min)
            query_rank = """
            SELECT 'top' as position, blueTop as champion, COUNT(*) as picks, AVG(blueWins) as winrate FROM matches_10min WHERE blueTop IS NOT NULL GROUP BY blueTop
            UNION ALL
            SELECT 'top' as position, redTop as champion, COUNT(*) as picks, AVG(1 - blueWins) as winrate FROM matches_10min WHERE redTop IS NOT NULL GROUP BY redTop
            UNION ALL
            SELECT 'jng' as position, blueJungle as champion, COUNT(*) as picks, AVG(blueWins) as winrate FROM matches_10min WHERE blueJungle IS NOT NULL GROUP BY blueJungle
            UNION ALL
            SELECT 'jng' as position, redJungle as champion, COUNT(*) as picks, AVG(1 - blueWins) as winrate FROM matches_10min WHERE redJungle IS NOT NULL GROUP BY redJungle
            UNION ALL
            SELECT 'mid' as position, blueMid as champion, COUNT(*) as picks, AVG(blueWins) as winrate FROM matches_10min WHERE blueMid IS NOT NULL GROUP BY blueMid
            UNION ALL
            SELECT 'mid' as position, redMid as champion, COUNT(*) as picks, AVG(1 - blueWins) as winrate FROM matches_10min WHERE redMid IS NOT NULL GROUP BY redMid
            UNION ALL
            SELECT 'bot' as position, blueAdc as champion, COUNT(*) as picks, AVG(blueWins) as winrate FROM matches_10min WHERE blueAdc IS NOT NULL GROUP BY blueAdc
            UNION ALL
            SELECT 'bot' as position, redAdc as champion, COUNT(*) as picks, AVG(1 - blueWins) as winrate FROM matches_10min WHERE redAdc IS NOT NULL GROUP BY redAdc
            UNION ALL
            SELECT 'sup' as position, blueSupport as champion, COUNT(*) as picks, AVG(blueWins) as winrate FROM matches_10min WHERE blueSupport IS NOT NULL GROUP BY blueSupport
            UNION ALL
            SELECT 'sup' as position, redSupport as champion, COUNT(*) as picks, AVG(1 - blueWins) as winrate FROM matches_10min WHERE redSupport IS NOT NULL GROUP BY redSupport
            """
            df_rank = pd.read_sql(query_rank, conn)
            conn.close()

            df_tour['champion'] = df_tour['champion'].apply(lambda c: self._normalize_champion_name(c))
            df_tour['position'] = df_tour['position'].astype(str).str.lower()
            df_rank['champion'] = df_rank['champion'].apply(lambda c: self._normalize_champion_name(c))

            rank_dict = {}
            df_rank_agg = df_rank.groupby(['position', 'champion']).agg(
                rank_picks=('picks', 'sum'),
                rank_wr=('winrate', 'mean')
            ).reset_index()
            for _, row in df_rank_agg.iterrows():
                pos = str(row['position']).lower()
                champ = row['champion']
                rank_dict[(pos, champ)] = {
                    'rank_picks': int(row['rank_picks']),
                    'rank_wr': float(row['rank_wr'])
                }

            # Tính toán Meta Picks riêng biệt cho từng Khu vực / Giải đấu trong REGIONAL_PROFILES
            for reg_code, reg_info in REGIONAL_PROFILES.items():
                target_lgs = [lg.upper() for lg in reg_info['leagues']]
                sub_tour = df_tour[df_tour['league'].isin(target_lgs)]
                sub_macro = df_macro[df_macro['league'].isin(target_lgs)]

                if not sub_macro.empty:
                    tot_g = int(sub_macro['games'].sum())
                    w_dur = float((sub_macro['avg_duration_min'] * sub_macro['games']).sum() / max(1, tot_g))
                    w_ckpm = float((sub_macro['avg_ckpm'] * sub_macro['games']).sum() / max(1, tot_g))
                    w_bwr = float((sub_macro['blue_winrate_pct'] * sub_macro['games']).sum() / max(1, tot_g))
                else:
                    tot_g, w_dur, w_ckpm, w_bwr = 0, None, None, None

                self.regional_macro_stats[reg_code] = {
                    'region': reg_code,
                    'label': reg_info['label'],
                    'style_dna': reg_info['style_dna'],
                    'games': tot_g,
                    'avg_duration_min': round(w_dur, 2) if w_dur is not None else None,
                    'avg_ckpm': round(w_ckpm, 2) if w_ckpm is not None else None,
                    'blue_winrate_pct': round(w_bwr, 1) if w_bwr is not None else None
                }

                tour_dict = {}
                if not sub_tour.empty:
                    sub_agg = sub_tour.groupby(['position', 'champion'], as_index=False).apply(
                        lambda g: pd.Series({
                            'tour_picks': int(g['picks'].sum()),
                            'tour_wr': float((g['picks'] * g['winrate']).sum() / max(1, g['picks'].sum()))
                        })
                    ).reset_index()
                    for _, row in sub_agg.iterrows():
                        tour_dict[(row['position'], row['champion'])] = {
                            'tour_picks': int(row['tour_picks']),
                            'tour_wr': float(row['tour_wr'])
                        }

                all_keys = set(tour_dict.keys()).union(set(rank_dict.keys()))
                lane_max = {}
                raw_meta = {}
                for pos, champ in all_keys:
                    t_info = tour_dict.get((pos, champ), {'tour_picks': 0, 'tour_wr': 0.50})
                    r_info = rank_dict.get((pos, champ), {'rank_picks': 0, 'rank_wr': 0.50})

                    if reg_code == 'ALL':
                        total_picks = t_info['tour_picks'] + r_info['rank_picks']
                        combined_wr = (t_info['tour_picks'] * t_info['tour_wr'] + r_info['rank_picks'] * r_info['rank_wr']) / max(1, total_picks)
                    else:
                        # Với từng khu vực riêng (LCK, LPL, LCP, MSI, WLDS, EWC), ưu tiên số lượt pick thực tế tại khu vực đó
                        total_picks = t_info['tour_picks']
                        combined_wr = (t_info['tour_picks'] * t_info['tour_wr'] + 5.0 * 0.50) / (t_info['tour_picks'] + 5.0) if total_picks > 0 else 0.50

                    raw_meta[(pos, champ)] = {
                        'picks': int(total_picks),
                        'tour_picks': int(t_info['tour_picks']),
                        'rank_picks': int(r_info['rank_picks']),
                        'winrate': round(float(combined_wr), 3)
                    }
                    lane_max[pos] = max(lane_max.get(pos, 0), int(total_picks))

                for (pos, champ), data in raw_meta.items():
                    max_p = lane_max.get(pos, 50)
                    norm_pick = data['picks'] / max(1, max_p)
                    self.regional_meta_picks[reg_code][(pos, champ)] = {
                        'picks': data['picks'],
                        'tour_picks': data['tour_picks'],
                        'rank_picks': data['rank_picks'],
                        'norm_pick': norm_pick,
                        'winrate': data['winrate']
                    }

            self.tournament_meta_picks = self.regional_meta_picks['ALL']
        except Exception as e:
            pass

    def _load_head_to_head_matchups(self):
        """
        Khai thác Ma trận Đối đầu Trực tiếp Cùng Đường (Head-to-Head Lane Matchups) Toàn cầu & Theo từng Khu vực / Giải đấu.
        """
        self.matchup_cache = {}
        self.regional_matchup_cache = {reg: {} for reg in REGIONAL_PROFILES}
        if not self.db_path.exists():
            return
        try:
            conn = open_clean_connection(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                UPPER(p1.league) as league,
                p1.position,
                p1.champion as champ,
                p2.champion as opp_champ,
                COUNT(*) as matches,
                SUM(p1.result) as wins,
                SUM(COALESCE(p1.golddiffat10, 0)) as sum_gd10,
                SUM(COALESCE(p1.xpdiffat10, 0)) as sum_xpd10,
                SUM(COALESCE(p1.csdiffat10, 0)) as sum_csd10
            FROM tournament_players p1
            JOIN tournament_players p2 ON p1.gameid = p2.gameid AND p1.position = p2.position AND p1.participantid != p2.participantid
            WHERE p1.position IS NOT NULL AND p1.champion IS NOT NULL AND p2.champion IS NOT NULL
            GROUP BY UPPER(p1.league), p1.position, p1.champion, p2.champion
            """)
            raw_rows = cursor.fetchall()
            conn.close()

            for reg_code, reg_info in REGIONAL_PROFILES.items():
                target_lgs = set(lg.upper() for lg in reg_info['leagues'])
                agg = {}
                for lg, pos, champ, opp, matches, wins, s_gd10, s_xpd10, s_csd10 in raw_rows:
                    if lg not in target_lgs:
                        continue
                    norm_c = self._normalize_champion_name(champ)
                    norm_opp = self._normalize_champion_name(opp)
                    p_str = str(pos).lower()
                    key = (p_str, norm_c, norm_opp)
                    if key not in agg:
                        agg[key] = [0, 0, 0.0, 0.0, 0.0]
                    agg[key][0] += int(matches)
                    agg[key][1] += int(wins or 0)
                    agg[key][2] += float(s_gd10 or 0.0)
                    agg[key][3] += float(s_xpd10 or 0.0)
                    agg[key][4] += float(s_csd10 or 0.0)

                for key, vals in agg.items():
                    m_cnt, w_cnt, sg, sx, sc = vals
                    self.regional_matchup_cache[reg_code][key] = {
                        'matches': m_cnt,
                        'wins': w_cnt,
                        'winrate': round(w_cnt / max(1, m_cnt), 3),
                        'avg_gd10': round(sg / max(1, m_cnt), 1),
                        'avg_xpd10': round(sx / max(1, m_cnt), 1),
                        'avg_csd10': round(sc / max(1, m_cnt), 1),
                        'source': reg_code
                    }

            self.matchup_cache = self.regional_matchup_cache['ALL']
        except Exception as e:
            pass

    def get_champion_counters(self, champ, position=None, top_k=5):
        hist=HistoricalRecommender(self.db_path)
        result=hist.counters(self._normalize_champion_name(champ),position,top_k)
        result['countered_by']=[{'opponent':r['champion'],'matches':r['games'],
                                'winrate':r['winrate_pct'],'gd10':None,'xpd10':None,
                                'historical':r['historical']} for r in result['counters']]
        _,_,matchups,_=hist.stats('ALL')
        role=result.get('position')
        targets=[]
        for (r,c,opp),(wins,n) in matchups.items():
            if r==role and c==result['champion'] and n>=hist.min_games:
                targets.append({'opponent':opp,'matches':n,'winrate':100*wins/n,
                                'historical':evidence(wins,n),'gd10':None,'xpd10':None,
                                'score':(wins+5)/(n+10)})
        result['counters']=sorted(targets,key=lambda x:(-x['score'],-x['matches'],x['opponent']))[:top_k]
        return result


    def get_candidate_lanes_for_champion(self, champ: str, available_lanes: List[str] = None) -> List[Tuple[str, int]]:
        """
        Xác định danh sách các vị trí hợp lệ cho tướng theo dữ liệu giải đấu thực tế (sắp xếp theo số lượt pick giảm dần)
        """
        lane_map = {'top': 'top', 'jungle': 'jng', 'mid': 'mid', 'bot': 'bot', 'support': 'sup'}
        if available_lanes is None:
            available_lanes = ['top', 'jungle', 'mid', 'bot', 'support']

        pos_stats = []
        for l in available_lanes:
            db_p = lane_map.get(l, l)
            p_info = self.tournament_meta_picks.get((db_p, champ), {})
            picks = p_info.get('tour_picks', p_info.get('picks', 0))
            meta_lane = self.metadata.get(champ, {}).get('lane', 'mid')
            if meta_lane == l and picks == 0:
                picks = 5
            if picks > 0:
                pos_stats.append((l, picks))

        if not pos_stats and available_lanes:
            meta_lane = self.metadata.get(champ, {}).get('lane', available_lanes[0])
            chosen_l = meta_lane if meta_lane in available_lanes else available_lanes[0]
            pos_stats.append((chosen_l, 1))

        return sorted(pos_stats, key=lambda x: x[1], reverse=True)

    def _infer_enemy_lane_assignment(self, enemy_team: List[str], reg_meta_map: dict, all_meta_map: dict) -> Dict[str, str]:
        """
        Giải bài toán phân bổ 1-1 vị trí cho danh sách tướng địch (hỗ trợ cả tướng Flex đa vị trí)
        để xác định chính xác tướng địch nào đang đi ở đường nào.
        """
        assigned = {}
        used_champs = set()
        lanes = ['top', 'jungle', 'mid', 'bot', 'support']
        db_map = {'top': 'top', 'jungle': 'jng', 'mid': 'mid', 'bot': 'bot', 'support': 'sup'}

        # Tính điểm khả năng đi từng đường của mỗi tướng địch
        pairs = []
        for ec in enemy_team:
            norm_ec = self._normalize_champion_name(ec)
            if not norm_ec:
                continue
            ec_meta_lane = self.metadata.get(norm_ec, {}).get('lane', '')
            for l in lanes:
                db_p = db_map[l]
                p_cnt = all_meta_map.get((db_p, norm_ec), {}).get('tour_picks', 0)
                r_cnt = reg_meta_map.get((db_p, norm_ec), {}).get('tour_picks', 0)
                score = p_cnt + (r_cnt * 2) + (40 if ec_meta_lane == l else 0)
                if score > 0:
                    pairs.append((score, l, norm_ec))

        for score, l, norm_ec in sorted(pairs, key=lambda x: x[0], reverse=True):
            if l not in assigned and norm_ec not in used_champs:
                assigned[l] = norm_ec
                used_champs.add(norm_ec)
        return assigned

    def recommend_picks(self, target_lane, ally_team, enemy_team, already_banned=None,
                        player_name=None, top_k=5, region='ALL', enemy_lane_champ=None):
        if not hasattr(self,'historical_engine'):
            self.historical_engine=HistoricalRecommender(self.db_path)
        return self.historical_engine.recommend(target_lane,ally_team,enemy_team,already_banned,
                                               player_name,top_k,normalize_region_code(region),enemy_lane_champ)


# =========================================================================
# 3. PHÂN HỆ 3: PUNISHER ENGINE (QUÉT LỖ HỔNG & GỢI Ý CON BÀI TRỪNG PHẠT)
# =========================================================================
class PunisherEngine:
    """
    Phân hệ Quét Lỗ Hổng Cấm/Chọn Của Địch & Gợi Ý Con Bài Trừng Phạt:
    1. Heavy Melee (3-4 Cận chiến): Gợi ý Illaoi, Darius, Mordekaiser, Cassiopeia, Brand (Hiện tượng Siwoo Illaoi)
    2. Full AD (0 AP): Gợi ý Malphite, Rammus, K'Sante, Taric
    3. Zero Hard CC (Không CC cứng): Gợi ý Master Yi, Katarina, Irelia, Zeri, Samira
    4. Full Squishy (Không chống chịu): Gợi ý Nocturne, Jarvan IV, Hecarim, Malphite, Akali
    """
    def __init__(self):
        self.metadata = CHAMPION_METADATA

    def detect_flaws_and_punishers(self, enemy_team):
        known=[c for c in enemy_team if c in self.metadata]
        unknown=[c for c in enemy_team if c not in self.metadata]
        flaws=[]
        # Qualitative expert rules only. No fixed champion list or numeric uplift.
        if len(known)>=3 and not unknown:
            rules=[('HEAVY_MELEE',sum(self.metadata[c].get('is_melee',False) for c in known)>=3,
                    'Nhiều tướng cận chiến; cân nhắc khả năng giữ khoảng cách.'),
                   ('LOW_AP',all(self.metadata[c].get('dmg_type')=='AD' for c in known),
                    'Nhãn chuyên gia thiên AD; cần kiểm tra build và sát thương thực tế.'),
                   ('LOW_CC',np.mean([self.metadata[c].get('hard_cc',.5) for c in known])<.4,
                    'Điểm khống chế theo bảng chuyên gia thấp.')]
            for name,active,description in rules:
                if active: flaws.append({'flaw_type':name,'severity':'REVIEW','description':description,
                                         'evidence_kind':'expert_rule','winrate_impact':None})
        return {'enemy_team':enemy_team,'flaws':flaws,'flaws_detected':len(flaws),'punishers':[],
                'unknown_champions':unknown,'evidence_kind':'expert_rules_not_empirical_probability',
                'summary':'Nhận xét định tính; dùng recommend_picks để xem thống kê lịch sử theo vị trí.',
                'expected_winrate_delta':None}


# =========================================================================
# 4. PHÂN HỆ 4: WIN CONDITION ENGINE (THẺ ĐIỀU KIỆN THẮNG CHIẾN THUẬT - ADR-014)
# =========================================================================
class WinConditionEngine:
    """
    Engine Trích Xuất Thẻ Điều Kiện Thắng (Win Condition Card - ADR-014):
    - Tích hợp mô hình K-Means models/archetype_kmeans.pkl
    - Trích xuất: Chủ lực gánh đội, Điểm rơi sức mạnh, Mục tiêu ưu tiên, Điều kiện thua cần tránh
    """
    def __init__(self, kmeans_path: Path = KMEANS_MODEL_PATH):
        self.kmeans_path = kmeans_path
        self.kmeans_pipeline = None
        self._load_kmeans()

    def _load_kmeans(self):
        if self.kmeans_path.exists():
            try:
                self.kmeans_pipeline = safe_load_pickle(self.kmeans_path)
            except Exception as e:
                # print(f"Warning loading K-Means: {e}")
                self.kmeans_pipeline = None

    def analyze_team_win_condition(self, team_champions: List[str]) -> Dict[str, Any]:
        """Trích xuất Thẻ Điều kiện thắng cho đội hình 5 tướng"""
        if len(team_champions) != 5:
            return {'error': 'Cần chọn đủ 5 tướng để phân tích điều kiện thắng hoàn chỉnh'}

        # Vector 5 trục
        # Import vector từ cluster_archetypes nếu có hoặc dùng default mapping
        import cluster_archetypes
        CHAMPION_TACTICAL_VECTOR = getattr(cluster_archetypes, 'CHAMPION_TACTICAL_VECTOR', {})
        
        vectors = []
        for c in team_champions:
            v = CHAMPION_TACTICAL_VECTOR.get(c, [0.5, 0.5, 0.5, 0.5, 0.5])
            vectors.append(v)
        vectors = np.array(vectors)

        # Trọng số 5 vị trí
        w_early = np.array([0.25, 0.30, 0.25, 0.15, 0.05])
        w_scaling = np.array([0.15, 0.05, 0.35, 0.40, 0.05])
        w_tf = np.array([0.25, 0.15, 0.30, 0.10, 0.20])
        w_pick = np.array([0.10, 0.30, 0.25, 0.05, 0.30])
        w_obj = np.array([0.10, 0.35, 0.20, 0.30, 0.05])

        early = float(np.sum(vectors[:, 0] * w_early))
        scaling = float(np.sum(vectors[:, 1] * w_scaling))
        tf = float(np.sum(vectors[:, 2] * w_tf))
        pick = float(np.sum(vectors[:, 3] * w_pick))
        obj = float(np.sum(vectors[:, 4] * w_obj))

        team_vector = np.array([[early, scaling, tf, pick, obj]])

        ARCHETYPE_NAMES = {
            0: "Early Snowball & Dive",
            1: "Wombocombo & Objective Control",
            2: "Late-Game Hypercarry",
            3: "Pick & Split-Push 1-3-1"
        }

        # Dự đoán cụm chiến thuật
        if self.kmeans_pipeline:
            scaler = self.kmeans_pipeline.get('scaler')
            kmeans = self.kmeans_pipeline.get('kmeans')
            archetypes_meta = self.kmeans_pipeline.get('archetypes_meta', {})
            
            scaled_vec = scaler.transform(team_vector)
            cluster_id = int(kmeans.predict(scaled_vec)[0])
            archetype_name = archetypes_meta.get(cluster_id, {}).get('name', ARCHETYPE_NAMES.get(cluster_id, f"Cụm {cluster_id}"))
            if archetype_name.startswith("Cụm"):
                archetype_name = ARCHETYPE_NAMES.get(cluster_id, archetype_name)
        else:
            # Rule-based fallback
            if early >= 0.73 and pick >= 0.75:
                cluster_id = 0
                archetype_name = "Early Snowball & Dive"
            elif tf >= 0.75 and obj >= 0.70:
                cluster_id = 1
                archetype_name = "Wombocombo & Objective Control"
            elif scaling >= 0.78:
                cluster_id = 2
                archetype_name = "Late-Game Hypercarry"
            else:
                cluster_id = 3
                archetype_name = "Pick & Split-Push 1-3-1"

        # Xác định Core Carry (Chủ lực)
        # Mid & Bot thường là carry
        carry_candidates = [team_champions[2], team_champions[3]]  # Mid & Bot
        core_carry = max(carry_candidates, key=lambda c: CHAMPION_TACTICAL_VECTOR.get(c, [0, 0, 0, 0, 0])[1])

        # Trích xuất thông tin Thẻ Điều Kiện Thắng theo Cụm
        if cluster_id == 0:  # Early Snowball & Dive
            timing = "Đầu trận (Phút 1 đến Phút 20 - Trước mốc Baron xuất hiện)"
            primary_obj = "Sâu Hư Không đợt 1 + Trụ Đầu (First Tower) trước phút 14"
            win_con = "Tạo chênh lệch >= 2,000 vàng lúc 10 phút, băng trụ 2 cánh liên tục, ép đối thủ vỡ trận trước 25 phút."
            lose_con = "Bị đối thủ phòng ngự kéo dài trận đấu qua phút 30 khi chất tướng hết thời gian lăn cầu tuyết."
            tactical_dos = ["Xâm lăng rừng đối phương sớm", "Gank tập trung đường Bot lấy giáp trụ", "Ăn trọn 3 Sâu Hư Không đợt 1"]
            tactical_donts = ["Đánh chậm chờ đồ", "Bỏ mục tiêu lớn giai đoạn đầu", "Để đối thủ kéo late"]
        elif cluster_id == 1:  # Wombocombo & Objective Control
            timing = "Giữa và Cuối trận (Phút 20 đến Phút 35 - Giai đoạn Rồng 3, 4 và Baron)"
            primary_obj = "Rồng Nguyên Tố (Thiết lập Linh Hồn Rồng) & Hang Baron"
            win_con = "Kiểm soát tầm nhìn trước 1 phút tại hang mục tiêu lớn, ép đối thủ vào các góc hẹp của sông và tung Wombocombo 5v5 quét sạch."
            lose_con = "Để đối thủ chia cắt đội hình đẩy lẻ 1-3-1 hoặc giao tranh khi chưa có đủ chiêu cuối mở combat."
            tactical_dos = ["Cắm mắt kiểm soát góc sông trước 1 phút", "Giao tranh 5v5 trực diện khi đủ 5 Ulti", "Ép ăn Baron để dụ combat"]
            tactical_donts = ["Đánh phân tán lẻ tẻ", "Giao tranh ở địa hình trống trải", "Combat khi chủ lực chưa hồi Tốc Biến"]
        elif cluster_id == 2:  # Late-Game Hypercarry
            timing = "Cuối trận (Sau Phút 28 - Khi chủ lực đạt ngưỡng 3-4 trang bị chuẩn)"
            primary_obj = "Baron Nashor & Rồng Ngàn Tuổi (Elder Dragon)"
            win_con = "Bảo kê tuyệt đối cho siêu chủ lực farm an toàn; chấp nhận nhường mục tiêu sớm nếu cần; hủy diệt giao tranh cuối trận."
            lose_con = "Bị đối thủ băng trụ lăn cầu tuyết thua > 2,500 vàng lúc 10 phút dẫn đến vỡ trận sớm."
            tactical_dos = ["Nhường tài nguyên rừng/lính cho chủ lực", "Đánh phòng thủ phản công", "Kéo dài trận đấu qua phút 30"]
            tactical_donts = ["Giao tranh vô nghĩa lúc 10 phút", "Bỏ rơi chủ lực trong combat", "Tham tranh chấp Rồng 1 khi đồ chưa có"]
        else:  # Pick & Split-Push 1-3-1
            timing = "Xuyên suốt trận đấu (Đặc biệt phát huy từ Phút 15 đến Phút 30)"
            primary_obj = "Trụ 2 cánh bản đồ & Bắt lẻ cô lập mục tiêu đi lẻ"
            win_con = "Tạo thế đẩy lẻ 1-3-1 hoặc 1-4, buộc đối thủ phải phân tán phòng thủ; rình rập bắt lẻ khi địch di chuyển và ép Baron khi hơn người."
            lose_con = "Bị đối thủ ép giao tranh 5v5 trực diện bất ngờ khi đội hình chưa kịp gom quân."
            tactical_dos = ["Cắm mắt sâu rừng đối thủ", "Đẩy lính 2 cánh tạo áp lực song song", "Bắt lẻ trước khi tranh chấp mục tiêu lớn"]
            tactical_donts = ["Đâm đầu vào giao tranh 5v5 chính diện", "Đẩy lẻ khi không có tầm nhìn", "Dừng nhịp đẩy cánh"]

        return {
            'team_champions': team_champions,
            'evidence_kind': 'expert_tactical_vectors_and_rules',
            'causal_uplift': None,
            'unknown_champions': [c for c in team_champions if c not in CHAMPION_TACTICAL_VECTOR],
            'archetype_id': cluster_id,
            'archetype_name': archetype_name,
            'radar_scores': {
                'Early_Power': round(early, 3),
                'Scaling': round(scaling, 3),
                'Teamfight_AOE': round(tf, 3),
                'Pick_Potential': round(pick, 3),
                'Objective_Control': round(obj, 3)
            },
            'win_condition_card': {
                'core_carry': core_carry,
                'power_spike_timing': timing,
                'primary_objective': primary_obj,
                'win_condition': win_con,
                'critical_lose_condition': lose_con,
                'tactical_dos': tactical_dos,
                'tactical_donts': tactical_donts
            }
        }


# =========================================================================
# 5. HỆ THỐNG GỢI Ý CẤM/CHỌN TỔNG HỢP (MASTER RECOMMENDER ENGINE)
# =========================================================================
class RecommenderEngine:
    """Hệ thống Đóng gói Toàn diện 4 Phân hệ Gợi ý Cấm/Chọn"""
    def __init__(self, db_path: Path = DB_PATH, accounts_path: Path = PRO_ACCOUNTS_PATH, kmeans_path: Path = KMEANS_MODEL_PATH):
        self.schema_version = 2
        self.target_ban_engine = TargetBanEngine(db_path=db_path, accounts_path=accounts_path)
        self.pick_recommender = MetaPickRecommender(db_path=db_path, accounts_path=accounts_path)
        self.pick_recommender.player_stats_cache = self.target_ban_engine.player_stats_cache
        self.punisher_engine = PunisherEngine()
        self.win_condition_engine = WinConditionEngine(kmeans_path=kmeans_path)

    def recommend_content_based(self, lane, seed_champion=None, player_name=None,
                                region='ALL', already_banned=None, top_k=5):
        from content_based import ContentBasedRecommender
        if (seed_champion is None) == (player_name is None):
            raise ValueError('Provide exactly one seed champion or player')
        if not hasattr(self,'content_recommender'):
            self.content_recommender=ContentBasedRecommender(self.pick_recommender.db_path)
        if seed_champion is not None:
            return self.content_recommender.recommend_similar(seed_champion,lane,normalize_region_code(region),already_banned,top_k)
        return self.content_recommender.recommend_for_player(player_name,lane,normalize_region_code(region),already_banned,top_k)

    def recommend_draft_picks(self, lane, ally_team, enemy_team, **kwargs):
        from draft_advisor import DraftAdvisor
        if not hasattr(self,'draft_advisor'):
            self.draft_advisor=DraftAdvisor(db_path=self.pick_recommender.db_path)
        return self.draft_advisor.recommend_picks(lane,ally_team,enemy_team,**kwargs)

    def recommend_draft_bans(self, enemy_roster, enemy_picks, own_picks, **kwargs):
        from draft_advisor import DraftAdvisor
        if not hasattr(self,'draft_advisor'):
            self.draft_advisor=DraftAdvisor(db_path=self.pick_recommender.db_path)
        return self.draft_advisor.recommend_bans(enemy_roster,enemy_picks,own_picks,**kwargs)

    def get_regional_meta_summary(self, region: str = 'LCK', top_k: int = 3) -> Dict[str, Any]:
        """Trích xuất Hồ sơ Meta Cấm/Chọn & Phong cách Chiến thuật của một Khu vực hoặc Giải đấu Quốc tế"""
        reg_code = normalize_region_code(region)
        macro = self.pick_recommender.regional_macro_stats.get(reg_code, {})
        p1_bans = self.target_ban_engine.get_pro_tournament_meta_bans(top_k=5, ban_phase=1, region=reg_code)
        p2_bans = self.target_ban_engine.get_pro_tournament_meta_bans(top_k=5, ban_phase=2, region=reg_code)

        reg_picks_map = self.pick_recommender.regional_meta_picks.get(reg_code, {})
        top_picks_by_lane = {}
        for pos in ['top', 'jng', 'mid', 'bot', 'sup']:
            pos_items = [
                {'champion': c, 'picks': info['tour_picks'], 'winrate_pct': round(info['winrate'] * 100, 1)}
                for (p, c), info in reg_picks_map.items()
                if p == pos and info['tour_picks'] >= 3
            ]
            pos_items = sorted(pos_items, key=lambda x: x['picks'], reverse=True)[:top_k]
            top_picks_by_lane[pos] = pos_items

        return {
            'region': reg_code,
            'label': REGIONAL_PROFILES[reg_code]['label'],
            'style_dna': REGIONAL_PROFILES[reg_code]['style_dna'],
            'style_evidence_kind': 'expert_description_not_learned',
            'macro': macro,
            'top_phase1_bans': p1_bans,
            'top_phase2_bans': p2_bans,
            'top_picks_by_lane': top_picks_by_lane
        }

    def save(self, output_path: Path = RECOMMENDER_MODEL_PATH):
        """Đóng gói toàn bộ engine thành file pkl"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            pickle.dump(self, f)
        print(f"-> Đã đóng gói thành công Recommender Engine vào: {output_path}")

    @staticmethod
    def load(filepath: Path = RECOMMENDER_MODEL_PATH) -> 'RecommenderEngine':
        engine = safe_load_pickle(filepath)
        if getattr(engine, 'schema_version', None) != 2:
            raise ValueError('Legacy recommender; rebuild with --save-model')
        return engine


# =========================================================================
# CLI COMMAND RUNNER & DEMO
# =========================================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Ban/Pick Recommender & Win Condition Engine (Task 3.5)")
    parser.add_argument('--content-based', action='store_true', help='Chương 6: hồ sơ tướng/tuyển thủ và cosine similarity')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--seed-champion', help='Tướng mẫu để tìm lựa chọn tương đồng')
    group.add_argument('--content-player', help='Tuyển thủ có lịch sử chọn tướng để lập user profile')
    parser.add_argument('--region', type=str, default="ALL", help="Khu vực / Giải đấu: ALL, LCK, LPL, LCP, INTERNATIONAL, WLDS (CKTG), MSI, EWC")
    parser.add_argument('--compare-regions', action='store_true', help="So sánh trực diện bản sắc Cấm/Chọn giữa LCK vs LPL vs LCP vs Quốc Tế (MSI/CKTG)")
    parser.add_argument('--target-ban', action='store_true', help="Chạy gợi ý CẤM mục tiêu theo Tuyển thủ")
    parser.add_argument('--player', type=str, default="Keria", help="Tên tuyển thủ đối phương (VD: Keria, Chovy, Kiaya, Knight)")
    parser.add_argument('--link-player', type=str, help="Tên tuyển thủ cần liên kết Riot ID")
    parser.add_argument('--riot-id', type=str, help="Riot ID của tuyển thủ (VD: Chovy#KR1)")

    parser.add_argument('--recommend-pick', action='store_true', help="Chạy gợi ý CHỌN tướng chuẩn Meta & Synergy")
    parser.add_argument('--lane', type=str, default="bot", help="Vị trí cần pick (top, jungle, mid, bot, support)")
    parser.add_argument('--ally', type=str, default="Renekton,Elise,Ahri", help="Danh sách tướng phe ta (phân cách bằng dấu phẩy)")
    parser.add_argument('--enemy', type=str, default="Malphite,Sejuani,Azir", help="Danh sách tướng phe địch (phân cách bằng dấu phẩy)")

    parser.add_argument('--detect-flaws', action='store_true', help="Quét lỗ hổng cấm/chọn của địch & gợi ý con bài trừng phạt")
    parser.add_argument('--enemy-comp', type=str, default="Renekton,Xin Zhao,Sylas,Samira,Nautilus", help="Đội hình địch (VD: Heavy Melee)")

    parser.add_argument('--win-condition', action='store_true', help="Trích xuất Thẻ Điều kiện thắng cho đội hình")
    parser.add_argument('--team', type=str, default="Renekton,Elise,LeBlanc,Kalista,Nautilus", help="5 tướng trong đội hình")

    parser.add_argument('--save-model', action='store_true', help="Đóng gói và lưu Recommender Engine vào models/")
    parser.add_argument('--demo', action='store_true', help="Chạy toàn bộ kịch bản Demo trực quan 4 phân hệ + Đối chiếu Khu vực")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.content_based:
        from content_based import ContentBasedRecommender
        content=ContentBasedRecommender()
        if args.seed_champion:
            result=content.recommend_similar(args.seed_champion,args.lane,normalize_region_code(args.region))
        elif args.content_player:
            result=content.recommend_for_player(args.content_player,args.lane,normalize_region_code(args.region))
        else:
            raise SystemExit('--content-based requires --seed-champion or --content-player')
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return
    engine = RecommenderEngine()
    reg_code = normalize_region_code(args.region)

    print("=" * 95)
    print(f"🎯 HỆ THỐNG TRỢ LÝ CẤM/CHỌN THÔNG MINH & NHẬN DIỆN ĐIỀU KIỆN THẮNG (BỐI CẢNH: {REGIONAL_PROFILES[reg_code]['label'].upper()})")
    print("=" * 95)

    # 1. Đăng ký liên kết tài khoản
    if args.link_player and args.riot_id:
        engine.target_ban_engine.link_player_account(args.link_player, args.riot_id)
        print(f"✅ Đã liên kết thành công Tuyển thủ: {args.link_player} -> Riot ID: {args.riot_id}")
        return

    # 1.5 So sánh Bản sắc Cấm/Chọn theo Khu vực & Giải Quốc Tế
    if args.compare_regions or args.demo:
        print("\n" + "=" * 95)
        print("🌍 ĐỐI CHIẾU BẢN SẮC CẤM/CHỌN (BAN/PICK META) THEO TỪNG KHU VỰC & GIẢI QUỐC TẾ (MSI / CKTG)")
        print("=" * 95)
        for r_key in ['LCK', 'LPL', 'LCP', 'MSI', 'WLDS', 'INTERNATIONAL']:
            prof = engine.get_regional_meta_summary(r_key, top_k=3)
            m = prof['macro']
            print(f"\n🏆 [{prof['region']}] {prof['label'].upper()} ({m.get('games', 0):,} trận | Thời lượng TB: {m.get('avg_duration_min', 0)}p | Nhịp độ: {m.get('avg_ckpm', 0)} mạng/p | Blue WR: {m.get('blue_winrate_pct', 50)}%)")
            print(f"   • Bản sắc chiến thuật: {prof['style_dna']}")
            p1_str = ", ".join([f"{b['champion']} ({b['ban_count']} cấm)" for b in prof['top_phase1_bans'][:4]])
            p2_str = ", ".join([f"{b['champion']} ({b['ban_count']} cấm)" for b in prof['top_phase2_bans'][:4]])
            print(f"   • Top Cấm Mở Đầu (Phase 1): {p1_str}")
            print(f"   • Top Cấm Nhắm Mục Tiêu (Phase 2): {p2_str}")
            lanes_line = []
            for pos_k, items in prof['top_picks_by_lane'].items():
                top_c = "/".join([f"{it['champion']}({it['picks']})" for it in items[:2]])
                lanes_line.append(f"{pos_k.upper()}: {top_c}")
            print(f"   • Tướng Ưu Tiên Chọn 5 Đường: {' | '.join(lanes_line)}")
        print("-" * 95)

    # 2. Phân hệ CẤM mục tiêu (Target Ban)
    if args.target_ban or args.demo:
        player = args.player
        print(f"\n[PHÂN HỆ 1] GỢI Ý CẤM MỤC TIÊU THEO TUYỂN THỦ: >>> {player.upper()} <<< (Khu vực: {reg_code})")
        print("-" * 90)
        bans = engine.target_ban_engine.recommend_target_bans(player, top_k=5, region=reg_code)
        for i, b in enumerate(bans, 1):
            print(f"  {i}. [{b['badge']}] {b['champion'].upper()} (Điểm đe dọa: {b['threat_score']})")
            print(f"     • Đấu giải: {b['tournament_stats']}")
            print(f"     • Solo Rank: {b['rank_stats']}")

    # 3. Phân hệ CHỌN tướng Meta & Synergy
    if args.recommend_pick or args.demo:
        lane = args.lane
        ally_list = [c.strip() for c in args.ally.split(',') if c.strip()]
        enemy_list = [c.strip() for c in args.enemy.split(',') if c.strip()]
        regions_to_show = [reg_code] if not args.demo else ['LCK', 'LPL', 'WLDS']
        for r_show in regions_to_show:
            print(f"\n[PHÂN HỆ 2] GỢI Ý CHỌN TƯỚNG CHUẨN META [{r_show}] CHO VỊ TRÍ: >>> {lane.upper()} <<<")
            print(f"  • Phe ta đã pick: {', '.join(ally_list) if ally_list else 'Chưa có'} | Phe địch đã pick: {', '.join(enemy_list) if enemy_list else 'Chưa có'}")
            print("-" * 90)
            picks = engine.pick_recommender.recommend_picks(lane, ally_list, enemy_list, top_k=5, region=r_show)
            for i, p in enumerate(picks, 1):
                print(f"  {i}. ⭐ {p['champion'].upper()} (Điểm đề xuất [{r_show}]: {p['score']} | {p['dmg_type']})")
                for r in p['reasons']:
                    print(f"     + {r}")

    # 4. Phân hệ Quét Lỗ Hổng & Con Bài Trừng Phạt (Punisher)
    if args.detect_flaws or args.demo:
        enemy_comp = [c.strip() for c in args.enemy_comp.split(',') if c.strip()]
        print(f"\n[PHÂN HỆ 3] QUÉT LỖ HỔNG CẤM/CHỌN ĐỊCH & GỢI Ý CON BÀI TRỪNG PHẠT:")
        print(f"  • Đội hình địch khảo sát: {', '.join(enemy_comp)}")
        print("-" * 90)
        flaw_res = engine.punisher_engine.detect_flaws_and_punishers(enemy_comp)
        if flaw_res['flaws']:
            for fl in flaw_res['flaws']:
                print(f"  🚨 [{fl['severity']}] {fl['flaw_type']}")
                print(f"     • Mô tả: {fl['description']}")
                print('     • Quy tắc chuyên gia; chưa ước lượng tác động winrate.')
            print("\n  ⚔️ TOP CON BÀI TRỪNG PHẠT KHUYÊN DÙNG:")
            for i, pu in enumerate(flaw_res['punishers'], 1):
                print(f"    {i}. [{pu['lane']}] {pu['champion'].upper()} - {pu['punisher_role']} ({pu['expected_winrate_delta']})")
                print(f"       -> Lý do: {pu['why_punish']}")
        else:
            print("  ✅ Đội hình địch cân bằng, không phát hiện lỗ hổng chí mạng.")

    # 5. Phân hệ Thẻ Điều Kiện Thắng (Win Condition Card)
    if args.win_condition or args.demo:
        team_list = [c.strip() for c in args.team.split(',') if c.strip()]
        print(f"\n[PHÂN HỆ 4] TRÍCH XUẤT THẺ ĐIỀU KIỆN THẮNG CHIẾN THUẬT (ADR-014):")
        print(f"  • 5 Tướng Đội hình: {', '.join(team_list)}")
        print("-" * 90)
        win_res = engine.win_condition_engine.analyze_team_win_condition(team_list)
        if 'error' in win_res:
            print(f"  ❌ Lỗi: {win_res['error']}")
        else:
            print(f"  🏆 TRƯỜNG PHÁI ĐỘI HÌNH: [{win_res['archetype_name'].upper()}]")
            print(f"  📊 Radar 5 trục: Early: {win_res['radar_scores']['Early_Power']} | Scaling: {win_res['radar_scores']['Scaling']} | Combat: {win_res['radar_scores']['Teamfight_AOE']} | Pick: {win_res['radar_scores']['Pick_Potential']} | Obj: {win_res['radar_scores']['Objective_Control']}")
            card = win_res['win_condition_card']
            print(f"\n  🎯 THẺ CHIẾN THUẬT (WIN CONDITION CARD):")
            print(f"     1. Chủ lực gánh đội (Core Carry): ⭐ {card['core_carry']}")
            print(f"     2. Điểm rơi sức mạnh: ⏱️ {card['power_spike_timing']}")
            print(f"     3. Mục tiêu số 1: 🐉 {card['primary_objective']}")
            print(f"     4. Điều kiện thắng: ✅ {card['win_condition']}")
            print(f"     5. Điều kiện thua cần tránh: ❌ {card['critical_lose_condition']}")
            print(f"     6. Việc NÊN làm: {', '.join(card['tactical_dos'])}")
            print(f"     7. Việc KHÔNG ĐƯỢC làm: {', '.join(card['tactical_donts'])}")

    # 6. Đóng gói mô hình
    if args.save_model or args.demo:
        print("\n" + "-" * 90)
        engine.save()

    print("\n" + "=" * 90)
    print("🎉 HOÀN THÀNH TOÀN BỘ QUY TRÌNH GỢI Ý CẤM/CHỌN THÔNG MINH (TASK 3.5)!")
    print("=" * 90)


if __name__ == '__main__':
    main()
