"""Auditable name normalization from official Data Dragon, no fuzzy aliases."""
import json
from pathlib import Path
import re
import unicodedata


def token(value):
    text = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]', '', text.lower())


class ChampionCatalog:
    def __init__(self, payload):
        self.by_id, self.aliases = {}, {}
        self.version = payload.get('version')
        for entry in payload['data'].values():
            canonical = entry['name']
            self.by_id[int(entry['key'])] = canonical
            for alias in (entry['id'], canonical):
                key = token(alias)
                if key in self.aliases and self.aliases[key] != canonical:
                    raise ValueError('ambiguous_official_champion_alias')
                self.aliases[key] = canonical

    @classmethod
    def read(cls, path):
        return cls(json.loads(Path(path).read_text(encoding='utf-8')))

    def name(self, value, champion_id=None):
        if champion_id is not None:
            result = self.by_id.get(int(champion_id))
            if result is None:
                raise ValueError('unknown_official_champion_id')
            # Authoritative ID resolves internal names without hand-written special cases.
            return result
        result = self.aliases.get(token(value))
        if result is None:
            raise ValueError(f'unknown_official_champion_name:{value}')
        return result


def normalize_observations(rows, catalog):
    rows = rows.copy()
    audit = []
    for col in ('champion', 'opponent'):
        mapping = {}
        for value in sorted(rows[col].dropna().unique()):
            mapping[value] = catalog.name(value)
            audit.append({'field': col, 'raw': value, 'canonical': mapping[value],
                          'changed': value != mapping[value]})
        rows[col] = rows[col].map(mapping)
    return rows, audit


def main():
    import argparse
    from datetime import datetime, timezone
    import hashlib
    import requests
    parser = argparse.ArgumentParser(description='Download pinned official Riot champion catalog; no API key needed.')
    parser.add_argument('--version', default='16.20.1')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'\d+\.\d+\.\d+', args.version):
        parser.error('Expected major.minor.build version')
    url = f'https://ddragon.leagueoflegends.com/cdn/{args.version}/data/en_US/champion.json'
    response = requests.get(url, timeout=25)
    response.raise_for_status()
    ChampionCatalog(response.json())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(response.text, encoding='utf-8')
    provenance = {'url': url, 'fetched_at': datetime.now(timezone.utc).isoformat(),
                  'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}
    args.output.with_suffix('.provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    print(f'Official catalog {args.version} saved.')


if __name__ == '__main__':
    main()
