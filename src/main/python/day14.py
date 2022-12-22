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

Point = namedtuple('Point', 'x y')
Line = namedtuple('Line', 'p1 p2')


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()
        self.rock_veins = None
        self.sand_points = []
        self.count = 0
        self.sand_history = []
        self.floor = False
        self.max_y = 0

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        rock_veins = []
        for line in data:
            points = line.split(' -> ')
            for p1, p2 in pairwise(points):
                p1x, p1y = p1.split(',')
                p2x, p2y = p2.split(',')
                rock_veins.append(
                    Line(Point(int(p1x), int(p1y)), Point(int(p2x), int(p2y))))

        min_x = 500
        max_x = 500
        min_y = 0
        max_y = 0
        
        for line in rock_veins:
            min_x = min(min_x, line.p1.x)
            min_x = min(min_x, line.p2.x)
            max_x = max(max_x, line.p1.x)
            max_x = max(max_x, line.p2.x)
            
            min_y = min(min_y, line.p1.y)
            min_y = min(min_y, line.p2.y)
            max_y = max(max_y, line.p1.y)
            max_y = max(max_y, line.p2.y)

        # print(f'({min_x}, {min_y}) ({max_x}, {max_y})')
        self.max_y = max_y
        return rock_veins

    def is_occupied_by_sand(self, point):
        return point in self.sand_points

    def is_occupied_by_rock(self, point):
        if self.floor:
            if point.y == self.max_y + 2:
                return True
        for line in self.rock_veins:
            if point.x == line.p1.x == line.p2.x:
                y1 = min(line.p1.y, line.p2.y)
                y2 = max(line.p1.y, line.p2.y)
                if y1 <= point.y <= y2:
                    return True
            elif point.y == line.p1.y == line.p2.y:
                x1 = min(line.p1.x, line.p2.x)
                x2 = max(line.p1.x, line.p2.x)
                if x1 <= point.x <= x2:
                    return True

        return False

    def is_occupied(self, point):
        if self.is_occupied_by_sand(point):
            return True
        return self.is_occupied_by_rock(point)

    def can_drop_left(self, point):
        return not self.is_occupied(Point(point.x - 1, point.y + 1))

    def can_drop_right(self, point):
        return not self.is_occupied(Point(point.x + 1, point.y + 1))

    def can_drop_down(self, point):
        return not self.is_occupied(Point(point.x, point.y + 1))

    def drop(self, point, indent=False):
        # Return True when done
        indentstr = '    ' if indent else ''
        # indentstr = '    ' * indent
        # print(f'{indentstr}{point}')
        # self.sand_history.append(f'{indentstr}{point}')
        if self.can_drop_down(point):
            obstruction = self.next_obstruction(point)
            if obstruction is None:
                return True
            p = Point(point.x, obstruction.y - 1)
            # print(f'\t{indentstr}drops down to {p}')
            # self.sand_history.append(f'\t{indentstr}drops down to {p}')
            result = self.drop(p, True)
            return result
        elif self.can_drop_left(point):
            p = Point(point.x - 1, point.y + 1)
            # print(f'\t{indentstr}rolls left to {p}')
            # self.sand_history.append(f'\t{indentstr}rolls left to {p}')
            result = self.drop(p, True)
            return result
        elif self.can_drop_right(point):
            p = Point(point.x + 1, point.y + 1)
            # print(f'\t{indentstr}rolls right to {p}')
            # self.sand_history.append(f'\t{indentstr}rolls right to {p}')
            result = self.drop(p, True)
            return result
        else:
            # print(f'\t{indentstr}comes to rest at {point}')
            # self.sand_history.append(f'\t{indentstr}comes to rest at {point}')
            if point in self.sand_points:
                # self.print()
                raise RuntimeError(f'Duplicate resting point {point}')
            else:
                self.sand_points.append(point)
            if self.floor and point == (500, 0):
                return True
            else:
                return False

    def next_obstruction(self, point):
        ys = []

        for p in self.sand_points:
            if p.x == point.x:
                ys.append(p.y)

        for line in self.rock_veins:
            x1 = min(line.p1.x, line.p2.x)
            x2 = max(line.p1.x, line.p2.x)
            if x1 <= point.x <= x2:
                ys.append(line.p1.y)
                ys.append(line.p2.y)

        if self.floor:
            ys.append(self.max_y + 2)
        filtered_ys = list(filter(lambda x: x > point.y, ys))
        if len(filtered_ys) == 0:
            return None
        y = min(filtered_ys)
        # print(f'Next obstruction for {point}: ', end='')
        if y == point.y:
            # print('None')
            return None
        else:
            p = Point(point.x, y)
            # print(f'{p}')
            return p

    def print(self, point=None):
        if True:
            return
        indentstr = ''
        if point is not None:
            indentstr += '    '
        for y in range(162):
            print(indentstr, end='')
            for x in range(480, 538):
                p = Point(x, y)
                if p == point:
                    print('O', end='')
                elif self.is_occupied_by_sand(p) and self.is_occupied_by_rock(p):
                    print('X', end='')
                elif self.is_occupied_by_sand(p):
                    if len(self.sand_points) > 1:
                        try:
                            idx = self.sand_points[-26:].index(p)
                            print(chr(65 + idx), end='')
                        except ValueError:
                            print('o', end='')
                        # if p == self.sand_points[-1]:
                        #    print('Z', end='')
                        # else:
                        #     print('o', end='')
                    else:
                        print('o', end='')
                elif self.is_occupied_by_rock(p):
                    print('#', end='')
                else:
                    if x == 500:
                        print('+', end='')
                    else:
                        print('.', end='')
            print('')

    def solve_part_1(self, data: Any) -> int:
        self.rock_veins = data
        done = False
        sand_point = Point(500, 0)
        # self.print()
        while not done:
            self.count += 1
            # print(f'\nnew sand {self.count}')
            prev = len(self.sand_points)
            self.sand_history.clear()
            done = self.drop(sand_point)
            # self.print(self)
            if len(self.sand_points) == prev:
                print(f'Sand not added in iteration {self.count}')
                print('\n'.join(self.sand_history))
                print(self)
        return len(self.sand_points)

    def solve_part_2(self, data: Any) -> int:
        self.rock_veins = data
        self.floor = True
        done = False
        sand_point = Point(500, 0)
        # self.print()
        try:
            while not done:
                self.count += 1
                # print(f'\nnew sand {self.count}')
                prev = len(self.sand_points)
                self.sand_history.clear()
                done = self.drop(sand_point)
                # self.print(self)
                if len(self.sand_points) == prev:
                    print(f'Sand not added in iteration {self.count}')
                    print('\n'.join(self.sand_history))
                    print(self)
        except RecursionError:
            print(f'Recursion error in iteration {self.count}')
            print('\n'.join(self.sand_history))
            print(self)

        return len(self.sand_points)

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
