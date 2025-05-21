class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return f"{self.rank_dict().get(self.rank, str(self.rank))}{self.suit[0]}"
    
    def rank_dict(self):
        return {
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
            **{i: str(i) for i in range(2, 11)}
        }