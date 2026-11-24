"""Chapter 6: numerical item profiles, implicit user profiles and cosine.

Profiles describe observed champion-role performance, NOT champion mechanics.
All aggregates/scaling bounds come from the supplied historical snapshot only.
This is aggregation and retrieval; no predictive model is trained.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis_data import DB_PATH, load_clean_tables
from historical_recommender import ALIASES, ROLES

FEATURES = ['dpm', 'cspm', 'wpm', 'damagetakenperminute', 'earnedgoldshare']


class ContentBasedRecommender:
    def __init__(self, db_path=DB_PATH, before=None, min_games=5, players=None):
        if min_games < 1:
            raise ValueError('min_games must be positive')
        self.before = before
        self.min_games = min_games
        self.players = (load_clean_tables(db_path)[2] if players is None else players).copy()
        required = ['gameid', 'date', 'league', 'position', 'champion', 'playername'] + FEATURES
        missing = set(required) - set(self.players.columns)
        if missing:
            raise ValueError(f'Missing content features: {sorted(missing)}')
        if before is not None:
            dates = pd.to_datetime(self.players.date, utc=True, errors='coerce')
            self.players = self.players[dates < pd.to_datetime(before, utc=True)].copy()
        self._catalogs = {}

    def catalog(self, lane, region='ALL'):
        role = ALIASES.get(lane.lower(), lane.lower())
        if role not in ROLES:
            raise ValueError('Unknown role')
        region = region.upper()
        key = role, region
        if key in self._catalogs:
            return self._catalogs[key]
        p = self.players[self.players.position.eq(role)].copy()
        leagues = {'LCP': ['LCP', 'VCS', 'PCS'],
                   'INTERNATIONAL': ['WLDS', 'MSI', 'EWC'],
                   'WORLDS': ['WLDS'], 'CKTG': ['WLDS']}.get(region, [region])
        if region != 'ALL':
            p = p[p.league.str.upper().isin(leagues)]
        # Missing measurements are not zeros. Deduplicate before counting games.
        measured = p.drop_duplicates(['gameid', 'position', 'champion', 'playername']).dropna(subset=FEATURES)
        measured = measured[np.isfinite(measured[FEATURES]).all(axis=1)
                            & (measured[FEATURES] >= 0).all(axis=1)]
        counts = measured.groupby('champion').size()
        raw = measured.groupby('champion')[FEATURES].mean()
        raw = raw.loc[counts.index[counts >= self.min_games]].sort_index()
        counts = counts.reindex(raw.index)
        lower, upper = raw.min(), raw.max()
        varying = (upper - lower) > 0
        features = list(raw.columns[varying])
        # Min-max normalization (Chapter 2), within role, historical data only.
        vectors = (raw[features] - lower[features]) / (upper[features] - lower[features])
        result = {'role': role, 'region': region, 'players': p,
                  'raw': raw, 'vectors': vectors, 'games': counts,
                  'feature_names': features,
                  'scaling_min': lower[features].to_dict(),
                  'scaling_max': upper[features].to_dict()}
        self._catalogs[key] = result
        return result

    def _rank(self, catalog, profile, excluded, top_k, profile_info):
        if top_k < 1:
            raise ValueError('top_k must be positive')
        base = {'method': 'content_based_cosine', 'score_kind': 'cosine_similarity_not_probability',
                'role': catalog['role'], 'region': catalog['region'],
                'feature_names': catalog['feature_names'], 'profile': profile_info,
                'historical_cutoff_exclusive': str(self.before) if self.before is not None else None,
                'probability': None, 'causal_uplift': None,
                'limitations': ['Measured performance depends on team, player, patch and opponent.',
                                'Pick frequency is implicit preference, not an explicit rating or proof of skill.',
                                'Similarity does not imply counter-pick, synergy or winrate improvement.']}
        if profile is None or len(profile) == 0 or np.linalg.norm(profile) == 0:
            return {**base, 'status': 'insufficient_profile', 'recommendations': []}
        frame = catalog['vectors']
        if frame.empty:
            return {**base, 'status': 'insufficient_catalog', 'recommendations': []}
        scores = cosine_similarity(np.asarray(profile).reshape(1, -1), frame.to_numpy())[0]
        rows = []
        for (champion, vector), score in zip(frame.iterrows(), scores):
            if champion in excluded or np.linalg.norm(vector.to_numpy()) == 0:
                continue
            rows.append({'champion': champion, 'cosine_similarity': float(np.clip(score, -1, 1)),
                         'score_kind': base['score_kind'], 'probability': None,
                         'profile_games': int(catalog['games'].loc[champion]),
                         'raw_item_profile': {k: float(v) for k, v in catalog['raw'].loc[champion].items()},
                         'normalized_item_profile': {k: float(v) for k, v in vector.items()}})
        rows.sort(key=lambda r: (-r['cosine_similarity'], r['champion']))
        return {**base, 'status': 'ok' if rows else 'no_candidates',
                'normalized_query_profile': dict(zip(catalog['feature_names'], map(float, profile))),
                'recommendations': rows[:top_k]}

    def recommend_similar(self, champion, lane, region='ALL', already_banned=None, top_k=5):
        catalog = self.catalog(lane, region)
        vector = catalog['vectors'].loc[champion].to_numpy() if champion in catalog['vectors'].index else None
        info = {'kind': 'seed_item_profile', 'champion': champion,
                'games': int(catalog['games'].get(champion, 0))}
        return self._rank(catalog, vector, set(already_banned or []) | {champion}, top_k, info)

    def recommend_for_player(self, player_name, lane, region='ALL', already_banned=None,
                             top_k=5, exclude_seen=False):
        catalog = self.catalog(lane, region)
        own = catalog['players'][catalog['players'].playername.eq(player_name)]
        counts = own.drop_duplicates(['gameid', 'champion']).groupby('champion').size()
        known = counts.reindex(catalog['vectors'].index, fill_value=0)
        if known.sum() and len(catalog['feature_names']):
            profile = np.average(catalog['vectors'].to_numpy(), axis=0, weights=known.to_numpy())
        else:
            profile = None
        info = {'kind': 'weighted_mean_item_profiles', 'player': player_name,
                'weight_kind': 'historical_pick_count_implicit_preference',
                'history_games': int(counts.sum()), 'represented_games': int(known.sum()),
                'item_weights': {c: int(n) for c, n in known.items() if n > 0}}
        excluded = set(already_banned or []) | (set(counts.index) if exclude_seen else set())
        return self._rank(catalog, profile, excluded, top_k, info)
