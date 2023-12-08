"""DAY 8"""
from __future__ import annotations

import pathlib
import math

def part_one(data:str):
    instructions = data.splitlines()[0]
    desert_map:dict[str,tuple[str,str]] = {}
    for line in data.splitlines()[2:]:
        node, left_right = line.split(' = ')
        desert_map[node] = tuple(left_right.strip('()').split(', '))
    
    instructions_count = len(instructions)
    location = 'AAA'
    steps = 0
    while location != 'ZZZ':
        location = desert_map[location][0] if instructions[steps%instructions_count] == 'L' else desert_map[location][1]
        steps += 1
    print(steps)

def part_two(data:str):
    instructions = data.splitlines()[0]
    desert_map:dict[str,tuple[str,str]] = {}
    z_enders = []
    locations:dict[str,str] = {}
    for line in data.splitlines()[2:]:
        node, left_right = line.split(' = ')
        desert_map[node] = tuple(left_right.strip('()').split(', '))
        if node[2] =="A":
            locations[node] = node
        elif node[2] == "Z":
            z_enders.append(node)
    
    ghost_hits = []
    for location in locations:
        ghost_location = location
        hits = []
        for ghost_step,instruction in enumerate( instructions*100):
            ghost_location = desert_map[ghost_location][0] if instruction == 'L' else desert_map[ghost_location][1]
            if ghost_location[2]=="Z":
                hits.append(ghost_step+1)
                break
        ghost_hits.append(hits)
    print(math.lcm(*[hits[0] for hits in ghost_hits]))

EXAMPLE = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

EXAMPLE2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/8_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE2
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
