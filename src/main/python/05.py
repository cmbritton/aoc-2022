#!/usr/bin/env python3
"""
Day 5: Something

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
        qty2 = qty
        # if qty2 > len(self.stacks[dst_stack]):
        #     qty2 = len(self.stacks[dst_stack]) - 1
        # if qty2 < 0:
        #     return
        self.stacks[dst_stack].extend(self.stacks[src_stack][-qty2:])
        del self.stacks[src_stack][-qty2:]
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

    def init_data(self) -> list[Any]:
        day = os.path.basename(__file__)[:-3]
        data = self.get_data(day)

        idx = data.index('')
        stack_data = data[0:idx]
        stack_data.reverse()
        stack_header_data = stack_data[0]
        stack_data = stack_data[1:]
        stack_names = stack_header_data.split()

        move_data = data[idx + 1:]

        # stack_header_pattern = r'^.(.)...(.)...(.).$'
        stack_header_pattern = r'^.(.)...(.)...(.)...(.)...(.)...(.)...(' \
                               r'.)...(.)...(.).$'

        self.cargo = Cargo()
        for line in stack_data:
            m = re.search(stack_header_pattern, line)
            # crates = m.group(1, 2, 3)
            crates = m.group(1, 2, 3, 4, 5, 6, 7, 8, 9)
            for i, crate in enumerate(crates):
                if crate.strip():
                    self.cargo.add_crate(i, crate)

        moves = []
        move_pattern = r'^move (\d*) from (\d*) to (\d*)$'
        for line in move_data:
            m = re.search(move_pattern, line)
            quantity, src_stack, dst_stack = m.group(1, 2, 3)
            moves.append(Move(int(quantity), 
                              int(src_stack) - 1, int(dst_stack) - 1))

        return moves

    def solve_part_1(self, data: list[Any]) -> Any:
        answer = 0
        for move in data:
            self.cargo.move_crates(move.qty, move.src_stack, move.dst_stack)
        return self.cargo.get_top_crates()

    def solve_part_2(self, data: list[Any]) -> Any:
        answer = 0
        for move in data:
            self.cargo.bulk_move_crates(move.qty, move.src_stack, move.dst_stack)
        return self.cargo.get_top_crates()


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
