"""
================================================================================
MODULE 02: DATA PREPROCESSING & CLEANING PIPELINE (LÀM SẠCH & TIỀN XỬ LÝ)
Dự án: Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI) - LMHT
Môn học: Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT)
Nhiệm vụ: Task 1.3 [Thành viên 1] - Làm sạch dữ liệu & Xử lý ngoại lai (IQR/Z-Score)
================================================================================
Mô tả chi tiết:
- Đọc dữ liệu từ CSDL SQLite (lol_live_data.db) và các tệp dữ liệu thô.
- Thực hiện 5 trụ cột làm sạch dữ liệu theo chuẩn giáo trình Chương 2 (Data Preparation):
    1. Domain Filtering: Loại bỏ 100% trận Remake (< 10 phút) và AFK (CS < 10).
    2. Missing Value Imputation:
       - Zero-Imputation cho các sự kiện đếm mục tiêu (elders, atakhans, doublekills...).
       - Categorical-Imputation ('NoBan') cho các lượt cấm bị bỏ qua.
       - Task-based Split: Lọc theo datacompleteness cho bài toán mốc 10 phút.
    3. Outlier Detection & Handling:
       - Phương pháp IQR (Interquartile Range) với ngưỡng [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
       - Phương pháp Z-Score với ngưỡng |Z| > 3.0.
       - Hỗ trợ cả 2 chế độ: Trimming (Lọc bỏ ngoại lai) và Winsorization (Cắt ngọn/Capping).
    4. Feature Engineering: Tính toán thêm các chỉ số chuẩn hóa phục vụ EDA và Machine Learning.
    5. Xuất các tập dữ liệu sạch vào data/processed/:
       - clean_ranked_10min.csv
       - clean_tournament_10min.csv
       - clean_tournament_draft.csv
       - clean_tournament_players.csv
================================================================================
"""

import os
import sys
import sqlite3
import argparse
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List, Optional, Any

# 1. Nạp cấu hình trung tâm từ src.config
try:
    from src.config.settings import (
        BASE_DIR,
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        DATABASE_DIR,
        OUTPUT_DB,
        OUTPUT_CSV,
        get_active_esports_file,
    )
except ImportError:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(CURRENT_DIR)
    BASE_DIR = os.path.dirname(SRC_DIR)
    sys.path.insert(0, BASE_DIR)
    from src.config.settings import (
        BASE_DIR,
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        DATABASE_DIR,
        OUTPUT_DB,
        OUTPUT_CSV,
        get_active_esports_file,
    )


class DataCleaner:
    """
    Class chịu trách nhiệm thực thi toàn bộ quy trình Làm sạch, Khử khuyết thiếu,
    và Xử lý giá trị ngoại lai cho cả 2 nguồn dữ liệu Solo Rank và Đấu Giải.
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        output_dir: Optional[str] = None,
        outlier_method: str = "iqr",
        outlier_action: str = "filter",
        z_thresh: float = 3.0,
        iqr_multiplier: float = 1.5,
    ):
        self.db_path = db_path or OUTPUT_DB
        self.output_dir = output_dir or PROCESSED_DATA_DIR
        self.outlier_method = outlier_method.lower()  # 'iqr', 'zscore', 'both'
        self.outlier_action = outlier_action.lower()  # 'filter' (trim), 'cap' (winsorize)
        self.z_thresh = z_thresh
        self.iqr_multiplier = iqr_multiplier
        os.makedirs(self.output_dir, exist_ok=True)

        # Nhật ký thống kê tiền xử lý (Audit Log)
        self.cleaning_log = {
            "ranked": {},
            "tournament_matches": {},
            "tournament_players": {},
        }

    def detect_outliers_iqr(self, df: pd.DataFrame, column: str) -> Tuple[pd.Series, float, float]:
        """
        Phát hiện ngoại lai theo phương pháp IQR (Chương 2).
        Trả về: boolean mask (True nếu là ngoại lai), lower_bound, upper_bound.
        """
        valid_series = df[column].dropna()
        q1 = valid_series.quantile(0.25)
        q3 = valid_series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - self.iqr_multiplier * iqr
        upper_bound = q3 + self.iqr_multiplier * iqr
        is_outlier = (df[column] < lower_bound) | (df[column] > upper_bound)
        return is_outlier, lower_bound, upper_bound

    def detect_outliers_zscore(self, df: pd.DataFrame, column: str) -> Tuple[pd.Series, float, float]:
        """
        Phát hiện ngoại lai theo phương pháp Z-Score (Chương 2).
        Trả về: boolean mask (True nếu là ngoại lai), lower_val, upper_val tương ứng |Z| = thresh.
        """
        valid_series = df[column].dropna()
        mean = valid_series.mean()
        std = valid_series.std()
        if std == 0 or np.isnan(std):
            return pd.Series(False, index=df.index), mean, mean
        z_scores = (df[column] - mean) / std
        is_outlier = z_scores.abs() > self.z_thresh
        lower_val = mean - self.z_thresh * std
        upper_val = mean + self.z_thresh * std
        return is_outlier, lower_val, upper_val

    def handle_outliers(
        self,
        df: pd.DataFrame,
        columns: List[str],
        dataset_name: str,
    ) -> pd.DataFrame:
        """
        Áp dụng thuật toán phát hiện và xử lý ngoại lai (Filter hoặc Cap) trên danh sách cột chỉ định.
        """
        df_clean = df.copy()
        outlier_summary = {}

        for col in columns:
            if col not in df_clean.columns:
                continue

            # Phát hiện ngoại lai theo phương pháp chỉ định
            if self.outlier_method == "zscore":
                is_outlier, lower, upper = self.detect_outliers_zscore(df_clean, col)
                method_label = f"Z-Score (|Z|>{self.z_thresh})"
            elif self.outlier_method == "both":
                is_iqr, low_iqr, up_iqr = self.detect_outliers_iqr(df_clean, col)
                is_z, low_z, up_z = self.detect_outliers_zscore(df_clean, col)
                is_outlier = is_iqr & is_z  # Ngoại lai đồng thuận cả 2 thuật toán
                lower, upper = max(low_iqr, low_z), min(up_iqr, up_z)
                method_label = "IQR & Z-Score Đồng Thuận"
            else:  # Mặc định IQR
                is_outlier, lower, upper = self.detect_outliers_iqr(df_clean, col)
                method_label = f"IQR ({self.iqr_multiplier}x)"

            outlier_count = int(is_outlier.sum())
            outlier_summary[col] = {
                "outlier_count": outlier_count,
                "lower_bound": round(lower, 2),
                "upper_bound": round(upper, 2),
                "method": method_label,
            }

            if outlier_count > 0:
                if self.outlier_action == "cap":
                    # Winsorization: Cắt ngọn các giá trị vượt ngưỡng về đúng giá trị cận
                    df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
                elif self.outlier_action == "filter":
                    # Trimming: Loại bỏ các dòng chứa giá trị ngoại lai
                    df_clean = df_clean[~is_outlier]

        self.cleaning_log[dataset_name]["outlier_details"] = outlier_summary
        return df_clean

    def clean_ranked_data(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        """
        Tiền xử lý và làm sạch dữ liệu Solo Rank (bảng matches_10min).
        """
        initial_rows = len(df_raw)
        df = df_raw.copy()

        # 1. Domain Filtering: Loại bỏ trận Remake và trận AFK
        # Remake: Thời lượng game thực tế < 600s (10 phút)
        is_remake = df["gameDuration"] < 600
        # AFK: Tổng lính cả đội lúc 10 phút < 10 (người chơi đứng yên ở bệ đá cổ)
        is_afk = (df["blueTotalMinionsKilled"] < 10) | (df["redTotalMinionsKilled"] < 10)

        invalid_mask = is_remake | is_afk
        remake_count = int(is_remake.sum())
        afk_count = int(is_afk.sum())
        df = df[~invalid_mask]

        # 2. Missing Value Imputation
        # Điền 'NoBan' cho các lượt cấm để trống
        if "blueBans" in df.columns:
            df["blueBans"] = df["blueBans"].fillna("NoBan")
        if "redBans" in df.columns:
            df["redBans"] = df["redBans"].fillna("NoBan")

        # Đảm bảo các cột kinh tế mốc 10 phút không bị âm bất thường
        econ_cols = [c for c in df.columns if "Gold" in c or "Experience" in c or "Kills" in c]
        for col in econ_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0).clip(lower=0)

        # 3. Outlier Handling trên các biến chênh lệch quan trọng
        outlier_target_cols = ["blueGoldDiff", "blueExperienceDiff", "blueTotalGold", "redTotalGold"]
        rows_before_outlier = len(df)
        df = self.handle_outliers(df, outlier_target_cols, "ranked")
        outliers_removed = rows_before_outlier - len(df)

        # 4. Feature Engineering: Tạo các chỉ số chuẩn hóa phục vụ EDA & Model
        df["goldDiffPerMin10"] = df["blueGoldDiff"] / 10.0
        df["blueKDA10"] = (df["blueKills"]) / np.maximum(df["blueDeaths"], 1)
        df["redKDA10"] = (df["redKills"]) / np.maximum(df["redDeaths"], 1)

        self.cleaning_log["ranked"].update({
            "initial_rows": initial_rows,
            "remake_removed": remake_count,
            "afk_removed": afk_count,
            "outliers_removed": outliers_removed,
            "final_rows": len(df),
            "retention_rate": round(len(df) * 100.0 / initial_rows, 2),
        })

        return df

    def clean_tournament_matches(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Tiền xử lý và làm sạch dữ liệu Đấu Giải Cấp Đội Tuyển (tournament_matches).
        Trả về 2 tập:
        - df_clean_10min: Tập dữ liệu sạch có mốc 10 phút (phục vụ mô hình Snowball & T-test)
        - df_clean_draft: Toàn bộ 100% các trận sạch (phục vụ mô hình Cấm/Chọn Draft AI & Recommender)
        """
        initial_rows = len(df_raw)
        df = df_raw.copy()

        # 1. Domain Filtering: Lọc trận quá ngắn (< 600s)
        is_remake = df["gamelength"] < 600
        remake_count = int(is_remake.sum())
        df = df[~is_remake]

        # 2. Missing Value Imputation (Chuẩn hóa 5 nhóm đã định nghĩa)
        # Nhóm 2: Lượt cấm rỗng -> Điền 'NoBan'
        ban_cols = ["ban1", "ban2", "ban3", "ban4", "ban5"]
        for b_col in ban_cols:
            if b_col in df.columns:
                df[b_col] = df[b_col].fillna("NoBan")

        # Nhóm 3: Các sự kiện đếm không xuất hiện -> Zero Imputation
        count_zero_cols = [
            "firstdragon", "dragons", "opp_dragons", "elementaldrakes", "opp_elementaldrakes",
            "infernals", "mountains", "clouds", "oceans", "chemtechs", "hextechs", "dragons_type_unknown",
            "elders", "opp_elders", "firstherald", "heralds", "opp_heralds", "void_grubs", "opp_void_grubs",
            "firstbaron", "barons", "opp_barons", "atakhans", "opp_atakhans", "firsttower", "towers",
            "opp_towers", "firstmidtower", "firsttothreetowers", "turretplates", "opp_turretplates",
            "inhibitors", "opp_inhibitors", "firstblood", "doublekills", "triplekills", "quadrakills", "pentakills",
        ]
        for c_col in count_zero_cols:
            if c_col in df.columns:
                df[c_col] = df[c_col].fillna(0)

        # Tập 1: Dành cho Cấm/Chọn (Draft Phase) - Giữ trọn vẹn toàn bộ các trận
        df_clean_draft = df.copy()

        # Tập 2: Dành cho Snowball Mốc 10 phút - Lọc các trận complete
        df_10min = df[df["datacompleteness"] == "complete"].copy()
        initial_10min_rows = len(df_10min)

        # 3. Outlier Handling trên tập 10 phút
        outlier_target_cols = ["golddiffat10", "xpdiffat10", "csdiffat10", "totalgold", "damagetochampions"]
        rows_before_outlier = len(df_10min)
        df_clean_10min = self.handle_outliers(df_10min, outlier_target_cols, "tournament_matches")
        outliers_removed = rows_before_outlier - len(df_clean_10min)

        # 4. Feature Engineering bổ trợ
        df_clean_10min["goldDiffPerMin10"] = df_clean_10min["golddiffat10"] / 10.0
        df_clean_10min["csDiffPerMin10"] = df_clean_10min["csdiffat10"] / 10.0

        self.cleaning_log["tournament_matches"].update({
            "initial_rows": initial_rows,
            "remake_removed": remake_count,
            "total_draft_matches": len(df_clean_draft),
            "complete_10min_initial": initial_10min_rows,
            "outliers_removed": outliers_removed,
            "final_10min_rows": len(df_clean_10min),
            "retention_rate_10min": round(len(df_clean_10min) * 100.0 / max(initial_10min_rows, 1), 2),
        })

        return df_clean_10min, df_clean_draft

    def clean_tournament_players(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        """
        Tiền xử lý và làm sạch dữ liệu Tuyển thủ Đấu Giải (tournament_players).
        """
        initial_rows = len(df_raw)
        df = df_raw.copy()

        # 1. Domain Filtering: Lọc bản ghi rỗng tướng hoặc thời lượng bất thường
        valid_mask = df["champion"].notna() & (df["gamelength"] >= 600)
        df = df[valid_mask]

        # 2. Missing Value Imputation
        # Điền 0 cho các chỉ số sự kiện cá nhân
        player_zero_cols = [
            "kills", "deaths", "assists", "doublekills", "triplekills", "quadrakills", "pentakills",
            "firstblood", "firstbloodkill", "firstbloodassist", "firstbloodvictim", "damageshare",
            "earnedgoldshare", "goldat10", "xpat10", "csat10", "golddiffat10", "xpdiffat10", "csdiffat10",
        ]
        for col in player_zero_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)

        # Điền 'Unknown' cho tên người chơi bị khuyết
        if "playername" in df.columns:
            df["playername"] = df["playername"].fillna("Unknown")

        # 3. Outlier Handling: Khử ngoại lai trên các chỉ số cá nhân mốc 10 phút
        outlier_cols = ["golddiffat10", "csdiffat10", "damagetochampions", "dpm"]
        rows_before_outlier = len(df)
        df_clean = self.handle_outliers(df, outlier_cols, "tournament_players")
        outliers_removed = rows_before_outlier - len(df_clean)

        # 4. Feature Engineering: KDA cá nhân
        df_clean["kda"] = (df_clean["kills"] + df_clean["assists"]) / np.maximum(df_clean["deaths"], 1)

        self.cleaning_log["tournament_players"].update({
            "initial_rows": initial_rows,
            "outliers_removed": outliers_removed,
            "final_rows": len(df_clean),
            "retention_rate": round(len(df_clean) * 100.0 / initial_rows, 2),
        })

        return df_clean

    def print_cleaning_report(self):
        """
        In Báo cáo Tổng kết Làm sạch Dữ liệu & Khử Ngoại lai trực quan (Data Cleaning Card).
        """
        print("\n" + "=" * 80)
        print("🧹 BÁO CÁO TỔNG KẾT TIỀN XỬ LÝ & LÀM SẠCH DỮ LIỆU (DATA CLEANING REPORT)")
        print(f"   • Phương pháp Ngoại lai: {self.outlier_method.upper()} (Hành động: {self.outlier_action.upper()})")
        print("=" * 80)

        # 1. Báo cáo Solo Rank
        r_log = self.cleaning_log.get("ranked", {})
        print(f"📊 1. Dữ Liệu Solo Rank Mốc 10 Phút (matches_10min):")
        print(f"   • Số dòng ban đầu     : {r_log.get('initial_rows', 0):,} dòng")
        print(f"   • Loại bỏ Remake/AFK  : {r_log.get('remake_removed', 0) + r_log.get('afk_removed', 0)} dòng")
        print(f"   • Loại bỏ Ngoại lai   : {r_log.get('outliers_removed', 0)} dòng")
        print(f"   • Số dòng sạch đầu ra : {r_log.get('final_rows', 0):,} dòng (Tỷ lệ giữ lại: {r_log.get('retention_rate', 0)}%)")

        # 2. Báo cáo Tournament Matches
        tm_log = self.cleaning_log.get("tournament_matches", {})
        print(f"\n🏆 2. Dữ Liệu Đấu Giải Cấp Đội Tuyển (tournament_matches):")
        print(f"   • Số dòng ban đầu     : {tm_log.get('initial_rows', 0):,} dòng")
        print(f"   • Tập Cấm/Chọn (Draft): {tm_log.get('total_draft_matches', 0):,} dòng (Giữ trọn vẹn 100% 3,000 trận)")
        print(f"   • Tập Mốc 10 Phút     : {tm_log.get('complete_10min_initial', 0):,} dòng (Các trận complete)")
        print(f"   • Loại bỏ Ngoại lai   : {tm_log.get('outliers_removed', 0)} dòng")
        print(f"   • Đầu ra sạch 10 phút : {tm_log.get('final_10min_rows', 0):,} dòng (Tỷ lệ giữ lại: {tm_log.get('retention_rate_10min', 0)}%)")

        # 3. Báo cáo Tournament Players
        tp_log = self.cleaning_log.get("tournament_players", {})
        print(f"\n👤 3. Dữ Liệu Tuyển Thủ Cá Nhân (tournament_players):")
        print(f"   • Số dòng ban đầu     : {tp_log.get('initial_rows', 0):,} dòng")
        print(f"   • Loại bỏ Ngoại lai   : {tp_log.get('outliers_removed', 0)} dòng")
        print(f"   • Số dòng sạch đầu ra : {tp_log.get('final_rows', 0):,} dòng (Tỷ lệ giữ lại: {tp_log.get('retention_rate', 0)}%)")

        print("=" * 80 + "\n")

    def run(self) -> Dict[str, pd.DataFrame]:
        """
        Thực thi toàn bộ luồng tiền xử lý, lưu các tệp CSV sạch và xuất báo cáo.
        """
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"LỖI: Không tìm thấy CSDL tại '{self.db_path}'! Hãy chạy Task 1.1 và 1.2 trước.")

        print(f"🚀 Bắt đầu quy trình Tiền xử lý & Làm sạch dữ liệu từ: {self.db_path}")
        conn = sqlite3.connect(self.db_path)

        try:
            # 1. Đọc dữ liệu từ SQLite
            print("📖 Đang nạp dữ liệu thô từ 3 bảng SQLite...")
            rank_raw = pd.read_sql("SELECT * FROM matches_10min", conn)
            tour_matches_raw = pd.read_sql("SELECT * FROM tournament_matches", conn)
            tour_players_raw = pd.read_sql("SELECT * FROM tournament_players", conn)

            # 2. Làm sạch từng tập dữ liệu
            print("🧹 Đang làm sạch dữ liệu Solo Rank...")
            clean_ranked = self.clean_ranked_data(rank_raw)

            print("🧹 Đang làm sạch dữ liệu Đấu Giải Cấp Đội Tuyển...")
            clean_tour_10min, clean_tour_draft = self.clean_tournament_matches(tour_matches_raw)

            print("🧹 Đang làm sạch dữ liệu Tuyển thủ Đấu Giải...")
            clean_tour_players = self.clean_tournament_players(tour_players_raw)

            # 3. Xuất các file CSV sạch vào data/processed/
            print(f"💾 Đang lưu các tập dữ liệu sạch vào: {self.output_dir}")
            clean_ranked_path = os.path.join(self.output_dir, "clean_ranked_10min.csv")
            clean_tour_10min_path = os.path.join(self.output_dir, "clean_tournament_10min.csv")
            clean_tour_draft_path = os.path.join(self.output_dir, "clean_tournament_draft.csv")
            clean_tour_players_path = os.path.join(self.output_dir, "clean_tournament_players.csv")

            clean_ranked.to_csv(clean_ranked_path, index=False)
            clean_tour_10min.to_csv(clean_tour_10min_path, index=False)
            clean_tour_draft.to_csv(clean_tour_draft_path, index=False)
            clean_tour_players.to_csv(clean_tour_players_path, index=False)

            print(f"   ✅ [1] Đã xuất: {clean_ranked_path} ({len(clean_ranked):,} dòng)")
            print(f"   ✅ [2] Đã xuất: {clean_tour_10min_path} ({len(clean_tour_10min):,} dòng)")
            print(f"   ✅ [3] Đã xuất: {clean_tour_draft_path} ({len(clean_tour_draft):,} dòng)")
            print(f"   ✅ [4] Đã xuất: {clean_tour_players_path} ({len(clean_tour_players):,} dòng)")

            # 4. In báo cáo hoàn tất
            self.print_cleaning_report()

            return {
                "clean_ranked_10min": clean_ranked,
                "clean_tournament_10min": clean_tour_10min,
                "clean_tournament_draft": clean_tour_draft,
                "clean_tournament_players": clean_tour_players,
            }

        finally:
            conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Data Preprocessing & Cleaning Pipeline (Làm sạch & Khử ngoại lai IQR/Z-score)"
    )
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help=f"Đường dẫn file SQLite CSDL (mặc định: {OUTPUT_DB})",
    )
    parser.add_argument(
        "--outlier-method",
        type=str,
        choices=["iqr", "zscore", "both"],
        default="iqr",
        help="Phương pháp phát hiện ngoại lai: iqr (mặc định), zscore, hoặc both",
    )
    parser.add_argument(
        "--outlier-action",
        type=str,
        choices=["filter", "cap"],
        default="filter",
        help="Hành động xử lý ngoại lai: filter (lọc bỏ/trimming) hoặc cap (cắt ngọn/winsorization)",
    )
    parser.add_argument(
        "--iqr-multiplier",
        type=float,
        default=1.5,
        help="Hệ số nhân IQR (mặc định: 1.5)",
    )
    parser.add_argument(
        "--z-thresh",
        type=float,
        default=3.0,
        help="Ngưỡng Z-Score (mặc định: 3.0)",
    )

    args = parser.parse_args()
    cleaner = DataCleaner(
        db_path=args.db,
        outlier_method=args.outlier_method,
        outlier_action=args.outlier_action,
        iqr_multiplier=args.iqr_multiplier,
        z_thresh=args.z_thresh,
    )
    cleaner.run()


if __name__ == "__main__":
    main()
