"""DAY 12"""
from __future__ import annotations

import pathlib
from tqdm import tqdm

def full_knowledge_check(arrangement:str,pattern:list[int],partial:bool=False,verbose:bool=False) -> bool:
    assert '?' not in arrangement
    groups:list[str] = [group for group in arrangement.split('.') if group]
    if partial and arrangement.endswith('#'):
        if verbose:
            print('partial',arrangement,pattern,groups)
        if len(groups)-1 >= len(pattern) or len(groups[-1]) > pattern[len(groups)-1]:
            return False
        groups.pop(-1)


    return all(len(group) == expected for group, expected in zip(groups, pattern)) and ((len(groups) <= len(pattern) and partial) or len(groups) == len(pattern) )

def violates_pattern(arrangement:str,pattern:list[int],verbose:bool = False) -> bool:
    if verbose:
        print()
        print('checking',arrangement,pattern)
    if '?' not in arrangement:
        return not full_knowledge_check(arrangement,pattern,verbose=verbose)
    start = arrangement[:arrangement.find('?')]
    if not full_knowledge_check(start, pattern,partial=True,verbose=verbose):
        if verbose:
            print('start',start,'does not match pattern',pattern)
        return True
    # end = arrangement[arrangement.rfind('?')+1:]
    # if not full_knowledge_check(end[::-1],pattern[::-1]):
    #     if verbose:
    #         print('end',end,'does not match pattern',pattern)
    #     return True
    return False


def generate_arrangements_recursive(pattern:list[int],arrangement:str,verbose:bool = False) -> list[str]:
    if '?' not in arrangement:
        return [arrangement]

    arrangements = []
    current_arrangement_hash = arrangement.replace('?','#',1)
    
    if not violates_pattern(current_arrangement_hash,pattern,verbose):
        arrangements.extend(generate_arrangements_recursive(pattern,current_arrangement_hash,verbose))
    current_arrangement_dot = arrangement.replace('?','.',1)
    if not violates_pattern(current_arrangement_dot,pattern,verbose):
        arrangements.extend(generate_arrangements_recursive(pattern,current_arrangement_dot,verbose))
    return arrangements

def generate_arrangements(pattern:list[int],arrangement:str,verbose:bool = False) -> list[str]:
    if '?' not in arrangement:
        return [arrangement]

    arrangements = []
    current_arrangement_hash = arrangement.replace('?','#',1)
    if not violates_pattern(current_arrangement_hash,pattern,verbose):
        arrangements.append(current_arrangement_hash)
    current_arrangement_dot = arrangement.replace('?','.',1)
    if not violates_pattern(current_arrangement_dot,pattern,verbose):
        arrangements.append(current_arrangement_dot)
    return arrangements



def part_one(data:str):
    verbose_lines = [
    ]

    result = 0
    for line in tqdm(data.splitlines()):
        # print(line)
        arrangement,raw_pattern = line.split()
        pattern = [int(x) for x in raw_pattern.split(',')]
        arrangement_count = len(generate_arrangements_recursive(pattern,arrangement,line in verbose_lines))
        # print(arrangement_count)
        result += arrangement_count
    print(result)

def part_two(data:str):
    result = 0
    verbose_lines = [
        # "???.### 1,1,3"
        # ".??..??...?##. 1,1,3"
        # "?#?#?#?#?#?#?#? 1,3,1,6"
        # "?###???????? 3,2,1"
    ]
    for line in tqdm(data.splitlines()):
        print()
        intersting_line = line in verbose_lines
        arrangement,raw_pattern = line.split()
        arrangement = (f'{arrangement}?' * 5)[:-1]
        raw_pattern = (f'{raw_pattern},' * 5)[:-1]
        print(line)
        print('possible arrangements',2**arrangement.count('?'))
        if intersting_line:
            print('generating arrangements')

        pattern = [int(x) for x in raw_pattern.split(',')]
        arrangements = set(generate_arrangements(pattern,arrangement,intersting_line))
        if intersting_line:
            print('arrangements',arrangements)
        full_arrangements = set()
        steps = 0
        while arrangements:
            arrangement = arrangements.pop()
            steps += 1
            # if steps % 100_000 == 0:
            #     print('step',steps)
            if intersting_line:
                print('maybe extending',arrangement, '?' not in arrangement )
            if '?' in arrangement:
                new_patterns = generate_arrangements(pattern,arrangement,intersting_line)
                if intersting_line:
                    print('new patterns',new_patterns)
                arrangements.update(new_patterns)
            else:
                full_arrangements.add(arrangement)
        print(len(full_arrangements))
        if intersting_line:
            for arrangement in sorted(full_arrangements):
                print(arrangement)
        result += len(full_arrangements)

    print(result)

EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/12_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
