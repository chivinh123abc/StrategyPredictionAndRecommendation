"""A dated professional meta snapshot, shared by every draft component."""
from dataclasses import dataclass
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from analysis_data import load_clean_tables, DB_PATH
from historical_recommender import evidence, wilson


def patch_code(value):
    """Oracle's numeric patch column loses trailing zeros: 16.2 -> 16.20."""
    try:return f'{float(value):.2f}' if np.isfinite(float(value)) else ''
    except (ValueError,TypeError):return ''


def region_leagues(region):
    r=region.upper()
    return None if r=='ALL' else {'INTERNATIONAL':['WLDS','MSI','EWC'],
                                   'LCP':['LCP','VCS','PCS'],
                                   'WORLDS':['WLDS'],'CKTG':['WLDS']}.get(r,[r])


@dataclass
class MetaPolicy:
    as_of: str | None = None
    patch: str | None = None
    lookback_days: int = 60
    half_life_days: float = 21.0
    prior_games: float = 10.0

    def __post_init__(self):
        if self.lookback_days<1 or self.half_life_days<=0 or self.prior_games<=0:
            raise ValueError('Invalid meta window/decay/prior')


class DraftMetaSnapshot:
    def __init__(self,db_path=DB_PATH,region='ALL',policy=None,tables=None):
        self.policy=policy or MetaPolicy()
        self.region=region.upper()
        _,matches,players=load_clean_tables(db_path) if tables is None else tables
        dates=pd.to_datetime(matches.date,utc=True,errors='coerce')
        # A date-only cutoff includes that day; timestamps are precise inclusive cutoffs.
        now=pd.Timestamp.now(tz='Asia/Ho_Chi_Minh').tz_convert('UTC')
        cutoff=pd.to_datetime(self.policy.as_of,utc=True) if self.policy.as_of else now
        if self.policy.as_of and re.fullmatch(r'\d{4}-\d{2}-\d{2}',self.policy.as_of):
            cutoff+=pd.Timedelta(days=1)-pd.Timedelta(nanoseconds=1)
        subset=matches[(dates<=cutoff)&dates.notna()].copy()
        leagues=region_leagues(region)
        if leagues is not None:subset=subset[subset.league.str.upper().isin(leagues)]
        if subset.empty:raise ValueError(f'Không có dữ liệu {region} trước thời điểm yêu cầu')
        subset['_date']=pd.to_datetime(subset.date,utc=True)
        subset['_patch']=subset.patch.map(patch_code)
        latest=subset.sort_values(['_date','gameid']).iloc[-1]
        target=patch_code(self.policy.patch) if self.policy.patch else latest['_patch']
        exact=subset[subset['_patch'].eq(target)]
        if exact.empty:
            available=', '.join(sorted(subset['_patch'].unique()))
            raise ValueError(f'Không có patch dataset {target} cho {region}; có: {available}. Không tự giả lập meta mới.')
        anchor=exact['_date'].max()
        # Backfill only earlier patches within the same client major season.
        major=target.split('.')[0]
        recent=subset[(subset['_date']<=anchor)&
                      (subset['_date']>=anchor-pd.Timedelta(days=self.policy.lookback_days))&
                      subset['_patch'].str.startswith(major+'.')].copy()
        self.matches=recent
        self.players=players[players.gameid.isin(recent.gameid)].copy()
        self.target_patch=target
        self.anchor=anchor
        self.cutoff=cutoff
        self.game_weights={g:float(2**(-(anchor-d).total_seconds()/86400/self.policy.half_life_days))
                           for g,d in recent.groupby('gameid')['_date'].first().items()}
        self.players['_weight']=self.players.gameid.map(self.game_weights)
        self.patch_games=set(exact.gameid)&set(recent.gameid)
        self._build()

    def _build(self):
        p=self.players
        self.role_counts=p.groupby(['position','champion']).size().to_dict()
        self.patch_role_counts=p[p.gameid.isin(self.patch_games)].groupby(['position','champion']).size().to_dict()
        self.weighted_role_counts=p.groupby(['position','champion'])['_weight'].sum().to_dict()
        self.player_counts=p.groupby(['playername','position','champion'])['_weight'].sum().to_dict()
        self.role_totals=p.groupby('position')['_weight'].sum().to_dict()
        self.player_totals=p.groupby(['playername','position'])['_weight'].sum().to_dict()
        self._build_role_pairs()
        # Presence is once per game, across both teams and all ban slots.
        presence={};current_presence={};bans={}
        for game,g in self.matches.groupby('gameid',sort=False):
            picked=set(p[p.gameid.eq(game)].champion)
            banned={str(v) for col in ['ban1','ban2','ban3','ban4','ban5'] if col in g for v in g[col].dropna()}
            banned={c for c in banned if c.lower() not in ['','noban','none','null']}
            weight=self.game_weights[game]
            for c in picked|banned:presence[c]=presence.get(c,0)+weight
            for c in banned:bans[c]=bans.get(c,0)+weight
            if game in self.patch_games:
                for c in picked|banned:current_presence[c]=current_presence.get(c,0)+1
        total=sum(self.game_weights.values())
        self.presence={c:v/total for c,v in presence.items()}
        self.ban_rate={c:v/total for c,v in bans.items()}
        self.patch_presence=current_presence
        # Aggregate observed pick order, independent of Blue/Red color.
        self.slot_counts={};self.slot_totals={}
        for row in self.matches.itertuples(index=False):
            if not hasattr(row,'firstPick') or pd.isna(row.firstPick):continue
            prefix='F' if int(row.firstPick)==1 else 'S'
            for n in range(1,6):
                champion=getattr(row,f'pick{n}',None)
                if pd.isna(champion) or not champion:continue
                slot=f'{prefix}{n}'
                weight=self.game_weights[row.gameid]
                self.slot_counts[(slot,champion)]=self.slot_counts.get((slot,champion),0)+weight
                self.slot_totals[slot]=self.slot_totals.get(slot,0)+weight

    def _build_role_pairs(self):
        """Observed same-team role pairs, never opponents or ambiguous role records."""
        self.pair_counts={};self.pair_weights={};self.pair_wins={}
        self.pair_anchor_counts={};self.pair_anchor_weights={}
        self.pair_candidate_weights={};self.pair_totals={}
        self.enemy_pair_counts={};self.enemy_pair_wins={}
        p=self.players
        if 'side' not in p:return
        for _,g in p.groupby(['gameid','side'],sort=False):
            if len(g)!=5 or g.position.nunique()!=5:continue
            for a in g.itertuples(index=False):
                for b in g.itertuples(index=False):
                    if a.position==b.position:continue
                    key=(a.position,a.champion,b.position,b.champion)
                    weight=self.game_weights[a.gameid]
                    self.pair_counts[key]=self.pair_counts.get(key,0)+1
                    self.pair_weights[key]=self.pair_weights.get(key,0)+weight
                    self.pair_wins[key]=self.pair_wins.get(key,0)+int(a.result)
                    anchor=(a.position,b.position,b.champion)
                    self.pair_anchor_counts[anchor]=self.pair_anchor_counts.get(anchor,0)+1
                    self.pair_anchor_weights[anchor]=self.pair_anchor_weights.get(anchor,0)+weight
                    candidate=(a.position,a.champion,b.position)
                    self.pair_candidate_weights[candidate]=self.pair_candidate_weights.get(candidate,0)+weight
                    roles=(a.position,b.position)
                    self.pair_totals[roles]=self.pair_totals.get(roles,0)+weight

        # Preserve both roles against all five opponents, not just the same lane.
        for _,g in p.groupby('gameid',sort=False):
            if len(g)!=10 or g.groupby('side').position.nunique().min()!=5:continue
            records=list(g.itertuples(index=False))
            for a in records:
                for b in records:
                    if a.side==b.side:continue
                    key=(a.position,a.champion,b.position,b.champion)
                    self.enemy_pair_counts[key]=self.enemy_pair_counts.get(key,0)+1
                    self.enemy_pair_wins[key]=self.enemy_pair_wins.get(key,0)+int(a.result)

    def enemy_evidence(self,role,champ,enemy_role,enemy):
        key=(role,champ,enemy_role,enemy)
        return {**evidence(self.enemy_pair_wins.get(key,0),self.enemy_pair_counts.get(key,0)),
                'enemy_role':enemy_role,'opponent':enemy,
                'interpretation':'observed_whole_game_result_not_mechanical_counter'}

    def pair_evidence(self,role,champ,ally_role,ally,min_games=5):
        key=(role,champ,ally_role,ally);anchor=(role,ally_role,ally)
        n=self.pair_counts.get(key,0);trials=self.pair_anchor_counts.get(anchor,0)
        weighted_trials=self.pair_anchor_weights.get(anchor,0)
        total=self.pair_totals.get((role,ally_role),0)
        base=self.pair_candidate_weights.get((role,champ,ally_role),0)/total if total else 0
        prior=self.policy.prior_games
        posterior=(self.pair_weights.get(key,0)+prior*base)/(weighted_trials+prior)
        lift=posterior/base if base else None
        # A single unusual co-pick must not create a huge bonus for a rare champion.
        # Positive association needs actual pair observations; negative association
        # needs observations of the fixed ally (including absence of this pair).
        reliability=(self.pair_weights.get(key,0)/(self.pair_weights.get(key,0)+prior)
                     if lift is not None and lift>1 else weighted_trials/(weighted_trials+prior))
        effective_lift=float(np.exp(reliability*np.log(lift))) if lift is not None else None
        # Independence -> 0.5. Absence with many anchor observations -> below 0.5.
        score=lift/(1+lift) if lift is not None else None
        status=('insufficient_anchor_history' if trials<min_games or base==0 else
                'unobserved_pair' if n==0 else 'sparse_pair' if n<min_games else 'observed_pair')
        return {**evidence(self.pair_wins.get(key,0),n),'role':role,'champion':champ,
                'ally_role':ally_role,'ally':ally,'anchor_games':trials,
                'co_pick_share':n/trials if trials else None,
                'co_pick_share_ci95_wilson':wilson(n,trials),
                'weighted_pair_games':self.pair_weights.get(key,0),
                'weighted_anchor_games':weighted_trials,'marginal_pick_share':base,
                'smoothed_conditional_pick_share':posterior,'smoothed_lift':lift,
                'association_reliability':reliability,'effective_lift':effective_lift,
                'association_score':score,'status':status,
                'score_kind':'observed_role_pair_association_not_causal_synergy'}

    def eligible(self,role,champ,min_games):
        return self.role_counts.get((role,champ),0)>=min_games and self.patch_presence.get(champ,0)>0

    def prior_pick_share(self,role,champ):
        return self.weighted_role_counts.get((role,champ),0)/max(self.role_totals.get(role,0),1)

    def slot_priority(self,slot,role,champ):
        prior=self.prior_pick_share(role,champ)
        if slot is None:return prior
        c=self.policy.prior_games
        return (self.slot_counts.get((slot,champ),0)+c*prior)/(self.slot_totals.get(slot,0)+c)

    def roster(self,team):
        normal=lambda s:re.sub(r'[^a-z0-9]','',str(s).lower())
        rows=self.players[self.players.teamname.map(normal).eq(normal(team))].copy()
        if rows.empty:return None
        for game in rows.sort_values(['date','gameid'],ascending=False).gameid.unique():
            g=rows[rows.gameid.eq(game)]
            if len(g)==5 and g.position.nunique()==5 and g.playername.notna().all():
                return {'players':dict(zip(g.position,g.playername)),
                        'date':str(g.date.iloc[0]),'gameid':str(game),'kind':'latest_observed_lineup_not_live_roster'}
        return None

    def role_probabilities(self,champ):
        counts={r:self.weighted_role_counts.get((r,champ),0) for r in ['top','jng','mid','bot','sup']}
        total=sum(counts.values())
        return {r:v/total for r,v in counts.items()} if total else {}

    def metadata(self):
        return {'region':self.region,'dataset_patch':self.target_patch,
                'data_through':self.anchor.isoformat(),'requested_as_of':self.cutoff.isoformat(),
                'staleness_days':max(0,int((self.cutoff-self.anchor).total_seconds()/86400)),
                'history_games':int(self.matches.gameid.nunique()),'patch_games':len(self.patch_games),
                'lookback_days':self.policy.lookback_days,'half_life_days':self.policy.half_life_days,
                'claim':'historical_snapshot_not_live_meta'}
