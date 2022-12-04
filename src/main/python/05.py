#!/usr/bin/env python3
"""
Day 5: Something

https://adventofcode.com/2022/day/5
"""
import os.path
import re
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class MyData:
    value: str


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self) -> list[Any]:
        pattern = r'(.*)'
        data = []
        day = os.path.basename(__file__)[:-3]
        for line in self.get_data(day):
            m = re.search(pattern, line)
            data.append(MyData(m.group(1)))

        return data

    def solve_part_1(self, data: list[Any]) -> int:
        answer = 0
        for d in data:
            answer += 1 if len(d) > 0 else 0
        return answer

    def solve_part_2(self, data: list[Any]) -> int:
        answer = 0
        for d in data:
            answer += 1 if len(d) > 5 else 0
        return answer


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
