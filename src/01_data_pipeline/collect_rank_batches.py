"""Bounded sequential collection campaign: distinct seed slices and seen-match dedup."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from types import SimpleNamespace

from collect_rank_snapshots import collect_run
from ranked_matchups import RiotClient, ROOT, write_json
from rank_eligibility import read_policy


def seen_matches(output):
    ids = set()
    for path in output.glob('*/matches.json'):
        rows = json.loads(path.read_text(encoding='utf-8'))
        ids.update(r['match_id'] for r in rows if r['status'] in ('accepted', 'rejected'))
    return ids


def campaign(args, client):
    defaults = read_policy(args.policy)['snapshot_collection']
    seen, seed_registry, runs = seen_matches(args.output), set(), []
    campaign_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    destination = args.output / 'campaigns' / f'{campaign_id}.json'
    for index in range(args.batches):
        print(f'Batch {index+1}/{args.batches}; HTTP attempts used {client.request_attempts}/{client.max_requests}', flush=True)
        options = SimpleNamespace(policy=args.policy, cache=args.cache, output=args.output,
            match_id=None, limit=args.matches_per_batch, seed_players=args.seeds_per_batch,
            matches_per_seed=1, platform=args.platform, routing=args.routing,
            seed_offset=args.seed_offset + index * args.seeds_per_batch,
            max_match_age_hours=defaults['max_match_age_hours'], max_snapshot_spread_minutes=defaults['max_snapshot_spread_minutes'],
            exclude_match_ids=set(seen), seed_registry=seed_registry)
        summary, matches = collect_run(options, client)
        seen.update(r['match_id'] for r in matches if r['status'] in ('accepted', 'rejected'))
        runs.append(summary)
        write_json(destination, {'campaign_id': campaign_id, 'request_budget': client.max_requests,
            'http_attempts': client.request_attempts, 'unique_seed_players': len(seed_registry), 'runs': runs})
        if summary['collection_status'] != 'complete':
            break
    print(json.dumps({'campaign_id': campaign_id, 'batches_completed': len(runs), 'http_attempts': client.request_attempts,
                      'accepted_games': sum(r['accepted_games'] for r in runs)}, ensure_ascii=False), flush=True)
    return runs


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--batches', type=int, default=3)
    p.add_argument('--matches-per-batch', type=int, default=5)
    p.add_argument('--seeds-per-batch', type=int, default=5)
    p.add_argument('--seed-offset', type=int, default=5)
    p.add_argument('--request-budget', type=int, default=200)
    p.add_argument('--platform', choices=['kr', 'vn2', 'tw2', 'na1', 'euw1'], default='kr')
    p.add_argument('--routing', choices=['asia', 'sea', 'americas', 'europe'])
    p.add_argument('--policy', type=Path, default=ROOT / 'src/config/draft_modes.json')
    p.add_argument('--cache', type=Path, default=ROOT / 'data/raw/riot_rank_snapshots')
    p.add_argument('--output', type=Path, default=ROOT / 'reports/rank_snapshot_collection')
    a = p.parse_args()
    if not (1 <= a.batches <= 10 and 1 <= a.seeds_per_batch <= 20 and 1 <= a.matches_per_batch <= 20
            and 0 <= a.seed_offset and a.seed_offset+a.batches*a.seeds_per_batch <= 300 and 1 <= a.request_budget <= 1000):
        p.error('Invalid bounded campaign limits')
    from config.settings import RIOT_API_KEY, SERVER_METADATA
    a.routing = a.routing or SERVER_METADATA[a.platform]['region']
    runs = campaign(a, RiotClient(RIOT_API_KEY, min_interval=1.3, max_requests=a.request_budget))
    return 2 if any(r['collection_status'] != 'complete' for r in runs) else 0


if __name__ == '__main__':
    raise SystemExit(main())
