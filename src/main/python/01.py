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

    def init_data(self) -> list[Any]:
        data = []
        items = []
        day = os.path.basename(__file__)[:-3]
        for line in self.get_data(day):
            if not line:
                data.append(Elf(items))
                items = []
                continue
            items.append(Item(int(line)))

        data.append(Elf(items))

        return data

    def solve_part_1(self, data: list[Any]) -> int:
        data.sort(reverse=True, key=lambda x: x.total_calories())
        return data[0].total_calories()

    def solve_part_2(self, data: list[Any]) -> int:
        data.sort(reverse=True, key=lambda x: x.total_calories())
        return sum(x.total_calories() for x in data[:3])


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
