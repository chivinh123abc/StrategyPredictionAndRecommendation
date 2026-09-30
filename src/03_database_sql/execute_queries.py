"""
================================================================================
MODULE 03: EXECUTE ADVANCED SQL ANALYTICAL QUERIES
Dự án: Hệ Thống Trợ Lý Phân Tích Cấm/Chọn (Ban/Pick AI) - LMHT
Môn học: Nhập môn Khoa học Dữ liệu (TS. Thái Tuyết Hải, PTIT)
Nhiệm vụ: Task 1.4 [Thành viên 1 + 2] - Thực thi 5 câu truy vấn SQL nâng cao
================================================================================
"""

import os
import sys
import sqlite3
import argparse
import pandas as pd
from typing import Dict, Any, Optional

# Nạp cấu hình trung tâm
try:
    from src.config.settings import (
        BASE_DIR,
        DATABASE_DIR,
        OUTPUT_DB,
        PROCESSED_DATA_DIR,
    )
except ImportError:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(CURRENT_DIR)
    BASE_DIR = os.path.dirname(SRC_DIR)
    sys.path.insert(0, BASE_DIR)
    from src.config.settings import (
        BASE_DIR,
        DATABASE_DIR,
        OUTPUT_DB,
        PROCESSED_DATA_DIR,
    )


SQL_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "queries.sql")


QUERY_DESCRIPTIONS = {
    1: {
        "title": "TRUY VẤN 1: PHÂN TÍCH KÈO ĐẤU ĐỐI ĐẦU 1V1 (LANE MATCHUP)",
        "skills": "Self-JOIN (tp1 JOIN tp2 qua gameid & position), GROUP BY, HAVING, WHERE",
        "desc": "Thống kê đối đầu trực tiếp giữa 2 tướng cùng lane để xác định tỉ lệ thắng và chênh lệch vàng lúc 10 phút.",
    },
    2: {
        "title": "TRUY VẤN 2: PHÂN TÍCH CẶP ĐÔI ĂN Ý ĐƯỜNG DƯỚI (BOT LANE SYNERGY DUO)",
        "skills": "Intra-team JOIN (p1 JOIN p2 cùng team), GROUP BY, HAVING count(*) >= 10",
        "desc": "Tìm các cặp đôi Xạ thủ + Hỗ trợ ăn ý nhất giải đấu để phục vụ gợi ý cấm/chọn (Chương 6).",
    },
    3: {
        "title": "TRUY VẤN 3: TƯỚNG CÓ TỶ LỆ CẤM/CHỌN CAO NHẤT (META PRESENCE RATE)",
        "skills": "Common Table Expressions (CTE / Subqueries), Unpivot UNION ALL, Aggregations",
        "desc": "Tính toán chỉ số Presence Rate = (Picks + Bans) / Tổng số trận của các vị tướng thống trị Meta.",
    },
    4: {
        "title": "TRUY VẤN 4: XẾP HẠNG TUYỂN THỦ LẤN ĐƯỜNG PHÚT 10 (LANE DOMINANCE RANKING)",
        "skills": "Window Functions (DENSE_RANK(), PARTITION BY position, AVG() OVER())",
        "desc": "Xếp hạng khả năng đè đường phút 10 của các tuyển thủ và đối chiếu với mức chuẩn trung bình (Benchmark).",
    },
    5: {
        "title": "TRUY VẤN 5: ĐỐI CHIẾU HIỆU QUẢ LĂN CẦU TUYẾT: ĐẤU GIẢI VS RANK ĐƠN",
        "skills": "UNION ALL, CASE WHEN (Rời rạc hóa phân tầng vàng), Multi-table Aggregation",
        "desc": "So sánh khả năng chuyển hóa lợi thế vàng lúc 10 phút thành chiến thắng giữa Đấu Giải và Rank Đơn.",
    },
}


def extract_queries_from_sql_file(filepath: str) -> Dict[int, str]:
    """Trích xuất 5 câu truy vấn từ file queries.sql dựa vào tag đánh dấu."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Không tìm thấy file SQL tại: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    queries = {}
    for q_id in range(1, 6):
        start_tag = f"-- !QUERY_{q_id}_START"
        end_tag = f"-- !QUERY_{q_id}_END"
        if start_tag in content and end_tag in content:
            q_sql = content.split(start_tag)[1].split(end_tag)[0].strip()
            queries[q_id] = q_sql
    return queries


class SQLQueryRunner:
    """Class điều phối thực thi các truy vấn SQL phân tích nâng cao trên SQLite."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or OUTPUT_DB
        self.queries = extract_queries_from_sql_file(SQL_FILE_PATH)

    def run_query(self, query_id: int, limit: Optional[int] = None) -> pd.DataFrame:
        """Thực thi một câu truy vấn theo ID và trả về Pandas DataFrame."""
        if query_id not in self.queries:
            raise ValueError(f"Query ID không hợp lệ: {query_id}. Chỉ hỗ trợ 1 đến 5.")

        sql = self.queries[query_id]
        if limit is not None and "LIMIT" not in sql.upper():
            sql = f"{sql.rstrip(';')} LIMIT {limit};"

        conn = sqlite3.connect(self.db_path)
        try:
            df = pd.read_sql(sql, conn)
            return df
        finally:
            conn.close()

    def display_query(self, query_id: int, limit: Optional[int] = 10, export: bool = False):
        """In kết quả truy vấn ra terminal dưới dạng bảng đẹp mắt."""
        info = QUERY_DESCRIPTIONS.get(query_id, {})
        print("\n" + "=" * 90)
        print(f"📌 {info.get('title', f'TRUY VẤN SỐ {query_id}')}")
        print(f"   • Kỹ thuật SQL áp dụng : {info.get('skills', '')}")
        print(f"   • Ý nghĩa nghiệp vụ    : {info.get('desc', '')}")
        print("-" * 90)

        df = self.run_query(query_id)
        display_df = df.head(limit) if limit else df

        # In DataFrame định dạng đẹp
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)
        pd.set_option("display.unicode.ambiguous_as_wide", True)
        pd.set_option("display.unicode.east_asian_width", True)
        print(display_df.to_string(index=False))

        print(f"\n   (Hiển thị {len(display_df):,} / {len(df):,} kết quả tổng cộng)")

        if export:
            export_path = os.path.join(PROCESSED_DATA_DIR, f"sql_query_{query_id}_result.csv")
            df.to_csv(export_path, index=False, encoding="utf-8-sig")
            print(f"   💾 Đã xuất toàn bộ kết quả ra: {export_path}")

        print("=" * 90)

    def run_all(self, limit: Optional[int] = 5, export: bool = False):
        """Thực thi và in toàn bộ 5 câu truy vấn SQL."""
        print("\n" + "#" * 90)
        print("🏆 BÁO CÁO THỰC THI 5 CÂU TRUY VẤN SQL NÂNG CAO - CHƯƠNG 5 & 5x (PTIT DATA SCIENCE)")
        print(f"   • Database File: {self.db_path}")
        print("#" * 90)

        for q_id in range(1, 6):
            self.display_query(q_id, limit=limit, export=export)

        print("\n🎉 Đã hoàn tất thực thi 100% 5 câu truy vấn SQL nâng cao xuất sắc!\n")


def main():
    parser = argparse.ArgumentParser(
        description="Thực thi 5 câu truy vấn SQL phân tích nâng cao (Chương 5 & 5x PTIT)"
    )
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help=f"Đường dẫn CSDL SQLite (mặc định: {OUTPUT_DB})",
    )
    parser.add_argument(
        "--query",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=None,
        help="Chạy riêng một câu truy vấn cụ thể (từ 1 đến 5)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Số dòng tối đa hiển thị trên console (mặc định: 10)",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Xuất kết quả truy vấn ra file CSV trong data/processed/",
    )

    args = parser.parse_args()
    runner = SQLQueryRunner(db_path=args.db)

    if args.query is not None:
        runner.display_query(args.query, limit=args.limit, export=args.export)
    else:
        runner.run_all(limit=args.limit, export=args.export)


if __name__ == "__main__":
    main()
