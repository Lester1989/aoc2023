"""DAY 19"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass

@dataclass
class Workflow:
    name:str
    rules:dict[tuple[str,bool,int],str]
    fallback:str

@dataclass
class Condition:
    attribute:str
    greater_than:bool
    value:int
    destination:str
    is_fallback:bool = False
    is_negated:bool = False

@dataclass
class Workflow_2:
    name:str
    conditions:list[Condition]

def part_one(data:str):
    result = 0
    rule_block,data_block = data.split('\n\n')
    workflows = construct_workflows(rule_block)

    for line in data_block.splitlines():
        data_package = {
            data_point.split('=')[0]:int(data_point.split('=')[1])
            for data_point in line[1:-1].split(',')
        }
        if is_accepted(workflows,data_package):
            result += sum(data_package.values())
    print(result)

def construct_workflow_2_s(rule_block:str):
    workflows:dict[str,Workflow_2] = {}
    for line in rule_block.splitlines():
        name = line.split('{')[0]
        raw_rules = line.split('{')[1].split('}')[0].split(',')
        conditions = []
        for rule in raw_rules:
            if ':' not in rule:
                conditions.append(Condition(None,None,None,rule,True))
            if '<' in rule:
                attribute,value = rule.split(':')[0].split('<')
                next_workflow = rule.split(':')[1]
                conditions.append(Condition(attribute,False,int(value),next_workflow))
            if '>' in rule:
                attribute,value = rule.split(':')[0].split('>')
                next_workflow = rule.split(':')[1]
                conditions.append(Condition(attribute,True,int(value),next_workflow))
        workflows[name] = Workflow_2(name,conditions)
    return workflows

def construct_workflows(rule_block:str):
    workflows:dict[str,Workflow] = {}
    for line in rule_block.splitlines():
        name = line.split('{')[0]
        raw_rules = line.split('{')[1].split('}')[0].split(',')
        rules = {}
        for rule in raw_rules:
            if ':' not in rule:
                fallback = rule
            if '<' in rule:
                attribute,value = rule.split(':')[0].split('<')
                next_workflow = rule.split(':')[1]
                rules[(attribute,False,int(value))] = next_workflow
            if '>' in rule:
                attribute,value = rule.split(':')[0].split('>')
                next_workflow = rule.split(':')[1]
                rules[(attribute,True,int(value))] = next_workflow
        workflows[name] = Workflow(name,rules,fallback)
    return workflows

def is_accepted(workflows:dict[str,Workflow],data_package:dict[str,int]) -> bool:
    current_workflow = 'in'
    while current_workflow not in ['R','A']:
        workflow = workflows[current_workflow]
        for rule in workflow.rules:
            attribute,greater_than,value = rule
            if (
                greater_than
                and data_package[attribute] > value
                or not greater_than
                and data_package[attribute] < value
            ):
                current_workflow = workflow.rules[rule]
                break
        else:
            current_workflow = workflow.fallback
    return current_workflow == 'A'

def part_two(data:str):
    result = 0
    rule_block,data_block = data.split('\n\n')
    workflows = construct_workflow_2_s(rule_block)
    # gather rules that lead to A
    accepting_paths:list[list[Condition]] = []
    current = 'in'
    paths:list[list[Condition]] = [
        [out] for out in workflows[current].conditions
        if not out.is_fallback
    ]
    paths.append([
        Condition(neg_condition.attribute,neg_condition.greater_than,neg_condition.value,neg_condition.destination,False,True)
        for neg_condition in workflows[current].conditions
        if not neg_condition.is_fallback
    ])

    while paths:
        current_path = paths.pop()
        current = current_path[-1].destination
        if current == 'A':
            print('found path to A')
            for condition in current_path:
                print(condition)
            accepting_paths.append(current_path)
            continue
        if current == 'R':
            continue
        for condition in workflows[current].conditions:
            if condition.destination != 'R' and all( condition.destination != x.destination for x in current_path ):
                if condition.is_fallback:
                    negated_conditions = [
                        Condition(neg_condition.attribute,neg_condition.greater_than,neg_condition.value,neg_condition.destination,False,True)
                        for neg_condition in workflows[condition.destination].conditions
                        if not neg_condition.is_fallback
                    ]
                    paths.append(current_path + negated_conditions)
                else:
                    paths.append(current_path + [condition])
    print(len(accepting_paths))
    possible_configurations = set()
    for path in accepting_paths:
        grouped_by_attribute:dict[str,list[Condition]] = { }
        for condition in path:
            if condition.attribute not in grouped_by_attribute:
                grouped_by_attribute[condition.attribute] = []
            grouped_by_attribute[condition.attribute].append(condition)
        lowers ={
            'x': 1,
            'm': 1,
            'a': 1,
            's': 1,
        }
        uppers ={
            'x': 4000,
            'm': 4000,
            'a': 4000,
            's': 4000,
        }
        for attribute,conditions in grouped_by_attribute.items():
            for condition in conditions:
                if condition.greater_than and not condition.is_negated:
                    lowers[attribute] = max(lowers[attribute],condition.value+1)
                elif condition.greater_than and condition.is_negated:
                    uppers[attribute] = min(uppers[attribute],condition.value)
                elif not condition.greater_than and not condition.is_negated:
                    uppers[attribute] = min(uppers[attribute],condition.value-1)
                elif not condition.greater_than and condition.is_negated:
                    lowers[attribute] = max(lowers[attribute],condition.value)
        # NOPE!!
        # path_possibilities = {
        #     (x,m,a,s)
        #     for x in range(lowers['x'],uppers['x']+1)
        #     for m in range(lowers['m'],uppers['m']+1)
        #     for a in range(lowers['a'],uppers['a']+1)
        #     for s in range(lowers['s'],uppers['s']+1)
        # }


        print(lowers,uppers)
        print(len(path_possibilities))
        possible_configurations |= path_possibilities
        print()
    print(len(possible_configurations))






EXAMPLE = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/19_data.txt').read_text(encoding='utf-8')
    input_data = EXAMPLE
    # part_one(input_data)
    print('--- PART TWO ---')
    part_two(input_data)
