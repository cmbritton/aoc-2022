#!/usr/bin/env python3
"""
Day 12: Hill Climbing Algorithm

https://adventofcode.com/2022/day/12
"""
import os.path
from functools import cache
from typing import Any

from src.main.python.util import AbstractSolver


class Node:

    def __init__(self, name, location) -> None:
        self.name = name
        self.location = location
        self.nodes = set()

class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()
        self.data = None

    def init_data(self, data_file_path: str = None) -> Any:
        return self.get_data(self.get_day(), data_file_path)

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

    def get_distance(self, n1: Node, n2: Node):
        if n1.name == 'S':
            n1v = ord('a')
        elif n1.name == 'E':
            n1v = ord('z')
        else:
            n1v = ord(n1.name)

        if n2.name == 'S':
            n2v = ord('a')
        elif n2.name == 'E':
            n2v = ord('z')
        else:
            n2v = ord(n2.name)

        return n2v - n1v + 30

    @cache
    def build_graph(self):
        nodes = dict()
        for r in range(len(self.data)):
            for c in range(len(self.data[0])):
                if (r, c) in nodes:
                    node = nodes[(r, c)]
                else:
                    node = Node(self.data[r][c], (r, c))
                    nodes[(r, c)] = node

                for nr, nc in self.get_neighbor_indexes(self.data, r, c):
                    if (nr, nc) in nodes:
                        nn = nodes[(nr, nc)]
                    else:
                        nn = Node(self.data[nr][nc], (nr, nc))
                        nodes[(nr, nc)] = nn
                    node.nodes.add(nn)
        return list(nodes.values())

    def get_start(self, nodes):
        for n in nodes:
            if n.name == 'S':
                return n
        return None

    def get_all_starts(self, nodes):
        starts = []
        for n in nodes:
            if n.name == 'a' or n.name == 'S':
                starts.append(n)
        return starts

    def get_end(self, nodes):
        for n in nodes:
            if n.name == 'E':
                return n
        return None

    def visit(self, node: Node, unvisited: set, distance: dict, prev):
        for c in node.nodes:
            if c in unvisited:
                d = self.get_distance(node, c)
                if d - 30 > 1:
                    continue
                d += distance[node]
                if d < distance[c]:
                    distance[c] = d
                    prev[c] = node
        unvisited.remove(node)

    def get_new_current(self, unvisited, distance):
        node = None
        min_dist = 999999999
        for n in unvisited:
            if distance[n] < min_dist:
                min_dist = distance[n]
                node = n
        return node

    def shortest_path(self, nodes, start_node):
        unvisited = set(nodes)
        distance = dict()
        for n in nodes:
            distance[n] = 999999999
        distance[start_node] = 0

        prev = dict()
        while self.get_end(nodes) in unvisited:
            node = self.get_new_current(unvisited, distance)
            if node is None:
                break
            self.visit(node, unvisited, distance, prev)

        return prev

    def get_path(self, nodes, prev):
        path = []
        node = self.get_end(nodes)
        while node in prev:
            path.append(node)
            node = prev[node]
            if node not in prev:
                path.append(node)

        return list(reversed(path))

    def solve_part_1(self, data: Any) -> int:
        # return 0
        self.data = data
        nodes = self.build_graph()
        prev = self.shortest_path(nodes, self.get_start(nodes))
        path = self.get_path(nodes, prev)

        return len(path) - 1

    def solve_part_2(self, data: Any) -> int:
        self.data = data
        min_steps = 999999999
        nodes = self.build_graph()
        start_nodes = self.get_all_starts(nodes)
        for start_node in start_nodes:
            nodes = self.build_graph()
            prev = self.shortest_path(nodes, start_node)
            path = self.get_path(nodes, prev)
            if len(path) > 0:
                if len(path) - 1 < min_steps:
                    min_steps = len(path) - 1

        return min_steps

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
