from collections import defaultdict
import PySimpleGUI as sg
import sys
import re


class Graph:

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)

    def BFS(self, s, t, parent):

        visited = [False] * (self.ROW)

        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    def FordFulkerson(self, source, sink):

        parent = [-1] * (self.ROW)

        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


if len(sys.argv) == 1:
    event1, values1 = sg.Window('Maximum Flow',
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

a = contents[0::6]
b = contents[1::6]
c = contents[2::6]
d = contents[3::6]
e = contents[4::6]
f = contents[5::6]

graphset = []
for item in range(len(a)):
    graph = [int(a[item]), int(b[item]), int(c[item]), int(d[item]), int(e[item]), int(f[item])]
    graphset.append(graph)

g = Graph(graphset)

source = 0;
sink = 5

print("The maximum possible flow is %d " % g.FordFulkerson(source, sink))
