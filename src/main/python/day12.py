#!/usr/bin/env python3
"""
Day 12: Hill Climbing Algorithm

https://adventofcode.com/2022/day/12
"""
import os.path
from typing import Any

from src.main.python.util import AbstractSolver


class Node:

    def __init__(self, name, location) -> None:
        self.name = name
        self.location = location
        self.nodes = set()

    def __key(self):
        return self.name, self.location

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Node):
            return self.__key() == o.__key()
        return NotImplemented

    def __repr__(self) -> str:
        return f'{self.name} {self.location}'


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

    def build_graph(self, data):
        nodes = []
        for r in range(len(data)):
            for c in range(len(data[0])):
                node = Node(data[r][c], (r, c))
                if node in nodes:
                    node = nodes[nodes.index(node)]
                else:
                    nodes.append(node)
                for nr, nc in self.get_neighbor_indexes(data, r, c):
                    nn = Node(data[nr][nc], (nr, nc))
                    if nn in nodes:
                        nn = nodes[nodes.index(nn)]
                    else:
                        nodes.append(nn)
                    node.nodes.add(nn)
        return nodes

    def get_start(self, nodes):
        for n in nodes:
            if n.name == 'S':
                return n
        return None

    def get_end(self, nodes):
        for n in nodes:
            if n.name == 'E':
                return n
        return None

    def print(self, nodes):
        for n in nodes:
            print(f'{n}')
            for c in n.nodes:
                print(f'\t{c}')

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

    def shortest_path(self, nodes):
        unvisited = set(nodes)
        distance = dict()
        for n in nodes:
            distance[n] = 999999999
        distance[self.get_start(nodes)] = 0

        prev = dict()
        while self.get_end(nodes) in unvisited:
            node = self.get_new_current(unvisited, distance)
            self.visit(node, unvisited, distance, prev)

        return prev

    def solve_part_1(self, data: Any) -> int:
        nodes = self.build_graph(data)
        prev = self.shortest_path(nodes)
        path = []
        node = self.get_end(nodes)
        while node in prev:
            path.append(node)
            node = prev[node]
            if node not in prev:
                path.append(node)

        return len(path) - 1

    def solve_part_2(self, data: Any) -> int:
        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
