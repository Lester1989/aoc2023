"""DAY 6"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass

@dataclass
class BoatRace:
    time:int
    distance:int

def part_one(data:str):
    result = 1
    time_line,distance_line = data.splitlines()
    races = [BoatRace(int(x),int(y)) for x,y in list(zip(time_line.split(), distance_line.split()))[1:]]
    for race in races:
        possibilities = 0
        for press_time in range(race.time):
            if press_time*(race.time-press_time)>race.distance:
                # print(f'{press_time} is valid')
                possibilities += 1
        result *= possibilities
    print(result)

def part_two(data:str):
    result = 1
    time_line,distance_line = data.splitlines()
    races = [BoatRace(int(x),int(y)) for x,y in list(zip(time_line.split(), distance_line.split()))[1:]]
    for race in races:
        possibilities = 0
        for press_time in range(race.time):
            if press_time*(race.time-press_time)>race.distance:
                # print(f'{press_time} is valid')
                possibilities += 1
        result *= possibilities
    print(result)

EXAMPLE = """Time:      7  15   30
Distance:  9  40  200"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/6_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data.replace(' ','').replace(':',' '))
