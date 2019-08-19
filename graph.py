#!/usr/bin/env python

import sys
import re
import argparse
import pydot
import networkx as nx


def main():
    """
    Main
    """
    parser = argparse.ArgumentParser(description="Transforms puppet- graphs to gexf files.")
    parser.add_argument("-i", "--input", dest="input",
                        help="The expanded_relationships.dot file",
                        required=True)
    parser.add_argument("--accept-regex", dest="regex",
                        help="Filters the string by this regex.",
                        default=".*")
    parser.add_argument("--reject-regex", dest="reject",
                        help="Filters the string by this regex.",
                        required=False)
    parser.add_argument("-c", "--cycles", dest="cycles",
                        action="store_true", help="Colorize cycles")
    parser.add_argument("--dot", dest="dot",
                        action="store_true", help="Save as dot")
    parser.add_argument("-o", "--output", dest="output",
                        help="The output file", default="output.gexf")
    args = parser.parse_args()

    if args.dot:
        try:
            import pygraphviz
            from networkx.drawing.nx_agraph import write_dot
        except ImportError as ie:
            print(f"Using gefx- mode {ie}")
            args.dot = False

    dot = pydot.graph_from_dot_file(args.input)[0]
    graph = nx.DiGraph()
    re_class = re.compile(r"(?P<status>(Admissible|Completed))_(?P<type>[^\[]+)\[(?P<name>[^\]]+)\]")
    re_resource = re.compile(r"(?P<type>[^\]]+)\[(?P<name>[^\]]+)\]")
    re_filter = re.compile(args.regex)

    if args.reject:
        re_reject = re.compile(args.reject)

    for node in dot.get_nodes():
        node_name = node.get_name().strip('"')
        if args.reject and re_reject.search(node_name):
            continue

        match = re_filter.search(node_name)\
                and (re_class.search(node_name)\
                or re_resource.search(node_name))

        if match:
            graph.add_node(node_name, **match.groupdict())

    for edge in dot.get_edges():
        src = edge.get_source().strip('"')
        dst = edge.get_destination().strip('"')

        if args.reject and ( re_reject.search(src) or re_reject.search(dst)):
            continue

        if re_filter.search(src) and re_filter.search(dst):
            graph.add_edge(src, dst)

    if args.cycles:
        try:
            cycles = nx.find_cycle(graph, orientation="original")
            for cycle in cycles:
                edge = graph.get_edge_data(cycle[0], cycle[1])
                edge['viz'] = {'color' : {'r': 255, 'g': 0, 'b': 0, 'a': 1.0}}
        except nx.exception.NetworkXNoCycle:
            print("No cycles found!")

    if args.dot:
        write_dot(graph, args.output.replace('gexf', 'dot'))
    else:
        nx.write_gexf(graph, args.output)

if __name__ == "__main__":
    SystemExit(main())
