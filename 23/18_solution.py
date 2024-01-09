"""DAY 18"""
from __future__ import annotations

import pathlib

def go_direction(direction:str,current_coord:tuple[int,int]) -> tuple[int,int]:
    if direction == 'R':
        return (current_coord[0]+1,current_coord[1])
    elif direction == 'L':
        return (current_coord[0]-1,current_coord[1])
    elif direction == 'U':
        return (current_coord[0],current_coord[1]-1)
    elif direction == 'D':
        return (current_coord[0],current_coord[1]+1)

def part_one(data:str):
    current_coord = (0,0)
    outline_coords = {current_coord}
    for line in data.splitlines():
        direction,steps,color = line.split()
        for _ in range(int(steps)):
            current_coord = go_direction(direction,current_coord)
            outline_coords.add(current_coord)
    min_x,max_x,min_y,max_y = bounds(outline_coords)
    print(min_x,max_x,min_y,max_y)
    do_print = input('print? (y/n)') == 'y'
    if do_print:
        show_grid(outline_coords)
    definitly_inside = find_inside(outline_coords)
    fill_inside(outline_coords,definitly_inside,do_print)

def find_inside(outline_coords:list[tuple[int,int]]):
    min_x,max_x,min_y,max_y = bounds(outline_coords)
    border_coord = None
    definitly_inside = None
    while not border_coord:
        for x in range(min_x,max_x+1):
            if (x,min_y) in outline_coords and (x,min_y+1) not in outline_coords:
                border_coord = (x,min_y)
                definitly_inside = (x,min_y+1)
                break
            if (x,max_y) in outline_coords and (x,max_y-1) not in outline_coords:
                border_coord = (x,max_y)
                definitly_inside = (x,max_y-1)
                break
        for y in range(min_y,max_y+1):
            if (min_x,y) in outline_coords and (min_x+1,y) not in outline_coords:
                border_coord = (min_x,y)
                definitly_inside = (min_x+1,y)
                break
            if (max_x,y) in outline_coords and (max_x-1,y) not in outline_coords:
                border_coord = (max_x,y)
                definitly_inside = (max_x-1,y)
                break
    # step into shape
    print('starting from',border_coord)
    print('definitly inside',definitly_inside)
    # show_grid(outline_coords,highlight={border_coord:'X',definitly_inside:'O'})
    return definitly_inside

def fill_inside(outline_coords:list[tuple[int,int]],definitly_inside:tuple[int,int],do_print:bool = False):
    inside_cords = {definitly_inside}
    visited = set()
    # fill
    while inside_cords:
        current_coord = inside_cords.pop()
        visited.add(current_coord)
        for direction in 'RULD':
            new_coord = go_direction(direction,current_coord)
            if new_coord not in outline_coords and new_coord not in visited:
                inside_cords.add(new_coord)
        # show_grid(outline_coords,highlight={coord:'.' for coord in visited}|{border_coord:'X',definitly_inside:'O',current_coord:'*'})
        # input('enter to continue')
    if do_print:
        show_grid(outline_coords,highlight={coord:'.' for coord in visited}|{definitly_inside:'O'})
    print(len(visited)+len(outline_coords))


def bounds(outline_coords:list[tuple[int,int]]):
    min_x = min(x for x,y in outline_coords)
    max_x = max(x for x,y in outline_coords)
    min_y = min(y for x,y in outline_coords)
    max_y = max(y for x,y in outline_coords)
    return min_x,max_x,min_y,max_y


def show_grid(outline_coords:list[tuple[int,int]],empty:str=' ',highlight:dict[tuple[int,int],str] = None):
    min_x,max_x,min_y,max_y = bounds(outline_coords)
    # fill interior
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            if highlight and (x,y) in highlight:
                print(highlight[(x,y)],end='')
            elif (x,y) not in outline_coords:
                print(' ',end='')
            else:
                print('#',end='')
        print()

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

def part_two(data:str):
    current_coord = (0,0)
    corners = [current_coord]
    steps_sum = 0
    for line in data.splitlines():
        _,_,color = line.split()
        # print(color[2:-2])
        steps = int(color[2:-2],16)
        direction = 'RDLU'[int(color[-2])]
        # print(color,'->',direction,steps)
        # direction,steps,color = line.split() # Part ONE
        # steps = int(steps)# Part ONE
        steps_sum += steps
        if direction == 'R':
            current_coord = (current_coord[0]+steps,current_coord[1])
        elif direction == 'L':
            current_coord = (current_coord[0]-steps,current_coord[1])
        elif direction == 'U':
            current_coord = (current_coord[0],current_coord[1]-steps)
        elif direction == 'D':
            current_coord = (current_coord[0],current_coord[1]+steps)
        corners.append(current_coord)
    print(corners)
    min_x,max_x,min_y,max_y = bounds(corners)
    # print(min_x,max_x,min_y,max_y)
    xs,ys = zip(*corners)
    plt.plot(xs,ys)
    plt.show()



EXAMPLE = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/18_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
