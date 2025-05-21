from .player import Player

class Game:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.player = Player()
        self.round = 1
        self.target_score = 100
        self._init_hand_rankings()
        
    def _init_hand_rankings(self):
        self.hand_rankings = {
            'High Card': lambda r,s,c: True,
            'Pair': lambda r,s,c: len(c) >= 2 and any(r.count(rank) >= 2 for rank in set(r)),
            # ... rest of hand rankings ...
        }
    
    def is_flush(self, suits):
        return len(set(suits)) == 1
    
    def is_straight(self, ranks):
        sorted_ranks = sorted(ranks)
        return (max(sorted_ranks) - min(sorted_ranks) == 4 and len(set(sorted_ranks)) == 5) or \
               set(sorted_ranks) == {2,3,4,5,14}
    
    def evaluate_hand(self, cards):
        ranks = [c.rank for c in cards]
        suits = [c.suit for c in cards]
        
        for hand in reversed(self.hand_rankings.keys()):
            if self.hand_rankings[hand](ranks, suits, cards):
                return hand
        return 'High Card'
    
    def calculate_score(self, hand_type):
        base_scores = {
            'High Card': 10,
            'Pair': 20,
            # ... rest of scores ...
        }
        return base_scores.get(hand_type, 0) * self.player.multiplier + self.player.chips