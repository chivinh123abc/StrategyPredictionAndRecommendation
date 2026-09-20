"""
================================================================================
SCRIPT ĐỒNG BỘ DỮ LIỆU TỰ ĐỘNG TỪ GOOGLE DRIVE (CLOUD DATA AUTO-SYNC)
Dự án: Nhập môn Khoa học Dữ liệu - PTIT
Mô tả: Tự động kiểm tra và đồng bộ tập dữ liệu đấu giải chuyên nghiệp 
       (Oracle's Elixir từ 2014-2026) được chia sẻ trên Google Drive về data/raw/
================================================================================
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime

# Thêm thư mục gốc và src vào sys.path để nạp config chuẩn mực
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == "01_data_pipeline":
    BASE_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

try:
    from src.config import (
        DRIVE_SYNC_MANIFEST,
        ESPORTS_TARGET_LEAGUES,
        GOOGLE_DRIVE_FOLDER_ID,
        GOOGLE_DRIVE_FOLDER_URL,
        MIN_MATCHES_THRESHOLD,
        RAW_DATA_DIR,
    )
except (ImportError, ModuleNotFoundError):
    try:
        from config import (
            DRIVE_SYNC_MANIFEST,
            ESPORTS_TARGET_LEAGUES,
            GOOGLE_DRIVE_FOLDER_ID,
            GOOGLE_DRIVE_FOLDER_URL,
            MIN_MATCHES_THRESHOLD,
            RAW_DATA_DIR,
        )
    except (ImportError, ModuleNotFoundError):
        MIN_MATCHES_THRESHOLD = 3000
        ESPORTS_TARGET_LEAGUES = None
        RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
        DRIVE_SYNC_MANIFEST = os.path.join(RAW_DATA_DIR, ".drive_sync_manifest.json")
        GOOGLE_DRIVE_FOLDER_ID = "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH"
        GOOGLE_DRIVE_FOLDER_URL = f"https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}"

try:
    import gdown
except ImportError:
    gdown = None


def parse_leagues(leagues_input):
    """
    Chuẩn hóa danh sách giải đấu truyền vào (chuỗi hoặc danh sách).
    Ví dụ: 'LCK,LCP,LPL' -> ['LCK', 'LCP', 'LPL']
    """
    if not leagues_input:
        return None
    if isinstance(leagues_input, str):
        items = [l.strip().upper() for l in leagues_input.split(",") if l.strip()]
        return items if items else None
    if isinstance(leagues_input, (list, tuple, set)):
        items = [str(l).strip().upper() for l in leagues_input if str(l).strip()]
        return items if items else None
    return None


class GoogleDriveDataSyncer:
    """Quản lý đồng bộ dữ liệu đám mây từ thư mục Google Drive dùng chung."""

    def __init__(self, folder_id=None):
        self.folder_id = folder_id or GOOGLE_DRIVE_FOLDER_ID
        self.raw_dir = RAW_DATA_DIR
        self.manifest_file = DRIVE_SYNC_MANIFEST
        self._remote_files_cache = None
        os.makedirs(self.raw_dir, exist_ok=True)

    def load_manifest(self):
        """Đọc lịch sử đồng bộ cục bộ để tránh tải lại file trùng lặp."""
        if os.path.exists(self.manifest_file):
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"last_sync": None, "files": {}}

    def save_manifest(self, manifest):
        """Lưu lại trạng thái đồng bộ sau khi tải file thành công."""
        try:
            with open(self.manifest_file, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Cảnh báo không thể ghi file manifest: {e}")

    def list_folder_files(self, force_refresh=False):
        """
        Lấy danh sách siêu dữ liệu (Tên file, File ID) từ Google Drive
        mà không cần tải toàn bộ nội dung file (skip_download=True).
        Có cơ chế lưu cache trong phiên chạy để không phải quét nhiều lần.
        """
        if self._remote_files_cache is not None and not force_refresh:
            return self._remote_files_cache

        print(f"[*] Đang quét danh mục file từ Google Drive Folder (ID: {self.folder_id})...")
        if not gdown:
            print("[!] Cảnh báo: Chưa cài đặt thư viện 'gdown'. Hãy chạy: pip install gdown")
            return {}
        try:
            drive_files = gdown.download_folder(
                id=self.folder_id,
                skip_download=True,
                quiet=True,
            )
            file_map = {}
            for item in drive_files:
                file_map[item.path] = item.id
            print(f"[+] Tìm thấy {len(file_map)} file dữ liệu trên Google Drive.")
            self._remote_files_cache = file_map
            return file_map
        except Exception as e:
            print(f"[!] Lỗi khi quét thư mục Google Drive: {e}")
            return {}

    def get_available_years(self):
        """Lấy danh sách tất cả các năm có sẵn trên Google Drive, sắp xếp tăng dần."""
        remote_files = self.list_folder_files()
        available_years = []
        for filename in remote_files.keys():
            match = re.match(r"^(\d{4})_LoL_esports_match_data_from_OraclesElixir\.csv$", filename)
            if match:
                available_years.append(int(match.group(1)))

        if not available_years:
            return [2026]
        return sorted(available_years)

    def count_matches(self, filepath, leagues=None):
        """Đếm số lượng trận đấu (unique gameid) trong file CSV, có hỗ trợ lọc theo giải đấu (leagues)."""
        if not os.path.exists(filepath):
            return 0
        leagues_list = parse_leagues(leagues)
        try:
            import pandas as pd
            cols = ["gameid"] if not leagues_list else ["gameid", "league"]
            df = pd.read_csv(filepath, usecols=cols, low_memory=False)
            if leagues_list and "league" in df.columns:
                df = df[df["league"].astype(str).str.upper().isin(leagues_list)]
            return int(df["gameid"].dropna().nunique())
        except Exception:
            try:
                # Fallback nhanh nếu không có pandas: ước tính qua số dòng
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = sum(1 for _ in f)
                return max(0, (lines - 1) // 12)
            except Exception:
                return 0

    def sync_smart_latest(self, min_matches=MIN_MATCHES_THRESHOLD, leagues=None, force=False):
        """
        Quy tắc quyết định mùa giải thông minh (Data Science Domain Logic):
        1. Luôn xác định mùa giải MỚI NHẤT có trên Google Drive (ví dụ: 2026, hoặc sau này là 2027).
        2. Tải/kiểm tra file mùa giải mới nhất về data/raw/.
        3. Thẩm định quy mô dữ liệu (có hỗ trợ lọc theo giải đấu leagues, ví dụ LCK, LCP, LPL):
           - Nếu ĐÃ ĐỦ số lượng cần thiết (>= min_matches):
             -> CHỈ SỬ DỤNG DUY NHẤT NĂM NÀY. KHÔNG kéo thêm năm trước để bảo toàn tính đồng nhất
                của Meta trò chơi, tránh bị trôi dạt khái niệm (Concept Drift).
           - Nếu CHƯA ĐỦ số lượng (< min_matches):
             -> TỰ ĐỘNG KÍCH HOẠT LẤY TOÀN BỘ NĂM MỚI NHẤT + PHẦN CUỐI NĂM TRƯỚC cho đến khi đủ số lượng.
        """
        leagues_list = parse_leagues(leagues or ESPORTS_TARGET_LEAGUES)
        available_years = self.get_available_years()
        latest_year = available_years[-1]
        previous_year = available_years[-2] if len(available_years) >= 2 else None

        print(f"\n[*] Mùa giải mới nhất phát hiện trên hệ thống: NĂM {latest_year}")
        if leagues_list:
            print(f"[*] Bộ lọc giải đấu (Leagues Filter): {', '.join(leagues_list)}")
        else:
            print("[*] Phạm vi giải đấu: Toàn bộ tất cả giải đấu (không lọc)")

        latest_filename = f"{latest_year}_LoL_esports_match_data_from_OraclesElixir.csv"

        # Bước 1: Đồng bộ file năm mới nhất
        print(f">>> [BƯỚC 1: ĐỒNG BỘ MÙA GIẢI MỚI NHẤT {latest_year}]")
        self.sync_file(filename=latest_filename, force=force)

        # Bước 2: Thẩm định quy mô dữ liệu thực tế
        dest_path = os.path.join(self.raw_dir, latest_filename)
        match_count = self.count_matches(dest_path, leagues=leagues_list)

        print(f"\n>>> [BƯỚC 2: THẨM ĐỊNH QUY MÔ DỮ LIỆU NĂM {latest_year}]")
        scope_str = f" ({', '.join(leagues_list)})" if leagues_list else ""
        print(f"    - Số trận đấu thực tế{scope_str}: {match_count:,} trận")
        print(f"    - Ngưỡng tối thiểu yêu cầu: {min_matches:,} trận")

        if match_count >= min_matches:
            print(f"\n[💡 KẾT LUẬN THUẬT TOÁN]:")
            print(f"    ✓ Năm {latest_year} ĐÃ ĐỦ DỮ LIỆU ({match_count:,} >= {min_matches:,} trận).")
            print(f"    ✓ Theo nguyên tắc Meta trò chơi: Giữ nguyên duy nhất mùa {latest_year},")
            print(f"      KHÔNG kéo thêm năm {previous_year} để tránh lệch phiên bản tướng/trang bị!")
            
            # Nếu có chỉ định bộ lọc giải đấu, xuất file active chứa các giải đó
            if leagues_list:
                try:
                    import pandas as pd
                    output_file = os.path.join(self.raw_dir, "esports_active_matches.csv")
                    df_latest = pd.read_csv(dest_path, low_memory=False)
                    df_filtered = df_latest[df_latest["league"].astype(str).str.upper().isin(leagues_list)]
                    df_filtered.to_csv(output_file, index=False)
                    print(f"    -> Đã lọc và lưu {match_count:,} trận ({len(df_filtered):,} dòng) của giải [{', '.join(leagues_list)}] vào: {output_file}")
                except Exception as e:
                    print(f"[!] Cảnh báo không thể lọc giải: {e}")

            return [latest_year]
        else:
            print(f"\n[💡 KẾT LUẬN THUẬT TOÁN]:")
            print(f"    ! Năm {latest_year} đang ở giai đoạn đầu mùa, CHƯA ĐỦ DỮ LIỆU ({match_count:,} < {min_matches:,} trận).")
            if previous_year:
                print(f"    -> TỰ ĐỘNG KÍCH HOẠT: Lấy TOÀN BỘ năm mới nhất ({latest_year}) + phần CUỐI NĂM của năm trước ({previous_year}) cho đến khi đủ {min_matches:,} trận!")
                self.build_adaptive_dataset(latest_year, previous_year, min_matches=min_matches, leagues=leagues_list)
                return [previous_year, latest_year]
            return [latest_year]

    def build_adaptive_dataset(self, latest_year, previous_year, min_matches=MIN_MATCHES_THRESHOLD, leagues=None):
        """
        Quy tắc ghép dữ liệu thích ứng (Adaptive Tail Merging):
        - Khi năm mới nhất chưa đủ số trận yêu cầu (giai đoạn đầu mùa giải):
          1. Lấy TOÀN BỘ trận đấu của năm mới nhất (latest_year), có lọc theo leagues nếu chỉ định.
          2. Đếm số trận còn thiếu: needed = min_matches - current_matches.
          3. Sắp xếp các trận đấu của năm liền trước (previous_year) theo ngày thi đấu lùi dần từ cuối năm về trước (CKTG / Mùa Hè).
          4. Trích xuất đúng số lượng 'needed' trận từ PHẦN CUỐI NĂM của năm trước đó cho đến khi vừa đủ ngưỡng yêu cầu.
          5. Ghép lại và xuất ra tệp dữ liệu hoạt động: data/raw/esports_active_matches.csv
        """
        latest_file = os.path.join(self.raw_dir, f"{latest_year}_LoL_esports_match_data_from_OraclesElixir.csv")
        prev_file = os.path.join(self.raw_dir, f"{previous_year}_LoL_esports_match_data_from_OraclesElixir.csv")
        output_file = os.path.join(self.raw_dir, "esports_active_matches.csv")
        leagues_list = parse_leagues(leagues or ESPORTS_TARGET_LEAGUES)

        if not os.path.exists(latest_file):
            print(f"[!] Không tìm thấy tệp năm mới nhất: {latest_file}")
            return False

        if not os.path.exists(prev_file):
            print(f"[*] Đang tải tệp năm trước ({previous_year}) để trích xuất dữ liệu cuối năm...")
            ok = self.sync_file(f"{previous_year}_LoL_esports_match_data_from_OraclesElixir.csv")
            if not ok or not os.path.exists(prev_file):
                print(f"[!] Không thể nạp tệp năm {previous_year}. Tiếp tục giữ nguyên năm {latest_year}.")
                return False

        try:
            import pandas as pd
            print(f"\n[*] Đang nạp dữ liệu năm {latest_year} và năm {previous_year} để ghép thích ứng...")
            df_latest = pd.read_csv(latest_file, low_memory=False)
            if leagues_list and "league" in df_latest.columns:
                df_latest = df_latest[df_latest["league"].astype(str).str.upper().isin(leagues_list)]

            current_count = int(df_latest["gameid"].dropna().nunique())
            needed_matches = min_matches - current_count

            if needed_matches <= 0:
                print(f"[✓] Năm {latest_year} đã có {current_count:,} trận (>= {min_matches:,} trận), không cần ghép thêm.")
                if leagues_list:
                    df_latest.to_csv(output_file, index=False)
                    print(f"    - Đã lưu tập dữ liệu sau khi lọc giải ({', '.join(leagues_list)}) vào: {output_file}")
                return True

            league_msg = f" thuộc các giải [{', '.join(leagues_list)}]" if leagues_list else ""
            print(f"[*] Năm {latest_year} có {current_count:,} trận{league_msg}. Cần bổ sung thêm {needed_matches:,} trận từ cuối năm {previous_year}...")

            df_prev = pd.read_csv(prev_file, low_memory=False)
            if leagues_list and "league" in df_prev.columns:
                df_prev = df_prev[df_prev["league"].astype(str).str.upper().isin(leagues_list)]

            if df_prev.empty:
                print(f"[!] Không tìm thấy trận đấu nào của năm {previous_year}{league_msg}.")
                df_latest.to_csv(output_file, index=False)
                return True

            # Nhóm theo gameid để lấy ngày thi đấu muộn nhất của từng trận trong năm trước
            prev_game_dates = df_prev.groupby("gameid")["date"].max().sort_values(ascending=False)

            # Lấy đúng số lượng needed_matches từ cuối năm lùi về trước
            tail_game_ids = prev_game_dates.head(needed_matches).index.tolist()
            df_prev_tail = df_prev[df_prev["gameid"].isin(tail_game_ids)]

            date_start = df_prev_tail["date"].min()
            date_end = df_prev_tail["date"].max()
            print(f"[+] Đã trích xuất {len(tail_game_ids):,} trận đấu từ phần cuối năm {previous_year} (từ ngày {date_start} đến {date_end}).")

            # Hợp nhất: [Phần cuối năm trước] + [Toàn bộ năm mới nhất]
            df_combined = pd.concat([df_prev_tail, df_latest], ignore_index=True)
            if "date" in df_combined.columns:
                df_combined = df_combined.sort_values(by=["date", "gameid"], ascending=[True, True])

            total_games = int(df_combined["gameid"].nunique())
            df_combined.to_csv(output_file, index=False)

            print(f"\n[🎉 HOÀN TẤT GHÉP DỮ LIỆU THÍCH ỨNG (ADAPTIVE DATASET)]")
            print(f"    - Toàn bộ năm mới nhất ({latest_year}): {current_count:,} trận")
            print(f"    - Phần cuối năm trước ({previous_year}): {len(tail_game_ids):,} trận")
            print(f"    - Tổng quy mô tập dữ liệu hoạt động: {total_games:,} trận ({len(df_combined):,} dòng)")
            print(f"    - Đã lưu vào tệp hoạt động: {output_file}")
            return True
        except Exception as e:
            print(f"[!] Lỗi khi ghép dữ liệu thích ứng: {e}")
            return False

    def sync_file(self, filename="2026_LoL_esports_match_data_from_OraclesElixir.csv", force=False):
        """
        Đồng bộ một file cụ thể từ Drive về thư mục data/raw/.
        Chỉ tải nếu file chưa có hoặc khi có yêu cầu force=True.
        """
        dest_path = os.path.join(self.raw_dir, filename)
        manifest = self.load_manifest()
        
        # 1. Quét danh sách file từ Drive để lấy ID
        remote_files = self.list_folder_files()
        if filename not in remote_files:
            print(f"[!] Không tìm thấy file '{filename}' trong thư mục Google Drive!")
            return False

        file_id = remote_files[filename]
        file_info = manifest.get("files", {}).get(filename, {})

        # 2. Kiểm tra nếu file đã tồn tại cục bộ và không yêu cầu tải lại ép buộc
        if os.path.exists(dest_path) and not force:
            local_size = os.path.getsize(dest_path)
            last_synced = file_info.get("synced_at", "Không rõ")
            print(f"[✓] File '{filename}' đã có sẵn tại: {dest_path}")
            print(f"    - Dung lượng: {local_size / (1024 * 1024):.2f} MB")
            print(f"    - Đồng bộ lần cuối: {last_synced}")
            print("    -> Bỏ qua tải lại để tiết kiệm băng thông (Dùng --force nếu muốn tải lại bản mới nhất).")
            return True

        # 3. Thực hiện tải file mới về từ Drive
        print(f"\n[↓] Bắt đầu tải file '{filename}' từ Google Drive (File ID: {file_id})...")
        try:
            gdown.download(id=file_id, output=dest_path, quiet=False, resume=True)
            new_size = os.path.getsize(dest_path)
            now_iso = datetime.now().isoformat()
            
            # Cập nhật manifest
            if "files" not in manifest:
                manifest["files"] = {}
            manifest["files"][filename] = {
                "id": file_id,
                "size": new_size,
                "synced_at": now_iso,
            }
            manifest["last_sync"] = now_iso
            self.save_manifest(manifest)
            
            print(f"\n[🎉 THÀNH CÔNG] Đã đồng bộ '{filename}' về thư mục data/raw/ ({new_size / (1024 * 1024):.2f} MB)!")
            return True
        except Exception as e:
            err_str = str(e)
            print(f"[!] Lỗi khi tải file '{filename}' từ Google Drive: {err_str}")
            if "Too many users" in err_str or "Quota exceeded" in err_str or "quota" in err_str.lower():
                print("\n" + "=" * 70)
                print("[!] NGUYÊN NHÂN: Google Drive chạm giới hạn băng thông công khai (Quota Exceeded)!")
                print(f"    File: {filename} (ID: {file_id})")
                print("    File này được rất nhiều nhà phân tích toàn cầu tải về nên Google tạm khóa lượt tải ẩn danh.")
                print("\n[*] CÁCH KHẮC PHỤC NHANH (100% THÀNH CÔNG TRONG 30 GIÂY):")
                print(f"    1. Truy cập trực tiếp link: https://drive.google.com/file/d/{file_id}/view")
                print("    2. Đăng nhập tài khoản Google của bạn trên trình duyệt.")
                print("    3. Nhấp biểu tượng 3 chấm (...) hoặc chuột phải -> chọn 'Tạo bản sao' (Make a copy).")
                print(f"    4. Tải bản sao đó về và di chuyển vào thư mục: data/raw/{filename}")
                print("    5. Chạy lại script này để hệ thống ghi nhận và kiểm tra tính toàn vẹn!")
                print("=" * 70 + "\n")
            return False

    def sync_all(self, force=False):
        """Đồng bộ toàn bộ các file (2014-2026) từ Google Drive."""
        remote_files = self.list_folder_files()
        if not remote_files:
            return False

        print(f"[*] Bắt đầu đồng bộ toàn bộ {len(remote_files)} file từ Google Drive...")
        success_count = 0
        for name in sorted(remote_files.keys()):
            ok = self.sync_file(filename=name, force=force)
            if ok:
                success_count += 1
        print(f"\n[+] Hoàn tất đồng bộ toàn bộ: {success_count}/{len(remote_files)} files.")
        return success_count == len(remote_files)


def main():
    parser = argparse.ArgumentParser(
        description="Đồng bộ tự động dữ liệu giải đấu LoL Esports từ Google Drive về data/raw/."
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Tên file cụ thể cần đồng bộ (ví dụ: 2025_LoL_esports_match_data_from_OraclesElixir.csv)",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Năm dữ liệu cần tải (ví dụ: 2026, 2025, 2024...)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Đồng bộ toàn bộ tất cả các năm từ 2014 đến 2026",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Chỉ liệt kê danh sách file có trên Drive, không tải",
    )
    parser.add_argument(
        "--min-matches",
        type=int,
        default=MIN_MATCHES_THRESHOLD,
        help=f"Ngưỡng số trận tối thiểu của năm mới nhất để quyết định có kéo thêm năm trước không (mặc định: {MIN_MATCHES_THRESHOLD})",
    )
    parser.add_argument(
        "--leagues",
        type=str,
        default=None,
        help="Danh sách các giải đấu cần lấy (ví dụ: LCK,LCP,LPL hoặc VCS). Phân tách bằng dấu phẩy. Mặc định: None (lấy toàn bộ giải đấu).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bắt buộc tải lại bản mới nhất từ Drive dù file cục bộ đã tồn tại",
    )

    args = parser.parse_args()
    syncer = GoogleDriveDataSyncer()

    print("=" * 80)
    print("   HỆ THỐNG ĐỒNG BỘ DỮ LIỆU TỰ ĐỘNG TỪ GOOGLE DRIVE (CLOUD DATA AUTO-SYNC)")
    print(f"   Thư mục Drive: {GOOGLE_DRIVE_FOLDER_URL}")
    print("=" * 80)

    if args.list:
        files = syncer.list_folder_files()
        print("\nDanh sách file có sẵn trên Google Drive:")
        for idx, (name, fid) in enumerate(sorted(files.items())):
            print(f"  {idx+1:2d}. {name:<55} (ID: {fid})")
        return

    if args.all:
        syncer.sync_all(force=args.force)
        return

    # Nếu chỉ định rõ --filename hoặc --year
    if args.filename or args.year:
        target_name = args.filename
        if args.year:
            target_name = f"{args.year}_LoL_esports_match_data_from_OraclesElixir.csv"
        syncer.sync_file(filename=target_name, force=args.force)
        return

    # Chế độ mặc định: Tự động lấy năm mới nhất, hỗ trợ lọc theo giải đấu (LCK, LCP, LPL...) và thẩm định quy mô
    syncer.sync_smart_latest(min_matches=args.min_matches, leagues=args.leagues, force=args.force)


if __name__ == "__main__":
    main()
