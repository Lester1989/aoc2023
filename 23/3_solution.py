"""
DAY 3
you need to install colorama to see colors in the terminal
`pip install colorama`
"""

from __future__ import annotations
import pathlib

import pkg_resources
has_colorama = "colorama" in [pkg.key for pkg in pkg_resources.working_set]
if has_colorama:
    from colorama import init as colorama_init
    from colorama import Fore
    from colorama import Style

    colorama_init()

def check_adjecent_to_symbol(grid:dict[tuple[int,int],str], coord:tuple[int,int]) -> tuple[str,set[tuple[int,int]]]:
    found = ""
    searched_coords = set()
    for i, j in [(-1,1), (0,1), (1,1), (-1,0), (1,0), (-1,-1), (0,-1), (1,-1)]:
        check_coord = (coord[0]+i,coord[1]+j)
        grid_content = grid.get(check_coord)
        searched_coords.add(check_coord)
        if grid_content and not grid_content.isdigit():
            found += grid_content
    return found, searched_coords

def find_complete_number(grid:dict[tuple[int,int],str], start_coord:tuple[int,int]) -> tuple[str,set[tuple[int,int]]]:
    while start_coord in grid and grid[start_coord].isdigit():
        start_coord = (start_coord[0]-1,start_coord[1])
    start_coord = (start_coord[0]+1,start_coord[1])
    number_string = grid[start_coord]
    number_coords = {start_coord}
    while (start_coord[0]+1,start_coord[1]) in grid and grid[(start_coord[0]+1,start_coord[1])].isdigit():
        start_coord = (start_coord[0]+1,start_coord[1])
        number_string += grid[start_coord]
        number_coords.add(start_coord)
    return number_string, number_coords

def part_one(data:str,verbosity:int=0):
    grid:dict[tuple[int,int],str] = {}
    for y,line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char != '.':
                grid[(x,y)] = char
    visited_digit = set()
    result = 0
    for x,y in grid.keys(): # .keys is not needed, but makes it more clear that we are iterating over the keys of type tuple[int,int]
        if (x,y) in visited_digit:
            continue
        if not grid[(x,y)].isdigit():
            continue
        number_string, number_coords = find_complete_number(grid, (x,y))
        visited_digit.update(number_coords)
        adjecent_to_symbols = ""
        relevant_coords = set()
        for coord in number_coords:
            new_adjecent_to_symbols,searched_coords = check_adjecent_to_symbol(grid, coord)
            adjecent_to_symbols += new_adjecent_to_symbols
            relevant_coords.update(searched_coords)
        if adjecent_to_symbols:
            result += int(number_string)
            if verbosity > 0:
                print(f"Found {number_string} with adjecent symbol {adjecent_to_symbols}")
        else:
            if verbosity > 0:
                print(f"Found {number_string} with no adjecent symbol")
        if verbosity > 1 and has_colorama:
            visualize_colored(grid, relevant_coords)
            input()
        elif verbosity > 1:
            visualize(grid, relevant_coords)
            input()

    print(result)

def visualize(grid, relevant_coords):
    min_x = min(coord[0] for coord in relevant_coords)
    max_x = max(coord[0] for coord in relevant_coords)
    min_y = min(coord[1] for coord in relevant_coords)
    max_y = max(coord[1] for coord in relevant_coords)
    for y in range(min_y,max_y+1):
        print("".join(grid.get((x,y),'.') for x in range(min_x,max_x+1)))

def visualize_colored(grid, relevant_coords):
    min_x = min(coord[0] for coord in relevant_coords)
    max_x = max(coord[0] for coord in relevant_coords)
    min_y = min(coord[1] for coord in relevant_coords)
    max_y = max(coord[1] for coord in relevant_coords)
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            char = grid.get((x,y),'.')
            if char.isdigit():
                print(Fore.BLUE + char, end="")
            elif (x,y) in grid:
                print(Fore.RED + char, end="")
            else:
                print(Fore.GREEN + char, end="")
        print(Style.RESET_ALL)

def part_two(data:str,verbosity:int=0):
    grid:dict[tuple[int,int],str] = {}
    for y,line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char != '.':
                grid[(x,y)] = char
    visited_digit = set()
    gears:dict[tuple[int,int],list[int]] = {}
    for x,y in grid.keys(): # .keys is not needed, but makes it more clear that we are iterating over the keys of type tuple[int,int]
        if (x,y) in visited_digit:
            continue
        if not grid[(x,y)].isdigit():
            continue
        number_string, number_coords = find_complete_number(grid, (x,y))
        visited_digit.update(number_coords)
        adjecent_to_symbols = ""
        relevant_coords = set()
        for coord in number_coords:
            new_adjecent_to_symbols,searched_coords = check_adjecent_to_symbol(grid, coord)
            adjecent_to_symbols += new_adjecent_to_symbols
            relevant_coords.update(searched_coords)
        if adjecent_to_symbols:
            if verbosity > 0:
                print(f"Found {number_string} with adjecent symbol {adjecent_to_symbols}")
            if '*' in adjecent_to_symbols:
                for coord in relevant_coords:
                    if coord in grid and grid[coord]=="*":
                        gears[coord] = gears.get(coord,[]) + [int(number_string)]
        elif verbosity > 0:
            print(f"Found {number_string} with no adjecent symbol")
    result = sum(
        numbers_at_gear[0] * numbers_at_gear[1]
        for numbers_at_gear in gears.values()
        if len(numbers_at_gear) == 2
    )
    print(result)


EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

if __name__ == "__main__":
    input_data = pathlib.Path('23/3_data.txt').read_text(encoding='utf-8')
    input_data = EXAMPLE

    part_one(input_data,2)
    print('--- PART TWO ---')
    part_two(input_data)
