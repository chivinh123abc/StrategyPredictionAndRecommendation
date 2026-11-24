from pathlib import Path
import sys
import unittest

sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parents[1]/'src/07_recommender')]
from simulate_draft_match import DraftState,ROLES
from simulate_fearless_series import validate_game
from draft_advisor import AdvisorPolicy


def game(number,used,first='blue'):
    s=DraftState(first_side=first,used_champions=list(used))
    for turn,(side,action) in enumerate(s.schedule):
        if action=='ban':s.apply(side,action,f'{side}_Ban{len(s.bans[side])}')
        else:
            role=ROLES[len(s.picks[side])]
            s.apply(side,action,f'Game{number}_{side}_{role}',role)
    return s.as_dict()


class FearlessTests(unittest.TestCase):
    def test_five_games_carry_picks_for_both_teams_and_reset_bans(self):
        used=[]
        for n in range(1,6):
            g=game(n,used,'blue' if n%2 else 'red')
            self.assertEqual(len(g['used_champions']),10*(n-1))
            used=validate_game(g,used)
            self.assertFalse(set(g['bans']['blue']+g['bans']['red'])&set(used))
        self.assertEqual(len(set(used)),50)

    def test_repeated_pick_or_incomplete_game_is_rejected(self):
        g=game(1,[]);used=validate_game(g,[])
        with self.assertRaises(ValueError):validate_game(g,used)
        g=game(2,used);g['history'][6]['champion']=used[0]
        with self.assertRaises(ValueError):validate_game(g,used)
        g=game(2,used);g['complete']=False
        with self.assertRaises(ValueError):validate_game(g,used)

    def test_candidate_threshold_does_not_lower_evidence_threshold(self):
        policy=AdvisorPolicy(candidate_min_games=1)
        self.assertEqual(policy.min_games,5)
        self.assertEqual(policy.candidate_min_games,1)
        self.assertEqual(AdvisorPolicy().candidate_min_games,5)
        with self.assertRaises(ValueError):AdvisorPolicy(candidate_min_games=0)
