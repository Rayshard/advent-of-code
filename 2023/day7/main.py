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


def get_hand_type(hand: str, j_is_joker: bool) -> HandType:
    mapping = defaultdict(int)

    for c in hand:
        mapping[c] += 1

    if not j_is_joker or mapping.get("J", 0) == 0:
        match len(mapping):
            case 5: return HandType.HIGH_CARD
            case 4: return HandType.ONE_PAIR
            case 3 if 2 in mapping.values(): return HandType.TWO_PAIR
            case 3 if 3 in mapping.values(): return HandType.THREE_OF_A_KIND
            case 2 if 3 in mapping.values(): return HandType.FULL_HOUSE
            case 2 if 4 in mapping.values(): return HandType.FOUR_OF_A_KIND
            case 1: return HandType.FIVE_OF_A_KIND
    else:
        mapping.pop("J")

        match list(sorted(mapping.values(), reverse=True)):
            case []: return HandType.FIVE_OF_A_KIND
            case [_]: return HandType.FIVE_OF_A_KIND
            case [1, 1, 1, 1]: return HandType.ONE_PAIR # 1 joker
            case [2, 1, 1]: return HandType.THREE_OF_A_KIND # 1 joker
            case [3, 1]: return HandType.FOUR_OF_A_KIND # 1 joker
            case [2, 2]: return HandType.FULL_HOUSE # 1 joker
            case [1, 1, 1]: return HandType.THREE_OF_A_KIND # 2 jokers
            case [2, 1]: return HandType.FOUR_OF_A_KIND # 2 jokers
            case [1, 1]: return HandType.FOUR_OF_A_KIND # 3 jokers
            case other: raise NotImplementedError(other)


class Hand:
    CARD_VALUES_WITH_J_AS_JACK = {c:i for i, c in enumerate("23456789TJQKA")}
    CARD_VALUES_WITH_J_AS_JOKER = {c:i for i, c in enumerate("J23456789TQKA")}
    
    def __init__(self, value: str, j_is_joker: bool) -> None:
        self.value = value
        self.type = get_hand_type(self.value, j_is_joker)
        self.card_values = Hand.CARD_VALUES_WITH_J_AS_JOKER if j_is_joker else Hand.CARD_VALUES_WITH_J_AS_JACK

    def __lt__(self, other: "Hand") -> bool:
        if self.type == other.type:
            for l, r in zip(self.value, other.value):
                if l != r:
                    return self.card_values[l] < self.card_values[r]
                
            return False
        
        return self.type < other.type


def part1(file: TextIOWrapper) -> int:
    game = ((Hand(hand, j_is_joker=False), int(bid)) for hand, bid in (line.split() for line in file))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(sorted(game)))

def part2(file: TextIOWrapper) -> int:
    game = ((Hand(hand, j_is_joker=True), int(bid)) for hand, bid in (line.split() for line in file))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(sorted(game)))


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
    
    with open("input.txt") as file:
        print(part2(file))
