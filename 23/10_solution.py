"""DAY 10"""
from __future__ import annotations

import pathlib
from enum import Enum

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
        
    def back(self) -> Direction:
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.EAST:
            return Direction.WEST
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.WEST:
            return Direction.EAST
        else:
            raise ValueError(f'Unknown direction {self}')


'''
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
'''

pipe_directions:dict[str,list[Direction]] = {
    '|': [Direction.NORTH, Direction.SOUTH],
    '-': [Direction.EAST, Direction.WEST],
    'L': [Direction.NORTH, Direction.EAST],
    'J': [Direction.NORTH, Direction.WEST],
    '7': [Direction.SOUTH, Direction.WEST],
    'F': [Direction.SOUTH, Direction.EAST],
    'S': [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
    '.': []
}

def show_grid(grid:dict[tuple[int,int],str]):
    min_x = min(x for x,y in grid)
    max_x = max(x for x,y in grid)
    min_y = min(y for x,y in grid)
    max_y = max(y for x,y in grid)
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(grid.get((x,y),' '),end='')
        print()


def step(grid:dict[tuple[int,int],str],current_coord:tuple[int,int],current_direction:Direction,verbose:bool = False) -> tuple[tuple[int,int],Direction]:
    if verbose:
        print(f'have reached {grid[current_coord]} ({current_coord}) from {current_direction}')
    possible_directions = [
        direction
        for direction in Direction
        if direction in pipe_directions[grid[current_coord]] and direction != current_direction.back()
    ]
    if verbose:
        print('possible directions',possible_directions)
    if len(possible_directions) == 1:
        return (possible_directions[0].go_from(current_coord),possible_directions[0])
    elif len(possible_directions) == 2:
        raise ValueError('there should be only 2-way pipes',possible_directions)


def part_one(data:str,verbose:bool=False):
    result = 0
    grid :dict[tuple[int,int],str] = {}
    start_coord:tuple[int,int]|None = None
    for y,line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[(x,y)] = char
            if char == 'S':
                start_coord = (x,y)
    distance_grid :dict[tuple[int,int],int] = {
        start_coord: 0
    }
    print('starting from',start_coord)
    possible_directions = (
        direction
        for direction in Direction
        if direction.back() in pipe_directions[grid.get(direction.go_from(start_coord),'.')]
    )
    forward,backward = possible_directions
    forward_coord = forward.go_from(start_coord)
    backward_coord = backward.go_from(start_coord)
    if verbose:
        print(forward_coord,backward_coord)
        show_grid(grid)
    for steps in range(len(grid)):
        if forward_coord in distance_grid or backward_coord in distance_grid:
            result = steps
            break
        distance_grid[forward_coord] = steps+1
        distance_grid[backward_coord] = steps+1
        forward_coord,forward = step(grid,forward_coord,forward,verbose)
        backward_coord,backward = step(grid,backward_coord,backward,verbose)
        if verbose:
            show_grid(distance_grid)
            print()

    print(result)

def part_two(data:str,verbose:bool=False):
    grid :dict[tuple[int,int],str] = {}
    start_coord:tuple[int,int]|None = None
    dot_coords:set[tuple[int,int]] = set()
    for y,line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[(x,y)] = char
            if char == 'S':
                start_coord = (x,y)
            elif char == '.':
                dot_coords.add((x,y))
    distance_grid :dict[tuple[int,int],int] = {
        start_coord: 0
    }
    print('starting from',start_coord, 'with',len(dot_coords),'dots')
    possible_directions = (
        direction
        for direction in Direction
        if direction.back() in pipe_directions[grid.get(direction.go_from(start_coord),'.')]
    )
    forward,backward = possible_directions
    forward_coord = forward.go_from(start_coord)
    backward_coord = backward.go_from(start_coord)
    if verbose:
        print(forward_coord,backward_coord)
        show_grid(grid)
    for steps in range(len(grid)):
        if forward_coord in distance_grid or backward_coord in distance_grid:
            break
        distance_grid[forward_coord] = steps+1
        distance_grid[backward_coord] = steps+1
        forward_coord,forward = step(grid,forward_coord,forward,verbose)
        backward_coord,backward = step(grid,backward_coord,backward,verbose)
        if verbose:
            show_grid(distance_grid)
            print()
    for coord in grid:
        if coord not in distance_grid:
            grid[coord] = '.'
            dot_coords.add(coord)
    if verbose:
        show_grid(grid)
    # enlarge grid to see gaps between pipes
    min_x = min(x for x,y in grid)
    max_x = max(x for x,y in grid)
    min_y = min(y for x,y in grid)
    max_y = max(y for x,y in grid)
    large_grid :dict[tuple[int,int],tuple[str,tuple[int,int],str]] = {
        (x,y):(None,None,' ')
        for x in range(min_x*2,max_x*2+1)
        for y in range(min_y*2,max_y*2+1)
    }
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            large_coord = (x*2,y*2)
            grid_content = grid.get((x,y),'.')
            large_grid[large_coord] = (grid_content,(x,y),'#' if grid_content != '.' else '.')
            for direction in pipe_directions[grid.get((x,y),'.')]:
                large_grid[direction.go_from(large_coord)] = (None,None,'+')
    printable_large_grid = {
        coord:data[2]
        for coord,data in large_grid.items()
    }
    if verbose:
        show_grid(printable_large_grid)
    groups = []
    while dot_coords:
        current_group = [dot_coords.pop()]
        # explore until no more
        for coord,data in large_grid.items():
            if data[1] == current_group[0]:
                large_coord = coord
                break
        visited = {large_coord}
        unvisited = {
            direction.go_from(large_coord)
            for direction in Direction
            if large_grid.get(direction.go_from(large_coord),(None,None,None))[2] in ('.',' ')
        }
        while unvisited:
            large_coord = unvisited.pop()
            visited.add(large_coord)
            if large_grid[large_coord][2] == '.':
                current_group.append(large_grid[large_coord][1])
                dot_coords.remove(large_grid[large_coord][1])
            for direction in Direction:
                new_coord = direction.go_from(large_coord)
                if new_coord not in visited and large_grid.get(new_coord,(None,None,None))[2] in ('.',' '):
                    unvisited.add(new_coord)
        groups.append(current_group)
    group_grid :dict[tuple[int,int],int] = {}
    for idx,group in enumerate( groups):
        if any(coord[0] in (0,max_x) or coord[1] in (0,max_y)  for coord in group):
            print(f'Group {idx+1}: {len(group)}')
            print('  outside')
        else:
            print(f'-->Group {idx+1}: {len(group)} <--')
        if verbose:
            for coord in group:
                group_grid[coord] = idx+1
    if verbose:
        show_grid(group_grid)


EXAMPLE = """.....
.S-7.
.|.|.
.L-J.
....."""

EXAMPLE_CLUTTERED = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

EXAMPLE_COMPLEX_CLUTTERED = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

EXAMPLE_ECNLOSEMENT ="""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""

EXAMPLE_COMPLEX_ECNLOSEMENT ="""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/10_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE_ECNLOSEMENT
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
