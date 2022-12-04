#!/usr/bin/env python3
"""
Day 4: Camp Cleanup

https://adventofcode.com/2022/day/4
"""
import os.path
import re
from dataclasses import dataclass
from typing import Any

from src.main.python.util import Timer, print_info


@dataclass
class SectionRange:
    low: int
    high: int

    def contains(self, section_range: 'SectionRange') -> bool:
        return self.low <= section_range.low <= self.high and \
            self.low <= section_range.high <= self.high

    def overlaps(self, section_range: 'SectionRange') -> bool:
        return self.low <= section_range.low <= self.high or \
            self.low <= section_range.high <= self.high


@dataclass
class Pair:
    section_range_1: SectionRange
    section_range_2: SectionRange

    def is_redundant(self):
        return self.section_range_1.contains(self.section_range_2) or \
            self.section_range_2.contains(self.section_range_1)

    def is_overlap(self):
        return self.section_range_1.overlaps(self.section_range_2) or \
            self.section_range_2.overlaps(self.section_range_1)


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
        pattern = r'([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)'
        for line in lines:
            m = re.search(pattern, line)
            min_1 = int(m.group(1))
            max_1 = int(m.group(2))
            min_2 = int(m.group(3))
            max_2 = int(m.group(4))
            data.append(
                Pair(SectionRange(min_1, max_1), SectionRange(min_2, max_2)))

        timer.stop()

        return data, timer

    @staticmethod
    def solve_part_1(data: list[Any]) -> tuple[int, Timer]:
        timer = Timer()
        answer = 0
        for pair in data:
            answer += 1 if pair.is_redundant() else 0
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
        answer = 0
        for pair in data:
            answer += 1 if pair.is_overlap() else 0
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
