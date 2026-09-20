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

import io
import time

# ── Cấu hình Google Drive API v3 (Tầng 2 chống Quota Exceeded) ───────────────
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, ".gdrive_token.json")
GDRIVE_API_SCOPES = ["https://www.googleapis.com/auth/drive"]


def _get_gdrive_service():
    """
    Xác thực OAuth2 và khởi tạo Google Drive API Service.
    - Lần đầu: Tự động mở trình duyệt để người dùng đăng nhập và ủy quyền.
    - Sau đó: Tự động dùng token cache trong .gdrive_token.json (không cần mở lại).
    """
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = None
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, GDRIVE_API_SCOPES)
            except Exception:
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None
            if not creds or not creds.valid:
                print("\n[*] Đang khởi tạo luồng ủy quyền Google OAuth 2.0 (Google Drive API)...")
                print("-> Trình duyệt web sẽ tự động mở để bạn đăng nhập tài khoản Google.")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, GDRIVE_API_SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
            print("[✓] Đã lưu phiên đăng nhập an toàn vào '.gdrive_token.json'!")

        return build("drive", "v3", credentials=creds)
    except Exception as e:
        print(f"[!] Lỗi khi kết nối Google Drive API: {e}")
        return None


def _download_via_api(file_id, dest_path, filename):
    """
    Tầng 2: Tải file qua Google Drive API v3 + OAuth2 chống Quota Exceeded.
    Quy trình 3 bước:
      1. Copy file về Google Drive cá nhân của người dùng (bản sao xóa bỏ 100% Quota Exceeded).
      2. Stream download nội dung từ bản copy về đĩa cục bộ (8MB/chunk).
      3. Tự động xóa bản copy khỏi Google Drive để không tốn dung lượng.
    """
    print(f"\n[🔑 TẦNG 2 - GOOGLE DRIVE API] Kích hoạt OAuth 2.0 để vượt Quota Exceeded...")
    service = _get_gdrive_service()
    if not service:
        print("[!] Không thể khởi tạo dịch vụ Google Drive API.")
        return False

    from googleapiclient.http import MediaIoBaseDownload
    copy_file_id = None
    try:
        # Bước 1: Tạo bản sao tạm trên My Drive
        print(f"    [1/3] Đang tạo bản sao tạm vào Google Drive của bạn...")
        copied = service.files().copy(
            fileId=file_id,
            body={"name": f"_tmp_lol_sync_{filename}"},
            supportsAllDrives=True
        ).execute()
        copy_file_id = copied.get("id")
        print(f"    [1/3] ✓ Đã tạo bản sao tạm (ID: {copy_file_id})")

        # Bước 2: Tải nội dung stream từ bản sao
        print(f"    [2/3] Đang stream tải dữ liệu về đĩa cục bộ...")
        request = service.files().get_media(fileId=copy_file_id, supportsAllDrives=True)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with io.FileIO(dest_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request, chunksize=8 * 1024 * 1024)
            done = False
            start_time = time.time()
            prev_pct = -1
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    pct = int(status.progress() * 100)
                    elapsed = max(0.1, time.time() - start_time)
                    mb_downloaded = status.resumable_progress / (1024 * 1024)
                    speed = mb_downloaded / elapsed
                    if pct != prev_pct and (pct % 5 == 0 or pct == 100):
                        print(f"    [2/3] [↓] Tiến trình: {pct}% ({mb_downloaded:.1f} MB) - {speed:.1f} MB/s", end="\r")
                        prev_pct = pct

        file_size = os.path.getsize(dest_path)
        print(f"    [2/3] ✓ Đã tải hoàn tất ({file_size / (1024 * 1024):.2f} MB)!                             ")
        return True

    except Exception as e:
        print(f"[!] Lỗi khi tải qua Drive API: {e}")
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except OSError:
                pass
        return False
    finally:
        # Bước 3: Luôn dọn dẹp bản sao tạm trên Drive
        if copy_file_id and service:
            try:
                service.files().delete(fileId=copy_file_id, supportsAllDrives=True).execute()
                print("    [3/3] ✓ Đã dọn dẹp bản sao tạm khỏi Google Drive.")
            except Exception:
                pass


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
            return [datetime.now().year]
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
        synced = self.sync_file(filename=latest_filename, force=force)
        dest_path = os.path.join(self.raw_dir, latest_filename)

        active_dataset = os.path.join(self.raw_dir, "esports_active_matches.csv")
        target_path = dest_path

        if not os.path.exists(dest_path):
            if os.path.exists(active_dataset):
                print(f"[✓] Chuyển sang sử dụng tệp dữ liệu hoạt động có sẵn: {os.path.basename(active_dataset)}")
                target_path = active_dataset
            else:
                print(f"\n[!] Không thể đồng bộ '{latest_filename}' và chưa có dữ liệu tại: {dest_path}")
                return []

        # Bước 2: Thẩm định quy mô dữ liệu thực tế
        match_count = self.count_matches(target_path, leagues=leagues_list)

        print(f"\n>>> [BƯỚC 2: THẨM ĐỊNH QUY MÔ DỮ LIỆU NĂM {latest_year}]")
        scope_str = f" ({', '.join(leagues_list)})" if leagues_list else ""
        print(f"    - Số trận đấu thực tế{scope_str}: {match_count:,} trận")
        print(f"    - Ngưỡng tối thiểu yêu cầu: {min_matches:,} trận")

        if match_count >= min_matches or target_path == active_dataset:
            print(f"\n[💡 KẾT LUẬN THUẬT TOÁN]:")
            print(f"    ✓ Năm {latest_year} ĐÃ ĐỦ DỮ LIỆU ({match_count:,} trận).")
            print(f"    ✓ Theo nguyên tắc Meta trò chơi: Giữ nguyên duy nhất mùa {latest_year},")
            print(f"      KHÔNG kéo thêm năm {previous_year} để tránh lệch phiên bản tướng/trang bị!")
            
            # Nếu có chỉ định bộ lọc giải đấu và đang đọc từ file gốc đầy đủ, xuất file active
            if leagues_list and target_path != active_dataset:
                self.filter_leagues(input_file=dest_path, leagues=leagues_list)

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

    def sync_file(self, filename=None, force=False):
        """
        Đồng bộ một file cụ thể từ Drive về thư mục data/raw/.
        Nếu không truyền filename, tự động phát hiện mùa giải mới nhất trên Drive.
        Chỉ tải nếu file chưa có hoặc khi có yêu cầu force=True.
        """
        if filename is None:
            available = self.get_available_years()
            latest_year = available[-1] if available else datetime.now().year
            filename = f"{latest_year}_LoL_esports_match_data_from_OraclesElixir.csv"

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
        # Tầng 1: Thử tải nhanh qua gdown
        print(f"\n[↓] Bắt đầu tải file '{filename}' từ Google Drive (File ID: {file_id})...")
        download_success = False
        is_quota_error = False

        if gdown:
            try:
                gdown.download(id=file_id, output=dest_path, quiet=True, resume=True)
                # Kiểm tra file tải về hợp lệ (> 100 KB và không phải trang HTML Quota exceeded)
                if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1024 * 100:
                    download_success = True
                else:
                    is_quota_error = True
                    if os.path.exists(dest_path):
                        try:
                            os.remove(dest_path)
                        except OSError:
                            pass
            except Exception as e:
                err_str = str(e)
                if "Too many users" in err_str or "Quota exceeded" in err_str or "quota" in err_str.lower():
                    is_quota_error = True
                else:
                    print(f"[!] Lỗi khi tải file qua gdown: {err_str}")
        else:
            is_quota_error = True

        # Tầng 2: Google Drive API v3 + OAuth2 (tự động kích hoạt khi Tầng 1 gặp Quota Exceeded)
        if not download_success and is_quota_error:
            print(f"[!] Tầng 1 (gdown) gặp Quota Exceeded: File công khai bị Google tạm khóa lượt tải ẩn danh.")
            if os.path.exists(CREDENTIALS_FILE):
                download_success = _download_via_api(file_id=file_id, dest_path=dest_path, filename=filename)
            else:
                print(f"[!] Không tìm thấy '{CREDENTIALS_FILE}' để kích hoạt Tầng 2 (Drive API).")

        if not download_success or not os.path.exists(dest_path):
            return False

        new_size = os.path.getsize(dest_path)
        now_iso = datetime.now().isoformat()
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

    def filter_leagues(self, input_file=None, output_file=None, leagues=None):
        """
        Lọc tập dữ liệu đấu giải chuyên nghiệp theo danh sách giải đấu mong muốn.
        
        Args:
            input_file (str, optional): Đường dẫn tệp CSV đầu vào. Mặc định là mùa giải mới nhất tại data/raw/.
            output_file (str, optional): Đường dẫn tệp CSV đầu ra. Mặc định là data/raw/esports_active_matches.csv.
            leagues (str | list, optional): Danh sách giải đấu (ví dụ: ['LCK', 'LCP', 'LPL'] hoặc 'LCK,LCP,LPL').
                                            Mặc định: ['LCK', 'LCP', 'LPL'].
        Returns:
            pandas.DataFrame | None: DataFrame đã được lọc, hoặc None nếu lỗi.
        """
        import pandas as pd

        # Xác định danh sách giải đấu (chuẩn hóa chữ hoa)
        target_leagues = parse_leagues(leagues) or parse_leagues(ESPORTS_TARGET_LEAGUES) or ["LCK", "LCP", "LPL"]
        
        # Xác định tệp đầu vào
        if not input_file:
            available = self.get_available_years()
            latest_year = available[-1] if available else datetime.now().year
            input_file = os.path.join(self.raw_dir, f"{latest_year}_LoL_esports_match_data_from_OraclesElixir.csv")
            if not os.path.exists(input_file):
                input_file = os.path.join(self.raw_dir, "esports_active_matches.csv")

        if not os.path.exists(input_file):
            print(f"[!] Lỗi: Không tìm thấy tệp dữ liệu đầu vào tại '{input_file}'!")
            return None

        # Xác định tệp đầu ra
        if not output_file:
            output_file = os.path.join(self.raw_dir, "esports_active_matches.csv")

        print("\n" + "=" * 70)
        print("           BỘ LỌC DỮ LIỆU GIẢI ĐẤU CHUYÊN NGHIỆP (LEAGUES FILTER)")
        print("=" * 70)
        print(f"[*] Tệp nguồn: {os.path.basename(input_file)} ({os.path.getsize(input_file) / (1024*1024):.2f} MB)")
        print(f"[*] Các giải đấu mục tiêu: {', '.join(target_leagues)}")
        print("[*] Đang đọc và trích xuất dữ liệu...")

        try:
            df = pd.read_csv(input_file, low_memory=False)
            total_rows_before = len(df)
            total_games_before = df["gameid"].dropna().nunique() if "gameid" in df.columns else 0

            # Lọc theo cột 'league'
            df["_league_upper"] = df["league"].astype(str).str.strip().str.upper()
            df_filtered = df[df["_league_upper"].isin(target_leagues)].copy()
            df_filtered.drop(columns=["_league_upper"], inplace=True)

            total_rows_after = len(df_filtered)
            total_games_after = df_filtered["gameid"].dropna().nunique() if "gameid" in df_filtered.columns else 0

            print(f"\n[+] Kết quả lọc dữ liệu:")
            print(f"    - Trước lọc: {total_rows_before:,} dòng ({total_games_before:,} trận)")
            print(f"    - Sau lọc:   {total_rows_after:,} dòng ({total_games_after:,} trận)")
            
            # Thống kê chi tiết từng giải
            print(f"\n[*] Chi tiết số lượng từng giải đấu sau khi lọc:")
            for lg in target_leagues:
                df_lg = df_filtered[df_filtered["league"].astype(str).str.strip().str.upper() == lg]
                lg_rows = len(df_lg)
                lg_games = df_lg["gameid"].dropna().nunique() if "gameid" in df_lg.columns else 0
                print(f"    • {lg:<8}: {lg_games:>5,} trận ({lg_rows:>6,} dòng)")

            # Lưu file kết quả
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            df_filtered.to_csv(output_file, index=False)
            print(f"\n[✓] Đã lưu tệp kết quả lọc thành công:")
            print(f"    -> Tệp lưu trữ: {output_file}")
            print(f"    -> Dung lượng:  {os.path.getsize(output_file) / (1024*1024):.2f} MB")
            print("=" * 70 + "\n")

            return df_filtered
        except Exception as e:
            print(f"[!] Lỗi khi lọc giải đấu: {e}")
            return None

    def check_data_health(self, filepath=None):
        """
        Kiểm tra độ sạch và tính toàn vẹn (Data Quality & Sanity Health Check) của tệp dữ liệu esports:
        - Quy mô số dòng, số trận (unique gameid).
        - Tính cân đối cấu trúc Oracle's Elixir (10 tuyển thủ + 2 đội = 12 dòng/trận).
        - Thống kê các giải đấu và dải thời gian thi đấu.
        - Tỷ lệ giá trị thiếu (Missing Values) ở các cột cốt lõi và cột mốc 10 phút.
        - Đưa ra kết luận thẩm định chất lượng dữ liệu.
        """
        import pandas as pd

        if not filepath:
            filepath = os.path.join(self.raw_dir, "esports_active_matches.csv")
            if not os.path.exists(filepath):
                available = self.get_available_years()
                latest_year = available[-1] if available else datetime.now().year
                filepath = os.path.join(self.raw_dir, f"{latest_year}_LoL_esports_match_data_from_OraclesElixir.csv")

        if not os.path.exists(filepath):
            print(f"[!] Lỗi: Không tìm thấy tệp dữ liệu để kiểm tra tại: '{filepath}'")
            return False

        print("\n" + "=" * 80)
        print("          BÁO CÁO THẨM ĐỊNH SỨC KHỎE DỮ LIỆU (DATA HEALTH CARD)")
        print("=" * 80)
        print(f"[*] Tệp kiểm tra: {os.path.basename(filepath)}")
        print(f"[*] Đường dẫn:    {filepath}")
        print(f"[*] Dung lượng:   {os.path.getsize(filepath) / (1024*1024):.2f} MB")
        print("[*] Đang đọc và phân tích cấu trúc dữ liệu...")

        try:
            df = pd.read_csv(filepath, low_memory=False)
            total_rows = len(df)
            total_cols = len(df.columns)

            if "gameid" not in df.columns:
                print("[❌ THẤT BẠI] File không có cột 'gameid' nhận diện trận đấu!")
                return False

            total_games = df["gameid"].dropna().nunique()

            # 1. Thống kê giải đấu
            leagues_summary = {}
            if "league" in df.columns:
                lg_counts = df.groupby(df["league"].astype(str).str.strip().str.upper())["gameid"].nunique()
                leagues_summary = lg_counts.to_dict()

            # 2. Dải thời gian
            date_range = "N/A"
            if "date" in df.columns:
                valid_dates = pd.to_datetime(df["date"], errors="coerce").dropna()
                if not valid_dates.empty:
                    date_range = f"{valid_dates.min().strftime('%Y-%m-%d')} đến {valid_dates.max().strftime('%Y-%m-%d')}"

            # 3. Kiểm tra cấu trúc Oracle's Elixir (12 dòng / trận)
            game_row_counts = df["gameid"].value_counts()
            perfect_12_games = int((game_row_counts == 12).sum())
            imperfect_games = int((game_row_counts != 12).sum())

            team_df = df[df["position"].astype(str).str.lower() == "team"]
            player_df = df[df["position"].astype(str).str.lower() != "team"]
            team_rows = len(team_df)
            player_rows = len(player_df)

            # 4. Kiểm tra missing values theo từng phân tầng dữ liệu
            core_cols = ["gameid", "league", "year", "date", "side", "position", "result", "gamelength"]
            minute10_cols = ["goldat10", "xpat10", "csat10", "golddiffat10", "xpdiffat10", "csdiffat10"]
            team_objective_cols = ["dragons", "heralds", "void_grubs", "barons", "towers"]

            print("\n" + "─" * 80)
            print("1. QUY MÔ & TÍNH TOÀN VẸN CƠ BẢN:")
            print(f"   • Tổng số dòng:              {total_rows:>10,}")
            print(f"   • Tổng số cột:               {total_cols:>10,}")
            print(f"   • Số trận đấu độc lập:       {total_games:>10,}")
            print(f"   • Khung thời gian thi đấu:   {date_range}")
            print(f"   • Dòng tuyển thủ (Player):   {player_rows:>10,} ({player_rows/total_rows*100:.1f}%)")
            print(f"   • Dòng đội tuyển (Team):     {team_rows:>10,} ({team_rows/total_rows*100:.1f}%)")

            print("\n2. CẤU TRÚC CHUẨN ORACLE'S ELIXIR (12 DÒNG / TRẬN):")
            pct_perfect = (perfect_12_games / total_games * 100) if total_games > 0 else 0
            print(f"   • Trận chuẩn đúng 12 dòng:   {perfect_12_games:>10,} ({pct_perfect:.2f}%)")
            if imperfect_games > 0:
                print(f"   • Trận lệch số dòng:         {imperfect_games:>10,} (Cần lọc bản ghi khuyết tại Module 02)")
            else:
                print(f"   • Trận lệch số dòng:                  0 (Hoàn hảo 100%)")

            print("\n3. PHÂN BỔ GIẢI ĐẤU (LEAGUES BREAKDOWN):")
            for lg, cnt in sorted(leagues_summary.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {lg:<10}: {cnt:>5,} trận ({cnt/total_games*100:>5.1f}%)")

            print("\n4. ĐỘ ĐẦY ĐỦ CỦA CÁC CỘT QUAN TRỌNG (MISSING VALUE AUDIT):")
            print(f"   {'Phân nhóm':<16} {'Tên cột':<18} {'Hiện diện':<12} {'Tỷ lệ Khuyết (%)':<20} {'Đánh giá'}")
            print("   " + "─" * 78)

            # Cốt lõi (trên toàn bộ DataFrame)
            for col in core_cols:
                if col in df.columns:
                    m_pct = df[col].isna().mean() * 100
                    st = "✓ SẠCH (0%)" if m_pct == 0 else f"! Khuyết {m_pct:.1f}%"
                    print(f"   {'[Toàn bộ]':<16} {col:<18} {'Có':<12} {m_pct:>8.2f}%            {st}")
                else:
                    print(f"   {'[Toàn bộ]':<16} {col:<18} {'KHÔNG CÓ':<12} {'100.00%':>8}            ⚠️ Thiếu cột")

            # Mục tiêu lớn (chỉ tính trên dòng Team vì Oracle's Elixir chỉ ghi nhận ở Team)
            for col in team_objective_cols:
                if col in df.columns:
                    m_pct = team_df[col].isna().mean() * 100
                    st = "✓ SẠCH (0%)" if m_pct == 0 else (f"! Khuyết {m_pct:.1f}%" if m_pct < 20 else f"⚠️ Thiếu {m_pct:.1f}%")
                    print(f"   {'[Mục tiêu Team]':<16} {col:<18} {'Có':<12} {m_pct:>8.2f}%            {st}")
                else:
                    print(f"   {'[Mục tiêu Team]':<16} {col:<18} {'KHÔNG CÓ':<12} {'100.00%':>8}            ⚠️ Thiếu cột")

            # Chỉ số mốc 10 phút (tính trên dòng Player & Team)
            for col in minute10_cols:
                if col in df.columns:
                    m_pct = df[col].isna().mean() * 100
                    valid_games = df[df[col].notna()]["gameid"].nunique()
                    st = f"✓ Có ở {valid_games:,} trận ({100-m_pct:.1f}%)"
                    print(f"   {'[Mốc 10 phút]':<16} {col:<18} {'Có':<12} {m_pct:>8.2f}%            {st}")
                else:
                    print(f"   {'[Mốc 10 phút]':<16} {col:<18} {'KHÔNG CÓ':<12} {'100.00%':>8}            ⚠️ Thiếu cột")

            print("\n" + "=" * 80)
            if pct_perfect >= 95.0 and team_df["dragons"].isna().mean() == 0:
                print("   [🎉 KẾT LUẬN: DỮ LIỆU ĐẠT CHUẨN XUẤT SẮC - SẴN SÀNG CHO TASK 1.2 (ETL SQLITE)]")
            else:
                print("   [ℹ️ KẾT LUẬN: DỮ LIỆU KHẢ DỤNG - CẦN MODULE 02 LỌC BỎ CÁC BẢN GHI KHUYẾT THIẾU]")
            print("=" * 80 + "\n")
            return True
        except Exception as e:
            print(f"[!] Lỗi khi thẩm định dữ liệu: {e}")
            return False


def filter_esports_by_leagues(input_file=None, output_file=None, leagues=None):
    """
    Hàm độc lập ở cấp độ module để dễ dàng import và gọi từ bất kỳ script nào.
    Ví dụ:
        from src.01_data_pipeline.sync_google_drive import filter_esports_by_leagues
        df = filter_esports_by_leagues(leagues=['LCK', 'LCP', 'LPL'])
    """
    syncer = GoogleDriveDataSyncer()
    return syncer.filter_leagues(input_file=input_file, output_file=output_file, leagues=leagues)


def check_esports_data_health(filepath=None):
    """
    Hàm độc lập ở cấp độ module kiểm tra sức khỏe và độ sạch của dữ liệu.
    Ví dụ:
        from src.01_data_pipeline.sync_google_drive import check_esports_data_health
        check_esports_data_health()
    """
    syncer = GoogleDriveDataSyncer()
    return syncer.check_data_health(filepath=filepath)


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
    parser.add_argument(
        "--filter",
        action="store_true",
        help="Thực hiện lọc dữ liệu giải đấu từ file cục bộ (LCK, LCP, LPL...) và xuất ra esports_active_matches.csv mà không tải lại",
    )
    parser.add_argument(
        "--filter-leagues",
        type=str,
        default=None,
        help="Chỉ định các giải đấu cần lọc (ví dụ: LCK,LCP,LPL hoặc VCS,LEC). Phân tách bằng dấu phẩy.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Kiểm tra độ sạch và tính toàn vẹn (Data Quality / Sanity Check) của tệp dữ liệu esports",
    )

    args = parser.parse_args()
    syncer = GoogleDriveDataSyncer()

    print("=" * 80)
    print("   HỆ THỐNG ĐỒNG BỘ DỮ LIỆU TỰ ĐỘNG TỪ GOOGLE DRIVE (CLOUD DATA AUTO-SYNC)")
    print(f"   Thư mục Drive: {GOOGLE_DRIVE_FOLDER_URL}")
    print("=" * 80)

    # Chế độ kiểm tra sức khỏe và độ sạch của dữ liệu
    if args.check:
        syncer.check_data_health(filepath=args.filename)
        return

    # Chế độ chỉ lọc giải đấu từ tệp dữ liệu đã tải sẵn trên máy
    if args.filter or args.filter_leagues:
        target_lgs = args.filter_leagues or args.leagues
        syncer.filter_leagues(input_file=args.filename, leagues=target_lgs)
        return

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
