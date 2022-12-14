#!/usr/bin/env python3
"""
Day 10: Cathode-Ray Tube

https://adventofcode.com/2022/day/10
"""
import os.path
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Op:
    # Step is a shorter name for instruction
    op: str
    arg: int

    def __init__(self, args: tuple) -> None:
        self.op = args[0]
        if len(args) > 1:
            self.arg = int(args[1])

    def is_noop(self):
        return self.op == 'noop'

    def is_addx(self):
        return self.op == 'addx'


class Crt:
    ROWS = 6
    COLS = 40

    cycle: int
    pixels: list[list[str]]

    sprite_pos: int

    curr_row: int

    def __init__(self) -> None:
        self.pixels = [['.' for _ in range(Crt.COLS)] for _ in range(Crt.ROWS)]
        self.cycle = 0
        self.sprite_pos = 1
        self.curr_row = -1

    def draw(self, cycle: int, sprite_pos: int):
        self.cycle = cycle
        row = (cycle - 1) // Crt.COLS
        col = (cycle - 1) % Crt.COLS
        if row != self.curr_row:
            self.curr_row = row
            self.sprite_pos = 1
        if col in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            self.pixels[row][col] = '#'

        self.sprite_pos = sprite_pos

    def render(self) -> str:
        return '\n' + '\n'.join([x for x in [''.join(a) for a in self.pixels]])


class Cpu:
    op: Op
    regx: int
    cycle: int
    signal_strengths: list[int]
    crt: Crt

    def __init__(self) -> None:
        self.regx = 1
        self.cycle = 0
        self.signal_strengths = []
        self.crt = Crt()

    def set_step(self, op: Op) -> None:
        self.op = op

    def execute(self):
        if self.op.op == 'noop':
            self.execute_noop()
        elif self.op.op == 'addx':
            self.execute_addx()
        else:
            raise RuntimeError(f'Unknown op: {self.op}')

    def execute_noop(self):
        self.tick()
        self.update_signal_strength()

    def execute_addx(self):
        self.tick()
        self.update_signal_strength()

        self.tick()
        self.update_signal_strength()
        self.regx += self.op.arg

    def tick(self):
        self.cycle += 1
        self.crt.draw(self.cycle, self.regx)

    def update_signal_strength(self):
        if self.cycle == 20 or ((self.cycle - 20) % 40) == 0:
            self.signal_strengths.append(self.regx * self.cycle)


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        d = self.get_data(self.get_day(), data_file_path)
        return [Op(tuple(x)) for x in [a.split() for a in d]]

    def solve_part_1(self, ops: Any) -> int:
        cpu = Cpu()
        for op in ops:
            cpu.set_step(op)
            cpu.execute()
        return sum(cpu.signal_strengths)

    def solve_part_2(self, ops: Any) -> Any:
        cpu = Cpu()
        for op in ops:
            cpu.set_step(op)
            cpu.execute()
        return cpu.crt.render()

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
