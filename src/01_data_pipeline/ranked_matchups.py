"""Separate, observational ranked matchup data. Never writes the canonical DB.

Raw responses stay in ignored data/raw; analytical exports contain no PUUIDs.
No ranked signal is consumed by the draft advisor in this implementation.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from numbers import Real
from pathlib import Path
import re
import sys
import time

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'src/07_recommender')]
from analysis_data import load_clean_tables
from historical_recommender import wilson
from draft_meta import patch_code

ROLES = {'TOP': 'top', 'JUNGLE': 'jng', 'MIDDLE': 'mid',
         'BOTTOM': 'bot', 'UTILITY': 'sup'}
KEYS = ['patch', 'role', 'champion', 'opponent']
METRICS = [f'{m}_diff_{minute}' for minute in (10, 15) for m in ('gold', 'xp', 'cs')]
COLUMNS = ['match_id', 'played_at', 'ended_at', 'platform', 'queue', 'game_version',
           'patch', 'role', 'champion', 'opponent', 'team_id', 'win',
           'frame_ms_10', 'frame_ms_15'] + METRICS


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    temporary.replace(path)


class RiotError(RuntimeError):
    """Sanitized errors: never include request headers or player identifiers."""
    def __init__(self, message, status_code=None, reason_code='riot_request_failed'):
        super().__init__(message)
        self.status_code = status_code
        self.reason_code = reason_code


class RiotClient:
    def __init__(self, key, session=None, sleep=time.sleep, min_interval=0, max_requests=None, deadline=None):
        if not key:
            raise RiotError('RIOT_API_KEY chưa được cấu hình.')
        self.session = session or requests.Session()
        self.session.headers.update({'X-Riot-Token': key})
        self.sleep = sleep
        self.min_interval = min_interval
        self.last_request = None
        self.max_requests = max_requests
        self.request_attempts = 0
        self.deadline = deadline

    def get(self, host, path, params=None):
        # Host supplied only from validated CLI routing values, not arbitrary URLs.
        for attempt in range(3):
            if self.deadline is not None and time.monotonic() >= self.deadline:
                raise RiotError('Đã hết thời gian phiên; lưu tiến độ và dừng.', reason_code='session_time_limit')
            if self.max_requests is not None and self.request_attempts >= self.max_requests:
                raise RiotError('Đã chạm ngân sách request; lưu tiến độ và dừng.', reason_code='request_budget_exhausted')
            if self.last_request is not None and self.min_interval:
                self.sleep(max(0, self.min_interval - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            self.request_attempts += 1
            try:
                response = self.session.get(f'https://{host}.api.riotgames.com{path}',
                                            params=params, timeout=25, allow_redirects=False)
            except requests.RequestException:
                if attempt == 2:
                    raise RiotError('Không kết nối được Riot sau 3 lần thử.') from None
                self.sleep(2 ** attempt)
                continue
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    raise RiotError('Riot trả JSON không hợp lệ.') from None
            if response.status_code in (401, 403):
                raise RiotError(f'Riot HTTP {response.status_code}: kiểm tra khóa/quyền API.', response.status_code)
            if response.status_code == 429:
                try:
                    delay = float(response.headers.get('Retry-After', '1'))
                except ValueError:
                    raise RiotError('Riot HTTP 429: Retry-After không hợp lệ.', 429) from None
                # Stop instead of retrying earlier than Riot permits or waiting unboundedly.
                if not math.isfinite(delay) or delay < 0 or delay > 30 or attempt == 2:
                    raise RiotError('Riot HTTP 429: dừng; chạy lại sau Retry-After.', 429)
                self.sleep(delay)
            elif response.status_code >= 500 and attempt < 2:
                self.sleep(2 ** attempt)
            else:
                raise RiotError(f'Riot HTTP {response.status_code}: dừng request.', response.status_code)
        raise RiotError('Hết số lần thử Riot.')


def numeric(value):
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)


def extract_match(detail, timeline, frame_policy='before', catalog=None):
    """Ten directed observations; roles reported post-game, not draft intent.

    A missing/duplicate role invalidates the match. No interpolation.
    before: no future frame; nearest: descriptive-only, within +/-1000ms.
    CS is lane minions + jungle minions, reported explicitly in documentation.
    """
    mid = detail.get('metadata', {}).get('matchId')
    if not mid or timeline.get('metadata', {}).get('matchId') != mid:
        raise ValueError('match_timeline_id_mismatch')
    info = detail.get('info', {})
    if info.get('queueId') != 420 or info.get('mapId') != 11:
        raise ValueError('not_solo_ranked_summoners_rift')
    if info.get('gameDuration', 0) < 600:
        raise ValueError('shorter_than_10_minutes')
    start = info.get('gameStartTimestamp')
    if not numeric(start) or start <= 0:
        raise ValueError('missing_game_start')
    version = info.get('gameVersion', '')
    match = re.match(r'^(\d+)\.(\d+)\.', version)
    if not match:
        raise ValueError('missing_game_version')
    patch = f'{int(match[1])}.{int(match[2]):02d}'
    participants = info.get('participants', [])
    teams, ids = {}, set()
    if len(participants) != 10:
        raise ValueError('not_ten_participants')
    for p in participants:
        team, role, pid = p.get('teamId'), ROLES.get(p.get('teamPosition')), p.get('participantId')
        if team not in (100, 200) or role is None or pid not in range(1, 11) or pid in ids:
            raise ValueError('ambiguous_team_role_or_participant')
        if not p.get('championName') or not isinstance(p.get('win'), bool):
            raise ValueError('missing_champion_or_result')
        ids.add(pid)
        if role in teams.setdefault(team, {}):
            raise ValueError('duplicate_role')
        teams[team][role] = p
    if any(set(teams.get(t, {})) != set(ROLES.values()) for t in (100, 200)):
        raise ValueError('incomplete_roles')
    wins = [{p['win'] for p in teams[t].values()} for t in (100, 200)]
    if len(wins[0]) != 1 or len(wins[1]) != 1 or wins[0] == wins[1]:
        raise ValueError('inconsistent_team_result')
    frames = timeline.get('info', {}).get('frames', [])
    snapshots = {}
    for minute in (10, 15):
        target = minute * 60000
        if frame_policy not in ('before', 'nearest'):
            raise ValueError('unknown_frame_policy')
        eligible = [f for f in frames if numeric(f.get('timestamp'))
                    and abs(target - f['timestamp']) <= 1000
                    and (frame_policy == 'nearest' or f['timestamp'] <= target)]
        snapshots[minute] = min(eligible, key=lambda f: (abs(target - f['timestamp']), f['timestamp'])) if eligible and info['gameDuration'] >= minute * 60 else None
    rows = []
    for team in (100, 200):
        for role, p in teams[team].items():
            enemy = teams[300 - team][role]
            row = dict(match_id=mid, played_at=datetime.fromtimestamp(start / 1000, timezone.utc).isoformat(),
                       ended_at=datetime.fromtimestamp(max(start + info['gameDuration'] * 1000,
                           info.get('gameEndTimestamp') or 0) / 1000, timezone.utc).isoformat(),
                       platform=mid.split('_')[0], queue=420, game_version=version, patch=patch,
                       role=role, champion=catalog.name(p['championName'], p.get('championId')) if catalog else p['championName'],
                       opponent=catalog.name(enemy['championName'], enemy.get('championId')) if catalog else enemy['championName'],
                       team_id=team, win=int(p['win']))
            for minute, frame in snapshots.items():
                row[f'frame_ms_{minute}'] = frame['timestamp'] if frame else None
                pf = frame.get('participantFrames', {}) if frame else {}
                own, other = pf.get(str(p['participantId']), {}), pf.get(str(enemy['participantId']), {})
                for metric, fields in [('gold', ['totalGold']), ('xp', ['xp']),
                                       ('cs', ['minionsKilled', 'jungleMinionsKilled'])]:
                    values = [x.get(k) for x in (own, other) for k in fields]
                    row[f'{metric}_diff_{minute}'] = (sum(own[k] for k in fields) - sum(other[k] for k in fields)
                        if all(numeric(v) and v >= 0 for v in values) else None)
            rows.append(row)
    return rows


def collect(args):
    from config.settings import RIOT_API_KEY, SERVER_METADATA
    client = RiotClient(RIOT_API_KEY, min_interval=1.3)
    region = args.routing or SERVER_METADATA[args.platform]['region']
    ids = list(dict.fromkeys(args.match_id or []))
    seed_count = 0
    seed_counts = []
    if not ids:
        league = client.get(args.platform, '/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5')
        for entry in league.get('entries', [])[:args.seed_players]:
            puuid = entry.get('puuid')
            if not puuid:
                continue  # Never guess IDs/roles; explicit IDs also supported.
            seed_count += 1
            params = {'queue': 420, 'type': 'ranked', 'start': 0,
                      'count': min(args.matches_per_seed, args.limit)}
            if args.start_time:
                params['startTime'] = int(pd.to_datetime(args.start_time, utc=True).timestamp())
            if args.end_time:
                params['endTime'] = int(pd.to_datetime(args.end_time, utc=True).timestamp())
            batch = client.get(region, f'/lol/match/v5/matches/by-puuid/{puuid}/ids', params)
            seed_counts.append({'seed_index': seed_count, 'returned_ids': len(batch)})
            ids = list(dict.fromkeys(ids + batch))
            if len(ids) >= args.limit:
                break
    if not ids:
        raise RiotError('Không tìm thấy match ID; có thể dùng --match-id.')
    args.cache.mkdir(parents=True, exist_ok=True)
    manifest = {'fetched_at': datetime.now(timezone.utc).isoformat(), 'platform': args.platform,
                'routing': region, 'seed_method': 'explicit_ids' if args.match_id else 'challenger_list_at_fetch',
                'seed_players_used': seed_count, 'seed_counts': seed_counts,
                'query_start': args.start_time, 'query_end': args.end_time,
                'matches_per_seed': args.matches_per_seed,
                'rank_at_match': 'unknown', 'matches': [], 'errors': []}
    try:
        for mid in ids[:args.limit]:
            if not re.fullmatch(r'[A-Z0-9]+_\d+', mid) or mid.split('_')[0].lower() != args.platform:
                raise RiotError('Match ID không hợp lệ hoặc khác platform.')
            for kind, suffix in [('match', ''), ('timeline', '/timeline')]:
                path = args.cache / f'{mid}.{kind}.json'
                if not path.exists():
                    response = client.get(region, f'/lol/match/v5/matches/{mid}{suffix}')
                    if response.get('metadata', {}).get('matchId') != mid:
                        raise RiotError('ID response không khớp ID request.')
                    write_json(path, response)
                    write_json(args.cache / f'{mid}.{kind}.provenance.json',
                               {'fetched_at': datetime.now(timezone.utc).isoformat(), 'routing': region,
                                'endpoint_kind': kind, 'match_id': mid})
            manifest['matches'].append(mid)
    except RiotError as exc:
        manifest['errors'].append(str(exc))
        raise
    finally:
        write_json(args.cache / 'collection_manifest.json', manifest)


def load_rank(cache, frame_policy='before', catalog=None):
    rows, rejected = [], []
    for path in sorted(Path(cache).glob('*.match.json')):
        mid = path.name.removesuffix('.match.json')
        try:
            rows.extend(extract_match(json.loads(path.read_text(encoding='utf-8')),
                       json.loads((Path(cache) / f'{mid}.timeline.json').read_text(encoding='utf-8')), frame_policy, catalog))
        except (ValueError, KeyError, TypeError, OSError) as exc:
            rejected.append({'match_id': mid, 'reason': str(exc) if isinstance(exc, ValueError) else type(exc).__name__})
    return pd.DataFrame(rows, columns=COLUMNS).drop_duplicates(['match_id', 'team_id', 'role']), rejected


def pro_observations(players):
    rows = []
    for mid, game in players.groupby('gameid'):
        if len(game) != 10 or set(game.side) != {'Blue', 'Red'}:
            continue
        teams = {s: game[game.side.eq(s)] for s in ('Blue', 'Red')}
        if any(len(t) != 5 or set(t.position) != set(ROLES.values()) for t in teams.values()):
            continue
        if any(t.result.nunique() != 1 for t in teams.values()) or sum(t.result.iloc[0] for t in teams.values()) != 1:
            continue
        for _, p in game.iterrows():
            enemy = game[game.side.ne(p.side) & game.position.eq(p.position)].iloc[0]
            row = dict(match_id=mid, played_at=p.date, platform=p.league, queue='pro',
                       patch=patch_code(p.patch), role=p.position, champion=p.champion,
                       opponent=enemy.champion, team_id=p.side, win=int(p.result))
            for minute in (10, 15):
                for metric, field in [('gold', 'gold'), ('xp', 'xp'), ('cs', 'cs')]:
                    a, b = p.get(f'{field}at{minute}'), enemy.get(f'{field}at{minute}')
                    row[f'{metric}_diff_{minute}'] = (float(a - b) if p.datacompleteness == 'complete'
                        and enemy.datacompleteness == 'complete' and numeric(a) and numeric(b)
                        and a >= 0 and b >= 0 and p.gamelength >= minute * 60 else None)
            rows.append(row)
    return pd.DataFrame(rows, columns=COLUMNS)


def summarize(rows, scope):
    columns = scope + KEYS + ['games', 'wins', 'winrate', 'ci95_low', 'ci95_high']
    columns += [f'{m}_{s}' for m in METRICS for s in ('n', 'mean', 'sd')]
    results = []
    # One row per match/team/role, counts are per directed matchup, never 10 independent wins per game.
    for keys, group in rows.groupby(scope + KEYS, dropna=False):
        n, wins = group.match_id.nunique(), int(group.win.sum())
        row = dict(zip(scope + KEYS, keys))
        lo, hi = wilson(wins, n)
        row.update(games=n, wins=wins, winrate=wins / n, ci95_low=lo, ci95_high=hi)
        for m in METRICS:
            values = group[m].dropna()
            row.update({f'{m}_n': len(values), f'{m}_mean': values.mean(), f'{m}_sd': values.std(ddof=1)})
        results.append(row)
    return pd.DataFrame(results, columns=columns)


def report(args):
    catalog = None
    if args.catalog:
        from rank_data_contract import ChampionCatalog, normalize_observations
        catalog = ChampionCatalog.read(args.catalog)
    rank, rejected = load_rank(args.cache, args.frame_policy, catalog)
    _, _, players = load_clean_tables()
    leagues = players.league.astype(str).str.upper()
    if args.pro_league.upper() not in set(leagues):
        raise RiotError('Không tìm thấy league giải trong dữ liệu sạch.')
    players = players[leagues.eq(args.pro_league.upper())].copy()
    if args.as_of:
        cutoff = pd.to_datetime(args.as_of, utc=True)
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', args.as_of):
            cutoff += pd.Timedelta(days=1) - pd.Timedelta(nanoseconds=1)
        rank = rank[pd.to_datetime(rank.played_at, utc=True, errors='coerce') <= cutoff]
        players = players[pd.to_datetime(players.date, utc=True, errors='coerce') <= cutoff]
    if args.patch:
        rank = rank[rank.patch.eq(args.patch)]
        players = players[players.patch.map(patch_code).eq(args.patch)]
    pro = pro_observations(players)
    if catalog:
        pro, name_audit = normalize_observations(pro, catalog)
        write_json(args.output / 'name_normalization.json', {'catalog_version': catalog.version, 'pro_names': name_audit})
    rs, ps = summarize(rank, ['platform', 'queue']), summarize(pro, ['platform', 'queue'])
    # Preserve scope columns on both sides; match only equal raw major.minor patch identifiers.
    comparison = rs.merge(ps, on=KEYS, how='inner', suffixes=('_rank', '_pro'))
    args.output.mkdir(parents=True, exist_ok=True)
    for name, table in [('rank_observations', rank), ('pro_observations', pro),
                        ('rank_matchups', rs), ('pro_matchups', ps), ('rank_pro_same_patch', comparison)]:
        table.to_csv(args.output / f'{name}.csv', index=False, encoding='utf-8-sig')
    summary = {'schema': 'rank-matchups-v2-ended-catalog', 'rank_games': int(rank.match_id.nunique()),
               'rank_rows': len(rank), 'pro_games': int(pro.match_id.nunique()), 'pro_rows': len(pro),
               'rank_patches': sorted(rank.patch.unique()), 'pro_patches': sorted(pro.patch.unique()),
               'same_patch_directed_pairs': len(comparison), 'rejected': rejected,
               'rank_metric_coverage': {m: int(rank[m].notna().sum()) for m in METRICS},
               'pro_metric_coverage': {m: int(pro[m].notna().sum()) for m in METRICS},
               'scope': {'pro_league': args.pro_league, 'as_of': args.as_of, 'patch': args.patch},
               'normalization_catalog_version': catalog.version if catalog else None,
               'observed_dates': {name: {'first': str(df.played_at.min()) if len(df) else None,
                                         'last': str(df.played_at.max()) if len(df) else None}
                                  for name, df in [('rank', rank), ('pro', pro)]},
               'raw_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                              for pattern in ('*.match.json', '*.timeline.json')
                              for p in sorted(args.cache.glob(pattern))},
               'contextual_uses_rank_signal': False, 'rank_at_match': 'unknown',
               'frame_policy': args.frame_policy, 'frame_tolerance_ms': 1000,
               'rank_frame_offsets_ms': {str(m): sorted((rank[f'frame_ms_{m}'].dropna() - m * 60000).unique().tolist()) for m in (10, 15)},
               'role_policy': 'reported post-game teamPosition; reject missing/duplicate roles'}
    write_json(args.output / 'summary.json', summary)
    lines = ['# Đối chiếu Rank / Pro — thống kê mô tả riêng', '',
             f"Rank: {summary['rank_games']} trận / {len(rank)} dòng; Pro ({args.pro_league}): {summary['pro_games']} trận / {len(pro)} dòng.",
             f"Patch Rank: {', '.join(summary['rank_patches']) or 'chưa có'}; Pro: {', '.join(summary['pro_patches']) or 'chưa có'}.",
             f"Cặp có cùng patch/role/tướng/đối thủ: {len(comparison)} dòng (mỗi platform giữ riêng).", '',
             '- Các CSV rank_matchups/pro_matchups ghi số trận, kết quả thắng cả đội, Wilson CI95 và n/mean/SD của chênh lệch vàng/XP/CS phút10/15.',
             '- rank_pro_same_patch.csv chỉ ghép mã patch major.minor trùng chính xác; không cộng số mẫu hai miền hoặc tự đổi phiên bản.',
             '- CS Rank = lính đường + quái rừng; CS Pro là total CS do nguồn cung cấp, cần kiểm tra tương thích trước khi dùng làm feature chung.',
             f'- Frame policy: {args.frame_policy}; chỉ nhận frame cách mốc tối đa1000ms. before: không sau mốc; nearest: có thể sau mốc, CHỈ thống kê mô tả, không dùng làm đầu vào dự báo đúng phút10/15. frame_ms ghi thời điểm thật; không nội suy.',
             '- Missing để trống; không dùng frame phút9 thay phút10, không giả lập chỉ số theo đường.',
             '- Role là phân loại sau trận của Riot, không xác nhận đi đường cả trận hay thứ tự draft. Pro cũng dùng role sau trận.',
             '- Seed Thách Đấu là cách lấy mẫu hiện tại, không chứng minh rank lịch sử của10người. Chưa thu rank cá nhân; không có phân tầng rank.',
             '- Hai hướng A→B/B→A trong cùng trận có liên hệ; Wilson giả định trận độc lập, cùng người chơi tái xuất làm CI lạc quan.',
             '- Chưa cân bằng trình độ/người chơi, phe, jungle/support, patch drift hoặc sửa sai số chọn mẫu; chưa chứng minh counter/cơ chế hoặc tăng thắng.',
             '- Contextual/legacy chưa đọc tín hiệu Rank. Chưa benchmark Pro-only/Rank-only/hybrid, chưa có quyết định trộn miền.', '',
             (f'- Tên tướng đã chuẩn hóa bằng ID/alias chính thức Data Dragon {catalog.version}; tên không xác nhận bị loại hoặc gây lỗi, không fuzzy-match.' if catalog else
              '- Chưa bật catalog: ghép đúng chuỗi tên; alias khác nhau có thể bỏ sót cặp. Dùng --catalog để chuẩn hóa.'),
             f"Số cache bị loại: {len(rejected)}. Xem summary.json để biết coverage và lý do.", '',
             'Nguồn kỹ thuật: [Riot LoL](https://developer.riotgames.com/docs/lol), [Match-v5](https://developer.riotgames.com/apis#match-v5/GET_getMatch), [HTTP/rate limits](https://developer.riotgames.com/docs/portal).']
    (args.output / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({k: summary[k] for k in ('rank_games', 'pro_games', 'same_patch_directed_pairs')}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collect', action='store_true', help='Gọi Riot; mặc định chỉ đọc cache offline.')
    parser.add_argument('--platform', choices=['kr', 'vn2', 'tw2', 'na1', 'euw1'], default='kr')
    parser.add_argument('--routing', choices=['asia', 'sea', 'americas', 'europe'])
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--seed-players', type=int, default=3)
    parser.add_argument('--matches-per-seed', type=int, default=5)
    parser.add_argument('--start-time', help='UTC timestamp/range start for ranked match-list query.')
    parser.add_argument('--end-time', help='UTC timestamp/range end; independently recheck event time in evaluation.')
    parser.add_argument('--catalog', type=Path, help='Pinned official Data Dragon champion.json.')
    parser.add_argument('--match-id', action='append')
    parser.add_argument('--cache', type=Path, default=ROOT / 'data/raw/riot_matchups')
    parser.add_argument('--output', type=Path, default=ROOT / 'reports/rank_pro_matchups')
    parser.add_argument('--pro-league', default='WLDS')
    parser.add_argument('--as-of')
    parser.add_argument('--patch', help='Mã dữ liệu major.minor, ví dụ16.20; lọc cả hai miền.')
    parser.add_argument('--frame-policy', choices=['before', 'nearest'], default='before',
                        help='before: không sau mốc; nearest: thống kê mô tả +/-1000ms, cấm dùng cho dự báo đúng mốc.')
    args = parser.parse_args()
    if not 1 <= args.limit <= 100 or not 1 <= args.seed_players <= 20:
        parser.error('limit phải1..100, seed-players phải1..20')
    if not 1 <= args.matches_per_seed <= 100:
        parser.error('matches-per-seed phải1..100')
    try:
        if args.collect:
            collect(args)
        report(args)
    except RiotError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
