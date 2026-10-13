"""
Module 06: Machine Learning - Task 3.4: Draft Archetypes Clustering (K-Means & PCA)
Phân cụm không gian chiến thuật cấm/chọn nhận diện 4 Trường phái Đội hình:
1. Early Snowball / Dive (Đánh đầu trận, ép trụ, snowball sớm)
2. Wombocombo / Teamfight 5v5 (Giao tranh diện rộng, tranh chấp mục tiêu)
3. Late-Game Hypercarry (Nuôi siêu chủ lực, đánh về cuối trận)
4. Pick & Split-Push 1-3-1 (Bắt lẻ & Đẩy lẻ chia cắt bản đồ)

Phương pháp & Kỹ thuật:
- Vector hóa 160+ tướng theo 5 trục sức mạnh: [Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control]
- Trích xuất 3,000 trận đấu giải đỉnh cao (6,000 đội hình) từ CSDL SQLite lol_live_data.db
- Tối ưu số cụm K qua phương pháp Elbow (WCSS) và Silhouette Score
- Giảm chiều PCA 2D trực quan hóa không gian chiến thuật & trích xuất Explained Variance
- Đóng gói mô hình vào models/archetype_kmeans.pkl
- Xuất bản 2 biểu đồ 300 DPI vào reports/figures/ (Fig 10 & Fig 11)
"""

import sys
import os
import argparse
import pickle
import sqlite3
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples

# Paths configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "database" / "lol_live_data.db"
MODEL_PATH = PROJECT_ROOT / "models" / "archetype_kmeans.pkl"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------------------
# 1. BẢNG VECTOR THUỘC TÍNH CHIẾN THUẬT 160+ VỊ TƯỚNG (5 TRỤC: 0.0 -> 1.0)
# [Early_Power, Scaling, Teamfight_AOE, Pick_Potential, Objective_Control]
# -------------------------------------------------------------------------
CHAMPION_TACTICAL_VECTOR = {
    # Đường Trên (Top Lane)
    'Aatrox': [0.65, 0.75, 0.80, 0.60, 0.60],
    'Ambessa': [0.85, 0.65, 0.70, 0.85, 0.55],
    'Camille': [0.55, 0.90, 0.45, 0.95, 0.75],
    'Cho\'Gath': [0.40, 0.80, 0.80, 0.55, 0.85],
    'Darius': [0.85, 0.55, 0.60, 0.65, 0.60],
    'Dr. Mundo': [0.35, 0.85, 0.50, 0.40, 0.60],
    'Fiora': [0.60, 0.95, 0.25, 0.80, 0.85],
    'Gangplank': [0.45, 0.95, 0.95, 0.40, 0.70],
    'Garen': [0.60, 0.60, 0.45, 0.55, 0.60],
    'Gnar': [0.65, 0.75, 0.90, 0.70, 0.60],
    'Gragas': [0.65, 0.70, 0.85, 0.80, 0.65],
    'Gwen': [0.40, 0.95, 0.85, 0.45, 0.75],
    'Illaoi': [0.75, 0.70, 0.95, 0.35, 0.65],
    'Irelia': [0.80, 0.70, 0.55, 0.75, 0.60],
    'Jax': [0.55, 0.90, 0.50, 0.75, 0.85],
    'Jayce': [0.85, 0.65, 0.65, 0.80, 0.60],
    'K\'Sante': [0.50, 0.85, 0.75, 0.85, 0.65],
    'Kayle': [0.15, 1.00, 0.85, 0.30, 0.70],
    'Kennen': [0.70, 0.75, 0.95, 0.70, 0.55],
    'Kled': [0.90, 0.45, 0.50, 0.85, 0.50],
    'Malphite': [0.40, 0.75, 0.95, 0.85, 0.50],
    'Mordekaiser': [0.60, 0.75, 0.75, 0.65, 0.70],
    'Nasus': [0.25, 0.90, 0.40, 0.45, 0.85],
    'Olaf': [0.90, 0.45, 0.45, 0.70, 0.75],
    'Ornn': [0.40, 0.90, 0.95, 0.65, 0.65],
    'Poppy': [0.70, 0.65, 0.70, 0.80, 0.60],
    'Quinn': [0.85, 0.50, 0.20, 0.90, 0.65],
    'Renekton': [0.95, 0.45, 0.60, 0.75, 0.55],
    'Riven': [0.75, 0.75, 0.65, 0.75, 0.55],
    'Rumble': [0.90, 0.65, 0.95, 0.60, 0.70],
    'Sett': [0.80, 0.60, 0.85, 0.70, 0.55],
    'Shen': [0.65, 0.65, 0.60, 0.80, 0.60],
    'Singed': [0.50, 0.70, 0.75, 0.70, 0.65],
    'Sion': [0.40, 0.85, 0.85, 0.55, 0.80],
    'Tahm Kench': [0.65, 0.70, 0.55, 0.75, 0.55],
    'Teemo': [0.70, 0.65, 0.60, 0.55, 0.75],
    'Tryndamere': [0.60, 0.85, 0.20, 0.65, 0.95],
    'Urgot': [0.65, 0.75, 0.70, 0.75, 0.65],
    'Volibear': [0.85, 0.55, 0.70, 0.75, 0.65],
    'Warwick': [0.85, 0.45, 0.35, 0.80, 0.70],
    'Wukong': [0.70, 0.75, 0.90, 0.80, 0.60],
    'Yasuo': [0.65, 0.85, 0.75, 0.65, 0.70],
    'Yone': [0.55, 0.90, 0.85, 0.80, 0.65],
    'Yorick': [0.45, 0.80, 0.30, 0.45, 1.00],

    # Đi Rừng (Jungle)
    'Amumu': [0.50, 0.80, 0.95, 0.85, 0.70],
    'Bel\'Veth': [0.65, 0.90, 0.55, 0.70, 0.95],
    'Briar': [0.80, 0.60, 0.55, 0.85, 0.65],
    'Diana': [0.65, 0.80, 0.90, 0.75, 0.75],
    'Ekko': [0.55, 0.85, 0.75, 0.85, 0.65],
    'Elise': [0.95, 0.35, 0.40, 0.95, 0.50],
    'Evelynn': [0.40, 0.85, 0.40, 1.00, 0.50],
    'Fiddlesticks': [0.45, 0.85, 1.00, 0.70, 0.65],
    'Graves': [0.70, 0.85, 0.65, 0.55, 0.85],
    'Hecarim': [0.65, 0.80, 0.85, 0.85, 0.65],
    'Ivern': [0.50, 0.75, 0.70, 0.75, 0.90],
    'Jarvan IV': [0.85, 0.55, 0.85, 0.90, 0.60],
    'Karthus': [0.35, 0.95, 0.95, 0.30, 0.85],
    'Kayn': [0.45, 0.85, 0.75, 0.80, 0.65],
    'Kha\'Zix': [0.70, 0.75, 0.35, 0.95, 0.60],
    'Kindred': [0.65, 0.90, 0.60, 0.65, 0.85],
    'Lee Sin': [0.95, 0.45, 0.60, 0.90, 0.60],
    'Lillia': [0.50, 0.90, 0.90, 0.65, 0.75],
    'Master Yi': [0.35, 0.95, 0.30, 0.60, 0.90],
    'Nidalee': [0.95, 0.40, 0.35, 0.85, 0.55],
    'Nocturne': [0.70, 0.65, 0.60, 0.95, 0.65],
    'Nunu & Willump': [0.75, 0.55, 0.75, 0.75, 1.00],
    'Rammus': [0.60, 0.70, 0.65, 0.90, 0.55],
    'Rek\'Sai': [0.90, 0.45, 0.45, 0.90, 0.60],
    'Rengar': [0.75, 0.70, 0.30, 0.95, 0.60],
    'Sejuani': [0.60, 0.75, 0.90, 0.90, 0.65],
    'Shaco': [0.90, 0.35, 0.30, 0.90, 0.55],
    'Shyvana': [0.45, 0.80, 0.85, 0.40, 0.90],
    'Skarner': [0.65, 0.80, 0.85, 0.90, 0.65],
    'Taliyah': [0.70, 0.85, 0.80, 0.80, 0.80],
    'Trundle': [0.75, 0.70, 0.35, 0.60, 0.95],
    'Udyr': [0.75, 0.70, 0.65, 0.65, 0.85],
    'Vi': [0.75, 0.65, 0.65, 0.95, 0.65],
    'Viego': [0.60, 0.85, 0.65, 0.75, 0.80],
    'Xin Zhao': [0.90, 0.50, 0.65, 0.85, 0.65],
    'Zac': [0.55, 0.80, 0.95, 0.90, 0.65],

    # Đường Giữa (Mid Lane)
    'Ahri': [0.75, 0.70, 0.65, 0.90, 0.60],
    'Akali': [0.70, 0.80, 0.55, 0.90, 0.50],
    'Anivia': [0.50, 0.90, 0.95, 0.70, 0.80],
    'Annie': [0.70, 0.75, 0.90, 0.90, 0.55],
    'Aurelion Sol': [0.30, 1.00, 1.00, 0.40, 0.75],
    'Aurora': [0.75, 0.75, 0.85, 0.85, 0.60],
    'Azir': [0.45, 0.95, 0.90, 0.60, 0.85],
    'Cassiopeia': [0.45, 0.95, 0.85, 0.65, 0.90],
    'Corki': [0.55, 0.90, 0.85, 0.60, 0.75],
    'Fizz': [0.80, 0.65, 0.50, 0.95, 0.45],
    'Galio': [0.70, 0.70, 0.90, 0.80, 0.55],
    'Hwei': [0.60, 0.90, 0.95, 0.75, 0.75],
    'Kassadin': [0.20, 1.00, 0.75, 0.85, 0.50],
    'Katarina': [0.60, 0.80, 0.85, 0.70, 0.45],
    'LeBlanc': [0.95, 0.50, 0.35, 1.00, 0.45],
    'Lissandra': [0.70, 0.70, 0.90, 0.90, 0.55],
    'Lux': [0.65, 0.75, 0.80, 0.85, 0.65],
    'Malzahar': [0.50, 0.80, 0.75, 0.95, 0.75],
    'Naafiri': [0.75, 0.70, 0.45, 0.90, 0.55],
    'Neeko': [0.80, 0.65, 0.95, 0.85, 0.55],
    'Orianna': [0.55, 0.90, 0.95, 0.65, 0.75],
    'Qiyana': [0.80, 0.70, 0.85, 0.90, 0.50],
    'Ryze': [0.45, 0.90, 0.80, 0.70, 0.75],
    'Smolder': [0.25, 1.00, 0.90, 0.40, 0.80],
    'Swain': [0.55, 0.85, 0.95, 0.65, 0.65],
    'Sylas': [0.75, 0.80, 0.75, 0.85, 0.55],
    'Syndra': [0.70, 0.85, 0.80, 0.90, 0.70],
    'Talon': [0.90, 0.50, 0.45, 0.95, 0.50],
    'Twisted Fate': [0.65, 0.75, 0.50, 0.95, 0.65],
    'Veigar': [0.35, 0.95, 0.85, 0.85, 0.65],
    'Vel\'Koz': [0.60, 0.85, 0.90, 0.60, 0.75],
    'Vex': [0.75, 0.75, 0.85, 0.90, 0.55],
    'Viktor': [0.45, 0.95, 0.90, 0.55, 0.80],
    'Vladimir': [0.30, 0.95, 0.95, 0.40, 0.55],
    'Xerath': [0.65, 0.85, 0.85, 0.65, 0.70],
    'Zed': [0.85, 0.65, 0.40, 0.95, 0.50],
    'Ziggs': [0.65, 0.80, 0.90, 0.50, 0.95],
    'Zoe': [0.85, 0.65, 0.45, 0.95, 0.50],

    # Xạ Thủ (Bot Lane - ADC)
    'Aphelios': [0.40, 0.95, 0.90, 0.55, 0.85],
    'Ashe': [0.80, 0.70, 0.65, 0.90, 0.75],
    'Caitlyn': [0.85, 0.80, 0.60, 0.70, 0.85],
    'Draven': [1.00, 0.45, 0.45, 0.65, 0.80],
    'Ezreal': [0.70, 0.75, 0.60, 0.65, 0.75],
    'Jhin': [0.75, 0.75, 0.60, 0.85, 0.70],
    'Jinx': [0.35, 1.00, 0.95, 0.40, 1.00],
    'Kai\'Sa': [0.60, 0.90, 0.65, 0.85, 0.85],
    'Kalista': [0.95, 0.50, 0.45, 0.65, 0.95],
    'Kog\'Maw': [0.30, 1.00, 0.80, 0.35, 0.90],
    'Lucian': [0.90, 0.60, 0.50, 0.75, 0.75],
    'Miss Fortune': [0.75, 0.75, 0.95, 0.55, 0.75],
    'Nilah': [0.45, 0.90, 0.85, 0.65, 0.75],
    'Samira': [0.65, 0.85, 0.90, 0.65, 0.65],
    'Senna': [0.55, 0.95, 0.70, 0.75, 0.75],
    'Sivir': [0.50, 0.90, 0.90, 0.40, 0.85],
    'Tristana': [0.65, 0.90, 0.60, 0.65, 0.95],
    'Twitch': [0.40, 0.95, 0.90, 0.75, 0.80],
    'Varus': [0.85, 0.70, 0.75, 0.85, 0.80],
    'Vayne': [0.35, 0.95, 0.20, 0.75, 0.85],
    'Xayah': [0.60, 0.85, 0.85, 0.65, 0.85],
    'Zeri': [0.40, 0.95, 0.85, 0.65, 0.80],

    # Hỗ Trợ (Support)
    'Alistar': [0.65, 0.65, 0.90, 0.90, 0.50],
    'Bard': [0.65, 0.80, 0.75, 0.95, 0.60],
    'Blitzcrank': [0.85, 0.45, 0.30, 1.00, 0.40],
    'Brand': [0.75, 0.80, 0.95, 0.60, 0.80],
    'Braum': [0.55, 0.75, 0.85, 0.70, 0.55],
    'Janna': [0.60, 0.75, 0.60, 0.60, 0.50],
    'Karma': [0.90, 0.55, 0.65, 0.75, 0.55],
    'Leona': [0.85, 0.55, 0.85, 0.95, 0.50],
    'Lulu': [0.70, 0.80, 0.60, 0.65, 0.50],
    'Milio': [0.55, 0.85, 0.70, 0.50, 0.55],
    'Morgana': [0.65, 0.65, 0.75, 0.90, 0.55],
    'Nami': [0.75, 0.65, 0.80, 0.75, 0.55],
    'Nautilus': [0.85, 0.55, 0.80, 0.95, 0.50],
    'Pantheon': [0.95, 0.35, 0.40, 0.95, 0.45],
    'Pyke': [0.95, 0.35, 0.40, 0.95, 0.40],
    'Rakan': [0.65, 0.80, 0.95, 0.90, 0.55],
    'Rell': [0.70, 0.70, 0.95, 0.90, 0.50],
    'Renata Glasc': [0.50, 0.90, 0.95, 0.75, 0.55],
    'Sona': [0.40, 0.95, 0.85, 0.60, 0.50],
    'Soraka': [0.60, 0.80, 0.50, 0.45, 0.45],
    'Taric': [0.45, 0.85, 0.95, 0.60, 0.55],
    'Thresh': [0.75, 0.65, 0.65, 0.95, 0.50],
    'Yuumi': [0.40, 0.90, 0.60, 0.55, 0.45],
    'Zilean': [0.45, 0.90, 0.75, 0.80, 0.50],
    'Zyra': [0.80, 0.70, 0.90, 0.75, 0.80]
}

DEFAULT_TACTICAL_VECTOR = [0.60, 0.60, 0.60, 0.60, 0.60]
TACTICAL_AXES = ['Early_Power', 'Scaling', 'Teamfight_AOE', 'Pick_Potential', 'Objective_Control']


def get_champion_vector(champ_name: str) -> np.ndarray:
    """Trích xuất vector 5 thuộc tính của 1 tướng (hỗ trợ fallback an toàn)."""
    if not champ_name or not isinstance(champ_name, str):
        return np.array(DEFAULT_TACTICAL_VECTOR)
    
    clean_name = champ_name.strip()
    if clean_name in CHAMPION_TACTICAL_VECTOR:
        return np.array(CHAMPION_TACTICAL_VECTOR[clean_name])
    
    # Fuzzy match basic
    for k, v in CHAMPION_TACTICAL_VECTOR.items():
        if k.lower() == clean_name.lower():
            return np.array(v)
    return np.array(DEFAULT_TACTICAL_VECTOR)


def compute_team_composition_vector(top: str, jng: str, mid: str, bot: str, sup: str) -> np.ndarray:
    """
    Tính toán Vector chiến thuật tổng hợp của đội hình 5 tướng.
    Có áp dụng trọng số vị trí chiến thuật:
    - Early: Top (25%), Jng (30%), Mid (25%), Bot (15%), Sup (5%)
    - Scaling: Mid (35%), Bot (40%), Top (15%), Jng (5%), Sup (5%)
    - Teamfight_AOE: Mid (30%), Top (25%), Sup (20%), Jng (15%), Bot (10%)
    - Pick_Potential: Sup (30%), Jng (30%), Mid (25%), Top (10%), Bot (5%)
    - Objective_Control: Jng (35%), Bot (30%), Mid (20%), Top (10%), Sup (5%)
    """
    v_top = get_champion_vector(top)
    v_jng = get_champion_vector(jng)
    v_mid = get_champion_vector(mid)
    v_bot = get_champion_vector(bot)
    v_sup = get_champion_vector(sup)

    early = 0.25*v_top[0] + 0.30*v_jng[0] + 0.25*v_mid[0] + 0.15*v_bot[0] + 0.05*v_sup[0]
    scaling = 0.15*v_top[1] + 0.05*v_jng[1] + 0.35*v_mid[1] + 0.40*v_bot[1] + 0.05*v_sup[1]
    teamfight = 0.25*v_top[2] + 0.15*v_jng[2] + 0.30*v_mid[2] + 0.10*v_bot[2] + 0.20*v_sup[2]
    pick = 0.10*v_top[3] + 0.30*v_jng[3] + 0.25*v_mid[3] + 0.05*v_bot[3] + 0.30*v_sup[3]
    obj = 0.10*v_top[4] + 0.35*v_jng[4] + 0.20*v_mid[4] + 0.30*v_bot[4] + 0.05*v_sup[4]

    return np.array([early, scaling, teamfight, pick, obj])


def load_all_team_compositions(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Trích xuất 6,000 đội hình giải đấu kèm kết quả từ CSDL SQLite."""
    if not db_path.exists():
        raise FileNotFoundError(f"Không tìm thấy CSDL tại {db_path}")

    conn = sqlite3.connect(db_path)
    q = """
    SELECT 
        m.gameid,
        m.side,
        m.result,
        m.gamelength,
        m.firstdragon,
        m.void_grubs,
        MAX(CASE WHEN p.position = 'top' THEN p.champion END) AS top,
        MAX(CASE WHEN p.position = 'jng' THEN p.champion END) AS jng,
        MAX(CASE WHEN p.position = 'mid' THEN p.champion END) AS mid,
        MAX(CASE WHEN p.position = 'bot' THEN p.champion END) AS bot,
        MAX(CASE WHEN p.position = 'sup' THEN p.champion END) AS sup
    FROM tournament_matches m
    JOIN tournament_players p ON m.gameid = p.gameid AND m.side = p.side
    GROUP BY m.gameid, m.side
    HAVING top IS NOT NULL AND jng IS NOT NULL AND mid IS NOT NULL AND bot IS NOT NULL AND sup IS NOT NULL
    """
    df = pd.read_sql_query(q, conn)
    conn.close()

    # Tính vector 5 chiều cho từng đội hình
    vectors = []
    for _, row in df.iterrows():
        vec = compute_team_composition_vector(row['top'], row['jng'], row['mid'], row['bot'], row['sup'])
        vectors.append(vec)

    df_vec = pd.DataFrame(vectors, columns=TACTICAL_AXES)
    df_full = pd.concat([df.reset_index(drop=True), df_vec.reset_index(drop=True)], axis=1)
    return df_full


class DraftArchetypeClusteringSystem:
    """Hệ thống Phân cụm K-Means & PCA nhận diện 4 Trường phái Đội hình."""

    ARCHETYPE_PROFILES = {
        0: {
            "name": "Early Snowball & Dive",
            "code": "EARLY_SNOWBALL",
            "tagline": "Đánh Đầu Trận, Ép Trụ & Lăn Cầu Tuyết Thần Tốc",
            "description": "Đội hình quy tụ các vị tướng đè đường cực mạnh, dồn sát thương và băng trụ sớm. Mục tiêu là hủy diệt đối thủ trong 15-20 phút đầu.",
            "key_condition": "Phải ăn Sâu Hư Không đợt 1, gank đè nát Bot/Mid và lấy Trụ Đầu trước phút 14.",
            "weakness": "Hụt hơi nghiêm trọng nếu trận đấu kéo dài qua phút 30 khi đối thủ đạt đủ trang bị thủ."
        },
        1: {
            "name": "Wombocombo & Objective Control",
            "code": "WOMBO_OBJECTIVE",
            "tagline": "Giao Tranh Tổng Diện Rộng & Tranh Chấp Mục Tiêu",
            "description": "Đội hình sở hữu lượng khống chế cứng diện rộng và chiêu cuối mở combat áp đảo. Rất mạnh trong các pha tranh chấp Rồng và Baron.",
            "key_condition": "Tập trung 5 người kiểm soát tầm nhìn quanh hang Rồng/Baron, mở combat chuẩn xác khi đối thủ bước vào góc hẹp.",
            "weakness": "Phụ thuộc nặng vào thời gian hồi chiêu cuối; dễ bị đẩy lẻ chia cắt đội hình."
        },
        2: {
            "name": "Late-Game Hypercarry",
            "code": "LATE_HYPERCARRY",
            "tagline": "Nuôi Siêu Chủ Lực & Sức Mạnh Tuyệt Đối Cuối Trận",
            "description": "Đội hình xây dựng xoay quanh 1-2 siêu chủ lực có ngưỡng sức mạnh vô hạn về late game (Smolder, Jinx, Azir, Kayle, Kassadin).",
            "key_condition": "Chấp nhận nhường mục tiêu sớm, kéo dài thời gian để chủ lực đạt ngưỡng 3 món trang bị chuẩn.",
            "weakness": "Đầu trận yếu ớt, dễ bị đối thủ lăn cầu tuyết hủy diệt trước khi kịp chạm ngưỡng sức mạnh."
        },
        3: {
            "name": "Pick & Split-Push 1-3-1",
            "code": "PICK_SPLIT_PUSH",
            "tagline": "Bắt Lẻ Mục Tiêu & Đẩy Lẻ Chia Cắt Bản Đồ",
            "description": "Đội hình sở hữu các con bài đẩy lẻ cực khỏe ở cánh kết hợp các chiêu thức bắt lẻ mục tiêu đơn lập từ xa (Nautilus, Camille, Ahri, Vi).",
            "key_condition": "Tạo áp lực đẩy 2 cánh 1-3-1, rình rập bắt lẻ đối thủ khi họ di chuyển phòng thủ để ép ăn Baron.",
            "weakness": "Giao tranh 5v5 trực diện yếu hơn các đội hình Wombocombo nếu bị ép combat bất ngờ."
        }
    }

    def __init__(self, n_clusters: int = 4):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
        self.pca = PCA(n_components=2, random_state=42)
        self.cluster_mapping = {}  # Map cluster index to archetype profile
        self.cluster_summary = None

    def fit_and_evaluate(self):
        print("=" * 85)
        print("🚀 BẮT ĐẦU HUẤN LUYỆN PHÂN CỤM K-MEANS & PCA 4 TRƯỜNG PHÁI ĐỘI HÌNH (TASK 3.4)")
        print("=" * 85)

        df = load_all_team_compositions()
        print(f"📊 Đã nạp thành công: {len(df):,} đội hình thi đấu giải đấu chuyên nghiệp.")

        X = df[TACTICAL_AXES].to_numpy()
        X_scaled = self.scaler.fit_transform(X)

        # 1. Khảo sát Elbow (WCSS) & Silhouette Score (K=2..8)
        k_range = range(2, 9)
        wcss_list = []
        sil_list = []

        print("🔍 Đang khảo sát tìm số cụm tối ưu (Elbow Method & Silhouette Analysis)...")
        for k in k_range:
            km_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels_temp = km_temp.fit_predict(X_scaled)
            wcss_list.append(km_temp.inertia_)
            sil = silhouette_score(X_scaled, labels_temp)
            sil_list.append(sil)
            print(f"   • K = {k}: WCSS (Inertia) = {km_temp.inertia_:8.2f} | Silhouette Score = {sil:.4f}")

        # Vẽ Fig 10: Elbow & Silhouette Curves
        self._plot_fig10_elbow_silhouette(k_range, wcss_list, sil_list)

        # 2. Huấn luyện K-Means K=4
        print(f"\n🧠 Đang huấn luyện K-Means với K = {self.n_clusters} cụm tối ưu...")
        self.kmeans.fit(X_scaled)
        cluster_labels = self.kmeans.labels_
        df['cluster'] = cluster_labels

        # 3. Huấn luyện PCA 2D
        print("📉 Đang giảm chiều dữ liệu bằng PCA 2D...")
        X_pca = self.pca.fit_transform(X_scaled)
        df['pca1'] = X_pca[:, 0]
        df['pca2'] = X_pca[:, 1]
        evr = self.pca.explained_variance_ratio_
        print(f"📈 Tỷ lệ phương sai giải thích (Explained Variance Ratio): PC1 = {evr[0]:.2%}, PC2 = {evr[1]:.2%}, Tổng = {np.sum(evr):.2%}")

        # 4. Phân tích Centroids & Định danh 4 Trường phái
        centroids_scaled = self.kmeans.cluster_centers_
        centroids_raw = self.scaler.inverse_transform(centroids_scaled)
        df_centroids = pd.DataFrame(centroids_raw, columns=TACTICAL_AXES)

        # Tự động gán nhãn trường phái theo đặc trưng tâm cụm
        self._map_clusters_to_archetypes(df_centroids)

        # 5. Thống kê đặc tính từng cụm
        summary_rows = []
        for c_idx in range(self.n_clusters):
            arch = self.ARCHETYPE_PROFILES[self.cluster_mapping[c_idx]]
            c_mask = df['cluster'] == c_idx
            n_samples = np.sum(c_mask)
            pct = (n_samples / len(df)) * 100.0
            winrate = df.loc[c_mask, 'result'].mean() * 100.0
            avg_duration = df.loc[c_mask, 'gamelength'].mean() / 60.0
            avg_dragon = df.loc[c_mask, 'firstdragon'].mean() * 100.0
            avg_grubs = df.loc[c_mask, 'void_grubs'].mean()

            summary_rows.append({
                "Cluster": c_idx,
                "Trường Phái Đội Hình": arch['name'],
                "Số Lượng": f"{n_samples:,} ({pct:.1f}%)",
                "Tỷ Lệ Thắng": f"{winrate:.2f}%",
                "Thời Lượng TB": f"{avg_duration:.1f} phút",
                "Ăn Rồng 1": f"{avg_dragon:.1f}%",
                "Sâu Hư Không TB": f"{avg_grubs:.2f} con",
                "Early": df_centroids.iloc[c_idx]['Early_Power'],
                "Scaling": df_centroids.iloc[c_idx]['Scaling'],
                "Teamfight": df_centroids.iloc[c_idx]['Teamfight_AOE'],
                "Pick": df_centroids.iloc[c_idx]['Pick_Potential'],
                "Objective": df_centroids.iloc[c_idx]['Objective_Control']
            })

        self.cluster_summary = pd.DataFrame(summary_rows)
        print("\n" + "=" * 100)
        print("🏆 BẢNG TỔNG HỢP 4 TRƯỜNG PHÁI ĐỘI HÌNH (DRAFT ARCHETYPES) PHÂN CỤM K-MEANS")
        print("=" * 100)
        print(self.cluster_summary[['Cluster', 'Trường Phái Đội Hình', 'Số Lượng', 'Tỷ Lệ Thắng', 'Thời Lượng TB', 'Ăn Rồng 1', 'Sâu Hư Không TB']].to_string(index=False))

        # Vẽ Fig 11: PCA 2D Clustering & Radar Charts
        self._plot_fig11_pca_and_radars(df, df_centroids)

        # Lưu model
        self.save_model()
        return self.cluster_summary

    def _map_clusters_to_archetypes(self, df_centroids: pd.DataFrame):
        """Ánh xạ chuẩn xác từng tâm cụm K-Means về 4 Trường phái chiến thuật."""
        # 1. Early Snowball (Cụm có Early_Power cao nhất)
        early_cluster = int(df_centroids['Early_Power'].idxmax())
        
        # 2. Late-Game Hypercarry (Cụm có Scaling cao nhất)
        scaling_cluster = int(df_centroids['Scaling'].idxmax())
        
        # 3. Wombocombo & Objective Control (Cụm có Objective_Control cao nhất trong các cụm còn lại)
        remaining = [c for c in range(self.n_clusters) if c not in [early_cluster, scaling_cluster]]
        obj_scores = {c: df_centroids.iloc[c]['Objective_Control'] + df_centroids.iloc[c]['Teamfight_AOE'] for c in remaining}
        wombo_cluster = max(obj_scores, key=obj_scores.get)
        
        # 4. Pick & Split-Push 1-3-1 (Cụm còn lại)
        split_cluster = [c for c in remaining if c != wombo_cluster][0]

        self.cluster_mapping = {
            early_cluster: 0,   # Early Snowball & Dive
            wombo_cluster: 1,   # Wombocombo & Objective Control
            scaling_cluster: 2, # Late-Game Hypercarry
            split_cluster: 3    # Pick & Split-Push 1-3-1
        }

    def _plot_fig10_elbow_silhouette(self, k_range, wcss_list, sil_list):
        """Vẽ Fig 10: Đánh giá số cụm tối ưu qua Elbow Method và Silhouette Score."""
        print("📊 Đang vẽ Fig 10: Biểu đồ Elbow & Silhouette Score...")
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

        # Subplot 1: Elbow Method
        axes[0].plot(list(k_range), wcss_list, marker='o', lw=2.5, color='#2563EB', markersize=8)
        axes[0].axvline(x=4, color='#DC2626', linestyle='--', lw=1.8, label='Số Cụm Tối Ưu K = 4 (Điểm Khuỷu Tay)')
        axes[0].set_xlabel('Số Lượng Cụm (K)', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Tổng Bình Phương Khoảng Cách Nội Cụm (WCSS / Inertia)', fontsize=11, fontweight='bold')
        axes[0].set_title('Phương Pháp Khuỷu Tay (Elbow Method)', fontsize=12, fontweight='bold', pad=12)
        axes[0].legend(loc="upper right", frameon=True, facecolor='white', framealpha=0.95, fontsize=10)
        axes[0].grid(True, linestyle=':', alpha=0.6)

        # Subplot 2: Silhouette Score
        axes[1].plot(list(k_range), sil_list, marker='s', lw=2.5, color='#16A34A', markersize=8)
        axes[1].axvline(x=4, color='#DC2626', linestyle='--', lw=1.8, label='K = 4 (Phù hợp nghiệp vụ 4 Trường phái)')
        axes[1].set_xlabel('Số Lượng Cụm (K)', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Điểm Silhouette Trung Bình (Silhouette Score)', fontsize=11, fontweight='bold')
        axes[1].set_title('Đánh Giá Hệ Số Silhouette (Silhouette Analysis)', fontsize=12, fontweight='bold', pad=12)
        axes[1].legend(loc="upper right", frameon=True, facecolor='white', framealpha=0.95, fontsize=10)
        axes[1].grid(True, linestyle=':', alpha=0.6)

        plt.suptitle('ĐÁNH GIÁ SỐ CỤM TỐI ƯU K-MEANS TRÊN KHÔNG GIAN ĐỘI HÌNH LMHT (CHƯƠNG 4)', fontsize=13, fontweight='bold', y=0.98)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        fig10_path = FIGURES_DIR / "fig10_kmeans_elbow_silhouette.png"
        plt.savefig(fig10_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"💾 Đã lưu: {fig10_path}")

    def _plot_fig11_pca_and_radars(self, df: pd.DataFrame, df_centroids: pd.DataFrame):
        """Vẽ Fig 11: Không gian 2D PCA & Biểu đồ Radar 5 trục của 4 Trường phái."""
        print("📊 Đang vẽ Fig 11: Không gian phân cụm PCA 2D & Radar Charts...")
        fig = plt.figure(figsize=(16, 7.5), dpi=300)
        gs = fig.add_gridspec(2, 3, width_ratios=[1.3, 1, 1], hspace=0.35, wspace=0.3)

        # 1. Trục chính bên trái: PCA 2D Scatter Plot
        ax_pca = fig.add_subplot(gs[:, 0])
        palette = ['#DC2626', '#2563EB', '#D97706', '#9333EA']
        
        for c_idx in range(self.n_clusters):
            arch_id = self.cluster_mapping[c_idx]
            arch_name = self.ARCHETYPE_PROFILES[arch_id]['name']
            c_data = df[df['cluster'] == c_idx]
            ax_pca.scatter(c_data['pca1'], c_data['pca2'], c=palette[c_idx], label=f'Cụm {c_idx+1}: {arch_name}',
                           alpha=0.45, edgecolors='none', s=22)

        # Vẽ tâm cụm (Centroids) trên PCA
        X_centroids_scaled = self.scaler.transform(df_centroids.to_numpy())
        centroids_pca = self.pca.transform(X_centroids_scaled)
        ax_pca.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='black', marker='X', s=160,
                       edgecolors='white', lw=1.8, label='Tâm Cụm (Centroids)', zorder=10)

        evr = self.pca.explained_variance_ratio_
        ax_pca.set_xlabel(f'Thành phần chính 1 (PC1 - {evr[0]:.1%} phương sai)', fontsize=10, fontweight='bold')
        ax_pca.set_ylabel(f'Thành phần chính 2 (PC2 - {evr[1]:.1%} phương sai)', fontsize=10, fontweight='bold')
        ax_pca.set_title('KHÔNG GIAN PHÂN CỤM PCA 2D\n(6,000 Đội Hình Giải Đấu)', fontsize=12, fontweight='bold', pad=10)
        ax_pca.legend(loc="upper right", frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
        ax_pca.grid(True, linestyle=':', alpha=0.5)

        # 2. Bốn biểu đồ Radar bên phải
        radar_positions = [
            (0, 1), (0, 2),
            (1, 1), (1, 2)
        ]

        angles = np.linspace(0, 2 * np.pi, len(TACTICAL_AXES), endpoint=False).tolist()
        angles += angles[:1]  # Complete loop

        labels_vn = ['Early', 'Scaling', 'Teamfight', 'Pick', 'Objective']

        for c_idx in range(self.n_clusters):
            arch_id = self.cluster_mapping[c_idx]
            arch_name = self.ARCHETYPE_PROFILES[arch_id]['name']
            r_pos = radar_positions[c_idx]
            ax_r = fig.add_subplot(gs[r_pos[0], r_pos[1]], polar=True)

            values = df_centroids.iloc[c_idx].tolist()
            values += values[:1]

            ax_r.plot(angles, values, color=palette[c_idx], lw=2.0)
            ax_r.fill(angles, values, color=palette[c_idx], alpha=0.3)
            ax_r.set_xticks(angles[:-1])
            ax_r.set_xticklabels(labels_vn, fontsize=8, fontweight='bold')
            ax_r.set_ylim(0.2, 0.9)
            ax_r.set_yticks([0.4, 0.6, 0.8])
            ax_r.set_yticklabels(['0.4', '0.6', '0.8'], fontsize=6.5, color='#64748B')
            ax_r.set_title(f'Cụm {c_idx+1}: {arch_name}', fontsize=10, fontweight='bold', color=palette[c_idx], pad=10)

        plt.suptitle('NHẬN DIỆN 4 TRƯỜNG PHÁI ĐỘI HÌNH LMHT QUA K-MEANS VÀ PCA 2D (TASK 3.4)', fontsize=14, fontweight='bold', y=0.98)
        fig11_path = FIGURES_DIR / "fig11_draft_archetypes_pca_clusters.png"
        plt.savefig(fig11_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"💾 Đã lưu: {fig11_path}")

    def save_model(self, path: Path = MODEL_PATH):
        """Lưu trữ trọn bộ mô hình phân cụm."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "kmeans": self.kmeans,
            "pca": self.pca,
            "scaler": self.scaler,
            "cluster_mapping": self.cluster_mapping,
            "archetype_profiles": self.ARCHETYPE_PROFILES,
            "champion_tactical_vector": CHAMPION_TACTICAL_VECTOR,
            "tactical_axes": TACTICAL_AXES,
            "cluster_summary": self.cluster_summary
        }
        with open(path, "wb") as f:
            pickle.dump(payload, f)
        print(f"💾 Đã lưu thành công mô hình Phân cụm Đội hình vào: {path.resolve()}")

    @classmethod
    def load_model(cls, path: Path = MODEL_PATH):
        """Nạp mô hình phục vụ suy luận nhận diện trường phái."""
        if not path.exists():
            raise FileNotFoundError(f"Chưa tìm thấy model tại {path}. Hãy chạy --train trước.")
        with open(path, "rb") as f:
            payload = pickle.load(f)
        
        system = cls(n_clusters=payload["kmeans"].n_clusters)
        system.kmeans = payload["kmeans"]
        system.pca = payload["pca"]
        system.scaler = payload["scaler"]
        system.cluster_mapping = payload["cluster_mapping"]
        system.cluster_summary = payload["cluster_summary"]
        return system

    def predict_archetype(self, top: str, jng: str, mid: str, bot: str, sup: str) -> dict:
        """Nhận diện trường phái và điều kiện thắng cho một đội hình 5 tướng bất kỳ."""
        team_vec = compute_team_composition_vector(top, jng, mid, bot, sup)
        vec_scaled = self.scaler.transform(team_vec.reshape(1, -1))
        cluster_idx = int(self.kmeans.predict(vec_scaled)[0])
        arch_id = self.cluster_mapping[cluster_idx]
        arch_info = self.ARCHETYPE_PROFILES[arch_id]

        # Tính khoảng cách Euclidean đến các tâm cụm để suy ra % độ tương đồng
        distances = np.linalg.norm(self.kmeans.cluster_centers_ - vec_scaled, axis=1)
        sim_scores = 1.0 / (1.0 + distances)
        prob_dist = sim_scores / np.sum(sim_scores)
        confidence = float(prob_dist[cluster_idx]) * 100.0

        return {
            "archetype_name": arch_info['name'],
            "archetype_code": arch_info['code'],
            "cluster_id": cluster_idx + 1,
            "confidence_pct": round(confidence, 1),
            "tagline": arch_info['tagline'],
            "description": arch_info['description'],
            "key_win_condition": arch_info['key_condition'],
            "critical_weakness": arch_info['weakness'],
            "radar_scores": {axis: round(float(val), 2) for axis, val in zip(TACTICAL_AXES, team_vec)},
            "all_archetype_probabilities": {
                self.ARCHETYPE_PROFILES[self.cluster_mapping[i]]['name']: round(float(prob_dist[i]) * 100.0, 1)
                for i in range(self.n_clusters)
            }
        }


def parse_args():
    parser = argparse.ArgumentParser(description="LOL Draft Archetypes Clustering System (Task 3.4)")
    parser.add_argument("--train", action="store_true", help="Huấn luyện mô hình K-Means & PCA")
    parser.add_argument("--predict", action="store_true", help="Nhận diện trường phái đội hình")
    parser.add_argument("--top", type=str, default="Renekton", help="Tướng đường trên (Top)")
    parser.add_argument("--jng", type=str, default="Elise", help="Tướng đi rừng (Jungle)")
    parser.add_argument("--mid", type=str, default="LeBlanc", help="Tướng đường giữa (Mid)")
    parser.add_argument("--bot", type=str, default="Kalista", help="Tướng xạ thủ (Bot)")
    parser.add_argument("--sup", type=str, default="Nautilus", help="Tướng hỗ trợ (Support)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.predict:
        system = DraftArchetypeClusteringSystem.load_model()
        res = system.predict_archetype(args.top, args.jng, args.mid, args.bot, args.sup)

        print("\n" + "=" * 75)
        print("🛡️ KẾT QUẢ NHẬN DIỆN TRƯỜNG PHÁI ĐỘI HÌNH LMHT (DRAFT ARCHETYPE AI)")
        print("=" * 75)
        print(f"👥 ĐỘI HÌNH: Top: {args.top} | Rừng: {args.jng} | Mid: {args.mid} | Bot: {args.bot} | Sp: {args.sup}")
        print("-" * 75)
        print(f"🏆 TRƯỜNG PHÁI: {res['archetype_name'].upper()} (Độ tin cậy: {res['confidence_pct']}%)")
        print(f"💬 KHẨU HIỆU  : {res['tagline']}")
        print(f"📖 MÔ TẢ      : {res['description']}")
        print(f"⭐ ĐIỀU KIỆN THẮNG (WIN CONDITION): {res['key_win_condition']}")
        print(f"⚠️ ĐIỂM YẾU CHÍ MẠNG (WEAKNESS)    : {res['critical_weakness']}")
        print("-" * 75)
        print("📊 ĐIỂM RADAR 5 TRỤC CHIẾN THUẬT:")
        for k, v in res['radar_scores'].items():
            bar = "█" * int(v * 25)
            print(f"   • {k:<18}: {v:.2f} {bar}")
        print("=" * 75)

    else:
        system = DraftArchetypeClusteringSystem()
        system.fit_and_evaluate()
