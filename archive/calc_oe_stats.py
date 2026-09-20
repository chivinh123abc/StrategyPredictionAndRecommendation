import pandas as pd

df = pd.read_csv('2026_LoL_esports_match_data_from_OraclesElixir.csv', low_memory=False)
teams = df[df['position'] == 'team'].dropna(subset=['golddiffat10', 'result'])
total_team_records = len(teams)
print(f"Tổng số bản ghi đội tuyển: {total_team_records:,} (Tương ứng {total_team_records//2:,} trận đấu có số liệu phút 10)")

blue_teams = teams[teams['side'] == 'Blue']
red_teams = teams[teams['side'] == 'Red']
print(f"Tỷ lệ thắng Phe Xanh (Blue Winrate): {blue_teams['result'].mean():.2%}")
print(f"Tỷ lệ thắng Phe Đỏ (Red Winrate)   : {red_teams['result'].mean():.2%}")

ahead_1k = teams[teams['golddiffat10'] >= 1000]
ahead_2k = teams[teams['golddiffat10'] >= 2000]
ahead_3k = teams[teams['golddiffat10'] >= 3000]

print(f"\n--- HIỆU QUẢ LĂN CẦU TUYẾT Ở ĐẤU GIẢI CHUYÊN NGHIỆP 2026 ---")
print(f"Dẫn >= 1,000 vàng lúc 10p: Tỷ lệ thắng = {ahead_1k['result'].mean():.2%} (Mẫu: {len(ahead_1k):,} ván)")
print(f"Dẫn >= 2,000 vàng lúc 10p: Tỷ lệ thắng = {ahead_2k['result'].mean():.2%} (Mẫu: {len(ahead_2k):,} ván)")
print(f"Dẫn >= 3,000 vàng lúc 10p: Tỷ lệ thắng = {ahead_3k['result'].mean():.2%} (Mẫu: {len(ahead_3k):,} ván)")

top_picked_champs = df[df['position'] != 'team']['champion'].value_counts()[:5]
print(f"\n--- TOP 5 TƯỚNG ĐƯỢC CHỌN NHIỀU NHẤT ĐẤU GIẢI 2026 ---")
for champ, count in top_picked_champs.items():
    print(f" - {champ:15s}: {count:,} ván")
