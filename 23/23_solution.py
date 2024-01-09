"""DAY 23"""

from __future__ import annotations

import itertools
import pathlib
from dataclasses import dataclass
from enum import Enum

import pkg_resources
has_colorama = "colorama" in [pkg.key for pkg in pkg_resources.working_set]
if has_colorama:
    from colorama import init as colorama_init
    from colorama import Fore
    from colorama import Style

    colorama_init()



class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


    def move(self,coord:tuple[int,int]) -> tuple[int,int]:
        if self == Direction.NORTH:
            return (coord[0],coord[1]-1)
        elif self == Direction.EAST:
            return (coord[0]+1,coord[1])
        elif self == Direction.SOUTH:
            return (coord[0],coord[1]+1)
        elif self == Direction.WEST:
            return (coord[0]-1,coord[1])
        else:
            raise ValueError('Invalid direction')

    def __repr__(self) -> str:
        if self == Direction.NORTH:
            return '^'
        elif self == Direction.EAST:
            return '>'
        elif self == Direction.SOUTH:
            return 'v'
        elif self == Direction.WEST:
            return '<'
        else:
            raise ValueError('Invalid direction')

    def __str__(self) -> str:
        if self == Direction.NORTH:
            return '^'
        elif self == Direction.EAST:
            return '>'
        elif self == Direction.SOUTH:
            return 'v'
        elif self == Direction.WEST:
            return '<'
        else:
            raise ValueError('Invalid direction')


    
@dataclass
class Crossroads:
    coord:tuple[int,int]
    neighbours:dict[tuple[int,int],int]
    neighbour_paths:dict[tuple[int,int],list[tuple[int,int]]] = None

    def __repr__(self) -> str:
        return f'{self.coord} -> {len(self.neighbours)} neighours: {self.neighbours}'

def show_path(start:tuple[int,int],path:list[tuple[int,int]],grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    if has_colorama:
        return show_path_colored(start,path,grid,max_x,max_y)
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) == start:
                print('S',end='  ')
            elif (x,y) in path:
                print('O',end=' ')
            elif (x,y) in grid:
                print(grid[(x,y)],end='  ')
            else:
                print(' ',end='  ')
        print()

def show_path_colored(start:tuple[int,int],path:list[tuple[int,int]],grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) == start:
                print(f'{Fore.GREEN}S', end=' ')
            elif (x,y) in path:
                print(f'{Fore.RED}O', end=' ')
            elif (x,y) in grid:
                print(Fore.WHITE + str(grid[(x,y)]),end=' ')
            else:
                print(end=' ')
        print(Style.RESET_ALL)

def reconstruct_path(crossroads_graph:dict[tuple[int,int],Crossroads] ,used_crossroads:list[tuple[int,int]]):
    path = []
    for i in range(len(used_crossroads)-1):
        path.extend(crossroads_graph[used_crossroads[i]].neighbour_paths[used_crossroads[i+1]])
    return path

def read_map(data:str):
    grid = {}
    max_y = len(data.splitlines())-1
    max_x = len(data.splitlines()[0])-1
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            grid[(x,y)] = char
    return grid,max_y,max_x

def part_one(data:str):
    result = 0
    grid,max_y,max_x = read_map(data)
    start = next((x,0) for x in range(max_x) if grid[(x,0)] == '.')
    end = next((x,max_y) for x in range(max_x) if grid[(x,max_y)] == '.')
    print(start,end)
    for path in find_paths(grid,start,end):
        # print('\n\n')
        # show_path(start,path,grid,max_x,max_y)
        print(len(path)-1)
        result = max(result,len(path)-1)
    print(result)

def find_paths(grid:dict[tuple[int,int],str],start:tuple[int,int],end:tuple[int,int]):
    paths = [[start]]
    while paths:
        path = paths.pop(0)
        current = path[-1]
        if current == end:
            yield path
        else:
            for direction in Direction:
                new_coord = direction.move(current)
                if new_coord in grid and grid[new_coord] in ['.', str(direction)] and new_coord not in path:
                    paths.append(path+[new_coord])


    
def get_path_length(path:list[tuple[int,int]],crossroad_graph:dict[tuple[int,int],Crossroads]):
    return sum(
        crossroad_graph[path[i]].neighbours[path[i + 1]]
        for i in range(len(path) - 1)
    )+len(path)-1

def find_crossroads(grid:dict[tuple[int,int],str],max_x:int,max_y:int):
    crossroads:set[tuple[int,int]] = set()
    for y, x in itertools.product(range(max_y), range(max_x)):
        if grid[(x,y)] == '#':
            continue
        connected_roads = 0
        for direction in Direction:
            new_coord = direction.move((x,y))
            if new_coord in grid and grid[new_coord] != '#':
                connected_roads += 1
        if connected_roads > 2:
            crossroads.add((x,y))
    print(f'found {len(crossroads)} crossroads: {sorted(crossroads)}')
    return crossroads


def construct_crossroads_graph(grid:dict[tuple[int,int],str],crossroads:set[tuple[int,int]]):
    crossroad_graph:dict[tuple[int,int],Crossroads] = {}
    for current_crossroad in crossroads:
        crossroad_graph[current_crossroad] = Crossroads(current_crossroad,{},{})
        paths = []
        for direction in Direction:
            new_coord = direction.move(current_crossroad)
            if new_coord in grid and grid[new_coord] != '#':
                paths.append([new_coord])
        while paths:
            path = paths.pop(0)
            current = path[-1]
            if current in crossroads:
                if current not in crossroad_graph:
                    crossroad_graph[current] = Crossroads(current,{current_crossroad,len(path)-1},{current_crossroad,current})
                crossroad_graph[current_crossroad].neighbours[current] = len(path)-1
                crossroad_graph[current_crossroad].neighbour_paths[current] = path
            else:
                for direction in Direction:
                    new_coord = direction.move(current)
                    if new_coord in grid and grid[new_coord] != '#' and new_coord not in path and new_coord != current_crossroad:
                        paths.append(path+[new_coord])
    for value in crossroad_graph.values():
        print(value)
    return crossroad_graph


def part_two(data:str):
    result = 0
    grid,max_y,max_x = read_map(data)
    start = next((x,0) for x in range(max_x) if grid[(x,0)] == '.')
    end = next((x,max_y) for x in range(max_x) if grid[(x,max_y)] == '.')
    print(start,end)
    crossroads:set[tuple[int,int]] = find_crossroads(grid,max_x,max_y)
    crossroads.add(start)
    crossroads.add(end)
    crossroads_graph = construct_crossroads_graph(grid,crossroads)
    for i,path in enumerate(find_paths_ignore_slopes(crossroads_graph,start,end)):
        # show_path(start,reconstruct_path(crossroads_graph,path),grid,max_x,max_y)
        if len(path) > len(crossroads)-4:
            length = get_path_length(path,crossroads_graph)
            if length > result:
                print('new max')
                print(f'crossroads: {len(path)-1} length: {length} ->  path: {path}')

            result = max(result,length)
        elif i % 1000 == 0:
            print(f'{i: <10}: crossroads: {len(path)}')
    print(result)
    
def find_paths_ignore_slopes(crossroad_graph:dict[tuple[int,int],Crossroads] ,start:tuple[int,int],end:tuple[int,int]):
    paths = [[start]]
    while paths:
        path = paths.pop(0)
        current = path[-1]
        if current == end:
            yield path
        else:
            for next_crossroad in crossroad_graph[current].neighbours:
                if next_crossroad not in path:
                    paths.append(path+[next_crossroad])


EXAMPLE = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/23_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
