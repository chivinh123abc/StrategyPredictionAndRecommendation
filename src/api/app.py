"""Small stateless local adapter: validate draft inputs, call the existing engine."""
from functools import lru_cache
import json
import hashlib
import math
from pathlib import Path
import sys
from threading import RLock
from typing import Literal

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src/07_recommender'),str(ROOT/'src/01_data_pipeline')]
from analysis_data import load_clean_tables
from draft_advisor import DraftAdvisor,AdvisorPolicy,ROLES
from draft_meta import MetaPolicy,region_leagues
from simulate_draft_match import DraftState,draft_schedule,pick_candidates,needs_tactical_review
from ban_planner import BanPlanner
from pair_reservation import PAIR_SAFETY_VERSION
from draft_safety import role_preferences,infer_free_role,LANE_REVIEW_VERSION,MANUAL_ROLE_VERSION
from rank_data_contract import ChampionCatalog
from matchup_evidence import CATALOG

Side=Literal['blue','red']
Role=Literal['top','jng','mid','bot','sup']
Region=Literal['ALL','LCK','LPL','LCP','WLDS','MSI','EWC','INTERNATIONAL']
LOCK=RLock()


class Input(BaseModel):
    model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)


class Settings(Input):
    region:Region='WLDS'
    blue_team:str=Field(default='T1',min_length=1,max_length=80)
    red_team:str=Field(default='Gen.G',min_length=1,max_length=80)
    ban_strategy:Literal['legacy','contextual']='contextual'
    as_of:str|None=Field(default=None,pattern=r'^\d{4}-\d{2}-\d{2}$')
    allow_statistical_auto:bool=False


class Move(Input):
    side:Side
    action:Literal['ban','pick']
    champion:str=Field(min_length=1,max_length=80)
    role:Role|None=None


class Swap(Input):
    side:Side
    champion:str=Field(min_length=1,max_length=80)
    to:Role
    after_turn:int=Field(ge=1,le=20)


class Game(Input):
    first_side:Side='blue'
    history:list[Move]=Field(default_factory=list,max_length=20)
    swaps:list[Swap]=Field(default_factory=list,max_length=80)


class Session(Input):
    settings:Settings=Field(default_factory=Settings)
    completed:list[Game]=Field(default_factory=list,max_length=4)
    current:Game=Field(default_factory=Game)
    snapshot_id:str|None=Field(default=None,pattern=r'^[0-9a-f]{64}$')


class ViewRequest(Input):
    session:Session
    only_role:Role|None=None


class ActionRequest(ViewRequest):
    champion:str|None=Field(default=None,max_length=80)
    role:Role|None=None
    auto:bool=False


class SwapRequest(ViewRequest):
    side:Side
    champion:str=Field(min_length=1,max_length=80)
    target_role:Role


class ExplainRequest(ViewRequest):
    game_index:int=Field(ge=0,le=4)
    turn:int=Field(ge=1,le=20)


def clean(value):
    if isinstance(value,np.generic):return clean(value.item())
    if isinstance(value,float):return value if math.isfinite(value) else None
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,set)):return [clean(v) for v in value]
    return value


def public_advice(row):
    fields={'champion','role','priority_pct','ranking_score','games','historical','reason','reasons',
        'review_required','evidence_status','cosine_similarity','enemy_context_coverage',
        'score_components','score_kind','mechanical_counter_status','selection_basis','matchup_source_comparison','pair_reservation','lane_review'}
    return {key:value for key,value in row.items() if key in fields}


@lru_cache(maxsize=1)
def registry():
    _,matches,players=load_clean_tables()
    official=ChampionCatalog.read(CATALOG)
    payload=json.loads(CATALOG.read_text(encoding='utf-8'))
    raw_names={official.name(name):name for name in sorted(players.champion.unique())}
    roles=players.groupby('champion').position.agg(lambda x:sorted(set(x))).to_dict()
    champions=[]
    for entry in payload['data'].values():
        name=raw_names.get(entry['name'],entry['name'])
        champions.append({'name':name,'label':entry['name'],'roles':roles.get(name,[]),
            'image':f"https://ddragon.leagueoflegends.com/cdn/{official.version}/img/champion/{entry['id']}.png"})
    champions.sort(key=lambda row:row['label'].casefold())
    regions=[]
    for code in ['WLDS','LCK','LPL','LCP','MSI','EWC','INTERNATIONAL','ALL']:
        leagues=region_leagues(code)
        selected=matches if leagues is None else matches[matches.league.str.upper().isin(leagues)]
        if len(selected):regions.append({'code':code,'teams':sorted(selected.teamname.unique()),
            'games':int(selected.gameid.nunique())})
    return {'champions':champions,'regions':regions,'catalog_version':official.version,
        'rank_mode':'supplementary_evidence_only','pick_scoring':'current'}


@lru_cache(maxsize=4)
def advisor_for(region,as_of):
    source_fingerprint()
    advisor=DraftAdvisor(policy=AdvisorPolicy(candidate_min_games=1),meta_policy=MetaPolicy(as_of=as_of))
    advisor.context(region)
    return advisor


@lru_cache(maxsize=1)
def source_fingerprint():
    """Bind in-memory snapshots to the database from this server lifetime."""
    return hashlib.sha256((ROOT/'data/database/lol_live_data.db').read_bytes()).hexdigest()


def known(champion):
    if champion not in {c['name'] for c in registry()['champions']}:
        raise ValueError('Tướng không có trong danh mục đã xác nhận')


def restore(game,used):
    state=DraftState(first_side=game.first_side,used_champions=list(used))
    swaps={}
    for swap in game.swaps:
        if swap.after_turn>len(game.history):raise ValueError('Đổi vị trí nằm sau lượt draft hiện tại')
        swaps.setdefault(swap.after_turn,[]).append(swap)
    for index,move in enumerate(game.history,1):
        known(move.champion)
        if move.action=='ban' and move.role is not None:raise ValueError('Lượt ban không có vị trí')
        state.apply(move.side,move.action,move.champion,move.role)
        for swap in swaps.get(index,[]):state.swap(swap.side,swap.champion,swap.to)
    return state


def states_for(session):
    if session.settings.blue_team.strip()==session.settings.red_team.strip():raise ValueError('Hai đội cần khác tên')
    used=[];states=[]
    for game in session.completed:
        state=restore(game,used)
        if not state.complete:raise ValueError('Ván trước chưa hoàn tất 20 lượt')
        used.extend(champion for side in ['blue','red'] for champion in state.picks[side].values())
        states.append(state)
    states.append(restore(session.current,used))
    return states


def context(settings):
    advisor=advisor_for(settings.region,settings.as_of)
    snapshot=advisor.context(settings.region)[0]
    names={'blue':settings.blue_team,'red':settings.red_team};rosters={}
    for side,name in names.items():
        observed=snapshot.roster(name)
        rosters[side]=observed['players'] if observed else {}
    return advisor,snapshot,names,rosters


def recommend(state,settings,only_role=None,top_k=5):
    if state.complete:return []
    advisor,snapshot,names,rosters=context(settings)
    side,action=state.schedule[len(state.history)]
    if only_role in state.picks[side]:only_role=None
    if action=='pick':return pick_candidates(advisor,state,side,rosters[side],settings.region,only_role=only_role,
        pair_safety=settings.ban_strategy=='contextual')[:top_k]
    if settings.ban_strategy=='contextual':
        return BanPlanner(advisor,rosters,names,settings.region).recommend(state,side,top_k=top_k)
    enemy='red' if side=='blue' else 'blue'
    slot=('F' if enemy==state.first_side else 'S')+str(len(state.picks[enemy])+1)
    return advisor.recommend_bans(rosters[enemy],state.picks[enemy],state.picks[side],state.unavailable,
        region=settings.region,top_k=top_k,enemy_next_slot=slot)


def numbered(state):
    counts={side:{'ban':0,'pick':0} for side in ['blue','red']};schedule=[]
    for turn,(side,action) in enumerate(state.schedule,1):
        counts[side][action]+=1
        schedule.append({'turn':turn,'side':side,'action':action,'number':counts[side][action]})
    return schedule


def make_view(session,only_role=None):
    session=session.model_copy(deep=True)
    if session.settings.as_of is None:
        # Pin a date on the first response, rather than silently moving the
        # cutoff each time a saved browser session is reopened.
        from datetime import datetime, timezone
        session.settings.as_of=datetime.now(timezone.utc).date().isoformat()
    states=states_for(session);state=states[-1]
    advisor,snapshot,names,rosters=context(session.settings)
    source_sha256=hashlib.sha256((ROOT/'data/database/lol_live_data.db').read_bytes()).hexdigest()
    if source_sha256!=source_fingerprint():
        raise HTTPException(409,'Dữ liệu Pro đã đổi. Hãy xuất phiên cũ và khởi động lại API để nạp dữ liệu mới.')
    identity={'source_sha256':source_sha256,
              'scope':snapshot.metadata(),'pick_scoring':advisor.policy.scoring,
              'candidate_min_games':advisor.policy.candidate_min_games,'evidence_min_games':advisor.policy.min_games,
              'ban_strategy':session.settings.ban_strategy,'contextual_version':'fixed_capacity_v2',
              'pair_safety':PAIR_SAFETY_VERSION if session.settings.ban_strategy=='contextual' else None,
              'lane_review_policy':LANE_REVIEW_VERSION if session.settings.ban_strategy=='contextual' else None,
              'manual_role_policy':MANUAL_ROLE_VERSION,
              'rosters':rosters,'teams':names}
    snapshot_id=hashlib.sha256(json.dumps(identity,sort_keys=True,default=str).encode()).hexdigest()
    if session.snapshot_id and session.snapshot_id!=snapshot_id:
        raise HTTPException(409,'Dữ liệu hoặc cấu hình phiên đã thay đổi. Hãy xuất phiên cũ và tạo phiên mới để tránh trộn kết quả.')
    session.snapshot_id=snapshot_id
    current=None if state.complete else numbered(state)[len(state.history)]
    if current and only_role in state.picks[current['side']]:only_role=None
    return clean({'session':session.model_dump(),'games':[s.as_dict() for s in states],
        'game_number':len(states),'turn':current,'schedule':numbered(state),
        'recommendations':[public_advice(row) for row in recommend(state,session.settings,only_role)],
        'scope':snapshot.metadata(),'rosters':rosters,'only_role':only_role,
        'role_preferences':role_preferences(snapshot),
        'configuration':{'pick_scoring':advisor.policy.scoring,'ban_strategy':session.settings.ban_strategy,
                         'contextual_version':'fixed_capacity_v2','snapshot_id':snapshot_id,
                         'pair_safety':PAIR_SAFETY_VERSION if session.settings.ban_strategy=='contextual' else None,
                         'lane_review_policy':LANE_REVIEW_VERSION if session.settings.ban_strategy=='contextual' else None,
                         'manual_role_policy':MANUAL_ROLE_VERSION},
        'candidate_min_games':advisor.policy.candidate_min_games,'evidence_min_games':advisor.policy.min_games,
        'series_complete':len(states)==5 and state.complete,
        'score_notice':'Điểm ưu tiên thống kê, không phải xác suất thắng hoặc counter đã xác nhận.'})


app=FastAPI(title='Draft Lab local API',version='0.1.0')


@app.exception_handler(ValueError)
async def bad_input(request,exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=400,content={'detail':str(exc)})


@app.get('/api/health')
def health():return {'status':'ok','mode':'local_pro_draft','pick_scoring':'current'}


@app.get('/api/catalog')
def catalog():
    with LOCK:return registry()


@app.post('/api/draft/view')
def view(payload:ViewRequest):
    with LOCK:return make_view(payload.session,payload.only_role)


@app.post('/api/draft/action')
def action(payload:ActionRequest):
    with LOCK:
        session=payload.session.model_copy(deep=True);state=states_for(session)[-1]
        if state.complete:raise ValueError('Ván đã hoàn tất')
        side,kind=state.schedule[len(state.history)]
        champion,role=payload.champion,payload.role
        if payload.auto:
            rows=recommend(state,session.settings,payload.only_role)
            if not rows:raise ValueError('Chưa có gợi ý đủ điều kiện; hãy chọn tay')
            selected=rows[0];champion=selected['champion'];role=selected.get('role')
            enemy='red' if side=='blue' else 'blue'
            if kind=='pick' and needs_tactical_review(selected,state.picks[enemy],session.settings.allow_statistical_auto):
                reason=selected.get('lane_review',{}).get('reason') or selected.get('pair_reservation',{}).get('reason')
                raise HTTPException(409,(reason+' ' if reason else '')+'Gợi ý cần xem lại bằng chứng; hãy chọn tay hoặc bật chế độ test.')
        if not champion:raise ValueError('Hãy chọn một tướng')
        known(champion)
        if kind=='pick' and role is None:
            role=infer_free_role(context(session.settings)[1],champion,state.picks[side])
        state.apply(side,kind,champion,role)
        session.current.history.append(Move(side=side,action=kind,champion=champion,role=role))
        return make_view(session,payload.only_role)


@app.post('/api/draft/swap')
def swap(payload:SwapRequest):
    with LOCK:
        session=payload.session.model_copy(deep=True);state=states_for(session)[-1]
        state.swap(payload.side,payload.champion,payload.target_role)
        session.current.swaps.append(Swap(side=payload.side,champion=payload.champion,to=payload.target_role,after_turn=len(state.history)))
        return make_view(session,payload.only_role)


@app.post('/api/draft/explain')
def explain(payload:ExplainRequest):
    """Recompute a past choice from its pre-action state; never trust client scores."""
    with LOCK:
        states=states_for(payload.session)
        if payload.game_index>=len(states):raise ValueError('Ván không tồn tại')
        original=states[payload.game_index]
        if payload.turn>len(original.history):raise ValueError('Lượt chưa diễn ra')
        games=[*payload.session.completed,payload.session.current];game=games[payload.game_index]
        previous=game.model_copy(deep=True)
        previous.history=previous.history[:payload.turn-1]
        previous.swaps=[s for s in previous.swaps if s.after_turn<payload.turn]
        before=restore(previous,original.used_champions)
        move=original.history[payload.turn-1]
        advisor,_,names,rosters=context(payload.session.settings)
        if move['action']=='pick':
            enemy='red' if move['side']=='blue' else 'blue'
            slot=('F' if move['side']==before.first_side else 'S')+str(len(before.picks[move['side']])+1)
            rows=advisor.recommend_picks(move['role'],before.picks[move['side']],before.picks[enemy],before.unavailable,
                rosters[move['side']].get(move['role']),region=payload.session.settings.region,top_k=10000,draft_slot=slot)
        else:rows=recommend(before,payload.session.settings,top_k=10000)
        selected=next((r for r in rows if r['champion']==move['champion']),None)
        if selected and move['action']=='pick' and payload.session.settings.ban_strategy=='contextual':
            guarded=pick_candidates(advisor,before,move['side'],rosters[move['side']],
                payload.session.settings.region,only_role=move['role'],pair_safety=True)
            selected=next((r for r in guarded if r['champion']==move['champion']),selected)
        return clean({'move':move,'advice':public_advice(selected) if selected else None,'notice':None if selected else 'Lựa chọn tay ngoài pool gợi ý có dữ liệu; không tạo điểm giả.'})


dist=ROOT/'web/dist'
if dist.exists():app.mount('/',StaticFiles(directory=dist,html=True),name='ui')
