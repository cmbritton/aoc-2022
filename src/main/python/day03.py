#!/usr/bin/env python3
"""
Day 3: Rucksack Reorganization

https://adventofcode.com/2022/day/3
"""
import os.path
from dataclasses import dataclass
from functools import reduce
from typing import Any

from src.main.python.util import AbstractSolver

LOWERCASE_OFFSET = ord('`')
UPPERCASE_OFFSET = ord('&')


@dataclass
class Rucksack:
    value: str

    def shared_items(self) -> set:
        return set(self.value[:int(len(self.value) / 2)]) & set(
                self.value[int(len(self.value) / 2):])

    @staticmethod
    def priority(item) -> int:
        offset = LOWERCASE_OFFSET if item.islower() else UPPERCASE_OFFSET
        return ord(item[0]) - offset

    def total_priorities(self) -> int:
        return sum([self.priority(i) for i in self.shared_items()])


@dataclass
class Group:
    value: list[Rucksack]

    def badge_type(self) -> str:
        return str(list(
                set(self.value[0].value) & set(self.value[1].value) & set(
                        self.value[2].value))[0])

    def badge_priority(self) -> int:
        badge_type = self.badge_type()
        offset = LOWERCASE_OFFSET if badge_type.islower() else UPPERCASE_OFFSET
        return ord(badge_type) - offset


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        rucksacks = []
        for line in data:
            rucksacks.append(Rucksack(line.strip()))

        return rucksacks

    @staticmethod
    def get_groups(data: list[Rucksack]):
        return [Group(data[i:i + 3]) for i in range(0, len(data), 3)]

    def solve_part_1(self, data: list[Any]) -> int:
        return reduce(lambda x, y: x + y, [r.total_priorities() for r in data])

    def solve_part_2(self, data: list[Any]) -> int:
        groups = self.get_groups(data)
        return reduce(lambda x, y: x + y, [g.badge_priority() for g in groups])

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
