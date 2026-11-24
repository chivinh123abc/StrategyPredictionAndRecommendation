"""Canonical domain cleaning shared by exports, statistics and ML.

No distribution fitted on the full dataset, no trimming of valid snowball games.
Raw SQLite is never modified. Missing measurements remain missing.
"""
from functools import lru_cache
from contextlib import closing
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / 'data/database/lol_live_data.db'
POLICY_VERSION = 'domain-v2-signed-no-trimming'


def clean_ranked(df):
    df = df.drop_duplicates('gameId').copy()
    required = ['blueTotalGold', 'redTotalGold', 'blueTotalExperience',
                'redTotalExperience', 'blueKills', 'redKills', 'blueDeaths', 'redDeaths',
                'blueTotalMinionsKilled', 'redTotalMinionsKilled',
                'blueTotalJungleMinionsKilled', 'redTotalJungleMinionsKilled']
    df = df.dropna(subset=required + ['blueWins', 'gameDuration'])
    df = df[(df.gameDuration >= 600) & df.blueWins.isin([0, 1])
            & (df[required] >= 0).all(axis=1) & np.isfinite(df[required]).all(axis=1)].copy()
    for metric, total in [('Gold', 'TotalGold'), ('Experience', 'TotalExperience')]:
        df['blue' + metric + 'Diff'] = df['blue' + total] - df['red' + total]
        df['red' + metric + 'Diff'] = -df['blue' + metric + 'Diff']
    return df.reset_index(drop=True)


def clean_matches(df):
    df = df.drop_duplicates(['gameid', 'side']).copy()
    df = df[(df.gamelength >= 600) & df.result.isin([0, 1]) & df.side.isin(['Blue', 'Red'])].copy()
    groups = df.groupby('gameid').agg(n=('side', 'size'), wins=('result', 'sum'))
    df = df[df.gameid.isin(groups.index[(groups.n == 2) & (groups.wins == 1)])].copy()
    for col in ['ban1', 'ban2', 'ban3', 'ban4', 'ban5']:
        if col in df: df[col] = df[col].fillna('NoBan')
    return df.reset_index(drop=True)


def complete_10min(df):
    cols = ['golddiffat10', 'xpdiffat10', 'csdiffat10', 'killsat10', 'deathsat10']
    rows = df[df.datacompleteness.eq('complete')].dropna(subset=cols).copy()
    rows = rows[np.isfinite(rows[cols]).all(axis=1)
                & (rows[['killsat10','deathsat10']] >= 0).all(axis=1)]
    # Keep both sides together; incomplete opposing measurements are not imputed.
    n = rows.groupby('gameid').size()
    return rows[rows.gameid.isin(n.index[n == 2])].reset_index(drop=True)


def clean_players(df, matches=None):
    df = df.drop_duplicates(['gameid', 'participantid']).copy()
    df = df[df.champion.notna() & df.result.isin([0, 1]) & (df.gamelength >= 600)
            & df.position.isin(['top', 'jng', 'mid', 'bot', 'sup'])].copy()
    if matches is not None:
        valid = pd.MultiIndex.from_frame(matches[['gameid', 'side']])
        df = df[pd.MultiIndex.from_frame(df[['gameid', 'side']]).isin(valid)].copy()
    if 'playername' in df: df['playername'] = df.playername.fillna('Unknown')
    return df.reset_index(drop=True)


@lru_cache(maxsize=4)
def _cached_tables(path, mtime, size):
    with closing(sqlite3.connect(Path(path).as_uri() + '?mode=ro', uri=True)) as c:
        rank = clean_ranked(pd.read_sql_query('SELECT * FROM matches_10min', c))
        matches = clean_matches(pd.read_sql_query('SELECT * FROM tournament_matches', c))
        players = clean_players(pd.read_sql_query('SELECT * FROM tournament_players', c), matches)
    return rank, matches, players


def load_clean_tables(db_path=DB_PATH):
    path = Path(db_path).resolve()
    stat = path.stat()
    return tuple(df.copy() for df in _cached_tables(str(path), stat.st_mtime_ns, stat.st_size))


def open_clean_connection(db_path=DB_PATH):
    """SQL-compatible cleaned snapshot, including original columns for EDA."""
    conn = sqlite3.connect(':memory:')
    tables = load_clean_tables(db_path)
    for name, frame in zip(['matches_10min', 'tournament_matches', 'tournament_players'], tables):
        frame.to_sql(name, conn, index=False)
    complete_10min(tables[1]).to_sql('tournament_matches_10min', conn, index=False)
    conn.execute('CREATE INDEX match_side ON tournament_matches(gameid,side)')
    conn.execute('CREATE INDEX player_role ON tournament_players(gameid,side,position)')
    return conn
