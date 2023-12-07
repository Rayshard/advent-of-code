from collections import defaultdict
from enum import IntEnum, auto
from io import TextIOWrapper

class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


def get_hand_type(hand: str) -> HandType:
    mapping = defaultdict(int)

    for c in hand:
        mapping[c] += 1

    match len(mapping):
        case 5: return HandType.HIGH_CARD
        case 4: return HandType.ONE_PAIR
        case 3 if 2 in mapping.values(): return HandType.TWO_PAIR
        case 3 if 3 in mapping.values(): return HandType.THREE_OF_A_KIND
        case 2 if 3 in mapping.values(): return HandType.FULL_HOUSE
        case 2 if 4 in mapping.values(): return HandType.FOUR_OF_A_KIND
        case 1: return HandType.FIVE_OF_A_KIND


class Hand:
    CARD_VALUES = {c:i for i, c in enumerate("23456789TJQKA")}
    
    def __init__(self, value: str) -> None:
        self.value = value
        self.type = get_hand_type(self.value)

    def __lt__(self, other: "Hand") -> bool:
        if self.type == other.type:
            for l, r in zip(self.value, other.value):
                if l != r:
                    return Hand.CARD_VALUES[l] < Hand.CARD_VALUES[r]
                
            return False
        
        return self.type < other.type


def part1(file: TextIOWrapper) -> int:
    game = ((Hand(hand), int(bid)) for hand, bid in (line.split() for line in file))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(sorted(game)))


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
