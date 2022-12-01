#!/usr/bin/env python3
"""
Day 1: Calorie Counting.

https://adventofcode.com/2022/day/1
"""
from dataclasses import dataclass

from src.main.python.util import Timer


@dataclass
class Item:
    """
    A food item.

    Attributes:
        calories: The number of calories this item provides.
    """
    calories: int


@dataclass
class Elf:
    """
    An elf.

    Attributes:
        items: The food Items the elf is carrying.
    """
    items: list[Item]

    def total_calories(self) -> int:
        return sum(x.calories for x in self.items)


@dataclass()
class Solver:
    """
    The main code to solve the puzzle and display the results.
    """

    def __init__(self):
        self.data = None

    @staticmethod
    def init_data() -> list[Elf]:
        """
        Read the puzzle data.

        Returns:
            A list of Elfs and their food.
        """
        elves = []
        items = []
        with open('../resources/day01.data', 'r') as data_file:
            lines = data_file.read().splitlines()
        for line in lines:
            if not line:
                elves.append(Elf(items))
                items = []
                continue
            items.append(Item(int(line)))

        elves.append(Elf(items))

        return elves

    @staticmethod
    def part_1(data: list[Elf]) -> int:
        """
        Find the elf carrying the most calories.

        Parameters:
            data: The list of elves (Elfs).

        Returns:
            The greatest number of calories carried by a single elf.
        """
        data.sort(reverse=True, key=lambda x: x.total_calories())
        return data[0].total_calories()

    @staticmethod
    def part_2(data: list[Elf]) -> int:
        """
        Find the top three elves carrying the most calories.

        Parameters:
            data: The list of elves (Elfs).

        Returns:
            The number of calories carried by the top three elves.
        """
        return sum(x.total_calories() for x in data[:3])

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

    def run(self) -> None:
        """
        Run the puzzle solver.
        """
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = self.part_1(data=data)
        solver_timer.stop()

        self.print_info(part='Part 1', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)

        solver_timer = Timer()
        answer = self.part_2(data=data)
        solver_timer.stop()
        self.print_info(part='Part 2', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
