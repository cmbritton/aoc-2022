#!/usr/bin/env python3
"""
Day 12: Hill Climbing Algorithm

https://adventofcode.com/2022/day/12
"""
import os.path
from dataclasses import dataclass
from typing import Any
import matplotlib.pyplot as plt

import networkx as nx

from src.main.python.util import AbstractSolver


@dataclass
class MyData:
    value: str


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        return self.get_data(self.get_day(), data_file_path)

    def get_label(self, d, r, c):
        return f'{d[r][c]}-{r}-{c}'

    def get_neighbor_indexes(self, d, r, c):
        indices = []
        if r != 0:
            indices.append((r - 1, c))
        if c != len(d[r]) - 1:
            indices.append((r, c + 1))
        if r != len(d) - 1:
            indices.append((r + 1, c))
        if c != 0:
            indices.append((r, c - 1))
        return indices

    def get_weight(self, u, v, p):
        print(f'u: {u}, v: {v}, weight: {p["weight"]}')
        return p['weight']

    def build_graph(self, data):
        g = nx.MultiDiGraph()
        for r in range(len(data)):
            for c in range(len(data[0])):
                label = self.get_label(data, r, c)
                for nr, nc in self.get_neighbor_indexes(data, r, c):
                    nl = self.get_label(data, nr, nc)

                    if data[r][c].startswith('S'):
                        weight = ord(data[nr][nc]) - ord('a')
                    elif data[r][c].startswith('E'):
                        weight = ord(data[nr][nc]) - ord('z')
                    else:
                        weight = ord(data[nr][nc]) - ord(data[r][c])

                    # if weight <= 0:
                    #     weight = 1
                    # if weight > 1:
                    #     weight = 9999
                    # weight += 100

                    if weight <= 0:
                        weight = 1
                    if weight > 1:
                        continue

                    # print(f'{label} <--> {nl} weight: {weight}')
                    g.add_edge(label, nl, weight=weight)
        return g

    def solve_part_1(self, data: Any) -> int:
        g = self.build_graph(data)
        print(nx.get_edge_attributes(g, 'weight'))
        print(nx.nodes(g))
        print(nx.dijkstra_path_length(g, 'S-0-0', 'E-2-5', 'weight'))
        path = nx.dijkstra_path(g, source='S-0-0', target='E-2-5', weight='weight')
        print(f'steps: {len(path)}')

        pos = dict()
        for r in range(len(data)):
            for c in range(len(data[r])):
                pos[self.get_label(data, r, c)] = (c, 4 - r)
            #
            # m = n.split('-')
            # pos[n] = (int(m[1]), int(m[2]))

        nx.draw_networkx(g, pos)
        plt.show()
        return path

    def solve_part_2(self, data: Any) -> int:
        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
