"""Descriptive historical recommendation, with counts and Wilson intervals.

Ranking is a documented heuristic over observations, never causal uplift or a
calibrated probability. Expert champion metadata does not affect this ranking.
"""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import sys
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analysis_data import load_clean_tables, DB_PATH

ROLES = ['top','jng','mid','bot','sup']
ALIASES = {'jungle':'jng','support':'sup','adc':'bot'}


def wilson(wins, n):
    if n == 0: return [None,None]
    z=1.959963984540054
    p=wins/n
    center=(p+z*z/(2*n))/(1+z*z/n)
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return [float(max(0,center-half)),float(min(1,center+half))]


def evidence(wins, n):
    return {'wins':int(wins),'games':int(n),'winrate':float(wins/n) if n else None,
            'ci95_wilson':wilson(wins,n),'statistic_kind':'historical_team_result',
            'causal_uplift':None}


class HistoricalRecommender:
    @classmethod
    def from_frames(cls,matches,players,min_games=5):
        """A scoped historical view; no second query silently widens its period."""
        engine=cls.__new__(cls)
        engine.db_path=None;engine.before=None;engine.min_games=min_games
        engine.matches=matches.copy();engine.players=players.copy();engine._regions={}
        return engine

    def __init__(self,db_path=DB_PATH,before=None,min_games=5):
        self.db_path=Path(db_path)
        self.before=before
        self.min_games=min_games
        _,self.matches,self.players=load_clean_tables(db_path)
        if before is not None:
            limit=pd.to_datetime(before,utc=True)
            self.matches=self.matches[pd.to_datetime(self.matches.date,utc=True)<limit].copy()
            self.players=self.players[self.players.gameid.isin(self.matches.gameid)].copy()
        self._regions={}

    def region_players(self,region):
        region=str(region).upper()
        leagues={'LCP':['LCP','VCS','PCS'],'INTERNATIONAL':['WLDS','MSI','EWC'],
                 'WORLDS':['WLDS'],'CKTG':['WLDS']}.get(region,[region])
        return self.players if region=='ALL' else self.players[self.players.league.str.upper().isin(leagues)]

    def stats(self,region):
        region=region.upper()
        if region in self._regions: return self._regions[region]
        p=self.region_players(region)[['gameid','position','champion','side','result','playername']].copy()
        base={(r,c):(int(g.result.sum()),len(g)) for (r,c),g in p.groupby(['position','champion'])}
        player={(n,r,c):(int(g.result.sum()),len(g)) for (n,r,c),g in p.groupby(['playername','position','champion'])}
        # Vectorized joins avoid repeatedly constructing wide per-game records.
        lane_counts=p.groupby(['gameid','position']).agg(n=('side','size'),sides=('side','nunique'))
        valid=lane_counts.index[(lane_counts.n==2)&(lane_counts.sides==2)]
        lanes=p[pd.MultiIndex.from_frame(p[['gameid','position']]).isin(valid)]
        opponents=lanes.merge(lanes,on=['gameid','position'],suffixes=('_a','_b'))
        opponents=opponents[opponents.side_a!=opponents.side_b]
        matchup={(r,c,o):(int(g.result_a.sum()),len(g)) for (r,c,o),g in
                 opponents.groupby(['position','champion_a','champion_b'])}
        team_counts=p.groupby(['gameid','side']).agg(n=('position','size'),roles=('position','nunique'))
        valid=team_counts.index[(team_counts.n==5)&(team_counts.roles==5)]
        teams=p[pd.MultiIndex.from_frame(p[['gameid','side']]).isin(valid)]
        teammates=teams.merge(teams,on=['gameid','side'],suffixes=('_a','_b'))
        teammates=teammates[teammates.position_a!=teammates.position_b]
        pairs={(r,c,a):(int(g.result_a.sum()),len(g)) for (r,c,a),g in
               teammates.groupby(['position_a','champion_a','champion_b'])}
        result=(base,player,matchup,pairs)
        self._regions[region]=result
        return result

    def recommend(self,target_lane,ally_team,enemy_team,already_banned=None,player_name=None,
                  top_k=5,region='ALL',enemy_lane_champ=None,**kwargs):
        role=ALIASES.get(target_lane.lower(),target_lane.lower())
        if role not in ROLES: raise ValueError('Unknown role')
        allies=list(ally_team.values()) if isinstance(ally_team,dict) else list(ally_team or [])
        enemies=list(enemy_team.values()) if isinstance(enemy_team,dict) else list(enemy_team or [])
        opponent=enemy_lane_champ
        if opponent is None and isinstance(enemy_team,dict):
            opponent=enemy_team.get(role) or enemy_team.get(target_lane)
        excluded=set(allies+enemies)|set(already_banned or [])
        base,players,matchups,pairs=self.stats(region)
        result=[]
        for (r,champ),(wins,n) in base.items():
            if r!=role or champ in excluded or n<self.min_games: continue
            ev=evidence(wins,n)
            components=[('role',wins,n)]
            matchup=evidence(*matchups.get((role,champ,opponent),(0,0))) if opponent else None
            if matchup and matchup['games']>=self.min_games: components.append(('matchup',matchup['wins'],matchup['games']))
            synergy=[]
            for ally in allies:
                w,k=pairs.get((role,champ,ally),(0,0))
                if k:
                    sy=evidence(w,k);sy['ally']=ally;synergy.append(sy)
                    if k>=self.min_games: components.append(('ally',w,k))
            mastery=evidence(*players.get((player_name,role,champ),(0,0))) if player_name else None
            if mastery and mastery['games']>=self.min_games: components.append(('player',mastery['wins'],mastery['games']))
            # Common Beta(5,5) shrinkage and sample reliability, same for all cases.
            weights=np.array([k/(k+10) for _,w,k in components])
            means=np.array([(w+5)/(k+10) for _,w,k in components])
            score=float(np.average(means,weights=weights))
            reasons=[f"Lịch sử {region}: {wins}/{n} trận thắng; WR {100*wins/n:.1f}%; CI95 [{100*ev['ci95_wilson'][0]:.1f}, {100*ev['ci95_wilson'][1]:.1f}]%"]
            if matchup: reasons.append(f"Đối đầu {opponent}: n={matchup['games']}; kết quả cả trận, không phải xác suất thắng đường")
            if opponent is None and enemies: reasons.append('Chưa xác định đối thủ cùng đường; không chấm điểm matchup')
            result.append({'champion':champ,'lane':target_lane.upper(),'region':region.upper(),
                           'score':score,'ranking_score':round(score*100,2),'score_kind':'historical_heuristic_points',
                           'probability':None,'expected_winrate_delta':None,'games':n,
                           'historical':ev,'matchup':matchup,'synergies':synergy,'player_history':mastery,
                           'ranking_components':[{'source':a,'wins':w,'games':k} for a,w,k in components],
                           'reasons':reasons,'dmg_type':'not_used','is_melee':None,'hard_cc':None,
                           'limitations':['Observational, confounded by team/player/patch/side.',
                                          'Wilson intervals assume independent games; no causal uplift.']})
        return sorted(result,key=lambda x:(-x['score'],-x['games'],x['champion']))[:top_k]

    def counters(self,champ,position=None,top_k=5,region='ALL'):
        base,_,matchups,_=self.stats(region)
        if position is None:
            roles=[(n,r) for (r,c),(w,n) in base.items() if c==champ]
            if not roles:return {'champion':champ,'counters':[],'reason':'No historical role evidence'}
            position=max(roles)[1]
        role=ALIASES.get(position,position)
        out=[]
        for (r,c,opp),(w,n) in matchups.items():
            if r==role and opp==champ and n>=self.min_games:
                ev=evidence(w,n)
                out.append({'champion':c,'games':n,'matches':n,'winrate_pct':100*w/n,
                            'score':(w+5)/(n+10),'historical':ev,'avg_gd10':None,
                            'score_kind':'historical_heuristic_points','causal_uplift':None})
        return {'champion':champ,'position':role,'counters':sorted(out,key=lambda x:(-x['score'],-x['games'],x['champion']))[:top_k],
                'interpretation':'Historical team winrates; not proof of a mechanical counter.'}
