"""DAY 25"""
from __future__ import annotations

import pathlib
import networkx as nx
import matplotlib.pyplot as plt

def part_one(data:str):
    result = 0
    nodes = set()
    edges = set()
    for line in data.splitlines():
        source,destinations = line.split(': ')
        nodes.add(source)
        for destination in destinations.split(' '):
            edges.add(tuple(sorted((source,destination))))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    # found by manual visual inspection
    # nx.draw(graph,with_labels=True)
    # plt.show()
    graph.remove_edge("lxb","vcq")
    graph.remove_edge("mmr","znk")
    graph.remove_edge("ddj","rnx")
    result = 1
    for comp in nx.connected_components(graph):
        print(len(comp))
        result *= len(comp)
    print(result)

def part_two(data:str):
    result = 0
    for line in data.splitlines():
        print(line)
    print(result)

EXAMPLE = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

if __name__ == "__main__":
    input_data = pathlib.Path('23/25_data.txt').read_text(encoding='utf-8')
    # input_data = EXAMPLE
    part_one(input_data)
    print('--- PART TWO ---')
    # part_two(input_data)
