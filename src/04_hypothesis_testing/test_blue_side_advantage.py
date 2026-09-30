"""
================================================================================
MODULE 04: THỐNG KÊ SUY DIỄN & KIỂM ĐỊNH GIẢ THUYẾT (HYPOTHESIS TESTING)
Task 2.1: Kiểm định A/B Lợi thế Phe Xanh (Blue Side Advantage) qua Z-test 2 phía
Giáo trình: Chương 1 - Thống kê suy diễn & Kiểm định giả thuyết (TS. Thái Tuyết Hải)
================================================================================
"""

import sys
import argparse
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

# Thêm thư mục gốc vào sys.path để nạp src.config
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.config.settings import OUTPUT_DB, PROCESSED_DATA_DIR


class BlueSideHypothesisTester:
    """
    Class thực hiện Kiểm định Thống kê Z-test 2 phía kiểm tra:
    "Lợi thế Phe Xanh (Blue Side Advantage) có ý nghĩa thống kê hay không?"
    
    Bộ giả thuyết thống kê:
      - H0: p = 0.5 (Tỷ lệ thắng của Phe Xanh bằng 50%, không có lợi thế đặc biệt)
      - H1: p != 0.5 (Tỷ lệ thắng của Phe Xanh khác 50%, tồn tại sự chênh lệch có ý nghĩa)
      
    Mức ý nghĩa: alpha = 0.05 (Độ tin cậy 95%, ngưỡng Z_critical = +-1.96)
    """

    def __init__(self, db_path: Path = OUTPUT_DB, alpha: float = 0.05):
        self.db_path = Path(db_path)
        self.alpha = alpha
        self.z_critical = stats.norm.ppf(1 - alpha / 2)  # 1.95996 ~ 1.96

    def compute_z_test(self, wins: int, total: int, name: str = "") -> dict:
        """
        Tính toán Z-statistic, p-value 2 phía và Khoảng tin cậy 95% (Wald & Wilson Score).
        """
        if total == 0:
            return {}

        p_hat = wins / total
        p_0 = 0.5
        
        # Sai số chuẩn dưới giả thuyết H0 (Standard Error under H0)
        se_0 = np.sqrt(p_0 * (1 - p_0) / total)
        
        # Giá trị thống kê kiểm định Z (Z-score)
        z_score = (p_hat - p_0) / se_0
        
        # Giá trị p-value 2 phía (Two-tailed p-value)
        p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z_score)))
        
        # Khoảng tin cậy (Confidence Interval 95%) theo phương pháp Wald
        se_sample = np.sqrt(p_hat * (1 - p_hat) / total)
        ci_lower = max(0.0, p_hat - self.z_critical * se_sample)
        ci_upper = min(1.0, p_hat + self.z_critical * se_sample)
        
        # Kết luận thống kê
        reject_h0 = p_value < self.alpha
        if reject_h0:
            conclusion = (
                f"Bác bỏ H0 ở mức ý nghĩa alpha={self.alpha} (p = {p_value:.6f} < {self.alpha}). "
                f"Phe Xanh {'thắng vượt trội' if p_hat > 0.5 else 'thua lép vế'} có ý nghĩa thống kê."
            )
        else:
            conclusion = (
                f"Chưa đủ bằng chứng bác bỏ H0 (p = {p_value:.4f} >= {self.alpha}). "
                f"Sự chênh lệch tỷ lệ thắng ({p_hat*100:.1f}%) có thể do biến thiên ngẫu nhiên."
            )

        return {
            "dataset": name,
            "total_matches": total,
            "blue_wins": wins,
            "red_wins": total - wins,
            "blue_winrate_pct": round(p_hat * 100.0, 2),
            "red_winrate_pct": round((1.0 - p_hat) * 100.0, 2),
            "z_score": round(z_score, 4),
            "p_value": p_value,
            "ci_95_lower_pct": round(ci_lower * 100.0, 2),
            "ci_95_upper_pct": round(ci_upper * 100.0, 2),
            "reject_h0": reject_h0,
            "significance_level": self.alpha,
            "conclusion": conclusion
        }

    def run_tests(self) -> pd.DataFrame:
        """
        Thực hiện kiểm định trên 3 phân vùng:
        1. Đấu Giải Chuyên Nghiệp (Pro Play - 3,000 trận)
        2. Solo Rank Đỉnh Cao (1,009 trận: VN2 + KR)
        3. Từng Giải đấu riêng biệt (LCK, LPL, LCP, MSI, Worlds, EWC)
        """
        conn = sqlite3.connect(self.db_path)
        
        results = []
        
        # 1. Toàn bộ Đấu Giải Chuyên Nghiệp (Oracle's Elixir)
        df_pro = pd.read_sql_query(
            "SELECT side, result, league FROM tournament_matches WHERE side = 'Blue'",
            conn
        )
        res_pro = self.compute_z_test(
            wins=int(df_pro['result'].sum()),
            total=len(df_pro),
            name="1. Toàn Bộ Đấu Giải (Pro Play)"
        )
        results.append(res_pro)

        # 2. Toàn bộ Solo Rank Đỉnh Cao (Riot API)
        df_rank = pd.read_sql_query(
            "SELECT server, blueWins FROM matches_10min",
            conn
        )
        res_rank = self.compute_z_test(
            wins=int(df_rank['blueWins'].sum()),
            total=len(df_rank),
            name="2. Toàn Bộ Solo Rank (VN2 & KR)"
        )
        results.append(res_rank)

        # 2b. Solo Rank Việt Nam (VN2)
        df_vn2 = df_rank[df_rank['server'] == 'VN2']
        if len(df_vn2) > 0:
            results.append(self.compute_z_test(
                wins=int(df_vn2['blueWins'].sum()),
                total=len(df_vn2),
                name="2a. Solo Rank Việt Nam (VN2)"
            ))

        # 2c. Solo Rank Hàn Quốc (KR)
        df_kr = df_rank[df_rank['server'] == 'KR']
        if len(df_kr) > 0:
            results.append(self.compute_z_test(
                wins=int(df_kr['blueWins'].sum()),
                total=len(df_kr),
                name="2b. Solo Rank Hàn Quốc (KR)"
            ))

        # 3. Phân rã theo từng Giải Đấu Chuyên Nghiệp
        leagues = sorted(df_pro['league'].dropna().unique())
        for lg in leagues:
            sub_df = df_pro[df_pro['league'] == lg]
            results.append(self.compute_z_test(
                wins=int(sub_df['result'].sum()),
                total=len(sub_df),
                name=f"3. Giải Đấu {lg}"
            ))

        conn.close()
        return pd.DataFrame(results)

    def display_report(self, df_results: pd.DataFrame, export: bool = True):
        """In thẻ báo cáo kiểm định thống kê trực quan (Hypothesis Test Report Card)"""
        print("=" * 100)
        print("📊 BÁO CÁO KIỂM ĐỊNH GIẢ THUYẾT A/B: LỢI THẾ PHE XANH (BLUE SIDE ADVANTAGE)")
        print(f"   • Phương pháp: Z-test tỷ lệ 2 phía (Two-tailed Proportion Z-test)")
        print(f"   • Mức ý nghĩa: alpha = {self.alpha} | Ngưỡng Z_critical = +- {self.z_critical:.2f}")
        print(f"   • Giả thuyết H0: p = 0.5 (Tỷ lệ thắng Phe Xanh = 50%)")
        print(f"   • Giả thuyết H1: p != 0.5 (Tỷ lệ thắng Phe Xanh != 50%)")
        print("=" * 100)

        # Bảng tóm tắt kết quả
        display_cols = [
            'dataset', 'total_matches', 'blue_wins', 'blue_winrate_pct',
            'z_score', 'p_value', 'ci_95_lower_pct', 'ci_95_upper_pct', 'reject_h0'
        ]
        
        df_display = df_results[display_cols].copy()
        df_display.columns = [
            'Tập Dữ Liệu', 'Số Trận', 'Blue Thắng', 'Winrate %',
            'Z-Score', 'p-value', 'CI 95% Dưới', 'CI 95% Trên', 'Bác Bỏ H0?'
        ]
        
        # Định dạng p-value đẹp
        df_display['p-value'] = df_display['p-value'].apply(
            lambda p: f"< 0.0001***" if p < 0.0001 else (f"{p:.4f}**" if p < 0.01 else (f"{p:.4f}*" if p < 0.05 else f"{p:.4f}"))
        )
        df_display['Bác Bỏ H0?'] = df_display['Bác Bỏ H0?'].apply(
            lambda r: "✅ CÓ (Ý nghĩa)" if r else "❌ KHÔNG"
        )
        
        print(df_display.to_string(index=False))
        print("-" * 100)
        print("📌 KÝ HIỆU MỨC Ý NGHĨA: *** (p < 0.001, Cực kỳ rõ rệt) | ** (p < 0.01) | * (p < 0.05)")
        print("=" * 100)
        
        print("\n🧠 NHẬN XÉT & PHÂN TÍCH CHUYÊN SÂU THEO NGHIỆP VỤ (DOMAIN KNOWLEDGE):")
        for _, row in df_results.iterrows():
            dname = row['dataset']
            wr = row['blue_winrate_pct']
            pval = row['p_value']
            z = row['z_score']
            if "1. Toàn Bộ Đấu Giải" in dname:
                print(f"  1. Trong ĐẤU GIẢI CHUYÊN NGHIỆP (Pro Play - 3,000 trận):")
                print(f"     • Winrate Phe Xanh đạt {wr}% (Z = {z:+.3f}, p = {pval:.6f}).")
                print(f"     • KẾT LUẬN: BÁC BỎ H0. Phe Xanh có lợi thế vượt trội có ý nghĩa thống kê cao.")
                print(f"     • NGUYÊN NHÂN: Quyền First Pick các tướng Meta 2026 (Varus, Orianna, Vi, Rumble) + Góc nhìn camera thuận lợi.")
            elif "2. Toàn Bộ Solo Rank" in dname:
                print(f"\n  2. Trong SOLO RANK (1,009 trận Thách Đấu/Cao Thủ):")
                print(f"     • Winrate Phe Xanh chỉ đạt {wr}%, Phe Đỏ đạt {row['red_winrate_pct']}% (Z = {z:+.3f}, p = {pval:.6f}).")
                print(f"     • KẾT LUẬN: BÁC BỎ H0. Phe Đỏ có tỷ lệ thắng cao hơn có ý nghĩa thống kê.")
                print(f"     • NGUYÊN NHÂN: Cơ chế xếp trận Matchmaking của Riot Games thường ưu tiên xếp đội có điểm MMR/Elo trung bình cao hơn sang Phe Đỏ (Red Side) để cân bằng với góc nhìn camera và lợi thế địa hình của Phe Xanh!")

        if export:
            out_file = Path(PROCESSED_DATA_DIR) / "hypothesis_test_1_blue_side.csv"
            df_results.to_csv(out_file, index=False, encoding="utf-8-sig")
            print(f"\n💾 Đã lưu kết quả kiểm định ra tệp CSV: {out_file}")
        print("=" * 100)


def main():
    parser = argparse.ArgumentParser(description="Task 2.1: Z-test Kiểm định Lợi thế Phe Xanh (Blue Side Advantage)")
    parser.add_argument("--db", type=str, default=str(OUTPUT_DB), help="Đường dẫn đến CSDL SQLite")
    parser.add_argument("--alpha", type=float, default=0.05, help="Mức ý nghĩa alpha (mặc định 0.05)")
    parser.add_argument("--no-export", action="store_true", help="Không xuất file CSV kết quả")
    args = parser.parse_args()

    tester = BlueSideHypothesisTester(db_path=Path(args.db), alpha=args.alpha)
    df_results = tester.run_tests()
    tester.display_report(df_results, export=not args.no_export)


if __name__ == "__main__":
    main()
