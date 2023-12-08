"""DAY 7"""
from __future__ import annotations

import pathlib
import collections
from enum import Enum
ordering = '23456789TJQKA' 
ordering2 = 'J23456789TQKA' 

class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

def part_one(data:str):
    result = 0
    hands = []
    for line in data.splitlines():
        hand, bid = line.split()
        values = dict(collections.Counter(hand))        
        if len(values) == 1:
            hands.append((HandType.FIVE_OF_A_KIND, hand, bid))
        elif len(values) == 2:
            if max(values.values()) == 4:
                hands.append((HandType.FOUR_OF_A_KIND, hand, bid))
            else:
                hands.append((HandType.FULL_HOUSE, hand, bid))
        elif len(values) == 3:
            if max(values.values()) == 3:
                hands.append((HandType.THREE_OF_A_KIND, hand, bid))
            else:
                hands.append((HandType.TWO_PAIR, hand, bid))
        elif len(values) == 4:
            hands.append((HandType.ONE_PAIR, hand, bid))
        else:
            hands.append((HandType.HIGH_CARD, hand, bid))
    
    ordered_hands = sorted(hands, key=lambda x: (x[0].value, ordering.index(x[1][0]), ordering.index(x[1][1]), ordering.index(x[1][2]), ordering.index(x[1][3]), ordering.index(x[1][4])))
    for idx, hand in enumerate(ordered_hands):
        print(idx+1, hand)
        result += (idx+1)*int(hand[2])

    print(result)

def part_two(data:str):
    result = 0
    hands = []
    for line in data.splitlines():

        hand, bid = line.split()
        print(hand)
        values = dict(collections.Counter(hand))
        if 'J' in values and len(values) >= 2:
            # increase hightest non-joker
            joker_count = values.pop('J')
           
            highest = max(values.values())
            print(f'found {joker_count} jokers, increasing {highest}')
            for card, count in values.items():
                if count == highest:
                    print(f'increasing {card} by {joker_count}')
                    values[card] += joker_count
                    break

        if len(values) == 1:
            hands.append((HandType.FIVE_OF_A_KIND, hand, bid))
        elif len(values) == 2:
            if max(values.values()) == 4:
                hands.append((HandType.FOUR_OF_A_KIND, hand, bid))
            else:
                hands.append((HandType.FULL_HOUSE, hand, bid))
        elif len(values) == 3:
            if max(values.values()) == 3:
                hands.append((HandType.THREE_OF_A_KIND, hand, bid))
            else:
                hands.append((HandType.TWO_PAIR, hand, bid))
        elif len(values) == 4:
            hands.append((HandType.ONE_PAIR, hand, bid))
        else:
            hands.append((HandType.HIGH_CARD, hand, bid))
    
    ordered_hands = sorted(hands, key=lambda x: (x[0].value, ordering2.index(x[1][0]), ordering2.index(x[1][1]), ordering2.index(x[1][2]), ordering2.index(x[1][3]), ordering2.index(x[1][4])))
    for idx, hand in enumerate(ordered_hands):
        print(idx+1, hand)
        result += (idx+1)*int(hand[2])

    print(result)

EXAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/7_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
