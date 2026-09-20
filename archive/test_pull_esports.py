import requests
import json
import sqlite3
import pandas as pd
import numpy as np

def run_esports_demo():
    print("================================================================================")
    print("          DEMO: PULLING REAL ESPORTS DATA & MAPPING TO COURSE SYLLABUS          ")
    print("================================================================================\n")

    # --------------------------------------------------------------------------
    # CHƯƠNG 2: THU THẬP DỮ LIỆU TỪ OFFICIAL RIOT API & PUBLIC DATASET
    # --------------------------------------------------------------------------
    print(">>> [CHƯƠNG 2: DATA PREPARATION] KÉO DỮ LIỆU THỰC TẾ...")
    # 1. Kéo dữ liệu Tướng từ Riot Data Dragon (Bản mới nhất)
    ver_res = requests.get('https://ddragon.leagueoflegends.com/api/versions.json', timeout=10)
    latest_ver = ver_res.json()[0]
    champs_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_ver}/data/vi_VN/champion.json"
    champs_raw = requests.get(champs_url, timeout=10).json()['data']

    champ_list = []
    for k, v in champs_raw.items():
        champ_list.append({
            'champ_id': int(v['key']),
            'name': v['name'],
            'title': v['title'],
            'primary_role': v['tags'][0] if v['tags'] else 'Unknown',
            'attack': v['info']['attack'],
            'defense': v['info']['defense'],
            'magic': v['info']['magic'],
            'difficulty': v['info']['difficulty'],
            'hp': v['stats']['hp'],
            'attackdamage': v['stats']['attackdamage'],
            'blurb': v['blurb'] # Dùng cho TF-IDF Recommender System
        })
    df_champs = pd.DataFrame(champ_list)
    print(f" [+] Kéo thành công {len(df_champs)} vị tướng LoL (Patch {latest_ver}) từ Riot Games.")

    # 2. Kéo dữ liệu 9,879 trận đấu rank Kim Cương thực tế
    matches_url = "https://raw.githubusercontent.com/SharnSingh/LeagueOfLegends_Diamond_PredictiveAnalysis/master/high_diamond_ranked_10min.csv"
    df_matches = pd.read_csv(matches_url)
    print(f" [+] Tải thành công {len(df_matches)} trận đấu Rank Cao (Diamond) với {df_matches.shape[1]} chỉ số/trận.\n")

    # --------------------------------------------------------------------------
    # CHƯƠNG 5 & 5x: LƯU TRỮ VÀO SQL DATABASE & TRUY VẤN SQL NÂNG CAO
    # --------------------------------------------------------------------------
    print(">>> [CHƯƠNG 5: SQL & DATABASES] TẠO SCHEMA & THỰC THI TRUY VẤN SQL...")
    conn = sqlite3.connect('esports_demo.db')
    cursor = conn.cursor()

    # DDL: Tạo bảng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Champions (
        champ_id INTEGER PRIMARY KEY,
        name TEXT,
        title TEXT,
        primary_role TEXT,
        attack INTEGER,
        defense INTEGER,
        magic INTEGER,
        difficulty INTEGER,
        hp REAL,
        attackdamage REAL,
        blurb TEXT
    )
    """)
    df_champs.to_sql('Champions', conn, if_exists='replace', index=False)
    
    # Lưu bảng trận đấu (lấy mẫu 1,000 trận cho demo nhẹ)
    df_matches.head(1000).to_sql('Matches', conn, if_exists='replace', index=False)

    # Viết câu truy vấn SQL có GROUP BY, HAVING, AVG theo đúng bài giảng Chapter 5
    query = """
    SELECT primary_role, 
           COUNT(*) as total_champions, 
           ROUND(AVG(attack), 2) as avg_attack, 
           ROUND(AVG(magic), 2) as avg_magic, 
           ROUND(AVG(hp), 1) as avg_base_hp
    FROM Champions
    GROUP BY primary_role
    HAVING COUNT(*) >= 5
    ORDER BY avg_attack DESC
    """
    df_sql_result = pd.read_sql_query(query, conn)
    print(" [SQL Query Output]: Thống kê chỉ số tướng theo Vai trò (GROUP BY & HAVING):")
    print(df_sql_result)
    print()

    # --------------------------------------------------------------------------
    # CHƯƠNG 1: THỐNG KÊ SUY LUẬN & KIỂM ĐỊNH GIẢ THUYẾT (HYPOTHESIS TESTING)
    # --------------------------------------------------------------------------
    print(">>> [CHƯƠNG 1: THỐNG KÊ TOÁN & KIỂM ĐỊNH] A/B TESTING LỢI THẾ SÂN NHÀ (BLUE SIDE)...")
    blue_wins = df_matches['blueWins']
    blue_win_rate = blue_wins.mean() * 100
    print(f" [+] Tỷ lệ thắng thực tế của Phe Xanh (Blue Team): {blue_win_rate:.2f}% (trên {len(df_matches)} trận)")
    
    # Kiểm định giả thuyết: Tỷ lệ thắng phe xanh có thực sự = 50% hay không?
    # Dùng Z-test cho tỷ lệ (Proportion Z-test)
    p0 = 0.50
    n = len(blue_wins)
    p_hat = blue_wins.mean()
    z_stat = (p_hat - p0) / np.sqrt((p0 * (1 - p0)) / n)
    # p-value 2 phía
    from math import erf
    def norm_cdf(z):
        return 0.5 * (1.0 + erf(z / np.sqrt(2.0)))
    p_val = 2 * (1 - norm_cdf(abs(z_stat)))
    
    print(f" [+] Kết quả kiểm định: Z-score = {z_stat:.4f}, p-value = {p_val:.4e}")
    if p_val < 0.05:
        print(" => KẾT LUẬN: Bác bỏ H0! Có bằng chứng thống kê vững chắc (p < 0.05) chứng minh phe Xanh có lợi thế bản đồ đáng kể!")
    else:
        print(" => KẾT LUẬN: Chưa đủ bằng chứng bác bỏ H0.")
    print()

    # --------------------------------------------------------------------------
    # CHƯƠNG 6: GỢI Ý TƯỚNG BẰNG COSINE SIMILARITY (CONTENT-BASED RECOMMENDER)
    # --------------------------------------------------------------------------
    print(">>> [CHƯƠNG 6: RECOMMENDATION SYSTEM] GỢI Ý TƯỚNG TƯƠNG ĐỒNG (COSINE SIMILARITY)...")
    # Tạo vector đặc trưng: attack, defense, magic, difficulty, hp, attackdamage
    feature_cols = ['attack', 'defense', 'magic', 'difficulty', 'hp', 'attackdamage']
    X_feat = df_champs[feature_cols].values
    
    # Chuẩn hóa vector (Z-score / Min-Max như Chapter 2)
    X_norm = (X_feat - X_feat.mean(axis=0)) / X_feat.std(axis=0)

    # Giả sử người chơi yêu thích tướng 'Yasuo'
    target_champ_name = 'Yasuo'
    yasuo_idx = df_champs[df_champs['name'] == target_champ_name].index[0]
    yasuo_vec = X_norm[yasuo_idx]

    # Tính Cosine Similarity giữa Yasuo và toàn bộ các tướng khác
    dot_prod = np.dot(X_norm, yasuo_vec)
    norms = np.linalg.norm(X_norm, axis=1) * np.linalg.norm(yasuo_vec)
    cos_sim = dot_prod / norms
    
    df_champs['similarity'] = cos_sim
    top_recommend = df_champs[df_champs['name'] != target_champ_name].sort_values(by='similarity', ascending=False).head(5)
    
    print(f" [+] Người chơi thích: [{target_champ_name} - {df_champs.loc[yasuo_idx, 'title']}]")
    print(f" [+] Top 5 vị tướng gợi ý tương đồng nhất (Chất tướng & phong cách):")
    for rank, (_, row) in enumerate(top_recommend.iterrows(), 1):
        print(f"     {rank}. {row['name']} ({row['title']}) - Độ tương đồng: {row['similarity']*100:.1f}% | Vai trò: {row['primary_role']}")

    print("\n================================================================================")
    print("   THỬ NGHIỆM THÀNH CÔNG: DỮ LIỆU THẬT - SQL THẬT - THỐNG KÊ THẬT - GỢI Ý THẬT!   ")
    print("================================================================================")

if __name__ == "__main__":
    run_esports_demo()
