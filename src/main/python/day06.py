#!/usr/bin/env python3
"""
Day 6: Something

https://adventofcode.com/2022/day/6
"""
import os.path
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class SignalData:
    value: str

    def start_of_packet_index(self) -> int:
        for i in range(len(self.value) - 4):
            window = self.value[i:i + 4]
            char_count = set(window)
            if len(window) == len(char_count):
                return i + 1
        return -1

    def start_of_message_index(self, start_idx: int) -> int:
        for i in range(start_idx, len(self.value) - 14):
            window = self.value[i:i + 14]
            char_count = set(window)
            if len(window) == len(char_count):
                return i + 1
        return -1


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self) -> list[Any]:
        day = os.path.basename(__file__)[3:5]
        return list(self.get_data(day))

    def solve_part_1(self, data: list[Any]) -> int:
        signalData = SignalData(data[0])
        return signalData.start_of_packet_index() + 3

    def solve_part_2(self, data: list[Any]) -> int:
        signalData = SignalData(data[0])
        start_idx = signalData.start_of_packet_index()
        return signalData.start_of_message_index(start_idx) + 13


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
