#!/usr/bin/env python3
"""
Day 16: Proboscidea Volcanium

https://adventofcode.com/2022/day/16
"""
import copy
import os.path
import re
from collections import defaultdict
from typing import Any

from src.main.python.util import AbstractSolver

MAX_TICKS = 30


class WeightedPath:

    def __init__(self, path: list[str], rate: int) -> None:
        self.path = path
        self.rate = rate


class Valve:

    def __init__(self, name, rate) -> None:
        self.name = name
        self.rate = rate
        self.children = set()
        self.is_open = False

    def __repr__(self) -> str:
        return f'name: {self.name}, rate: {self.rate}'


class Cave:

    def __init__(self) -> None:
        self.valves = dict()

    def add_valve(self, valve: Valve) -> None:
        if valve.name in self.valves:
            raise RuntimeError(f'Valve exists: {valve}')
        self.valves[valve.name] = valve

    def get_valve(self, name: str) -> Valve | None:
        return self.valves[name]

    def path_flow_rate(self, path: list[str]) -> int:
        rate = 0
        for i, name in enumerate(path):
            rate += self.valves[name].rate * (MAX_TICKS - i)
        return rate


class Solver(AbstractSolver):
    IN_ROUTE = 1
    OPENING_VALVE = 2
    IDLE = 3

    def __init__(self) -> None:
        super().__init__()
        self.cave = Cave()
        self.ticks = MAX_TICKS
        self.src_pathmap = dict()
        self.state = Solver.IN_ROUTE
        self.current_path = None
        self.current_valve_name = 'AA'
        self.current_path_index = 0

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        pattern = r'Valve (\S+) has flow rate=(\d+); tunnels? leads? ' \
                  r'to valves? (.+)'
        child_valve_names = dict()
        self.cave.valves.clear()
        for line in data:
            m = re.search(pattern, line)
            name = m.group(1)
            rate = m.group(2)
            self.cave.add_valve(Valve(name, int(rate)))
            child_valve_names[name] = m.group(3).split(', ')

        for name in child_valve_names:
            for child_name in child_valve_names[name]:
                self.cave.get_valve(name).children.add(
                        self.cave.get_valve(child_name))

        return self.cave

    def dfs(self, src: Valve, dst: Valve, visited: defaultdict[str, bool],
            path: list[str], paths: list[WeightedPath]) -> None:
        visited[src.name] = True
        path.append(src.name)
        if src.name == dst.name:
            path_flow_rate = self.cave.path_flow_rate(path)
            paths.append(WeightedPath(copy.deepcopy(path), path_flow_rate))
        else:
            for valve in src.children:
                if not visited[valve.name]:
                    self.dfs(valve, dst, visited, path, paths)

        path.pop()
        visited[src.name] = False

    def get_all_paths_from(self, src_name: str) -> defaultdict:
        dst_pathmap = defaultdict(list[WeightedPath])
        for dst_name in self.cave.valves:
            if dst_name == src_name:
                continue
            path = []
            paths = []
            visited = defaultdict(lambda: False)
            self.dfs(self.cave.get_valve(src_name),
                     self.cave.get_valve(dst_name),
                     visited, path, paths)
            dst_pathmap[dst_name] = paths
        return dst_pathmap

    def init_src_pathmap(self) -> None:
        for src_name in self.cave.valves:
            self.src_pathmap[src_name] = self.get_all_paths_from(src_name)

    def get_best_flow_rate_path(self, src_name: str) -> WeightedPath:
        rate = 0
        path = None
        for dst_name in self.src_pathmap[src_name]:
            if not self.cave.valves[dst_name].is_open:
                for weighted_path in self.src_pathmap[src_name][dst_name]:
                    if weighted_path.rate > rate:
                        path = weighted_path
                        rate = weighted_path.rate
        return path

    def tick_in_route(self) -> None:
        if self.current_path is None:
            self.current_path = self.get_best_flow_rate_path(
                    self.current_valve_name)
            if self.current_path is None:
                return
            self.current_path_index = 0

        self.current_path_index += 1
        self.current_valve_name = self.current_path.path[
            self.current_path_index]
        print(f'You move to valve {self.current_valve_name}')
        if self.current_path_index == len(self.current_path.path) - 1 or \
                not self.cave.valves[self.current_valve_name].is_open and \
                self.cave.valves[self.current_valve_name].rate > 0:
            self.state = Solver.OPENING_VALVE

    def all_valves_open(self) -> bool:
        for valve in self.cave.valves.values():
            if valve.rate > 0 and not valve.is_open:
                return False
        return True

    def tick_opening_valve(self):
        self.cave.valves[self.current_valve_name].is_open = True
        print(f'You open valve {self.current_valve_name}')
        self.current_path = None
        if self.all_valves_open():
            self.state = Solver.IDLE
        else:
            self.state = Solver.IN_ROUTE

    def tick(self) -> None:
        match self.state:
            case Solver.IN_ROUTE:
                self.tick_in_route()
            case Solver.OPENING_VALVE:
                self.tick_opening_valve()
            case Solver.IDLE:
                pass
            case _:
                raise RuntimeError(f'Unknown state: {self.state}')

    def accumulate_flow(self):
        flow = 0
        open_valves = []
        for valve in self.cave.valves.values():
            if valve.is_open:
                flow += valve.rate
                open_valves.append(valve.name)
        print(f'Valves {open_valves} are open, releasing {flow} pressure')
        return flow

    def solve_part_1(self, data: Any) -> int:
        self.init_src_pathmap()
        total_flow = 0
        while self.ticks > 0:
            print(f'\n== Minute {MAX_TICKS - self.ticks + 1} ==')
            total_flow += self.accumulate_flow()
            self.tick()
            self.ticks -= 1

        return total_flow

    def solve_part_2(self, data: Any) -> int:
        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
