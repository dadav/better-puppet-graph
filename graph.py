#!/usr/bin/env python

import pydot
import sys
from collections import defaultdict
from itertools import cycle

graph = pydot.graph_from_dot_file(sys.argv[1])
dot = graph[0]
dot.set_rankdir("LR")

relations = defaultdict(list)
nodes = dict()

c = cycle(["red", "blue"])

for node in dot.get_nodes():
    nodes[node.get_name()] = node

for edge in dot.get_edges():
    src = edge.get_source()
    dst = edge.get_destination()
    relations[src].append(dst)

for src, dst_list in relations.items():
    s = pydot.Subgraph(rank='same')
    node_color = c.__next__()
    for dst in dst_list:
        node = nodes[dst]
        node.set_fillcolor(node_color)
        s.add_node(node)
    dot.add_subgraph(s)

dot.write('output.dot')
