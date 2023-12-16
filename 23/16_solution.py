"""DAY 16"""
from __future__ import annotations

import pathlib
from enum import Enum
from dataclasses import dataclass
from tqdm import tqdm
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def move(self,position:tuple[int,int]) -> tuple[int,int]:
        x,y = position
        if self == Direction.UP:
            return (x,y-1)
        elif self == Direction.RIGHT:
            return (x+1,y)
        elif self == Direction.DOWN:
            return (x,y+1)
        elif self == Direction.LEFT:
            return (x-1,y)

    def turn_left(self) -> Direction:
        return Direction((self.value-1)%4)

    def turn_right(self) -> Direction:
        return Direction((self.value+1)%4)

@dataclass
class Beam:
    position:tuple[int,int]
    direction:Direction

    finished:bool = False
    finished_at:tuple[int,int] = None
    finished_direction:Direction = None
    start_position:tuple[int,int] = None
    start_direction:Direction = None
    energized_tiles:set[tuple[int,int]] = None

    def __init__(self,position:tuple[int,int],direction:Direction) -> None:
        self.position = position
        self.direction = direction
        self.start_position = position
        self.start_direction = direction
        self.energized_tiles = {position}

    @property
    def id(self) -> tuple[int,int,Direction]:
        return (*self.start_position,self.start_direction)

    def __eq__(self, __value: object) -> bool:
        return False if not isinstance(__value,Beam) else self.id == __value.id

    def __hash__(self) -> int:
        return hash(self.id)

    def next_pos (self) -> tuple[int,int]:
        return self.direction.move(self.position)

    def step_on(self,postion:tuple[int,int],tile_content:str) -> None:
        self.position = postion
        self.energized_tiles.add(postion)
        if tile_content == '/':
            if self.direction in (Direction.UP,Direction.DOWN):
                # print('turning right')
                self.direction = self.direction.turn_right()
            elif self.direction in (Direction.LEFT,Direction.RIGHT):
                # print('turning left')
                self.direction = self.direction.turn_left()
        elif tile_content == '\\':
            if self.direction in (Direction.UP,Direction.DOWN):
                # print('turning left')
                self.direction = self.direction.turn_left()
            elif self.direction in (Direction.LEFT,Direction.RIGHT):
                # print('turning right')
                self.direction = self.direction.turn_right()

    def finish(self) -> None:
        self.finished = True
        self.finished_at = self.position
        self.finished_direction = self.direction

    def split(self,postion:tuple[int,int],tile_content:str) -> list[Beam]:
        self.position = postion
        self.energized_tiles.add(postion)
        if tile_content == '|' and self.direction in (Direction.LEFT,Direction.RIGHT):
            self.finished = True
            self.finished_at = self.position
            self.finished_direction = self.direction
            # print('splitting up/down')
            return [Beam(self.position,Direction.UP),Beam(self.position,Direction.DOWN)]
        elif tile_content == '-' and self.direction in (Direction.UP,Direction.DOWN):
            self.finished = True
            self.finished_at = self.position
            self.finished_direction = self.direction
            # print('splitting left/right')
            return [Beam(self.position,Direction.LEFT),Beam(self.position,Direction.RIGHT)]

def part_one(data:str):
    grid, max_y, max_x = read_map(data)

    beams = [Beam((0,0),Direction.DOWN) ]
    energized_tiles = {(0,0)}
    beam_starts:set[tuple[int,int,Direction]] = {(*beams[0].position,beams[0].direction)}
    while beams:
        current_beam = beams.pop()

        next_pos = current_beam.direction.move(current_beam.position)
        print(current_beam.position,'-',current_beam.direction,'>',next_pos)
        if 0<=next_pos[0]<max_x and 0<=next_pos[1]<max_y:
            energized_tiles.add(next_pos)
        else:
            print('out of bounds')
            continue
        if next_pos in grid:
            if grid[next_pos] == '/' and current_beam.direction in (Direction.UP,Direction.DOWN):
                print('turning right')
                current_beam.direction = current_beam.direction.turn_right()
            elif grid[next_pos] == '/' and current_beam.direction in (Direction.LEFT,Direction.RIGHT):
                print('turning left')
                current_beam.direction = current_beam.direction.turn_left()
            elif grid[next_pos] == '\\' and current_beam.direction in (Direction.UP,Direction.DOWN):
                print('turning left')
                current_beam.direction = current_beam.direction.turn_left()
            elif grid[next_pos] == '\\' and current_beam.direction in (Direction.LEFT,Direction.RIGHT):
                print('turning right')
                current_beam.direction = current_beam.direction.turn_right()
            elif grid[next_pos] == '|' and current_beam.direction in (Direction.LEFT,Direction.RIGHT):
                print('splitting up/down')
                if (*next_pos,Direction.UP) not in beam_starts:
                    beams.append(Beam(next_pos,Direction.UP))
                    beam_starts.add((*next_pos,Direction.UP))
                if (*next_pos,Direction.DOWN) not in beam_starts:
                    beams.append(Beam(next_pos,Direction.DOWN))
                    beam_starts.add((*next_pos,Direction.DOWN))
                continue
            elif grid[next_pos] == '-' and current_beam.direction in (Direction.UP,Direction.DOWN):
                print('splitting left/right')
                if (*next_pos,Direction.LEFT) not in beam_starts:
                    beams.append(Beam(next_pos,Direction.LEFT))
                    beam_starts.add((*next_pos,Direction.LEFT))
                if (*next_pos,Direction.RIGHT) not in beam_starts:
                    beams.append(Beam(next_pos,Direction.RIGHT))
                    beam_starts.add((*next_pos,Direction.RIGHT))
                continue
        current_beam.position = next_pos
        beams.append(current_beam)
        # show_energy(grid,max_x,max_y,energized_tiles)
        # print(f'\n====={len(beams)}===\n')
        # input()

    print(len(energized_tiles))

def show_energized(grid:dict[tuple[int,int],str],max_x:int,max_y:int,energized_tiles:set[tuple[int,int]]):
    for y in range(max_y):
        for x in range(max_x):
            if (x,y) in energized_tiles:
                print('#',end='')
            elif (x,y) in grid:
                print(grid[(x,y)],end='')
            else:
                print('.',end='')
        print()

def read_map(data:str):
    grid = {}
    max_y = len(data.splitlines())
    max_x = len(data.splitlines()[0])
    for y,line in enumerate(data.splitlines()):
        for x,char in enumerate(line):
            if char != '.':
                grid[(x,y)] = char
    return grid,max_y,max_x

def part_two(data:str):
    grid, max_y, max_x = read_map(data)
    starting_beams = [
        Beam((0,y),Direction.RIGHT)
        for y in range(max_y)
    ]
    starting_beams.extend([
        Beam((x,0),Direction.DOWN)
        for x in range(max_x)
    ])
    starting_beams.extend([
        Beam((max_x,y),Direction.LEFT)
        for y in range(max_y)
    ])
    starting_beams.extend([
        Beam((x,max_y),Direction.UP)
        for x in range(max_x)
    ])
    current_best = 0
    for beam in tqdm(starting_beams):
        current_best = max(current_best,follow_beam(grid,max_x,max_y,beam))
    print(current_best)


def follow_beam(grid:dict[tuple[int,int],str],max_x:int,max_y:int,start_beam:Beam) -> int:
    beams = [start_beam]
    all_beams:set[Beam] = set()
    while beams:
        current_beam = beams.pop()
        next_pos = current_beam.next_pos()
        # print(current_beam.position,'-',current_beam.direction,'>',next_pos)
        in_map = 0<=next_pos[0]<max_x and 0<=next_pos[1]<max_y
        if not in_map:
            # print('out of bounds')
            continue
        content = grid.get(next_pos,'.')
        while not current_beam.finished and (content != '|' or current_beam.direction in (Direction.UP,Direction.DOWN)) and (content != '-' or current_beam.direction in (Direction.LEFT,Direction.RIGHT)):
            current_beam.step_on(next_pos,content)
            next_pos = current_beam.next_pos()
            content = grid.get(next_pos,'.')
            # print(current_beam.position,'-',current_beam.direction,'>',next_pos)
            in_map = 0<=next_pos[0]<max_x and 0<=next_pos[1]<max_y
            if not in_map:
                current_beam.finish()
                all_beams.add(current_beam)
                # print('out of bounds')
        if current_beam.finished:
            continue
        current_beam.finish()
        all_beams.add(current_beam)
        left,right = current_beam.split(next_pos,content)
        if left not in all_beams:
            beams.append(left)
        if right not in all_beams:
            beams.append(right)
        # show_energized(grid,max_x,max_y,current_beam.energized_tiles)
    all_energized = set()
    for beam in all_beams:
        all_energized.update(beam.energized_tiles)
    # show_energized(grid,max_x,max_y,all_energized)
    return(len(all_energized))


EXAMPLE = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

if __name__ == "__main__":
    input_data = pathlib.Path('23/16_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
