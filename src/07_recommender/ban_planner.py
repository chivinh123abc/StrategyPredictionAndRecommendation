"""Contextual one-step ban scoring; no response-tree search.

Pool loss and self-denial are draft-priority heuristics, not win probabilities.
"""
from copy import deepcopy
from dataclasses import dataclass,asdict
from time import perf_counter
import numpy as np
from draft_advisor import ROLES


@dataclass(frozen=True)
class ContextualBanPolicy:
    pool_top_k:int=3
    own_cost_weight:float=1.

    def __post_init__(self):
        if not isinstance(self.pool_top_k,int) or self.pool_top_k<1:
            raise ValueError('Pool top-k must be a positive integer')
        if not np.isfinite(self.own_cost_weight) or self.own_cost_weight<0:
            raise ValueError('Invalid own-cost weight')


class BanPlanner:
    def __init__(self,advisor,rosters,names,region,policy=None):
        self.advisor=advisor;self.rosters=deepcopy(rosters);self.names=dict(names);self.region=region
        self.policy=policy or ContextualBanPolicy()
        self.snapshot=advisor.context(region)[0]
        self._rank_cache={};self._context_cache={}

    @staticmethod
    def other(side):return 'red' if side=='blue' else 'blue'

    def slot(self,state,side):
        return ('F' if side==state.first_side else 'S')+str(len(state.picks[side])+1)

    def rank_role(self,state,side,role):
        """Score once without exclusions, then filter; never cache a mutable state."""
        enemy=self.other(side);own=state.picks[side];opp=state.picks[enemy]
        key=(side,role,tuple(sorted(own.items())),tuple(sorted(opp.items())),self.slot(state,side))
        if key not in self._rank_cache:
            self._rank_cache[key]=self.advisor.recommend_picks(role,own,opp,player_name=self.rosters[side].get(role),
                                    region=self.region,draft_slot=self.slot(state,side),top_k=10000)
        return [r for r in self._rank_cache[key] if r['champion'] not in state.unavailable]

    def pools(self,state,side):
        result={}
        for role in ROLES:
            if role in state.picks[side]:continue
            ranked=self.rank_role(state,side,role)
            # Sparse choices remain explicitly a backoff, never silently replace
            # well-supported candidates just because an isolated score is large.
            supported=[r for r in ranked if r.get('evidence_status')!='sparse_candidate']
            effective=supported or ranked
            result[role]=effective
        return result

    def pool_value(self,rows):
        selected=rows[:self.policy.pool_top_k]
        return float(np.mean([r['score'] for r in selected])) if selected else 0.

    def access_before_enemy(self,state,side):
        # Derive acquisition order from actual schedule, including phase2 and
        # first-pick independent of map color; no Blue-first assumption.
        for actor,action in state.schedule[len(state.history)+1:]:
            if action=='pick':return actor==side
        return False

    def contextual(self,state,side,protected=None,target_role=None):
        key=(side,tuple(sorted(state.picks['blue'].items())),tuple(sorted(state.picks['red'].items())),
             tuple(sorted(state.unavailable)),len(state.history),tuple(sorted(protected or [])),target_role)
        if key in self._context_cache:return self._context_cache[key]
        enemy=self.other(side);own=self.pools(state,side);opp=self.pools(state,enemy)
        legal={r['champion'] for values in opp.values() for r in values}
        legal-=set(protected or [])
        if target_role:legal&={r['champion'] for r in opp.get(target_role,[])}
        first_access=self.access_before_enemy(state,side)
        rows=[]
        for champ in sorted(legal):
            components={};enemy_loss=0.;own_loss=0.;scarcity=0.
            for tag,pool in [('enemy',opp),('own',own)]:
                for role,values in pool.items():
                    after=[r for r in values if r['champion']!=champ]
                    loss=max(0.,self.pool_value(values)-self.pool_value(after))
                    # A cheap backup becoming the only remaining choice is
                    # visible through the top-k mean and role count, not tier tables.
                    if tag=='enemy':
                        enemy_loss+=loss
                        if len(after)<len(values):scarcity+=1/max(1,len(values))
                    else:own_loss+=loss
                    if len(after)<len(values):
                        components[f'{tag}:{role}']={'before_options':len(values),'after_options':len(after),
                            'before_top':[r['champion'] for r in values[:3]],'after_top':[r['champion'] for r in after[:3]],
                            'before_value':self.pool_value(values),'after_value':self.pool_value(after),'loss':loss}
            # Being first to acquire a shared high-priority champion makes its
            # self-denial more expensive. If second, enemy acquisition is likelier.
            own_access_cost=own_loss*(1. if first_access else .5)
            score=(enemy_loss-self.policy.own_cost_weight*own_access_cost)/5
            rows.append({'champion':champ,'contextual_score':float(score),'enemy_pool_loss':enemy_loss/5,
                         'own_pool_loss':own_loss/5,'own_access_cost':own_access_cost/5,
                         'own_next_pick_before_enemy':first_access,'enemy_role_scarcity':scarcity,
                         'pool_impact':components,'first_pick_side':state.first_side,
                         'fearless_locked_count':len(state.used_champions)})
        result=sorted(rows,key=lambda r:(-r['contextual_score'],-r['enemy_role_scarcity'],r['champion']))
        self._context_cache[key]=result
        return result

    def actions(self,state,side):
        if state.schedule[len(state.history)][1]=='pick':return self.picks(state,side)
        return [{**r,'role':None} for r in self.contextual(state,side)]

    def recommend(self,state,side,mode='contextual',protected=None,target_role=None,top_k=5):
        if mode!='contextual':raise ValueError('Only contextual ban scoring is supported')
        if state.complete or state.schedule[len(state.history)]!=(side,'ban'):
            raise ValueError('Contextual ban scoring called on wrong turn')
        start=perf_counter()
        rows=self.contextual(state,side,protected,target_role)
        ranked=[]
        for candidate in rows:
            item=deepcopy(candidate);score=item['contextual_score']
            reason=(f"Mất pool địch {item['enemy_pool_loss']:.4f}; chi phí tự cấm {item['own_access_cost']:.4f}; "
                    f"đội mình lấy lượt pick tới trước địch={item['own_next_pick_before_enemy']}; "
                    f"Fearless khóa {item['fearless_locked_count']}; chấm theo pool ngữ cảnh")
            item.update(score_kind='contextual_ban_priority_not_probability',ban_priority=float(score),
                        priority_pct=round(score*100,3),probability=None,denial_loss=item['enemy_pool_loss'],
                        contextual_policy=asdict(self.policy),meta_scope=self.snapshot.metadata(),
                        target_roles=[k.split(':')[1]for k in item['pool_impact']if k.startswith('enemy:')],
                        reason=reason,reasons=[reason],badge='CẤM THEO NGỮ CẢNH')
            ranked.append(item)
        summary=[{k:r[k]for k in ['champion','ban_priority','contextual_score','enemy_pool_loss','own_access_cost']}for r in ranked]
        public_state={'first_pick_side':state.first_side,'picks':deepcopy(state.picks),'bans':deepcopy(state.bans),
                      'used_champions':list(state.used_champions),'history':[
                          {k:h.get(k)for k in ['turn','side','action','champion','role']}for h in state.history]}
        trace={'mode':'contextual','state':public_state,'root_side':side,'legal_candidates':len(rows),
               'candidate_summary':summary,'elapsed_seconds':perf_counter()-start,'policy':asdict(self.policy),
               'limitations':['One-step pool heuristic; no opponent-response search or full BO5 planning.',
                              'Priority is not mechanical-counter evidence or game win probability.']}
        for item in ranked:item['contextual_trace']=trace
        return ranked[:top_k]
