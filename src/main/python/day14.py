#!/usr/bin/env python3
"""
Day 14: Regolith Reservoir

https://adventofcode.com/2022/day/14
"""
import os.path
from collections import namedtuple
from itertools import pairwise
from typing import Any

from src.main.python.util import AbstractSolver

INFINITY = 999999

Point = namedtuple('Point', 'x y')
Line = namedtuple('Line', 'p1 p2')


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()
        self.matrix = []

    @staticmethod
    def is_vertical(line: Line) -> bool:
        return line.p1.x == line.p2.x

    def line_to_points(self, line: Line) -> list[Point]:
        if self.is_vertical(line):
            min_y = min(line.p1.y, line.p2.y)
            max_y = max(line.p1.y, line.p2.y)
            return [Point(line.p1.x, y) for y in
                    range(min_y, max_y + 1)]
        else:
            min_x = min(line.p1.x, line.p2.x)
            max_x = max(line.p1.x, line.p2.x)
            return [Point(x, line.p1.y) for x in
                    range(min_x, max_x + 1)]

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        max_x = -INFINITY
        max_y = -INFINITY
        rock_lines = []
        for line in data:
            points = line.split(' -> ')
            for p1, p2 in pairwise(points):
                p1x, p1y = p1.split(',')
                p2x, p2y = p2.split(',')
                max_x = max(max_x, int(p1x), int(p2x))
                max_y = max(max_y, int(p1y), int(p2y))
                rock_lines.append(Line(Point(int(p1x), int(p1y)),
                                       Point(int(p2x), int(p2y))))

        matrix = [['.'] * (max_x * 2) for _ in range(max_y + 1)]
        for line in rock_lines:
            for p in self.line_to_points(line):
                matrix[p.y][p.x] = '#'

        return matrix

    def is_occupied(self, point):
        return self.matrix[point.y][point.x] != '.'

    def is_point_in_bounds(self, point: Point):
        return len(self.matrix[0]) > point.x >= 0 and \
            len(self.matrix) > point.y >= 0

    def can_drop_left(self, point):
        p = Point(point.x - 1, point.y + 1)
        return self.is_point_in_bounds(p) and \
            not self.is_occupied(p)

    def can_drop_right(self, point):
        p = Point(point.x + 1, point.y + 1)
        return self.is_point_in_bounds(p) and \
            not self.is_occupied(p)

    def can_drop_down(self, point):
        p = Point(point.x, point.y + 1)
        return self.is_point_in_bounds(p) and \
            not self.is_occupied(p)

    def drop(self, point):
        # Return True when done
        if self.can_drop_down(point):
            obstruction = self.next_obstruction(point)
            if obstruction is None:
                return True
            return self.drop(Point(point.x, obstruction.y - 1))
        elif self.can_drop_left(point):
            return self.drop(Point(point.x - 1, point.y + 1))
        elif self.can_drop_right(point):
            return self.drop(Point(point.x + 1, point.y + 1))
        else:
            return self.add_sand_at_rest(point)

    def add_sand_at_rest(self, point):
        # Return True when done
        if point.y == len(self.matrix) - 1:
            return True
        self.matrix[point.y][point.x] = 'o'
        if point == (500, 0):
            return True
        else:
            return False

    def next_obstruction(self, point):
        for y in range(point.y, len(self.matrix)):
            if self.matrix[y][point.x] != '.':
                return Point(point.x, y)
        return None

    def sand_count(self):
        count = 0
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                count += 1 if self.matrix[y][x] == 'o' else 0
        return count

    def solve_part_1(self, data: Any) -> int:
        self.matrix = data
        done = False
        sand_point = Point(500, 0)
        while not done:
            done = self.drop(sand_point)
        return self.sand_count()

    def solve_part_2(self, data: Any) -> int:
        self.matrix = data
        self.matrix.append(['.'] * len(self.matrix[-1]))
        self.matrix.append(['#'] * len(self.matrix[-1]))
        done = False
        sand_point = Point(500, 0)
        while not done:
            done = self.drop(sand_point)
        return self.sand_count()

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
