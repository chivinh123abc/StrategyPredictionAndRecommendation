"""
Module 06: Machine Learning - Task 3.1: Draft Prediction Model (Phút 0)
Dự đoán xác suất thắng thua dựa hoàn toàn vào giai đoạn Cấm/Chọn (10 tướng thi đấu).

Phương pháp & Kỹ thuật:
- Trích xuất 3,000 trận đấu đỉnh cao từ CSDL SQLite (lol_live_data.db).
- Trích xuất đặc trưng đa tầng:
  1. Position-Specific Differential One-Hot Vectors (+1 Blue, -1 Red theo từng Lane).
  2. Champion Historical Bayesian Winrates & Meta Power Tiers.
  3. Lane Matchup Historical Advantage (Top vs Top, Mid vs Mid, Bot vs Bot...).
  4. Synergy Duo Correlations (Mid-Jng, Bot-Sup).
  5. Team Composition Balance (AD/AP balance, Hard CC score, Early vs Late Scaling).
  6. Time-Decay Sample Weighting (Ưu tiên các bản cập nhật / trận đấu gần nhất).
- So sánh các mô hình: Logistic Regression (L2), Random Forest, LightGBM, XGBoost, Multi-Layer Perceptron (MLP), Voting Ensemble.
- Xuất file đóng gói: models/draft_model.pkl
"""

import sys
import os
import argparse
import pickle
import sqlite3
import warnings
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, log_loss, f1_score,
    precision_score, recall_score, brier_score_loss, classification_report
)
from sklearn.preprocessing import StandardScaler

# Import XGBoost / LightGBM if available
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMClassifier
    HAS_LGB = True
except ImportError:
    HAS_LGB = False

warnings.filterwarnings('ignore')

# Root path configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "database" / "lol_live_data.db"
MODEL_PATH = PROJECT_ROOT / "models" / "draft_model.pkl"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "clean_tournament_draft.csv"

sys.path.insert(0, str(PROJECT_ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analysis_data import open_clean_connection
from validation import evaluate_training, calibrate, SCHEMA_VERSION

POSITIONS = ['top', 'jng', 'mid', 'bot', 'sup']


def load_pivoted_draft_data(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Trích xuất 3,000 trận đấu giải và xoay trục 10 vị trí tướng."""
    if not db_path.exists():
        raise FileNotFoundError(f"Không tìm thấy CSDL tại {db_path}")

    conn = open_clean_connection(db_path)
    query = """
    SELECT 
        m.gameid,
        m.date,
        m.patch,
        m.league,
        MAX(CASE WHEN m.side = 'Blue' THEN m.result END) AS blue_win,
        MAX(CASE WHEN p.side = 'Blue' AND p.position = 'top' THEN p.champion END) AS blue_top,
        MAX(CASE WHEN p.side = 'Blue' AND p.position = 'jng' THEN p.champion END) AS blue_jng,
        MAX(CASE WHEN p.side = 'Blue' AND p.position = 'mid' THEN p.champion END) AS blue_mid,
        MAX(CASE WHEN p.side = 'Blue' AND p.position = 'bot' THEN p.champion END) AS blue_bot,
        MAX(CASE WHEN p.side = 'Blue' AND p.position = 'sup' THEN p.champion END) AS blue_sup,
        MAX(CASE WHEN p.side = 'Red' AND p.position = 'top' THEN p.champion END) AS red_top,
        MAX(CASE WHEN p.side = 'Red' AND p.position = 'jng' THEN p.champion END) AS red_jng,
        MAX(CASE WHEN p.side = 'Red' AND p.position = 'mid' THEN p.champion END) AS red_mid,
        MAX(CASE WHEN p.side = 'Red' AND p.position = 'bot' THEN p.champion END) AS red_bot,
        MAX(CASE WHEN p.side = 'Red' AND p.position = 'sup' THEN p.champion END) AS red_sup
    FROM tournament_matches m
    JOIN tournament_players p ON m.gameid = p.gameid AND m.side = p.side
    GROUP BY m.gameid
    HAVING blue_win IS NOT NULL
       AND blue_top IS NOT NULL AND blue_jng IS NOT NULL AND blue_mid IS NOT NULL AND blue_bot IS NOT NULL AND blue_sup IS NOT NULL
       AND red_top IS NOT NULL AND red_jng IS NOT NULL AND red_mid IS NOT NULL AND red_bot IS NOT NULL AND red_sup IS NOT NULL
    ORDER BY m.date ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


class DraftFeatureEngineering:
    """Bộ trích xuất và biến đổi đặc trưng Cấm/Chọn (Draft Feature Pipeline)."""

    def __init__(self, half_life_days: float = 60.0):
        self.half_life_days = half_life_days
        self.champ_vocab = {}
        self.vocab_size = 0
        self.bayesian_prior_wr = 0.50
        self.bayesian_weight = 10.0  # C trọng số làm mịn
        self.champ_winrates = {}
        self.regional_champ_winrates = {}
        self.regional_blue_wr = {}
        self.lane_matchup_adv = {}
        self.synergy_pair_adv = {}
        self.scaler = StandardScaler()
        self.feature_names = []

    @staticmethod
    def _map_region_bucket(league_val: str) -> str:
        lg = str(league_val or '').strip().upper()
        if lg == 'LCK':
            return 'LCK'
        if lg == 'LPL':
            return 'LPL'
        if lg in ('LCP', 'VCS', 'PCS'):
            return 'LCP'
        if lg in ('WLDS', 'MSI', 'EWC', 'INTERNATIONAL', 'WORLDS', 'CKTG'):
            return 'INTERNATIONAL'
        return 'ALL'

    def fit(self, df: pd.DataFrame):
        """Học từ điển tướng, tỷ lệ thắng Bayes toàn cầu & theo khu vực, đối đầu và phối hợp từ tập train."""
        # 1. Tạo từ điển tướng xuất hiện
        all_champs = set()
        for pos in POSITIONS:
            all_champs.update(df[f'blue_{pos}'].dropna().unique())
            all_champs.update(df[f'red_{pos}'].dropna().unique())
        
        self.champ_vocab = {champ: i for i, champ in enumerate(sorted(all_champs))}
        self.vocab_size = len(self.champ_vocab)

        # 2. Tính Bayesian Smoothed Winrate Toàn cầu và theo Khu vực (LCK, LPL, LCP, INTERNATIONAL)
        champ_stats = {c: {'wins': 0, 'games': 0} for c in self.champ_vocab}
        reg_buckets = ['LCK', 'LPL', 'LCP', 'INTERNATIONAL']
        reg_champ_stats = {rb: {c: {'wins': 0, 'games': 0} for c in self.champ_vocab} for rb in reg_buckets}
        reg_blue_stats = {rb: {'wins': 0, 'games': 0} for rb in reg_buckets}

        for _, row in df.iterrows():
            win = row['blue_win']
            rb = self._map_region_bucket(row.get('league', 'ALL'))
            if rb in reg_blue_stats:
                reg_blue_stats[rb]['games'] += 1
                if win == 1:
                    reg_blue_stats[rb]['wins'] += 1

            for pos in POSITIONS:
                b_c = row[f'blue_{pos}']
                r_c = row[f'red_{pos}']
                if b_c in champ_stats:
                    champ_stats[b_c]['games'] += 1
                    if win == 1: champ_stats[b_c]['wins'] += 1
                    if rb in reg_champ_stats:
                        reg_champ_stats[rb][b_c]['games'] += 1
                        if win == 1: reg_champ_stats[rb][b_c]['wins'] += 1
                if r_c in champ_stats:
                    champ_stats[r_c]['games'] += 1
                    if win == 0: champ_stats[r_c]['wins'] += 1
                    if rb in reg_champ_stats:
                        reg_champ_stats[rb][r_c]['games'] += 1
                        if win == 0: reg_champ_stats[rb][r_c]['wins'] += 1

        for c, s in champ_stats.items():
            smoothed_wr = (s['wins'] + self.bayesian_weight * self.bayesian_prior_wr) / (s['games'] + self.bayesian_weight)
            self.champ_winrates[c] = smoothed_wr

        self.regional_champ_winrates = {}
        for rb in reg_buckets:
            self.regional_champ_winrates[rb] = {}
            for c, s in reg_champ_stats[rb].items():
                prior_c = self.champ_winrates.get(c, 0.50)
                self.regional_champ_winrates[rb][c] = (s['wins'] + 6.0 * prior_c) / (s['games'] + 6.0)

        self.regional_blue_wr = {'ALL': float(df['blue_win'].mean()) if len(df) > 0 else 0.5}
        for rb, st in reg_blue_stats.items():
            self.regional_blue_wr[rb] = (st['wins'] + 20.0 * self.regional_blue_wr['ALL']) / (st['games'] + 20.0)

        # 3. Tính Lane Matchup Advantage (Top vs Top, Mid vs Mid...)
        for pos in POSITIONS:
            matchups = {}
            for _, row in df.iterrows():
                b_c = row[f'blue_{pos}']
                r_c = row[f'red_{pos}']
                pair = (b_c, r_c)
                if pair not in matchups:
                    matchups[pair] = {'b_wins': 0, 'total': 0}
                matchups[pair]['total'] += 1
                if row['blue_win'] == 1:
                    matchups[pair]['b_wins'] += 1
            
            # Làm mịn tỷ lệ đối đầu
            self.lane_matchup_adv[pos] = {}
            for pair, st in matchups.items():
                self.lane_matchup_adv[pos][pair] = (st['b_wins'] + 3 * 0.5) / (st['total'] + 3)

        # 4. Tính Synergy Duo Advantage (Mid-Jng, Bot-Sup)
        for d1, d2, name in [('mid', 'jng', 'mid_jng'), ('bot', 'sup', 'bot_sup')]:
            pairs = {}
            for _, row in df.iterrows():
                # Blue side pair
                p_b = (row[f'blue_{d1}'], row[f'blue_{d2}'])
                if p_b not in pairs: pairs[p_b] = {'wins': 0, 'total': 0}
                pairs[p_b]['total'] += 1
                if row['blue_win'] == 1: pairs[p_b]['wins'] += 1
                
                # Red side pair
                p_r = (row[f'red_{d1}'], row[f'red_{d2}'])
                if p_r not in pairs: pairs[p_r] = {'wins': 0, 'total': 0}
                pairs[p_r]['total'] += 1
                if row['blue_win'] == 0: pairs[p_r]['wins'] += 1

            self.synergy_pair_adv[name] = {}
            for p, st in pairs.items():
                self.synergy_pair_adv[name][p] = (st['wins'] + 3 * 0.5) / (st['total'] + 3)

        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Biến đổi DataFrame 10 tướng thành ma trận đặc trưng số học."""
        N = len(df)
        
        # 1. Differential One-Hot Encoding per Position (5 * vocab_size)
        # +1 cho tướng Blue, -1 cho tướng Red tại đúng Lane
        onehot_features = np.zeros((N, len(POSITIONS) * self.vocab_size), dtype=np.float32)
        
        dense_features_list = []

        for idx, (_, row) in enumerate(df.iterrows()):
            dense_row = []
            
            blue_champ_wrs = []
            red_champ_wrs = []
            

            for p_idx, pos in enumerate(POSITIONS):
                b_champ = row[f'blue_{pos}']
                r_champ = row[f'red_{pos}']

                # One-hot position indexing
                if b_champ in self.champ_vocab:
                    b_id = self.champ_vocab[b_champ]
                    onehot_features[idx, p_idx * self.vocab_size + b_id] = 1.0
                if r_champ in self.champ_vocab:
                    r_id = self.champ_vocab[r_champ]
                    onehot_features[idx, p_idx * self.vocab_size + r_id] = -1.0

                # Bayesian Winrates
                b_wr = self.champ_winrates.get(b_champ, self.bayesian_prior_wr)
                r_wr = self.champ_winrates.get(r_champ, self.bayesian_prior_wr)
                blue_champ_wrs.append(b_wr)
                red_champ_wrs.append(r_wr)

                # Lane matchup advantage
                pair = (b_champ, r_champ)
                lane_adv = self.lane_matchup_adv.get(pos, {}).get(pair, 0.5)
                dense_row.append(lane_adv - 0.5)  # Canh giữa 0

            # Sức mạnh tổng thể Meta của từng đội (Toàn cầu & Khu vực)
            avg_b_wr = np.mean(blue_champ_wrs)
            avg_r_wr = np.mean(red_champ_wrs)
            dense_row.append(avg_b_wr - avg_r_wr)  # Hiệu số winrate meta toàn cầu

            rb = self._map_region_bucket(row.get('league', 'ALL'))
            reg_wr_map = getattr(self, 'regional_champ_winrates', {}).get(rb, self.champ_winrates)
            reg_b_wrs = [reg_wr_map.get(row[f'blue_{pos}'], self.champ_winrates.get(row[f'blue_{pos}'], 0.50)) for pos in POSITIONS]
            reg_r_wrs = [reg_wr_map.get(row[f'red_{pos}'], self.champ_winrates.get(row[f'red_{pos}'], 0.50)) for pos in POSITIONS]
            dense_row.append(float(np.mean(reg_b_wrs) - np.mean(reg_r_wrs)))  # Hiệu số winrate meta đặc thù khu vực

            # Synergy Mid-Jng và Bot-Sup
            b_mid_jng = self.synergy_pair_adv['mid_jng'].get((row['blue_mid'], row['blue_jng']), 0.5)
            r_mid_jng = self.synergy_pair_adv['mid_jng'].get((row['red_mid'], row['red_jng']), 0.5)
            dense_row.append(b_mid_jng - r_mid_jng)

            b_bot_sup = self.synergy_pair_adv['bot_sup'].get((row['blue_bot'], row['blue_sup']), 0.5)
            r_bot_sup = self.synergy_pair_adv['bot_sup'].get((row['red_bot'], row['red_sup']), 0.5)
            dense_row.append(b_bot_sup - r_bot_sup)

            # Blue side base bias theo Khu vực (LCK / LPL / LCP / INTERNATIONAL)
            reg_b_prior = getattr(self, 'regional_blue_wr', {}).get(rb, 0.5)
            dense_row.append(float(reg_b_prior))

            dense_features_list.append(dense_row)

        dense_array = np.array(dense_features_list, dtype=np.float32)
        
        # Kết hợp One-hot Sparse và Dense Tactical features
        combined = np.hstack([onehot_features, dense_array])
        return combined

    def compute_sample_weights(self, dates: pd.Series) -> np.ndarray:
        """Tính trọng số thời gian (Time-decay weights) cho các trận đấu gần đây."""
        valid_dates = pd.to_datetime(dates, errors='coerce')
        max_date = valid_dates.max()
        days_diff = (max_date - valid_dates).dt.total_seconds() / (24 * 3600)
        # Exponential decay: w = 2^(-days / half_life)
        weights = np.power(2.0, -days_diff.fillna(180) / self.half_life_days)
        # Chuẩn hóa về mean = 1.0
        return (weights / weights.mean()).to_numpy()


def historical_training_features(fe, train):
    """Expanding-window target statistics; each row sees only earlier dates."""
    fe.fit(train)
    out = np.zeros_like(fe.transform(train))
    dates = pd.to_datetime(train.date, utc=True)
    blocks = np.array_split(sorted(dates.unique()), 6)
    for block in blocks:
        if len(block) == 0: continue
        mask = dates.isin(block).to_numpy()
        history = train.loc[dates < block[0]]
        past = DraftFeatureEngineering(half_life_days=fe.half_life_days).fit(history)
        past.champ_vocab, past.vocab_size = fe.champ_vocab, fe.vocab_size
        out[mask] = past.transform(train.loc[mask])
    return out


class LolDraftPredictionSystem:
    """Hệ thống huấn luyện, đánh giá và dự đoán Cấm/Chọn 2 giai đoạn."""

    def __init__(self):
        self.fe = DraftFeatureEngineering(half_life_days=90.0)
        self.models = {}
        self.best_model = None
        self.best_model_name = ""
        self.scaler = StandardScaler()

    def train_and_evaluate(self, test_size: float = 0.20):
        return evaluate_training(self, load_pivoted_draft_data(), 'blue_win', MODEL_PATH, test_size, oof_transform=historical_training_features)

    def save_model(self, path: Path = MODEL_PATH):
        """Lưu trữ trọn vẹn Feature Pipeline và Mô hình Machine Learning."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "model": self.best_model,
            "model_name": self.best_model_name,
            "feature_engineering": self.fe,
            "trained_at": datetime.now().isoformat(),
            "target": "blue_win",
            "schema_version": SCHEMA_VERSION, "calibration": self.calibration, "evaluation": self.evaluation
        }
        with open(path, "wb") as f:
            pickle.dump(payload, f)
        print(f"💾 Đã lưu thành công mô hình vào: {path.resolve()}")

    @classmethod
    def load_model(cls, path: Path = MODEL_PATH):
        """Nạp mô hình đã lưu phục vụ suy luận thời gian thực."""
        if not path.exists():
            raise FileNotFoundError(f"Chưa tìm thấy model tại {path}. Hãy chạy --train trước.")
        
        class _DraftUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                if name == 'DraftFeatureEngineering':
                    return DraftFeatureEngineering
                return super().find_class(module, name)

        with open(path, "rb") as f:
            payload = _DraftUnpickler(f).load()
        
        if payload.get('schema_version') != SCHEMA_VERSION:
            raise ValueError('Legacy model: run draft_model.py --train')
        system = cls()
        system.calibration = payload['calibration']
        system.evaluation = payload['evaluation']
        system.best_model = payload["model"]
        system.best_model_name = payload["model_name"]
        system.fe = payload["feature_engineering"]
        return system

    def predict_draft(self, blue_team: dict, red_team: dict, region: str = "ALL") -> dict:
        """
        Dự đoán xác suất thắng giữa 2 đội hình theo bối cảnh Khu vực / Giải đấu (LCK, LPL, LCP, WLDS, MSI, EWC, ALL).
        """
        if set(blue_team) != set(POSITIONS) or set(red_team) != set(POSITIONS):
            raise ValueError('Exactly five role assignments per team are required')
        champs = list(blue_team.values()) + list(red_team.values())
        if len(set(champs)) != 10 or any(c not in self.fe.champ_vocab for c in champs):
            raise ValueError('Unknown or duplicate champion')
        row_dict = {}
        for pos in POSITIONS:
            row_dict[f'blue_{pos}'] = blue_team.get(pos, 'Aatrox')
            row_dict[f'red_{pos}'] = red_team.get(pos, 'Renekton')
        row_dict['blue_win'] = 0  # Placeholder
        row_dict['league'] = region

        df_single = pd.DataFrame([row_dict])
        X = self.fe.transform(df_single)
        
        blue_prob = float(calibrate(self.best_model.predict_proba(X)[:, 1], self.calibration)[0])
        red_prob = 1.0 - blue_prob

        # Phân tích tương quan sức mạnh từng Lane
        lane_analysis = {}
        for pos in POSITIONS:
            b_c = blue_team.get(pos, 'Unknown')
            r_c = red_team.get(pos, 'Unknown')
            pair = (b_c, r_c)
            adv = self.fe.lane_matchup_adv.get(pos, {}).get(pair, 0.50)
            lane_analysis[pos] = {
                "blue_champion": b_c,
                "red_champion": r_c,
                "historical_encoding": round(float(adv), 4),
                "statistic_kind": "smoothed_training_feature_not_lane_win_probability"
            }

        return {
            "region": region.upper(),
            "blue_win_probability_pct": round(blue_prob * 100.0, 2),
            "red_win_probability_pct": round(red_prob * 100.0, 2),
            "favored_team": "Phe Xanh (Blue Side)" if blue_prob >= 0.50 else "Phe Đỏ (Red Side)",
            "lane_matchup_details": lane_analysis,
            "probability_kind": "calibrated_model_estimate",
            "causal_uplift": None,
            "lane_statistic_kind": "historical_team_winrate_not_lane_win_probability",
            "model_used": self.best_model_name
        }


def remove_vietnamese_accents(text: str) -> str:
    """Loại bỏ dấu tiếng Việt sinh ra do gõ Telex nhầm."""
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalize_champion_name(raw_name: str, valid_champions: list) -> str:
    """Chuẩn hóa tên tướng: xử lý viết thường, bỏ khoảng trắng/ký tự lạ/dấu telex và fuzzy match."""
    cleaned = raw_name.strip()
    # 1. Khớp chính xác
    for c in valid_champions:
        if c.lower() == cleaned.lower():
            return c
    
    # 2. Xóa khoảng trắng, dấu nháy và dấu telex
    no_accents = remove_vietnamese_accents(cleaned)
    simplified_input = no_accents.lower().replace(" ", "").replace("'", "").replace(".", "")
    
    for c in valid_champions:
        sim_c = c.lower().replace(" ", "").replace("'", "").replace(".", "")
        if sim_c == simplified_input:
            return c
            
    # 3. Bảng ánh xạ các lỗi chính tả / tên viết tắt / telex phổ biến
    alias_map = {
        'leesin': 'Lee Sin', 'lessin': 'Lee Sin', 'lein': 'Lee Sin', 'caitlynm': 'Caitlyn', 'cait': 'Caitlyn',
        'scarner': 'Skarner', 'vicktor': 'Viktor', 'viktor': 'Viktor', 'alista': 'Alistar', 'alistar': 'Alistar',
        'kam': 'Karma', 'kama': 'Karma', 'karma': 'Karma', 'locke': 'Corki', 'corki': 'Corki',
        'oriana': 'Orianna', 'orianna': 'Orianna', 'wukong': 'Wukong', 'monkey': 'Wukong', 'monkeyking': 'Wukong',
        'kaisa': 'Kai\'Sa', 'ksante': 'K\'Sante', 'ambesa': 'Ambessa', 'anie': 'Annie', 'annie': 'Annie',
        'rayze': 'Ryze', 'ynara': 'Yunara', 'yunara': 'Yunara', 'tf': 'Twisted Fate', 'asol': 'Aurelion Sol',
        'j4': 'Jarvan IV', 'jarvan': 'Jarvan IV', 'morde': 'Mordekaiser', 'renata': 'Renata Glasc',
        'tahm': 'Tahm Kench', 'tk': 'Tahm Kench', 'blitz': 'Blitzcrank', 'naut': 'Nautilus',
        'heca': 'Hecarim', 'kata': 'Katarina', 'yi': 'Master Yi', 'ez': 'Ezreal', 'mf': 'Miss Fortune', 'gp': 'Gangplank'
    }
    if simplified_input in alias_map and alias_map[simplified_input] in valid_champions:
        return alias_map[simplified_input]

    # 4. Tìm kiếm chuỗi con tương đồng
    for c in valid_champions:
        sim_c = c.lower().replace(" ", "").replace("'", "").replace(".", "")
        if simplified_input in sim_c or sim_c in simplified_input:
            return c

    return cleaned


def parse_args():
    parser = argparse.ArgumentParser(description="LOL Draft AI Prediction System (Phút 0)")
    parser.add_argument("--train", action="store_true", help="Huấn luyện và đánh giá toàn bộ mô hình")
    parser.add_argument("--predict", action="store_true", help="Chạy suy luận dự đoán với đội hình chỉ định")
    parser.add_argument("--region", type=str, default="ALL", help="Khu vực / Giải đấu: ALL, LCK, LPL, LCP, WLDS (CKTG), MSI, EWC, INTERNATIONAL")
    parser.add_argument("--blue", type=str, default="Aatrox,Vi,Ahri,Kai'Sa,Nautilus", help="Danh sách 5 tướng Phe Xanh (top,jng,mid,bot,sup)")
    parser.add_argument("--red", type=str, default="Renekton,Sejuani,Syndra,Ezreal,Leona", help="Danh sách 5 tướng Phe Đỏ (top,jng,mid,bot,sup)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.predict:
        system = LolDraftPredictionSystem.load_model()
        valid_champs = list(system.fe.champ_vocab.keys())

        b_raw = [c.strip() for c in args.blue.split(',')]
        r_raw = [c.strip() for c in args.red.split(',')]
        if len(b_raw) != 5 or len(r_raw) != 5:
            print("❌ Lỗi: Cần cung cấp chính xác 5 tướng theo thứ tự: top, jng, mid, bot, sup.")
            sys.exit(1)

        b_list = [normalize_champion_name(c, valid_champs) for c in b_raw]
        r_list = [normalize_champion_name(c, valid_champs) for c in r_raw]

        b_dict = dict(zip(POSITIONS, b_list))
        r_dict = dict(zip(POSITIONS, r_list))

        res = system.predict_draft(b_dict, r_dict, region=args.region)

        print("\n" + "=" * 70)
        print(f"🎮 KẾT QUẢ DỰ ĐOÁN XÁC SUẤT THẮNG DRAFT AI (PHÚT 0 - KHU VỰC: {res['region']})")
        print("=" * 70)
        print(f"🔵 PHE XANH (Blue Side): {', '.join(b_list)}")
        print(f"🔴 PHE ĐỎ   (Red Side) : {', '.join(r_list)}")
        print("-" * 70)
        print(f"⭐ TỶ LỆ THẮNG PHE XANH : {res['blue_win_probability_pct']}%")
        print(f"⭐ TỶ LỆ THẮNG PHE ĐỎ   : {res['red_win_probability_pct']}%")
        print(f"🏆 ĐỘI CHIẾM ƯU THẾ    : {res['favored_team']}")
        print(f"🤖 MÔ HÌNH SỬ DỤNG      : {res['model_used']}")
        print("-" * 70)
        print("📊 PHÂN TÍCH TƯƠNG QUAN 5 ĐƯỜNG THI ĐẤU:")
        for pos, info in res['lane_matchup_details'].items():
            print(f"  • {pos.upper():<4}: {info['blue_champion']:<12} vs {info['red_champion']:<12} -> Historical encoding: {info['historical_encoding']} (không phải xác suất thắng đường)")
        print("=" * 70)

    elif args.train:
        # Explicit training only
        system = LolDraftPredictionSystem()
        system.train_and_evaluate()
