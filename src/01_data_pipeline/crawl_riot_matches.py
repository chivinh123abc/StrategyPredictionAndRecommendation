"""
================================================================================
SCRIPT CÀO DỮ LIỆU LIÊN MINH HUYỀN THOẠI TRỰC TIẾP TỪ RIOT GAMES API (PHIÊN BẢN HIỆN TẠI)
Dự án: Nhập môn Khoa học Dữ liệu - PTIT
Hỗ trợ: Máy chủ Việt Nam (VN2) và Hàn Quốc (KR)
Đặc tả: Cào các trận đấu Rank Cao (Thách Đấu / Kim Cương), trích xuất chỉ số phút thứ 10
        và lưu đồng thời ra file CSV và SQLite Database.
================================================================================
"""

import os
import sys
import time
import json
import sqlite3
import requests
import pandas as pd
from datetime import datetime

# Thêm thư mục gốc vào sys.path để luôn tìm thấy module cấu hình trong src/config
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
        ACTIVE_SERVERS,
        OUTPUT_CSV,
        OUTPUT_DB,
        RIOT_API_KEY,
        SERVER_METADATA,
        TARGET_MATCHES_PER_SERVER,
    )
except (ImportError, ModuleNotFoundError):
    from config import (
        ACTIVE_SERVERS,
        OUTPUT_CSV,
        OUTPUT_DB,
        RIOT_API_KEY,
        SERVER_METADATA,
        TARGET_MATCHES_PER_SERVER,
    )




# ==============================================================================
# 2. CLASS QUẢN LÝ GỌI API & CHỐNG CHẶN RATE LIMIT (100 req / 2 phút)
# ==============================================================================
class RiotApiCrawler:
    def __init__(self, api_key, platform="vn2"):
        self.api_key = api_key.strip()
        self.platform = platform.lower()
        meta = SERVER_METADATA.get(self.platform, {"region": "sea", "country": "Unknown", "label": self.platform})
        self.region = meta["region"]
        self.country = meta["country"]
        self.label = meta["label"]
        self.headers = {"X-Riot-Token": self.api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Tải bảng ánh xạ ID tướng sang Tên tướng từ Riot CDN để giải mã danh sách Cấm (Bans)
        self.champ_id_map = self.load_champion_id_map()

        # Tạo bảng trong SQLite để lưu dữ liệu an toàn
        self.init_db()

    def load_champion_id_map(self):
        """Tải bảng ánh xạ ID tướng sang Tên tướng từ Riot CDN để giải mã mã tướng bị Cấm"""
        try:
            v_res = requests.get('https://ddragon.leagueoflegends.com/api/versions.json', timeout=5).json()
            latest_v = v_res[0]
            res = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{latest_v}/data/en_US/champion.json', timeout=10)
            data = res.json()['data']
            id_map = {int(v['key']): v['name'] for v in data.values()}
            print(f"[+] Đã tải danh mục {len(id_map)} vị tướng từ Riot CDN (Phiên bản {latest_v}).")
            return id_map
        except Exception as e:
            print(f"[!] Không thể tải bảng ánh xạ tướng: {e}")
            return {}

    def parse_team_positions(self, participants):
        """Phân tích vị trí thi đấu chuẩn của 5 thành viên: TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY"""
        roles = {'TOP': 'Unknown', 'JUNGLE': 'Unknown', 'MIDDLE': 'Unknown', 'BOTTOM': 'Unknown', 'UTILITY': 'Unknown'}
        unassigned = []
        for p in participants:
            pos = p.get('teamPosition', '')
            c = p.get('championName', 'Unknown')
            if pos in roles and roles[pos] == 'Unknown':
                roles[pos] = c
            else:
                unassigned.append(c)
        for k in ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']:
            if roles[k] == 'Unknown' and unassigned:
                roles[k] = unassigned.pop(0)
        return roles

    def init_db(self):
        conn = sqlite3.connect(OUTPUT_DB)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches_10min (
                gameId TEXT PRIMARY KEY,
                gameVersion TEXT,
                gameDuration INTEGER,
                blueWins INTEGER,
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
                blueTotalGold INTEGER,
                blueTotalExperience INTEGER,
                blueTotalMinionsKilled INTEGER,
                blueTotalJungleMinionsKilled INTEGER,
                blueKills INTEGER,
                blueDeaths INTEGER,
                blueDragons INTEGER,
                blueHeralds INTEGER,
                blueVoidgrubs INTEGER,
                blueTowersDestroyed INTEGER,
                blueGoldDiff INTEGER,
                blueExperienceDiff INTEGER,
                redTotalGold INTEGER,
                redTotalExperience INTEGER,
                redTotalMinionsKilled INTEGER,
                redTotalJungleMinionsKilled INTEGER,
                redKills INTEGER,
                redDeaths INTEGER,
                redDragons INTEGER,
                redHeralds INTEGER,
                redVoidgrubs INTEGER,
                redTowersDestroyed INTEGER,
                redGoldDiff INTEGER,
                redExperienceDiff INTEGER,
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Tự động cập nhật thêm cột hoặc loại bỏ cột dư thừa (Chuẩn hóa 1NF & 3NF)
        cursor.execute("PRAGMA table_info(matches_10min)")
        existing_cols = [c[1] for c in cursor.fetchall()]
        if 'blueChampions' in existing_cols:
            cursor.execute("ALTER TABLE matches_10min DROP COLUMN blueChampions")
        if 'redChampions' in existing_cols:
            cursor.execute("ALTER TABLE matches_10min DROP COLUMN redChampions")
        if 'country' in existing_cols:
            cursor.execute("ALTER TABLE matches_10min DROP COLUMN country")

        lane_cols = [
            'blueBans', 'redBans',
            'blueTop', 'blueJungle', 'blueMid', 'blueAdc', 'blueSupport',
            'redTop', 'redJungle', 'redMid', 'redAdc', 'redSupport',
            'server'
        ]
        for col in lane_cols:
            if col not in existing_cols:
                cursor.execute(f"ALTER TABLE matches_10min ADD COLUMN {col} TEXT")
                
        # Tự động gán server cho các trận cũ nếu còn thiếu dựa vào tiền tố gameId
        cursor.execute("UPDATE matches_10min SET server = 'VN2' WHERE (server IS NULL OR server = '') AND gameId LIKE 'VN2_%'")
        cursor.execute("UPDATE matches_10min SET server = 'KR' WHERE (server IS NULL OR server = '') AND gameId LIKE 'KR_%'")
        cursor.execute("UPDATE matches_10min SET server = 'TW2' WHERE (server IS NULL OR server = '') AND gameId LIKE 'TW2_%'")
        conn.commit()
        conn.close()

    def get_with_retry(self, url):
        """Tự động ngủ và gửi lại request nếu chạm trần giới hạn gọi API (Rate Limit 429)"""
        while True:
            try:
                res = self.session.get(url, timeout=15)
                if res.status_code == 200:
                    return res.json()
                elif res.status_code == 429:
                    # Chạm rate limit của Riot, đọc thời gian cần ngủ từ header
                    retry_after = int(res.headers.get("Retry-After", 10))
                    print(f"   [!] Chạm Rate Limit Riot API. Tự động tạm dừng {retry_after + 1}s...")
                    time.sleep(retry_after + 1)
                elif res.status_code == 403:
                    print("\n[LỖI 403 - FORBIDDEN]: API Key của bạn chưa hợp lệ hoặc đã hết hạn 24h!")
                    print("-> Vui lòng vào https://developer.riotgames.com bấm 'Regenerate Key' và dán lại vào code.")
                    sys.exit(1)
                elif res.status_code == 404:
                    return None
                else:
                    print(f"   [!] Mã lỗi HTTP {res.status_code} từ Riot API: {url}")
                    time.sleep(2)
                    return None
            except requests.exceptions.RequestException as e:
                print(f"   [!] Lỗi mạng: {e}. Thử lại sau 3s...")
                time.sleep(3)

    def get_high_elo_puuids(self, limit=100):
        """Lấy danh sách tuyển thủ Thách Đấu / Đại Cao Thủ để cào các trận rank đỉnh cao"""
        print(f"\n[1/3] Đang lấy danh sách người chơi Rank Cao máy chủ '{self.platform.upper()}'...")
        url = f"https://{self.platform}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
        data = self.get_with_retry(url)
        
        puuids = []
        if data and "entries" in data:
            entries = data["entries"]
            print(f"-> Tìm thấy {len(entries)} người chơi Thách Đấu.")
            
            # Lấy PUUID từ summonerId
            for i, entry in enumerate(entries[:limit]):
                puuid = entry.get("puuid")
                if not puuid:
                    # Gọi Summoner API để đổi sang puuid
                    s_id = entry.get("summonerId")
                    s_url = f"https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/{s_id}"
                    s_data = self.get_with_retry(s_url)
                    if s_data and "puuid" in s_data:
                        puuid = s_data["puuid"]
                    time.sleep(1.2) # Giữ khoảng cách request
                
                if puuid:
                    puuids.append(puuid)
                if len(puuids) >= limit:
                    break
                    
        print(f"-> Đã thu thập được {len(puuids)} PUUID người chơi để dò tìm trận đấu.")
        return puuids

    def get_match_ids(self, puuids, target_count=100):
        """Lấy danh sách mã trận đấu xếp hạng Solo/Duo (queue 420)"""
        print(f"\n[2/3] Đang dò tìm {target_count} mã trận đấu Xếp Hạng mới nhất...")
        match_ids = set()
        
        # Kiểm tra các trận đã có sẵn trong DB để không cào trùng
        conn = sqlite3.connect(OUTPUT_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT gameId FROM matches_10min")
        existing_ids = set(row[0] for row in cursor.fetchall())
        conn.close()
        print(f"-> Trong cơ sở dữ liệu hiện đã có sẵn {len(existing_ids)} trận.")

        for idx, puuid in enumerate(puuids):
            if len(match_ids) >= target_count:
                break
                
            url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=20"
            ids = self.get_with_retry(url)
            if ids:
                for m_id in ids:
                    if m_id not in existing_ids:
                        match_ids.add(m_id)
                        if len(match_ids) >= target_count:
                            break
                            
            print(f"   - Đã quét xong người chơi {idx+1}/{len(puuids)}: Gom được {len(match_ids)} mã trận mới.", end="\r")
            time.sleep(1.2) # Tránh nghẽn request

        print(f"\n-> Hoàn tất gom {len(match_ids)} mã trận đấu mới đủ điều kiện.")
        return list(match_ids)

    def extract_10min_features(self, match_id):
        """Trích xuất dữ liệu mốc phút thứ 10 từ Match Detail và Match Timeline"""
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
            return None # Không đủ 10 phút

        frame_10 = frames[10]
        p_frames = frame_10.get("participantFrames", {})

        # Tách 2 đội: Player 1-5 là Blue Team, 6-10 là Red Team
        blue_gold = sum(p_frames[str(i)]["totalGold"] for i in range(1, 6) if str(i) in p_frames)
        blue_xp = sum(p_frames[str(i)]["xp"] for i in range(1, 6) if str(i) in p_frames)
        blue_cs = sum(p_frames[str(i)]["minionsKilled"] for i in range(1, 6) if str(i) in p_frames)
        blue_jungle = sum(p_frames[str(i)]["jungleMinionsKilled"] for i in range(1, 6) if str(i) in p_frames)

        red_gold = sum(p_frames[str(i)]["totalGold"] for i in range(6, 11) if str(i) in p_frames)
        red_xp = sum(p_frames[str(i)]["xp"] for i in range(6, 11) if str(i) in p_frames)
        red_cs = sum(p_frames[str(i)]["minionsKilled"] for i in range(6, 11) if str(i) in p_frames)
        red_jungle = sum(p_frames[str(i)]["jungleMinionsKilled"] for i in range(6, 11) if str(i) in p_frames)

        # Đếm các sự kiện xảy ra TRƯỚC phút thứ 10 (mạng, rồng, sứ giả, sâu hư không, trụ)
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
                    elif m_type == "HORDE" or "GRUBS" in sub_type:  # Sâu Hư Không (Phiên bản mới)
                        if is_blue: blue_grubs += 1
                        else: red_grubs += 1
                elif e_type == "BUILDING_KILL" and event.get("buildingType") == "TOWER_BUILDING":
                    team_id = event.get("teamId", 0)
                    if team_id == 200: # Đội Đỏ mất trụ => Đội Xanh ăn
                        blue_towers += 1
                    elif team_id == 100:
                        red_towers += 1

        # Trích xuất danh sách Cấm (Bans) của 2 đội (Chương 6: Phân tích Cấm/Chọn)
        teams = info.get("teams", [])
        blue_bans = []
        red_bans = []
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

        blue_bans_str = ", ".join(blue_bans) if blue_bans else "None"
        red_bans_str = ", ".join(red_bans) if red_bans else "None"

        # Trích xuất 10 vị tướng và vị trí thi đấu 5 đường (Top, Jungle, Mid, ADC, Support - Chương 6)
        blue_roles = self.parse_team_positions(info.get("participants", [])[:5])
        red_roles = self.parse_team_positions(info.get("participants", [])[5:10])

        record = {
            "gameId": match_id,
            "server": self.platform.upper(),
            "gameVersion": game_version,
            "gameDuration": duration,
            "blueWins": blue_win,
            "blueBans": blue_bans_str,
            "redBans": red_bans_str,
            "blueTop": blue_roles['TOP'],
            "blueJungle": blue_roles['JUNGLE'],
            "blueMid": blue_roles['MIDDLE'],
            "blueAdc": blue_roles['BOTTOM'],
            "blueSupport": blue_roles['UTILITY'],
            "redTop": red_roles['TOP'],
            "redJungle": red_roles['JUNGLE'],
            "redMid": red_roles['MIDDLE'],
            "redAdc": red_roles['BOTTOM'],
            "redSupport": red_roles['UTILITY'],
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

    def save_record(self, record):
        """Lưu ngay lập tức từng trận vào SQLite để không bao giờ bị mất dữ liệu khi mất mạng"""
        conn = sqlite3.connect(OUTPUT_DB)
        cursor = conn.cursor()
        cols = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        sql = f"INSERT OR REPLACE INTO matches_10min ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, list(record.values()))
        conn.commit()
        conn.close()

    def export_to_csv(self):
        """Xuất toàn bộ bảng SQLite ra file CSV tiêu chuẩn để làm bài tập lớn"""
        conn = sqlite3.connect(OUTPUT_DB)
        df = pd.read_sql_query("SELECT * FROM matches_10min", conn)
        conn.close()
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"\n[THÀNH CÔNG] Đã xuất {len(df)} trận đấu ra file CSV: '{OUTPUT_CSV}'!")
        return df

    def backfill_missing_champions(self):
        """Tự động bổ sung thông tin Cấm/Chọn (Bans & 5 Vị trí Picks) cho những trận đã cào trước đó nếu còn thiếu"""
        conn = sqlite3.connect(OUTPUT_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT gameId FROM matches_10min WHERE blueTop IS NULL OR blueTop = '' OR blueBans IS NULL OR blueBans = ''")
        missing_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if missing_ids:
            print(f"\n[+] Phát hiện {len(missing_ids)} trận đã lưu trước đó chưa có 5 Vị trí & Cấm/Chọn. Đang tự động cập nhật...")
            for idx, m_id in enumerate(missing_ids):
                detail_url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{m_id}"
                detail = self.get_with_retry(detail_url)
                time.sleep(1.2)
                if detail and "info" in detail:
                    info = detail["info"]
                    participants = info.get("participants", [])
                    b_roles = self.parse_team_positions(participants[:5])
                    r_roles = self.parse_team_positions(participants[5:10])

                    b_champs = [p.get("championName", "") for p in participants if p.get("teamId") == 100]
                    r_champs = [p.get("championName", "") for p in participants if p.get("teamId") == 200]
                    
                    teams = info.get("teams", [])
                    b_bans = []
                    r_bans = []
                    if len(teams) > 0:
                        for b in teams[0].get("bans", []):
                            cid = b.get("championId", -1)
                            if cid != -1 and cid in self.champ_id_map:
                                b_bans.append(self.champ_id_map[cid])
                    if len(teams) > 1:
                        for b in teams[1].get("bans", []):
                            cid = b.get("championId", -1)
                            if cid != -1 and cid in self.champ_id_map:
                                r_bans.append(self.champ_id_map[cid])

                    conn = sqlite3.connect(OUTPUT_DB)
                    c = conn.cursor()
                    c.execute("""UPDATE matches_10min 
                                 SET blueBans = ?, redBans = ?,
                                     blueTop = ?, blueJungle = ?, blueMid = ?, blueAdc = ?, blueSupport = ?,
                                     redTop = ?, redJungle = ?, redMid = ?, redAdc = ?, redSupport = ?
                                 WHERE gameId = ?""", 
                              (", ".join(b_bans) if b_bans else "None", 
                               ", ".join(r_bans) if r_bans else "None",
                               b_roles['TOP'], b_roles['JUNGLE'], b_roles['MIDDLE'], b_roles['BOTTOM'], b_roles['UTILITY'],
                               r_roles['TOP'], r_roles['JUNGLE'], r_roles['MIDDLE'], r_roles['BOTTOM'], r_roles['UTILITY'],
                               m_id))
                    conn.commit()
                    conn.close()
                    print(f"   [{idx+1}/{len(missing_ids)}] Điền 5 đường cho {m_id}: Mid [{b_roles['MIDDLE']} vs {r_roles['MIDDLE']}] | Top [{b_roles['TOP']} vs {r_roles['TOP']}]")
            self.export_to_csv()
            print("[+] Hoàn tất cập nhật 5 Vị trí & Cấm/Chọn cho các trận cũ!\n")

    def run_for_server(self, target_matches=50):
        print("\n" + "=" * 80)
        print(f"   BẮT ĐẦU CÀO DỮ LIỆU MÁY CHỦ: {self.label.upper()} ({self.country.upper()})")
        print("=" * 80)
        
        if "YOUR-KEY-HERE" in self.api_key or not self.api_key.startswith("RGAPI-"):
            print("\n[CHÚ Ý QUAN TRỌNG]: Bạn chưa gắn mã API Key thật của Riot Games!")
            return 0

        # 0. Tự động kiểm tra và điền thông tin Cấm/Chọn cho các trận cũ nếu có
        self.backfill_missing_champions()

        # 1. Thu thập người chơi
        puuids = self.get_high_elo_puuids(limit=50)
        if not puuids:
            print(f"[!] Không tìm thấy danh sách người chơi máy chủ {self.platform.upper()}. Bỏ qua máy chủ này.")
            return 0

        # 2. Gom danh sách trận đấu
        match_ids = self.get_match_ids(puuids, target_count=target_matches)

        # 3. Tiến hành cào chi tiết từng trận
        print(f"\n[3/3] Bắt đầu trích xuất mốc 10 phút của {len(match_ids)} trận ({self.country})...")
        saved_count = 0
        for idx, m_id in enumerate(match_ids):
            try:
                record = self.extract_10min_features(m_id)
                if record:
                    self.save_record(record)
                    saved_count += 1
                    print(f"[{saved_count}/{len(match_ids)}] [{record['server']}] Lưu {m_id} | Mid: [{record['blueMid']} vs {record['redMid']}] | Top: [{record['blueTop']} vs {record['redTop']}] | Lệch vàng: {record['blueGoldDiff']:+d}")
                else:
                    print(f"[-] Bỏ qua trận {m_id} (Trận Remake hoặc thời lượng < 10 phút)")
            except Exception as e:
                print(f"[!] Lỗi khi xử lý trận {m_id}: {e}")

            # Cứ mỗi 10 trận tự động cập nhật file CSV 1 lần
            if saved_count > 0 and saved_count % 10 == 0:
                self.export_to_csv()

        # Xuất file cuối cùng
        self.export_to_csv()
        print(f"\n[+] Hoàn tất cào máy chủ {self.label}: Đã lưu {saved_count} trận mới.")
        return saved_count


if __name__ == "__main__":
    print("=" * 80)
    print("   HỆ THỐNG CÀO DỮ LIỆU ĐA QUỐC GIA (MULTI-SERVER) TỪ RIOT GAMES API   ")
    print(f"   Danh sách máy chủ mục tiêu: {[SERVER_METADATA[s]['label'] for s in ACTIVE_SERVERS]}")
    print("=" * 80)
    
    total_saved = 0
    for srv in ACTIVE_SERVERS:
        crawler = RiotApiCrawler(api_key=RIOT_API_KEY, platform=srv)
        count = crawler.run_for_server(target_matches=TARGET_MATCHES_PER_SERVER)
        total_saved += count
        
    print("\n" + "=" * 80)
    print(f"🎉 TỔNG KẾT: Đã hoàn tất cào toàn bộ các máy chủ! Tổng số trận mới: {total_saved}")
    print(f"File lưu trữ: '{OUTPUT_CSV}' và cơ sở dữ liệu SQLite: '{OUTPUT_DB}'")
    print("=" * 80)
