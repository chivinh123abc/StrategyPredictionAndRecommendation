import pandas as pd
import numpy as np

def run_analysis():
    url = 'https://raw.githubusercontent.com/SharnSingh/LeagueOfLegends_Diamond_PredictiveAnalysis/master/high_diamond_ranked_10min.csv'
    df = pd.read_csv(url)
    print("=" * 75)
    print(f"TỔNG SỐ TRẬN TRONG TẬP DỮ LIỆU: {len(df)} TRẬN (RANK KIM CƯƠNG HÀN QUỐC)")
    print("=" * 75)

    print("\n[PHẦN 1] BẢN CHẤT CÁC TRẬN REMAKE TRONG DỮ LIỆU LIÊN MINH HUYỀN THOẠI")
    print("-" * 75)
    print("1. Cơ chế Remake của Riot:")
    print("   - Khi 1 người chơi mất kết nối từ đầu trận, lệnh /remake sẽ xuất hiện ở phút 3:00 - 3:30.")
    print("   - Khi bỏ phiếu Remake thành công, trận đấu LẬP TỨC KẾT THÚC ở khoảng 180s - 210s.")
    print("2. Trong dataset đầy đủ từ Riot Match API (có cột 'gameDuration'):")
    print("   - Tiêu chuẩn lọc Remake kinh điển: df_clean = df[df['gameDuration'] >= 300] (>= 5 phút).")
    print("3. Trong dataset 'high_diamond_ranked_10min.csv' này:")
    print("   - Do crawler trích xuất dữ liệu snapshot ĐÚNG MỐC PHÚT 10 (Frame 10:00 = 600s),")
    print("     nên các trận Remake dưới 4 phút ĐÃ TỰ ĐỘNG KHÔNG XUẤT HIỆN trong file này")
    print("     (bởi vì trận đã bị hủy ở phút thứ 3, không thể có dữ liệu ở phút 10).")

    print("\n[PHẦN 2] DÒ TÌM CÁC TRẬN 'AFK / THOÁT GAME / RAGE QUIT' NGAY SAU PHÚT THỨ 3")
    print("-" * 75)
    print("Mặc dù trận không Remake được, nhưng người chơi vẫn AFK hoặc mất kết nối sau phút thứ 3:")
    
    # A. AFK lính cực thấp
    afk_cs = df[(df['blueTotalMinionsKilled'] < 120) | (df['redTotalMinionsKilled'] < 120)]
    print(f"\n1. Dấu hiệu AFK qua chỉ số lính toàn đội (CS < 120 so với chuẩn 216 lính):")
    print(f"   -> Phát hiện {len(afk_cs)} trận có người chơi bỏ lane/AFK hoàn toàn:")
    for _, r in afk_cs.iterrows():
        print(f"   * Game ID {int(r['gameId'])}: Phe Xanh = {int(r['blueTotalMinionsKilled'])} CS, Phe Đỏ = {int(r['redTotalMinionsKilled'])} CS | Chênh vàng: {int(r['blueGoldDiff'])}")

    # B. Rừng AFK
    jungle_afk = df[(df['blueTotalJungleMinionsKilled'] < 10) | (df['redTotalJungleMinionsKilled'] < 10)]
    print(f"\n2. Dấu hiệu Đi Rừng AFK / Bỏ quái rừng (Jungle CS < 10 so với chuẩn 51 con quái):")
    print(f"   -> Phát hiện {len(jungle_afk)} trận rừng không farm (AFK hoặc bị cướp 100% tài nguyên):")
    for _, r in jungle_afk.head(3).iterrows():
        print(f"   * Game ID {int(r['gameId'])}: Rừng Xanh = {int(r['blueTotalJungleMinionsKilled'])} quái, Rừng Đỏ = {int(r['redTotalJungleMinionsKilled'])} quái")

    # C. Troll cắm mắt phá game (Griefing / Ward Spamming)
    ward_troll = df[(df['blueWardsPlaced'] > 50) | (df['redWardsPlaced'] > 50)]
    print(f"\n3. Dấu hiệu Phá game / Cắm mắt troll trong bệ đá cổ (Wards > 50 mắt/10p so với chuẩn 22 mắt):")
    print(f"   -> Phát hiện {len(ward_troll)} trận người chơi mua mắt cắm nát bệ đá cổ:")
    for _, r in ward_troll.head(5).iterrows():
        print(f"   * Game ID {int(r['gameId'])}: Phe Xanh cắm {int(r['blueWardsPlaced'])} mắt, Phe Đỏ cắm {int(r['redWardsPlaced'])} mắt")

    print("\n[PHẦN 3] DÒ TÌM CÁC ĐIỂM NGOẠI LAI (OUTLIERS) BẰNG THUẬT TOÁN CHƯƠNG 2")
    print("-" * 75)
    # Thuật toán IQR (Interquartile Range)
    q1 = df['blueGoldDiff'].quantile(0.25)
    q3 = df['blueGoldDiff'].quantile(0.75)
    iqr = q3 - q1
    lower_iqr = q1 - 1.5 * iqr
    upper_iqr = q3 + 1.5 * iqr
    outliers_iqr = df[(df['blueGoldDiff'] < lower_iqr) | (df['blueGoldDiff'] > upper_iqr)]

    # Thuật toán Z-score
    mean_gold = df['blueGoldDiff'].mean()
    std_gold = df['blueGoldDiff'].std()
    z_scores = np.abs((df['blueGoldDiff'] - mean_gold) / std_gold)
    outliers_z = df[z_scores > 3]

    print(f"1. Thuật toán IQR (Tukey Outlier Boxplot rule: Q1 - 1.5*IQR đến Q3 + 1.5*IQR):")
    print(f"   - Ngưỡng bình thường: [{lower_iqr:.1f} đến {upper_iqr:.1f} vàng]")
    print(f"   - Số trận ngoại lai phát hiện: {len(outliers_iqr)} trận ({len(outliers_iqr)/len(df)*100:.2f}%)")
    print(f"2. Thuật toán Z-score (|Z| > 3):")
    print(f"   - Ngưỡng |Z| > 3 (ngoài 99.7% phân phối chuẩn):")
    print(f"   - Số trận ngoại lai phát hiện: {len(outliers_z)} trận ({len(outliers_z)/len(df)*100:.2f}%)")

    top_outlier = df.loc[df['blueGoldDiff'].abs().idxmax()]
    print(f"\n-> Trận đấu kỷ lục lệch vàng: Game ID {int(top_outlier['gameId'])}:")
    print(f"   - Chênh lệch: {int(top_outlier['blueGoldDiff'])} vàng ở phút thứ 10!")
    print(f"   - Tỉ số hạ gục: Xanh {int(top_outlier['blueKills'])} - {int(top_outlier['redKills'])} Đỏ")

if __name__ == '__main__':
    run_analysis()
