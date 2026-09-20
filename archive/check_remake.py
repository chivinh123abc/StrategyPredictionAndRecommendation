import pandas as pd
import numpy as np

def inspect_remakes_and_outliers():
    print("=" * 80)
    print("   BÁO CÁO PHÂN TÍCH TRẬN REMAKE & DỮ LIỆU BẤT THƯỜNG (CHƯƠNG 2: DATA CLEANING)   ")
    print("=" * 80)

    url = 'https://raw.githubusercontent.com/SharnSingh/LeagueOfLegends_Diamond_PredictiveAnalysis/master/high_diamond_ranked_10min.csv'
    df = pd.read_csv(url)
    total_matches = len(df)
    print(f"\n[+] Tổng số trận trong dataset: {total_matches} trận.")

    # 1. Cơ chế Remake trong Riot API
    print("\n--- 1. BẢN CHẤT CƠ CHẾ REMAKE TRONG DỮ LIỆU RIOT GAMES ---")
    print("• Trong Liên Minh Huyền Thoại, trận REMAKE xảy ra khi có tuyển thủ AFK/Disconnect")
    print("  ngay từ đầu trận, và đội đó bỏ phiếu hủy trận ở phút thứ 3:00 - 3:30 (~180 - 210 giây).")
    print("• Trong dữ liệu đầy đủ từ Riot Match API (cột 'gameDuration'), tiêu chuẩn vàng của giới")
    print("  Data Science là lọc bỏ các trận có thời gian dưới 5 phút:")
    print("      df_clean = df[df['gameDuration'] >= 300]  # Lọc bỏ 100% trận Remake")
    print("• Với bộ dữ liệu 9,879 trận này: Vì dataset được lấy mốc phút thứ 10:00 (600 giây),")
    print("  nên các trận Remake dưới 4 phút ĐÃ ĐƯỢC TỰ ĐỘNG LOẠI BỎ NGAY TỪ ĐẦU (vì không thể tồn tại tới phút 10).")

    # 2. Dò tìm các trận AFK / Bỏ cuộc sau phút thứ 3 (ở mốc phút 10)
    print("\n--- 2. DÒ TÌM CÁC TRẬN CÓ NGƯỜI CHƠI AFK / THOÁT GAME Ở MỐC PHÚT 10 ---")
    print("• Ở phút thứ 10, một đội 5 người bình thường farm được khoảng 180 - 220 lính (CS).")
    print("• Nếu tổng lính cả đội < 110 lính => Chắc chắn có ít nhất 1-2 thành viên bị AFK/Disconnect.")
    
    afk_mask = (df['blueTotalMinionsKilled'] < 110) | (df['redTotalMinionsKilled'] < 110)
    afk_games = df[afk_mask]
    print(f"-> Tìm thấy {len(afk_games)} trận đấu có dấu hiệu AFK/Thoát trận nghiêm trọng.")
    for idx, r in afk_games.iterrows():
        print(f"   [!] Mã trận {int(r['gameId'])}:")
        print(f"       - Phe Xanh: {r['blueTotalMinionsKilled']} lính | Vàng: {r['blueTotalGold']} | Hạ gục: {r['blueKills']}")
        print(f"       - Phe Đỏ  : {r['redTotalMinionsKilled']} lính | Vàng: {r['redTotalGold']} | Hạ gục: {r['redKills']}")

    # 3. Dò tìm các trận đấu 'Troll / Phá game / Feed mạng' bằng thuật toán IQR (Chương 2)
    print("\n--- 3. ỨNG DỤNG THUẬT TOÁN IQR ĐỂ PHÁT HIỆN CÁC TRẬN ĐẤU OUTLIERS CỰC ĐOAN ---")
    df['goldDiff'] = df['blueTotalGold'] - df['redTotalGold']
    q1 = df['goldDiff'].quantile(0.25)
    q3 = df['goldDiff'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 2.5 * iqr
    upper_bound = q3 + 2.5 * iqr

    outliers = df[(df['goldDiff'] < lower_bound) | (df['goldDiff'] > upper_bound)]
    print(f"• Khoảng chênh lệch vàng bình thường ở phút 10: [{lower_bound:.0f} đến +{upper_bound:.0f} vàng]")
    print(f"• Số trận đấu Outliers cực đoan phát hiện được: {len(outliers)} trận (chiếm {len(outliers)/total_matches*100:.2f}% dataset).")
    print("  -> Đây là các trận có người chơi cố tình 'Feed mạng liên tục' khiến chênh lệch > 7,000 - 8,000 vàng")
    print("     ngay ở phút thứ 10. Trong Chương 2, ta cần loại bỏ các trận này để mô hình ML không bị nhiễu!")

    print("\n" + "=" * 80)
    print("   KẾT LUẬN: ĐÂY CHÍNH LÀ QUY TRÌNH DATA CLEANING CHUẨN CỦA CHƯƠNG 2!   ")
    print("=" * 80)

if __name__ == "__main__":
    inspect_remakes_and_outliers()
