#!/usr/bin/env python3
"""
Day 4: Camp Cleanup

https://adventofcode.com/2022/day/4
"""
import os.path
import re
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Sections:
    low: int
    high: int

    def contains(self, section_range: 'Sections') -> bool:
        return self.low <= section_range.low <= self.high and \
            self.low <= section_range.high <= self.high

    def overlaps(self, section_range: 'Sections') -> bool:
        return self.low <= section_range.low <= self.high or \
            self.low <= section_range.high <= self.high


@dataclass
class Pair:
    sections_1: Sections
    sections_2: Sections

    def has_redundant(self) -> bool:
        return self.sections_1.contains(self.sections_2) or \
            self.sections_2.contains(self.sections_1)

    def has_overlap(self) -> bool:
        return self.sections_1.overlaps(self.sections_2) or \
            self.sections_2.overlaps(self.sections_1)


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self) -> list[Any]:
        pattern = r'([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)'
        data = []
        day = os.path.basename(__file__)[3:5]
        for line in self.get_data(day):
            m = re.search(pattern, line)
            a, b, c, d = m.group(1, 2, 3, 4)
            data.append(Pair(Sections(int(a), int(b)),
                             Sections(int(c), int(d))))

        return data

    def solve_part_1(self, data: list[Pair]) -> int:
        answer = 0
        for pair in data:
            answer += 1 if pair.has_redundant() else 0
        return answer

    def solve_part_2(self, data: list[Pair]) -> int:
        answer = 0
        for pair in data:
            answer += 1 if pair.has_overlap() else 0
        return answer


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
