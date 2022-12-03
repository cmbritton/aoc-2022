#!/usr/bin/env python3
"""
Day 3: Rucksack Reorganization

https://adventofcode.com/2022/day/3
"""
from dataclasses import dataclass
from functools import reduce

from src.main.python.util import Timer, print_info

LOWERCASE_OFFSET = ord('`')
UPPERCASE_OFFSET = ord('&')


@dataclass
class Rucksack:
    value: str

    def shared_items(self):
        return set(self.value[:int(len(self.value) / 2)]) & set(
                self.value[int(len(self.value) / 2):])

    @staticmethod
    def priority(item):
        offset = LOWERCASE_OFFSET if item.islower() else UPPERCASE_OFFSET
        return ord(item[0]) - offset

    def total_priorities(self):
        return sum([self.priority(i) for i in self.shared_items()])


@dataclass
class Group:
    value: list[Rucksack]

    def badge_type(self):
        return str(list(
                set(self.value[0].value) & set(self.value[1].value) & set(
                        self.value[2].value))[0])

    def badge_priority(self):
        badge_type = self.badge_type()
        offset = LOWERCASE_OFFSET if badge_type.islower() else UPPERCASE_OFFSET
        return ord(badge_type) - offset


@dataclass
class Solver:
    """
    The main code to solve the puzzle and display the results.
    """

    def __init__(self):
        self.data = None

    @staticmethod
    def init_data() -> list[Rucksack]:
        """
        Read the puzzle data.

        Returns:
            A list of RuckSacks.
        """
        rucksacks = []
        with open('../resources/day03.data', 'r') as data_file:
            lines = data_file.read().splitlines()
        for line in lines:
            rucksacks.append(Rucksack(line.strip()))

        return rucksacks

    def part_1(self) -> None:
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = reduce(lambda x, y: x + y,
                        [r.total_priorities() for r in data])
        solver_timer.stop()

        print_info(part='Part 1', init_timer=init_timer,
                   solver_timer=solver_timer, answer=answer)

        if answer != 8176:
            print('ERROR!')

    @staticmethod
    def get_groups(data):
        return [Group(data[i:i + 3]) for i in range(0, len(data), 3)]

    def part_2(self) -> None:
        init_timer = Timer()
        groups = self.get_groups(self.init_data())
        init_timer.stop()

        solver_timer = Timer()
        answer = reduce(lambda x, y: x + y,
                        [g.badge_priority() for g in groups])
        solver_timer.stop()

        print_info(part='Part 2', init_timer=init_timer,
                   solver_timer=solver_timer, answer=answer)

        if answer != 2689:
            print('ERROR!')

    def run(self) -> None:
        """
        Run the puzzle solver.
        """
        self.part_1()
        self.part_2()


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
