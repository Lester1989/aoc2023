"""DAY 22"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from tqdm import tqdm

@dataclass
class Block:
    coords:list[tuple[int,int,int]]
    name:str

def load_blocks(data:str) -> list[Block]:
    blocks:list[Block] = []
    for i,line in enumerate(data.splitlines()):
        name = str(i)
        start_coords,end_coords = line.split('~')
        start_coords = tuple(int(c) for c in start_coords.split(','))
        end_coords = tuple(int(c) for c in end_coords.split(','))
        if start_coords[0] != end_coords[0]:
            blocks.append(Block([(c,start_coords[1],start_coords[2]) for c in range(start_coords[0],end_coords[0]+1)],name))
        elif start_coords[1] != end_coords[1]:
            blocks.append(Block([(start_coords[0],c,start_coords[2]) for c in range(start_coords[1],end_coords[1]+1)],name))
        elif start_coords[2] != end_coords[2]:
            blocks.append(Block([(start_coords[0],start_coords[1],c) for c in range(start_coords[2],end_coords[2]+1)],name))
        else:
            blocks.append(Block([start_coords],name))
        
    print('loaded',len(blocks),'blocks')
    return blocks

def part_one(data:str):
    result = 0
    blocks = load_blocks(data)
    world:dict[tuple[int,int,int],str] = {}
    fall_blocks(world,blocks)
    # inspect_world(world)
    for desintegrated_block in tqdm(blocks):
        # print('\ndesintegrating',desintegrated_block.name)
        what_if_world = {
        }
        what_if_blocks = [
            Block(block.coords.copy(),block.name) for block in blocks
            if block.name != desintegrated_block.name
        ]
        # if desintegrated_block.name == 'F':
        #     inspect_world(what_if_world)
        if not fall_blocks(what_if_world,what_if_blocks):
            # print('block',desintegrated_block.name,'is not needed')
            result += 1
    print(result)

def fall_blocks(world:dict[tuple[int,int,int],str],blocks:list[Block])->int:
    fallen_block_names = set()
    for block in sorted(blocks,key=lambda b: b.coords[0][2]):
        # print(block)
        has_fallen = True
        while has_fallen:
            has_fallen = False
            for x,y,z in block.coords:
                if world.get((x,y,z-1),'#') not in ['#',block.name]  or z ==1:
                    # print('reached bottom or block')
                    break
            else:
                # print('falling')
                has_fallen = True
                block.coords = [(x,y,z-1) for x,y,z in block.coords]
                fallen_block_names.add(block.name)
        for x,y,z in block.coords:
            world[(x,y,z)] = block.name
    return len(fallen_block_names)

def inspect_world(world:dict[tuple[int,int,int],str]):
    while True:
        level = input('show lvl')
        if not level:
            break
        if any(z == int(level) for x,y,z in world.keys()):
            print('level',level)
        else:
            print('no level',level)
            continue
        max_x = max(x for x,y,z in world.keys() if z == int(level))
        max_y = max(y for x,y,z in world.keys() if z == int(level))
        for y in range(max_y+1):
            for x in range(max_x+1):
                # print(world.get((x,y,int(level)),'.') ,end='')
                print('#' if (x,y,int(level)) in world else '.',end='')
            print()

def part_two(data:str):
    result = 0
    blocks = load_blocks(data)
    world:dict[tuple[int,int,int],str] = {}
    fall_blocks(world,blocks)
    for desintegrated_block in tqdm(blocks):
        # print('\ndesintegrating',desintegrated_block.name)
        what_if_world = {
        }
        what_if_blocks = [
            Block(block.coords.copy(),block.name) for block in blocks
            if block.name != desintegrated_block.name
        ]
        # if desintegrated_block.name == 'F':
        #     inspect_world(what_if_world)
        result += fall_blocks(what_if_world,what_if_blocks)
    print(result)

EXAMPLE = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/22_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
