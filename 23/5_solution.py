"""DAY 5"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from tqdm import tqdm

VERBOSITY = 0
@dataclass
class ConvertEntry:
    destintation_start:int
    source_start:int
    range_length:int

    def __repr__(self):
        return f'[{self.source_start} .. {self.source_start+self.range_length}] -> [{self.destintation_start} .. {self.destintation_start+self.range_length}]'

    def convert(self, seed:int) -> int:
        if seed >= self.source_start and seed <= self.source_start+self.range_length:
            return self.destintation_start + seed - self.source_start
        return seed

@dataclass
class Converter:
    from_name:str
    to_name:str
    convert_map:list[ConvertEntry]

    def convert(self, seed:int) -> int:
        for convert_entry in self.convert_map:
            if seed >= convert_entry.source_start and seed <= convert_entry.source_start+convert_entry.range_length:
                return convert_entry.convert(seed)
        return seed

def part_one(data:str):
    seeds = []
    convert_maps:list[Converter] = []
    for block in data.split("\n\n"):
        if not seeds:
            seeds = [int(x) for x in block.split(":")[1].split()]
            continue
        # create maps
        lines = block.splitlines()
        from_name = lines[0].split("-")[0]
        to_name = lines[0].split("-")[2].split()[0]
        convert_entries = [
            ConvertEntry(*[int(x) for x in line.split()]) 
            for line in lines[1:]
        ]
        convert_maps.append(Converter(from_name, to_name, convert_entries))
    # print(seeds)
    # print(convert_maps)
    translated_seeds = []
    for seed in seeds:
        # print(seed)
        for convert_map in convert_maps:
            # print (convert_map.from_name, convert_map.to_name)
            if convert_map.from_name == convert_map.to_name:
                continue
            seed = convert_map.convert(seed)
            # print('->',seed)
        translated_seeds.append(seed)


    print(min(translated_seeds))

@dataclass
class SeedGroup:
    start:int
    end:int

@dataclass
class GroupConverter:
    from_name:str
    to_name:str
    convert_map:list[ConvertEntry]

    def convert(self, seed:SeedGroup) -> list[SeedGroup]:
        result_groups:list[SeedGroup] = []
        unconverted:list[SeedGroup] = [SeedGroup(seed.start, seed.end)]
        # print('converting',seed)
        # print('using map',self.convert_map)
        while unconverted:
            remaining_seed = unconverted.pop()
            if VERBOSITY > 1:
                print('remaining',remaining_seed)
                input()
            for convert_entry in self.convert_map:
                if VERBOSITY > 1:
                    print(convert_entry,'?')
                # for every convert entry check 5 cases:
                # outside -> nothing
                # intersect front -> split in non_convert and convert
                # intersect back -> split in convert and non_convert
                # inside -> convert
                # intersect front and back -> split in non_convert, convert, non_convert
                if remaining_seed.start > convert_entry.source_start + convert_entry.range_length or remaining_seed.end < convert_entry.source_start:
                    # outside
                    if VERBOSITY > 1:
                        print('outside',remaining_seed.start ,'>', convert_entry.source_start + convert_entry.range_length, 'or', remaining_seed.end, '<', convert_entry.source_start)
                    continue
                if remaining_seed.start < convert_entry.source_start and remaining_seed.end > convert_entry.source_start and remaining_seed.end <= convert_entry.source_start + convert_entry.range_length:
                    # intersect front
                    if VERBOSITY > 1:
                        print('intersect front')
                    # non_convert
                    unconverted.append(SeedGroup(remaining_seed.start, convert_entry.source_start-1))

                    # convert
                    result_groups.append(SeedGroup(convert_entry.destintation_start, convert_entry.convert(remaining_seed.end)))
                    remaining_seed = None
                    break
                if remaining_seed.start >= convert_entry.source_start and remaining_seed.start < convert_entry.source_start + convert_entry.range_length and remaining_seed.end > convert_entry.source_start + convert_entry.range_length:
                    # intersect back
                    if VERBOSITY > 1:
                        print('intersect back')
                    # convert
                    result_groups.append(SeedGroup(convert_entry.convert(remaining_seed.start), convert_entry.destintation_start + convert_entry.range_length))
                    # non_convert
                    unconverted.append(SeedGroup(convert_entry.source_start + convert_entry.range_length+1, remaining_seed.end))
                    remaining_seed = None
                    break
                if remaining_seed.start >= convert_entry.source_start and remaining_seed.end <= convert_entry.source_start + convert_entry.range_length:
                    # inside
                    if VERBOSITY > 1:
                        print('inside')
                    result_groups.append(SeedGroup(convert_entry.convert(remaining_seed.start), convert_entry.convert(remaining_seed.end)))
                    remaining_seed = None
                    break
                if remaining_seed.start < convert_entry.source_start and remaining_seed.end > convert_entry.source_start + convert_entry.range_length:
                    # intersect front and back
                    if VERBOSITY > 1:
                        print('intersect front and back')
                    # non_convert
                    unconverted.append(SeedGroup(remaining_seed.start, convert_entry.source_start-1))

                    # convert
                    result_groups.append(SeedGroup(convert_entry.destintation_start, convert_entry.destintation_start + convert_entry.range_length))

                    # non_convert
                    unconverted.append(SeedGroup(convert_entry.source_start + convert_entry.range_length+1, remaining_seed.end))
                    remaining_seed = None
                    break
            if remaining_seed:
                if VERBOSITY > 1:
                    print('no convert')
                result_groups.append(remaining_seed)
        # print('result',result_groups)
        return result_groups

def merge_groups(groups:list[SeedGroup]) -> list[SeedGroup]:
    result_groups:list[SeedGroup] = []
    # print('merging groups',groups)
    ordered_groups = sorted(groups, key=lambda x: x.start)
    currend_start = ordered_groups[0].start
    current_end = ordered_groups[0].end
    for group in ordered_groups[1:]:
        if group.start <= current_end:
            current_end = max(current_end, group.end)
        else:
            result_groups.append(SeedGroup(currend_start, current_end))
            currend_start = group.start
            current_end = group.end
    result_groups.append(SeedGroup(currend_start, current_end))
    # print('result',result_groups)
    return result_groups

def part_two(data:str):
    seeds:list[SeedGroup] = []
    convert_maps:list[GroupConverter] = []
    for block in data.split("\n\n"):
        if not seeds:
            raw_seeds = block.split(":")[1].split()
            for idx in range(0,len(raw_seeds),2):
                seeds.append(SeedGroup(int(raw_seeds[idx]), int(raw_seeds[idx])+int(raw_seeds[idx+1])))
            continue
        # create maps
        lines = block.splitlines()
        from_name = lines[0].split("-")[0]
        to_name = lines[0].split("-")[2].split()[0]
        convert_entries = [
            ConvertEntry(*[int(x) for x in line.split()]) 
            for line in lines[1:]
        ]
        convert_maps.append(GroupConverter(from_name, to_name, convert_entries))
    seeds = merge_groups(seeds)
    for convert_map in tqdm(convert_maps):
        next_gen = []
        for seed in seeds:
            next_seeds = convert_map.convert(seed)
            next_gen.extend( next_seeds)
        seeds = merge_groups(next_gen)
        # print(f'converted to {convert_map.to_name}\n')

    # print(seeds)
    print(min(seeds, key=lambda x: x.start).start)

EXAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/5_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
