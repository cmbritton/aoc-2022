#!/usr/bin/env python3
"""
Day 15: Beacon Exclusion Zone

https://adventofcode.com/2022/day/15
"""
import os.path
import re
from collections import namedtuple
from functools import reduce, cache
from typing import Any

from src.main.python.util import AbstractSolver

INFINITY = 999999999

Point = namedtuple('Point', 'x y')


class Beacon:

    def __init__(self, location: Point) -> None:
        self.location = location


class Sensor:

    def __init__(self, location: Point, beacon: Beacon = None) -> None:
        self.location = location
        self.beacon = beacon

    @cache
    def beacon_distance(self) -> int:
        return self.taxi_distance(self.beacon.location)

    def taxi_distance(self, p: Point) -> int:
        return abs(self.location.x - p.x) + abs(self.location.y - p.y)

    @cache
    def excluded_x_interval(self, y: int) -> tuple[int, int] | None:
        if (self.beacon_distance() - abs(y - self.location.y)) < 0:
            return None
        x1 = self.location.x - (
                self.beacon_distance() - abs(y - self.location.y))
        x2 = self.location.x + (
                self.beacon_distance() - abs(y - self.location.y))
        return min(x1, x2), max(x1, x2)

    def is_in_exclusion_zone(self, p: Point):
        return self.taxi_distance(p) <= self.beacon_distance()


class Solver(AbstractSolver):
    def __init__(self, row: int = 2000000, max_xy: int = 4000000) -> None:
        super().__init__()
        self.row = row
        self.max_xy = max_xy
        self.min_x = INFINITY
        self.max_x = -INFINITY
        self.min_y = INFINITY
        self.max_y = -INFINITY
        self.beacon_points = []
        self.sensor_points = []

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        pattern = r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is ' \
                  r'at x=([-\d]+), y=([-\d]+)'
        sensors = []
        for line in data:
            m = re.search(pattern, line)

            p1 = Point(int(m.group(3)), int(m.group(4)))
            beacon = Beacon(p1)
            self.beacon_points.append(p1)

            p2 = Point(int(m.group(1)), int(m.group(2)))
            sensors.append(Sensor(p2, beacon))
            self.sensor_points.append(p2)

            self.min_x = min(self.min_x, p1.x, p2.x)
            self.min_y = min(self.min_y, p1.y, p2.y)
            self.max_x = max(self.max_x, p1.x, p2.x)
            self.max_y = max(self.max_y, p1.y, p2.y)

        return sensors

    @staticmethod
    def current_contains_next(current_interval, next_interval):
        return current_interval[0] <= next_interval[0] and \
            current_interval[1] >= next_interval[1]

    @staticmethod
    def next_contains_current(current_interval, next_interval):
        return next_interval[0] <= current_interval[0] and \
            next_interval[1] >= current_interval[1]

    @staticmethod
    def next_extends_current(current_interval, next_interval):
        return next_interval[0] <= current_interval[1] + 1 <= next_interval[1]

    def collapse_intervals(self, excluded_x_intervals):
        if not excluded_x_intervals:
            return []
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
        return collapsed_intervals

    def solve_part_1(self, sensors: Any) -> int:
        excluded_x_intervals = []
        for sensor in sensors:
            interval = sensor.excluded_x_interval(self.row)
            if interval is not None:
                excluded_x_intervals.append(interval)

        collapsed_intervals = self.collapse_intervals(excluded_x_intervals)
        return reduce(lambda a, b: a + (b[1] - b[0]), collapsed_intervals, 0)

    def solve_part_2(self, sensors: Any) -> int:
        collapsed_intervals = dict()
        intervals = []
        y = 0
        for y in range(self.max_xy + 1):
            excluded_x_intervals = []
            for sensor in sensors:
                interval = sensor.excluded_x_interval(y)
                if interval:
                    if interval[0] < 0:
                        interval = 0, interval[1]
                    if interval[1] > self.max_xy:
                        interval = interval[0], self.max_xy
                    excluded_x_intervals.append(interval)

            intervals = self.collapse_intervals(excluded_x_intervals)
            if len(intervals) == 2:
                break

        return ((intervals[0][1] + 1) * 4000000) + y

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
