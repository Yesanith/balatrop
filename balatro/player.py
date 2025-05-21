import random
from .card import Card

class Player:
    def __init__(self):
        self.deck = []
        self.hand = []
        self.discard = []
        self.chips = 0
        self.multiplier = 1
        self.create_deck()
        
    def create_deck(self):
        suits = ['♥', '♦', '♣', '♠']
        ranks = list(range(2, 15))
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)
        
    def draw_hand(self, size=5):
        while len(self.hand) < size and self.deck:
            self.hand.append(self.deck.pop())
        if not self.deck:
            self.recycle_discard()
            
    def recycle_discard(self):
        self.deck = self.discard.copy()
        self.discard = []
        random.shuffle(self.deck)
        
    def discard_hand(self):
        self.discard.extend(self.hand)
        self.hand = []