from __future__ import annotations

import pathlib


def part_one(data:str):
    line_numbers = []
    for line in data.splitlines():
        line_number:str = ""
        for character in line:
            if character.isdigit():
                line_number = character
                break
        for character in line[::-1]:
            if character.isdigit():
                line_number += character
                break
        line_numbers.append(int(line_number))
    print(line_numbers)
    print(sum(line_numbers))

def part_two(data:str):
    line_numbers = []
    spelled_numbers = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    print(data)
    for line in data.splitlines():
        line_number:str = ""
        while line:
            if line[0].isdigit():
                line_number = line[0]
                break
            elif any(line.startswith(spelled_number) for spelled_number in spelled_numbers):
                for spelled_number in spelled_numbers:
                    if line.startswith(spelled_number):
                        line_number = spelled_numbers[spelled_number]
                        break
                break
            else:
                line = line[1:]
        while line:
            if line[-1].isdigit():
                line_number += line[-1]
                break
            elif any(line.endswith(spelled_number) for spelled_number in spelled_numbers):
                for spelled_number in spelled_numbers:
                    if line.endswith(spelled_number):
                        line_number += spelled_numbers[spelled_number]
                        break
                break
            else:
                line = line[:-1]
        line_numbers.append(int(line_number))
    # print(line_numbers)
    print(sum(line_numbers))

example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

if __name__ == "__main__":
    data = pathlib.Path('23/1_data.txt').read_text()
    #data = example2
    part_one(data)
    print('--- PART TWO ---')
    part_two(data)
