"""
Simulate Full Ban/Pick Match (Mô Phỏng Toàn Diện Cấm/Chọn Đấu Giải: Tương Tác Trực Tiếp Bằng Bàn Phím)
Module 07: Recommender Engine Showcase

Tính năng:
1. Chế độ Tương Tác Trực Tiếp (Interactive Mode):
   - Bạn đóng vai trò là Huấn Luyện Viên / Tuyển Thủ T1 (Phe Xanh).
   - Ở mỗi lượt Cấm / Chọn của T1, hệ thống hiển thị bảng gợi ý [1], [2], [3]... kèm % ưu tiên và lý do dữ liệu.
   - Bạn chỉ cần gõ số (1, 2, 3...) và bấm ENTER để chốt.
   - Gen.G (AI) sẽ tự động tính toán phản ứng tối ưu nhất theo chuẩn Giải Đấu 2026.
2. Tuân thủ chuẩn Riot Esports 4 Giai Đoạn:
   - Giai đoạn 1: Cấm 1 (6 lượt xen kẽ: T1 -> Gen.G -> T1 -> Gen.G -> T1 -> Gen.G)
   - Giai đoạn 2: Chọn 1 (6 lượt: T1(1) -> Gen.G(2) -> T1(2) -> Gen.G(1))
   - Giai đoạn 3: Cấm 2 (4 lượt: Gen.G(1) -> T1(2) -> Gen.G(1))
   - Giai đoạn 4: Chọn 2 (4 lượt: Gen.G(1) -> T1(2) -> Gen.G(1 - Last Pick))
3. Phân tích Thẻ Chiến Thuật + Radar 5 Trục + Dự đoán Tỷ lệ Thắng Phút 0.

Học phần: Nhập môn Khoa học Dữ liệu - PTIT (TS. Thái Tuyết Hải)
"""

import sys
import os
import time
import argparse
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np

# Path setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "06_machine_learning"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "07_recommender"))

import cluster_archetypes
from recommender_engine import RecommenderEngine, safe_load_pickle

DRAFT_MODEL_PATH = PROJECT_ROOT / "models" / "draft_model.pkl"

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

LANE_TO_ROSTER_KEY = {'top': 'top', 'jungle': 'jng', 'mid': 'mid', 'bot': 'bot', 'support': 'sup'}
LANE_TITLE = {'top': 'Đường Trên', 'jungle': 'Đi Rừng', 'mid': 'Đường Giữa', 'bot': 'Xạ Thủ', 'support': 'Hỗ Trợ'}


def prompt_user_selection(cands: List[Dict[str, Any]], prompt_title: str, all_banned: set, all_picked: set, engine: RecommenderEngine, is_ban_mode: bool = True, enemy_roster: dict = None, my_picks: dict = None, enemy_picks: dict = None, available_lanes: list = None, team_roster: dict = None, ban_phase: int = 1, user_team_name: str = "BẠN") -> Dict[str, Any]:
    """Hiển thị menu gợi ý và nhận phím bấm (1, 2, 3... hoặc tên tướng bất kỳ) từ người dùng"""
    print(f"\n💡 BẢNG GỢI Ý CHIẾN THUẬT CHO BẠN ({prompt_title}):")
    print("─" * 92)
    for idx, item in enumerate(cands, 1):
        c_name = item['champion']
        pct = item.get('priority_pct', item.get('score', 90.0))
        if isinstance(pct, float) and pct <= 1.0:
            pct = round(pct * 100, 1)
        pct = min(99.0, max(50.0, round(float(pct), 1)))
        reason = item.get('reason', '')
        if not reason and 'reasons' in item and item['reasons']:
            reason = item['reasons'][0]
        badge = item.get('badge', '⭐ TỐI ƯU')
        lane_str = f" [{item['lane_title']}]" if 'lane_title' in item else ""
        print(f"  [{idx}] 🎯 {c_name.upper()}{lane_str} ({pct}%) [{badge}]")
        print(f"      └─ 📊 Lý do: {reason}")
    print("─" * 92)

    while True:
        try:
            guide_str = " (hoặc gõ 'top', 'jng', 'mid', 'bot', 'sp' để xem riêng từng đường)"
            user_in = input(f"👉 [{user_team_name.upper()}] Nhập số (1-{len(cands)}) hoặc gõ tên tướng bất kỳ{guide_str}: ").strip()
            if not user_in:
                chosen = cands[0]
                print(f"   -> Mặc định chọn [{1}] {chosen['champion'].upper()}")
                return chosen

            role_alias = {'sp': 'support', 'sup': 'support', 'support': 'support', 'top': 'top', 'mid': 'mid', 'bot': 'bot', 'ad': 'bot', 'adc': 'bot', 'jng': 'jungle', 'jungle': 'jungle', 'rừng': 'jungle'}

            if user_in.lower() in role_alias:
                filt_lane = role_alias[user_in.lower()]
                if is_ban_mode:
                    # Gợi ý cấm theo đường: Kết hợp cả Meta Cấm Phase hiện tại + Tướng tủ tuyển thủ đối phương
                    filt_p = (enemy_roster or {}).get(LANE_TO_ROSTER_KEY.get(filt_lane, filt_lane), None)
                    sub_cands = []
                    seen_c = set()

                    # 1. Trích xuất từ Bảng cấm tổng hợp (chuẩn xác Phase 1 hoặc Phase 2)
                    all_bans = engine.target_ban_engine.recommend_team_bans(enemy_roster or {}, top_k=40, ban_phase=ban_phase, already_banned=all_banned)
                    db_l = {'jungle': 'jng', 'support': 'sup'}.get(filt_lane, filt_lane)
                    for b in all_bans:
                        c_n = b['champion']
                        if c_n in all_banned or c_n in all_picked or c_n in seen_c:
                            continue
                        c_meta = engine.pick_recommender.metadata.get(c_n, {})
                        c_picks = engine.pick_recommender.tournament_meta_picks.get((db_l, c_n), {}).get('picks', 0)
                        p_role_match = (b.get('player_role') == LANE_TO_ROSTER_KEY.get(filt_lane))
                        if c_meta.get('lane') == filt_lane or c_picks >= 10 or p_role_match:
                            seen_c.add(c_n)
                            sub_cands.append({
                                'champion': c_n,
                                'priority_pct': b['priority_pct'],
                                'lane': filt_lane,
                                'lane_title': LANE_TITLE[filt_lane],
                                'badge': f"🚫 CẤM {LANE_TITLE[filt_lane].upper()}",
                                'reason': b['reason']
                            })

                    # 2. Bổ sung các tướng tủ riêng của tuyển thủ đối phương nếu chưa có
                    if filt_p:
                        raw_target_bans = engine.target_ban_engine.recommend_target_bans(filt_p, top_k=8, ban_phase=ban_phase)
                        for rb in raw_target_bans:
                            c_n = rb['champion']
                            if c_n not in all_banned and c_n not in all_picked and c_n not in seen_c:
                                seen_c.add(c_n)
                                sub_cands.append({
                                    'champion': c_n,
                                    'priority_pct': round(rb['threat_score'] * 100, 1),
                                    'lane': filt_lane,
                                    'lane_title': LANE_TITLE[filt_lane],
                                    'badge': rb.get('badge', f"🚫 CẤM {LANE_TITLE[filt_lane].upper()}"),
                                    'reason': f"Chặn bài tủ còn lại của {filt_p} ({rb.get('tournament_stats', rb.get('reason', ''))})"
                                })

                    if sub_cands:
                        cands = sorted(sub_cands, key=lambda x: x['priority_pct'], reverse=True)[:5]
                        print(f"\n🔍 BẢNG GỢI Ý CẤM RIÊNG CHO VỊ TRÍ {LANE_TITLE[filt_lane].upper()}{f' (Target vào {filt_p})' if filt_p else ''}:")
                        print("─" * 92)
                        for s_idx, sc in enumerate(cands, 1):
                            print(f"  [{s_idx}] 🎯 {sc['champion'].upper()} ({sc['priority_pct']}%) [{sc['badge']}]")
                            print(f"      └─ 📊 Lý do: {sc['reason']}")
                        print("─" * 92)
                    else:
                        print(f"ℹ️ Không có tướng cấm đáng chú ý nào ở vị trí {LANE_TITLE[filt_lane]}!")
                    continue
                else:
                    # Gợi ý pick theo đường của phe mình
                    filt_p = (team_roster or {}).get(LANE_TO_ROSTER_KEY.get(filt_lane, filt_lane), None)
                    lane_picks = engine.pick_recommender.recommend_picks(
                        filt_lane,
                        list((my_picks or {}).values()),
                        list((enemy_picks or {}).values()),
                        already_banned=all_banned,
                        player_name=filt_p,
                        top_k=6
                    )
                    sub_cands = []
                    for lp in lane_picks:
                        c_n = lp['champion']
                        if c_n not in all_banned and c_n not in all_picked:
                            p_score = min(99.0, max(50.0, round(lp['score'] * 100, 1)))
                            r_txt = lp['reasons'][0] if lp.get('reasons') else f'Chuẩn Meta {LANE_TITLE[filt_lane]}'
                            sub_cands.append({
                                'champion': c_n,
                                'priority_pct': p_score,
                                'lane': filt_lane,
                                'lane_title': LANE_TITLE[filt_lane],
                                'badge': f'⭐ TOP {LANE_TITLE[filt_lane].upper()}',
                                'reason': r_txt
                            })
                    if sub_cands:
                        cands = sub_cands[:5]
                        print(f"\n🔍 BẢNG GỢI Ý RIÊNG CHO VỊ TRÍ {LANE_TITLE[filt_lane].upper()}{f' ({filt_p})' if filt_p else ''}:")
                        print("─" * 92)
                        for s_idx, sc in enumerate(cands, 1):
                            print(f"  [{s_idx}] 🎯 {sc['champion'].upper()} ({sc['priority_pct']}%) [{sc['badge']}]")
                            print(f"      └─ 📊 Lý do: {sc['reason']}")
                        print("─" * 92)
                    continue

            if not is_ban_mode and (user_in.lower().startswith('swap') or user_in.lower().startswith('doi')):
                # Cú pháp: swap <tướng> <đường> (Ví dụ: swap camille top)
                swap_tokens = user_in.split()
                if len(swap_tokens) >= 3:
                    sw_champ_raw = swap_tokens[1]
                    sw_lane_raw = swap_tokens[2].lower()
                    sw_norm = engine.pick_recommender._normalize_champion_name(sw_champ_raw)
                    inv_roster = {'top': 'top', 'jng': 'jungle', 'mid': 'mid', 'bot': 'bot', 'sup': 'support'}
                    found_curr_role = None
                    for r_k, c_n in (my_picks or {}).items():
                        if c_n.lower() == sw_norm.lower():
                            found_curr_role = r_k
                            break
                    if not found_curr_role:
                        print(f"⚠️ Không tìm thấy tướng '{sw_norm}' trong danh sách đã pick của đội!")
                        continue
                    
                    role_alias = {'sp': 'support', 'sup': 'support', 'support': 'support', 'top': 'top', 'mid': 'mid', 'bot': 'bot', 'ad': 'bot', 'adc': 'bot', 'jng': 'jungle', 'jungle': 'jungle'}
                    target_l = role_alias.get(sw_lane_raw, sw_lane_raw)
                    if target_l not in LANE_TITLE:
                        print(f"⚠️ Vị trí '{sw_lane_raw}' không hợp lệ (hỗ trợ: top, jng, mid, bot, sup)!")
                        continue
                    
                    target_rk = LANE_TO_ROSTER_KEY[target_l]
                    curr_lane = inv_roster[found_curr_role]
                    if target_rk == found_curr_role:
                        print(f"ℹ️ Tướng '{sw_norm}' hiện đã ở vị trí {LANE_TITLE[target_l]} rồi!")
                        continue
                    
                    if available_lanes and target_l in available_lanes:
                        available_lanes.remove(target_l)
                        available_lanes.append(curr_lane)
                        del my_picks[found_curr_role]
                        my_picks[target_rk] = sw_norm
                        print(f"\n🔄 [ĐỔI VỊ TRÍ THÀNH CÔNG] Đã chuyển {sw_norm.upper()} từ {LANE_TITLE[curr_lane]} sang {LANE_TITLE[target_l]}!")
                        print(f"   Đội hình hiện tại: {', '.join([f'{LANE_TITLE[inv_roster[k]]}: {v.upper()}' for k, v in my_picks.items()])}\n")
                        continue
                    elif my_picks and target_rk in my_picks:
                        other_champ = my_picks[target_rk]
                        my_picks[target_rk] = sw_norm
                        my_picks[found_curr_role] = other_champ
                        print(f"\n🔄 [HOÁN ĐỔI 2 VỊ TRÍ THÀNH CÔNG] Đã đổi {sw_norm.upper()} sang {LANE_TITLE[target_l]} và {other_champ.upper()} sang {LANE_TITLE[curr_lane]}!")
                        print(f"   Đội hình hiện tại: {', '.join([f'{LANE_TITLE[inv_roster[k]]}: {v.upper()}' for k, v in my_picks.items()])}\n")
                        continue
                else:
                    print("💡 Cú pháp đổi đường: swap <tên_tướng> <đường_mới> (Ví dụ: swap camille top)")
                    continue

            if user_in.isdigit():
                idx_val = int(user_in)
                if 1 <= idx_val <= len(cands):
                    chosen = cands[idx_val - 1]
                    print(f"   -> Bạn đã chọn [{idx_val}] {chosen['champion'].upper()}")
                    return chosen
                else:
                    print(f"⚠️ Vui lòng nhập số hợp lệ từ 1 đến {len(cands)}!")
            else:
                # Phân tích cú pháp: Hỗ trợ gõ 'Camille sp', 'Camille top', 'Poppy sup', v.v.
                tokens = user_in.strip().split()
                role_alias = {'sp': 'support', 'sup': 'support', 'support': 'support', 'top': 'top', 'mid': 'mid', 'bot': 'bot', 'ad': 'bot', 'adc': 'bot', 'jng': 'jungle', 'jungle': 'jungle'}
                explicit_lane = None
                
                # Kiểm tra token cuối có phải vị trí không
                if len(tokens) >= 2 and tokens[-1].lower() in role_alias:
                    explicit_lane = role_alias[tokens[-1].lower()]
                    champ_raw = " ".join(tokens[:-1])
                elif len(tokens) >= 2 and tokens[0].lower() in role_alias:
                    explicit_lane = role_alias[tokens[0].lower()]
                    champ_raw = " ".join(tokens[1:])
                else:
                    champ_raw = user_in

                norm_name = engine.pick_recommender._normalize_champion_name(champ_raw)
                if norm_name in all_banned or norm_name in all_picked:
                    print(f"⚠️ Tướng '{norm_name}' đã bị cấm hoặc đã được chọn trước đó! Hãy chọn tướng khác.")
                elif norm_name in engine.pick_recommender.metadata:
                    print(f"   -> Bạn đã nhập trực tiếp tướng: ⭐ {norm_name.upper()}")
                    
                    if is_ban_mode:
                        # Phân tích dữ liệu tự động cho tướng cấm tự chọn
                        b_cnt = engine.target_ban_engine.tournament_ban_counts.get(norm_name, 0)
                        b_rate = round((b_cnt / float(engine.target_ban_engine.max_ban_count)) * 30.1, 1) if engine.target_ban_engine.max_ban_count > 0 else 10.0
                        
                        target_player = None
                        target_role = None
                        if enemy_roster:
                            for r_k, p_n in enemy_roster.items():
                                p_stats = engine.target_ban_engine.player_stats_cache.get(p_n, {}).get(norm_name)
                                if p_stats:
                                    target_player = p_n
                                    target_role = r_k
                                    break
                        
                        if target_player:
                            dyn_reason = f"Target trực tiếp {target_player} ({target_role.upper()}) & Có {b_cnt} lượt cấm giải ({b_rate}%)"
                            dyn_pct = min(98.0, 75.0 + (b_cnt / 50.0))
                        elif b_cnt > 0:
                            dyn_reason = f"Lựa chọn cấm theo chiến thuật HLV ({b_cnt} lượt cấm giải - {b_rate}%)"
                            dyn_pct = min(95.0, 70.0 + (b_cnt / 60.0))
                        else:
                            dyn_reason = "Lựa chọn cấm chiến thuật trực tiếp của Huấn Luyện Viên"
                            dyn_pct = 85.0

                        return {
                            'champion': norm_name,
                            'priority_pct': round(dyn_pct, 1),
                            'reason': dyn_reason,
                            'badge': '🎯 CẤM TỰ CHỌN'
                        }
                    else:
                        # Phân tích vị trí tối ưu từ Dữ liệu Đấu Giải thực tế (Flex Pick Detection)
                        candidate_lanes = engine.pick_recommender.get_candidate_lanes_for_champion(norm_name, available_lanes)
                        
                        target_lane = None
                        if explicit_lane and explicit_lane in available_lanes:
                            target_lane = explicit_lane
                        elif candidate_lanes:
                            # Nếu tướng có thể chơi nhiều vị trí còn trống và có số trận giải đáng kể ở cả 2 vị trí (>15 trận)
                            viable_lanes = [cl for cl in candidate_lanes if cl[0] in available_lanes and cl[1] >= 15]
                            if len(viable_lanes) > 1:
                                print(f"\n🔄 Tướng Flex đa vị trí: '{norm_name.upper()}' có thể chơi tốt ở nhiều lane.")
                                print(f"   (💡 Bạn hoàn toàn có thể đổi vị trí tướng này sau bất cứ lúc nào qua lệnh 'swap {norm_name} <đường>' hoặc pick thêm tướng cùng vị trí!)")
                                for f_idx, (f_l, f_picks) in enumerate(viable_lanes, 1):
                                    print(f"   [{f_idx}] {LANE_TITLE.get(f_l, f_l)} ({f_picks} trận giải)")
                                try:
                                    f_choice = input(f"👉 Chọn vị trí cho {norm_name} (1-{len(viable_lanes)}) [Mặc định 1 - {LANE_TITLE[viable_lanes[0][0]]}]: ").strip()
                                    if f_choice.isdigit() and 1 <= int(f_choice) <= len(viable_lanes):
                                        target_lane = viable_lanes[int(f_choice) - 1][0]
                                    else:
                                        target_lane = viable_lanes[0][0]
                                except Exception:
                                    target_lane = viable_lanes[0][0]
                            else:
                                # Tự động chọn lane có số lượt pick giải đấu cao nhất
                                target_lane = candidate_lanes[0][0]
                        else:
                            target_lane = available_lanes[0] if available_lanes else 'mid'
                        
                        # Kiểm tra synergy với đồng đội đã chọn
                        syn_text = ""
                        for ally_c in (my_picks.values() if my_picks else []):
                            pair = (norm_name, ally_c)
                            rev_pair = (ally_c, norm_name)
                            if pair in engine.pick_recommender.duo_synergies:
                                syn_text = f"🔥 Cặp bài trùng huỷ diệt với {ally_c} (Synergy {int(engine.pick_recommender.duo_synergies[pair]*100)}%)"
                                break
                            elif rev_pair in engine.pick_recommender.duo_synergies:
                                syn_text = f"🔥 Cặp bài trùng huỷ diệt với {ally_c} (Synergy {int(engine.pick_recommender.duo_synergies[rev_pair]*100)}%)"
                                break
                        
                        picks_at_pos = engine.pick_recommender.tournament_meta_picks.get(({'support': 'sup', 'jungle': 'jng'}.get(target_lane, target_lane), norm_name), {}).get('tour_picks', 0)
                        pos_desc = f" ({picks_at_pos} trận giải ở {LANE_TITLE.get(target_lane, target_lane)})" if picks_at_pos > 0 else ""
                        dyn_reason = syn_text if syn_text else f"Lựa chọn chiến thuật trọng tâm cho {LANE_TITLE.get(target_lane, target_lane)}{pos_desc}"
                        
                        return {
                            'champion': norm_name,
                            'priority_pct': 95.0,
                            'lane': target_lane,
                            'lane_title': LANE_TITLE.get(target_lane, target_lane),
                            'reason': dyn_reason,
                            'badge': '⭐ CHỌN TỰ DO'
                        }
                else:
                    print(f"⚠️ Không nhận diện được tướng '{user_in}', vui lòng thử lại!")
        except (EOFError, KeyboardInterrupt):
            return cands[0]


# =========================================================================
# MÔ PHỎNG CẤM/CHỌN ĐẤU GIẢI CHUYÊN NGHIỆP (TƯƠNG TÁC HOẶC TỰ ĐỘNG)
# =========================================================================
def run_pro_tournament_draft_simulation(blue_team_name: str = "T1",
                                        red_team_name: str = "Gen.G",
                                        blue_roster: dict = None,
                                        red_roster: dict = None,
                                        user_side: str = "blue",
                                        first_side: str = "blue",
                                        wishlist: Optional[List[str]] = None,
                                        interactive: bool = True):
    engine = RecommenderEngine()

    b_key = blue_team_name.upper()
    r_key = red_team_name.upper()

    if blue_roster is None:
        blue_roster = TEAM_PRESETS.get(b_key, {
            'top': f'{blue_team_name}_Top',
            'jng': f'{blue_team_name}_Rừng',
            'mid': f'{blue_team_name}_Mid',
            'bot': f'{blue_team_name}_AD',
            'sup': f'{blue_team_name}_SP'
        })
    if red_roster is None:
        red_roster = TEAM_PRESETS.get(r_key, {
            'top': f'{red_team_name}_Top',
            'jng': f'{red_team_name}_Rừng',
            'mid': f'{red_team_name}_Mid',
            'bot': f'{red_team_name}_AD',
            'sup': f'{red_team_name}_SP'
        })

    active_wishlist = []
    if wishlist:
        for w in wishlist:
            norm_name = engine.pick_recommender._normalize_champion_name(w)
            if norm_name:
                active_wishlist.append(norm_name)

    t1_side, t1_name, t1_roster, t1_color = "BLUE", blue_team_name, blue_roster, "🔷"
    t2_side, t2_name, t2_roster, t2_color = "RED", red_team_name, red_roster, "🔴"
    
    is_user_t1 = (user_side.lower() == "blue")
    is_user_t2 = (user_side.lower() == "red")
    user_team_name = blue_team_name if is_user_t1 else red_team_name
    user_color = "🔷" if is_user_t1 else "🔴"
    user_side_label = "PHE XANH (FIRST PICK)" if is_user_t1 else "PHE ĐỎ (LAST PICK COUNTER)"

    print("\n" + "=" * 95)
    print(f"🏆 [ĐẤU GIẢI CHUYÊN NGHIỆP 2026] CẤM/CHỌN RIOT TOURNAMENT: {blue_team_name.upper()} vs {red_team_name.upper()}")
    print(f"🎮 BẠN ĐANG ĐIỀU KHIỂN: {user_color} {user_team_name.upper()} ({user_side_label})")
    if active_wishlist:
        print(f"🎯 ĐỘI HÌNH / TƯỚNG DỰ KIẾN: {', '.join(active_wishlist).upper()} (Tự động kích hoạt Cấm Dọn Đường)")
    print("=" * 95)
    print(f"🔷 PHE XANH ({blue_team_name}): Top: {blue_roster['top']} | Jng: {blue_roster['jng']} | Mid: {blue_roster['mid']} | Bot: {blue_roster['bot']} | Sup: {blue_roster['sup']}")
    print(f"🔴 PHE ĐỎ   ({red_team_name}): Top: {red_roster['top']} | Jng: {red_roster['jng']} | Mid: {red_roster['mid']} | Bot: {red_roster['bot']} | Sup: {red_roster['sup']}")
    print("-" * 95)

    all_banned = set()
    t1_bans, t2_bans = [], []
    t1_picks, t2_picks = {}, {}
    t1_available_lanes = ['top', 'jungle', 'mid', 'bot', 'support']
    t2_available_lanes = ['top', 'jungle', 'mid', 'bot', 'support']

    def get_all_picked():
        return set(t1_picks.values()).union(set(t2_picks.values()))

    # =========================================================================
    # GIAI ĐOẠN 1: CẤM 1 (T1_Ban1 -> T2_Ban1 -> T1_Ban2 -> T2_Ban2 -> T1_Ban3 -> T2_Ban3)
    # =========================================================================
    print("\n" + "─" * 34 + " GIAI ĐOẠN 1: CẤM 1 (PHASE 1 BANS - 6 LƯỢT XEN KẼ) " + "─" * 34)
    print(f"🎯 Thứ tự cấm 1: {t1_name} (1) -> {t2_name} (1) -> {t1_name} (2) -> {t2_name} (2) -> {t1_name} (3) -> {t2_name} (3)\n")

    for ban_turn in range(1, 4):
        # 1. LƯỢT CẤM CỦA T1 (BLUE SIDE)
        cands_t1 = []
        if active_wishlist:
            for w_champ in active_wishlist:
                enabling = engine.target_ban_engine.recommend_enabling_bans(w_champ, enemy_roster=t2_roster, top_k=4, already_banned=all_banned)
                if enabling:
                    cands_t1.extend(enabling)

        team_bans_1 = engine.target_ban_engine.recommend_team_bans(t2_roster, top_k=6, ban_phase=1, already_banned=all_banned)
        cands_t1.extend(team_bans_1)
        valid_t1 = [c for c in cands_t1 if c['champion'] not in all_banned and c['champion'] not in active_wishlist]
        
        seen_1 = set()
        dedup_valid_t1 = []
        for c in valid_t1:
            if c['champion'] not in seen_1:
                seen_1.add(c['champion'])
                dedup_valid_t1.append(c)
        valid_t1 = sorted(dedup_valid_t1, key=lambda x: x.get('priority_pct', 80.0), reverse=True)[:5]

        if interactive and is_user_t1:
            print(f"\n👉 LƯỢT CỦA BẠN: {t1_color} [{t1_name.upper()}_BAN {ban_turn}]")
            chosen_ban_1 = prompt_user_selection(valid_t1, f"Lượt Cấm {ban_turn} của {t1_name}", all_banned, get_all_picked(), engine, is_ban_mode=True, enemy_roster=t2_roster, ban_phase=1, user_team_name=t1_name)
            p_score_1 = chosen_ban_1.get('priority_pct', 90.0)
            print(f"🔒 {t1_color} [{t1_name.upper()} ĐÃ CẤM {ban_turn}]: 🚫 {chosen_ban_1['champion'].upper()} ({p_score_1}%) [{chosen_ban_1.get('reason','')}]")
        else:
            chosen_ban_1 = valid_t1[0] if valid_t1 else {'champion': 'Orianna', 'priority_pct': 98.0, 'reason': 'Tướng Meta bị cấm số 1 giải đấu'}
            p_score_1 = chosen_ban_1.get('priority_pct', 90.0)
            print(f"🤖 {t1_color} [{t1_name.upper()} ĐÃ CẤM {ban_turn}]: 🚫 {chosen_ban_1['champion'].upper()} ({p_score_1}%) [{chosen_ban_1.get('reason','')}]")

        ban_champ_1 = chosen_ban_1['champion']
        all_banned.add(ban_champ_1)
        t1_bans.append(ban_champ_1)

        # 2. LƯỢT CẤM CỦA T2 (RED SIDE)
        cands_t2 = []
        if is_user_t2 and active_wishlist:
            for w_champ in active_wishlist:
                enabling_t2 = engine.target_ban_engine.recommend_enabling_bans(w_champ, enemy_roster=t1_roster, top_k=4, already_banned=all_banned)
                if enabling_t2:
                    cands_t2.extend(enabling_t2)

        team_bans_2 = engine.target_ban_engine.recommend_team_bans(t1_roster, top_k=6, ban_phase=1, already_banned=all_banned)
        cands_t2.extend(team_bans_2)
        valid_t2 = [c for c in cands_t2 if c['champion'] not in all_banned and c['champion'] not in active_wishlist]
        
        seen_2 = set()
        dedup_valid_t2 = []
        for c in valid_t2:
            if c['champion'] not in seen_2:
                seen_2.add(c['champion'])
                dedup_valid_t2.append(c)
        valid_t2 = sorted(dedup_valid_t2, key=lambda x: x.get('priority_pct', 80.0), reverse=True)[:5]

        if interactive and is_user_t2:
            print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()}_BAN {ban_turn}]")
            chosen_ban_2 = prompt_user_selection(valid_t2, f"Lượt Cấm {ban_turn} của {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=True, enemy_roster=t1_roster, ban_phase=1, user_team_name=t2_name)
            p_score_2 = chosen_ban_2.get('priority_pct', 90.0)
            print(f"🔒 {t2_color} [{t2_name.upper()} ĐÃ CẤM {ban_turn}]: 🚫 {chosen_ban_2['champion'].upper()} ({p_score_2}%) [{chosen_ban_2.get('reason','')}]")
        else:
            chosen_ban_2 = valid_t2[0] if valid_t2 else {'champion': 'Orianna', 'priority_pct': 98.0, 'reason': 'Tướng Meta bị cấm số 1 giải đấu'}
            p_score_2 = chosen_ban_2.get('priority_pct', 90.0)
            print(f"🤖 {t2_color} [{t2_name.upper()} ĐÃ CẤM {ban_turn}]: 🚫 {chosen_ban_2['champion'].upper()} ({p_score_2}%) [{chosen_ban_2.get('reason','')}]")

        ban_champ_2 = chosen_ban_2['champion']
        all_banned.add(ban_champ_2)
        t2_bans.append(ban_champ_2)

    # =========================================================================
    # GIAI ĐOẠN 2: CHỌN 1 (T1(1) -> T2(2) -> T1(2) -> T2(1))
    # =========================================================================
    print("\n" + "─" * 38 + " GIAI ĐOẠN 2: CHỌN 1 (PHASE 1 PICKS) " + "─" * 38)

    def assign_champion_to_lane(team_name: str, team_picks: dict, available_lanes: list, champ: str, desired_lane: str, team_roster: dict, engine: RecommenderEngine):
        roster_k = LANE_TO_ROSTER_KEY.get(desired_lane, desired_lane)
        
        # 1. Trường hợp bình thường: Vị trí đó đang còn trống
        if desired_lane in available_lanes:
            available_lanes.remove(desired_lane)
            team_picks[roster_k] = champ
            return desired_lane

        # 2. Trường hợp Vị trí đó đã có người (ví dụ: Camille đang ở Hỗ Trợ, nhưng bạn pick thêm Nautilus Hỗ Trợ)
        current_occupant = team_picks.get(roster_k, None)
        if current_occupant and available_lanes:
            alt_lanes = engine.pick_recommender.get_candidate_lanes_for_champion(current_occupant, available_lanes)
            if alt_lanes:
                best_alt_lane = alt_lanes[0][0]
                alt_picks = alt_lanes[0][1]
                alt_roster_k = LANE_TO_ROSTER_KEY[best_alt_lane]
                
                # Thực hiện Flex Swap!
                available_lanes.remove(best_alt_lane)
                team_picks[alt_roster_k] = current_occupant
                team_picks[roster_k] = champ
                
                print(f"\n🔄 [CHIẾN THUẬT ĐẢO ĐƯỜNG - FLEX SWAP THÀNH CÔNG!]")
                print(f"   └─ Đẩy {current_occupant.upper()} từ {LANE_TITLE[desired_lane]} sang {LANE_TITLE[best_alt_lane]} cho {team_roster[alt_roster_k]} ({alt_picks} trận giải)")
                print(f"   └─ Nhường vị trí {LANE_TITLE[desired_lane]} cho tân binh {champ.upper()} ({team_roster[roster_k]})!\n")
                return desired_lane

        # 3. Fallback: Nếu không swap được, lấy vị trí còn trống đầu tiên
        fallback_lane = available_lanes.pop(0) if available_lanes else 'mid'
        fb_k = LANE_TO_ROSTER_KEY.get(fallback_lane, fallback_lane)
        team_picks[fb_k] = champ
        return fallback_lane

    def generate_pick_candidates(team_name, roster, picks_dict, available_lanes, enemy_picks_dict, is_t1_pick=False):
        cands = []
        # Ưu tiên Wishlist nếu có (áp dụng cho đội do người dùng điều khiển)
        is_user_team = (team_name == user_team_name)
        if is_user_team and active_wishlist:
            for w_champ in active_wishlist:
                if w_champ not in all_banned and w_champ not in get_all_picked():
                    w_lane = engine.pick_recommender.metadata.get(w_champ, {}).get('lane', 'bot')
                    if w_lane in available_lanes:
                        cands.append({
                            'champion': w_champ,
                            'score': 0.99,
                            'priority_pct': 99.0,
                            'lane': w_lane,
                            'lane_title': LANE_TITLE[w_lane],
                            'badge': '🔥 WISHLIST CHỦ LỰC',
                            'reason': 'Quân bài trọng tâm theo Đội hình Chiến thuật định sẵn (Wishlist)'
                        })

        # 1. Gợi ý cho các lane đang còn trống
        for lane in available_lanes:
            lane_player = roster.get(LANE_TO_ROSTER_KEY.get(lane, lane), None)
            lane_cands = engine.pick_recommender.recommend_picks(
                lane, 
                list(picks_dict.values()), 
                list(enemy_picks_dict.values()), 
                already_banned=all_banned,
                player_name=lane_player,
                top_k=6
            )
            for lc in lane_cands:
                if lc['champion'] not in all_banned and lc['champion'] not in get_all_picked():
                    db_l = {'jungle': 'jng', 'support': 'sup'}.get(lane, lane)
                    pos_picks = engine.pick_recommender.tournament_meta_picks.get((db_l, lc['champion']), {}).get('picks', 0)
                    reason_text = lc['reasons'][0] if lc.get('reasons') else 'Chuẩn Meta Đấu Giải 2026'
                    r_lower = reason_text.lower()

                    if 'cặp bài trùng' in r_lower:
                        badge_text = '🔥 COMBO SYNERGY'
                    elif 'khắc chế' in r_lower or 'kèo trên' in r_lower:
                        badge_text = '⚔️ COUNTER-PICK (META)' if pos_picks >= 40 else '⚔️ COUNTER TÌNH HUỐNG'
                    elif 'tướng tủ' in r_lower:
                        badge_text = '🔥 TƯỚNG TỦ TUYỂN THỦ'
                    elif pos_picks >= 150:
                        badge_text = '⭐ META TIER S+'
                    elif pos_picks >= 40:
                        badge_text = '⭐ META TIER S'
                    elif pos_picks >= 15:
                        badge_text = '✨ LỰA CHỌN CHIẾN THUẬT'
                    else:
                        badge_text = '📊 POCKET PICK / TÌNH HUỐNG'

                    cands.append({
                        'champion': lc['champion'],
                        'score': lc['score'],
                        'priority_pct': round(lc['score'] * 100, 1),
                        'lane': lane,
                        'lane_title': LANE_TITLE[lane],
                        'badge': badge_text,
                        'reason': reason_text
                    })

        # 2. Gợi ý FLEX SWAP nếu có tướng trong đội hình có thể chuyển sang lane trống khác
        for occupied_role, occ_champ in picks_dict.items():
            inv_lane = {'top': 'top', 'jng': 'jungle', 'mid': 'mid', 'bot': 'bot', 'sup': 'support'}.get(occupied_role, occupied_role)
            alt_lanes = engine.pick_recommender.get_candidate_lanes_for_champion(occ_champ, available_lanes)
            viable_alts = [al for al in alt_lanes if al[0] in available_lanes and al[1] >= 10]
            if viable_alts:
                best_alt = viable_alts[0][0]
                swap_cands = engine.pick_recommender.recommend_picks(
                    inv_lane,
                    list(picks_dict.values()),
                    list(enemy_picks_dict.values()),
                    already_banned=all_banned,
                    top_k=2
                )
                for sc in swap_cands:
                    if sc['champion'] not in all_banned and sc['champion'] not in get_all_picked() and sc['champion'] != occ_champ:
                        cands.append({
                            'champion': sc['champion'],
                            'score': sc['score'] + 0.04,
                            'priority_pct': min(99.0, round((sc['score'] + 0.04) * 100, 1)),
                            'lane': inv_lane,
                            'lane_title': LANE_TITLE[inv_lane],
                            'badge': f"🔄 FLEX SWAP (XOAY {occ_champ.upper()} -> {LANE_TITLE[best_alt].upper()})",
                            'reason': f"Pick {sc['champion']} {LANE_TITLE[inv_lane]} để đẩy {occ_champ} sang {LANE_TITLE[best_alt]} né kèo counter đối thủ!"
                        })

        # Sắp xếp và lấy top 5 lựa chọn đa dạng theo vị trí
        unique_cands = []
        seen_c = set()
        
        # 1. Đảm bảo mỗi lane còn trống có đại diện số 1
        for lane in available_lanes:
            lane_items = [c for c in sorted(cands, key=lambda x: x['priority_pct'], reverse=True) if c.get('lane') == lane]
            if lane_items and lane_items[0]['champion'] not in seen_c:
                seen_c.add(lane_items[0]['champion'])
                unique_cands.append(lane_items[0])

        # 2. Bổ sung các lựa chọn có điểm cao nhất còn lại
        for c in sorted(cands, key=lambda x: x['priority_pct'], reverse=True):
            if c['champion'] not in seen_c:
                seen_c.add(c['champion'])
                unique_cands.append(c)

        return sorted(unique_cands[:7], key=lambda x: x['priority_pct'], reverse=True)

    # 1. T1 Pick 1 (FIRST PICK)
    cands_p1 = generate_pick_candidates(t1_name, t1_roster, t1_picks, t1_available_lanes, t2_picks, is_t1_pick=True)
    if interactive and is_user_t1:
        print(f"\n👉 LƯỢT CỦA BẠN: {t1_color} [{t1_name.upper()} 1 - FIRST PICK]")
        chosen_p1 = prompt_user_selection(cands_p1, f"Lựa chọn mở đầu (First Pick) cho {t1_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t2_roster, my_picks=t1_picks, enemy_picks=t2_picks, available_lanes=t1_available_lanes, team_roster=t1_roster, user_team_name=t1_name)
        p1_prefix = f"🔒 {t1_color}"
    else:
        chosen_p1 = cands_p1[0]
        p1_prefix = f"🤖 {t1_color}"
    p1_champ = chosen_p1['champion']
    p1_desired_lane = chosen_p1.get('lane', engine.pick_recommender.metadata.get(p1_champ, {}).get('lane', 'mid'))
    p1_actual_lane = assign_champion_to_lane(t1_name, t1_picks, t1_available_lanes, p1_champ, p1_desired_lane, t1_roster, engine)
    if p1_champ in active_wishlist:
        active_wishlist.remove(p1_champ)
    print(f"{p1_prefix} [{t1_name} FIRST PICK]: ⭐ {p1_champ.upper()} ({LANE_TITLE[p1_actual_lane]} - {t1_roster[LANE_TO_ROSTER_KEY[p1_actual_lane]]}) [{chosen_p1.get('reason','')}]")

    # 2. T2 Pick 1 & 2
    for r_turn in [1, 2]:
        cands_r = generate_pick_candidates(t2_name, t2_roster, t2_picks, t2_available_lanes, t1_picks, is_t1_pick=False)
        if interactive and is_user_t2:
            print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()} PICK {r_turn}]")
            chosen_r = prompt_user_selection(cands_r, f"Lượt chọn thứ {r_turn} của {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t1_roster, my_picks=t2_picks, enemy_picks=t1_picks, available_lanes=t2_available_lanes, team_roster=t2_roster, user_team_name=t2_name)
            r_prefix = f"🔒 {t2_color}"
        else:
            chosen_r = cands_r[0]
            r_prefix = f"🤖 {t2_color}"
        r_champ = chosen_r['champion']
        r_desired_lane = chosen_r.get('lane', engine.pick_recommender.metadata.get(r_champ, {}).get('lane', 'top'))
        r_actual_lane = assign_champion_to_lane(t2_name, t2_picks, t2_available_lanes, r_champ, r_desired_lane, t2_roster, engine)
        if r_champ in active_wishlist:
            active_wishlist.remove(r_champ)
        print(f"{r_prefix} [{t2_name} PICK {r_turn}]: ⭐ {r_champ.upper()} ({LANE_TITLE[r_actual_lane]} - {t2_roster[LANE_TO_ROSTER_KEY[r_actual_lane]]}) [{chosen_r.get('reason','')}]")

    # 3. T1 Pick 2 & 3
    for b_turn in [2, 3]:
        cands_b = generate_pick_candidates(t1_name, t1_roster, t1_picks, t1_available_lanes, t2_picks, is_t1_pick=True)
        if interactive and is_user_t1:
            print(f"\n👉 LƯỢT CỦA BẠN: {t1_color} [{t1_name.upper()} PICK {b_turn}]")
            chosen_b = prompt_user_selection(cands_b, f"Lượt chọn thứ {b_turn} của {t1_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t2_roster, my_picks=t1_picks, enemy_picks=t2_picks, available_lanes=t1_available_lanes, team_roster=t1_roster, user_team_name=t1_name)
            b_prefix = f"🔒 {t1_color}"
        else:
            chosen_b = cands_b[0]
            b_prefix = f"🤖 {t1_color}"
        b_champ = chosen_b['champion']
        b_desired_lane = chosen_b.get('lane', engine.pick_recommender.metadata.get(b_champ, {}).get('lane', 'bot'))
        b_actual_lane = assign_champion_to_lane(t1_name, t1_picks, t1_available_lanes, b_champ, b_desired_lane, t1_roster, engine)
        if b_champ in active_wishlist:
            active_wishlist.remove(b_champ)
        print(f"{b_prefix} [{t1_name} PICK {b_turn}]: ⭐ {b_champ.upper()} ({LANE_TITLE[b_actual_lane]} - {t1_roster[LANE_TO_ROSTER_KEY[b_actual_lane]]}) [{chosen_b.get('reason','')}]")

    # 4. T2 Pick 3
    cands_r3 = generate_pick_candidates(t2_name, t2_roster, t2_picks, t2_available_lanes, t1_picks, is_t1_pick=False)
    if interactive and is_user_t2:
        print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()} PICK 3]")
        chosen_r3 = prompt_user_selection(cands_r3, f"Lượt chọn thứ 3 của {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t1_roster, my_picks=t2_picks, enemy_picks=t1_picks, available_lanes=t2_available_lanes, team_roster=t2_roster, user_team_name=t2_name)
        r3_prefix = f"🔒 {t2_color}"
    else:
        chosen_r3 = cands_r3[0]
        r3_prefix = f"🤖 {t2_color}"
    r3_champ = chosen_r3['champion']
    r3_desired_lane = chosen_r3.get('lane', engine.pick_recommender.metadata.get(r3_champ, {}).get('lane', 'mid'))
    r3_actual_lane = assign_champion_to_lane(t2_name, t2_picks, t2_available_lanes, r3_champ, r3_desired_lane, t2_roster, engine)
    if r3_champ in active_wishlist:
        active_wishlist.remove(r3_champ)
    print(f"{r3_prefix} [{t2_name} PICK 3]: ⭐ {r3_champ.upper()} ({LANE_TITLE[r3_actual_lane]} - {t2_roster[LANE_TO_ROSTER_KEY[r3_actual_lane]]}) [{chosen_r3.get('reason','')}]")

    # =========================================================================
    # GIAI ĐOẠN 3: CẤM 2 (T2_Ban4 -> T1_Ban4 -> T1_Ban5 -> T2_Ban5)
    # =========================================================================
    print("\n" + "─" * 34 + " GIAI ĐOẠN 3: CẤM 2 (PHASE 2 BANS - 4 LƯỢT) " + "─" * 34)
    print(f"🎯 Thể thức Cấm 2: {t2_name} cấm 4 -> {t1_name} cấm 4 & 5 -> {t2_name} cấm 5\n")

    # 1. T2 Ban 4
    t1_rem_l1 = LANE_TO_ROSTER_KEY[t1_available_lanes[0]] if t1_available_lanes else 'top'
    cands_p2_r4 = [c for c in engine.target_ban_engine.recommend_target_bans(t1_roster[t1_rem_l1], top_k=6, ban_phase=2) if c['champion'] not in all_banned and c['champion'] not in get_all_picked()]
    for c in cands_p2_r4:
        c['reason'] = f"Chặn bài tủ còn lại của {t1_roster[t1_rem_l1]} ({c.get('tournament_stats','')})"
        c['priority_pct'] = round(c['threat_score'] * 100, 1)

    if interactive and is_user_t2:
        print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()}_BAN 4]")
        chosen_r4_b = prompt_user_selection(cands_p2_r4[:5], f"Lượt Cấm 4 của {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=True, enemy_roster=t1_roster, ban_phase=2, user_team_name=t2_name)
        ban_r4 = chosen_r4_b['champion']
        print(f"🔒 {t2_color} [{t2_name.upper()} ĐÃ CẤM 4]: 🚫 {ban_r4.upper()} ({chosen_r4_b.get('priority_pct', 90.0)}%) [{chosen_r4_b.get('reason','')}]")
    else:
        ban_r4 = cands_p2_r4[0]['champion'] if cands_p2_r4 else 'Poppy'
        print(f"🤖 {t2_color} [{t2_name.upper()}_BAN 4]: 🚫 {ban_r4.upper()} (Target vào {t1_roster[t1_rem_l1]})")
    all_banned.add(ban_r4)
    t2_bans.append(ban_r4)

    # 2. T1 Ban 4 & 5
    for b_idx, l_idx in [(4, 0), (5, -1)]:
        t2_rem_l = LANE_TO_ROSTER_KEY[t2_available_lanes[l_idx]] if t2_available_lanes else 'top'
        cands_p2_b = [c for c in engine.target_ban_engine.recommend_target_bans(t2_roster[t2_rem_l], top_k=6, ban_phase=2) if c['champion'] not in all_banned and c['champion'] not in get_all_picked()]
        for c in cands_p2_b:
            c['reason'] = f"Chặn bài tủ còn lại của {t2_roster[t2_rem_l]} ({c.get('tournament_stats','')})"
            c['priority_pct'] = round(c['threat_score'] * 100, 1)

        if interactive and is_user_t1:
            print(f"\n👉 LƯỢT CỦA BẠN: {t1_color} [{t1_name.upper()}_BAN {b_idx}]")
            chosen_b_p2 = prompt_user_selection(cands_p2_b[:5], f"Lượt Cấm {b_idx} của {t1_name}", all_banned, get_all_picked(), engine, is_ban_mode=True, enemy_roster=t2_roster, ban_phase=2, user_team_name=t1_name)
            ban_b_val = chosen_b_p2['champion']
            print(f"🔒 {t1_color} [{t1_name.upper()} ĐÃ CẤM {b_idx}]: 🚫 {ban_b_val.upper()} ({chosen_b_p2.get('priority_pct',90.0)}%) [{chosen_b_p2.get('reason','')}]")
        else:
            chosen_b_p2 = cands_p2_b[0] if cands_p2_b else {'champion': 'Nautilus', 'priority_pct': 85.0}
            ban_b_val = chosen_b_p2['champion']
            print(f"🤖 {t1_color} [{t1_name.upper()} ĐÃ CẤM {b_idx}]: 🚫 {ban_b_val.upper()} (Target vào {t2_roster[t2_rem_l]})")
        all_banned.add(ban_b_val)
        t1_bans.append(ban_b_val)

    # 3. T2 Ban 5
    t1_rem_l2 = LANE_TO_ROSTER_KEY[t1_available_lanes[-1]] if t1_available_lanes else 'top'
    cands_p2_r5 = [c for c in engine.target_ban_engine.recommend_target_bans(t1_roster[t1_rem_l2], top_k=6, ban_phase=2) if c['champion'] not in all_banned and c['champion'] not in get_all_picked()]
    for c in cands_p2_r5:
        c['reason'] = f"Chặn bài tủ còn lại của {t1_roster[t1_rem_l2]} ({c.get('tournament_stats','')})"
        c['priority_pct'] = round(c['threat_score'] * 100, 1)

    if interactive and is_user_t2:
        print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()}_BAN 5]")
        chosen_r5_b = prompt_user_selection(cands_p2_r5[:5], f"Lượt Cấm 5 của {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=True, enemy_roster=t1_roster, ban_phase=2, user_team_name=t2_name)
        ban_r5 = chosen_r5_b['champion']
        print(f"🔒 {t2_color} [{t2_name.upper()} ĐÃ CẤM 5]: 🚫 {ban_r5.upper()} ({chosen_r5_b.get('priority_pct', 90.0)}%) [{chosen_r5_b.get('reason','')}]")
    else:
        ban_r5 = cands_p2_r5[0]['champion'] if cands_p2_r5 else 'Nautilus'
        print(f"🤖 {t2_color} [{t2_name.upper()}_BAN 5]: 🚫 {ban_r5.upper()} (Target vào {t1_roster[t1_rem_l2]})")
    all_banned.add(ban_r5)
    t2_bans.append(ban_r5)

    # =========================================================================
    # GIAI ĐOẠN 4: CHỌN 2 (T2(1) -> T1(2) -> T2(1 - LAST PICK))
    # =========================================================================
    print("\n" + "─" * 38 + " GIAI ĐOẠN 4: CHỌN 2 (PHASE 2 PICKS) " + "─" * 38)

    # 1. T2 Pick 4
    cands_r4 = generate_pick_candidates(t2_name, t2_roster, t2_picks, t2_available_lanes, t1_picks, is_t1_pick=False)
    if interactive and is_user_t2:
        print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()} PICK 4]")
        chosen_r4 = prompt_user_selection(cands_r4, f"Lượt chọn thứ 4 của {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t1_roster, my_picks=t2_picks, enemy_picks=t1_picks, available_lanes=t2_available_lanes, team_roster=t2_roster, user_team_name=t2_name)
        r4_prefix = f"🔒 {t2_color}"
    else:
        chosen_r4 = cands_r4[0]
        r4_prefix = f"🤖 {t2_color}"
    r4_champ = chosen_r4['champion']
    r4_desired_lane = chosen_r4.get('lane', t2_available_lanes[0])
    r4_actual_lane = assign_champion_to_lane(t2_name, t2_picks, t2_available_lanes, r4_champ, r4_desired_lane, t2_roster, engine)
    print(f"{r4_prefix} [{t2_name} PICK 4]: ⭐ {r4_champ.upper()} ({LANE_TITLE[r4_actual_lane]} - {t2_roster[LANE_TO_ROSTER_KEY[r4_actual_lane]]}) [{chosen_r4.get('reason','')}]")

    # 2. T1 Pick 4 & 5
    for p_idx in [4, 5]:
        cands_p = generate_pick_candidates(t1_name, t1_roster, t1_picks, t1_available_lanes, t2_picks, is_t1_pick=True)
        if interactive and is_user_t1:
            print(f"\n👉 LƯỢT CỦA BẠN: {t1_color} [{t1_name.upper()} PICK {p_idx}]")
            chosen_p = prompt_user_selection(cands_p, f"Lượt chọn thứ {p_idx} hoàn thiện đội hình {t1_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t2_roster, my_picks=t1_picks, enemy_picks=t2_picks, available_lanes=t1_available_lanes, team_roster=t1_roster, user_team_name=t1_name)
            p_prefix = f"🔒 {t1_color}"
        else:
            chosen_p = cands_p[0]
            p_prefix = f"🤖 {t1_color}"
        p_champ = chosen_p['champion']
        p_desired_lane = chosen_p.get('lane', t1_available_lanes[0])
        p_actual_lane = assign_champion_to_lane(t1_name, t1_picks, t1_available_lanes, p_champ, p_desired_lane, t1_roster, engine)
        print(f"{p_prefix} [{t1_name} PICK {p_idx}]: ⭐ {p_champ.upper()} ({LANE_TITLE[p_actual_lane]} - {t1_roster[LANE_TO_ROSTER_KEY[p_actual_lane]]}) [{chosen_p.get('reason','')}]")

    # 3. T2 Pick 5 (LAST PICK)
    cands_r5 = generate_pick_candidates(t2_name, t2_roster, t2_picks, t2_available_lanes, t1_picks, is_t1_pick=False)
    if interactive and is_user_t2:
        print(f"\n👉 LƯỢT CỦA BẠN: {t2_color} [{t2_name.upper()} LAST PICK 5 (COUNTER ĐỐI THỦ)]")
        chosen_r5 = prompt_user_selection(cands_r5, f"Lựa chọn then chốt cuối cùng (Counter Last Pick) cho {t2_name}", all_banned, get_all_picked(), engine, is_ban_mode=False, enemy_roster=t1_roster, my_picks=t2_picks, enemy_picks=t1_picks, available_lanes=t2_available_lanes, team_roster=t2_roster, user_team_name=t2_name)
        r5_prefix = f"🔒 {t2_color}"
    else:
        chosen_r5 = cands_r5[0]
        r5_prefix = f"🤖 {t2_color}"
    r5_champ = chosen_r5['champion']
    r5_desired_lane = chosen_r5.get('lane', t2_available_lanes[0])
    r5_actual_lane = assign_champion_to_lane(t2_name, t2_picks, t2_available_lanes, r5_champ, r5_desired_lane, t2_roster, engine)
    print(f"{r5_prefix} [{t2_name} LAST PICK 5]: ⭐ {r5_champ.upper()} ({LANE_TITLE[r5_actual_lane]} - {t2_roster[LANE_TO_ROSTER_KEY[r5_actual_lane]]}) [{chosen_r5.get('reason','')}]")

    blue_picks = t1_picks if first_side.lower() == "blue" else t2_picks
    red_picks = t2_picks if first_side.lower() == "blue" else t1_picks

    _display_summary_and_win_conditions(blue_team_name, red_team_name, blue_picks, red_picks, blue_roster, red_roster, engine)


# =========================================================================
# HELPER: HIỂN THỊ TỔNG KẾT, THẺ CHIẾN THUẬT & DỰ ĐOÁN TỶ LỆ THẮNG
# =========================================================================
def _display_summary_and_win_conditions(blue_team_name, red_team_name, blue_picks, red_picks, blue_roster, red_roster, engine):
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

    # 3. Dự Đoán Xác Suất Thắng Thua
    print("\n" + "─" * 35 + " DỰ ĐOÁN XÁC SUẤT THẮNG THUA (PHÚT 0) " + "─" * 35)
    blue_early = blue_win_res['radar_scores']['Early_Power']
    red_early = red_win_res['radar_scores']['Early_Power']
    blue_late = blue_win_res['radar_scores']['Scaling']
    red_late = red_win_res['radar_scores']['Scaling']

    blue_prob = 0.525 + (blue_early - red_early) * 0.15 + (blue_late - red_late) * 0.10
    blue_prob = round(float(np.clip(blue_prob, 0.35, 0.68)), 3)
    red_prob = round(1.0 - blue_prob, 3)

    print(f"🔷 TỶ LỆ THẮNG DỰ BÁO {blue_team_name.upper()} (BLUE): {round(blue_prob * 100, 1)}%")
    print(f"🔴 TỶ LỆ THẮNG DỰ BÁO {red_team_name.upper()} (RED) : {round(red_prob * 100, 1)}%")
    print("-" * 95)
    if blue_prob > red_prob:
        print(f"🏆 ĐÁNH GIÁ TỔNG QUAN: {blue_team_name} có lợi thế cấm chọn tốt hơn (+{round((blue_prob - red_prob)*100, 1)}%), kiểm soát nhịp độ trận đấu.")
    else:
        print(f"🏆 ĐÁNH GIÁ TỔNG QUAN: {red_team_name} có lợi thế tương tác đội hình tốt hơn (+{round((red_prob - blue_prob)*100, 1)}%).")

    print("=" * 95 + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Full Match Ban/Pick Interactive Simulation (Pro Play 2026)")
    parser.add_argument('--wishlist', type=str, default="", help="Tướng hoặc đội hình chiến thuật dự kiến (VD: 'Orianna' hoặc 'Zeri,Lulu')")
    parser.add_argument('--blue-team', type=str, default="", help="Tên Phe Xanh")
    parser.add_argument('--red-team', type=str, default="", help="Tên Phe Đỏ")
    parser.add_argument('--user-side', type=str, default="blue", choices=["blue", "red"], help="Phe bạn điều khiển ('blue' hoặc 'red')")
    parser.add_argument('--auto', action='store_true', help="Chạy chế độ tự động (không chờ phím bấm)")
    args = parser.parse_args()

    blue_team = args.blue_team
    red_team = args.red_team
    user_side = args.user_side
    wishlist_list = [c.strip() for c in args.wishlist.split(',')] if args.wishlist else None

    # Nếu không truyền tham số qua CLI và không phải chế độ auto -> hiển thị Menu chọn kịch bản
    if not blue_team and not red_team and not args.auto:
        print("\n" + "=" * 95)
        print("🎮 CHỌN TRẬN ĐẤU MÔ PHỎNG CẤM / CHỌN TOURNAMENT DRAFT (LCK/WORLDS 2026):")
        print("=" * 95)
        print("  [1] 🌟 ĐỘI VÔ DANH (Bạn - Phe Xanh First Pick) vs T1 (Faker, Oner, Keria, Doran, Peyz)")
        print("  [2] 🔴 ĐỘI VÔ DANH (Bạn - Phe Đỏ Counter Last Pick) vs T1 (Thách thức Quỷ Vương)")
        print("  [3] ⚔️ T1 (Bạn - Phe Xanh) vs GEN.G (Chovy, Canyon, Ruler, Kiin, Lehends)")
        print("  [4] 🇻🇳 GAM Esports (Bạn - Phe Xanh) vs T1 (Kiaya, Levi vs Faker, Oner)")
        print("  [5] ⚙️ Tùy chỉnh đội tuyển & Phe thi đấu")
        print("─" * 95)
        
        try:
            choice = input("👉 Nhập số (1-5, Mặc định [1]): ").strip()
        except EOFError:
            choice = "1"

        if choice == "2":
            blue_team = "T1"
            red_team = "ĐỘI VÔ DANH"
            user_side = "red"
        elif choice == "3":
            blue_team = "T1"
            red_team = "GEN.G"
            user_side = "blue"
        elif choice == "4":
            blue_team = "GAM"
            red_team = "T1"
            user_side = "blue"
        elif choice == "5":
            blue_team = input("   Nhập tên Phe Xanh (VD: T1, BLG, ĐỘI VÔ DANH): ").strip() or "ĐỘI VÔ DANH"
            red_team = input("   Nhập tên Phe Đỏ (VD: T1, GEN.G): ").strip() or "T1"
            side_in = input("   Bạn điều khiển phe nào? (blue/red, mặc định blue): ").strip().lower()
            user_side = "red" if side_in == "red" else "blue"
        else: # Mặc định [1]
            blue_team = "ĐỘI VÔ DANH"
            red_team = "T1"
            user_side = "blue"
    else:
        blue_team = blue_team or "T1"
        red_team = red_team or "Gen.G"

    run_pro_tournament_draft_simulation(
        blue_team_name=blue_team,
        red_team_name=red_team,
        user_side=user_side,
        first_side="blue",
        wishlist=wishlist_list,
        interactive=not args.auto
    )
