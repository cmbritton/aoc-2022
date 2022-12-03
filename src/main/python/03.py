#!/usr/bin/env python3
"""
Day 3: Rucksack Reorganization

https://adventofcode.com/2022/day/3
"""
from dataclasses import dataclass

from src.main.python.util import Timer


@dataclass
class Rucksack:
    value: str

    def compartment_1_item_types(self):
        return self.value[:int(len(self.value) / 2)]

    def compartment_2_item_types(self):
        return self.value[int(len(self.value) / 2):]

    def shared_items(self):
        return set(self.compartment_1_item_types()) & set(
            self.compartment_2_item_types())

    def item_priority(self, item):
        if item.islower():
            return ord(item[0]) - 96
        else:
            return ord(item[0]) - 38

    def total_priorities(self):
        total = 0
        l = len(self.value)
        for item in self.shared_items():
            c1 = self.compartment_1_item_types()
            l1 = len(c1)
            c2 = self.compartment_2_item_types()
            l2 = len(c2)
            s = self.shared_items()
            total += self.item_priority(item)
        return total


# 7619 is wrong
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

    @staticmethod
    def print_info(part: str, init_timer: Timer,
                   solver_timer: Timer, answer: int) -> None:
        """
        Print the answer and elapsed time information for this puzzle.

        Parameters:
            part: Description of puzzle. 'Part 1' or 'Part 2'.
            init_timer: Elapsed time for initialization.
            solver_timer: Elapsed time to solve the puzzle.
            answer: The puzzle answer.
        """
        print(f'{part}\n'
              f'\tElapsed Time\n'
              f'\t\t  Init: {init_timer.elapsed_time()}\n'
              f'\t\t   Run: {solver_timer.elapsed_time()}\n'
              f'\t\tAnswer: {answer}')

    def part_1(self) -> None:
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = 0
        for rucksack in data:
            answer += rucksack.total_priorities()
        solver_timer.stop()

        self.print_info(part='Part 1', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)

    def part_2(self) -> None:
        pass

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
