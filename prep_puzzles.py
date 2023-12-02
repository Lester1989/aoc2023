import os
 
year = 23
 
if __name__ == "__main__":
    os.makedirs(f"{year}", exist_ok=True)
    for puzzle_number in range(1,27):
        if not os.path.exists(f"{year}/{puzzle_number}_data.txt"):
            with open(f"{year}/{puzzle_number}_data.txt", "w+") as f:
                f.write("")
        if not os.path.exists(f"{year}/{puzzle_number}_solution.py"):
            with open(f"{year}/{puzzle_number}_solution.py", "w+") as f:
                f.write( f'''"""DAY {puzzle_number}"""
from __future__ import annotations

import pathlib

def part_one(data:str):
    result = 0
    for line in data.splitlines():
        print(line)
    print(result)

def part_two(data:str):
    result = 0
    for line in data.splitlines():
        print(line)
    print(result)

EXAMPLE = """"""

if __name__ == "__main__":
    input_data = pathlib.Path('{year}/{puzzle_number}_data.txt').read_text(encoding='utf-8')
    input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
''' )