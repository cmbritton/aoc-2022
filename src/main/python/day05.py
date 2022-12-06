#!/usr/bin/env python3
"""
Day 5: Supply Stacks

https://adventofcode.com/2022/day/5
"""
import os.path
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Stack:
    value: list[str]


class Cargo:
    stacks: defaultdict[int, list]

    def __init__(self) -> None:
        self.stacks = defaultdict(list)

    def add_crate(self, stack, crate):
        self.stacks[stack].append(crate)

    def move_crate(self, src_stack, dst_stack):
        self.add_crate(dst_stack, self.stacks[src_stack].pop())

    def move_crates(self, qty, src_stack, dst_stack):
        for i in range(qty):
            self.move_crate(src_stack, dst_stack)

    def bulk_move_crates(self, qty, src_stack, dst_stack):
        self.stacks[dst_stack].extend(self.stacks[src_stack][-qty:])
        del self.stacks[src_stack][-qty:]
        pass

    def get_top_crates(self):
        top_creates = []
        for i in range(len(self.stacks)):
            if self.stacks[i]:
                top_creates.append(self.stacks[i][len(self.stacks[i]) - 1])

        return ''.join(top_creates)


@dataclass
class Move:
    qty: int
    src_stack: int
    dst_stack: int


class Solver(AbstractSolver):
    cargo: Cargo

    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)

        idx = data.index('')
        stack_data = data[0:idx]
        stack_data.reverse()
        stack_data = stack_data[1:]

        move_data = data[idx + 1:]

        stack_header_pattern = r'\s?(\[\S+\]|\s\s\s)\s?'

        self.cargo = Cargo()
        for line in stack_data:
            crates = re.findall(stack_header_pattern, line)
            for i, crate in enumerate(crates):
                if crate.strip():
                    self.cargo.add_crate(i, crate[1])

        moves = []
        move_pattern = r'^move (\d*) from (\d*) to (\d*)$'
        for line in move_data:
            m = re.search(move_pattern, line)
            quantity, src_stack, dst_stack = m.group(1, 2, 3)
            moves.append(Move(int(quantity),
                              int(src_stack) - 1, int(dst_stack) - 1))

        return moves

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]

    def solve_part_1(self, data: list[Any]) -> Any:
        for move in data:
            self.cargo.move_crates(move.qty, move.src_stack, move.dst_stack)
        return self.cargo.get_top_crates()

    def solve_part_2(self, data: list[Any]) -> Any:
        for move in data:
            self.cargo.bulk_move_crates(move.qty, move.src_stack,
                                        move.dst_stack)
        return self.cargo.get_top_crates()


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
