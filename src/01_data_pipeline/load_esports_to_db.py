"""
================================================================================
MODULE 01: LOAD ESPORTS DATA TO SQLITE DATABASE (ETL PIPELINE)
Dự án: Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI) - LMHT
Môn học: Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT)
Nhiệm vụ: Task 1.2 [Thành viên 1] - Nạp dữ liệu giải đấu chuyên nghiệp vào SQLite
================================================================================
Mô tả chi tiết:
- Đọc dữ liệu giải đấu hoạt động (tệp esports_active_matches.csv hoặc mùa giải mới nhất)
- Phân tách và chuẩn hóa dữ liệu thành 2 bảng quan hệ chuẩn 1NF/3NF:
    1. tournament_matches : Thông tin tổng quan cấp trận & đội tuyển (6,000 dòng = 3,000 trận x 2 phe)
    2. tournament_players : Thống kê chi tiết từng tuyển thủ theo 5 vị trí (30,000 dòng = 3,000 trận x 10 người)
- Tự động chuẩn hóa tên cột (snake_case hợp lệ, khử khoảng trắng và ký tự đặc biệt)
- Thiết lập Primary Key, Foreign Key (gameid) và hệ thống Index tối ưu truy vấn SQL
- Xác thực toàn vẹn dữ liệu (Data Integrity Validation) sau khi nạp.
================================================================================
"""

import os
import sys
import time
import sqlite3
import argparse
import pandas as pd
from typing import Optional, Tuple, Dict, Any

# 1. Nạp cấu hình trung tâm từ src.config
try:
    from src.config.settings import (
        BASE_DIR,
        DATA_DIR,
        RAW_DATA_DIR,
        DATABASE_DIR,
        OUTPUT_DB,
        get_active_esports_file,
        ESPORTS_SEASON,
    )
except ImportError:
    # Fallback nếu chạy trực tiếp script từ thư mục bất kỳ
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(CURRENT_DIR)
    BASE_DIR = os.path.dirname(SRC_DIR)
    sys.path.insert(0, BASE_DIR)
    from src.config.settings import (
        BASE_DIR,
        DATA_DIR,
        RAW_DATA_DIR,
        DATABASE_DIR,
        OUTPUT_DB,
        get_active_esports_file,
        ESPORTS_SEASON,
    )


# 2. Bảng ánh xạ chuẩn hóa tên cột đặc biệt trong dữ liệu Oracle's Elixir
COLUMN_RENAME_MAP = {
    "team kpm": "team_kpm",
    "dragons (type unknown)": "dragons_type_unknown",
    "earned gpm": "earned_gpm",
    "total cs": "total_cs",
}


def sanitize_column_name(col: str) -> str:
    """Chuẩn hóa tên cột thành định dạng hợp lệ cho SQL identifier."""
    if col in COLUMN_RENAME_MAP:
        return COLUMN_RENAME_MAP[col]
    cleaned = col.strip().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    return cleaned


def infer_sqlite_type(series: pd.Series) -> str:
    """Suy luận kiểu dữ liệu SQLite từ Pandas Series."""
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "REAL"
    elif pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    else:
        return "TEXT"


class EsportsDatabaseLoader:
    """
    Class quản lý toàn bộ quy trình ETL nạp dữ liệu Đấu giải chuyên nghiệp vào SQLite.
    """

    def __init__(self, source_csv: Optional[str] = None, db_path: Optional[str] = None):
        self.source_csv = source_csv or get_active_esports_file()
        self.db_path = db_path or OUTPUT_DB

    def load_and_clean_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Đọc tệp CSV giải đấu, chuẩn hóa tên cột và phân tách thành 2 tập dữ liệu:
        - matches_df: Cấp độ trận đấu / đội tuyển (position == 'team')
        - players_df: Cấp độ tuyển thủ cá nhân (position != 'team')
        """
        if not os.path.exists(self.source_csv):
            raise FileNotFoundError(
                f"LỖI: Không tìm thấy tệp dữ liệu giải đấu tại '{self.source_csv}'!\n"
                f"Hãy chạy lệnh sau để đồng bộ dữ liệu từ Google Drive trước:\n"
                f"  python src/01_data_pipeline/sync_google_drive.py --leagues LCK,LCP,LPL,MSI,WLDS,EWC"
            )

        print(f"📖 Đang đọc dữ liệu giải đấu từ: {self.source_csv}")
        start_time = time.time()
        raw_df = pd.read_csv(self.source_csv, low_memory=False)
        read_duration = time.time() - start_time
        print(f"   -> Đã đọc {len(raw_df):,} dòng, {len(raw_df.columns)} cột ({read_duration:.2f}s)")

        # Chuẩn hóa tên cột
        raw_df.rename(columns=sanitize_column_name, inplace=True)

        # 1. Phân tách tập trận đấu / đội tuyển
        team_mask = raw_df["position"] == "team"
        matches_df = raw_df[team_mask].copy()

        # Loại bỏ các cột chỉ thuộc cấp độ cá nhân (100% rỗng ở hàng team)
        team_null_cols = [c for c in matches_df.columns if matches_df[c].isna().all()]
        if "position" in matches_df.columns:
            team_null_cols.append("position")  # Redundant vì luôn là 'team'
        matches_df.drop(columns=list(set(team_null_cols)), inplace=True, errors="ignore")

        # 2. Phân tách tập tuyển thủ cá nhân
        players_df = raw_df[~team_mask].copy()

        # Loại bỏ các cột chỉ thuộc cấp độ đội (100% rỗng ở hàng player)
        player_null_cols = [c for c in players_df.columns if players_df[c].isna().all()]
        players_df.drop(columns=list(set(player_null_cols)), inplace=True, errors="ignore")

        print(f"   -> Tập Trận đấu (tournament_matches): {len(matches_df):,} dòng, {len(matches_df.columns)} cột")
        print(f"   -> Tập Tuyển thủ (tournament_players): {len(players_df):,} dòng, {len(players_df.columns)} cột")

        return matches_df, players_df

    def create_schema(self, conn: sqlite3.Connection, matches_df: pd.DataFrame, players_df: pd.DataFrame, force: bool = False):
        """
        Tạo cấu trúc bảng tournament_matches và tournament_players với ràng buộc PK, FK và Data Types chuẩn.
        """
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        if force:
            print("⚠️ Cờ --force được kích hoạt: Xóa bảng cũ nếu đã tồn tại...")
            cursor.execute("DROP TABLE IF EXISTS tournament_players;")
            cursor.execute("DROP TABLE IF EXISTS tournament_matches;")
            conn.commit()

        # 1. Tạo bảng tournament_matches
        match_col_defs = []
        for col in matches_df.columns:
            sql_type = infer_sqlite_type(matches_df[col])
            match_col_defs.append(f"    {col} {sql_type}")
        
        # Thêm ràng buộc khóa chính: (gameid, side) hoặc (gameid, participantid)
        match_col_defs.append("    PRIMARY KEY (gameid, side)")

        create_matches_sql = f"""
CREATE TABLE IF NOT EXISTS tournament_matches (
{',\n'.join(match_col_defs)}
);
"""
        cursor.execute(create_matches_sql)

        # 2. Tạo bảng tournament_players
        player_col_defs = []
        for col in players_df.columns:
            sql_type = infer_sqlite_type(players_df[col])
            player_col_defs.append(f"    {col} {sql_type}")
        
        # Thêm ràng buộc khóa chính và khóa ngoại
        player_col_defs.append("    PRIMARY KEY (gameid, participantid)")
        player_col_defs.append("    FOREIGN KEY (gameid, side) REFERENCES tournament_matches(gameid, side) ON DELETE CASCADE")

        create_players_sql = f"""
CREATE TABLE IF NOT EXISTS tournament_players (
{',\n'.join(player_col_defs)}
);
"""
        cursor.execute(create_players_sql)
        conn.commit()
        print("✅ Đã thiết lập cấu trúc Schema chuẩn hóa cho tournament_matches & tournament_players.")

    def insert_dataframe(self, conn: sqlite3.Connection, table_name: str, df: pd.DataFrame, batch_size: int = 2000):
        """
        Nạp DataFrame vào bảng SQLite sử dụng lệnh INSERT OR REPLACE (Idempotent Transaction).
        """
        cols = list(df.columns)
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        sql = f"INSERT OR REPLACE INTO {table_name} ({col_names}) VALUES ({placeholders});"

        # Thay thế NaN bằng None để SQLite nhận diện là NULL
        records = df.where(pd.notnull(df), None).values.tolist()

        cursor = conn.cursor()
        total_rows = len(records)
        print(f"📥 Đang nạp {total_rows:,} bản ghi vào bảng '{table_name}'...")

        start_time = time.time()
        for i in range(0, total_rows, batch_size):
            batch = records[i:i + batch_size]
            cursor.executemany(sql, batch)
            conn.commit()
            sys.stdout.write(f"\r   -> Tiến độ: {min(i + batch_size, total_rows):,}/{total_rows:,} dòng ({((min(i + batch_size, total_rows)/total_rows)*100):.1f}%)")
            sys.stdout.flush()
        
        duration = time.time() - start_time
        print(f"\n   ✅ Hoàn tất nạp bảng '{table_name}' trong {duration:.2f}s ({total_rows / max(duration, 0.001):.0f} dòng/s)")

    def create_indexes(self, conn: sqlite3.Connection):
        """
        Tạo hệ thống Index tối ưu hóa tốc độ thực thi cho 5 câu truy vấn SQL nâng cao ở Module 03.
        """
        cursor = conn.cursor()
        print("⚡ Đang tạo hệ thống Index tối ưu hiệu năng truy vấn...")

        indexes = [
            # Indexes cho tournament_matches
            "CREATE INDEX IF NOT EXISTS idx_tm_league_year ON tournament_matches (league, year);",
            "CREATE INDEX IF NOT EXISTS idx_tm_teamname ON tournament_matches (teamname);",
            "CREATE INDEX IF NOT EXISTS idx_tm_date ON tournament_matches (date);",
            "CREATE INDEX IF NOT EXISTS idx_tm_patch ON tournament_matches (patch);",
            "CREATE INDEX IF NOT EXISTS idx_tm_result ON tournament_matches (result);",
            
            # Indexes cho tournament_players
            "CREATE INDEX IF NOT EXISTS idx_tp_gameid ON tournament_players (gameid);",
            "CREATE INDEX IF NOT EXISTS idx_tp_playername ON tournament_players (playername);",
            "CREATE INDEX IF NOT EXISTS idx_tp_champion ON tournament_players (champion);",
            "CREATE INDEX IF NOT EXISTS idx_tp_position ON tournament_players (position);",
            "CREATE INDEX IF NOT EXISTS idx_tp_champ_pos ON tournament_players (champion, position);",
            "CREATE INDEX IF NOT EXISTS idx_tp_teamname ON tournament_players (teamname);",
            "CREATE INDEX IF NOT EXISTS idx_tp_league ON tournament_players (league);",
        ]

        for idx_sql in indexes:
            cursor.execute(idx_sql)
        conn.commit()
        print(f"✅ Đã tạo thành công {len(indexes)} Indexes tối ưu hóa.")

    def run_validation(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        """
        Chạy bộ kiểm thử thẩm định tính toàn vẹn dữ liệu (Data Integrity Check & Sample Analytics).
        """
        cursor = conn.cursor()
        print("\n" + "=" * 80)
        print("🔍 BÁO CÁO THẨM ĐỊNH DỮ LIỆU CƠ SỞ DỮ LIỆU SQLITE (DATA INTEGRITY AUDIT)")
        print("=" * 80)

        results = {}

        # 1. Đếm số lượng dòng trong các bảng
        cursor.execute("SELECT COUNT(*) FROM tournament_matches;")
        results["total_match_records"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT gameid) FROM tournament_matches;")
        results["unique_matches"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tournament_players;")
        results["total_player_records"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT playername) FROM tournament_players WHERE playername IS NOT NULL;")
        results["unique_players"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT champion) FROM tournament_players WHERE champion IS NOT NULL;")
        results["unique_champions"] = cursor.fetchone()[0]

        print(f"📊 1. Quy mô Dữ liệu Đấu Giải:")
        print(f"   • Tổng số trận đấu độc lập (Unique Matches): {results['unique_matches']:,} trận")
        print(f"   • Bảng 'tournament_matches' (Cấp Team)   : {results['total_match_records']:,} dòng ({results['unique_matches'] * 2:,} dòng kỳ vọng)")
        print(f"   • Bảng 'tournament_players' (Cấp Tuyển thủ): {results['total_player_records']:,} dòng ({results['unique_matches'] * 10:,} dòng kỳ vọng)")
        print(f"   • Số tuyển thủ chuyên nghiệp xuất hiện    : {results['unique_players']:,} tuyển thủ")
        print(f"   • Số vị tướng đã được lựa chọn           : {results['unique_champions']:,} tướng")

        # 2. Phân bổ theo giải đấu (League Distribution)
        cursor.execute("""
            SELECT league, COUNT(DISTINCT gameid) as match_count, COUNT(*) as team_rows
            FROM tournament_matches
            GROUP BY league
            ORDER BY match_count DESC;
        """)
        league_rows = cursor.fetchall()
        print(f"\n🏆 2. Phân Bổ Theo Giải Đấu (League Distribution):")
        for league, m_cnt, t_cnt in league_rows:
            print(f"   • Giải {league:8s}: {m_cnt:5,d} trận ({t_cnt:5,d} dòng team)")

        # 3. Thống kê tỷ lệ có số liệu Timeline 10 phút
        cursor.execute("""
            SELECT 
                COUNT(*) as total_team_rows,
                COUNT(golddiffat10) as rows_with_timeline10,
                ROUND(COUNT(golddiffat10) * 100.0 / COUNT(*), 2) as timeline10_pct
            FROM tournament_matches;
        """)
        total_team, with_time10, pct_time10 = cursor.fetchone()
        print(f"\n⏱️ 3. Mức Độ Đầy Đủ Timeline Mốc 10 Phút:")
        print(f"   • Số dòng có chỉ số 10 phút: {with_time10:,} / {total_team:,} ({pct_time10}%)")

        # 4. Truy vấn thử nghiệm 1: Top 5 tướng có Pick Rate cao nhất
        print(f"\n🌟 4. Truy Vấn Phân Tích Thử Nghiệm: Top 5 Tướng Được Chọn Nhiều Nhất:")
        cursor.execute("""
            SELECT 
                champion, 
                position,
                COUNT(*) as pick_count,
                ROUND(AVG(result) * 100.0, 1) as winrate_pct,
                ROUND(AVG(kills), 1) as avg_kills,
                ROUND(AVG(deaths), 1) as avg_deaths,
                ROUND(AVG(assists), 1) as avg_assists
            FROM tournament_players
            WHERE champion IS NOT NULL
            GROUP BY champion, position
            ORDER BY pick_count DESC
            LIMIT 5;
        """)
        top_picks = cursor.fetchall()
        print(f"   {'Tướng':<15} {'Vị trí':<8} {'Số trận':<10} {'Tỉ lệ thắng':<14} {'KDA Trung bình':<15}")
        print(f"   {'-'*15} {'-'*8} {'-'*10} {'-'*14} {'-'*15}")
        for champ, pos, p_cnt, wr, k, d, a in top_picks:
            print(f"   {champ:<15} {pos:<8} {p_cnt:<10,d} {wr:>5.1f}%         {k:.1f}/{d:.1f}/{a:.1f}")

        # 5. Truy vấn thử nghiệm 2: Top 5 Đội tuyển có Tỷ lệ Thắng cao nhất (Tối thiểu 15 trận)
        print(f"\n🔥 5. Truy Vấn Phân Tích Thử Nghiệm: Top 5 Đội Tuyển Tỷ Lệ Thắng Cao Nhất (>= 15 trận):")
        cursor.execute("""
            SELECT 
                teamname, 
                league,
                COUNT(*) as games_played,
                SUM(result) as wins,
                ROUND(AVG(result) * 100.0, 1) as winrate_pct,
                ROUND(AVG(golddiffat10), 0) as avg_gold_diff_10
            FROM tournament_matches
            GROUP BY teamname, league
            HAVING games_played >= 15
            ORDER BY winrate_pct DESC, games_played DESC
            LIMIT 5;
        """)
        top_teams = cursor.fetchall()
        print(f"   {'Đội tuyển':<22} {'Giải đấu':<10} {'Số trận':<10} {'Thắng':<8} {'Tỉ lệ thắng':<14} {'Chênh vàng 10p':<15}")
        print(f"   {'-'*22} {'-'*10} {'-'*10} {'-'*8} {'-'*14} {'-'*15}")
        for team, lg, gp, wins, wr, gd10 in top_teams:
            gd_str = f"{gd10:+,.0f}" if gd10 is not None else "N/A"
            print(f"   {team:<22} {lg:<10} {gp:<10,d} {wins:<8,d} {wr:>5.1f}%         {gd_str:>10}")

        print("=" * 80 + "\n")
        return results

    def run(self, force: bool = False, verify_only: bool = False):
        """
        Thực thi toàn bộ quy trình ETL.
        """
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        conn = sqlite3.connect(self.db_path)

        try:
            if verify_only:
                self.run_validation(conn)
                return

            print(f"🚀 Bắt đầu nạp dữ liệu Đấu giải vào CSDL SQLite: {self.db_path}")
            matches_df, players_df = self.load_and_clean_data()
            self.create_schema(conn, matches_df, players_df, force=force)
            self.insert_dataframe(conn, "tournament_matches", matches_df)
            self.insert_dataframe(conn, "tournament_players", players_df)
            self.create_indexes(conn)
            self.run_validation(conn)
            print(f"🎉 Hoàn thành Task 1.2 xuất sắc! Toàn bộ dữ liệu đã được lưu vào: {self.db_path}")

        finally:
            conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="ETL Nạp Dữ Liệu Giải Đấu Chuyên Nghiệp Vào SQLite (tournament_matches & tournament_players)"
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Đường dẫn file CSV nguồn (mặc định lấy từ settings.get_active_esports_file())",
    )
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help=f"Đường dẫn file CSDL SQLite đích (mặc định: {OUTPUT_DB})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Xóa và tạo lại bảng từ đầu nếu bảng đã tồn tại",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Chỉ chạy kiểm định và hiển thị báo cáo dữ liệu hiện có trong CSDL",
    )

    args = parser.parse_args()
    loader = EsportsDatabaseLoader(source_csv=args.source, db_path=args.db)
    loader.run(force=args.force, verify_only=args.verify)


if __name__ == "__main__":
    main()
