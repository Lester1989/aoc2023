"""DAY 9"""
from __future__ import annotations

import pathlib

def part_one(data:str):
    result = 0
    for line in data.splitlines():
        numbers = [int(x) for x in line.split()]
        generations = [numbers]
        print(numbers)
        result += numbers[-1]
        # down
        while any(x!=0 for x in generations[-1]):
            new_generation = []
            last_generation = generations[-1]
            for idx, number in enumerate(last_generation[:-1]):
                
                new_generation.append(last_generation[idx+1]-number)
            generations.append(new_generation)
            print(new_generation)
            result +=new_generation[-1]
        print()
        
    print(result)

def part_two(data:str):
    result = 0
    for line in data.splitlines():
        numbers = [int(x) for x in line.split()]
        generations = [numbers]
        print(numbers)
        # down
        while any(x!=0 for x in generations[-1]):
            new_generation = []
            last_generation = generations[-1]
            for idx, number in enumerate(last_generation[:-1]):
                
                new_generation.append(last_generation[idx+1]-number)
            generations.append(new_generation)
            print(new_generation)
        print()
        # up
        new_val = 0
        for current in generations[::-1]:
            print(new_val,current)
            new_val = current[0]-new_val
        result += new_val
        
    print('->',result)

EXAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/9_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
