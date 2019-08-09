#!/usr/bin/env python

import pydot
import sys
from collections import defaultdict

graph = pydot.graph_from_dot_file(sys.argv[1])
dot = graph[0]
dot.set_rankdir("LR")

relations = defaultdict(list)
nodes = dict()

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
        s.add_node(nodes[dst])
    dot.add_subgraph(s)

dot.write('output.dot')
