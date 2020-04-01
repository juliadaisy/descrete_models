import re
import PySimpleGUI as sg
import sys

if len(sys.argv) == 1:
    event1, values1 = sg.Window('Boruvka',
                                [[sg.Text('Choose a file')],
                                 [sg.In(), sg.FileBrowse()],
                                 [sg.Open(), sg.Cancel()]]).read(close=True)
    fname = values1[0]

else:
    fname = sys.argv[1]

if not fname:
    raise SystemExit("Cancelling: no filename supplied...")

f = open(fname, "r")
if f.mode == 'r':
    contents = f.read()
    contents = re.split(r'[,\s]\s*', contents)

values = contents[0::3]
v1 = contents[1::3]
v2 = contents[2::3]


def find_vertices(v1, v2):
    a = []
    for item in v1:
        a.append(item)
    for item in v2:
        a.append(item)
    a_sorted = sorted(a)
    return list(set(a_sorted))


parent = dict()
rank = dict()

graphset = []
for item in range(len(values)):
    a = [int(values[item]), v1[item], v2[item]]
    graphset.append(a)

graphset = list(set(map(tuple, graphset)))


def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0


def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]


def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
        if rank[root1] == rank[root2]:
            rank[root2] += 1


def max_boruvka(graph):
    for vertice in graph['vertices']:
        make_set(vertice)
        maximum_spanning_tree = set()
        edges = list(graph['edges'])
        edges = sorted(edges, reverse=True)
        # print edges
    for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            maximum_spanning_tree.add(edge)

    return sorted(maximum_spanning_tree, reverse=True)


def min_boruvka(graph):
    for vertice in graph['vertices']:
        make_set(vertice)
        minimum_spanning_tree = set()
        edges = list(graph['edges'])
        edges = sorted(edges)
        # print edges
    for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add(edge)

    return sorted(minimum_spanning_tree)


graph = {
    'vertices': sorted(find_vertices(v1, v2)),
    'edges': set(graphset)
}

print("Minimal Spanning Tree")
min_tree = min_boruvka(graph)

for item in min_tree:
    print(item)

print("\nMaximal Spanning Tree")
max_tree = max_boruvka(graph)

for item in max_tree:
    print(item)
