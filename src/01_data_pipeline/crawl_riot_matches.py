"""
================================================================================
MODULE 01: RIOT GAMES API DATA PIPELINE
Dự án: Nhập môn Khoa học Dữ liệu - PTIT
Mô tả: Thu thập dữ liệu trận đấu Rank Cao (Thách Đấu / Cao Thủ) mốc 10 phút
       từ Riot Games API, chuẩn hóa 1NF/3NF và lưu trữ vào SQLite & CSV.
Hỗ trợ máy chủ: Việt Nam (VN2), Hàn Quốc (KR), Đài Loan (TW2),...
================================================================================
"""

import os
import sys
import time
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

import requests
import pandas as pd


# ==============================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN & BIẾN MÔI TRƯỜNG (PATH & CONFIG)
# ==============================================================================

# Xác định thư mục gốc dự án chuẩn xác bằng pathlib (không phụ thuộc vị trí gọi lệnh)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_dotenv_custom(env_path: Path) -> None:
    """Nạp cấu hình từ file .env bằng thư viện chuẩn Python, không cần package ngoài."""
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

# Nạp file .env từ thư mục gốc
load_dotenv_custom(BASE_DIR / ".env")

# Đọc cấu hình bảo mật từ biến môi trường
RIOT_API_KEY = os.getenv("RIOT_API_KEY", "").strip()
if not RIOT_API_KEY or "xxx" in RIOT_API_KEY:
    raise ValueError(
        "❌ LỖI BẢO MẬT: Chưa cấu hình RIOT_API_KEY hợp lệ trong file .env!\n"
        "Hãy mở file .env và dán key của bạn vào: RIOT_API_KEY=\"RGAPI-...\""
    )

# Cấu hình danh sách máy chủ và số trận mục tiêu
RAW_SERVERS = os.getenv("ACTIVE_SERVERS", "vn2,kr")
ACTIVE_SERVERS: List[str] = [s.strip().lower() for s in RAW_SERVERS.split(",") if s.strip()]
TARGET_MATCHES_PER_SERVER: int = int(os.getenv("TARGET_MATCHES_PER_SERVER", "50"))

# Đường dẫn lưu trữ dữ liệu đầu ra
DATA_DIR = BASE_DIR / "data"
OUTPUT_CSV = DATA_DIR / "processed" / "lol_live_ranked_10min.csv"
OUTPUT_DB = DATA_DIR / "database" / "lol_live_data.db"

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_DB.parent.mkdir(parents=True, exist_ok=True)

# Bảng ánh xạ máy chủ và định tuyến khu vực địa lý của Riot Games
SERVER_METADATA: Dict[str, Dict[str, str]] = {
    "vn2": {"platform": "vn2", "region": "sea", "country": "Vietnam", "label": "Việt Nam (VN2)"},
    "kr":  {"platform": "kr",  "region": "asia", "country": "Korea", "label": "Hàn Quốc (KR - Đấu trường Hàn & Trung)"},
    "tw2": {"platform": "tw2", "region": "sea", "country": "Taiwan", "label": "Đài Loan (TW2)"},
    "na1": {"platform": "na1", "region": "americas", "country": "North America", "label": "Bắc Mỹ (NA1)"},
    "euw1":{"platform": "euw1", "region": "europe", "country": "Europe", "label": "Tây Âu (EUW1)"}
}


# ==============================================================================
# 2. CLASS ĐIỀU PHỐI CÀO DỮ LIỆU (CRAWLER CONTROLLER)
# ==============================================================================

class RiotApiCrawler:
    """
    Class điều phối toàn bộ chu trình cào dữ liệu:
    - Quản lý phiên gọi API và Rate Limiting (Exponential Backoff).
    - Phân tích và trích xuất chỉ số mốc phút thứ 10 từ Timeline.
    - Lưu trữ đồng thời vào SQLite (chuẩn 1NF/3NF) và file CSV.
    """

    def __init__(self, api_key: str, platform: str = "vn2") -> None:
        self.api_key = api_key.strip()
        self.platform = platform.lower()
        meta = SERVER_METADATA.get(self.platform, {"region": "sea", "country": "Unknown", "label": self.platform})
        self.region = meta["region"]
        self.country = meta["country"]
        self.label = meta["label"]

        # Khởi tạo HTTP session có sẵn header chứng thực
        self.session = requests.Session()
        self.session.headers.update({"X-Riot-Token": self.api_key})

        # Tải danh mục tướng từ Riot CDN để giải mã mã tướng Cấm (Bans)
        self.champ_id_map: Dict[int, str] = self.load_champion_id_map()

        # Khởi tạo hoặc cập nhật bảng CSDL SQLite
        self.init_db()

    def get_db_connection(self) -> sqlite3.Connection:
        """Tạo kết nối an toàn đến SQLite database."""
        return sqlite3.connect(str(OUTPUT_DB))

    def load_champion_id_map(self) -> Dict[int, str]:
        """Tải bảng ánh xạ {championId: championName} từ Riot Data Dragon CDN."""
        try:
            v_res = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", timeout=5).json()
            latest_v = v_res[0]
            res = requests.get(
                f"https://ddragon.leagueoflegends.com/cdn/{latest_v}/data/en_US/champion.json", 
                timeout=10
            )
            data = res.json()["data"]
            id_map = {int(v["key"]): v["name"] for v in data.values()}
            print(f"[+] Đã tải danh mục {len(id_map)} vị tướng từ Riot CDN (Phiên bản {latest_v}).")
            return id_map
        except Exception as e:
            print(f"[!] Không thể tải bảng ánh xạ tướng từ CDN: {e}")
            return {}

    def parse_team_positions(self, participants: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Phân tích 5 vị trí thi đấu nguyên tử chuẩn 1NF:
        TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY (Support).
        """
        roles = {
            "TOP": "Unknown", 
            "JUNGLE": "Unknown", 
            "MIDDLE": "Unknown", 
            "BOTTOM": "Unknown", 
            "UTILITY": "Unknown"
        }
        unassigned: List[str] = []
        for p in participants:
            pos = p.get("teamPosition", "")
            c = p.get("championName", "Unknown")
            if pos in roles and roles[pos] == "Unknown":
                roles[pos] = c
            else:
                unassigned.append(c)

        for k in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:
            if roles[k] == "Unknown" and unassigned:
                roles[k] = unassigned.pop(0)

        return roles

    def init_db(self) -> None:
        """Khởi tạo bảng matches_10min trong SQLite với 42 cột chuẩn 1NF và 3NF."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches_10min (
                    gameId TEXT PRIMARY KEY,
                    server TEXT NOT NULL,
                    gameVersion TEXT NOT NULL,
                    gameDuration INTEGER NOT NULL,
                    blueWins INTEGER NOT NULL,
                    blueBans TEXT,
                    redBans TEXT,
                    blueTop TEXT,
                    blueJungle TEXT,
                    blueMid TEXT,
                    blueAdc TEXT,
                    blueSupport TEXT,
                    redTop TEXT,
                    redJungle TEXT,
                    redMid TEXT,
                    redAdc TEXT,
                    redSupport TEXT,
                    blueTotalGold INTEGER NOT NULL,
                    blueTotalExperience INTEGER NOT NULL,
                    blueTotalMinionsKilled INTEGER NOT NULL,
                    blueTotalJungleMinionsKilled INTEGER NOT NULL,
                    blueKills INTEGER NOT NULL,
                    blueDeaths INTEGER NOT NULL,
                    blueDragons INTEGER NOT NULL,
                    blueHeralds INTEGER NOT NULL,
                    blueVoidgrubs INTEGER NOT NULL,
                    blueTowersDestroyed INTEGER NOT NULL,
                    blueGoldDiff INTEGER NOT NULL,
                    blueExperienceDiff INTEGER NOT NULL,
                    redTotalGold INTEGER NOT NULL,
                    redTotalExperience INTEGER NOT NULL,
                    redTotalMinionsKilled INTEGER NOT NULL,
                    redTotalJungleMinionsKilled INTEGER NOT NULL,
                    redKills INTEGER NOT NULL,
                    redDeaths INTEGER NOT NULL,
                    redDragons INTEGER NOT NULL,
                    redHeralds INTEGER NOT NULL,
                    redVoidgrubs INTEGER NOT NULL,
                    redTowersDestroyed INTEGER NOT NULL,
                    redGoldDiff INTEGER NOT NULL,
                    redExperienceDiff INTEGER NOT NULL,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Đảm bảo tương thích: tự động gỡ cột cũ (nếu có) để duy trì chuẩn 1NF & 3NF
            cursor.execute("PRAGMA table_info(matches_10min)")
            existing_cols = [c[1] for c in cursor.fetchall()]
            for legacy_col in ["blueChampions", "redChampions", "country"]:
                if legacy_col in existing_cols:
                    cursor.execute(f"ALTER TABLE matches_10min DROP COLUMN {legacy_col}")

            conn.commit()

    def get_with_retry(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Thực hiện HTTP GET kèm giải thuật Exponential Backoff:
        Tự động chờ khi chạm giới hạn Rate Limit (HTTP 429) của Riot API.
        """
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                res = self.session.get(url, timeout=15)
                if res.status_code == 200:
                    return res.json()
                elif res.status_code == 429:
                    retry_after = int(res.headers.get("Retry-After", 10))
                    print(f"   [!] Rate Limit Riot API (429). Tự động tạm dừng {retry_after + 1}s...")
                    time.sleep(retry_after + 1)
                    retry_count += 1
                elif res.status_code == 403:
                    print("\n[LỖI 403 - FORBIDDEN]: Riot API Key đã hết hạn (24h) hoặc không hợp lệ!")
                    print("-> Vui lòng vào https://developer.riotgames.com bấm 'Regenerate API Key' và dán lại vào .env.")
                    sys.exit(1)
                elif res.status_code == 404:
                    return None
                else:
                    print(f"   [!] Mã lỗi HTTP {res.status_code} từ Riot API: {url}")
                    time.sleep(2)
                    return None
            except requests.exceptions.RequestException as e:
                print(f"   [!] Lỗi kết nối mạng: {e}. Thử lại sau 3s...")
                time.sleep(3)
                retry_count += 1

        return None

    def get_high_elo_puuids(self, limit: int = 50) -> List[str]:
        """Lấy danh sách PUUID người chơi bậc Thách Đấu của máy chủ."""
        print(f"\n[1/3] Đang lấy danh sách người chơi Thách Đấu máy chủ '{self.platform.upper()}'...")
        url = f"https://{self.platform}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
        data = self.get_with_retry(url)

        puuids: List[str] = []
        if data and "entries" in data:
            entries = data["entries"]
            print(f"-> Tìm thấy {len(entries)} người chơi trong bảng Thách Đấu.")

            for entry in entries[:limit]:
                puuid = entry.get("puuid")
                if not puuid:
                    s_id = entry.get("summonerId")
                    s_url = f"https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/{s_id}"
                    s_data = self.get_with_retry(s_url)
                    if s_data and "puuid" in s_data:
                        puuid = s_data["puuid"]
                    time.sleep(1.2)

                if puuid:
                    puuids.append(puuid)
                if len(puuids) >= limit:
                    break

        print(f"-> Đã thu thập được {len(puuids)} PUUID người chơi để dò tìm trận đấu.")
        return puuids

    def get_match_ids(self, puuids: List[str], target_count: int = 50) -> List[str]:
        """Lấy danh sách mã trận đấu xếp hạng đơn đôi (Queue 420)."""
        print(f"\n[2/3] Đang dò tìm {target_count} mã trận đấu Xếp Hạng mới nhất...")
        match_ids = set()

        # Kiểm tra các trận đã có sẵn trong CSDL để không cào trùng
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT gameId FROM matches_10min WHERE server = ?", (self.platform.upper(),))
            existing_ids = set(row[0] for row in cursor.fetchall())

        print(f"-> Trong CSDL hiện đã có sẵn {len(existing_ids)} trận máy chủ {self.platform.upper()}.")

        for idx, puuid in enumerate(puuids):
            if len(match_ids) >= target_count:
                break

            url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=20"
            ids = self.get_with_retry(url)
            if ids:
                for m_id in ids:
                    if m_id not in existing_ids and m_id not in match_ids:
                        match_ids.add(m_id)
                        if len(match_ids) >= target_count:
                            break

            print(f"   - Đã quét người chơi {idx+1}/{len(puuids)}: Gom được {len(match_ids)}/{target_count} mã trận mới.", end="\r")
            time.sleep(1.2)

        print(f"\n-> Hoàn tất gom {len(match_ids)} mã trận đấu mới đủ điều kiện.")
        return list(match_ids)

    def extract_10min_features(self, match_id: str) -> Optional[Dict[str, Any]]:
        """
        Trích xuất dữ liệu mốc phút thứ 10 từ Match Detail và Match Timeline.
        Lọc bỏ trận Remake (thời lượng < 900 giây).
        """
        # 1. Gọi Match Detail
        detail_url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        detail = self.get_with_retry(detail_url)
        time.sleep(1.2)
        if not detail or "info" not in detail:
            return None

        info = detail["info"]
        duration = info.get("gameDuration", 0)

        # Lọc bỏ trận Remake hoặc kết thúc trước phút 10 (Chương 2)
        if duration < 600:
            return None

        game_version = info.get("gameVersion", "Unknown")
        blue_win = 1 if info["teams"][0]["win"] else 0

        # 2. Gọi Match Timeline để lấy snapshot phút thứ 10
        timeline_url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        timeline = self.get_with_retry(timeline_url)
        time.sleep(1.2)
        if not timeline or "info" not in timeline:
            return None

        frames = timeline["info"].get("frames", [])
        if len(frames) < 11:
            return None  # Không đủ 10 phút dữ liệu

        frame_10 = frames[10]
        p_frames = frame_10.get("participantFrames", {})

        # Tách 2 đội: Người chơi 1-5 là Blue Team, 6-10 là Red Team
        blue_gold = sum(p_frames[str(i)]["totalGold"] for i in range(1, 6) if str(i) in p_frames)
        blue_xp = sum(p_frames[str(i)]["xp"] for i in range(1, 6) if str(i) in p_frames)
        blue_cs = sum(p_frames[str(i)]["minionsKilled"] for i in range(1, 6) if str(i) in p_frames)
        blue_jungle = sum(p_frames[str(i)]["jungleMinionsKilled"] for i in range(1, 6) if str(i) in p_frames)

        red_gold = sum(p_frames[str(i)]["totalGold"] for i in range(6, 11) if str(i) in p_frames)
        red_xp = sum(p_frames[str(i)]["xp"] for i in range(6, 11) if str(i) in p_frames)
        red_cs = sum(p_frames[str(i)]["minionsKilled"] for i in range(6, 11) if str(i) in p_frames)
        red_jungle = sum(p_frames[str(i)]["jungleMinionsKilled"] for i in range(6, 11) if str(i) in p_frames)

        # Đếm các sự kiện xảy ra TRƯỚC phút thứ 10
        blue_kills, red_kills = 0, 0
        blue_dragons, red_dragons = 0, 0
        blue_heralds, red_heralds = 0, 0
        blue_grubs, red_grubs = 0, 0
        blue_towers, red_towers = 0, 0

        for f in frames[:11]:
            for event in f.get("events", []):
                e_type = event.get("type")
                if e_type == "CHAMPION_KILL":
                    killer = event.get("killerId", 0)
                    if 1 <= killer <= 5:
                        blue_kills += 1
                    elif 6 <= killer <= 10:
                        red_kills += 1
                elif e_type == "ELITE_MONSTER_KILL":
                    killer = event.get("killerId", 0)
                    m_type = event.get("monsterType", "")
                    sub_type = event.get("monsterSubType", "")
                    is_blue = (1 <= killer <= 5)
                    if m_type == "DRAGON":
                        if is_blue: blue_dragons += 1
                        else: red_dragons += 1
                    elif m_type == "RIFTHERALD":
                        if is_blue: blue_heralds += 1
                        else: red_heralds += 1
                    elif m_type == "HORDE" or "GRUBS" in sub_type:
                        if is_blue: blue_grubs += 1
                        else: red_grubs += 1
                elif e_type == "BUILDING_KILL" and event.get("buildingType") == "TOWER_BUILDING":
                    team_id = event.get("teamId", 0)
                    if team_id == 200:
                        blue_towers += 1
                    elif team_id == 100:
                        red_towers += 1

        # Trích xuất danh sách Cấm (Bans) của 2 đội
        teams = info.get("teams", [])
        blue_bans, red_bans = [], []
        if len(teams) > 0:
            for b in teams[0].get("bans", []):
                cid = b.get("championId", -1)
                if cid != -1 and cid in self.champ_id_map:
                    blue_bans.append(self.champ_id_map[cid])
        if len(teams) > 1:
            for b in teams[1].get("bans", []):
                cid = b.get("championId", -1)
                if cid != -1 and cid in self.champ_id_map:
                    red_bans.append(self.champ_id_map[cid])

        # Trích xuất 10 tướng theo 5 vị trí thi đấu nguyên tử (Chuẩn 1NF)
        blue_roles = self.parse_team_positions(info.get("participants", [])[:5])
        red_roles = self.parse_team_positions(info.get("participants", [])[5:10])

        record: Dict[str, Any] = {
            "gameId": match_id,
            "server": self.platform.upper(),
            "gameVersion": game_version,
            "gameDuration": duration,
            "blueWins": blue_win,
            "blueBans": ", ".join(blue_bans) if blue_bans else "None",
            "redBans": ", ".join(red_bans) if red_bans else "None",
            "blueTop": blue_roles["TOP"],
            "blueJungle": blue_roles["JUNGLE"],
            "blueMid": blue_roles["MIDDLE"],
            "blueAdc": blue_roles["BOTTOM"],
            "blueSupport": blue_roles["UTILITY"],
            "redTop": red_roles["TOP"],
            "redJungle": red_roles["JUNGLE"],
            "redMid": red_roles["MIDDLE"],
            "redAdc": red_roles["BOTTOM"],
            "redSupport": red_roles["UTILITY"],
            "blueTotalGold": blue_gold,
            "blueTotalExperience": blue_xp,
            "blueTotalMinionsKilled": blue_cs,
            "blueTotalJungleMinionsKilled": blue_jungle,
            "blueKills": blue_kills,
            "blueDeaths": red_kills,
            "blueDragons": blue_dragons,
            "blueHeralds": blue_heralds,
            "blueVoidgrubs": blue_grubs,
            "blueTowersDestroyed": blue_towers,
            "blueGoldDiff": blue_gold - red_gold,
            "blueExperienceDiff": blue_xp - red_xp,
            "redTotalGold": red_gold,
            "redTotalExperience": red_xp,
            "redTotalMinionsKilled": red_cs,
            "redTotalJungleMinionsKilled": red_jungle,
            "redKills": red_kills,
            "redDeaths": blue_kills,
            "redDragons": red_dragons,
            "redHeralds": red_heralds,
            "redVoidgrubs": red_grubs,
            "redTowersDestroyed": red_towers,
            "redGoldDiff": red_gold - blue_gold,
            "redExperienceDiff": red_xp - blue_xp
        }
        return record

    def save_record(self, record: Dict[str, Any]) -> None:
        """Lưu một bản ghi trận đấu vào SQLite với cơ chế INSERT OR REPLACE."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cols = ", ".join(record.keys())
            placeholders = ", ".join(["?"] * len(record))
            sql = f"INSERT OR REPLACE INTO matches_10min ({cols}) VALUES ({placeholders})"
            cursor.execute(sql, list(record.values()))
            conn.commit()

    def export_to_csv(self) -> pd.DataFrame:
        """Đồng bộ toàn bộ bảng SQLite ra file CSV."""
        with self.get_db_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM matches_10min ORDER BY crawled_at DESC", conn)
        df.to_csv(str(OUTPUT_CSV), index=False, encoding="utf-8-sig")
        return df

    def run_for_server(self, target_matches: int = 50) -> int:
        """Thực hiện chu trình cào hoàn chỉnh cho một máy chủ."""
        print("\n" + "=" * 80)
        print(f"   BẮT ĐẦU CÀO DỮ LIỆU MÁY CHỦ: {self.label.upper()} ({self.country.upper()})")
        print("=" * 80)

        puuids = self.get_high_elo_puuids(limit=50)
        if not puuids:
            print(f"[!] Không tìm thấy người chơi máy chủ {self.platform.upper()}. Bỏ qua máy chủ này.")
            return 0

        match_ids = self.get_match_ids(puuids, target_count=target_matches)
        if not match_ids:
            print(f"[+] Máy chủ {self.platform.upper()} đã thu thập đủ số trận mục tiêu!")
            return 0

        print(f"\n[3/3] Bắt đầu trích xuất mốc 10 phút của {len(match_ids)} trận ({self.country})...")
        saved_count = 0

        for idx, m_id in enumerate(match_ids, 1):
            try:
                record = self.extract_10min_features(m_id)
                if record:
                    self.save_record(record)
                    saved_count += 1
                    print(
                        f"[{saved_count}/{len(match_ids)}] [{record['server']}] Lưu {m_id} | "
                        f"Mid: [{record['blueMid']} vs {record['redMid']}] | "
                        f"Lệch vàng: {record['blueGoldDiff']:+d}"
                    )
                else:
                    print(f"[-] Bỏ qua trận {m_id} (Trận Remake hoặc thời lượng < 10 phút)")
            except Exception as e:
                print(f"[!] Lỗi khi xử lý trận {m_id}: {e}")

            # Đồng bộ CSV định kỳ mỗi 10 trận
            if saved_count > 0 and saved_count % 10 == 0:
                self.export_to_csv()

        # Xuất file CSV lần cuối sau khi hoàn tất
        self.export_to_csv()
        print(f"\n[+] Hoàn tất cào máy chủ {self.label}: Đã lưu {saved_count} trận mới vào CSDL.")
        return saved_count


# ==============================================================================
# 3. ĐIỂM KHỞI CHẠY CHÍNH (MAIN ENTRYPOINT)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("   HỆ THỐNG CÀO DỮ LIỆU ĐA QUỐC GIA (MULTI-SERVER) TỪ RIOT GAMES API   ")
    print(f"   Máy chủ mục tiêu: {[SERVER_METADATA.get(s, {}).get('label', s) for s in ACTIVE_SERVERS]}")
    print(f"   Chỉ tiêu mỗi máy chủ: {TARGET_MATCHES_PER_SERVER} trận")
    print("=" * 80)

    total_new_matches = 0
    for srv in ACTIVE_SERVERS:
        crawler = RiotApiCrawler(api_key=RIOT_API_KEY, platform=srv)
        count = crawler.run_for_server(target_matches=TARGET_MATCHES_PER_SERVER)
        total_new_matches += count

    print("\n" + "=" * 80)
    print(f"🎉 TỔNG KẾT: Đã hoàn tất! Thu thập thành công {total_new_matches} trận mới.")
    print(f"CSDL SQLite: '{OUTPUT_DB}'")
    print(f"Tệp CSV:     '{OUTPUT_CSV}'")
    print("=" * 80)
