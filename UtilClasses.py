SUIT_SYMBOLS = {
    "C": "♣",
    "D": "♦",
    "H": "♥",
    "S": "♠",
}


class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit = SUIT_SYMBOLS[suit]
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: "Card"):
        return self.rank == other.rank and self.suit == other.suit
