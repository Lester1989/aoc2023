"""DAY 13"""
from __future__ import annotations

import pathlib

def mirror_vertical_at(grid:dict[tuple[int,int],str],mirror_after_x:int) -> bool:
    max_x = max(x for x,_ in grid.keys())
    max_y = max(y for _,y in grid.keys())
    # print()
    # print('checking',mirror_after_x)
    for y in range(1,max_y+1):
        # print(''.join(grid[(x,y)] for x in range(y,mirror_after_x+1)),'><',''.join(grid[(x,y)] for x in range(mirror_after_x+1,max_x+1)))
        for x in range(1,mirror_after_x+1):
            mirrored_x = int(2*(mirror_after_x+.5))-x
            # if y==1:
            #     print(x,'->',mirrored_x)
            #     print(grid[(x,y)],grid.get((mirrored_x,y),'-'))
            if (mirrored_x,y) in grid and grid[(x,y)] != grid[mirrored_x,y]:
                return False
    return True

def mirror_horizontal_at(grid:dict[tuple[int,int],str],mirror_after_y:int) -> bool:
    max_x = max(x for x,_ in grid.keys())
    max_y = max(y for _,y in grid.keys())
    # print()
    # print('checking',mirror_after_y)
    for x in range(1,max_x+1):
        # print(''.join(grid[(x,y)] for y in range(x,mirror_after_y+1)),'><',''.join(grid[(x,y)] for y in range(mirror_after_y+1,max_y+1)))
        for y in range(1,mirror_after_y+1):
            mirrored_y = int(2*(mirror_after_y+.5))-y
            # if x==1:
            #     print(y,'->',mirrored_y)
            #     print(grid[(x,y)],grid.get((x,mirrored_y),'-'))
            if (x,mirrored_y) in grid and grid[(x,y)] != grid[x,mirrored_y]:
                return False
    return True

def smudged_mirror_vertical_at(grid:dict[tuple[int,int],str],mirror_after_x:int) -> bool:
    max_x = max(x for x,_ in grid.keys())
    max_y = max(y for _,y in grid.keys())
    error_count = 0
    # print()
    # print('checking',mirror_after_x)
    for y in range(1,max_y+1):
        # print(''.join(grid[(x,y)] for x in range(y,mirror_after_x+1)),'><',''.join(grid[(x,y)] for x in range(mirror_after_x+1,max_x+1)))
        for x in range(1,mirror_after_x+1):
            mirrored_x = int(2*(mirror_after_x+.5))-x
            # if y==1:
            #     print(x,'->',mirrored_x)
            #     print(grid[(x,y)],grid.get((mirrored_x,y),'-'))
            if (mirrored_x,y) in grid and grid[(x,y)] != grid[mirrored_x,y]:
                error_count += 1
                if error_count > 1:
                    return False
    return error_count==1

def smudged_mirror_horizontal_at(grid:dict[tuple[int,int],str],mirror_after_y:int) -> bool:
    max_x = max(x for x,_ in grid.keys())
    max_y = max(y for _,y in grid.keys())
    error_count = 0
    # print()
    # print('checking',mirror_after_y)
    for x in range(1,max_x+1):
        # print(''.join(grid[(x,y)] for y in range(x,mirror_after_y+1)),'><',''.join(grid[(x,y)] for y in range(mirror_after_y+1,max_y+1)))
        for y in range(1,mirror_after_y+1):
            mirrored_y = int(2*(mirror_after_y+.5))-y
            # if x==1:
            #     print(y,'->',mirrored_y)
            #     print(grid[(x,y)],grid.get((x,mirrored_y),'-'))
            if (x,mirrored_y) in grid and grid[(x,y)] != grid[x,mirrored_y]:
                error_count += 1
                if error_count > 1:
                    return False
    return error_count==1

def part_one(data:str):
    result = 0
    for data_block in data.split('\n\n'):
        grid = {}
        for y,line in enumerate(data_block.splitlines()):
            for x,char in enumerate(line):
                grid[(x+1,y+1)] = char
        max_x = max(x for x,y in grid.keys())
        max_y = max(y for x,y in grid.keys())
        # check vertical mirroring
        for x in range(1,max_x):
            if mirror_vertical_at(grid,x):
                result += x
                break
        # check horizontal mirroring
        for y in range(1,max_y):
            if mirror_horizontal_at(grid,y):
                result += y*100
                break

    print(result)

def part_two(data:str):
    result = 0
    for data_block in data.split('\n\n'):
        grid = {}
        for y,line in enumerate(data_block.splitlines()):
            for x,char in enumerate(line):
                grid[(x+1,y+1)] = char
        max_x = max(x for x,y in grid.keys())
        max_y = max(y for x,y in grid.keys())
        # check vertical mirroring
        for x in range(1,max_x):
            if smudged_mirror_vertical_at(grid,x):
                result += x
                break
        # check horizontal mirroring
        for y in range(1,max_y):
            if smudged_mirror_horizontal_at(grid,y):
                result += y*100
                break
    print(result)

EXAMPLE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/13_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
