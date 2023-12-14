"""DAY 14"""
from __future__ import annotations
import pathlib
from tqdm import tqdm

def roll_north(grid:dict[tuple[int,int],str],max_x:int,max_y:int) -> bool:
    moved_at_all = False
    moved = True
    while moved:
        moved = False
        for y in range(1,max_y+1):
            for x in range(0,max_x+1):
                if grid[(x,y)] == 'O' and grid[(x,y-1)] == '.':
                    grid[(x,y-1)] = 'O'
                    grid[(x,y)] = '.'
                    moved = True
                    moved_at_all = True
    return moved_at_all

    

def roll_east(grid:dict[tuple[int,int],str],max_x:int,max_y:int) -> bool:
    moved_at_all = False
    moved = True
    while moved:
        moved = False
        for x in range(max_x-1,-1,-1):
            for y in range(0,max_y+1):
                if grid[(x,y)] == 'O' and grid[(x+1,y)] == '.':
                    grid[(x+1,y)] = 'O'
                    grid[(x,y)] = '.'
                    moved = True
                    moved_at_all = True
    return moved_at_all

def roll_south(grid:dict[tuple[int,int],str],max_x:int,max_y:int) -> bool:
    moved_at_all = False
    moved = True
    while moved:
        moved = False
        for y in range(max_y-1,-1,-1):
            for x in range(0,max_x+1):
                if grid[(x,y)] == 'O' and grid[(x,y+1)] == '.':
                    grid[(x,y+1)] = 'O'
                    grid[(x,y)] = '.'
                    moved = True
                    moved_at_all = True
    return moved_at_all


def roll_west(grid:dict[tuple[int,int],str],max_x:int,max_y:int) -> bool:
    moved_at_all = False
    moved = True
    while moved:
        moved = False
        for x in range(1,max_x+1):
            for y in range(0,max_y+1):
                if grid[(x,y)] == 'O' and grid[(x-1,y)] == '.':
                    grid[(x-1,y)] = 'O'
                    grid[(x,y)] = '.'
                    moved = True
                    moved_at_all = True
    return moved_at_all

def calc_score(o_coords:list[tuple[int,int]],max_y:int) -> int:
    return sum(max_y-y+1 for x,y in o_coords)


def part_one(data:str):
    result = 0
    grid = {}
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            grid[(x,y)] = char
    # roll round north
    max_y = max(y for x,y in grid.keys())
    max_x = max(x for x,y in grid.keys())
    moved = True
    while moved:
        moved = roll_north(grid,max_x,max_y)
    for y in range(max_y+1):
        for x in range(max_x+1):
            
            print(grid[(x,y)],end='')
        print()


    print(calc_score([(x,y) for x,y in grid.keys() if grid[(x,y)] == 'O'],max_y))



def show_grid(grid:dict[tuple[int,int],str],max_x:int,max_y:int):
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(grid[(x,y)],end='')
        print()

def part_two(data:str,full_cycles:int = 1_000_000_000):
    result = 0
    grid = {}
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            grid[(x,y)] = char
    # roll round north
    max_y = max(y for x,y in grid.keys())
    max_x = max(x for x,y in grid.keys())
    grid_cache:dict[int,list[tuple[int,int]]] = {}
    grid_scores:dict[int,int] = {}

    for cycles in tqdm(range(full_cycles)):
        moved = False

        moved |= roll_north(grid,max_x,max_y)
        moved |= roll_west(grid,max_x,max_y)
        moved |= roll_south(grid,max_x,max_y)
        moved |= roll_east(grid,max_x,max_y)
        grid_cache[cycles] = [(x,y) for x,y in grid.keys() if grid[(x,y)] == 'O']
        grid_scores[cycles] = calc_score(grid_cache[cycles],max_y)
        if cycles > 1:
            for compare_cycle in range(1,cycles-1):
                if compare_cycle == cycles:
                    continue
                if all(grid_cache[compare_cycle][i] == grid_cache[cycles][i] for i in range(len(grid_cache[cycles]))):
                    print('cycle found at',cycles,'and',compare_cycle)
                    # show_grid(grid,max_x,max_y)
                    print()
                    remainder = cycles -compare_cycle
                    search_cycle = full_cycles % remainder
                    print('searching for',compare_cycle+search_cycle, '+-3')
                    for offset in range(-4,3):
                        if compare_cycle+search_cycle+offset in grid_cache:
                            print(offset,calc_score(grid_cache[compare_cycle+search_cycle+offset],max_y))
                    if cycles == 500:
                        for c,score in grid_scores.items():
                            print(f'{c: 4}:{score: 10}')
                        return 


        if not moved:
            print('yay')
            show_grid(grid,max_x,max_y)
            break

    for y in range(max_y+1):
        for x in range(max_x+1):
            if grid[(x,y)] == 'O':
                result += max_y-y+1
            # print(grid[(x,y)],end='')
        # print()
    print(result)

EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

def test_rolls(data:str):
    grid = {}
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            grid[(x,y)] = char
    max_y = max(y for x,y in grid.keys())
    max_x = max(x for x,y in grid.keys())

    print('before')
    show_grid(grid,max_x,max_y)
    print()
    roll_north(grid,max_x,max_y)
    print('after north')
    show_grid(grid,max_x,max_y)
    print()
    roll_west(grid,max_x,max_y)
    print('after west')
    show_grid(grid,max_x,max_y)
    print()
    roll_south(grid,max_x,max_y)
    print('after south')
    show_grid(grid,max_x,max_y)
    print()
    roll_east(grid,max_x,max_y)
    print('after east')
    show_grid(grid,max_x,max_y)
    print()

if __name__ == "__main__":
    input_data = pathlib.Path('23/14_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE

    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
    # test_rolls(input_data)
