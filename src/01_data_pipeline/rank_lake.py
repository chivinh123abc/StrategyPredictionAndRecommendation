"""Private incremental evidence DB. Canonical lol_live_data.db is never opened."""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sqlite3
import time

from ranked_matchups import ROOT


@contextmanager
def exclusive_writer(db_path):
    path = Path(db_path).with_suffix('.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            try: msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError: raise RuntimeError('Another updater is using this evidence DB') from None
        else:
            import fcntl
            try: fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError: raise RuntimeError('Another updater is using this evidence DB') from None
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt': msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else: fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class RankLake:
    def __init__(self, path, policy):
        path = Path(path).resolve()
        if path == (ROOT / 'data/database/lol_live_data.db').resolve():
            raise ValueError('Refusing canonical DB as evidence-store destination')
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS seeds(platform TEXT,puuid TEXT,tier TEXT,source TEXT,
          observed_at TEXT,last_polled REAL DEFAULT 0,page_start INTEGER DEFAULT 0,
          PRIMARY KEY(platform,puuid));
        CREATE TABLE IF NOT EXISTS jobs(match_id TEXT PRIMARY KEY,platform TEXT,routing TEXT,
          status TEXT NOT NULL DEFAULT 'pending',detail_path TEXT,timeline_path TEXT,
          detail_fetched_at TEXT,classification_json TEXT,evidence_json TEXT,available_at TEXT,updated_at REAL,
          next_attempt REAL NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS snapshots(platform TEXT,puuid TEXT,observed_at TEXT,
          record_json TEXT NOT NULL,PRIMARY KEY(platform,puuid));
        CREATE TABLE IF NOT EXISTS observations(match_id TEXT,team_id INTEGER,role TEXT,
          platform TEXT,queue INTEGER,patch TEXT,tier_floor TEXT,champion_id INTEGER,
          opponent_id INTEGER,puuid TEXT,opponent_puuid TEXT,row_json TEXT NOT NULL,
          PRIMARY KEY(match_id,team_id,role),FOREIGN KEY(match_id) REFERENCES jobs(match_id));
        CREATE TABLE IF NOT EXISTS sessions(session_id TEXT PRIMARY KEY,started_at TEXT,
          finished_at TEXT,status TEXT,http_attempts INTEGER DEFAULT 0,detail_json TEXT);
        CREATE INDEX IF NOT EXISTS jobs_status ON jobs(status,next_attempt);
        CREATE INDEX IF NOT EXISTS seeds_poll ON seeds(last_polled,platform,tier);
        CREATE INDEX IF NOT EXISTS observations_matchup ON observations(platform,queue,patch,role,champion_id,opponent_id);
        ''')
        fingerprint = json.dumps({'floor':policy['pro']['rank_tier_floor'], **policy['snapshot_collection']}, sort_keys=True)
        old = self.meta('cohort_policy')
        if old and old != fingerprint:
            self.db.close()
            raise ValueError('Cohort policy changed: use a separate evidence DB; do not mix thresholds')
        version=self.meta('schema_version')
        if version not in (None,'rank-lake-v1'):
            self.db.close()
            raise ValueError('Unsupported evidence DB schema version')
        self.set_meta('schema_version','rank-lake-v1')
        self.set_meta('cohort_policy', fingerprint)

    def close(self): self.db.close()

    def meta(self, key):
        row = self.db.execute('SELECT value FROM metadata WHERE key=?',(key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key, value):
        with self.db: self.db.execute('INSERT OR REPLACE INTO metadata VALUES(?,?)',(key,value))

    def add_seed(self, platform, puuid, tier, source, observed_at):
        with self.db:
            self.db.execute('''INSERT INTO seeds(platform,puuid,tier,source,observed_at) VALUES(?,?,?,?,?)
              ON CONFLICT(platform,puuid) DO UPDATE SET tier=excluded.tier,source=excluded.source,observed_at=excluded.observed_at''',
              (platform.lower(),puuid,tier,source,observed_at))

    def enqueue(self, mid, platform, routing):
        with self.db:
            return self.db.execute('INSERT OR IGNORE INTO jobs(match_id,platform,routing,updated_at) VALUES(?,?,?,?)',
                (mid,platform.lower(),routing,time.time())).rowcount

    def cache_snapshot(self, record):
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO snapshots VALUES(?,?,?,?)',
                (record['platform'].lower(),record['puuid'],record['observed_at'],json.dumps(record)))

    def snapshot(self, platform, puuid):
        row = self.db.execute('SELECT record_json FROM snapshots WHERE platform=? AND puuid=?',
                              (platform.lower(),puuid)).fetchone()
        return json.loads(row[0]) if row else None

    def counts(self):
        counts = dict(self.db.execute('SELECT status,COUNT(*) FROM jobs GROUP BY status').fetchall())
        counts.update(accepted_observations=self.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0],
                      seeds=self.db.execute('SELECT COUNT(*) FROM seeds').fetchone()[0])
        return counts

    def persist_result(self, mid, classification, available_at, observations):
        with self.db:
            self.db.execute('''UPDATE jobs SET status=?,classification_json=?,available_at=?,updated_at=?,next_attempt=? WHERE match_id=?''',
                (classification['status'],json.dumps(classification),available_at,time.time(),
                 time.time()+300 if classification['status']=='missing' else 0,mid))
            if observations:
                if len(observations)!=10 or len({(r['team_id'],r['role']) for r in observations})!=10:
                    raise ValueError('Atomic ingestion requires ten unique team-role rows')
                for r in observations:
                    self.db.execute('INSERT OR IGNORE INTO observations VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                        (mid,r['team_id'],r['role'],r['platform'],r['queue'],r['patch'],r['tier_floor'],
                         r['champion_id'],r['opponent_id'],r['_puuid'],r['_enemy_puuid'],json.dumps(r)))


def import_snapshot_runs(lake, public_root, private_root, policy):
    from rank_coverage import load_cohort, observations
    selected, _, _, _ = load_cohort(public_root, private_root, policy)
    frame, games = observations(selected)
    # NaN values in missing timeline fields become JSON null, never invented zeros.
    frame = frame.astype(object).where(frame.notna(), None)
    added = 0
    for mid, item in selected.items():
        created = lake.enqueue(mid,item['scope'][0],
                               {'KR':'asia','EUW1':'europe','NA1':'americas','VN2':'sea','TW2':'sea'}[item['scope'][0]])
        if not created and lake.db.execute('SELECT COUNT(*) FROM observations WHERE match_id=?',(mid,)).fetchone()[0]:
            continue
        private = item['private']
        with lake.db:
            lake.db.execute('UPDATE jobs SET detail_path=?,timeline_path=?,detail_fetched_at=? WHERE match_id=?',
                (str(private/f'{mid}.match.json'),str(private/f'{mid}.timeline.json'),item['available_at'],mid))
        saved = next(r for r in json.loads((public_root/item['run_id']/'matches.json').read_text(encoding='utf-8')) if r['match_id']==mid)
        records = frame[frame.match_id.eq(mid)].to_dict('records')
        lake.persist_result(mid,saved,item['available_at'],records)
        added += 1
        for p in item['detail']['info']['participants']:
            snap = item['snapshots'][(item['scope'][0],p['puuid'])]
            lake.add_seed(item['scope'][0],p['puuid'],snap['tier'],'imported_accepted_participant',snap['observed_at'])
    return added
