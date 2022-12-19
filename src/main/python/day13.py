#!/usr/bin/env python3
"""
Day 13: Distress Signal

https://adventofcode.com/2022/day/13
"""
import os.path
from dataclasses import dataclass
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
            return 'valid'
        elif p1 > p2:
            return 'notvalid'
        else:
            return 'undetermined'

    def compare(self, p1, p2):
        if isinstance(p1, int) and (isinstance(p2, int)):
            return self.compare_int(p1, p2)
        elif isinstance(p1, int) and (isinstance(p2, list)):
            return self.is_valid([p1], p2)
        elif isinstance(p1, list) and (isinstance(p2, int)):
            return self.is_valid(p1, [p2])
        else:
            return self.is_valid(p1, p2)

    def is_valid(self, p1, p2):
        for v1, v2 in zip_longest(p1, p2):
            if v1 is None:
                return 'valid'
            elif v2 is None:
                return 'notvalid'

            result = self.compare(v1, v2)
            if result == 'valid':
                return 'valid'
            elif result == 'notvalid':
                return 'notvalid'
        return 'undetermined'

    def solve_part_1(self, data: Any) -> int:
        indexes = []
        for i, packet_pair in enumerate(data):
            if self.is_valid(packet_pair[0], packet_pair[1]) == 'valid':
                indexes.append(i + 1)
        return sum(indexes)

    def solve_part_2(self, data: Any) -> int:
        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
