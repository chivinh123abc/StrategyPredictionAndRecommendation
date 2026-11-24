"""Separate descriptive Pro/Rank matchup evidence; never changes draft scores."""
from pathlib import Path
from contextlib import closing
import hashlib
import json
import sqlite3
import sys
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/01_data_pipeline')]
from draft_meta import patch_code
from rank_data_contract import ChampionCatalog
from rank_matchup_tables import aggregate
from ranked_matchups import METRICS,write_json
from historical_recommender import evidence

CATALOG=ROOT/'data/raw/riot_matchups_study/champion_16.20.1.json'
RANK_DB=ROOT/'data/database/ranked_evidence.db'


def pro_observations(matches,players,catalog):
    required={'gameid','position','side','champion','result','playername'}
    if not required<=set(players) or not {'gameid','side','date','gamelength','patch','league'}<=set(matches):
        return pd.DataFrame()
    p=players.copy()
    if p.duplicated(['gameid','side','position']).any():
        raise ValueError('Duplicate Pro role within a game/team')
    counts=p.groupby(['gameid','side']).position.nunique()
    good=counts[counts.eq(5)].reset_index().groupby('gameid').size()
    p=p[p.gameid.isin(good[good.eq(2)].index)]
    p=p.merge(matches[['gameid','side','date','gamelength','patch','league']],
        on=['gameid','side'],suffixes=('_player',''),validate='many_to_one')
    pairs=p.merge(p,on=['gameid','position'],suffixes=('_a','_b'))
    pairs=pairs[pairs.side_a.ne(pairs.side_b)].copy()
    if pairs.empty:return pd.DataFrame()
    def canonical(value):
        try:return catalog.name(value)
        except ValueError:return None
    for column in ['champion_a','champion_b']:
        pairs[column]=pairs[column].map(canonical)
    unknown=set(pairs.loc[pairs[['champion_a','champion_b']].isna().any(axis=1),'gameid'])
    pairs=pairs[~pairs.gameid.isin(unknown)]
    start=pd.to_datetime(pairs.date_a,utc=True,errors='coerce')
    ends=start+pd.to_timedelta(pairs.gamelength_a,unit='s')
    official_ids={name:cid for cid,name in catalog.by_id.items()}
    out=pd.DataFrame(dict(match_id=pairs.gameid,team_id=pairs.side_a,role=pairs.position,
        platform=pairs.league_a.str.upper(),queue='PRO',patch=pairs.patch_a.map(patch_code),tier_floor='PRO',
        champion=pairs.champion_a,opponent=pairs.champion_b,champion_id=pairs.champion_a.map(official_ids),
        opponent_id=pairs.champion_b.map(official_ids),win=pairs.result_a,_puuid=pairs.playername_a,
        _enemy_puuid=pairs.playername_b,played_at=start,ended_at=ends))
    for minute in (10,15):
        for metric,field in [('gold','gold'),('xp','xp'),('cs','cs')]:
            a=pd.to_numeric(pairs.get(f'{field}at{minute}_a',pd.Series(np.nan,index=pairs.index)),errors='coerce')
            b=pd.to_numeric(pairs.get(f'{field}at{minute}_b',pd.Series(np.nan,index=pairs.index)),errors='coerce')
            valid=a.ge(0)&b.ge(0)&np.isfinite(a)&np.isfinite(b)&pairs.gamelength_a.ge(minute*60)
            out[f'{metric}_diff_{minute}']=(a-b).where(valid)
    return out.reset_index(drop=True)


def read_rank_snapshot(path=RANK_DB):
    """One coherent read transaction while the collector continues writing WAL."""
    if not Path(path).exists():return pd.DataFrame()
    with closing(sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True)) as c:
        c.execute('BEGIN')
        records=c.execute('''SELECT o.row_json,j.updated_at FROM observations o
            JOIN jobs j ON j.match_id=o.match_id WHERE j.status='accepted'
            ORDER BY o.match_id,o.team_id,o.role''').fetchall()
    data=[]
    for raw,recorded in records:
        row=json.loads(raw)
        # Original qualification availability alone can predate timeline ingestion.
        row['available_at']=max(pd.to_datetime(row['available_at'],utc=True),pd.to_datetime(recorded,unit='s',utc=True)).isoformat()
        data.append(row)
    return pd.DataFrame(data)


def normalize_rank(rows,catalog):
    if rows.empty:return rows.copy(),0
    result=rows.copy();bad=set()
    for column,id_column in [('champion','champion_id'),('opponent','opponent_id')]:
        names=[]
        for row in result.itertuples():
            try:names.append(catalog.name(getattr(row,column),getattr(row,id_column)))
            except ValueError:names.append(None);bad.add(row.match_id)
        result[column]=names
    # Keep complete verified cohorts; unknown IDs do not become hand-written aliases.
    result=result[~result.match_id.isin(bad)].copy()
    return result,len(bad)


def available_before(rows,cutoff):
    if rows.empty:return rows.copy()
    cut=pd.to_datetime(cutoff,utc=True)
    mask=pd.to_datetime(rows.ended_at,utc=True,errors='coerce').le(cut)
    mask&=pd.to_datetime(rows.available_at,utc=True,errors='coerce').le(cut)
    return rows[mask].copy()


class SourceView:
    def __init__(self,rows,min_games=5):
        self.rows=rows;self.min_games=min_games;self.cache={}
        self.groups={k:g for k,g in rows.groupby(['role','champion','opponent'])} if len(rows) else {}

    def lookup(self,role,champion,opponent):
        key=(role,champion,opponent)
        if key not in self.cache:
            group=self.groups.get(key)
            if group is None:
                row={**evidence(0,0),'evidence_status':'missing','early_status':'missing'}
                for metric in METRICS:
                    row.update({f'{metric}_n':0,f'{metric}_mean':None,
                        f'{metric}_mean_ci95_low':None,f'{metric}_mean_ci95_high':None})
                row.update(patches='[]',platforms='[]')
            else:
                row=aggregate(group,self.min_games,pooled=True).iloc[0].to_dict()
                row['ci95_wilson']=[row['win_ci95_low'],row['win_ci95_high']]
            self.cache[key]=json.loads(json.dumps(row,default=lambda x:x.item() if hasattr(x,'item') else str(x)))
        return dict(self.cache[key])


def compare_sources(pro,rank,min_games=5):
    def sign(source):
        lo,hi=source['gold_diff_15_mean_ci95_low'],source['gold_diff_15_mean_ci95_high']
        if source['gold_diff_15_n']<min_games or lo is None or hi is None:return 0
        return 1 if lo>0 else -1 if hi<0 else 0
    enough=pro['games']>=min_games and rank['games']>=min_games
    a,b=pro['gold_diff_15_mean'],rank['gold_diff_15_mean']
    return {'sample_status':'both_observed' if enough else 'insufficient_samples',
        'gd15_comparison':('insufficient_measurements' if pro['gold_diff_15_n']<min_games or rank['gold_diff_15_n']<min_games else
            'opposite_supported_intervals' if sign(pro)*sign(rank)==-1 else
            'opposite_means_uncertain' if a*b<0 else 'no_observed_direction_conflict'),
        'winrate_direction_conflict':bool(enough and (pro['winrate']-.5)*(rank['winrate']-.5)<0),
        'mechanical_counter_confirmed':False}


class MatchupExplanations:
    def __init__(self,catalog_path=CATALOG,rank_rows=None,rank_db=RANK_DB):
        self.catalog=ChampionCatalog.read(catalog_path)
        raw=read_rank_snapshot(rank_db) if rank_rows is None else rank_rows
        self.rank_rows,self.unknown_rank_games=normalize_rank(raw,self.catalog)
        self.rank_frozen_at=pd.Timestamp.now(tz='UTC').isoformat()
        self.contexts={}

    def explain(self,role,champion,role_masses,snapshot,min_games=5):
        key=(id(snapshot),min_games)
        if key not in self.contexts:
            pro=pro_observations(snapshot.matches,snapshot.players,self.catalog)
            if len(pro):pro=pro[pd.to_datetime(pro.ended_at,utc=True).le(snapshot.cutoff)]
            rank=available_before(self.rank_rows,snapshot.cutoff)
            self.contexts[key]=(SourceView(pro,min_games),SourceView(rank,min_games))
        pro,rank=self.contexts[key];rows=[]
        for opponent,prob in role_masses.get(role,{}).items():
            try:a=self.catalog.name(champion);b=self.catalog.name(opponent)
            except ValueError:continue
            p,r=pro.lookup(role,a,b),rank.lookup(role,a,b)
            rows.append({'role':role,'champion':champion,'opponent':opponent,'enemy_role_probability':float(prob),
                'pro':p,'rank':r,'comparison':compare_sources(p,r,min_games),
                'pro_scope':'current advisor historical window/region, unweighted descriptive observations',
                'rank_scope':'all observed patches/servers available before requested as_of',
                'rank_frozen_at':self.rank_frozen_at,'unknown_rank_games_excluded':self.unknown_rank_games,
                'affects_main_score':False})
        return rows


def format_evidence(rows):
    lines=[]
    def number(x):return 'NA' if x is None else f'{x:+.0f}'
    for row in rows:
        lines.append(f"{row['champion']} vs {row['opponent']} ({row['role']}, p(role)={row['enemy_role_probability']:.2f})")
        for source in ['pro','rank']:
            s=row[source];wr='NA' if s['winrate'] is None else f"{s['winrate']:.1%}"
            ci=s['ci95_wilson'];interval='NA' if ci[0] is None else f'{ci[0]:.1%}..{ci[1]:.1%}'
            labels={'gold':'GD','xp':'XPD','cs':'CSD'}
            stats='; '.join(f"{labels[m]}{t}={number(s[f'{m}_diff_{t}_mean'])} (n={s[f'{m}_diff_{t}_n']})" for t in (10,15) for m in ['gold','xp','cs'])
            lines.append(f"  {source.upper()}: n={s['games']}, WR={wr}, Wilson95={interval}; {stats}")
            lines.append(f"    GD15 mean CI95=[{number(s['gold_diff_15_mean_ci95_low'])}, {number(s['gold_diff_15_mean_ci95_high'])}]; {s['early_status']}; patches={s['patches']}; sources={s['platforms']}")
        lines.append(f"  {row['comparison']['sample_status']}; {row['comparison']['gd15_comparison']}; WR trung bình trái chiều={row['comparison']['winrate_direction_conflict']}")
    return lines


def export_pro(output,catalog_path=CATALOG):
    from analysis_data import load_clean_tables,DB_PATH
    _,matches,players=load_clean_tables()
    catalog=ChampionCatalog.read(catalog_path);rows=pro_observations(matches,players,catalog)
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    rows.drop(columns=['_puuid','_enemy_puuid']).to_csv(output/'observations.csv',index=False,encoding='utf-8-sig')
    for name,pooled in [('all_matchups',False),('pooled_all_matchups',True)]:
        table=aggregate(rows,pooled=pooled)
        table.to_csv(output/f'{name}.csv',index=False,encoding='utf-8-sig')
    supported=table[table.games.ge(5)]
    for name,metric,ascending in [('best_full_game_matchups','winrate',False),
            ('unfavorable_full_game_matchups','winrate',True),('early_gold_advantages','gold_diff_15_mean',False)]:
        subset=supported[supported.gold_diff_15_n.ge(5)] if metric=='gold_diff_15_mean' else supported
        subset.sort_values(['role','opponent',metric,'games'],ascending=[True,True,ascending,False]).to_csv(output/f'{name}.csv',index=False,encoding='utf-8-sig')
    summary={'games':int(rows.match_id.nunique()),'input_games':int(matches.gameid.nunique()),'rows':len(rows),'catalog_version':catalog.version,
        'generated_at':pd.Timestamp.now(tz='UTC').isoformat(),'db_sha256':hashlib.sha256(DB_PATH.read_bytes()).hexdigest(),
        'metric_valid_counts':{m:int(rows[m].notna().sum()) for m in METRICS},
        'pooled_matchups':len(table),'pooled_matchups_n5':len(supported),
        'semantics':'same-role observed resource differences; no inferred lane values or causal counter claim'}
    write_json(output/'summary.json',summary)
    (output/'REPORT.md').write_text('# Thống kê đối đầu Pro\n\n'+
        f"{summary['games']} trận, {len(rows)} observations; {len(table)} kèo gộp, {len(supported)} kèo n>=5.\n\n"+
        'Ghép cùng game/role, khác side. GD/XPD/CSD = chỉ số người chọn trừ người đối diện; giữ số âm và missing.\n\n'+
        'all_matchups tách league/patch; pooled và ba bảng xếp gộp các league/patch thực có, giữ danh sách nguồn. Bảng giải thích runtime dùng đúng cửa sổ/region của advisor, không lấy cả corpus để chấm trận quá khứ.\n\n'+
        'Winrate là kết quả cả đội, Wilson95; mean resource CI dùng Student-t. Người chơi lặp, đội hình, gank và patch là confounding; không xác nhận counter nhân quả. N5 chỉ là ngưỡng hiển thị. Không có dữ liệu lane suy tạo.\n',encoding='utf-8')
    return summary


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'reports/pro_matchups')
    p.add_argument('--catalog',type=Path,default=CATALOG)
    a=p.parse_args();print(json.dumps(export_pro(a.output,a.catalog)))
