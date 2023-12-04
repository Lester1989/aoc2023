"""DAY 4"""
from __future__ import annotations

import pathlib

def part_one(data:str,verbosity:int=0):
    result = 0
    for line in data.splitlines():
        card,numbers_part = line.split(':')
        winning_numbers,elf_numbers = numbers_part.split('|')
        winning_numbers = {int(number) for number in winning_numbers.split() if number.isdigit()}
        elf_numbers = {int(number) for number in elf_numbers.split() if number.isdigit()}
        if matching_numbers := winning_numbers.intersection(elf_numbers):
            result += pow(2,len(matching_numbers)-1)
            if verbosity > 0:
                print(f"Points {pow(2,len(matching_numbers)-1)} for {card}")
        elif verbosity > 0:
            print(f'No points for {card}')


    print(result)

def part_two(data:str,verbosity:int=0):
    won_cards = {}
    for line in data.splitlines():
        card,numbers_part = line.split(':')
        card_number = int(card.split()[1])
        won_cards[card_number] = won_cards.get(card_number,0)+1
        winning_numbers,elf_numbers = numbers_part.split('|')
        winning_numbers = {int(number) for number in winning_numbers.split() if number.isdigit()}
        elf_numbers = {int(number) for number in elf_numbers.split() if number.isdigit()}
        won_next = len(winning_numbers.intersection(elf_numbers))
        for wn in range(won_next):
            won_cards[card_number+wn+1] = won_cards.get(card_number+wn+1,0)+won_cards[card_number]
        
    print(sum(won_cards.values()))

EXAMPLE = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/4_data_schroeder.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    part_one(input_data,1)
    print('--- PART TWO ---')
    part_two(input_data)
