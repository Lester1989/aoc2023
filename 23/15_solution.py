"""DAY 15"""
from __future__ import annotations

import pathlib
def myhash(val:str)->int:
    result = 0
    for c in val:
        result += ord(c)
        result *= 17
        result = result % 256
    return result


def part_one(data:str):
    result = 0
    for line in data.split(','):
        result += myhash(line)
    print(result)

def part_two(data:str):
    result = 0
    boxes:dict[int,list[tuple[str,int]]] = {}
    for lense in data.split(','):
        if '=' in lense:
            label,focal_length= lense.split('=')
            box_id = myhash(label)
            if box_id not in boxes:
                boxes[box_id] = []
            for idx,(exiting_label,_) in enumerate(boxes[box_id]):
                if exiting_label == label:
                    boxes[box_id][idx] = (label,int(focal_length))
                    break
            else:
                boxes[box_id].append((label,int(focal_length)))

        elif '-' in lense:
            label= lense.split('-')[0]
            box_id = myhash(label)
            if box_id not in boxes:
                boxes[box_id] = []
            boxes[box_id] = [(existing_label,focal_length) for existing_label,focal_length in boxes[box_id] if existing_label != label]
    for box_id,lenses in boxes.items():
        for slot,(label,focal_length) in enumerate(lenses):
            result += (box_id+1) * (slot+1) * focal_length
    print(result)

EXAMPLE = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/15_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    print(myhash("cm"))
    # part_one(input_data)
    print('--- PART TWO ---')
    # part_two(input_data)
