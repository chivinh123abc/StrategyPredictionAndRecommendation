"""Canonical domain cleaning and CSV export.

Retains signed differences, legitimate extreme games and missing measurements.
IQR/Z-score helper methods are available for separate teaching experiments;
they do not filter or cap the canonical datasets used for analysis/training.
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


sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

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
        from analysis_data import clean_ranked
        df = clean_ranked(df_raw)
        self.cleaning_log['ranked'].update(initial_rows=len(df_raw),final_rows=len(df),retention_rate=round(100*len(df)/max(len(df_raw),1),2))
        return df

    def clean_tournament_matches(self, df_raw):
        from analysis_data import clean_matches, complete_10min
        draft = clean_matches(df_raw)
        minute10 = complete_10min(draft)
        self.cleaning_log['tournament_matches'].update(initial_rows=len(df_raw), total_draft_matches=len(draft), complete_10min_initial=len(minute10),final_10min_rows=len(minute10),retention_rate_10min=round(100*len(minute10)/max(len(df_raw),1),2))
        return minute10,draft

    def clean_tournament_players(self, df_raw):
        from analysis_data import clean_players
        df=clean_players(df_raw)
        self.cleaning_log['tournament_players'].update(initial_rows=len(df_raw),final_rows=len(df),retention_rate=round(100*len(df)/max(len(df_raw),1),2))
        return df

    def print_cleaning_report(self):
        """
        In Báo cáo Tổng kết Làm sạch Dữ liệu & Khử Ngoại lai trực quan (Data Cleaning Card).
        """
        print("\n" + "=" * 80)
        print("🧹 BÁO CÁO TỔNG KẾT TIỀN XỬ LÝ & LÀM SẠCH DỮ LIỆU (DATA CLEANING REPORT)")
        print("   • Canonical policy: domain-v2-signed-no-trimming; IQR/Z-score chỉ dùng khảo sát riêng.")
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
            from analysis_data import load_clean_tables
            rank_raw, tour_matches_raw, tour_players_raw = load_clean_tables(self.db_path)

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
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',default=None)
    parser.add_argument('--output-dir',default=None)
    args=parser.parse_args()
    DataCleaner(db_path=args.db,output_dir=args.output_dir).run()


if __name__=='__main__':main()
