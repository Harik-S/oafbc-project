from UtilClasses import Card

SUITS = ["D", "H", "C", "S"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def generate_card_deck() -> list[Card]:
    return [Card(suit, rank) for suit in SUITS for rank in RANKS]
