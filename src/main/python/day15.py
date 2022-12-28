#!/usr/bin/env python3
"""
Day 15: Beacon Exclusion Zone

https://adventofcode.com/2022/day/15
"""
import os.path
import re
from functools import reduce
from typing import Any

from src.main.python.util import AbstractSolver


class Beacon:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'x: {self.x}, y: {self.y}'


class Sensor:

    def __init__(self, x: int, y: int, beacon: Beacon = None) -> None:
        self.x = x
        self.y = y
        self.beacon = beacon

    def __repr__(self) -> str:
        return f'x: {self.x}, y: {self.y}, beacon: {self.beacon}'

    def beacon_distance(self) -> int:
        return abs(self.x - self.beacon.x) + abs(self.y - self.beacon.y)

    def excluded_x_interval(self, y: int) -> tuple[int, int] | None:
        if (self.beacon_distance() - abs(y - self.y)) < 0:
            return None
        x1 = self.x - (self.beacon_distance() - abs(y - self.y))
        x2 = self.x + (self.beacon_distance() - abs(y - self.y))
        return min(x1, x2), max(x1, x2)


class Solver(AbstractSolver):
    def __init__(self, row: int = 2000000, max_xy: int = 0) -> None:
        super().__init__()
        self.row = row

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        pattern = r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is ' \
                  r'at x=([-\d]+), y=([-\d]+)'
        sensors = []
        for line in data:
            m = re.search(pattern, line)
            beacon = Beacon(int(m.group(3)), int(m.group(4)))
            sensors.append(Sensor(int(m.group(1)), int(m.group(2)), beacon))

        return sensors

    def current_contains_next(self, current_interval, next_interval):
        return current_interval[0] <= next_interval[0] and \
            current_interval[1] >= next_interval[1]

    def next_contains_current(self, current_interval, next_interval):
        return next_interval[0] <= current_interval[0] and \
            next_interval[1] >= current_interval[1]

    def next_extends_current(self, current_interval, next_interval):
        return next_interval[0] <= current_interval[1] <= next_interval[1]

    # 6180329 is too high
    def solve_part_1(self, sensors: Any) -> int:
        excluded_x_intervals = []
        for sensor in sensors:
            interval = sensor.excluded_x_interval(self.row)
            if interval is not None:
                excluded_x_intervals.append(interval)

        collapsed_intervals = []
        ordered_excluded_intervals = sorted(excluded_x_intervals)
        current_interval = ordered_excluded_intervals[0]
        for next_interval in ordered_excluded_intervals[1:]:
            if self.current_contains_next(current_interval, next_interval):
                continue
            elif self.next_contains_current(current_interval, next_interval):
                current_interval = next_interval
                continue
            elif self.next_extends_current(current_interval, next_interval):
                current_interval = current_interval[0], next_interval[1]
            else:
                collapsed_intervals.append(current_interval)
                current_interval = next_interval
        collapsed_intervals.append(current_interval)
        return reduce(lambda a, b: a + (b[1] - b[0]), collapsed_intervals, 0)

    def solve_part_2(self, sensors: Any) -> int:

        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
