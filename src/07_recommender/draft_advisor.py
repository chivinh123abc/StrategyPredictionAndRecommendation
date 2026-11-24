"""Contextual draft ranking and one-step ban denial, with explicit evidence.

Weighted component scoring is a heuristic objective, not a win probability.
Cosine and observed match/team results do not prove causal counter-picks.
"""
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from itertools import permutations
from draft_meta import DraftMetaSnapshot, MetaPolicy
from historical_recommender import evidence
from historical_recommender import HistoricalRecommender, ALIASES, ROLES
from content_based import ContentBasedRecommender

DISPLAY_ROLES = {'top':'top','jng':'jungle','mid':'mid','bot':'bot','sup':'support'}


def role_key(role):
    key=ALIASES.get(str(role).lower(),str(role).lower())
    if key not in ROLES:raise ValueError('Vị trí không hợp lệ')
    return key


def role_dict(picks):
    return {role_key(r):c for r,c in (picks or {}).items() if c}


def percentile(values):
    if not values:return []
    if len(values)==1:return [1.0]
    return ((pd.Series(values).rank(method='average')-1)/(len(values)-1)).tolist()


@dataclass
class AdvisorPolicy:
    weights: dict = field(default_factory=lambda:{'meta':1.0,'draft_order':1.0,
                                                 'historical':.25,'matchup':.5,
                                                 'synergy':.25,'composition':1.0,'mastery':.5,'content':.1})
    min_games: int = 5
    candidate_min_games: int | None = None

    def __post_init__(self):
        if self.candidate_min_games is None:self.candidate_min_games=self.min_games
        required={'meta','draft_order','historical','matchup','synergy','composition','mastery','content'}
        if set(self.weights)!=required or not all(np.isfinite(v) and v>=0 for v in self.weights.values()):
            raise ValueError('Invalid advisor weights')
        if self.weights['meta']+self.weights['historical']<=0 or self.min_games<1 or self.candidate_min_games<1:
            raise ValueError('A supported historical objective is required')


class DraftAdvisor:
    def __init__(self,db_path=None,policy=None,historical=None,content=None,meta_policy=None):
        self.policy=policy or AdvisorPolicy()
        kwargs={} if db_path is None else {'db_path':db_path}
        self.history=historical or HistoricalRecommender(**kwargs,min_games=self.policy.candidate_min_games)
        self.content=content or ContentBasedRecommender(**kwargs,min_games=self.policy.min_games)
        self._content_cache={}
        self.meta_policy=meta_policy or MetaPolicy()
        self._contexts={}

    def context(self,region):
        if region not in self._contexts:
            snapshot=DraftMetaSnapshot(region=region,policy=self.meta_policy,
                                       tables=(None,self.history.matches,self.history.players))
            history=HistoricalRecommender.from_frames(snapshot.matches,snapshot.players,self.policy.candidate_min_games)
            content=ContentBasedRecommender(players=snapshot.players,min_games=self.policy.min_games)
            self._contexts[region]=(snapshot,history,content)
        return self._contexts[region]

    def infer_enemy_roles(self,enemies,snapshot):
        champs=sorted(set(enemies.values()))
        masses=[]
        for roles in permutations(ROLES,len(champs)):
            mass=float(np.prod([snapshot.role_probabilities(c).get(r,0) for c,r in zip(champs,roles)]))
            if mass>0:masses.append((roles,mass))
        total=sum(m for _,m in masses)
        result={r:{} for r in ROLES}
        if total:
            for roles,mass in masses:
                for c,r in zip(champs,roles):result[r][c]=result[r].get(c,0)+mass/total
        return result

    def evaluate_enemy_context(self,role,champ,role_masses,snapshot,baseline,enemy_count):
        evidence_rows=[];residual=0.;covered=0.
        for enemy_role,masses in role_masses.items():
            for opponent,prob in masses.items():
                ev=snapshot.enemy_evidence(role,champ,enemy_role,opponent)
                ev['role_probability']=prob
                ev['status']='observed_context' if ev['games']>=self.policy.min_games else 'insufficient_context'
                if ev['games']>=self.policy.min_games:
                    residual+=prob*(ev['winrate']-baseline)*ev['games']/(ev['games']+self.meta_policy.prior_games)
                    covered+=prob
                evidence_rows.append(ev)
        return (float(np.clip(.5+residual/max(1,enemy_count),0,1)),evidence_rows,
                float(covered/max(1,enemy_count)))

    def content_scores(self,player,role,region,seeds):
        key=(player,role,region,tuple(sorted(seeds or [])))
        if key in self._content_cache:return self._content_cache[key]
        _,_,content=self.context(region)
        response=content.recommend_for_player(player or '',role,region,top_k=10000)
        label=f'profile tuyển thủ {player}'
        # User-provided preferred seeds are explicit intent, not inferred matchup labels.
        if seeds:
            aggregate={}
            count=0
            for seed in seeds:
                seed_result=content.recommend_similar(seed,role,region,top_k=10000)
                if seed_result['status']!='ok':continue
                count+=1
                for row in seed_result['recommendations']:
                    aggregate[row['champion']]=aggregate.get(row['champion'],0)+row['cosine_similarity']
                aggregate[seed]=aggregate.get(seed,0)+1.0
            if count:
                result=({c:v/count for c,v in aggregate.items()},'tướng mẫu do người chơi chỉ định')
                self._content_cache[key]=result
                return result
        result=({r['champion']:r['cosine_similarity'] for r in response['recommendations']},label)
        self._content_cache[key]=result
        return result

    def recommend_picks(self,lane,ally_team,enemy_team,already_banned=None,player_name=None,
                        top_k=5,region='ALL',seeds=None,draft_slot=None):
        role=role_key(lane)
        allies,enemies=role_dict(ally_team),role_dict(enemy_team)
        snapshot,history,_=self.context(region)
        # Do not treat the simulator's provisional enemy role assignment as fact.
        candidates=history.recommend(role,allies,{},set(already_banned or [])|set(enemies.values()),
                                     player_name,top_k=10000,region=region)
        rows=[r for r in candidates if snapshot.eligible(role,r['champion'],self.policy.candidate_min_games)]
        if not rows:return []
        _,_,matchups,_=history.stats(region)
        all_role_masses=self.infer_enemy_roles(enemies,snapshot) if enemies else {}
        role_masses=all_role_masses.get(role,{})
        cosine,content_source=self.content_scores(player_name,role,region,seeds)
        active={'meta','historical'}
        if draft_slot:active.add('draft_order')
        if snapshot.player_totals.get((player_name,role),0)>0:active.add('mastery')
        if any(r['champion'] in cosine for r in rows):active.add('content')
        if enemies:active.add('matchup')
        if allies:active.add('synergy')
        pair_evidence={r['champion']:[snapshot.pair_evidence(role,r['champion'],ar,ac,self.policy.min_games)
                                   for ar,ac in allies.items() if ar!=role] for r in rows}
        if any(e['status']!='insufficient_anchor_history' for values in pair_evidence.values() for e in values):
            active.add('composition')
        weights={k:v for k,v in self.policy.weights.items() if k in active and v>0}
        for row in rows:
            champ=row['champion'];base_wr=row['historical']['winrate']
            matchup_evidence=[]
            for opponent,prob in role_masses.items():
                wins,n=matchups.get((role,champ,opponent),(0,0))
                ev={**evidence(wins,n),'opponent':opponent,'role_probability':prob}
                matchup_evidence.append(ev)
            # Whole revealed enemy team: jungle-only history cannot establish
            # whether this champion fits the other four enemy picks.
            matchup_score,enemy_context,context_coverage=self.evaluate_enemy_context(
                role,champ,all_role_masses,snapshot,base_wr,len(enemies))
            # Pair evidence must preserve both roles; champion-only joins mix flex positions.
            row['synergies']=pair_evidence[champ]
            synergies=[r for r in row['synergies'] if r['games']>=self.policy.min_games]
            synergy=.5
            if synergies:
                synergy+=float(np.mean([(x['winrate']-base_wr)*x['games']/(x['games']+self.meta_policy.prior_games) for x in synergies]))
            supported=[e for e in pair_evidence[champ] if e['status']!='insufficient_anchor_history']
            composition=.5
            composition_lift=1.0
            if supported:
                reliability=[e['weighted_anchor_games']/(e['weighted_anchor_games']+self.meta_policy.prior_games) for e in supported]
                composition=float(np.average([e['association_score'] for e in supported],weights=reliability))
                composition_lift=float(np.exp(np.average([np.log(e['effective_lift']) for e in supported],weights=reliability)))
            scores={'meta':snapshot.presence.get(champ,0),
                    'draft_order':snapshot.slot_priority(draft_slot,role,champ),
                    'historical':row['historical']['ci95_wilson'][0],
                    'matchup':matchup_score,'synergy':float(np.clip(synergy,0,1)),'composition':composition,
                    'mastery':snapshot.player_counts.get((player_name,role,champ),0)/max(1,snapshot.player_totals.get((player_name,role),0)),
                    'content':cosine.get(champ,0)}
            base_weights={k:v for k,v in weights.items() if k!='composition'}
            base_score=sum(base_weights[k]*scores[k] for k in base_weights)/sum(base_weights.values())
            # Item-item association adjusts priority odds, instead of an additive bonus
            # that can reward a never-observed pairing just for champion popularity.
            factor=composition_lift**weights.get('composition',0)
            score=base_score*factor/(1-base_score+base_score*factor)
            patch_count=snapshot.patch_role_counts.get((role,champ),0)
            reasons=[f"Patch dataset {snapshot.target_patch}: presence cửa sổ gần đây {snapshot.presence.get(champ,0):.1%}; {patch_count} lượt chọn đúng vị trí trên patch, {row['games']} trận trong cửa sổ gần đây",
                     f"Slot {draft_slot or 'chưa chỉ định'}: ưu tiên chọn quan sát {scores['draft_order']:.3f}; không phải xác suất thắng"]
            if matchup_evidence:
                reasons.append('Vị trí địch còn là giả định: '+', '.join(f"{e['opponent']} p(role)={e['role_probability']:.2f}, n={e['games']}" for e in matchup_evidence))
            else:reasons.append('Chưa đủ căn cứ đối đầu cùng đường; không gán kèo khắc chế cố định')
            if synergies:reasons.append('Phối hợp lịch sử: '+', '.join(f"{r['ally']} n={r['games']}" for r in synergies))
            if enemies:
                reasons.append(f"Đã xét cả đội địch được lộ; coverage đối đầu đủ mẫu {context_coverage:.0%}. Chưa có evaluator cơ chế kỹ năng; không xác nhận đây là counter hoặc lựa chọn tối ưu.")
            for ev in pair_evidence[champ]:
                reasons.append(f"Cặp {role}/{ev['ally_role']} với {ev['ally']}: {ev['games']}/{ev['anchor_games']} lần ghép, {ev['status']}; association={ev['association_score']}; không phải xác suất thắng hoặc chứng minh tối ưu")
            if champ in cosine:reasons.append(f"Cosine {cosine[champ]:.3f} từ {content_source}; chỉ là hỗ trợ tương đồng")
            row.update(score=float(score),ranking_score=round(score*100,2),
                       score_kind='patch_aware_draft_priority_points',cosine_similarity=cosine.get(champ),
                       score_components={k:{'value':float(scores[k]),'weight':float(weights[k])} for k in weights},
                       reasons=reasons,lane=DISPLAY_ROLES[role],matchup_candidates=matchup_evidence,
                       composition_evidence=pair_evidence[champ],
                       enemy_context_evidence=enemy_context,enemy_context_coverage=float(context_coverage),
                       mechanical_counter_status='not_evaluated',
                       selection_basis='statistical_priority_not_validated_counter',
                       review_required=bool(enemies and context_coverage==0),
                       score_formula='base_priority_odds_times_geometric_role_pair_lift',
                       base_priority=float(base_score),composition_lift=composition_lift,
                       evidence_status='sparse_candidate' if row['games']<self.policy.min_games else 'observed_candidate',
                       matchup=None,meta_scope=snapshot.metadata(),draft_slot=draft_slot,
                       objective='recent_patch_presence_and_observed_draft_order_with_context',
                       policy={'weights':self.policy.weights,'min_games':self.policy.min_games,'candidate_min_games':self.policy.candidate_min_games})
        return sorted(rows,key=lambda r:(r['evidence_status']=='sparse_candidate',-r['score'],-r['games'],r['champion']))[:top_k]

    def recommend_bans(self,enemy_roster,enemy_picks,own_picks,banned=None,region='ALL',
                       top_k=5,protected=None,target_role=None,enemy_next_slot=None):
        enemies,own=role_dict(enemy_picks),role_dict(own_picks)
        excluded=set(banned or [])|set(enemies.values())|set(own.values())|set(protected or [])
        roles=[role_key(target_role)] if target_role else ROLES
        roles=[r for r in roles if r not in enemies]
        roster=role_dict(enemy_roster)
        snapshot,_,_=self.context(region)
        candidates={}
        for role in roles:
            picks=self.recommend_picks(role,enemies,own,excluded,roster.get(role),top_k=10000,
                                       region=region,draft_slot=enemy_next_slot)
            if not picks:continue
            for rank,pick in enumerate(picks):
                item=candidates.setdefault(pick['champion'],{'champion':pick['champion'],'denial_loss':0.0,
                                                            'enemy_priority':0.0,'target_roles':[],'reasons':[]})
                if rank==0:
                    replacement=picks[1]['score'] if len(picks)>1 else 0
                    item['denial_loss']+=max(0,pick['score']-replacement)
                item['enemy_priority']=max(item['enemy_priority'],pick['score'])
                item['target_roles'].append(role)
        rows=[]
        for item in candidates.values():
            champion=item['champion']
            presence=snapshot.presence.get(champion,0)
            # Presence dominates; a rare champion cannot win only from a percentile gap.
            score=.6*presence+.25*item['enemy_priority']+.15*min(1,item['denial_loss'])
            reason=f"Presence gần đây {presence:.1%}, bị cấm {snapshot.ban_rate.get(champion,0):.1%}; điểm ưu tiên đối thủ {item['enemy_priority']:.3f}; chênh lựa chọn {item['denial_loss']:.3f}"
            item.update(priority_pct=round(score*100,2),ban_priority=float(score),
                        score_kind='patch_aware_ban_priority_points',probability=None,
                        meta_scope=snapshot.metadata(),reason=reason,reasons=[reason],badge='CẤM THEO META/PICK ĐỐI THỦ')
            rows.append(item)
        return sorted(rows,key=lambda r:(-r['ban_priority'],-r['enemy_priority'],r['champion']))[:top_k]
