"""DAY 20"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from enum import Enum
from tqdm import tqdm

class Pulse(Enum):
    HIGH = 1
    LOW = 2

class State(Enum):
    ON = 1
    OFF = 2

@dataclass
class ElfSignal:
    source:str
    pulse:Pulse
    target:str
@dataclass
class ElfModule:
    inputs:dict[str,Pulse]
    outputs:list[str]
    name:str

    def tick(self,signal:ElfSignal)->list[ElfSignal]:
        pass
@dataclass
class Flipflip(ElfModule):
    state:State = State.OFF

    def tick(self,signal:ElfSignal)->list[ElfSignal]:
        if signal.pulse == Pulse.HIGH:
            return []
        self.state = State.ON if self.state == State.OFF else State.OFF
        return [
            ElfSignal(
                self.name,
                Pulse.HIGH if self.state == State.ON else Pulse.LOW,
                output
            ) for output in self.outputs
        ]

@dataclass
class Broadcaster(ElfModule):

    def tick(self,signal:ElfSignal)->list[ElfSignal]:
        return [
            ElfSignal(
                self.name,
                signal.pulse,
                output
            ) for output in self.outputs
        ]

@dataclass
class Conjunction(ElfModule):
    
    def tick(self,signal:ElfSignal)->list[ElfSignal]:
        self.inputs[signal.source] = signal.pulse
        if all(received_puls == Pulse.HIGH for received_puls in self.inputs.values()):
            return [
                ElfSignal(
                    self.name,
                    Pulse.LOW,
                    output
                ) for output in self.outputs
            ]
        return [
                ElfSignal(
                    self.name,
                    Pulse.HIGH,
                    output
                ) for output in self.outputs
            ]




def part_one(data:str,button_pushes:int=1):
    puls_counter = {
        Pulse.HIGH:0,
        Pulse.LOW:0
    }
    modules = build_modules(data)
    for button_push in tqdm(range(button_pushes)):
        #print('button_push ==',button_push,'==')
        # print(puls_counter)
        signals:list[ElfSignal] = [ElfSignal('button',Pulse.LOW,'broadcaster')]
        while signals:
            signal = signals.pop(0)
            # print('tick',signal)
            puls_counter[signal.pulse] += 1
            if signal.target not in modules:
                # print('target not found', signal.target)
                continue
            new_signals = modules[signal.target].tick(signal)
            # print('new_signals',new_signals)
            signals.extend(new_signals)
    print((puls_counter[Pulse.HIGH])*(puls_counter[Pulse.LOW]))

def build_modules(data:str) -> dict[str,ElfModule]:
    modules:dict[str,ElfModule] = {}
    for line in data.splitlines():
        if line.startswith('%'):
            # flipflip
            name = line.split(' -> ')[0][1:]
            modules[name] = Flipflip(
                {},
                line.split(' -> ')[1].split(', '),
                name
            )
        elif line.startswith('&'):
            # conjunction
            name = line.split()[0][1:]
            modules[name] = Conjunction(
                {},
                line.split(' -> ')[1].split(', '),
                name
            )
        elif line.startswith('broadcaster'):
            # broadcaster
            name = line.split()[0]
            modules[name] = Broadcaster(
                {},
                line.split(' -> ')[1].split(', '),
                name
            )
        else:
            print('error')
    for module in modules.values():
        for sends_to in module.outputs:
            if sends_to not in modules:
                continue
            modules[sends_to].inputs[module.name] = Pulse.LOW
    return modules

import math

def part_two(data:str,button_pushes:int=18_000):
    modules = build_modules(data)
    tg_input_cycles = {
        source:[]
        for source in modules['tg'].inputs.keys()
    }
    for button_push in tqdm(range(button_pushes)):
        # if button_push % 1000 == 0:
        #     print('button_push ==',button_push,'==')
        low_signals_to_rx = 0
        signals:list[ElfSignal] = [ElfSignal('button',Pulse.LOW,'broadcaster')]
        while signals:
            signal = signals.pop(0)
            # print('tick',signal)
            if signal.target =='rx' and signal.pulse == Pulse.LOW:
                low_signals_to_rx += 1
            if signal.target =='tg' and signal.pulse == Pulse.HIGH:
                tg_input_cycles[signal.source].append(button_push)
            if signal.target not in modules:
                # print('target not found', signal.target)
                continue
            new_signals = modules[signal.target].tick(signal)
            # print('new_signals',new_signals)
            signals.extend(new_signals)
        if low_signals_to_rx == 1:
            print('button_push',button_push)
            break
    print(tg_input_cycles)
    cycles = [tg_input_cycles[source][1]-tg_input_cycles[source][0] for source in tg_input_cycles.keys()]
    for source,send_numbers in tg_input_cycles.items():
        print(source,':')
        print(send_numbers)
        print([n-send_numbers[0] for n in send_numbers ])
        print()

    print(math.lcm(*cycles))

def mermaidify(data:str):
    result = 'flowchart TD\n'
    result_lines:list[str] = []
    for line in data.splitlines():
        outputs = line.split(' -> ')[1].split(', ')
        if line.startswith('%'):
            # flipflip
            name = line.split(' -> ')[0][1:]
            result_lines.extend(
                f'{name}(Flipflop {name}) -->{output}\n' for output in outputs
            )
        elif line.startswith('&'):
            # conjunction
            name = line.split()[0][1:]
            result_lines.extend(
                f'{name}(Conjunction {name}) -->{output}\n'
                for output in outputs
            )
        elif line.startswith('broadcaster'):
            # broadcaster
            name = line.split()[0]
            result_lines.extend(
                f'{name}(Broadcaster {name}) -->{output}\n'
                for output in outputs
            )
        else:
            print('error')

    # manuel sort types
    for line in result_lines:
        if line.startswith('broadcaster'):
            result += line

    for line in sorted(result_lines):
        if 'Conjunction' not in line and 'Broadcaster' not in line:
            result += line

    for line in sorted(result_lines):
        if 'Conjunction' in line:
            result += line

    return result

EXAMPLE = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

EXAMPLE_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/20_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE_2
    # part_one(input_data,1000)
    print('--- PART TWO ---')
    part_two(input_data)
    # print(mermaidify(input_data))
