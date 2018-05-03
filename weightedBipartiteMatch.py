import numpy as np
from collections import deque

M=[]
class spfa():

    # nx: list of drivers
    # ny: list of requests
    # edge: 01 adjacency matrix to represent edge from driver to request,
    # weight: adjacency matrix to represent weight for each edge
    def __init__(self, nx, ny, edge, weight):
        self.nx, self.ny=nx, ny
        self.edge = edge
        self.weight = weight

    def max_match(self):
        self.construct_graph()
        return self.minCostMaxFlow()

    def construct_graph(self):
        self.nx_size = len(self.nx)

        self.S = len(self.nx) + len(self.ny)
        self.T = self.S + 1
        self.total_v = len(self.nx) + len(self.ny) + 2
        self.edge_list = [[] for i in range(self.total_v)]
        for i, x in enumerate(self.nx):
            for j, y in enumerate(self.ny):
                if self.edge[i][j]:
                    self.add_edge(i, j + self.nx_size, self.weight[i][j])

        for i, x in enumerate(self.nx):
            self.add_edge(self.S, i, 0)

        for j, y in enumerate(self.ny):
            self.add_edge(j + self.nx_size, self.T, 0)

    def add_edge(self, x, y, weight):
        ex = {'v': y, 'weight': weight, 'rest_flow': 1}
        ey = {'v': x, 'weight': -weight, 'rest_flow': 0}
        ex['rev'] = ey
        ey['rev'] = ex
        self.edge_list[x].append(ex)
        self.edge_list[y].append(ey)

    def minCostMaxFlow(self):
        weight_sum = 0
        max_flow = 0
        while True:
            path = [{}] * self.total_v
            in_queue = [False] * self.total_v
            distance = [np.inf] * self.total_v
            Q = deque([self.S])
            in_queue[self.S] = True
            distance[self.S] = 0
            while len(Q) > 0:
                v = Q.popleft()
                for e in self.edge_list[v]:
                    y = e['v']
                    if e['rest_flow'] > 0 and distance[y] > distance[v] + e['weight'] + 1e-10:
                        distance[y] = distance[v] + e['weight']
                        path[y] = e
                        if not in_queue[y]:
                            in_queue[y] = True
                            Q.append(y)
                in_queue[v] = False
            if distance[self.T] == np.inf:
                break
            weight_sum += distance[self.T]
            max_flow += 1
            p = path[self.T]
            while p:
                p['rest_flow'] -= 1
                p['rev']['rest_flow'] += 1
                p = path[p['rev']['v']]
        return (max_flow, weight_sum)

    def get_matching_detail(self):
        matching = []
        for i, x in enumerate(self.nx):
            for edge in self.edge_list[i]:
                y = edge['v']
                if not y == self.S and edge['rest_flow'] == 0:
                    matching.append((i, y - self.nx_size))
        return matching
