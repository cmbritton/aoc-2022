#!/usr/bin/env python3
"""
Day 13: Distress Signal

https://adventofcode.com/2022/day/13
"""
import os.path
import re
from dataclasses import dataclass
from functools import cmp_to_key
from itertools import zip_longest
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class MyData:
    value: str


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        packet_pairs = []
        packet_pair = []
        for line in data:
            if not line:
                packet_pairs.append(packet_pair)
                packet_pair = []
                continue
            packet_pair.append(eval(line))

        if packet_pair:
            packet_pairs.append(packet_pair)

        return packet_pairs

    def compare_int(self, p1, p2):
        if p1 < p2:
            return -1
        elif p1 > p2:
            return 1
        else:
            return 0

    def compare(self, p1, p2):
        if isinstance(p1, int) and (isinstance(p2, int)):
            return self.compare_int(p1, p2)
        elif isinstance(p1, int) and (isinstance(p2, list)):
            return self.is_valid([p1], p2)
        elif isinstance(p1, list) and (isinstance(p2, int)):
            return self.is_valid(p1, [p2])
        else:
            return self.is_valid(p1, p2)

    def compare_packets(self, p1, p2):
        if isinstance(p1, int) and (isinstance(p2, int)):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
            else:
                return 0
        elif isinstance(p1, int) and (isinstance(p2, list)):
            return self.is_valid([p1], p2)
        elif isinstance(p1, list) and (isinstance(p2, int)):
            return self.is_valid(p1, [p2])
        else:
            return self.is_valid(p1, p2)

    def is_valid(self, p1, p2):
        for v1, v2 in zip_longest(p1, p2):
            if v1 is None:
                return -1
            elif v2 is None:
                return 1

            result = self.compare(v1, v2)
            if result == -1:
                return -1
            elif result == 1:
                return 1
        return 0

    def solve_part_1(self, data: Any) -> int:
        indexes = []
        for i, packet_pair in enumerate(data):
            if self.is_valid(packet_pair[0], packet_pair[1]) == -1:
                indexes.append(i + 1)
        return sum(indexes)

    def solve_part_2(self, data: Any) -> int:
        packets = []
        for p1, p2 in data:
            packets.append(p1)
            packets.append(p2)

        packets.append([[2]])
        packets.append([[6]])

        packet_map = dict()
        # pattern = r'\[\]'
        for p in packets:
            # m = re.search(pattern, str(p))
            # if m:
            #     key = str(p).replace('[', '').replace(']', '')
            # else:
            #     key = str(p).replace('[', ')').replace(']', '(')
            s = str(p)
            if '[]' in s:
                key = str(p).replace('[', ')').replace(']', '(')
            else:
                key = str(p).replace('[', '').replace(']', '')
            packet_map[key] = p

        sorted_packets = []
        for p in sorted(packets, key=cmp_to_key(self.is_valid)):
        # for k in sorted(packet_map.keys()):
            sorted_packets.append(p)

# 30800 is too high

        x1 = sorted_packets.index([[2]]) + 1
        x2 = sorted_packets.index([[6]]) + 1

        return x1 * x2

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
