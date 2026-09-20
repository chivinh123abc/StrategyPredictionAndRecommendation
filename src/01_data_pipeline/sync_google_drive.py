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
        GOOGLE_DRIVE_FOLDER_ID,
        GOOGLE_DRIVE_FOLDER_URL,
        RAW_DATA_DIR,
    )
except (ImportError, ModuleNotFoundError):
    from config import (
        DRIVE_SYNC_MANIFEST,
        GOOGLE_DRIVE_FOLDER_ID,
        GOOGLE_DRIVE_FOLDER_URL,
        RAW_DATA_DIR,
    )

import gdown


class GoogleDriveDataSyncer:
    """Quản lý đồng bộ dữ liệu đám mây từ thư mục Google Drive dùng chung."""

    def __init__(self, folder_id=None):
        self.folder_id = folder_id or GOOGLE_DRIVE_FOLDER_ID
        self.raw_dir = RAW_DATA_DIR
        self.manifest_file = DRIVE_SYNC_MANIFEST
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

    def list_folder_files(self):
        """
        Lấy danh sách siêu dữ liệu (Tên file, File ID) từ Google Drive
        mà không cần tải toàn bộ nội dung file (skip_download=True).
        """
        print(f"[*] Đang quét danh mục file từ Google Drive Folder (ID: {self.folder_id})...")
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
            return file_map
        except Exception as e:
            print(f"[!] Lỗi khi quét thư mục Google Drive: {e}")
            return {}

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
            print(f"[!] Lỗi khi tải file từ Google Drive: {e}")
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
        default="2026_LoL_esports_match_data_from_OraclesElixir.csv",
        help="Tên file cần đồng bộ (mặc định: 2026_LoL_esports_match_data_from_OraclesElixir.csv)",
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

    target_name = args.filename
    if args.year:
        target_name = f"{args.year}_LoL_esports_match_data_from_OraclesElixir.csv"

    syncer.sync_file(filename=target_name, force=args.force)


if __name__ == "__main__":
    main()
