"""Interactive single-game ban/pick with contextual historical + content advice."""
from dataclasses import dataclass, field
from pathlib import Path
import argparse
import json
import sys
from itertools import combinations

PROJECT_ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(PROJECT_ROOT),str(PROJECT_ROOT/'src/06_machine_learning'),str(Path(__file__).resolve().parent)]
from recommender_engine import RecommenderEngine, normalize_region_code
from draft_advisor import DraftAdvisor, ROLES, role_key, DISPLAY_ROLES
from draft_meta import MetaPolicy

# Presets are editable demo rosters, not a live roster service.
TEAM_PRESETS = {
    "T1": {'top': 'Doran', 'jng': 'Oner', 'mid': 'Faker', 'bot': 'Peyz', 'sup': 'Keria'},
    "GEN.G": {'top': 'Kiin', 'jng': 'Canyon', 'mid': 'Chovy', 'bot': 'Ruler', 'sup': 'Lehends'},
    "GAM": {'top': 'Kiaya', 'jng': 'Levi', 'mid': 'Emo', 'bot': 'Easylove', 'sup': 'Elio'},
    "BLG": {'top': 'Bin', 'jng': 'Xun', 'mid': 'Knight', 'bot': 'Elk', 'sup': 'ON'},
    "HLE": {'top': 'Zeus', 'jng': 'Peanut', 'mid': 'Zeka', 'bot': 'Viper', 'sup': 'Delight'},
    "TES": {'top': '369', 'jng': 'Tian', 'mid': 'Creme', 'bot': 'JackeyLove', 'sup': 'Meiko'},
    "ĐỘI VÔ DANH": {'top': 'Tân Binh Top', 'jng': 'Tân Binh Rừng', 'mid': 'Tân Binh Mid', 'bot': 'Tân Binh AD', 'sup': 'Tân Binh SP'},
    "UNDERDOG": {'top': 'Tân Binh Top', 'jng': 'Tân Binh Rừng', 'mid': 'Tân Binh Mid', 'bot': 'Tân Binh AD', 'sup': 'Tân Binh SP'},
    "CHALLENGER": {'top': 'Ẩn Danh Top', 'jng': 'Ẩn Danh Rừng', 'mid': 'Ẩn Danh Mid', 'bot': 'Ẩn Danh AD', 'sup': 'Ẩn Danh SP'}
}

LANE_TITLE={'top':'Top','jng':'Rừng','mid':'Mid','bot':'Xạ thủ','sup':'Hỗ trợ'}


def needs_tactical_review(choice,enemy_picks,allow_statistical_auto=False):
    """Do not auto-finalize a full-team response without supported enemy evidence."""
    return bool(not allow_statistical_auto and len(enemy_picks)==5 and
                choice.get('review_required',False))


def draft_schedule(first_side='blue'):
    if first_side not in ['blue','red']:raise ValueError('Invalid first-pick side')
    a,b=first_side,('red' if first_side=='blue' else 'blue')
    return ([(s,'ban') for s in [a,b,a,b,a,b]]+
            [(s,'pick') for s in [a,b,b,a,a,b]]+
            [(s,'ban') for s in [b,a,b,a]]+
            [(s,'pick') for s in [b,a,a,b]])


@dataclass
class DraftState:
    first_side:str='blue'
    picks:dict=field(default_factory=lambda:{'blue':{},'red':{}})
    bans:dict=field(default_factory=lambda:{'blue':[],'red':[]})
    history:list=field(default_factory=list)
    swaps:list=field(default_factory=list)
    used_champions:list=field(default_factory=list)

    @property
    def schedule(self):return draft_schedule(self.first_side)
    @property
    def complete(self):return len(self.history)==len(self.schedule)
    @property
    def unavailable(self):return set(self.used_champions+self.bans['blue']+self.bans['red']+list(self.picks['blue'].values())+list(self.picks['red'].values()))

    def apply(self,side,action,champion,role=None):
        if self.complete or (side,action)!=self.schedule[len(self.history)]:raise ValueError('Sai lượt cấm/chọn')
        if not champion or champion in self.unavailable:raise ValueError('Tướng đã cấm/chọn hoặc tên không hợp lệ')
        if action=='pick':
            role=role_key(role)
            if role in self.picks[side]:raise ValueError('Vị trí đã có tướng; dùng swap để đổi trước')
            self.picks[side][role]=champion
        else:self.bans[side].append(champion)
        self.history.append({'turn':len(self.history)+1,'side':side,'action':action,'champion':champion,'role':role})

    def swap(self,side,champion,target_role):
        role=role_key(target_role)
        current=next((r for r,c in self.picks[side].items() if c==champion),None)
        if current is None:raise ValueError('Tướng chưa được đội bạn chọn')
        other=self.picks[side].get(role)
        if current==role:return
        self.picks[side][role]=champion
        if other:self.picks[side][current]=other
        else:del self.picks[side][current]
        self.swaps.append({'after_turn':len(self.history),'side':side,'champion':champion,'from':current,'to':role})

    def as_dict(self):
        return {'first_pick_side':self.first_side,'picks':self.picks,'bans':self.bans,
                'history':self.history,'swaps':self.swaps,'complete':self.complete,'used_champions':self.used_champions}


def roster_for(name):
    return dict(TEAM_PRESETS.get(name.upper(),{r:f'{name}_{r}' for r in ROLES}))


def pick_candidates(advisor,state,side,roster,region,wishlist=None,only_role=None):
    enemy='red' if side=='blue' else 'blue'
    roles=[role_key(only_role)] if only_role else ROLES
    roles=[r for r in roles if r not in state.picks[side]]
    all_rows=[]
    for role in roles:
        slot=('F' if side==state.first_side else 'S')+str(len(state.picks[side])+1)
        rows=advisor.recommend_picks(role,state.picks[side],state.picks[enemy],state.unavailable,
                                    roster.get(role),top_k=5,region=region,seeds=wishlist,draft_slot=slot)
        for row in rows:
            row={**row,'role':role,'lane_title':LANE_TITLE[role],
                 'priority_pct':row['ranking_score'],'player':roster.get(role),
                 'user_preference':row['champion'] in (wishlist or [])}
            row['alternatives_same_role']=[{k:r[k] for k in ['champion','ranking_score','games','enemy_context_coverage',
                'mechanical_counter_status','evidence_status']} for r in rows if r['champion']!=row['champion']][:3]
            all_rows.append(row)
    # Keep multiple role assignments for a flex champion; UI specifies each role.
    all_rows.sort(key=lambda r:(not r['user_preference'],r.get('evidence_status')=='sparse_candidate',-r['score'],-r['games'],r['champion'],r['role']))
    if only_role:return all_rows[:5]
    result=[]
    # Give every open role an entry, then fill with highest-ranked remaining pairs.
    for role in roles:
        best=next((r for r in all_rows if r['role']==role),None)
        if best:result.append(best)
    keys={(r['champion'],r['role']) for r in result}
    for row in all_rows:
        if (row['champion'],row['role']) not in keys:
            result.append(row);keys.add((row['champion'],row['role']))
        if len(result)>=8:break
    return sorted(result,key=lambda r:(not r['user_preference'],r.get('evidence_status')=='sparse_candidate',-r['score'],-r['games'],r['champion'],r['role']))


def show_board(state,names):
    print('\n'+'='*90)
    for side in ['blue','red']:
        slots=' | '.join(f"{LANE_TITLE[r]}: {state.picks[side].get(r,'—')}" for r in ROLES)
        print(f"{side.upper()} {names[side]} | Cấm: {', '.join(state.bans[side]) or '—'}")
        print(slots)


def show_candidates(rows,action):
    for i,row in enumerate(rows,1):
        role=f" [{row['lane_title']}: {row.get('player')}]" if action=='pick' else ''
        points=row.get('priority_pct',0)
        preference=' | ưu tiên do bạn đặt' if row.get('user_preference') else ''
        print(f" [{i}] {row['champion']}{role} | {points:.2f} điểm{preference}")
        if action=='pick':
            print(f"     n={row['games']} trận; {row['reasons'][1]}")
            if row.get('review_required'):print('     Cần xem lại chiến thuật: chưa có đối đầu đủ mẫu với đội địch đã lộ; không xác nhận counter.')
            if row.get('cosine_similarity') is not None:print(f"     Cosine={row['cosine_similarity']:.3f} (độ tương đồng)")
        else:print('     '+row['reason'])
    if not rows:print(' Chưa đủ lịch sử để gợi ý. Có thể nhập tướng và vị trí trực tiếp hoặc đổi khu vực.')


def explain(row):
    for text in row.get('reasons',[row.get('reason','')]):print('  • '+text)
    if row.get('contextual_trace'):
        trace=row['contextual_trace']
        print(f"  • Contextual: xét {trace['legal_candidates']} ứng viên hợp lệ, không tìm nhánh phản ứng.")
        for c in trace['candidate_summary'][:3]:
            print(f"  • {c['champion']}: điểm {c['ban_priority']:.5f}, mất pool địch {c['enemy_pool_loss']:.5f}, tự cấm {c['own_access_cost']:.5f}")
    for name,part in row.get('score_components',{}).items():
        if name=='composition':
            print(f"  • composition: geometric lift {row.get('composition_lift',1):.3f}, số mũ {part['weight']:g}; điều chỉnh odds điểm nền, không cộng vào điểm trung bình")
        else:print(f"  • {name}: {part['value']:.3f} × trọng số {part['weight']:g}")
    print('  Điểm là heuristic tham khảo; không phải xác suất hay mức tăng thắng.')


def choose_interactively(candidates,refresh,state,side,action,engine,advisor,region,input_fn=input):
    rows=candidates
    valid=set(advisor.history.players.champion.unique())|set(engine.pick_recommender.metadata)
    while True:
        try:raw=input_fn('Chọn số/Enter; tên tướng hoặc "mid Ahri"; role; why 1; swap Ahri top; auto; quit: ').strip()
        except (EOFError,KeyboardInterrupt):return None,'quit'
        low=raw.lower()
        if low in ['quit','exit','q']:return None,'quit'
        if low=='auto':return (rows[0] if rows else None),'auto'
        if low in ['help','?']:
            print('Enter chọn gợi ý đầu; top/jng/mid/bot/sup lọc vị trí; all xem mọi vị trí; why N xem bằng chứng.');continue
        if low=='all' or low in ['top','jng','jungle','mid','bot','adc','sup','support','sp']:
            role=None if low=='all' else ('sup' if low=='sp' else role_key(low))
            rows=refresh(role);show_candidates(rows,action);continue
        if low.startswith('why '):
            token=raw.split()[-1]
            if token.isdigit() and 1<=int(token)<=len(rows):explain(rows[int(token)-1])
            else:print('Số gợi ý không hợp lệ')
            continue
        if low.startswith('swap ') or low.startswith('doi '):
            if action!='pick':print('Đổi vị trí trong lượt chọn của bạn.');continue
            try:
                champ_text,role=raw.split(maxsplit=1)[1].rsplit(maxsplit=1)
                champ=engine.pick_recommender._normalize_champion_name(champ_text)
                state.swap(side,champ,'sup' if role=='sp' else role)
                rows=refresh(None);show_candidates(rows,action)
            except ValueError as exc:print(str(exc))
            continue
        if not raw or raw.isdigit():
            index=0 if not raw else int(raw)-1
            if 0<=index<len(rows):return rows[index],'pick'
            print('Số gợi ý không hợp lệ');continue
        role=None;champ_text=raw
        words=raw.split(maxsplit=1)
        if len(words)==2 and words[0].lower() in ['top','jng','jungle','mid','bot','adc','sup','support','sp']:
            role='sup' if words[0].lower()=='sp' else role_key(words[0])
            champ_text=words[1]
        champ=engine.pick_recommender._normalize_champion_name(champ_text)
        if champ not in valid:print('Không nhận diện được tướng');continue
        if champ in state.unavailable:print('Tướng đã cấm/chọn');continue
        if action=='ban':return {'champion':champ,'score_kind':'user_choice_unscored'},'pick'
        available=[r for r in ROLES if r not in state.picks[side]]
        if role is None:
            base,_,_,_=advisor.history.stats(region)
            observed=[(base.get((r,champ),(0,0))[1],r) for r in available]
            if observed and max(observed)[0]>0:role=max(observed)[1]
        if role not in available:
            print('Hãy ghi rõ vị trí còn trống, ví dụ "mid Ahri", hoặc swap trước.');continue
        return {'champion':champ,'role':role,'score_kind':'user_choice_unscored'},'pick'


def run_pro_tournament_draft_simulation(blue_team_name='T1',red_team_name='GEN.G',
                                        blue_roster=None,red_roster=None,user_side='blue',
                                        first_side='blue',wishlist=None,interactive=True,region='ALL',
                                        input_fn=input,save_session=None,engine=None,advisor=None,
                                        meta_policy=None,max_data_age_days=None,used_champions=None,opponent_model_path=None,
                                        allow_statistical_auto=False,ban_strategy='legacy'):
    if user_side not in ['blue','red']:raise ValueError('Phe điều khiển phải là blue hoặc red')
    print('Đang nạp lịch sử trận đấu và hồ sơ tướng...',flush=True)
    engine=engine or RecommenderEngine()
    advisor=advisor or DraftAdvisor(db_path=engine.pick_recommender.db_path,meta_policy=meta_policy)
    state=DraftState(first_side=first_side,used_champions=[engine.pick_recommender._normalize_champion_name(c) for c in used_champions or []])
    names={'blue':blue_team_name,'red':red_team_name}
    reg=normalize_region_code(region)
    snapshot,_,_=advisor.context(reg)
    scope=snapshot.metadata()
    predictor=None
    if opponent_model_path:
        from opponent_model import OpponentModel,public_simulation_state
        predictor=OpponentModel.load(opponent_model_path)
        if predictor.evaluation['region'].upper()!=reg:raise ValueError('Opponent model region does not match this session')
    if max_data_age_days is not None and scope['staleness_days']>max_data_age_days:
        raise ValueError(f"Dữ liệu {reg} cũ {scope['staleness_days']} ngày, vượt giới hạn {max_data_age_days}; cần cập nhật dữ liệu.")
    rosters={};roster_sources={}
    for side,explicit in [('blue',blue_roster),('red',red_roster)]:
        observed=snapshot.roster(names[side]) if not explicit else None
        rosters[side]=explicit or (observed['players'] if observed else roster_for(names[side]))
        roster_sources[side]=observed or {'kind':'explicit_user_roster' if explicit else 'demo_roster_no_recent_observation'}
    if ban_strategy not in ['legacy','contextual']:raise ValueError('Invalid ban strategy')
    ban_planner=None
    if ban_strategy!='legacy':
        from ban_planner import BanPlanner
        ban_planner=BanPlanner(advisor,rosters,names,reg)
    preferred=[engine.pick_recommender._normalize_champion_name(c) for c in wishlist or []]
    auto=not interactive
    manual_review=None
    print('GIẢ LẬP BAN/PICK MỘT VÁN — LỊCH SỬ + CONTENT-BASED')
    print(f"Bạn: {user_side}; phe chọn trước: {first_side}; dữ liệu: {reg}")
    print(f"SNAPSHOT LỊCH SỬ: patch dataset {scope['dataset_patch']}, dữ liệu đến {scope['data_through']}, cũ {scope['staleness_days']} ngày so với mốc yêu cầu")
    print(f"{scope['history_games']} trận trong cửa sổ {scope['lookback_days']} ngày, {scope['patch_games']} trận patch đích; không gọi là live meta.")
    for side in ['blue','red']:
        print(f"Lineup {names[side]} ({roster_sources[side]['kind']}): "+', '.join(f'{r}={p}' for r,p in rosters[side].items()))
    print('Ưu tiên presence/nhịp draft gần đây; bể tướng, đối đầu và cosine là tín hiệu hỗ trợ. Điểm không phải xác suất.')
    while not state.complete:
        side,action=state.schedule[len(state.history)]
        enemy='red' if side=='blue' else 'blue'
        forecast=None
        if predictor:
            forecast={'state':public_simulation_state(state,names,scope,reg),
                      'trained_through':predictor.train_through}
            forecast['predictions']=predictor.rank(forecast['state'])
            print('Dự đoán hành động kế tiếp (không phải lựa chọn tối ưu): '+', '.join(r['champion'] for r in forecast['predictions']))
        seeds=preferred if side==user_side else []
        def refresh(role=None):
            if action=='pick':return pick_candidates(advisor,state,side,rosters[side],reg,seeds,role)
            if ban_planner:return ban_planner.recommend(state,side,mode=ban_strategy,protected=seeds,target_role=role)
            enemy_slot=('F' if enemy==state.first_side else 'S')+str(len(state.picks[enemy])+1)
            return advisor.recommend_bans(rosters[enemy],state.picks[enemy],state.picks[side],state.unavailable,
                                           reg,top_k=5,protected=seeds,target_role=role,enemy_next_slot=enemy_slot)
        rows=refresh()
        show_board(state,names)
        print(f"\nLƯỢT {len(state.history)+1}/20: {side.upper()} {names[side]} — {'CẤM' if action=='ban' else 'CHỌN'}")
        if not auto and side==user_side:
            show_candidates(rows,action)
            chosen,mode=choose_interactively(rows,refresh,state,side,action,engine,advisor,reg,input_fn)
            if mode=='quit':break
            if mode=='auto':auto=True
        else:chosen=rows[0] if rows else None
        if chosen is None:
            print('Dừng: không có lựa chọn được dữ liệu hỗ trợ. Hãy chạy lại với khu vực rộng hơn hoặc chọn thủ công.');break
        if action=='pick' and (auto or side!=user_side) and needs_tactical_review(chosen,state.picks[enemy],allow_statistical_auto):
            manual_review={'turn':len(state.history)+1,'side':side,'role':chosen['role'],
                           'candidate':chosen['champion'],'reason':'no_supported_enemy_context_with_full_enemy_team',
                           'alternatives':chosen.get('alternatives_same_role',[]),
                           'counter_status':'not_established','enemy_revealed':dict(state.picks[enemy])}
            print('DỪNG TỰ CHỌN: đội địch đã lộ đủ nhưng không có đối đầu đủ mẫu cho ứng viên dẫn đầu. Cần chọn tay/xem lại chiến thuật; không xác nhận counter.')
            print('Ứng viên điểm cao:',chosen['champion'],'| phương án khác:',', '.join(r['champion'] for r in manual_review['alternatives']))
            break
        state.apply(side,action,chosen['champion'],chosen.get('role'))
        if forecast:state.history[-1]['next_action_forecast']=forecast
        state.history[-1]['advice']={k:chosen[k] for k in ['score_kind','ranking_score','score_components','score_formula','base_priority','composition_lift','evidence_status','enemy_context_evidence','enemy_context_coverage','mechanical_counter_status','selection_basis','review_required','alternatives_same_role','denial_loss','ban_priority','cosine_similarity','games','historical','matchup','matchup_candidates','composition_evidence','synergies','player_history','reasons','reason','draft_slot','meta_scope','contextual_score','pool_impact','enemy_pool_loss','own_pool_loss','own_access_cost','own_next_pick_before_enemy','fearless_locked_count','contextual_trace','contextual_policy'] if k in chosen}
        print(f"ĐÃ {'CẤM' if action=='ban' else 'CHỌN'}: {chosen['champion']}"+(f" [{chosen['role']}]" if action=='pick' else ''))
        if action=='ban' and chosen.get('reason'):print('  Căn cứ: '+chosen['reason'])
        elif chosen.get('reasons'):print('  Căn cứ: '+chosen['reasons'][1])
    show_board(state,names)
    composition_summary={}
    for side,picks in state.picks.items():
        pairs=[snapshot.pair_evidence(r1,picks[r1],r2,picks[r2],advisor.policy.min_games)
               for r1,r2 in combinations(ROLES,2) if r1 in picks and r2 in picks]
        composition_summary[side]={'pairs':pairs,'observed_pairs':sum(e['status']=='observed_pair' for e in pairs),
                                   'sparse_pairs':sum(e['status']=='sparse_pair' for e in pairs),
                                   'unobserved_pairs':sum(e['status']=='unobserved_pair' for e in pairs),
                                   'insufficient_anchor_pairs':sum(e['status']=='insufficient_anchor_history' for e in pairs)}
        print(f"Căn cứ cặp {names[side]}: "+', '.join(f"{key}={value}" for key,value in composition_summary[side].items() if key!='pairs'))
    if state.complete:
        _display_summary_and_win_conditions(names['blue'],names['red'],state.picks['blue'],state.picks['red'],rosters['blue'],rosters['red'],engine,reg,
                                           show_prediction=advisor.meta_policy.as_of is None)
    else:print('Phiên dừng trước khi hoàn thành; chưa tính dự báo đội hình cuối.')
    result={**state.as_dict(),'teams':names,'rosters':rosters,'region':reg,'policy':advisor.policy.weights,
            'manual_review':manual_review,'allow_statistical_auto':allow_statistical_auto,
            'candidate_min_games':advisor.policy.candidate_min_games,'evidence_min_games':advisor.policy.min_games,
            'objective':'patch_aware_presence_draft_order_role_pair_context','causal_uplift':None,
            'composition_summary':composition_summary,
            'ban_strategy':ban_strategy,
            'meta_scope':scope,'roster_sources':roster_sources,'ban_policy':{'presence':.6,'enemy_priority':.25,'gap':.15}}
    if save_session:
        path=Path(save_session)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print('Đã lưu phiên:',path)
    return result


def _display_summary_and_win_conditions(blue_team_name, red_team_name, blue_picks, red_picks, blue_roster, red_roster, engine, reg_code='ALL',show_prediction=True):
    blue_final = [blue_picks['top'], blue_picks['jng'], blue_picks['mid'], blue_picks['bot'], blue_picks['sup']]
    red_final = [red_picks['top'], red_picks['jng'], red_picks['mid'], red_picks['bot'], red_picks['sup']]

    print("\n" + "=" * 95)
    print("📋 BẢNG ĐỘI HÌNH HOÀN THIỆN SAU KHI CẤM/CHỌN (FINAL DRAFT)")
    print("=" * 95)
    print(f"🔷 PHE XANH ({blue_team_name}):")
    print(f"   • TOP: {blue_picks['top']} ({blue_roster['top']})")
    print(f"   • JNG: {blue_picks['jng']} ({blue_roster['jng']})")
    print(f"   • MID: {blue_picks['mid']} ({blue_roster['mid']})")
    print(f"   • BOT: {blue_picks['bot']} ({blue_roster['bot']})")
    print(f"   • SUP: {blue_picks['sup']} ({blue_roster['sup']})")

    print(f"\n🔴 PHE ĐỎ ({red_team_name}):")
    print(f"   • TOP: {red_picks['top']} ({red_roster['top']})")
    print(f"   • JNG: {red_picks['jng']} ({red_roster['jng']})")
    print(f"   • MID: {red_picks['mid']} ({red_roster['mid']})")
    print(f"   • BOT: {red_picks['bot']} ({red_roster['bot']})")
    print(f"   • SUP: {red_picks['sup']} ({red_roster['sup']})")

    print('Radar và thẻ chiến thuật dùng thuộc tính/quy tắc chuyên gia; chưa được xác nhận như điều kiện thắng nhân quả.')
    # 1. Thẻ Điều Kiện Thắng Phe Xanh
    blue_win_res = engine.win_condition_engine.analyze_team_win_condition(blue_final)
    print("\n" + "─" * 38 + f" THẺ CHIẾN THUẬT: {blue_team_name.upper()} (BLUE) " + "─" * 38)
    print(f"🏆 Trường phái: [{blue_win_res['archetype_name'].upper()}]")
    print(f"📊 Radar 5 trục: Early: {blue_win_res['radar_scores']['Early_Power']} | Scaling: {blue_win_res['radar_scores']['Scaling']} | Combat: {blue_win_res['radar_scores']['Teamfight_AOE']} | Pick: {blue_win_res['radar_scores']['Pick_Potential']} | Obj: {blue_win_res['radar_scores']['Objective_Control']}")
    b_card = blue_win_res['win_condition_card']
    print(f"⭐ Chủ lực (Core Carry): {b_card['core_carry']}")
    print(f"⏱️ Điểm rơi sức mạnh: {b_card['power_spike_timing']}")
    print(f"🐉 Mục tiêu số 1: {b_card['primary_objective']}")
    print(f"✅ Điều kiện thắng: {b_card['win_condition']}")
    print(f"❌ Cần tránh: {b_card['critical_lose_condition']}")

    # 2. Thẻ Điều Kiện Thắng Phe Đỏ
    red_win_res = engine.win_condition_engine.analyze_team_win_condition(red_final)
    print("\n" + "─" * 38 + f" THẺ CHIẾN THUẬT: {red_team_name.upper()} (RED) " + "─" * 38)
    print(f"🏆 Trường phái: [{red_win_res['archetype_name'].upper()}]")
    print(f"📊 Radar 5 trục: Early: {red_win_res['radar_scores']['Early_Power']} | Scaling: {red_win_res['radar_scores']['Scaling']} | Combat: {red_win_res['radar_scores']['Teamfight_AOE']} | Pick: {red_win_res['radar_scores']['Pick_Potential']} | Obj: {red_win_res['radar_scores']['Objective_Control']}")
    r_card = red_win_res['win_condition_card']
    print(f"⭐ Chủ lực (Core Carry): {r_card['core_carry']}")
    print(f"⏱️ Điểm rơi sức mạnh: {r_card['power_spike_timing']}")
    print(f"🐉 Mục tiêu số 1: {r_card['primary_objective']}")
    print(f"✅ Điều kiện thắng: {r_card['win_condition']}")
    print(f"❌ Cần tránh: {r_card['critical_lose_condition']}")

    # Model probabilities must come from the validated model, never radar arithmetic.
    if not show_prediction:
        print('Phiên có mốc lịch sử: bỏ dự báo từ model lưu sẵn vì chưa bảo đảm model được fit trước mốc này.')
        return
    from draft_model import LolDraftPredictionSystem
    try:
        prediction=LolDraftPredictionSystem.load_model().predict_draft(blue_picks,red_picks,region=reg_code)
        print("\nXÁC SUẤT ƯỚC LƯỢNG TỪ MÔ HÌNH (không phải mức tăng thắng do draft):")
        print(f"Blue: {prediction['blue_win_probability_pct']}% | Red: {prediction['red_win_probability_pct']}%")
        print(f"Model: {prediction['model_used']}")
    except (FileNotFoundError,ValueError) as exc:
        print(f"Chưa có dự báo hợp lệ: {exc}")

    print("=" * 95 + "\n")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blue-team',default='')
    parser.add_argument('--red-team',default='')
    parser.add_argument('--user-side',choices=['blue','red'],default='blue')
    parser.add_argument('--first-pick',choices=['blue','red'],default='blue')
    parser.add_argument('--region',default='ALL')
    parser.add_argument('--wishlist',default='')
    parser.add_argument('--as-of',help='Mốc dữ liệu YYYY-MM-DD hoặc timestamp; không sử dụng trận sau mốc này')
    parser.add_argument('--patch',help='Mã patch theo dataset, ví dụ 16.16; không tự suy ra patch không có dữ liệu')
    parser.add_argument('--lookback-days',type=int,default=60)
    parser.add_argument('--half-life-days',type=float,default=21)
    parser.add_argument('--max-data-age-days',type=int,help='Từ chối chạy nếu snapshot quá cũ so với mốc yêu cầu')
    parser.add_argument('--used-champions',default='',help='Các tướng đã dùng ván trước, không còn được cấm/chọn trong phiên này')
    parser.add_argument('--opponent-model',type=Path,nargs='?',const=PROJECT_ROOT/'models/opponent_model.pkl',
                        help='Dự đoán hành động tiếp theo bằng model đã lưu; không thay điểm chiến thuật')
    parser.add_argument('--allow-statistical-auto',action='store_true',
                        help='Cho phép demo tự chọn chỉ theo điểm thống kê dù thiếu căn cứ đối đầu toàn đội; không xác nhận counter')
    parser.add_argument('--ban-strategy',choices=['legacy','contextual'],default='legacy')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--auto',action='store_true')
    mode.add_argument('--interactive',action='store_true')
    parser.add_argument('--save-session',type=Path)
    args=parser.parse_args()
    blue,red,side,region=args.blue_team,args.red_team,args.user_side,args.region
    try:
        if not blue and not red and not args.auto:
            print('1. Bạn vs T1 (Blue) | 2. Bạn vs T1 (Red) | 3. T1 vs GEN.G | 4. BLG vs TES | 5. Tùy chỉnh')
            choice=input('Chọn kịch bản [1]: ').strip() or '1'
            if choice=='2':blue,red,side='T1','UNDERDOG','red'
            elif choice=='3':blue,red='T1','GEN.G'
            elif choice=='4':blue,red='BLG','TES'
            elif choice=='5':
                blue=input('Đội Blue [UNDERDOG]: ').strip() or 'UNDERDOG'
                red=input('Đội Red [T1]: ').strip() or 'T1'
                side=input('Bạn điều khiển blue/red [blue]: ').strip() or 'blue'
            else:blue,red='UNDERDOG','T1'
            region=input(f'Khu vực ALL/LCK/LPL/LCP/MSI/WLDS [{region}]: ').strip() or region
        result=run_pro_tournament_draft_simulation(blue or 'T1',red or 'GEN.G',user_side=side,
                                            first_side=args.first_pick,region=region,
                                            wishlist=[c.strip() for c in args.wishlist.split(',') if c.strip()],
                                            interactive=not args.auto,save_session=args.save_session,
                                            meta_policy=MetaPolicy(args.as_of,args.patch,args.lookback_days,args.half_life_days),
                                            max_data_age_days=args.max_data_age_days,
                                            used_champions=[c.strip() for c in args.used_champions.split(',') if c.strip()],
                                            opponent_model_path=args.opponent_model,
                                            allow_statistical_auto=args.allow_statistical_auto,ban_strategy=args.ban_strategy)
        if result.get('manual_review'):parser.exit(3,'Phiên chờ xem lại chiến thuật; chưa tự chốt lựa chọn thiếu căn cứ.\n')
    except (EOFError,KeyboardInterrupt):print('\nĐã dừng phiên.')
    except ValueError as exc:parser.exit(2,f'{exc}\n')


if __name__=='__main__':main()
