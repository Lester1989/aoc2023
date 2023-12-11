"""DAY 11"""
from __future__ import annotations

import pathlib


def show_grid(grid:dict[tuple[int,int],str],empty:str=' '):
    min_x = min(x for x,y in grid)
    max_x = max(x for x,y in grid)
    min_y = min(y for x,y in grid)
    max_y = max(y for x,y in grid)
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(grid.get((x,y),empty),end='')
        print()

def part_one(data:str):
    result = 0
    grid :dict[tuple[int,int],str] = {}
    y = 0
    for line in data.splitlines():
        for x,char in enumerate(line):
            if char == '#':
                grid[(x,y)] = char
        y += 1
        # expand empty rows
        if '#' not in line:
            y += 1
            for x,char in enumerate(line):
                if char == '#':
                    grid[(x,y)] = char
    max_x = max(x for x,_ in grid)
    empty_columns = {
        x
        for x in range(max_x)
        if all((x, y)  not in grid for y in range(max(y for _,y in grid)+1))
    }
    print(sorted(empty_columns))
    # expand empty columns
    expanded_grid = {}
    for x,y in list(grid.keys()):
        moved_by_empty_columns = len([empty_x for empty_x in empty_columns if empty_x < x])
        # print(x,y,'->',(x+moved_by_empty_columns,y), moved_by_empty_columns)
        expanded_grid[(x+moved_by_empty_columns,y)] = '#'
    # show_grid(expanded_grid,'.')
    pairs = set()
    for start_coord in expanded_grid:
        for end_coord in expanded_grid:
            if start_coord != end_coord:
                pairs.add(tuple(sorted([start_coord,end_coord])))
    # print(len(pairs))
    for a,b in sorted(pairs):
        manhattan_distance = abs(a[0]-b[0])+abs(a[1]-b[1])
        # print(a,b,'->',manhattan_distance)
        result += manhattan_distance
    print(result)


def part_two(data:str,expansion:int=10):
    result = 0
    grid :dict[tuple[int,int],str] = {}
    empty_rows = set()
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            if char == '#':
                grid[(x,y)] = char
        if '#' not in line:
            empty_rows.add(y)
    
    max_x = max(x for x,_ in grid)
    empty_columns = {
        x
        for x in range(max_x)
        if all((x, y)  not in grid for y in range(max(y for _,y in grid)+1))
    }
    print('empty cols',sorted(empty_columns))
    print('empty rows',sorted(empty_rows))
    pairs = set()
    for start_coord in grid:
        for end_coord in grid:
            if start_coord != end_coord:
                pairs.add(tuple(sorted([start_coord,end_coord])))
    for a,b in sorted(pairs):
        crossed_empty_rows = [
            empty_row
            for empty_row in empty_rows
            if min(a[1],b[1]) < empty_row < max(a[1],b[1])
        ]
        crossed_empty_columns = [
            empty_column
            for empty_column in empty_columns
            if a[0] < empty_column < b[0]
        ]
        manhattan_distance = abs(a[0]-b[0])+abs(a[1]-b[1])
        if crossed_empty_rows:
            manhattan_distance += (expansion-1)*len(crossed_empty_rows)
            # print('crossed empty rows',crossed_empty_rows,'->',manhattan_distance)
        if crossed_empty_columns:
            manhattan_distance += (expansion-1)*len(crossed_empty_columns)
            # print('crossed empty columns',crossed_empty_columns,'->',manhattan_distance)
        # print(a,b,'->',manhattan_distance, ('rows',crossed_empty_rows),('cols',crossed_empty_columns))
        result += manhattan_distance

    # print('cols',empty_columns)
    # print('rows',empty_rows)
    print(result)

EXAMPLE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

if __name__ == "__main__":
    input_data = pathlib.Path('23/11_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data,1_000_000)
