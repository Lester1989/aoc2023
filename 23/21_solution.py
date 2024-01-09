"""DAY 21"""
from __future__ import annotations

import pathlib
from enum import Enum
from tqdm import tqdm
import matplotlib.pyplot as plt
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def go_from(self,current_coord:tuple[int,int]) -> tuple[int,int]:
        if self == Direction.NORTH:
            return (current_coord[0],current_coord[1]-1)
        elif self == Direction.EAST:
            return (current_coord[0]+1,current_coord[1])
        elif self == Direction.SOUTH:
            return (current_coord[0],current_coord[1]+1)
        elif self == Direction.WEST:
            return (current_coord[0]-1,current_coord[1])
        else:
            raise ValueError(f'Unknown direction {self}')



def part_one(data:str,steps:int=6):
    result = 0
    grid = {}
    start_pos = None
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            if char == '.':
                grid[(x,y)] = char
            elif char == 'S':
                grid[(x,y)] = '.'
                start_pos = (x,y)

    possible_locations = {start_pos}
    for step in range(steps):
        new_possible_locations = set()
        for location in possible_locations:
            for direction in Direction:
                new_location = direction.go_from(location)
                if new_location in grid:
                    new_possible_locations.add(new_location)
        possible_locations = new_possible_locations
        print('step',step,len(possible_locations))
    print(len(possible_locations))

def part_two(data:str,steps:int=6):
    result = 0
    grid = {}
    start_pos = None
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            if char == '.':
                grid[(x,y)] = char
            elif char == 'S':
                grid[(x,y)] = '.'
                start_pos = (x,y)
    max_x = max(x for x,y in grid)
    max_y = max(y for x,y in grid)
    possible_locations = {start_pos}
    position_history = []
    for _ in tqdm(range(steps)):
        new_possible_locations = set()
        for location in possible_locations:
            for direction in Direction:
                new_x,new_y = direction.go_from(location)
                new_grid_location = (new_x%(max_x+1),new_y%(max_y+1))
                if new_grid_location in grid:
                    new_possible_locations.add((new_x,new_y))
        position_history.append((len(new_possible_locations)/len(possible_locations)))
        possible_locations = new_possible_locations
    print(len(possible_locations))
    plt.plot(position_history)
    plt.show()
    # TODO frequency analysis
    # TODO find repeating pattern
    # TODO predict end result

EXAMPLE = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

if __name__ == "__main__":
    input_data = pathlib.Path('23/21_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data,10)
    print('--- PART TWO ---')
    part_two(input_data,200)
