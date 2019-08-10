#!/usr/bin/env python

from collections import defaultdict
import pydot
import sys


GRAPH = pydot.graph_from_dot_file(sys.argv[1])
DOT = GRAPH[0]
DOT.set_rankdir("LR")

RELATIONS = defaultdict(list)
NODES = dict()

for node in DOT.get_nodes():
    if 'Admissible_' in node.get_name():
        node.set_style('filled')
        node.set_color('Green')
    elif 'Completed_' in node.get_name():
        node.set_style('filled')
        node.set_color('Red')
    NODES[node.get_name()] = node

for edge in DOT.get_edges():
    src = edge.get_source()
    dst = edge.get_destination()
    RELATIONS[src].append(dst)

for src, dst_list in RELATIONS.items():
    s = pydot.Subgraph(rank='same')
    for dst in dst_list:
        s.add_node(NODES[dst])
    DOT.add_subgraph(s)

DOT.write('output.dot')
