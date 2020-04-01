import argparse
import sys

import data.data
from chinesepostman import eularian, network


def setup_args():
    parser = argparse.ArgumentParser(description='Find an Eularian Cicruit.')
    parser.add_argument('graph', nargs='?', help='Name of graph to load')
    args = parser.parse_args()
    return args.graph


def main():
    edges = None
    graph_name = setup_args()
    try:
        edges = getattr(data.data, graph_name)
    except (AttributeError, TypeError):
        print('Invalid graph name. Available graphs:\n\t{}\n'.format(
            '\n\t'.join([x for x in dir(data.data)
                         if not x.startswith('__')])))
        sys.exit()

    original_graph = network.Graph(edges)

    print('Number of edges: {}'.format(len(original_graph)))
    if not original_graph.is_eularian:
        graph, num_dead_ends = eularian.make_eularian(original_graph)
        # print('\tAdded {} edges'.format(len(graph) - len(original_graph) + num_dead_ends))
        print('Total cost: {}'.format(graph.total_cost))
    else:
        graph = original_graph

    route, attempts = eularian.eularian_path(graph, start=1)
    if not route:
        print('Gave up after <{}> attempts.'.format(attempts))
    else:
        print('Solution ({} edges):'.format(len(route) - 1))
        print('{}'.format(route))


if __name__ == '__main__':
    main()
