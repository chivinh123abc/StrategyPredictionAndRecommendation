"""Preserve observed bot partnerships across a ban window; no search tree.

Association is not mechanical synergy. A ban budget is a worst-case capacity,
not a prediction that the opponent will spend those bans on these champions.
"""
PAIR_SAFETY_VERSION='bot_reservation_v1'
BOT_PARTNER={'bot':'sup','sup':'bot'}


def enemy_bans_before_next_pick(state,side):
    enemy='red' if side=='blue' else 'blue'
    count=0
    for actor,action in state.schedule[len(state.history)+1:]:
        if actor==side and action=='pick':break
        if actor==enemy and action=='ban':count+=1
    return count


def reserve_pairs(rows,advisor,state,side,region):
    """Preserve scores; attach an explicit scheduling-priority tier.

    Partners are drawn from complete, legal role candidate lists. User role
    filters are applied after this check so they do not falsify pool counts.
    """
    enemy='red' if side=='blue' else 'blue'
    if not all(role in state.picks[enemy] for role in BOT_PARTNER):return rows
    snapshot=advisor.context(region)[0]
    minimum=advisor.policy.min_games
    budget=enemy_bans_before_next_pick(state,side)
    own=state.picks[side]
    pools={role:[r for r in rows if r['role']==role] for role in BOT_PARTNER}
    cache={}

    def partners(anchor_role,anchor,excluded=None):
        missing=BOT_PARTNER[anchor_role]
        key=(anchor_role,anchor)
        if key not in cache:
            options=[]
            for row in pools[missing]:
                if row['champion']==anchor or row['champion'] in state.unavailable:continue
                ev=snapshot.pair_evidence(missing,row['champion'],anchor_role,anchor,minimum)
                if ev['games']>=minimum and (ev.get('effective_lift') or 0)>=1:
                    options.append({'champion':row['champion'],'games':ev['games'],
                        'winrate':ev['winrate'],'ci95_wilson':ev['ci95_wilson'],
                        'effective_lift':ev['effective_lift']})
            cache[key]=options
        return [p for p in cache[key] if p['champion']!=excluded]

    partial=[r for r in BOT_PARTNER if r in own]
    initial_options=partners(partial[0],own[partial[0]]) if len(partial)==1 else []
    endangered=budget>0 and 0<len(initial_options)<=budget
    result=[]
    for original in rows:
        row=dict(original);after={**own,row['role']:row['champion']}
        present=[r for r in BOT_PARTNER if r in after]
        info={'version':PAIR_SAFETY_VERSION,'enemy_bans_before_next_own_pick':budget,
              'opponent_bot_revealed':True,'priority_tier':1,'requires_review':False,
              'interpretation':'observed_co_pick_support_not_mechanical_synergy'}
        if len(present)==2:
            ev=snapshot.pair_evidence('bot',after['bot'],'sup',after['sup'],minimum)
            supported=ev['games']>=minimum and (ev.get('effective_lift') or 0)>=1
            info.update(status='completed_supported' if supported else 'completed_insufficient_support',
                        pair_evidence=ev,requires_review=not supported and row['role'] in BOT_PARTNER)
            if endangered and supported:
                info.update(status='secure_now',priority_tier=0)
                info['reason']=(f"Giữ cặp bot ngay: chỉ còn {len(initial_options)} đối tác có n≥{minimum} "
                    f"và association≥1; địch có {budget} lượt ban trước lượt pick kế tiếp. "
                    'Đây là phòng ngừa theo lịch, không dự đoán chắc địch sẽ ban.')
            elif not supported:
                info['reason']=f"Cặp bot có {ev['games']} mẫu; chưa đạt cả ngưỡng n≥{minimum} và association≥1. Không xác nhận cặp yếu hay tối ưu."
        elif len(present)==1:
            anchor_role=present[0];anchor=after[anchor_role]
            options=partners(anchor_role,anchor,row['champion'] if row['role']!=anchor_role else None)
            fragile=budget>0 and 0<len(options)<=budget
            info.update(status='at_risk' if fragile else 'insufficient_history' if not options else 'partners_available',
                anchor_role=anchor_role,anchor=anchor,missing_role=BOT_PARTNER[anchor_role],
                supported_partners=options,supported_partner_count=len(options),
                worst_case_partners_remaining=max(0,len(options)-budget),
                requires_review=budget>0 and not options)
            if fragile:
                info['reason']=(f"Để {anchor} chờ ghép: còn {len(options)} đối tác đủ mẫu; "
                    f"địch có {budget} lượt ban trước lượt pick tiếp. Có thể mất toàn bộ nhóm này.")
                if not partial or row['champion'] in {p['champion'] for p in initial_options}:
                    info['priority_tier']=2
            elif not options:
                info['reason']='Chưa có đối tác đạt ngưỡng lịch sử trong pool hợp lệ; thiếu mẫu không chứng minh không phối hợp được.'
        else:
            result.append(row);continue
        row['pair_reservation']=info
        if info.get('reason'):row['reasons']=[info['reason'],*row.get('reasons',[])]
        result.append(row)
    return result
