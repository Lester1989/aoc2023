"""DAY 4"""
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
    input_data = pathlib.Path('23/4_data.txt').read_text(encoding='utf-8')
    input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
