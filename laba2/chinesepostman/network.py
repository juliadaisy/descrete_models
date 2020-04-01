import copy

from . import my_math

class Graph(object):

    def __init__(self, data=None):
        self.edges = {}
        if data:  # data is simply a list of edges
            self.add_edges(data)

    def __repr__(self):
        return 'Graph({})'.format(str(self.edges))

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge) # edge is a tuple of data

    def add_edge(self, *args):
        self.edges[len(self.edges)] = Edge(*args)

    def remove_edges(self, edges):
        for edge in edges:
            if isinstance(edge, int):
                self.remove_edge(edge)
            else:
                self.remove_edge(*edge.contents)

    def remove_edge(self, *args):
        if len(args) == 1 and isinstance(args[0], int):
            del self.edges[args[0]]  # Remove by key
        else:
            match = self.find_edge(*args)  # Returns all matches
            del self.edges[list(match.keys())[0]]  # Delete first match only

    @property
    def nodes(self):
        return set([node for edge in self.edges.values() for node in (edge.head, edge.tail)])

    @property
    def node_keys(self):
        return sorted(self.nodes)

    @property
    def node_orders(self):
        return {x: len(self.edge_options(x)) for x in self.nodes}

    @property
    def odd_nodes(self):
        return [k for k in self.nodes if not my_math.is_even(self.node_orders[k])]

    def node_options(self, node):
        options = []
        for edge in self.edges.values():
            if edge.head == node:
                options.append(edge.tail)
            elif edge.tail == node:
                options.append(edge.head)
        return sorted(options)

    @property
    def is_eularian(self):
        return len(self.odd_nodes) == 0

    @property
    def is_semi_eularian(self):
        return len(self.odd_nodes) == 2

    @property
    def all_edges(self):
        return list(self.edges.values())

    def find_edges(self, head, tail, cost=None, directed=None):
        results = {}
        for key, edge in self.edges.items():
            if not cost and not directed:
                if (head, tail) == (edge.head, edge.tail) or \
                   (tail, head) == (edge.head, edge.tail):
                    results[key] = edge
            elif not directed:
                if (head, tail, cost) == edge or \
                   (tail, head, cost) == edge:
                    results[key] = edge
            else:
                if directed and (head, tail, cost, directed) == edge:
                    results[key] = edge
                elif (tail, head, cost, directed) == edge:
                    results[key] = edge
        return results

    def find_edge(self, head, tail, cost=None, directed=None):
        matches = self.find_edges(head, tail, cost, directed)
        return dict((matches.popitem(),))  # One result only

    def edge_options(self, node):
        return {k: v for k, v in self.edges.items() \
                if node in (v.head, v.tail)}

    def edge_cost(self, *args):
        weight = min([edge.weight for edge in self.find_edges(*args).values() if edge.weight])
        return weight

    @property
    def total_cost(self):
        return sum(x.weight for x in self.edges.values() if x.weight)

    def is_bridge(self, key):
        graph = copy.deepcopy(self)

        start = graph.edges[key].tail  # Could start at either end.

        graph.remove_edge(key)  # Don't include the given edge

        stack = []
        visited = set()  # Visited nodes
        while True:
            if start not in stack:
                stack.append(start)
            visited.add(start)
            nodes = [x for x in graph.node_options(start) \
                     if x not in visited]
            if nodes:
                start = nodes[0]  # Ascending
            else:  # Dead end
                try:
                    stack.pop()
                    start = stack[-1]  # Go back to the previous node
                except IndexError:  # We are back to the beginning
                    break

        if len(visited) == len(self.nodes):  # We visited every node
            return False  # ... therefore we did not disconnect the graph
        else:
            return True  # The edge is a bridge

    def __len__(self):
        return len(self.edges)


class Edge(object):
    def __init__(self, head=None, tail=None, weight=0, directed=False):
        self.head = head  # Start node
        self.tail = tail  # End node
        self.weight = weight  # aka Cost
        self.directed = directed  # Undirected by default

    def __eq__(self, other):
        if len(other) == 3:
            other = other + (False,)  # Assume undirected
        return (self.head, self.tail, self.weight, self.directed) == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.contents)

    def __repr__(self):
        return 'Edge({}, {}, {}, {})'.format(self.head, self.tail, self.weight, self.directed)

    def __len__(self):
        return len([x for x in (self.head, self.tail, self.weight, self.directed) if x is not None])

    def end(self, node):
        if node == self.head:
            return self.tail
        elif node == self.tail:
            return self.head
        else:
            raise ValueError('Node ({}) not in edge ({})'.format(node, self))

    @property
    def contents(self):
        return (self.head, self.tail, self.weight, self.directed)


if __name__ == '__main__':
    import tests.run_tests
    tests.run_tests.run(['network'])
