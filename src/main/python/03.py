#!/usr/bin/env python3
"""
Day 3: Rucksack Reorganization

https://adventofcode.com/2022/day/3
"""
import os.path
from dataclasses import dataclass
from functools import reduce
from typing import Any

from src.main.python.util import Timer, print_info

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


@dataclass
class Solver:
    def __init__(self) -> None:
        self.data = None

    @staticmethod
    def init_data() -> tuple[list[Any], Timer]:
        timer = Timer()

        rucksacks = []
        day = os.path.basename(__file__)[:-3]
        with open(f'../resources/day{day}.data', 'r') as data_file:
            lines = data_file.read().splitlines()
        for line in lines:
            rucksacks.append(Rucksack(line.strip()))

        timer.stop()

        return rucksacks, timer

    @staticmethod
    def solve_part_1(data: list[Any]) -> tuple[int, Timer]:
        timer = Timer()
        answer = reduce(lambda x, y: x + y,
                        [r.total_priorities() for r in data])
        timer.stop()
        return answer, timer

    def part_1(self) -> None:
        data, init_timer = self.init_data()
        answer, solver_timer = self.solve_part_1(data)
        print_info(part='Part 1', init_timer=init_timer,
                   solver_timer=solver_timer, answer=answer)

        if answer != 8176:
            print('ERROR!')

    @staticmethod
    def get_groups(data: list[Rucksack]):
        return [Group(data[i:i + 3]) for i in range(0, len(data), 3)]

    @staticmethod
    def solve_part_2(groups: list[Any]) -> tuple[int, Timer]:
        timer = Timer()
        answer = reduce(lambda x, y: x + y,
                        [g.badge_priority() for g in groups])
        timer.stop()
        return answer, timer

    def part_2(self) -> None:
        data, init_timer = self.init_data()
        groups = self.get_groups(data)
        answer, solver_timer = self.solve_part_2(groups)

        print_info(part='Part 2', init_timer=init_timer,
                   solver_timer=solver_timer, answer=answer)

        if answer != 2689:
            print('ERROR!')

    def run(self) -> None:
        self.part_1()
        self.part_2()


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
