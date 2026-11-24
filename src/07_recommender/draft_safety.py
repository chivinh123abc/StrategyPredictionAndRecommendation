"""Observed role frequencies and review of the explicitly assigned lane opponent."""
ROLES=['top','jng','mid','bot','sup']
LANE_REVIEW_VERSION='assigned_lane_review_v3'
MANUAL_ROLE_VERSION='observed_free_role_v1'


def lane_support_priority(row,enabled):
    """Only promote an adequately observed lane; never rank sparse Wilson CIs.

    The missing/low-sample tier shares the unchanged aggregate score ordering.
    This is evidence availability, not a claim that a supported matchup is good.
    """
    info=row.get('lane_review',{})
    return bool(enabled and info.get('opponent') and info.get('requires_review',False))


def role_preferences(snapshot):
    result={}
    for (role,champion),games in snapshot.role_counts.items():
        if role in ROLES and games>0:
            result.setdefault(champion,[]).append({'role':role,'games':int(games)})
    for rows in result.values():rows.sort(key=lambda r:(-r['games'],ROLES.index(r['role'])))
    return result


def infer_free_role(snapshot,champion,occupied):
    for row in role_preferences(snapshot).get(champion,[]):
        if row['role'] not in occupied:return row['role']
    raise ValueError('Không còn vị trí đã được quan sát và đang trống cho tướng này. Hãy kéo đổi đội hình để tạo chỗ hoặc chọn tướng khác.')


def annotate_lane_support(rows,snapshot,enemies,minimum):
    result=[]
    for original in rows:
        row=dict(original);role=row['role'];opponent=enemies.get(role)
        if opponent:
            evidence=snapshot.enemy_evidence(role,row['champion'],role,opponent)
            enough=evidence['games']>=minimum
            info={**evidence,'role':role,'opponent':opponent,'requires_review':not enough,
                'status':'observed_lane' if enough else 'insufficient_lane',
                'ranking_confidence_bound':evidence['ci95_wilson'][0],
                'ranking_basis':'adequate_lane_sample_tier_then_original_score_wilson_display_only',
                'version':LANE_REVIEW_VERSION,'assignment_source':'current_draft_role_not_inferred_counter'}
            if not enough:
                info['reason']=(f"Đối thủ cùng vị trí đã lộ: {opponent} ({role}); kèo này có "
                    f"{evidence['games']} mẫu Pro, dưới {minimum}. Không tự chốt dựa vào điểm tổng.")
                row['reasons']=[info['reason'],*row.get('reasons',[])]
        else:
            info={'version':LANE_REVIEW_VERSION,'role':role,'opponent':None,
                  'games':None,'status':'lane_not_revealed','requires_review':False}
        row['lane_review']=info;result.append(row)
    return result
