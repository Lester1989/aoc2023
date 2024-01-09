"""DAY 24"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
import itertools
from skspatial.objects import Line,Point
from tqdm import tqdm

@dataclass
class Hailstone:
    position:tuple[int,int,int]
    velocity:tuple[int,int,int]

def part_one(data:str,lower_bound:int=7,upper_bound:int=27,verbose:bool=False):
    result = 0
    hailstones = []
    for line in data.splitlines():
        raw_position, raw_velocity = line.split(' @ ')
        velocity = tuple(int(v) for v in raw_velocity.split(','))
        position = tuple(int(p) for p in raw_position.split(','))
        hailstones.append(Hailstone(position,velocity))
        # print(position,velocity)
    print(len(hailstones),'hailstones calculating intersections')
    # for each pair of hailstones, calculate the intersection
    for first,second in tqdm(itertools.combinations(hailstones,2),total=len(hailstones)*(len(hailstones)-1)//2):
        if verbose:
            print()
            print(first)
            print(second)
        intersection = calculate_intersection_2d(first,second,verbose)
        if not intersection:
            continue
        if verbose:
            print(intersection)
        if lower_bound <= intersection[0] <= upper_bound and lower_bound <= intersection[1] <= upper_bound:
            if verbose:
                print('inside')
            result += 1
        elif verbose:
            print('outside')
    print(result)

def calculate_intersection_2d(first:Hailstone,second:Hailstone,verbose:bool=False) -> tuple[int,int]:
    first_line = Line(point=[first.position[0],first.position[1]],direction=[first.velocity[0],first.velocity[1]])
    second_line = Line(point=[second.position[0],second.position[1]],direction=[second.velocity[0],second.velocity[1]])
    try:
        intersection = first_line.intersect_line(second_line)
    except ValueError:
        if verbose:
            print('no intersection')
        return None
    # check if intersection is in direction of velocity for both hailstones
    first_point = Point([first.position[0],first.position[1]])
    second_point = Point([second.position[0],second.position[1]])
    try:
        first_angle_to_intersection = first_line.direction.angle_between(Line.from_points(first_point,intersection).direction)
        # print('first_angle_to_intersection',first_angle_to_intersection)
        if abs(first_angle_to_intersection)>.1:
            if verbose:
                print('not in direction of first')
            return None
        second_angle_to_intersection = second_line.direction.angle_between(Line.from_points(second_point,intersection).direction)
        # print('second_angle_to_intersection',second_angle_to_intersection)
        if abs(second_angle_to_intersection)>.1:
            if verbose:
                print('not in direction of second')
            return None
    except ValueError:
        return  ((intersection[0]),(intersection[1]))
    return ((intersection[0]),(intersection[1]))




def part_two(data:str):
    result = 0
    for line in data.splitlines():
        print(line)
    print(result)

EXAMPLE = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/24_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    part_one(input_data,200000000000000,400000000000000)
    print('--- PART TWO ---')
    # part_two(input_data)
