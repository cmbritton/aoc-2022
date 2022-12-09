#!/usr/bin/env python3
"""
Day 9: Rope Bridge

https://adventofcode.com/2022/day/9
"""
import os.path
from typing import Any

from src.main.python.util import AbstractSolver


class Move:
    direction: str
    count: int

    def __init__(self, direction: str, count: int) -> None:
        self.direction = direction
        self.count = count

    def is_up(self):
        return self.direction == 'U'

    def is_down(self):
        return self.direction == 'D'

    def is_left(self):
        return self.direction == 'L'

    def is_right(self):
        return self.direction == 'R'


class Head:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def move(self, move: Move) -> None:
        # print(f'Move H from ({self.x}, {self.y}) to ', end='')
        if move.is_up():
            self.y += move.count
        elif move.is_down():
            self.y -= move.count
        elif move.is_left():
            self.x -= move.count
        elif move.is_right():
            self.x += move.count
        else:
            raise RuntimeError(f'Unknown move: {move}')

        # print(f'({self.x}, {self.y})')

    def is_e(self, tail: 'Tail'):
        return self.x > tail.x and self.y == tail.y

    def is_n(self, tail: 'Tail'):
        return self.x == tail.x and self.y > tail.y

    def is_w(self, tail: 'Tail'):
        return self.x < tail.x and self.y == tail.y

    def is_s(self, tail: 'Tail'):
        return self.x == tail.x and self.y < tail.y

    def is_ne(self, tail: 'Tail'):
        return self.x > tail.x and self.y > tail.y

    def is_nw(self, tail: 'Tail'):
        return self.x < tail.x and self.y > tail.y

    def is_sw(self, tail: 'Tail'):
        return self.x < tail.x and self.y < tail.y

    def is_se(self, tail: 'Tail'):
        return self.x > tail.x and self.y < tail.y


class Tail:
    x: int
    y: int
    visited: set[tuple[int, int]]

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = set()
        self.add_visited((x, y))

    def move(self, head: Head) -> None:
        # print(f'    Move T from ({self.x}, {self.y}) to ', end='')
        if self.is_adjacent_or_same(head):
            # print(f'({self.x}, {self.y}) No move')
            return
        if head.is_e(self):
            self.move_e(head)
        elif head.is_ne(self):
            self.move_ne(head)
        elif head.is_n(self):
            self.move_n(head)
        elif head.is_nw(self):
            self.move_nw(head)
        elif head.is_w(self):
            self.move_w(head)
        elif head.is_sw(self):
            self.move_sw(head)
        elif head.is_s(self):
            self.move_s(head)
        elif head.is_se(self):
            self.move_se(head)
        pass
        # print(f'({self.x}, {self.y})')

    def move_e(self, head: Head):
        for x in range(self.x + 1, head.x):
            self.add_visited((x, self.y))
        self.x = head.x - 1
        self.y = head.y

    def move_ene(self, head: Head):
        for x in range(self.x + 1, head.x):
            self.add_visited((x, head.y))
        self.x = head.x - 1
        self.y = head.y

    def move_ne(self, head: Head):
        if abs(self.y - head.y) == 1:
            self.move_ene(head)
        else:
            self.move_nne(head)

    def move_nne(self, head: Head):
        for y in range(self.y + 1, head.y):
            self.add_visited((head.x, y))
        self.x = head.x
        self.y = head.y - 1

    def move_n(self, head: Head):
        for y in range(self.y + 1, head.y):
            self.add_visited((self.x, y))
        self.x = head.x
        self.y = head.y - 1

    def move_nnw(self, head: Head):
        for y in range(self.y + 1, head.y):
            self.add_visited((head.x, y))
        self.x = head.x
        self.y = head.y - 1

    def move_nw(self, head: Head):
        if abs(self.x - head.x) == 1:
            self.move_nnw(head)
        else:
            self.move_wnw(head)

    def move_wnw(self, head: Head):
        for x in range(self.x - 1, head.x, -1):
            self.add_visited((x, head.y))
        self.x = head.x + 1
        self.y = head.y

    def move_w(self, head: Head):
        for x in range(self.x - 1, head.x, -1):
            self.add_visited((x, self.y))
        self.x = head.x + 1
        self.y = head.y

    def move_wsw(self, head: Head):
        for x in range(self.x - 1, head.x, -1):
            self.add_visited((x, head.y))
        self.x = head.x + 1
        self.y = head.y

    def move_sw(self, head: Head):
        if abs(self.y - head.y) == 1:
            self.move_wsw(head)
        else:
            self.move_ssw(head)

    def move_ssw(self, head: Head):
        for y in range(self.y - 1, head.y, -1):
            self.add_visited((head.x, y))
        self.x = head.x
        self.y = head.y + 1

    def move_s(self, head: Head):
        for y in range(self.y - 1, head.y, - 1):
            self.add_visited((self.x, y))
        self.x = head.x
        self.y = head.y + 1

    def move_sse(self, head: Head):
        for y in range(self.y - 1, head.y, -1):
            self.add_visited((head.x, y))
        self.x = head.x
        self.y = head.y + 1

    def move_se(self, head: Head):
        if abs(self.x - head.x) == 1:
            self.move_sse(head)
        else:
            self.move_ese(head)

    def move_ese(self, head: Head):
        for x in range(self.x + 1, head.x):
            self.add_visited((x, head.y))
        self.x = head.x - 1
        self.y = head.y

    def is_adjacent_or_same(self, head: Head) -> bool:
        return head.x in range(self.x - 1, self.x + 2) and \
            head.y in range(self.y - 1, self.y + 2)
    
    def add_visited(self, xy: tuple[int, int]):
        self.visited.add(xy)
        print(f'added {xy}')


class Solver(AbstractSolver):
    head: Head
    tail: Tail

    def __init__(self) -> None:
        super().__init__()
        self.head = Head(0, 0)
        self.tail = Tail(0, 0)

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        return [Move(x[0], int(x[1])) for x in [a.split() for a in data]]

    def solve_part_1(self, moves: Any) -> int:
        min_x = min_y = max_x = max_y = 0
        for move in moves:
            print(f'\nmoved H {move.direction} {move.count} from ({self.head.x}, {self.head.y}) to ', end='')
            self.head.move(move)
            print(f'({self.head.x}, {self.head.y})')
            x = self.tail.x
            y = self.tail.y
            self.tail.move(self.head)
            print(f'moved T from ({x}, {y}) to ', end='')
            print(f'({self.tail.x}, {self.tail.y})')
            assert self.tail.is_adjacent_or_same(self.head)
            if move.count > 2:
                assert self.tail.x == self.head.x or self.tail.y == self.head.y
            if self.tail.x < min_x:
                min_x = self.tail.x
            if self.tail.x > max_x:
                max_x = self.tail.x
            if self.tail.y < min_y:
                min_y = self.tail.y
            if self.tail.y > max_y:
                max_y = self.tail.y

        # print(f'visited={list(sorted(self.tail.visited))}')
        return len(self.tail.visited)

    def solve_part_2(self, data: Any) -> int:
        return 0

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
