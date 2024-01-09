"""DAY 17"""
from __future__ import annotations

import pathlib
from enum import Enum
from dataclasses import dataclass
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

    def turn_left(self) -> Direction:
        if self == Direction.NORTH:
            return Direction.WEST
        elif self == Direction.WEST:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.NORTH
        else:
            raise ValueError('Invalid direction')

    def turn_right(self) -> Direction:
        if self == Direction.NORTH:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.WEST
        elif self == Direction.WEST:
            return Direction.NORTH
        else:
            raise ValueError('Invalid direction')

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
class Crucible:
    position:tuple[int,int]
    direction:Direction
    path:list[tuple[int,int]]
    directions: list[Direction]
    start_direction:Direction
    start_position:tuple[int,int]
    direction_length:int =0

    def __init__(self,position:tuple[int,int],direction:Direction):
        self.position = position
        self.direction = direction
        self.path = [position]
        self.directions = [direction]
        self.direction_length = 0
        self.start_direction = direction
        self.start_position = position

    def copy(self) -> Crucible:
        new_crucible = Crucible(self.position,self.direction)
        new_crucible.path = self.path.copy()
        new_crucible.direction_length = self.direction_length
        new_crucible.start_direction = self.start_direction
        new_crucible.start_position = self.start_position
        return new_crucible

    def heat_loss(self,grid:dict[tuple[int,int]]) -> int:
        return sum(grid[coord] for coord in self.path)

    def copy_move_forward(self) -> None:
        moving_copy = self.copy()
        moving_copy.position = self.direction.move(self.position)
        moving_copy.direction_length += 1
        moving_copy.path.append(self.position)
        moving_copy.directions.append(self.direction)
        return moving_copy

    def copy_turn_left(self) -> None:
        moving_copy = self.copy()
        moving_copy.direction = self.direction.turn_left()
        moving_copy.direction_length = 0
        moving_copy.position = self.direction.move(self.position)
        moving_copy.direction_length += 1
        moving_copy.path.append(self.position)
        moving_copy.directions.append(self.direction)
        return moving_copy

    def copy_turn_right(self) -> None:
        moving_copy = self.copy()
        moving_copy.direction = self.direction.turn_right()
        moving_copy.direction_length = 0
        moving_copy.position = self.direction.move(self.position)
        moving_copy.direction_length += 1
        moving_copy.path.append(self.position)
        moving_copy.directions.append(self.direction)
        return moving_copy

    def can_move_forward(self,grid:dict[tuple[int,int],int],minimal_heat_loss:int) -> bool:
        test_pos = self.direction.move(self.position)
        return self.direction_length<3 and  test_pos in grid and test_pos not in self.path and self.heat_loss(grid)+grid[test_pos] < minimal_heat_loss

    def can_turn_left(self,grid:dict[tuple[int,int],int],minimal_heat_loss:int) -> bool:
        test_pos = self.direction.turn_left().move(self.position)
        return self.direction_length<3 and test_pos in grid and test_pos not in self.path and self.heat_loss(grid)+grid[test_pos] < minimal_heat_loss

    def can_turn_right(self,grid:dict[tuple[int,int],int],minimal_heat_loss:int) -> bool:
        test_pos = self.direction.turn_right().move(self.position)
        return self.direction_length<3 and test_pos in grid and test_pos not in self.path and self.heat_loss(grid)+grid[test_pos] < minimal_heat_loss


def read_map(data:str):
    grid = {}
    max_y = len(data.splitlines())-1
    max_x = len(data.splitlines()[0])-1
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            grid[(x,y)] = int(char)
    return grid,max_y,max_x



def directions_from(heat_loss_map:dict[tuple[int,int],tuple[list[Direction],int]],grid:dict[tuple[int,int],int],position:tuple[int,int]) -> list[Direction]:
    possible_directions:list[Direction] = []
    directions,current_heat_loss= heat_loss_map[position]
    must_turn = len(directions) > 2 and directions[-1] == directions[-2] == directions[-3]
    if not must_turn:
        forward_coord = directions[-1].move(position)
        if forward_coord in grid:
            possible_directions.append(directions[-1])
    left_coord = directions[-1].turn_left().move(position)
    if left_coord in grid:
        possible_directions.append(directions[-1].turn_left())
    right_coord = directions[-1].turn_right().move(position)
    if right_coord in grid:
        possible_directions.append(directions[-1].turn_right())
    return possible_directions

def find_direct_path(grid:dict[tuple[int,int],int],max_y:int,max_x:int) -> int:
    target_pos = (max_x,max_y)
    direct_crucible_south = Crucible((0,0),Direction.SOUTH)
    while direct_crucible_south.position != target_pos:
        if direct_crucible_south.direction == Direction.EAST:
            direct_crucible_south = direct_crucible_south.copy_turn_right()
        elif direct_crucible_south.direction == Direction.SOUTH:
            direct_crucible_south = direct_crucible_south.copy_turn_left()
    direct_crucible_east = Crucible((0,0),Direction.EAST)
    while direct_crucible_east.position != target_pos:
        if direct_crucible_east.direction == Direction.EAST:
            direct_crucible_east = direct_crucible_east.copy_turn_right()
        elif direct_crucible_east.direction == Direction.SOUTH:
            direct_crucible_east = direct_crucible_east.copy_turn_left()
        
        # show_cruicible_colored(direct_crucible,grid,max_x,max_y)
    heat_loss = min(direct_crucible_south.heat_loss(grid),direct_crucible_east.heat_loss(grid))
    print('direct path heat loss',heat_loss)
    input('press enter to continue')
    return heat_loss


def part_one(data:str):
    result = 0
    grid,max_y,max_x = read_map(data)
    target = (max_x,max_y)
    full_paths = []
    paths = [Crucible((0,0),Direction.EAST),Crucible((0,0),Direction.SOUTH)]
    minimal_heat_loss = find_direct_path(grid,max_y,max_x)
    while paths:
        if full_paths:
            # next_idx = explore_paths(grid,max_y,max_x,paths)
            # next_idx = select_longest(paths)
            next_idx = select_minimal_heat_loss(paths,grid)
        else:
            next_idx = len(paths)-1
        if next_idx == -1:
            print('exit')
            return
        crucible = paths.pop(next_idx)
        print(len(paths)+1,'paths;',len(full_paths),'full paths;',minimal_heat_loss,'minimal heat loss','exploring path of length',len(crucible.path),'; heat loss',crucible.heat_loss(grid))
        target_distance = abs(target[0]-crucible.position[0])+abs(target[1]-crucible.position[1])
        if crucible.heat_loss(grid)+target_distance-2 > minimal_heat_loss:
            # print('early exit',crucible.heat_loss(grid))
            # print(len(paths),'paths;',len(full_paths),'full paths;',minimal_heat_loss,'minimal heat loss')
            # print('minimal heat loss',minimal_heat_loss)
            continue
        if crucible.position == target:
            print('found path',crucible.heat_loss(grid))
            minimal_heat_loss = min(minimal_heat_loss,crucible.heat_loss(grid))
            print('minimal heat loss',minimal_heat_loss)
            print(len(paths),'paths;',len(full_paths),'full paths;',minimal_heat_loss,'minimal heat loss')
            full_paths.append(crucible)
        else:
            moved = False
            if crucible.can_move_forward(grid,minimal_heat_loss):
                moved = True
                # print('moving forward')
                paths.append(crucible.copy_move_forward())
            if crucible.can_turn_left(grid,minimal_heat_loss):
                moved = True
                # print('turning left')
                paths.append(crucible.copy_turn_left())
            if crucible.can_turn_right(grid,minimal_heat_loss):
                moved = True
                # print('turning right')
                paths.append(crucible.copy_turn_right())
            # if not moved:
            #     print('dead end')
    print('found paths',len(full_paths))
    print('minimal heat loss',minimal_heat_loss)
    explore_paths(grid,max_y,max_x,full_paths)

def select_longest(paths:list[Crucible]):
    next_idx = 0
    best_val = 0
    for idx,cruicible in enumerate(paths):
        if len(cruicible.path) > best_val:
            best_val = len(cruicible.path)
            next_idx = idx
    return next_idx

def select_minimal_heat_loss(paths:list[Crucible],grid:dict[tuple[int,int],int]) -> int:
    next_idx = 0
    best_val = 1_000_000_000
    for idx,cruicible in enumerate(paths):
        if cruicible.heat_loss(grid) < best_val:
            best_val = cruicible.heat_loss(grid)
            next_idx = idx
    return next_idx


def map_exploration(grid:dict[tuple[int,int],int],max_y:int,max_x:int) -> None:
    heat_loss_map:dict[tuple[int,int],tuple[list[Direction],int]] = {
        Direction.EAST.move((0,0)):([Direction.EAST],grid[Direction.EAST.move((0,0))]),
        Direction.SOUTH.move((0,0)):([Direction.SOUTH],grid[Direction.SOUTH.move((0,0))])
    }
    while (max_x-1,max_y-1) not in heat_loss_map:
        for position in list(heat_loss_map.keys()):
            directions,current_heat_loss = heat_loss_map[position]
            possible_directions = directions_from(heat_loss_map,grid,position)
            for direction in possible_directions:
                new_position = direction.move(position)
                new_heat_loss = current_heat_loss + grid[new_position]
                if new_position in heat_loss_map:
                    existing_directions,existing_heat_loss = heat_loss_map[new_position]
                    if new_heat_loss < existing_heat_loss:
                        heat_loss_map[new_position] = (directions + [direction],new_heat_loss)
                else:
                    heat_loss_map[new_position] = (directions + [direction],new_heat_loss)
        # show_grid({key:heat_loss for key,(_,heat_loss) in heat_loss_map.items()},max_x,max_y)
        # input()
    show_path((0,0),heat_loss_map[(max_x-1,max_y-1)][0],grid,max_x,max_y)
    print(heat_loss_map[(max_x-1,max_y-1)][1])
    command = ''
    while command != 'q':
        print('q: quit, \np,x,y: show path to x,y')
        command = input('enter command: ')
        if command == 'q':
            break
        elif command.startswith('p'):
            x,y = command[2:].split(',')
            show_path((0,0),heat_loss_map[(int(x),int(y))][0],grid,max_x,max_y)
            print(heat_loss_map[(int(x),int(y))][1])

def explore_paths(grid:dict[tuple[int,int],int],max_y:int,max_x:int,cruicibles:list[Crucible]) -> int:
    command = ''
    try:
        while command != 'q':
            # for idx,cruicible in enumerate(cruicibles):
            #     print(idx,':',len(cruicible.path),'steps; loss:',cruicible.heat_loss(grid))
            print('q: quit, \np,idx: show path to x,y\nl: list cruicibles\nc continue')
            command = input('enter command: ')
            if command == 'q':
                return -1
            elif command.startswith('l'):
                for idx,cruicible in enumerate(cruicibles):
                    print(idx,':',len(cruicible.path),'steps; loss:',cruicible.heat_loss(grid))
            elif command.startswith('p'):
                idx = int(command[2:])
                show_cruicible(cruicibles[idx],grid,max_x,max_y)
            elif command.startswith('s'):
                idx = int(command[2:])
                print('expanding cruicible',idx)
                return idx
            else:
                idx = 0
                longest = 0
                for cruicible in cruicibles:
                    if len(cruicible.path) > longest:
                        longest = len(cruicible.path)
                        idx = cruicibles.index(cruicible)
                return idx 
    except Exception as e:
        print(e)
        return 0



def show_grid(grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(grid.get((x,y),' '),end=' ')
        print()
    
def show_path(start:tuple[int,int],directions:list[Direction],grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    if has_colorama:
        return show_path_colored(start,directions,grid,max_x,max_y)
    direction_coords = {start:directions[0]}
    current_coord = start
    for direction in directions:
        current_coord = direction.move(current_coord)
        direction_coords[current_coord] = direction
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) == start:
                print('S',end='  ')
            elif (x,y) in direction_coords:
                print(direction_coords[(x,y)],end=' ')
            elif (x,y) in grid:
                print(grid[(x,y)],end='  ')
            else:
                print(' ',end='  ')
        print()

def show_cruicible(cruicible:Crucible,grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    print(cruicible.direction,cruicible.position,cruicible.direction_length,cruicible.heat_loss(grid))
    if has_colorama:
        return show_cruicible_colored(cruicible,grid,max_x,max_y)
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) == cruicible.start_position:
                print(' S',end='  ')
            elif (x,y) in cruicible.path:
                print(f'({grid[(x,y)]})',end='')
            elif (x,y) in grid:
                print(f' {grid[(x,y)]}',end='  ')
            else:
                print(' ',end='  ')
        print()

def show_cruicible_colored(cruicible:Crucible,grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) == cruicible.start_position:
                print(f'{Fore.GREEN} S', end='  ')
            elif (x,y) in cruicible.path:
                print(f'{Fore.RED}({Fore.WHITE}{grid[x, y]}{Fore.RED})', end=' ')
            elif (x,y) in grid:
                print(f'{Fore.WHITE} {grid[x, y]}', end='  ')
            else:
                print(' ',end='  ')
        print(Style.RESET_ALL)

def show_path_colored(start:tuple[int,int],directions:list[Direction],grid:dict[tuple[int,int],int],max_x:int,max_y:int):
    direction_coords = {start:directions[0]}
    current_coord = start
    for direction in directions:
        current_coord = direction.move(current_coord)
        direction_coords[current_coord] = direction
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) == start:
                print(Fore.GREEN + 'S',end='  ')
            elif (x,y) in direction_coords:
                print(Fore.WHITE +str(grid[(x,y)])+Fore.RED + str(direction_coords[(x,y)]),end=' ')
            elif (x,y) in grid:
                print(Fore.WHITE + str(grid[(x,y)]),end='  ')
            else:
                print(' ',end='  ')
        print(Style.RESET_ALL)


def part_two(data:str):
    result = 0
    for line in data.splitlines():
        print(line)
    print(result)

EXAMPLE = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/17_data.txt').read_text(encoding='utf-8')
    input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    # part_two(input_data)
