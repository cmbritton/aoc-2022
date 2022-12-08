#!/usr/bin/env python3
"""
Day 1: Calorie Counting.

https://adventofcode.com/2022/day/1
"""
import os
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Item:
    calories: int


@dataclass
class Elf:
    items: list[Item]

    def total_calories(self) -> int:
        return sum(x.calories for x in self.items)


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        elves = []
        items = []
        for line in data:
            if not line:
                elves.append(Elf(items))
                items = []
                continue
            items.append(Item(int(line)))

        elves.append(Elf(items))

        return elves

    def solve_part_1(self, data: list[Any]) -> Any:
        data.sort(reverse=True, key=lambda x: x.total_calories())
        return data[0].total_calories()

    def solve_part_2(self, data: list[Any]) -> Any:
        data.sort(reverse=True, key=lambda x: x.total_calories())
        return sum(x.total_calories() for x in data[:3])

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
