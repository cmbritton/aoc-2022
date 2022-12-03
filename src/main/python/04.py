#!/usr/bin/env python3
"""
Day x:

https://adventofcode.com/2022/day/x
"""
import os.path
from dataclasses import dataclass
from functools import reduce
from typing import Any

from src.main.python.util import Timer, print_info


@dataclass
class SomeData:
    value: str

    def foo(self) -> int:
        return 5


@dataclass
class Solver:
    def __init__(self) -> None:
        self.data = None

    @staticmethod
    def init_data() -> tuple[list[Any], Timer]:
        timer = Timer()

        data = []
        day = os.path.basename(__file__)[:-3]
        with open(f'../resources/day{day}.data', 'r') as data_file:
            lines = data_file.read().splitlines()
        for line in lines:
            data.append(SomeData(line.strip()))

        timer.stop()

        return data, timer

    @staticmethod
    def solve_part_1(data: list[Any]) -> tuple[int, Timer]:
        timer = Timer()
        answer = reduce(lambda x, y: x + y, [r.foo() for r in data])
        timer.stop()
        return answer, timer

    def part_1(self) -> None:
        data, init_timer = self.init_data()
        answer, solver_timer = self.solve_part_1(data)
        print_info(part='Part 1', init_timer=init_timer,
                   solver_timer=solver_timer, answer=answer)

    @staticmethod
    def solve_part_2(data: list[Any]) -> tuple[int, Timer]:
        timer = Timer()
        answer = reduce(lambda x, y: x + y, [r.foo() for r in data])
        timer.stop()
        return answer, timer

    def part_2(self) -> None:
        data, init_timer = self.init_data()
        answer, solver_timer = self.solve_part_2(data)
        print_info(part='Part 2', init_timer=init_timer,
                   solver_timer=solver_timer, answer=answer)

    def run(self) -> None:
        self.part_1()
        self.part_2()


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
