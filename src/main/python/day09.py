#!/usr/bin/env python3
"""
Day X: Something

https://adventofcode.com/2022/day/9
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

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        pattern = r'(.*)'
        my_data = []
        for line in data:
            m = re.search(pattern, line)
            my_data.append(MyData(m.group(1)))

        return my_data

    def solve_part_1(self, data: Any) -> int:
        return 0

    def solve_part_2(self, data: Any) -> int:
        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
