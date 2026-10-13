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

POSITIONS = ['top', 'jng', 'mid', 'bot', 'sup']

# Bảng thuộc tính chiến thuật nền tảng cho các nhóm tướng chính
# [AP_ratio, Hard_CC, Tankiness, Early_Power, Scaling]
CHAMPION_ARCHETYPE_MAP = {
    # Mages / AP
    'Ahri': [0.9, 0.7, 0.3, 0.6, 0.7], 'Syndra': [1.0, 0.8, 0.2, 0.5, 0.9],
    'Orianna': [1.0, 0.7, 0.3, 0.4, 0.9], 'Taliyah': [0.9, 0.7, 0.3, 0.7, 0.8],
    'Azir': [0.9, 0.6, 0.3, 0.3, 1.0], 'Viktor': [1.0, 0.5, 0.2, 0.3, 1.0],
    'LeBlanc': [0.9, 0.6, 0.2, 0.9, 0.6], 'Hwei': [1.0, 0.7, 0.2, 0.4, 0.9],
    'Cassiopeia': [1.0, 0.7, 0.4, 0.3, 1.0], 'Brand': [1.0, 0.6, 0.2, 0.6, 0.8],
    # Tanks / Frontliners
    'K\'Sante': [0.2, 0.8, 0.9, 0.4, 0.8], 'Ornn': [0.4, 0.9, 1.0, 0.3, 0.9],
    'Sion': [0.2, 0.8, 1.0, 0.3, 0.8], 'Malphite': [0.6, 0.9, 0.9, 0.3, 0.8],
    'Maokai': [0.7, 0.9, 0.9, 0.5, 0.7], 'Sejuani': [0.4, 0.9, 0.9, 0.5, 0.7],
    'Zac': [0.6, 0.9, 0.9, 0.4, 0.8], 'Rammus': [0.3, 0.8, 1.0, 0.4, 0.7],
    'Nautilus': [0.6, 1.0, 0.9, 0.7, 0.4], 'Leona': [0.3, 1.0, 0.9, 0.7, 0.4],
    'Alistar': [0.4, 1.0, 0.9, 0.6, 0.5], 'Rell': [0.3, 1.0, 0.8, 0.7, 0.5],
    # Bruisers / Juggernauts
    'Aatrox': [0.1, 0.6, 0.7, 0.6, 0.8], 'Renekton': [0.1, 0.6, 0.7, 0.9, 0.4],
    'Gwen': [0.9, 0.2, 0.6, 0.3, 1.0], 'Jax': [0.3, 0.6, 0.7, 0.5, 0.9],
    'Camille': [0.2, 0.7, 0.6, 0.4, 0.9], 'Rumble': [0.9, 0.5, 0.5, 0.9, 0.6],
    'Illaoi': [0.1, 0.3, 0.8, 0.7, 0.7], 'Darius': [0.1, 0.5, 0.7, 0.8, 0.5],
    'Mordekaiser': [0.9, 0.5, 0.8, 0.6, 0.7], 'Gnar': [0.2, 0.7, 0.7, 0.6, 0.7],
    # Junglers (Fighters & Assassins)
    'Vi': [0.1, 0.9, 0.6, 0.7, 0.6], 'Jarvan IV': [0.2, 0.8, 0.7, 0.8, 0.5],
    'Xin Zhao': [0.1, 0.6, 0.6, 0.9, 0.4], 'Lee Sin': [0.1, 0.6, 0.5, 0.9, 0.4],
    'Nocturne': [0.1, 0.6, 0.5, 0.7, 0.6], 'Viego': [0.1, 0.5, 0.5, 0.6, 0.8],
    'Nidalee': [0.9, 0.1, 0.2, 0.9, 0.4], 'Elise': [0.9, 0.7, 0.3, 0.9, 0.3],
    # Marksmen (ADCs)
    'Varus': [0.4, 0.6, 0.2, 0.8, 0.6], 'Kalista': [0.1, 0.4, 0.3, 0.9, 0.4],
    'Ashe': [0.2, 0.8, 0.2, 0.8, 0.6], 'Kai\'Sa': [0.4, 0.1, 0.3, 0.5, 0.9],
    'Jinx': [0.1, 0.4, 0.2, 0.3, 1.0], 'Ezreal': [0.2, 0.1, 0.3, 0.6, 0.7],
    'Jhin': [0.1, 0.6, 0.2, 0.7, 0.7], 'Lucian': [0.2, 0.1, 0.3, 0.9, 0.5],
    'Zeri': [0.2, 0.2, 0.3, 0.3, 1.0], 'Xayah': [0.1, 0.5, 0.4, 0.5, 0.8],
    'Draven': [0.1, 0.4, 0.3, 1.0, 0.3], 'Smolder': [0.3, 0.2, 0.2, 0.2, 1.0],
    # Enchanters / Supports
    'Lulu': [0.8, 0.7, 0.3, 0.6, 0.8], 'Nami': [0.8, 0.8, 0.2, 0.7, 0.6],
    'Karma': [0.8, 0.4, 0.4, 0.9, 0.5], 'Renata Glasc': [0.7, 0.9, 0.4, 0.5, 0.9],
    'Bard': [0.7, 0.9, 0.4, 0.6, 0.8], 'Rakan': [0.5, 0.9, 0.6, 0.6, 0.7],
    'Braum': [0.3, 0.8, 0.9, 0.6, 0.6], 'Tahm Kench': [0.6, 0.7, 0.9, 0.5, 0.7]
}
DEFAULT_ARCHETYPE = [0.3, 0.5, 0.5, 0.5, 0.5]


def load_pivoted_draft_data(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Trích xuất 3,000 trận đấu giải và xoay trục 10 vị trí tướng."""
    if not db_path.exists():
        raise FileNotFoundError(f"Không tìm thấy CSDL tại {db_path}")

    conn = sqlite3.connect(db_path)
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
        self.lane_matchup_adv = {}
        self.synergy_pair_adv = {}
        self.scaler = StandardScaler()
        self.feature_names = []

    def fit(self, df: pd.DataFrame):
        """Học từ điển tướng, tỷ lệ thắng Bayes, đối đầu và phối hợp từ tập train."""
        # 1. Tạo từ điển tướng xuất hiện
        all_champs = set()
        for pos in POSITIONS:
            all_champs.update(df[f'blue_{pos}'].dropna().unique())
            all_champs.update(df[f'red_{pos}'].dropna().unique())
        
        self.champ_vocab = {champ: i for i, champ in enumerate(sorted(all_champs))}
        self.vocab_size = len(self.champ_vocab)

        # 2. Tính Bayesian Smoothed Winrate cho từng tướng
        champ_stats = {c: {'wins': 0, 'games': 0} for c in self.champ_vocab}
        for _, row in df.iterrows():
            win = row['blue_win']
            for pos in POSITIONS:
                b_c = row[f'blue_{pos}']
                r_c = row[f'red_{pos}']
                if b_c in champ_stats:
                    champ_stats[b_c]['games'] += 1
                    if win == 1: champ_stats[b_c]['wins'] += 1
                if r_c in champ_stats:
                    champ_stats[r_c]['games'] += 1
                    if win == 0: champ_stats[r_c]['wins'] += 1

        for c, s in champ_stats.items():
            # Bayesian formula: (wins + C * prior) / (games + C)
            smoothed_wr = (s['wins'] + self.bayesian_weight * self.bayesian_prior_wr) / (s['games'] + self.bayesian_weight)
            self.champ_winrates[c] = smoothed_wr

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

    def _extract_archetype(self, champ_name: str) -> list:
        return CHAMPION_ARCHETYPE_MAP.get(champ_name, DEFAULT_ARCHETYPE)

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
            
            blue_comp_arch = np.zeros(5)
            red_comp_arch = np.zeros(5)

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

                # Archetype attributes
                blue_comp_arch += np.array(self._extract_archetype(b_champ))
                red_comp_arch += np.array(self._extract_archetype(r_champ))

            # Sức mạnh tổng thể Meta của từng đội
            avg_b_wr = np.mean(blue_champ_wrs)
            avg_r_wr = np.mean(red_champ_wrs)
            dense_row.append(avg_b_wr - avg_r_wr)  # Hiệu số winrate meta

            # Synergy Mid-Jng và Bot-Sup
            b_mid_jng = self.synergy_pair_adv['mid_jng'].get((row['blue_mid'], row['blue_jng']), 0.5)
            r_mid_jng = self.synergy_pair_adv['mid_jng'].get((row['red_mid'], row['red_jng']), 0.5)
            dense_row.append(b_mid_jng - r_mid_jng)

            b_bot_sup = self.synergy_pair_adv['bot_sup'].get((row['blue_bot'], row['blue_sup']), 0.5)
            r_bot_sup = self.synergy_pair_adv['bot_sup'].get((row['red_bot'], row['red_sup']), 0.5)
            dense_row.append(b_bot_sup - r_bot_sup)

            # Cân bằng thuộc tính đội hình (Blue - Red)
            diff_arch = (blue_comp_arch - red_comp_arch) / 5.0
            dense_row.extend(diff_arch.tolist())

            # Blue side base bias
            dense_row.append(1.0)

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


class LolDraftPredictionSystem:
    """Hệ thống huấn luyện, đánh giá và dự đoán Cấm/Chọn 2 giai đoạn."""

    def __init__(self):
        self.fe = DraftFeatureEngineering(half_life_days=90.0)
        self.models = {}
        self.best_model = None
        self.best_model_name = ""
        self.scaler = StandardScaler()

    def train_and_evaluate(self, test_size: float = 0.20):
        """Huấn luyện toàn diện và so sánh các thuật toán Machine Learning."""
        print("=" * 80)
        print("🚀 BẮT ĐẦU HUẤN LUYỆN MÔ HÌNH DỰ ĐOÁN DRAFT AI (PHÚT 0)")
        print("=" * 80)

        df = load_pivoted_draft_data()
        print(f"📊 Đã nạp thành công: {len(df):,} trận đấu giải chuyên nghiệp.")

        # Phân chia tập Train / Test theo thời gian (Time-based split 80/20)
        split_idx = int(len(df) * (1 - test_size))
        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()

        print(f"📁 Tập Huấn Luyện (Train Set): {len(train_df):,} trận (từ {train_df['date'].min()[:10]} đến {train_df['date'].max()[:10]})")
        print(f"📁 Tập Kiểm Thử (Test Set): {len(test_df):,} trận (từ {test_df['date'].min()[:10]} đến {test_df['date'].max()[:10]})")

        # Fit & Transform Features
        self.fe.fit(train_df)
        X_train = self.fe.transform(train_df)
        y_train = train_df['blue_win'].to_numpy()
        sample_weights_train = self.fe.compute_sample_weights(train_df['date'])

        X_test = self.fe.transform(test_df)
        y_test = test_df['blue_win'].to_numpy()

        print(f"🔢 Số chiều không gian đặc trưng (Feature Dimensions): {X_train.shape[1]:,} cột.")

        # Định nghĩa các mô hình ứng viên
        candidate_models = {
            "Logistic Regression (L2)": LogisticRegression(C=0.15, penalty='l2', max_iter=1000, random_state=42),
            "Random Forest (150 trees)": RandomForestClassifier(n_estimators=150, max_depth=8, min_samples_split=6, random_state=42, n_jobs=-1),
            "Multi-Layer Perceptron (MLP)": MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', alpha=0.01, max_iter=400, random_state=42)
        }

        if HAS_LGB:
            candidate_models["LightGBM Classifier"] = LGBMClassifier(
                n_estimators=120, max_depth=5, learning_rate=0.03, subsample=0.8,
                colsample_bytree=0.8, random_state=42, verbose=-1
            )

        if HAS_XGB:
            candidate_models["XGBoost Classifier"] = XGBClassifier(
                n_estimators=120, max_depth=4, learning_rate=0.04, subsample=0.8,
                colsample_bytree=0.8, random_state=42, eval_metric='logloss'
            )

        results = []

        for name, model in candidate_models.items():
            print(f"⏳ Đang huấn luyện: {name}...")
            # Huấn luyện có sample weights nếu thuật toán hỗ trợ
            if hasattr(model, 'fit') and 'sample_weight' in model.fit.__code__.co_varnames:
                model.fit(X_train, y_train, sample_weight=sample_weights_train)
            else:
                model.fit(X_train, y_train)

            # Dự đoán trên Test set
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            acc = accuracy_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_prob)
            ll = log_loss(y_test, y_prob)
            brier = brier_score_loss(y_test, y_prob)
            f1 = f1_score(y_test, y_pred)

            results.append({
                "Mô Hình (Algorithm)": name,
                "Accuracy": acc,
                "ROC-AUC": auc,
                "Log Loss": ll,
                "Brier Score": brier,
                "F1-Score": f1
            })
            self.models[name] = model

        # Xây dựng Ensemble Voting Classifier (Kết hợp Logistic Regression + Random Forest / LightGBM)
        ensemble_estimators = [
            ('lr', candidate_models["Logistic Regression (L2)"]),
            ('rf', candidate_models["Random Forest (150 trees)"])
        ]
        if HAS_LGB:
            ensemble_estimators.append(('lgb', candidate_models["LightGBM Classifier"]))

        ensemble_model = VotingClassifier(estimators=ensemble_estimators, voting='soft')
        ensemble_model.fit(X_train, y_train)
        y_pred_ens = ensemble_model.predict(X_test)
        y_prob_ens = ensemble_model.predict_proba(X_test)[:, 1]

        results.append({
            "Mô Hình (Algorithm)": "Ensemble (Soft Voting: LR + RF + LGB)",
            "Accuracy": accuracy_score(y_test, y_pred_ens),
            "ROC-AUC": roc_auc_score(y_test, y_prob_ens),
            "Log Loss": log_loss(y_test, y_prob_ens),
            "Brier Score": brier_score_loss(y_test, y_prob_ens),
            "F1-Score": f1_score(y_test, y_pred_ens)
        })
        self.models["Ensemble Model"] = ensemble_model

        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)

        print("\n" + "=" * 90)
        print("🏆 BẢNG TỔNG HỢP KẾT QUẢ SO SÁNH CÁC MÔ HÌNH DỰ ĐOÁN DRAFT AI (TEST SET 600 TRẬN)")
        print("=" * 90)
        print(df_results.to_string(index=False, formatters={
            'Accuracy': '{:.2%}'.format,
            'ROC-AUC': '{:.4f}'.format,
            'Log Loss': '{:.4f}'.format,
            'Brier Score': '{:.4f}'.format,
            'F1-Score': '{:.4f}'.format
        }))

        # Chọn mô hình tốt nhất
        self.best_model_name = df_results.iloc[0]["Mô Hình (Algorithm)"]
        self.best_model = self.models.get(self.best_model_name, ensemble_model)
        print(f"\n🌟 Mô hình tối ưu được chọn: {self.best_model_name} (ROC-AUC: {df_results.iloc[0]['ROC-AUC']:.4f})")

        # Lưu model
        self.save_model()
        return df_results

    def save_model(self, path: Path = MODEL_PATH):
        """Lưu trữ trọn vẹn Feature Pipeline và Mô hình Machine Learning."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "model": self.best_model,
            "model_name": self.best_model_name,
            "feature_engineering": self.fe,
            "trained_at": datetime.now().isoformat(),
            "target": "blue_win"
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
        
        system = cls()
        system.best_model = payload["model"]
        system.best_model_name = payload["model_name"]
        system.fe = payload["feature_engineering"]
        return system

    def predict_draft(self, blue_team: dict, red_team: dict) -> dict:
        """
        Dự đoán xác suất thắng giữa 2 đội hình.
        Input format:
        blue_team = {'top': 'Aatrox', 'jng': 'Vi', 'mid': 'Ahri', 'bot': 'Kai\'Sa', 'sup': 'Nautilus'}
        red_team  = {'top': 'Renekton', 'jng': 'Sejuani', 'mid': 'Syndra', 'bot': 'Ezreal', 'sup': 'Leona'}
        """
        row_dict = {}
        for pos in POSITIONS:
            row_dict[f'blue_{pos}'] = blue_team.get(pos, 'Aatrox')
            row_dict[f'red_{pos}'] = red_team.get(pos, 'Renekton')
        row_dict['blue_win'] = 0  # Placeholder

        df_single = pd.DataFrame([row_dict])
        X = self.fe.transform(df_single)
        
        blue_prob = float(self.best_model.predict_proba(X)[0, 1])
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
                "blue_lane_advantage_pct": round(adv * 100.0, 1),
                "favored_side": "Blue" if adv >= 0.50 else "Red"
            }

        return {
            "blue_win_probability_pct": round(blue_prob * 100.0, 2),
            "red_win_probability_pct": round(red_prob * 100.0, 2),
            "favored_team": "Phe Xanh (Blue Side)" if blue_prob >= 0.50 else "Phe Đỏ (Red Side)",
            "lane_matchup_details": lane_analysis,
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

        res = system.predict_draft(b_dict, r_dict)

        print("\n" + "=" * 70)
        print("🎮 KẾT QUẢ DỰ ĐOÁN XÁC SUẤT THẮNG DRAFT AI (PHÚT 0)")
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
            print(f"  • {pos.upper():<4}: {info['blue_champion']:<12} vs {info['red_champion']:<12} -> Blue Advantage: {info['blue_lane_advantage_pct']}% ({info['favored_side']})")
        print("=" * 70)

    else:
        # Default action: Train & Evaluate
        system = LolDraftPredictionSystem()
        system.train_and_evaluate()
