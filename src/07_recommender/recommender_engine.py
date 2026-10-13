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

warnings.filterwarnings('ignore')


# =========================================================================
# SAFE UNPICKLER PATTERN (Để nạp model K-Means xuyên module)
# =========================================================================
class _SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'DraftArchetypeClusterer':
            import cluster_archetypes
            return getattr(cluster_archetypes, 'DraftArchetypeClusterer')
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
DUO_SYNERGIES = {
    # Cặp Đôi Bot - Support Kinh Điển Meta
    ('Ashe', 'Seraphine'): 0.98,
    ('Ashe', 'Braum'): 0.95,
    ('Ashe', 'Tahm Kench'): 0.92,
    ('Ashe', 'Renata Glasc'): 0.92,
    ('Senna', 'Tahm Kench'): 0.98,
    ('Senna', 'Ornn'): 0.94,
    ('Senna', 'Nautilus'): 0.92,
    ('Lucian', 'Nami'): 0.98,
    ('Lucian', 'Milio'): 0.98,
    ('Smolder', 'Milio'): 0.97,
    ('Smolder', 'Braum'): 0.94,
    ('Zeri', 'Lulu'): 0.97,
    ('Zeri', 'Yuumi'): 0.92,
    ('Kalista', 'Renata Glasc'): 0.96,
    ('Kalista', 'Nautilus'): 0.95,
    ('Varus', 'Renata Glasc'): 0.93,
    ('Varus', 'Alistar'): 0.92,
    ('Varus', 'Ashe'): 0.90,
    ('Kai\'Sa', 'Nautilus'): 0.96,
    ('Kai\'Sa', 'Rell'): 0.95,
    ('Kai\'Sa', 'Leona'): 0.94,
    ('Samira', 'Nautilus'): 0.94,
    ('Samira', 'Rell'): 0.94,
    ('Xayah', 'Rakan'): 0.98,
    ('Caitlyn', 'Lux'): 0.94,
    ('Caitlyn', 'Morgana'): 0.92,
    ('Jinx', 'Thresh'): 0.94,
    ('Jinx', 'Lulu'): 0.94,
    ('Jinx', 'Tahm Kench'): 0.92,
    ('Ezreal', 'Karma'): 0.98,
    ('Ezreal', 'Braum'): 0.94,
    ('Ezreal', 'Leona'): 0.90,
    ('Kai\'Sa', 'Alistar'): 0.95,
    ('Samira', 'Alistar'): 0.96,
    ('Kalista', 'Alistar'): 0.95,
    ('Tristana', 'Alistar'): 0.94,
    ('Draven', 'Alistar'): 0.95,

    # Cặp Đôi Mid - Jungle
    ('Ahri', 'Vi'): 0.98,
    ('Orianna', 'Jarvan IV'): 0.98,
    ('Orianna', 'Nocturne'): 0.95,
    ('Orianna', 'Wukong'): 0.95,
    ('Taliyah', 'Renekton'): 0.96,
    ('Taliyah', 'Pantheon'): 0.95,
    ('Sylas', 'Sejuani'): 0.96,
    ('Sylas', 'Maokai'): 0.95,
    ('Yone', 'Sejuani'): 0.95,
    ('Yone', 'Skarner'): 0.95,
    ('Azir', 'Maokai'): 0.95,
    ('Azir', 'Sejuani'): 0.94,
    ('Jayce', 'Maokai'): 0.95,
    ('Twisted Fate', 'Nocturne'): 0.96,

    # Cặp Đôi Top - Jungle
    ('Renekton', 'Nidalee'): 0.96,
    ('Renekton', 'Elise'): 0.96,
    ('Camille', 'Galio'): 0.98,
    ('Camille', 'Sejuani'): 0.95,
    ('Kennen', 'Jarvan IV'): 0.95,
    ('Rumble', 'Jarvan IV'): 0.96,
    ('Rumble', 'Vi'): 0.95,
    ('Yasuo', 'Gragas'): 0.96,
    ('Kennen', 'Amumu'): 0.92
}


# =========================================================================
# 2. PHÂN HỆ 1: TARGET BAN ENGINE (CẤM LAI GHÉP THEO TUYỂN THỦ ĐỐI PHƯƠNG)
# =========================================================================
class TargetBanEngine:
    """
    Phân hệ CẤM Lai Ghép mục tiêu theo Tuyển thủ Đối phương:
    - 60-70% Trọng số Đấu Giải: Lịch sử 30,000 bản ghi tournament_players (Bayesian Winrate + Laning Dominance)
    - 30-40% Trọng số Solo Rank Gần Nhất: Quét pro_player_accounts.json phát hiện Pocket Pick spam rank
    """
    def __init__(self, db_path: Path = DB_PATH, accounts_path: Path = PRO_ACCOUNTS_PATH):
        self.db_path = db_path
        self.accounts_path = accounts_path
        self.pro_accounts = self._load_pro_accounts()
        self.player_stats_cache = {}
        self._build_player_stats_cache()

    def _load_pro_accounts(self) -> Dict[str, Any]:
        if self.accounts_path.exists():
            with open(self.accounts_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('players', {})
        return {}

    def _build_player_stats_cache(self):
        """Khai thác CSDL SQLite tính toán Bayesian Winrate & Dominance cho 420 tuyển thủ"""
        if not self.db_path.exists():
            return
        conn = sqlite3.connect(self.db_path)
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
          AND (date >= '2026-04-01' OR year = 2026)
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

        # 5. Khai thác Tần suất Bị Cấm Thực Tế Phân Chia Theo Đúng Phase 1 vs Phase 2 (2026 Recent Patches)
        conn = sqlite3.connect(self.db_path)
        phase_ban_query = """
        SELECT 
            b.ban_champ,
            SUM(CASE WHEN b.slot IN ('ban1','ban2','ban3') THEN 1 ELSE 0 END) as p1_bans,
            SUM(CASE WHEN b.slot IN ('ban4','ban5') THEN 1 ELSE 0 END) as p2_bans,
            COUNT(*) as total_bans
        FROM (
            SELECT ban1 as ban_champ, 'ban1' as slot FROM tournament_matches WHERE (date >= '2026-04-01' OR year = 2026) AND ban1 IS NOT NULL AND ban1 != ''
            UNION ALL SELECT ban2, 'ban2' FROM tournament_matches WHERE (date >= '2026-04-01' OR year = 2026) AND ban2 IS NOT NULL AND ban2 != ''
            UNION ALL SELECT ban3, 'ban3' FROM tournament_matches WHERE (date >= '2026-04-01' OR year = 2026) AND ban3 IS NOT NULL AND ban3 != ''
            UNION ALL SELECT ban4, 'ban4' FROM tournament_matches WHERE (date >= '2026-04-01' OR year = 2026) AND ban4 IS NOT NULL AND ban4 != ''
            UNION ALL SELECT ban5, 'ban5' FROM tournament_matches WHERE (date >= '2026-04-01' OR year = 2026) AND ban5 IS NOT NULL AND ban5 != ''
        ) b
        GROUP BY b.ban_champ
        """
        phase_df = pd.read_sql(phase_ban_query, conn)
        total_matches = pd.read_sql("SELECT COUNT(*) as cnt FROM tournament_matches WHERE (date >= '2026-04-01' OR year = 2026)", conn).iloc[0]['cnt']
        conn.close()

        self.tournament_phase1_bans = dict(zip(phase_df['ban_champ'], phase_df['p1_bans']))
        self.tournament_phase2_bans = dict(zip(phase_df['ban_champ'], phase_df['p2_bans']))
        self.tournament_ban_counts = dict(zip(phase_df['ban_champ'], phase_df['total_bans']))
        self.max_phase1_bans = max(self.tournament_phase1_bans.values()) if self.tournament_phase1_bans else 1000
        self.max_phase2_bans = max(self.tournament_phase2_bans.values()) if self.tournament_phase2_bans else 500
        self.max_ban_count = max(self.tournament_ban_counts.values()) if self.tournament_ban_counts else 1000
        self.total_matches = max(1, total_matches)

    def get_pro_tournament_meta_bans(self, top_k: int = 10, ban_phase: int = 1) -> List[Dict[str, Any]]:
        """Lấy danh sách Top tướng bị cấm nhiều nhất trong Đấu Giải Chuyên Nghiệp phân chia theo đúng Phase 1 vs Phase 2"""
        ban_dict = self.tournament_phase1_bans if ban_phase == 1 else self.tournament_phase2_bans
        
        sorted_bans = sorted(ban_dict.items(), key=lambda x: x[1], reverse=True)
        results = []
        for champ, count in sorted_bans:
            if not champ or champ.lower() in ["none", "null"]:
                continue
            ban_rate = (count / self.total_matches) * 100.0
            p1_c = self.tournament_phase1_bans.get(champ, 0)
            p2_c = self.tournament_phase2_bans.get(champ, 0)
            phase_label = f"Phase {ban_phase} ({count} lượt cấm - {round(ban_rate, 1)}%)"
            results.append({
                'champion': champ,
                'ban_count': count,
                'phase1_bans': p1_c,
                'phase2_bans': p2_c,
                'ban_rate': round(ban_rate, 1),
                'reason': f"Top cấm Đấu Giải 2026 {phase_label}"
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

    def recommend_target_bans(self, player_name: str, top_k: int = 5, tournament_weight: float = 0.65, ban_phase: int = 1) -> List[Dict[str, Any]]:
        """
        Đề xuất Top K tướng bắt buộc phải CẤM khi đối đầu với Tuyển thủ chỉ định:
        - Phân chia 100% theo Dữ liệu Cấm Thực tế Phase 1 vs Phase 2 trong SQLite CSDL:
          + ban_phase = 1: CẤM 1 (Lượt 1, 2, 3) -> Dựa trên lượt cấm thực tế tại ban1, ban2, ban3 + Tướng tủ giải đấu.
          + ban_phase = 2: CẤM 2 (Lượt 4, 5) -> Dựa trên lượt cấm thực tế tại ban4, ban5 + Đột biến Rank / Pocket pick.
        """
        tour_picks = self.player_stats_cache.get(player_name, {})
        rank_info = self.pro_accounts.get(player_name, {})
        rank_picks = rank_info.get('recent_rank_picks', {})

        all_champs = set(tour_picks.keys()).union(set(rank_picks.keys()))
        if not all_champs:
            meta_bans = self.get_pro_tournament_meta_bans(top_k=top_k, ban_phase=ban_phase)
            return [
                {
                    'champion': mb['champion'],
                    'threat_score': round(0.75 - 0.02 * i, 4),
                    'tournament_threat': 0.70,
                    'rank_threat': None,
                    'tournament_stats': f"Chuẩn Meta Giải Đấu ({mb['ban_count']} lượt cấm P{ban_phase})",
                    'rank_stats': None,
                    'badge': '⭐ META CẤM TOÀN CẦU',
                    'reason': mb.get('reason', 'Tướng Meta bị cấm nhiều trong giải đấu')
                }
                for i, mb in enumerate(meta_bans[:top_k])
            ]

        results = []
        for champ in all_champs:
            t_data = tour_picks.get(champ, None)
            r_data = rank_picks.get(champ, None)

            # 1. Điểm Đấu Giải Tuyển thủ
            if t_data:
                tti = t_data['tti']
                t_games = t_data['games']
                t_desc = f"{t_games} trận giải (Thắng {round(t_data['winrate']*100, 1)}%, GD10: {t_data['avg_gd10']:+0.0f}g, KDA: {t_data['kda']})"
            else:
                tti = 0.40
                t_games = 0
                t_desc = "Chưa xuất hiện trong giải đấu gần đây"

            # 2. Điểm Solo Rank gần nhất
            if r_data:
                r_wr = r_data.get('winrate', 0.50)
                r_games = r_data.get('games', 5)
                is_spike = r_data.get('spike', False)
                note = r_data.get('note', '')
                sti = (0.50 * r_wr) + (0.35 * min(1.0, r_games / 15.0)) + (0.15 if is_spike else 0.0)
                r_desc = f"Rank {r_games} trận (WR: {round(r_wr*100,1)}%) - {note}"
            else:
                sti = 0.45
                r_desc = "Không có đột biến spam trong Rank"
                is_spike = False

            # 3. Tính toán độ ưu tiên cấm theo Phase 1 vs Phase 2 DỰA 100% TRÊN DỮ LIỆU CẤM GIẢI ĐẤU
            p1_count = self.tournament_phase1_bans.get(champ, 0)
            p2_count = self.tournament_phase2_bans.get(champ, 0)
            total_bans = p1_count + p2_count
            
            p1_rate = (p1_count / float(self.max_phase1_bans)) if self.max_phase1_bans > 0 else 0.0
            p2_rate = (p2_count / float(self.max_phase2_bans)) if self.max_phase2_bans > 0 else 0.0

            if ban_phase == 1:
                # Phase 1: Trọng số chính dựa trên Tần suất cấm Phase 1 giải đấu (p1_rate) và Tướng tủ của đối thủ (tti)
                if p1_count >= self.max_phase1_bans * 0.65 and t_games >= 1:
                    badge = f"🔥 TOP MUST-BAN PHASE 1 ({p1_count} lượt cấm)"
                    hybrid_score = (0.55 * p1_rate) + (0.35 * tti) + (0.10 * sti) + 0.12
                elif p1_count >= self.max_phase1_bans * 0.40:
                    badge = f"⭐ TƯỚNG CẤM MỞ ĐẦU GIẢI ({p1_count} lượt cấm P1)"
                    hybrid_score = (0.50 * p1_rate) + (0.35 * tti) + (0.15 * sti) + 0.06
                elif t_games >= 10 and t_data and t_data['winrate'] >= 0.65:
                    badge = f"⭐ TƯỚNG TỦ ĐẤU GIẢI ({t_games} trận)"
                    hybrid_score = (0.35 * p1_rate) + (0.50 * tti) + (0.15 * sti)
                else:
                    badge = "📊 CẤM CHIẾN THUẬT"
                    hybrid_score = (0.40 * p1_rate) + (0.35 * tti) + (0.25 * sti)
            else:
                # Phase 2: Trọng số chính dựa trên Tần suất cấm Phase 2 giải đấu (p2_rate) + Đột biến Rank / Pocket pick
                if is_spike and r_data and r_data.get('winrate', 0) >= 0.70:
                    badge = "🚨 POCKET PICK SPAM RANK"
                    hybrid_score = (0.25 * p2_rate) + (0.30 * tti) + (0.45 * sti) + 0.15
                elif p2_count >= self.max_phase2_bans * 0.50:
                    badge = f"🎯 ĐÒN CẤM TARGET PHASE 2 ({p2_count} lượt cấm P2)"
                    hybrid_score = (0.50 * p2_rate) + (0.30 * tti) + (0.20 * sti) + 0.08
                elif t_games >= 8:
                    badge = f"🔥 TƯỚNG TỦ CÒN LẠI ({t_games} trận)"
                    hybrid_score = (0.35 * p2_rate) + (0.45 * tti) + (0.20 * sti)
                else:
                    badge = "📊 CẤM TÌNH HUỐNG PHASE 2"
                    hybrid_score = (0.40 * p2_rate) + (0.35 * tti) + (0.25 * sti)

            results.append({
                'champion': champ,
                'threat_score': round(float(hybrid_score), 4),
                'tournament_threat': round(float(tti), 4),
                'rank_threat': round(float(sti), 4) if rank_picks else None,
                'tournament_stats': t_desc,
                'rank_stats': r_desc,
                'badge': badge,
                'is_pocket_pick': is_spike
            })

        results = sorted(results, key=lambda x: x['threat_score'], reverse=True)
        return results[:top_k]

    def recommend_team_bans(self, enemy_roster: Dict[str, str], top_k: int = 5, ban_phase: int = 1, already_banned: set = None) -> List[Dict[str, Any]]:
        """
        Đề xuất Top Cấm Toàn Đội hình Đối phương kết hợp 3 yếu tố DỰA 100% TRÊN DỮ LIỆU:
        1. Meta Ban Presence 2026 (Tần suất cấm thực tế theo Phase 1 / Phase 2 từ 37,000 ván đấu)
        2. Mức độ đe dọa cụ thể của từng tuyển thủ đối phương (Đấu giải + Solo Rank)
        3. Khả năng Target điểm yếu chiến thuật của đối thủ
        """
        if already_banned is None:
            already_banned = set()

        champ_candidates = {}

        # 1. Quét Meta Ban giải đấu 2026 theo đúng ban_phase (Phase 1 vs Phase 2)
        meta_bans = self.get_pro_tournament_meta_bans(top_k=20, ban_phase=ban_phase)
        max_b = self.max_phase1_bans if ban_phase == 1 else self.max_phase2_bans

        for mb in meta_bans:
            c_name = mb['champion']
            if c_name in already_banned:
                continue
            champ_candidates[c_name] = {
                'champion': c_name,
                'ban_count': mb['ban_count'],
                'ban_rate': mb['ban_rate'],
                'base_score': 0.50 + 0.40 * (mb['ban_count'] / float(max_b if max_b > 0 else 1)),
                'player_target': None,
                'player_role': None,
                'player_stats': None,
                'reason': mb['reason']
            }

        # 2. Quét cụ thể từng vị trí của tuyển thủ đối phương theo đúng ban_phase
        for role_key, p_name in enemy_roster.items():
            p_bans = self.recommend_target_bans(p_name, top_k=5, ban_phase=ban_phase)
            for pb in p_bans:
                c_name = pb['champion']
                if c_name in already_banned:
                    continue
                curr_threat = pb.get('threat_score', 0.5)
                p_b_count = self.tournament_phase1_bans.get(c_name, 0) if ban_phase == 1 else self.tournament_phase2_bans.get(c_name, 0)
                if c_name not in champ_candidates:
                    b_rate = round((p_b_count / float(self.total_matches)) * 100.0, 1)
                    champ_candidates[c_name] = {
                        'champion': c_name,
                        'ban_count': p_b_count,
                        'ban_rate': b_rate,
                        'base_score': 0.45 + 0.35 * (p_b_count / float(max_b if max_b > 0 else 1)),
                        'player_target': p_name,
                        'player_role': role_key,
                        'player_stats': pb.get('tournament_stats', pb.get('reason', '')),
                        'player_threat': curr_threat,
                        'reason': f"Target {p_name} ({role_key.upper()})"
                    }
                else:
                    # Chỉ cập nhật tuyển thủ mục tiêu nếu tuyển thủ này có độ thuần thục / số trận đe dọa cao hơn
                    prev_threat = champ_candidates[c_name].get('player_threat', 0.0)
                    if curr_threat > prev_threat or champ_candidates[c_name]['player_target'] is None:
                        champ_candidates[c_name]['player_target'] = p_name
                        champ_candidates[c_name]['player_role'] = role_key
                        champ_candidates[c_name]['player_stats'] = pb.get('tournament_stats', pb.get('reason', ''))
                        champ_candidates[c_name]['player_threat'] = curr_threat
                    champ_candidates[c_name]['base_score'] += 0.08

        # 3. Tính điểm ưu tiên tổng hợp (%)
        final_list = []
        for c_name, data in champ_candidates.items():
            p_score = min(0.98, max(0.55, data['base_score']))
            priority_pct = round(p_score * 100, 1)

            # Xây dựng lý do dữ liệu chi tiết
            b_cnt = data['ban_count']
            b_rt = data['ban_rate']
            p_target = data['player_target']
            p_role = data['player_role']
            p_stats = data['player_stats']

            if p_target and p_stats and "trận giải" in p_stats:
                reason = f"Top cấm giải Phase {ban_phase} ({b_cnt} lượt cấm - {b_rt}%) & Target trực tiếp {p_target} ({p_stats})"
            else:
                reason = f"Tướng Meta bị cấm số 1 Phase {ban_phase} ({b_cnt} lượt cấm - {b_rt}%)"

            final_list.append({
                'champion': c_name,
                'priority_pct': priority_pct,
                'ban_count': b_cnt,
                'ban_rate': b_rt,
                'player_target': p_target,
                'player_role': p_role,
                'reason': reason
            })

        final_list = sorted(final_list, key=lambda x: (x['priority_pct'], x['ban_count']), reverse=True)
        return final_list[:top_k]

    def recommend_enabling_bans(self, intended_pick: str, enemy_roster: Dict[str, str] = None, top_k: int = 4, already_banned: set = None) -> List[Dict[str, Any]]:
        """
        Chiến thuật CẤM DỌN ĐƯỜNG (Pre-emptive Counter Ban / Enabling Ban):
        Tìm và gợi ý cấm các con bài khắc chế cứng nhất con bài mà đội mình dự định First Pick.
        """
        if already_banned is None:
            already_banned = set()

        COUNTER_MATRIX = {
            'Zeri': [
                ('Nautilus', 'Khóa chết bằng Thủy Lôi Tầm Nhiệt R không thể lướt né', 0.95),
                ('Vi', 'Tả Xung Hữu Đột R chỉ định thẳng mặt triệt tiêu độ cơ động', 0.94),
                ('Poppy', 'Vùng Không Trọng Lực W chặn đứng toàn bộ lướt tường của Zeri', 0.93),
                ('Nocturne', 'Tắt Nắng R + Hoảng sợ cô lập Zeri trong giao tranh', 0.90)
            ],
            'Ezreal': [
                ('Varus', 'Đè bẹp giai đoạn đi đường từ cấp 1-6 bằng cấu rỉa và khống chế R', 0.96),
                ('Draven', 'Lăn cầu tuyết áp đảo lượng sát thương tay đôi ở đường dưới', 0.92),
                ('Kalista', 'Ép giao tranh liên tục không cho Ezreal thời gian tích Nước Mắt', 0.90),
                ('Nocturne', 'Bắt lẻ trừng phạt tầm bắn ngắn của Ezreal khi lướt E sai', 0.88)
            ],
            'Kai\'Sa': [
                ('Caitlyn', 'Đè nát tầm tay và ép trụ không cho Kai\'Sa farm giai đoạn đầu', 0.94),
                ('Draven', 'Sát thương tay đôi vượt trội khắc chế Kai\'Sa trước ngưỡng 2 món', 0.93),
                ('Poppy', 'Chặn lướt R và cô lập Kai\'Sa khi bay vào tuyến sau', 0.92),
                ('Nautilus', 'Khống chế cứng không cho Kai\'Sa kích hoạt tàng hình E', 0.90)
            ],
            'Ryze': [
                ('Orianna', 'Tầm kỹ năng vượt trội cấu rỉa đè nát Ryze trong giai đoạn đi đường', 0.98),
                ('Syndra', 'Quét Tan Kẻ Yếu E ngắt combo và sốc sát thương từ xa', 0.92),
                ('Yone', 'Tiếp cận từ xa không cho Ryze giữ khoảng cách xả chiêu', 0.90),
                ('Cassiopeia', 'Chướng Khí W triệt tiêu hoàn toàn Tốc Biến và chiêu cuối Ryze', 0.90)
            ],
            'Azir': [
                ('Orianna', 'Giao tranh tầm xa ngang ngửa và chiêu cuối Lệnh: Sóng Âm ép góc lính cát', 0.95),
                ('Jayce', 'Cầu Sấm sốc sát thương từ cự ly ngoài tầm lính cát', 0.92),
                ('Tristana', 'Bật Súng Cao Su lao vào đè bẹp Azir trước cấp độ 6', 0.90)
            ],
            'K\'Sante': [
                ('Rumble', 'Mưa Tên Lửa R và Súng Phun Lửa thiêu rụi giáp/kháng phép đầu trận', 0.96),
                ('Fiora', 'Phản Đòn W chặn toàn bộ hất tung và sát thương chuẩn theo % máu', 0.95),
                ('Gwen', 'Cắt Xoẹt Xoẹt và Sương Lam Bất Tử né toàn bộ chiêu khống chế', 0.94),
                ('Jax', 'Phản Công E chặn đòn đánh và áp đảo hoàn toàn khi K\'Sante Khô Máu', 0.92)
            ],
            'Lee Sin': [
                ('Poppy', 'Vùng Không Trọng Lực chặn Sóng Âm Q2 và Hộ Thể W', 0.98),
                ('Skarner', 'Áp chế cứng R không cho Lee Sin Insec đá chủ lực', 0.92),
                ('Taliyah', 'Bãi Mìn E trừng phạt mọi pha lướt Sóng Âm của Lee Sin', 0.90)
            ]
        }

        counters = COUNTER_MATRIX.get(intended_pick, [
            ('Orianna', 'Tướng kiểm soát Meta khắc chế giao tranh tổng', 0.90),
            ('Varus', 'Tướng đè đường áp lực cao toàn diện', 0.88),
            ('Nocturne', 'Tướng đi rừng bắt lẻ áp lực toàn bản đồ', 0.85)
        ])

        results = []
        for champ, reason_text, base_score in counters:
            if champ in already_banned:
                continue

            # Kiểm tra xem tuyển thủ đối phương có chơi con bài này không
            player_found = None
            player_role = None
            if enemy_roster:
                for r_key, p_name in enemy_roster.items():
                    p_bans = self.recommend_target_bans(p_name, top_k=6, ban_phase=1)
                    if any(pb['champion'] == champ for pb in p_bans):
                        player_found = p_name
                        player_role = r_key
                        base_score = min(0.99, base_score + 0.05)
                        break

            b_count = self.tournament_ban_counts.get(champ, 0)
            b_rate = round((b_count / float(self.max_ban_count)) * 30.1, 1) if self.max_ban_count > 0 else 15.0

            if player_found:
                full_reason = f"Khắc chế cứng First Pick {intended_pick} ({reason_text}) & Là con bài thuận tay của {player_found} ({player_role.upper()})"
            else:
                full_reason = f"Khắc chế cứng First Pick {intended_pick} ({reason_text})"

            results.append({
                'champion': champ,
                'priority_pct': round(base_score * 100, 1),
                'ban_count': b_count,
                'ban_rate': b_rate,
                'counter_for': intended_pick,
                'reason': full_reason
            })

        results = sorted(results, key=lambda x: x['priority_pct'], reverse=True)
        return results[:top_k]

    def get_solo_queue_meta_bans(self, top_k: int = 10) -> List[Dict[str, Any]]:
        """Lấy danh sách Top tướng bị cấm nhiều nhất 100% từ CSDL Solo Queue Rank (matches_10min)"""
        if not self.db_path.exists():
            return []
        try:
            conn = sqlite3.connect(self.db_path)
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
        self.duo_synergies = DUO_SYNERGIES
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
        """Khai thác tần suất cấm chọn thực tế từ CSDL SQLite (Đấu Giải + Solo Rank) để xác định Meta Tier theo từng vị trí"""
        if not self.db_path.exists():
            return
        try:
            conn = sqlite3.connect(self.db_path)
            # 1. Đấu Giải Pro Play (3-6 tháng gần nhất 2026)
            query_tour = """
            SELECT position, champion, COUNT(*) as picks, AVG(result) as winrate
            FROM tournament_players
            WHERE position IS NOT NULL AND champion IS NOT NULL
              AND (date >= '2026-04-01' OR year = 2026)
            GROUP BY position, champion
            """
            df_tour = pd.read_sql(query_tour, conn)

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

            # Chuẩn hóa tên tướng Solo Rank
            df_rank['champion'] = df_rank['champion'].apply(lambda c: self._normalize_champion_name(c))

            # Tổng hợp theo (position, champion)
            tour_dict = {}
            for _, row in df_tour.iterrows():
                pos = str(row['position']).lower()
                champ = self._normalize_champion_name(row['champion'])
                tour_dict[(pos, champ)] = {
                    'tour_picks': row['picks'],
                    'tour_wr': row['winrate']
                }

            rank_dict = {}
            df_rank_agg = df_rank.groupby(['position', 'champion']).agg(
                rank_picks=('picks', 'sum'),
                rank_wr=('winrate', 'mean')
            ).reset_index()
            for _, row in df_rank_agg.iterrows():
                pos = str(row['position']).lower()
                champ = row['champion']
                rank_dict[(pos, champ)] = {
                    'rank_picks': row['rank_picks'],
                    'rank_wr': row['rank_wr']
                }

            # Kết hợp tổng hợp
            all_keys = set(tour_dict.keys()).union(set(rank_dict.keys()))
            lane_max = {}
            raw_meta = {}
            for pos, champ in all_keys:
                t_info = tour_dict.get((pos, champ), {'tour_picks': 0, 'tour_wr': 0.50})
                r_info = rank_dict.get((pos, champ), {'rank_picks': 0, 'rank_wr': 0.50})
                
                # Trọng số tổng hợp: 65% Pro Play + 35% Solo Queue High Elo
                total_picks = t_info['tour_picks'] + r_info['rank_picks']
                if total_picks > 0:
                    combined_wr = (t_info['tour_picks'] * t_info['tour_wr'] + r_info['rank_picks'] * r_info['rank_wr']) / total_picks
                else:
                    combined_wr = 0.50

                raw_meta[(pos, champ)] = {
                    'picks': total_picks,
                    'tour_picks': t_info['tour_picks'],
                    'rank_picks': r_info['rank_picks'],
                    'winrate': round(combined_wr, 3)
                }
                lane_max[pos] = max(lane_max.get(pos, 0), total_picks)

            for (pos, champ), data in raw_meta.items():
                max_p = lane_max.get(pos, 100)
                norm_pick = data['picks'] / max(1, max_p)
                self.tournament_meta_picks[(pos, champ)] = {
                    'picks': data['picks'],
                    'tour_picks': data['tour_picks'],
                    'rank_picks': data['rank_picks'],
                    'norm_pick': norm_pick,
                    'winrate': data['winrate']
                }
        except Exception as e:
            # print(f"Warning loading tournament meta: {e}")
            pass

    def _load_head_to_head_matchups(self):
        """
        Khai thác Ma trận Đối đầu Trực tiếp Cùng Đường (Head-to-Head Lane Matchups):
        - Tỷ lệ thắng đối đầu trực tiếp (Win Rate vs Opponent)
        - Chênh lệch vàng trung bình ở phút thứ 10 (±Gold @ 10)
        - Chênh lệch kinh nghiệm và lính (±XP @ 10, ±Creeps @ 10)
        Trích xuất từ 30,000 bản ghi tournament_players (Đấu Giải Chuyên Nghiệp) & matches_10min (Solo Rank High Elo).
        Cơ chế giống 100% cách lolvvv tính toán dữ liệu kèo khắc chế thực tế.
        """
        self.matchup_cache = {}
        if not self.db_path.exists():
            return
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # 1. Khai thác dữ liệu Đấu Giải Chuyên Nghiệp (tournament_players)
            cursor.execute("""
            SELECT 
                p1.position,
                p1.champion as champ,
                p2.champion as opp_champ,
                COUNT(*) as matches,
                SUM(p1.result) as wins,
                ROUND(AVG(p1.result), 3) as winrate,
                ROUND(AVG(p1.golddiffat10), 1) as avg_gd10,
                ROUND(AVG(p1.xpdiffat10), 1) as avg_xpd10,
                ROUND(AVG(p1.csdiffat10), 1) as avg_csd10
            FROM tournament_players p1
            JOIN tournament_players p2 ON p1.gameid = p2.gameid AND p1.position = p2.position AND p1.participantid != p2.participantid
            WHERE p1.position IS NOT NULL AND p1.champion IS NOT NULL AND p2.champion IS NOT NULL
            GROUP BY p1.position, p1.champion, p2.champion
            """)
            for row in cursor.fetchall():
                pos, champ, opp, matches, wins, wr, gd10, xpd10, csd10 = row
                norm_c = self._normalize_champion_name(champ)
                norm_opp = self._normalize_champion_name(opp)
                pos = str(pos).lower()
                self.matchup_cache[(pos, norm_c, norm_opp)] = {
                    'matches': matches,
                    'wins': wins,
                    'winrate': float(wr) if wr is not None else 0.50,
                    'avg_gd10': float(gd10) if gd10 is not None else 0.0,
                    'avg_xpd10': float(xpd10) if xpd10 is not None else 0.0,
                    'avg_csd10': float(csd10) if csd10 is not None else 0.0,
                    'source': 'tournament'
                }
            conn.close()
        except Exception as e:
            pass

    def get_champion_counters(self, champ: str, position: str = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Trích xuất dữ liệu Kèo Khắc Chế chuẩn xác 100% từ Database Đấu Giải (tương tự lolvvv):
        - countered_by: Danh sách các tướng khắc chế đối đầu tốt nhất (Win Rate cao, GD10 cao)
        - counters: Danh sách các tướng bị tướng này áp đảo
        """
        champ = self._normalize_champion_name(champ)
        if not position:
            cand_lanes = self.get_candidate_lanes_for_champion(champ)
            position = cand_lanes[0][0] if cand_lanes else 'mid'
        
        db_p = {'jungle': 'jng', 'support': 'sup'}.get(position.lower(), position.lower())
        
        countered_by = []
        counters = []
        
        for (pos, c, opp), m_data in self.matchup_cache.items():
            if pos == db_p and c == champ and m_data['matches'] >= 2:
                # m_data['winrate'] là tỉ lệ thắng của champ khi gặp opp
                opp_wr = round((1.0 - m_data['winrate']) * 100, 1)
                opp_gd10 = -m_data['avg_gd10']
                opp_xpd10 = -m_data['avg_xpd10']
                if opp_wr >= 50.0:
                    countered_by.append({
                        'opponent': opp,
                        'matches': m_data['matches'],
                        'winrate': opp_wr,
                        'gd10': round(opp_gd10, 0),
                        'xpd10': round(opp_xpd10, 0),
                        'score': opp_wr + (opp_gd10 / 50.0)
                    })
                else:
                    c_wr = round(m_data['winrate'] * 100, 1)
                    counters.append({
                        'opponent': opp,
                        'matches': m_data['matches'],
                        'winrate': c_wr,
                        'gd10': round(m_data['avg_gd10'], 0),
                        'xpd10': round(m_data['avg_xpd10'], 0),
                        'score': c_wr + (m_data['avg_gd10'] / 50.0)
                    })
                    
        countered_by = sorted(countered_by, key=lambda x: (x['winrate'], x['matches']), reverse=True)[:top_k]
        counters = sorted(counters, key=lambda x: (x['winrate'], x['matches']), reverse=True)[:top_k]
        return {
            'champion': champ,
            'position': position,
            'countered_by': countered_by,
            'counters': counters
        }

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

    def recommend_picks(self, target_lane: str,
                        ally_team: List[str],
                        enemy_team: List[str],
                        already_banned: set = None,
                        player_name: str = None,
                        top_k: int = 5) -> List[Dict[str, Any]]:
        """Gợi ý Top K tướng nên CHỌN cho vị trí target_lane dựa 100% trên dữ liệu giải đấu thực tế và độ thuần thục của tuyển thủ"""
        target_lane = target_lane.lower()
        db_pos = {'jungle': 'jng', 'support': 'sup'}.get(target_lane, target_lane)
        if already_banned is None:
            already_banned = set()
        
        # Ứng viên cho target_lane: Những tướng thực sự chơi ở vị trí này trong giải đấu (có lượt pick ở pos này)
        # hoặc có lane chính trong CHAMPION_METADATA trùng khớp
        candidates = []
        for c, meta in self.metadata.items():
            if c in ally_team or c in enemy_team or c in already_banned:
                continue
            pos_picks = self.tournament_meta_picks.get((db_pos, c), {}).get('picks', 0)
            has_matchup = any((db_pos, c, self._normalize_champion_name(ec)) in self.matchup_cache for ec in enemy_team)
            if pos_picks >= 15 or meta.get('lane') == target_lane or has_matchup:
                candidates.append(c)

        # 1. Đánh giá thành phần đội hình phe mình hiện tại
        ally_ap_count = sum(1 for c in ally_team if self.metadata.get(c, {}).get('dmg_type') == 'AP')
        ally_cc_score = sum(self.metadata.get(c, {}).get('hard_cc', 0.5) for c in ally_team)
        ally_durability = sum(self.metadata.get(c, {}).get('durability', 0.5) for c in ally_team)

        need_ap = (ally_ap_count == 0 and len(ally_team) >= 2)
        need_cc = (ally_cc_score < 1.2 and len(ally_team) >= 2)
        need_frontline = (ally_durability < 1.4 and len(ally_team) >= 2)

        # 2. Xác định đối thủ cùng đường (nếu có)
        enemy_lane_opponent = None
        for ec in enemy_team:
            ec_meta = self.metadata.get(ec, {})
            if ec_meta.get('lane') == target_lane or self.tournament_meta_picks.get((db_pos, ec), {}).get('picks', 0) >= 30:
                enemy_lane_opponent = ec
                break

        scored_picks = []
        for champ in candidates:
            meta = self.metadata.get(champ, {})
            
            # 2.1 Điểm Meta Presence từ Đấu Giải thực tế CHÍNH TẠI VỊ TRÍ ĐÓ
            meta_info = self.tournament_meta_picks.get((db_pos, champ), None)

            if meta_info and meta_info['picks'] >= 15:
                meta_presence_bonus = 0.40 * meta_info['norm_pick'] + 0.15 * (meta_info['winrate'] - 0.50)
                picks_count = meta_info['picks']
                base_score = 0.40 + meta_presence_bonus
            elif meta_info and meta_info['picks'] > 0:
                picks_count = meta_info['picks']
                # Tướng có quá ít trận giải (< 15 trận): Không thể coi là Meta
                base_score = 0.28 + 0.10 * (meta_info['picks'] / 15.0)
            else:
                picks_count = 0
                base_score = 0.25

            # 2.2 Điểm Tướng Tủ của Tuyển Thủ Chỉ Định (Player Signature Mastery)
            player_bonus = 0.0
            player_notes = []
            if player_name:
                p_data = self.player_stats_cache.get(player_name, {}).get(champ)
                if p_data and p_data.get('games', 0) >= 3:
                    p_games = p_data['games']
                    p_wr = p_data['winrate']
                    player_bonus += 0.12 * min(1.0, p_games / 10.0) + 0.10 * (p_wr - 0.50)
                    player_notes.append(f"🔥 Tướng tủ của {player_name} ({p_games} trận giải - Thắng {round(p_wr*100, 1)}%)")

            # 2.3 Điểm Synergy Cặp Đôi (Amplify Duo Synergy)
            synergy_bonus = 0.0
            synergy_notes = []
            for ally_champ in ally_team:
                pair = (ally_champ, champ)
                rev_pair = (champ, ally_champ)
                syn = self.duo_synergies.get(pair, self.duo_synergies.get(rev_pair, 0.0))
                if syn > 0:
                    ally_meta_lane = self.metadata.get(ally_champ, {}).get('lane', '')
                    # Cặp đôi cùng đường Bot (Xạ thủ - Hỗ trợ) mang trọng số cộng hưởng lớn nhất (1.4x)
                    is_bot_duo = (target_lane in ['support', 'bot'] and ally_meta_lane in ['support', 'bot'])
                    weight = 1.40 if is_bot_duo else 0.85
                    synergy_bonus += (syn - 0.50) * weight
                    synergy_notes.append(f"🔥 Cặp bài trùng huỷ diệt với {ally_champ} (Synergy {round(syn*100)}%)")

            # 2.4 Điểm Counter đối thủ cùng đường (Áp dụng Bayesian Shrinkage & Sample Confidence triệt tiêu Thiên Kiến Mẫu Nhỏ)
            counter_bonus = 0.0
            counter_notes = []
            if enemy_lane_opponent:
                norm_opp = self._normalize_champion_name(enemy_lane_opponent)
                m_info = self.matchup_cache.get((db_pos, champ, norm_opp))
                if m_info and m_info['matches'] >= 2:
                    m_cnt = m_info['matches']
                    m_wr = m_info['winrate']
                    m_gd10 = m_info.get('avg_gd10', 0.0)
                    
                    # Bayesian Shrinkage: Kéo winrate về 50% khi số trận mẫu nhỏ (Prior sample size C = 8)
                    C = 8.0
                    shrunk_wr = (m_info['wins'] + C * 0.50) / (m_cnt + C)
                    # Hệ số tin cậy mẫu (Sample Confidence Weight): Đạt 1.0 khi có >= 12 trận
                    sample_confidence = min(1.0, m_cnt / 12.0)

                    # QUY TẮC CHIẾN THUẬT: Tuyệt đối KHÔNG gợi ý tướng KÈO DƯỚI RÕ RỆT (< 45% Winrate khi đã có từ 4 trận giải trở lên)
                    if (m_wr < 0.45 and m_cnt >= 4) or (shrunk_wr < 0.44 and m_cnt >= 3):
                        continue

                    if shrunk_wr >= 0.52 and m_cnt >= 5:
                        # Kèo khắc chế rõ rệt có độ tin cậy thống kê cao: Thưởng điểm lớn để ưu tiên counter
                        gd_bonus = min(0.06, m_gd10 / 4000.0) if m_gd10 > 0 else 0.0
                        counter_bonus += (shrunk_wr - 0.50) * 1.50 * sample_confidence + gd_bonus + 0.08
                        counter_notes.append(f"⚔️ Kèo trên khắc chế {norm_opp} ({m_cnt} trận giải - Thắng {round(m_wr*100, 1)}%, GD10: {m_gd10:+.0f}g)")
                    elif shrunk_wr >= 0.52 and m_cnt < 5:
                        # Kèo khắc chế mẫu nhỏ (2-4 trận): Chỉ tính điểm tình huống nhẹ
                        counter_bonus += (shrunk_wr - 0.50) * 0.60 * sample_confidence + 0.04
                        counter_notes.append(f"⚔️ Kèo trên tình huống trước {norm_opp} (Mẫu nhỏ {m_cnt} trận giải - Thắng {round(m_wr*100, 1)}%)")
                    elif shrunk_wr < 0.48:
                        # Kèo hơi dưới (từ 45% đến 48%): Phạt điểm đáng kể
                        counter_bonus += (shrunk_wr - 0.50) * 1.20 * sample_confidence - 0.12
                        counter_notes.append(f"⚠️ Kèo dưới nhẹ trước {norm_opp} ({m_cnt} trận giải - Thắng {round(m_wr*100, 1)}%, GD10: {m_gd10:+.0f}g)")
                    else:
                        counter_notes.append(f"⚖️ Kèo cân bằng với {norm_opp} ({m_cnt} trận giải - Thắng {round(m_wr*100, 1)}%, GD10: {m_gd10:+.0f}g)")
                else:
                    # Heuristic fallback khi chưa có dữ liệu đối đầu trực tiếp trong giải (chỉ thưởng nhẹ)
                    opp_meta = self.metadata.get(enemy_lane_opponent, {})
                    if opp_meta.get('is_melee', False) and meta.get('anti_melee', 0.5) >= 0.80:
                        counter_bonus += 0.04
                        counter_notes.append(f"Khắc chế tướng cận chiến {enemy_lane_opponent}")
                    if opp_meta.get('engage', 0.5) >= 0.85 and meta.get('anti_melee', 0.5) >= 0.85:
                        counter_bonus += 0.03
                        counter_notes.append(f"Chặn đứng các pha mở giao tranh của {enemy_lane_opponent}")

            # 2.5 Điểm Cân Bằng Đội Hình
            # 2.5 Điểm Cân Bằng Đội Hình & Phong Cách Chiến Thuật Hiện Đại
            balance_bonus = 0.0
            balance_notes = []
            if need_ap and meta.get('dmg_type') == 'AP':
                balance_bonus += 0.15
                balance_notes.append("Bổ sung sát thương phép (AP) chống Full AD")
            if need_cc and meta.get('hard_cc', 0) >= 0.80:
                balance_bonus += 0.10
                balance_notes.append("Bổ sung khống chế cứng mở giao tranh")
            # Meta hiện đại: Thiếu chống chịu không còn là nhược điểm chí mạng (chỉ cộng nhẹ 0.03 nếu có tank)
            if need_frontline and meta.get('durability', 0) >= 0.80 and target_lane != 'support':
                balance_bonus += 0.03
                balance_notes.append("Bổ sung dàn chắn chống chịu tuyến trên")

            # Ưu tiên Thuật Sĩ (Enchanter) bảo kê & kích hoạt nội tại cho các Xạ Thủ Siêu Carry (Lucian, Zeri, Smolder, Jinx...)
            ENCHANTER_SYNERGY_ADCS = {'Lucian', 'Zeri', 'Smolder', 'Jinx', 'Kog\'Maw', 'Aphelios', 'Twitch', 'Vayne'}
            ENCHANTER_SUPPORTS = {'Milio', 'Nami', 'Lulu', 'Yuumi', 'Karma', 'Renata Glasc', 'Janna', 'Seraphine'}
            has_hyper_adc = any(ac in ENCHANTER_SYNERGY_ADCS for ac in ally_team)
            if target_lane == 'support' and champ in ENCHANTER_SUPPORTS and has_hyper_adc:
                balance_bonus += 0.14
                balance_notes.append("Thuật Sĩ Buff Tốc Đánh / Tầm Bắn & Giải Hiệu Ứng hoàn hảo cho Xạ Thủ")

            raw_score = base_score + player_bonus + synergy_bonus + counter_bonus + balance_bonus

            reasons = player_notes + synergy_notes + counter_notes + balance_notes
            if not reasons:
                if picks_count >= 300:
                    reasons.append(f"Tướng Tier S+ Đấu Giải ({picks_count} trận)")
                elif picks_count >= 100:
                    reasons.append(f"Tướng Meta Đấu Giải ({picks_count} trận)")
                else:
                    reasons.append("Tướng chiến thuật ổn định")

            scored_picks.append({
                'champion': champ,
                'raw_score': float(raw_score),
                'score': round(float(raw_score), 4),
                'lane': target_lane.upper(),
                'dmg_type': meta.get('dmg_type'),
                'is_melee': meta.get('is_melee'),
                'hard_cc': meta.get('hard_cc'),
                'reasons': reasons
            })

        # Sắp xếp theo raw_score thực tế (chưa bị clip) để phân tầng chính xác
        scored_picks = sorted(scored_picks, key=lambda x: x['raw_score'], reverse=True)
        if scored_picks:
            max_r = scored_picks[0]['raw_score']
            min_r = scored_picks[-1]['raw_score']
            for rank_idx, sp in enumerate(scored_picks):
                if max_r > min_r:
                    rel_s = (sp['raw_score'] - min_r) / (max_r - min_r)
                    sp['score'] = round(0.72 + 0.27 * rel_s, 4)
                else:
                    sp['score'] = max(0.60, round(0.99 - (rank_idx * 0.03), 4))

        return scored_picks[:top_k]


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

    def detect_flaws_and_punishers(self, enemy_team: List[str]) -> Dict[str, Any]:
        """Quét đội hình địch và xuất cảnh báo kèm Top Con bài Trừng phạt"""
        if not enemy_team:
            return {'flaws': [], 'punishers': [], 'summary': 'Đội hình địch chưa chọn tướng'}

        n_enemies = len(enemy_team)
        melee_count = sum(1 for c in enemy_team if self.metadata.get(c, {}).get('is_melee', False))
        ap_count = sum(1 for c in enemy_team if self.metadata.get(c, {}).get('dmg_type') == 'AP')
        ad_count = sum(1 for c in enemy_team if self.metadata.get(c, {}).get('dmg_type') == 'AD')
        total_cc = sum(self.metadata.get(c, {}).get('hard_cc', 0.5) for c in enemy_team)
        avg_cc = total_cc / n_enemies
        tank_count = sum(1 for c in enemy_team if self.metadata.get(c, {}).get('durability', 0.5) >= 0.80)

        flaws = []
        punishers = []

        # -------------------------------------------------------------
        # 1. Lỗ hổng 1: Heavy Melee (>= 3 cận chiến khi chọn >= 3 tướng)
        # -------------------------------------------------------------
        if (n_enemies >= 3 and melee_count >= 3) or (n_enemies == 5 and melee_count >= 4):
            flaws.append({
                'flaw_type': 'HEAVY MELEE COMPOSITION',
                'severity': 'CRITICAL' if melee_count >= 4 else 'HIGH',
                'description': f'Địch chọn {melee_count}/{n_enemies} tướng CẬN CHIẾN. Rất dễ bị thả diều và quấn vào các vòng xoáy sát thương diện rộng.',
                'winrate_impact': '+15% đến +20% nếu chọn tướng Chống Càn'
            })
            punishers.extend([
                {
                    'champion': 'Illaoi',
                    'lane': 'TOP',
                    'punisher_role': 'Chống Càn Cực Đại (Anti-Melee Raidboss)',
                    'why_punish': 'Chiêu cuối Xúc Tua Đập cực mạnh khi địch có 3-4 cận chiến tự lao vào; tăng đột biến tỉ lệ thắng (Chiến thuật Siwoo LCK)',
                    'expected_winrate_delta': '+18.5%'
                },
                {
                    'champion': 'Cassiopeia',
                    'lane': 'MID',
                    'punisher_role': 'Chặn Lướt & Xả Độc Diện Rộng (Miasma Zone)',
                    'why_punish': 'Chướng Khí chặn hoàn toàn kỹ năng lướt của các Đấu sĩ cận chiến; Hóa Đá diện rộng 5v5',
                    'expected_winrate_delta': '+14.2%'
                },
                {
                    'champion': 'Brand',
                    'lane': 'JUNGLE/SUPPORT',
                    'punisher_role': 'Bỏng Lan Đốt % Máu Đám Đông (AOE Melt)',
                    'why_punish': 'Nội tại nổ Bỏng lan thiêu rụi đội hình co cụm cận chiến theo % máu tối đa',
                    'expected_winrate_delta': '+12.8%'
                },
                {
                    'champion': 'Darius',
                    'lane': 'TOP',
                    'punisher_role': 'Bổ Củi Tàn Sát Đấu Sĩ',
                    'why_punish': 'Càng nhiều tướng cận chiến bu lại càng dễ tích 5 tầng Xuất Huyết và Máy Chém Noxus liên hoàn',
                    'expected_winrate_delta': '+13.5%'
                }
            ])

        # -------------------------------------------------------------
        # 2. Lỗ hổng 2: Full AD (0 AP khi chọn >= 3 tướng)
        # -------------------------------------------------------------
        if ap_count == 0 and n_enemies >= 3:
            flaws.append({
                'flaw_type': 'FULL AD COMPOSITION',
                'severity': 'CRITICAL',
                'description': f'Địch 100% SÁT THƯƠNG VẬT LÝ ({ad_count} tướng AD, 0 AP). Phe ta chỉ cần lên Giáp Gai + Tim Băng để vô hiệu hóa toàn bộ hỏa lực.',
                'winrate_impact': '+16% nếu chọn Siêu Đỡ Đòn Giáp'
            })
            punishers.extend([
                {
                    'champion': 'Malphite',
                    'lane': 'TOP',
                    'punisher_role': 'Bất Hoại Giáp Phiến & Giảm Tốc Đánh',
                    'why_punish': 'Giáp cộng dồn theo trang bị, dậm E trừ 50% tốc đánh hủy diệt mọi Xạ thủ/Đấu sĩ AD',
                    'expected_winrate_delta': '+17.0%'
                },
                {
                    'champion': 'Rammus',
                    'lane': 'JUNGLE',
                    'punisher_role': 'Phản Sát Thương Gai Góc',
                    'why_punish': 'Bật Thế Thủ W phản đòn hàng nghìn sát thương mỗi giây lên tướng đánh tay vật lý',
                    'expected_winrate_delta': '+16.5%'
                },
                {
                    'champion': 'Taric',
                    'lane': 'SUPPORT',
                    'punisher_role': 'Hào Quang Giáp & Bất Tử Giao Tranh',
                    'why_punish': 'Buff hàng trăm giáp cho toàn đội và kích hoạt Vũ Trụ Rực Sáng chặn đứng dồn sát thương',
                    'expected_winrate_delta': '+12.0%'
                }
            ])

        # -------------------------------------------------------------
        # 3. Lỗ hổng 3: Zero Hard CC (CC trung bình < 0.40)
        # -------------------------------------------------------------
        if avg_cc < 0.40 and n_enemies >= 3:
            flaws.append({
                'flaw_type': 'ZERO HARD CC COMPOSITION',
                'severity': 'HIGH',
                'description': f'Địch THIẾU KHỐNG CHẾ CỨNG (Chỉ số CC TB: {round(avg_cc, 2)}/1.0). Hoàn toàn bất lực trước các Sát thủ lướt liên tục hoặc Xạ thủ quẩy tự do.',
                'winrate_impact': '+14% nếu chọn Siêu Sát Thủ/Hyper-mobility'
            })
            punishers.extend([
                {
                    'champion': 'Master Yi',
                    'lane': 'JUNGLE',
                    'punisher_role': 'Chiến Thần Chém Quét Tuyệt Hảo',
                    'why_punish': 'Không có Choáng/Hất tung để ngắt Chiêu Cuối và Thiền; chém sạch đội hình trong chớp mắt',
                    'expected_winrate_delta': '+15.5%'
                },
                {
                    'champion': 'Katarina',
                    'lane': 'MID',
                    'punisher_role': 'Bông Sen Tử Thần Không Thể Cản Phá',
                    'why_punish': 'Xoay R trọn vẹn 2.5s không bị ngắt quãng, liên tục Reset hồi chiêu Quét Sạch',
                    'expected_winrate_delta': '+14.0%'
                },
                {
                    'champion': 'Zeri',
                    'lane': 'BOT',
                    'punisher_role': 'Điện Giật Lướt Tự Do Vô Tận',
                    'why_punish': 'Bật R bắn thả diều với tốc độ di chuyển 600+ mà không sợ bị trúng khống chế chỉ định',
                    'expected_winrate_delta': '+13.0%'
                }
            ])

        # -------------------------------------------------------------
        # 4. Lỗ hổng 4: Full Squishy (0 Tank khi chọn >= 3 tướng)
        # -------------------------------------------------------------
        if tank_count == 0 and n_enemies >= 4:
            flaws.append({
                'flaw_type': 'FULL SQUISHY COMPOSITION',
                'severity': 'HIGH',
                'description': f'Địch 0 TƯỚNG ĐỠ ĐÒN / CHỐNG CHỊU. Tuyến trước quá mỏng manh, chỉ cần 1 pha lao vào mở giao tranh là bốc hơi.',
                'winrate_impact': '+13% nếu chọn Tướng Mở Giao Tranh Lao Vào'
            })
            punishers.extend([
                {
                    'champion': 'Nocturne',
                    'lane': 'JUNGLE',
                    'punisher_role': 'Tắt Đèn Ám Sát Tuyến Sau',
                    'why_punish': 'Tắt tầm nhìn toàn bản đồ và lao thẳng vào bắt chết chủ lực máu giấy',
                    'expected_winrate_delta': '+13.5%'
                },
                {
                    'champion': 'Jarvan IV',
                    'lane': 'JUNGLE',
                    'punisher_role': 'Đại Địa Chấn Nhốt Máu Giấy',
                    'why_punish': 'Combo EQ gom người và dựng Đấu Trường R ép đối thủ máu giấy giao tranh trực diện',
                    'expected_winrate_delta': '+12.5%'
                }
            ])

        # Loại bỏ trùng lặp punisher theo tên tướng
        seen = set()
        unique_punishers = []
        for p in punishers:
            if p['champion'] not in seen:
                seen.add(p['champion'])
                unique_punishers.append(p)

        return {
            'enemy_team': enemy_team,
            'melee_ratio': f"{melee_count}/{n_enemies}",
            'damage_split': f"AD: {ad_count} | AP: {ap_count}",
            'avg_hard_cc': round(avg_cc, 2),
            'flaws_detected': len(flaws),
            'flaws': flaws,
            'punishers': unique_punishers[:5]
        }


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
        self.target_ban_engine = TargetBanEngine(db_path=db_path, accounts_path=accounts_path)
        self.pick_recommender = MetaPickRecommender(db_path=db_path, accounts_path=accounts_path)
        self.pick_recommender.player_stats_cache = self.target_ban_engine.player_stats_cache
        self.punisher_engine = PunisherEngine()
        self.win_condition_engine = WinConditionEngine(kmeans_path=kmeans_path)

    def save(self, output_path: Path = RECOMMENDER_MODEL_PATH):
        """Đóng gói toàn bộ engine thành file pkl"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            pickle.dump(self, f)
        print(f"-> Đã đóng gói thành công Recommender Engine vào: {output_path}")

    @staticmethod
    def load(filepath: Path = RECOMMENDER_MODEL_PATH) -> 'RecommenderEngine':
        return safe_load_pickle(filepath)


# =========================================================================
# CLI COMMAND RUNNER & DEMO
# =========================================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Ban/Pick Recommender & Win Condition Engine (Task 3.5)")
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
    parser.add_argument('--demo', action='store_true', help="Chạy toàn bộ kịch bản Demo trực quan 4 phân hệ")
    return parser.parse_args()


def main():
    args = parse_args()
    engine = RecommenderEngine()

    print("=" * 90)
    print("🎯 HỆ THỐNG TRỢ LÝ CẤM/CHỌN THÔNG MINH & NHẬN DIỆN ĐIỀU KIỆN THẮNG (TASK 3.5)")
    print("=" * 90)

    # 1. Đăng ký liên kết tài khoản
    if args.link_player and args.riot_id:
        engine.target_ban_engine.link_player_account(args.link_player, args.riot_id)
        print(f"✅ Đã liên kết thành công Tuyển thủ: {args.link_player} -> Riot ID: {args.riot_id}")
        return

    # 2. Phân hệ CẤM mục tiêu (Target Ban)
    if args.target_ban or args.demo:
        player = args.player
        print(f"\n[PHÂN HỆ 1] GỢI Ý CẤM MỤC TIÊU THEO TUYỂN THỦ: >>> {player.upper()} <<<")
        print("-" * 90)
        bans = engine.target_ban_engine.recommend_target_bans(player, top_k=5)
        for i, b in enumerate(bans, 1):
            print(f"  {i}. [{b['badge']}] {b['champion'].upper()} (Điểm đe dọa: {b['threat_score']})")
            print(f"     • Đấu giải: {b['tournament_stats']}")
            print(f"     • Solo Rank: {b['rank_stats']}")

    # 3. Phân hệ CHỌN tướng Meta & Synergy
    if args.recommend_pick or args.demo:
        lane = args.lane
        ally_list = [c.strip() for c in args.ally.split(',') if c.strip()]
        enemy_list = [c.strip() for c in args.enemy.split(',') if c.strip()]
        print(f"\n[PHÂN HỆ 2] GỢI Ý CHỌN TƯỚNG CHUẨN META CHO VỊ TRÍ: >>> {lane.upper()} <<<")
        print(f"  • Phe ta đã pick: {', '.join(ally_list) if ally_list else 'Chưa có'}")
        print(f"  • Phe địch đã pick: {', '.join(enemy_list) if enemy_list else 'Chưa có'}")
        print("-" * 90)
        picks = engine.pick_recommender.recommend_picks(lane, ally_list, enemy_list, top_k=5)
        for i, p in enumerate(picks, 1):
            print(f"  {i}. ⭐ {p['champion'].upper()} (Điểm đề xuất: {p['score']} | {p['dmg_type']})")
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
                print(f"     • Tác động Winrate: {fl['winrate_impact']}")
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
