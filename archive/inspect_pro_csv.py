import pandas as pd

file_path = "2026_LoL_esports_match_data_from_OraclesElixir.csv"
print(f"Loading first 1000 rows from {file_path}...")

df_sample = pd.read_csv(file_path, nrows=1000, low_memory=False)
print("Shape of sample:", df_sample.shape)
print("\n--- ALL COLUMNS (Total:", len(df_sample.columns), ") ---")
for i, col in enumerate(df_sample.columns):
    print(f"{i+1:3d}. {col}", end="  |  " if (i+1)%4 != 0 else "\n")
print("\n")

print("--- UNIQUE POSITIONS ---")
print(df_sample['position'].unique())

print("\n--- SAMPLE LEAGUES ---")
print(df_sample['league'].unique()[:10])

print("\n--- SAMPLE TEAMS ---")
print(df_sample['teamname'].dropna().unique()[:10])

# Check a single game structure
game_id = df_sample['gameid'].iloc[0]
single_game = df_sample[df_sample['gameid'] == game_id]
print(f"\n--- GAME STRUCTURE FOR gameid: {game_id} (Rows: {len(single_game)}) ---")
print(single_game[['side', 'position', 'playername', 'teamname', 'champion', 'result', 'goldat10', 'xpat10', 'csat10', 'golddiffat10']])

# Check total rows in file efficiently
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    total_lines = sum(1 for _ in f)
print(f"\nTotal lines in CSV: {total_lines:,} (approx {total_lines // 12:,} matches)")
