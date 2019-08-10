#!/usr/bin/env python

import pydot
import sys
import re
import networkx as nx


DOT = pydot.graph_from_dot_file(sys.argv[1])[0]
GRAPH = nx.DiGraph()
RE_CLASS = re.compile(r"(?P<status>(Admissible|Completed))_(?P<type>[^\]]+)\[(?P<name>[^\]]+)\]")
RE_RESOURCE = re.compile(r"(?P<type>[^\]]+)\[(?P<name>[^\]]+)\]")

for node in DOT.get_nodes():
    NODE_NAME = node.get_name().strip('"')
    match = RE_CLASS.search(NODE_NAME) or RE_RESOURCE.search(NODE_NAME)

    if match:
        GRAPH.add_node(NODE_NAME, **match.groupdict())


for edge in DOT.get_edges():
    src = edge.get_source().strip('"')
    dst = edge.get_destination().strip('"')
    GRAPH.add_edge(src, dst)

nx.write_gexf(GRAPH, f"{sys.argv[1]}.gexf")
