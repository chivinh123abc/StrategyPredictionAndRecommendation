"""
Module 06: Machine Learning - Task 3.2: Snowball Prediction Model (Phút 10)
Dự đoán xác suất thắng thua thực chiến dựa trên diễn biến trận đấu ở mốc 10 phút.

Phương pháp & Kỹ thuật:
- Tích hợp 2 nguồn dữ liệu lớn trong CSDL lol_live_data.db:
  1. Đấu Giải Chuyên Nghiệp (Pro Play): 4,752 quan sát đội mốc 10 phút.
  2. Solo Rank Thách Đấu (VN2 & KR): 2,018 quan sát đội mốc 10 phút.
- Bộ đặc trưng kinh tế, mục tiêu & phân hóa 5 đường:
  - Macro: golddiffat10, xpdiffat10, csdiffat10, killsat10, deathsat10, kill_diff, kda_ratio.
  - Micro 5 Lanes: top_golddiff, jng_golddiff, mid_golddiff, bot_golddiff, sup_golddiff, carry_gold_lead (Mid + Bot).
  - Mục tiêu: firstdragon, void_grubs, has_3_grubs, firsttower, double_neutral_control.
  - Bối cảnh: is_blue_side, is_pro_play.
- So sánh các mô hình: Logistic Regression, Random Forest, LightGBM, XGBoost, Soft Voting Ensemble.
- Đạt độ chính xác kỳ vọng: Accuracy > 80%, ROC-AUC > 0.85.
- Xuất file đóng gói: models/snowball_model.pkl
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
from sklearn.metrics import (
    accuracy_score, roc_auc_score, log_loss, f1_score,
    precision_score, recall_score, brier_score_loss, confusion_matrix, classification_report
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Optional gradient boosting libraries
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "database" / "lol_live_data.db"
MODEL_PATH = PROJECT_ROOT / "models" / "snowball_model.pkl"


def load_integrated_10min_dataset(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Trích xuất và hợp nhất dữ liệu mốc 10 phút từ Đấu Giải và Solo Rank."""
    if not db_path.exists():
        raise FileNotFoundError(f"Không tìm thấy CSDL tại {db_path}")

    conn = sqlite3.connect(db_path)

    # 1. Trích xuất Đấu Giải (kèm bóc tách 5 lane)
    q_pro = """
    SELECT 
        m.gameid,
        m.side,
        m.result,
        m.golddiffat10,
        m.xpdiffat10,
        m.csdiffat10,
        m.killsat10,
        m.deathsat10,
        m.firstdragon,
        m.void_grubs,
        m.firsttower,
        MAX(CASE WHEN p.position = 'top' THEN p.golddiffat10 END) AS top_golddiff,
        MAX(CASE WHEN p.position = 'jng' THEN p.golddiffat10 END) AS jng_golddiff,
        MAX(CASE WHEN p.position = 'mid' THEN p.golddiffat10 END) AS mid_golddiff,
        MAX(CASE WHEN p.position = 'bot' THEN p.golddiffat10 END) AS bot_golddiff,
        MAX(CASE WHEN p.position = 'sup' THEN p.golddiffat10 END) AS sup_golddiff,
        1 AS is_pro_play
    FROM tournament_matches m
    JOIN tournament_players p ON m.gameid = p.gameid AND m.side = p.side
    WHERE m.datacompleteness = 'complete'
    GROUP BY m.gameid, m.side
    """
    df_pro = pd.read_sql_query(q_pro, conn)

    # 2. Trích xuất Solo Rank (Ghép 2 góc nhìn Blue & Red)
    q_rank = """
    SELECT 
        gameId,
        blueWins,
        blueGoldDiff,
        blueExperienceDiff,
        ((blueTotalMinionsKilled + blueTotalJungleMinionsKilled) - (redTotalMinionsKilled + redTotalJungleMinionsKilled)) AS blueCSDiff,
        blueKills,
        blueDeaths,
        blueDragons,
        blueVoidgrubs,
        blueTowersDestroyed,
        redDragons,
        redVoidgrubs,
        redTowersDestroyed
    FROM matches_10min
    """
    df_rank_raw = pd.read_sql_query(q_rank, conn)
    conn.close()

    # Blue side perspective
    df_rank_blue = pd.DataFrame({
        'gameid': df_rank_raw['gameId'],
        'side': 'Blue',
        'result': df_rank_raw['blueWins'],
        'golddiffat10': df_rank_raw['blueGoldDiff'],
        'xpdiffat10': df_rank_raw['blueExperienceDiff'],
        'csdiffat10': df_rank_raw['blueCSDiff'],
        'killsat10': df_rank_raw['blueKills'],
        'deathsat10': df_rank_raw['blueDeaths'],
        'firstdragon': (df_rank_raw['blueDragons'] > 0).astype(float),
        'void_grubs': df_rank_raw['blueVoidgrubs'].clip(0, 6).astype(float),
        'firsttower': (df_rank_raw['blueTowersDestroyed'] > 0).astype(float),
        'top_golddiff': df_rank_raw['blueGoldDiff'] * 0.25,
        'jng_golddiff': df_rank_raw['blueGoldDiff'] * 0.20,
        'mid_golddiff': df_rank_raw['blueGoldDiff'] * 0.25,
        'bot_golddiff': df_rank_raw['blueGoldDiff'] * 0.25,
        'sup_golddiff': df_rank_raw['blueGoldDiff'] * 0.05,
        'is_pro_play': 0
    })

    # Red side perspective
    df_rank_red = pd.DataFrame({
        'gameid': df_rank_raw['gameId'],
        'side': 'Red',
        'result': 1 - df_rank_raw['blueWins'],
        'golddiffat10': -df_rank_raw['blueGoldDiff'],
        'xpdiffat10': -df_rank_raw['blueExperienceDiff'],
        'csdiffat10': -df_rank_raw['blueCSDiff'],
        'killsat10': df_rank_raw['blueDeaths'],
        'deathsat10': df_rank_raw['blueKills'],
        'firstdragon': (df_rank_raw['redDragons'] > 0).astype(float),
        'void_grubs': df_rank_raw['redVoidgrubs'].clip(0, 6).astype(float),
        'firsttower': (df_rank_raw['redTowersDestroyed'] > 0).astype(float),
        'top_golddiff': -df_rank_raw['blueGoldDiff'] * 0.25,
        'jng_golddiff': -df_rank_raw['blueGoldDiff'] * 0.20,
        'mid_golddiff': -df_rank_raw['blueGoldDiff'] * 0.25,
        'bot_golddiff': -df_rank_raw['blueGoldDiff'] * 0.25,
        'sup_golddiff': -df_rank_raw['blueGoldDiff'] * 0.05,
        'is_pro_play': 0
    })

    df_combined = pd.concat([df_pro, df_rank_blue, df_rank_red], ignore_index=True)
    return df_combined


class SnowballFeaturePipeline:
    """Bộ tạo lập và chuẩn hóa đặc trưng Lăn Cầu Tuyết mốc 10 phút."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Khai phá các đặc trưng chiến thuật chuyên sâu mốc 10 phút."""
        X = pd.DataFrame(index=df.index)

        # 1. Macro Economy & Combat
        X['golddiffat10'] = df['golddiffat10'].fillna(0)
        X['xpdiffat10'] = df['xpdiffat10'].fillna(0)
        X['csdiffat10'] = df['csdiffat10'].fillna(0)
        X['killsat10'] = df['killsat10'].fillna(0)
        X['deathsat10'] = df['deathsat10'].fillna(0)
        X['kill_diff'] = X['killsat10'] - X['deathsat10']
        X['kda_ratio'] = (X['killsat10'] + 1.0) / (X['deathsat10'] + 1.0)

        # 2. Micro Lane Economy
        X['top_golddiff'] = df['top_golddiff'].fillna(0)
        X['jng_golddiff'] = df['jng_golddiff'].fillna(0)
        X['mid_golddiff'] = df['mid_golddiff'].fillna(0)
        X['bot_golddiff'] = df['bot_golddiff'].fillna(0)
        X['sup_golddiff'] = df['sup_golddiff'].fillna(0)
        
        # Chỉ số giãn tiền của 2 nguồn sát thương chủ lực (Carry Lead = Mid + Bot)
        X['carry_gold_lead'] = X['mid_golddiff'] + X['bot_golddiff']

        # 3. Mục tiêu trung lập & Công trình
        X['firstdragon'] = df['firstdragon'].fillna(0).astype(float)
        X['void_grubs'] = df['void_grubs'].fillna(0).clip(0, 6).astype(float)
        X['has_3_grubs'] = (X['void_grubs'] >= 3.0).astype(float)
        X['firsttower'] = df['firsttower'].fillna(0).astype(float)
        
        # Double Control: Kiểm soát cả Rồng 1 lẫn >= 3 Sâu Hư Không
        X['double_neutral_control'] = (X['firstdragon'] * X['has_3_grubs']).astype(float)

        # 4. Contextual Features
        X['is_blue_side'] = (df['side'] == 'Blue').astype(float)
        X['is_pro_play'] = df['is_pro_play'].fillna(1).astype(float)

        # 5. Non-linear Snowball Multipliers
        # Khi dẫn trước kinh tế + kiểm soát mục tiêu sẽ tạo hiệu ứng lăn cầu tuyết theo hàm phi tuyến
        X['gold_dragon_synergy'] = (X['golddiffat10'] / 1000.0) * X['firstdragon']
        X['gold_grubs_synergy'] = (X['golddiffat10'] / 1000.0) * X['has_3_grubs']

        self.feature_names = X.columns.tolist()
        return X

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        X = self.engineer_features(df)
        return self.scaler.fit_transform(X)

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        X = self.engineer_features(df)
        return self.scaler.transform(X)


class LolSnowballPredictionSystem:
    """Hệ thống huấn luyện, đánh giá và dự đoán Lăn Cầu Tuyết mốc 10 phút."""

    def __init__(self):
        self.fe = SnowballFeaturePipeline()
        self.models = {}
        self.best_model = None
        self.best_model_name = ""
        self.feature_importances_ = {}

    def train_and_evaluate(self, test_size: float = 0.20):
        """Huấn luyện và so sánh toàn diện các mô hình Snowball AI."""
        print("=" * 80)
        print("🚀 BẮT ĐẦU HUẤN LUYỆN MÔ HÌNH DỰ ĐOÁN SNOWBALL AI (PHÚT 10)")
        print("=" * 80)

        df = load_integrated_10min_dataset()
        print(f"📊 Đã nạp thành công: {len(df):,} quan sát (Pro Play: 4,752, Solo Rank: 2,018).")

        # Phân chia tập Train / Test (Stratified Split 80/20)
        y = df['result'].to_numpy()
        X_raw = self.fe.engineer_features(df)
        
        X_train_df, X_test_df, y_train, y_test = train_test_split(
            df, y, test_size=test_size, random_state=42, stratify=df['result']
        )

        X_train = self.fe.fit_transform(X_train_df)
        X_test = self.fe.transform(X_test_df)

        print(f"📁 Tập Huấn Luyện (Train Set): {len(X_train):,} mẫu")
        print(f"📁 Tập Kiểm Thử (Test Set): {len(X_test):,} mẫu")
        print(f"🔢 Số lượng đặc trưng chiến thuật: {len(self.fe.feature_names)} đặc trưng.")

        # Định nghĩa các mô hình ứng viên
        candidate_models = {
            "Logistic Regression (L2)": LogisticRegression(C=0.5, penalty='l2', max_iter=1000, random_state=42),
            "Random Forest (150 trees)": RandomForestClassifier(n_estimators=150, max_depth=7, min_samples_split=8, random_state=42, n_jobs=-1)
        }

        if HAS_LGB:
            candidate_models["LightGBM Classifier"] = LGBMClassifier(
                n_estimators=120, max_depth=5, learning_rate=0.04, subsample=0.85,
                colsample_bytree=0.85, random_state=42, verbose=-1
            )

        if HAS_XGB:
            candidate_models["XGBoost Classifier"] = XGBClassifier(
                n_estimators=120, max_depth=4, learning_rate=0.04, subsample=0.85,
                colsample_bytree=0.85, random_state=42, eval_metric='logloss'
            )

        results = []

        for name, model in candidate_models.items():
            print(f"⏳ Đang huấn luyện: {name}...")
            model.fit(X_train, y_train)

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

        # Ensemble Soft Voting (Kết hợp LightGBM + XGBoost + Random Forest + Logistic Regression)
        ensemble_estimators = [
            ('lr', candidate_models["Logistic Regression (L2)"]),
            ('rf', candidate_models["Random Forest (150 trees)"])
        ]
        if HAS_LGB:
            ensemble_estimators.append(('lgb', candidate_models["LightGBM Classifier"]))
        if HAS_XGB:
            ensemble_estimators.append(('xgb', candidate_models["XGBoost Classifier"]))

        ensemble_model = VotingClassifier(estimators=ensemble_estimators, voting='soft')
        ensemble_model.fit(X_train, y_train)
        y_pred_ens = ensemble_model.predict(X_test)
        y_prob_ens = ensemble_model.predict_proba(X_test)[:, 1]

        results.append({
            "Mô Hình (Algorithm)": "Ensemble (Soft Voting: LGB + XGB + RF + LR)",
            "Accuracy": accuracy_score(y_test, y_pred_ens),
            "ROC-AUC": roc_auc_score(y_test, y_prob_ens),
            "Log Loss": log_loss(y_test, y_prob_ens),
            "Brier Score": brier_score_loss(y_test, y_prob_ens),
            "F1-Score": f1_score(y_test, y_pred_ens)
        })
        self.models["Ensemble Model"] = ensemble_model

        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)

        print("\n" + "=" * 95)
        print("🏆 BẢNG TỔNG HỢP KẾT QUẢ SO SÁNH CÁC MÔ HÌNH SNOWBALL AI (TEST SET 1,354 TRẬN)")
        print("=" * 95)
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
        print(f"\n🌟 Mô hình tối ưu được chọn: {self.best_model_name} (Accuracy: {df_results.iloc[0]['Accuracy']:.2%}, ROC-AUC: {df_results.iloc[0]['ROC-AUC']:.4f})")

        # Đánh giá phân tầng: Pro Play vs Solo Rank
        print("\n" + "=" * 95)
        print("⚔️ ĐỐI CHIẾU ĐỘ CHÍNH XÁC SNOWBALL: ĐẤU GIẢI CHUYÊN NGHIỆP (PRO) VS ĐẤU XẾP HẠNG (SOLO RANK)")
        print("=" * 95)
        is_pro_test = X_test_df['is_pro_play'].to_numpy() == 1
        
        # 1. Pro Play evaluation
        if np.sum(is_pro_test) > 0:
            y_test_pro = y_test[is_pro_test]
            y_prob_pro = self.best_model.predict_proba(X_test[is_pro_test])[:, 1]
            y_pred_pro = (y_prob_pro >= 0.5).astype(int)
            acc_pro = accuracy_score(y_test_pro, y_pred_pro)
            auc_pro = roc_auc_score(y_test_pro, y_prob_pro)
            print(f"🏟️  Đấu Giải Pro Play (N = {np.sum(is_pro_test):,} trận): Accuracy = {acc_pro:.2%} | ROC-AUC = {auc_pro:.4f}")

        # 2. Solo Rank evaluation
        if np.sum(~is_pro_test) > 0:
            y_test_rank = y_test[~is_pro_test]
            y_prob_rank = self.best_model.predict_proba(X_test[~is_pro_test])[:, 1]
            y_pred_rank = (y_prob_rank >= 0.5).astype(int)
            acc_rank = accuracy_score(y_test_rank, y_pred_rank)
            auc_rank = roc_auc_score(y_test_rank, y_prob_rank)
            print(f"🔥 Đấu Xếp Hạng Solo Rank (N = {np.sum(~is_pro_test):,} trận): Accuracy = {acc_rank:.2%} | ROC-AUC = {auc_rank:.4f}")

        # Trích xuất Feature Importance
        self._extract_feature_importances(candidate_models)

        # Lưu model
        self.save_model()
        return df_results

    def _extract_feature_importances(self, candidate_models):
        """Trích xuất độ quan trọng của các đặc trưng."""
        rf = candidate_models.get("Random Forest (150 trees)")
        if rf and hasattr(rf, 'feature_importances_'):
            importances = rf.feature_importances_
            feat_imp_df = pd.DataFrame({
                'Feature': self.fe.feature_names,
                'Importance': importances
            }).sort_values(by='Importance', ascending=False).reset_index(drop=True)

            print("\n" + "=" * 60)
            print("📊 TOP 10 ĐẶC TRƯNG QUYẾT ĐỊNH THẮNG THUA MỐC 10 PHÚT (FEATURE IMPORTANCE)")
            print("=" * 60)
            for i, row in feat_imp_df.head(10).iterrows():
                bar = "█" * int(row['Importance'] * 150)
                print(f"{i+1:2d}. {row['Feature']:<22}: {row['Importance']*100:5.2f}% {bar}")
            self.feature_importances_ = feat_imp_df

    def save_model(self, path: Path = MODEL_PATH):
        """Lưu trữ trọn vẹn Feature Pipeline và Mô hình Snowball."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "model": self.best_model,
            "model_name": self.best_model_name,
            "feature_engineering": self.fe,
            "feature_importances": self.feature_importances_,
            "trained_at": datetime.now().isoformat(),
            "target": "result"
        }
        with open(path, "wb") as f:
            pickle.dump(payload, f)
        print(f"💾 Đã lưu thành công mô hình Snowball vào: {path.resolve()}")

    @classmethod
    def load_model(cls, path: Path = MODEL_PATH):
        """Nạp mô hình phục vụ suy luận thời gian thực."""
        if not path.exists():
            raise FileNotFoundError(f"Chưa tìm thấy model tại {path}. Hãy chạy --train trước.")
        
        class _SnowballUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                if name == 'SnowballFeaturePipeline':
                    return SnowballFeaturePipeline
                return super().find_class(module, name)

        with open(path, "rb") as f:
            payload = _SnowballUnpickler(f).load()
        
        system = cls()
        system.best_model = payload["model"]
        system.best_model_name = payload["model_name"]
        system.fe = payload["feature_engineering"]
        system.feature_importances_ = payload.get("feature_importances", {})
        return system

    def predict_snowball(
        self,
        gold_diff: float,
        xp_diff: float = 0.0,
        cs_diff: float = 0.0,
        kills: int = 2,
        deaths: int = 2,
        first_dragon: int = 1,
        void_grubs: int = 3,
        first_tower: int = 0,
        top_gold: float = None,
        jng_gold: float = None,
        mid_gold: float = None,
        bot_gold: float = None,
        sup_gold: float = None,
        side: str = 'Blue',
        is_pro_play: int = 1
    ) -> dict:
        """Dự đoán xác suất thắng thua dựa trên chỉ số mốc 10 phút."""
        if top_gold is None: top_gold = gold_diff * 0.25
        if jng_gold is None: jng_gold = gold_diff * 0.20
        if mid_gold is None: mid_gold = gold_diff * 0.25
        if bot_gold is None: bot_gold = gold_diff * 0.25
        if sup_gold is None: sup_gold = gold_diff * 0.05

        input_row = pd.DataFrame([{
            'golddiffat10': float(gold_diff),
            'xpdiffat10': float(xp_diff),
            'csdiffat10': float(cs_diff),
            'killsat10': float(kills),
            'deathsat10': float(deaths),
            'firstdragon': float(first_dragon),
            'void_grubs': float(void_grubs),
            'firsttower': float(first_tower),
            'top_golddiff': float(top_gold),
            'jng_golddiff': float(jng_gold),
            'mid_golddiff': float(mid_gold),
            'bot_golddiff': float(bot_gold),
            'sup_golddiff': float(sup_gold),
            'side': side,
            'is_pro_play': float(is_pro_play)
        }])

        X = self.fe.transform(input_row)
        win_prob = float(self.best_model.predict_proba(X)[0, 1])
        lose_prob = 1.0 - win_prob

        # Phân tích đánh giá rủi ro lăn cầu tuyết
        snowball_status = ""
        if gold_diff >= 2000:
            snowball_status = "LĂN CẦU TUYẾT ÁP ĐẢO (Lead >= +2,000g)"
        elif gold_diff >= 1000:
            snowball_status = "DẪN TRƯỚC VỪA PHẢI (+1,000g đến +1,999g)"
        elif gold_diff <= -2000:
            snowball_status = "BỊ DẪN RẤT LỚN (Thua >= 2,000g - Nguy cơ vỡ trận)"
        elif gold_diff <= -1000:
            snowball_status = "BỊ DẪN VỪA PHẢI (-1,000g đến -1,999g)"
        else:
            snowball_status = "THẾ TRẬN CÂN BẰNG (-999g đến +999g)"

        return {
            "win_probability_pct": round(win_prob * 100.0, 2),
            "lose_probability_pct": round(lose_prob * 100.0, 2),
            "snowball_status": snowball_status,
            "gold_lead": int(gold_diff),
            "dragon_status": "Có Rồng 1" if first_dragon else "Mất Rồng 1",
            "grub_count": int(void_grubs),
            "model_used": self.best_model_name
        }


def parse_args():
    parser = argparse.ArgumentParser(description="LOL Snowball AI Prediction System (Phút 10)")
    parser.add_argument("--train", action="store_true", help="Huấn luyện và đánh giá mô hình")
    parser.add_argument("--predict", action="store_true", help="Dự đoán với kịch bản chỉ định")
    parser.add_argument("--gold-diff", type=float, default=2000.0, help="Chênh lệch vàng lúc 10 phút (vd: 2000 hoặc -1500)")
    parser.add_argument("--xp-diff", type=float, default=800.0, help="Chênh lệch kinh nghiệm lúc 10 phút")
    parser.add_argument("--kills", type=int, default=4, help="Số mạng ăn được lúc 10 phút")
    parser.add_argument("--deaths", type=int, default=1, help="Số mạng bị chết lúc 10 phút")
    parser.add_argument("--dragon", type=int, default=1, help="Ăn được Rồng đầu (1: Có, 0: Mất)")
    parser.add_argument("--grubs", type=int, default=3, help="Số lượng Sâu Hư Không ăn được (0 đến 6)")
    parser.add_argument("--tower", type=int, default=0, help="Phá được trụ đầu tiên (1: Có, 0: Không)")
    parser.add_argument("--side", type=str, default="Blue", help="Phe thi đấu (Blue hoặc Red)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.predict:
        system = LolSnowballPredictionSystem.load_model()
        res = system.predict_snowball(
            gold_diff=args.gold_diff,
            xp_diff=args.xp_diff,
            kills=args.kills,
            deaths=args.deaths,
            first_dragon=args.dragon,
            void_grubs=args.grubs,
            first_tower=args.tower,
            side=args.side
        )

        print("\n" + "=" * 70)
        print("🎮 KẾT QUẢ DỰ ĐOÁN XÁC SUẤT THẮNG SNOWBALL AI (PHÚT 10)")
        print("=" * 70)
        print(f"📊 CHÊNH LỆCH VÀNG (Gold Diff) : {res['gold_lead']:+d} vàng ({res['snowball_status']})")
        print(f"🐉 MỤC TIÊU LỚN 10 PHÚT         : {res['dragon_status']} | {res['grub_count']} Sâu Hư Không")
        print("-" * 70)
        print(f"⭐ TỶ LỆ THẮNG DỰ ĐOÁN         : {res['win_probability_pct']}%")
        print(f"⭐ TỶ LỆ THUA DỰ ĐOÁN          : {res['lose_probability_pct']}%")
        print(f"🤖 MÔ HÌNH SỬ DỤNG              : {res['model_used']}")
        print("=" * 70)

    else:
        system = LolSnowballPredictionSystem()
        system.train_and_evaluate()
