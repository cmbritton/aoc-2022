#!/usr/bin/env python3
"""
Day 9: Rope Bridge

https://adventofcode.com/2022/day/9
"""
import os.path
from typing import Any

from src.main.python.util import AbstractSolver


class Move:

    def __init__(self, direction: str, count: int) -> None:
        self.direction = direction
        self.count = count

    def __repr__(self):
        return f'{self.direction} {self.count}'

    def is_up(self):
        return self.direction == 'U'

    def is_down(self):
        return self.direction == 'D'

    def is_left(self):
        return self.direction == 'L'

    def is_right(self):
        return self.direction == 'R'


class Knot:
    last_id: int = 0

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.prev = None
        self.next = None
        self.visited = set()
        self.add_visited((x, y))
        self.id = Knot.last_id
        Knot.last_id += 1

    def __repr__(self):
        return f'id={self.id} ({self.x:>3}, {self.y:>3})'

    def is_head(self):
        return self.prev is None

    def is_tail(self):
        return self.next is None

    def add_knot(self, knot: 'Knot'):
        self.next = knot
        knot.prev = self

    def move(self, move: Move) -> None:
        if move.is_up():
            self._move_up(move.count)
        elif move.is_down():
            self._move_down(move.count)
        elif move.is_left():
            self._move_left(move.count)
        elif move.is_right():
            self._move_right(move.count)
        else:
            raise RuntimeError(f'Unknown move: {move}')

    def _move_up(self, count: int):
        for y in range(self.y + 1, self.y + count + 1):
            self.y += 1
            self.follow()

    def _move_down(self, count: int):
        for y in range(self.y - 1, self.y - count - 1, -1):
            self.y -= 1
            self.follow()

    def _move_right(self, count: int):
        for x in range(self.x + 1, self.x + count + 1):
            self.x += 1
            self.follow()

    def _move_left(self, count: int):
        for x in range(self.x - 1, self.x - count - 1, -1):
            self.x -= 1
            self.follow()

    def is_e_of(self, knot: 'Knot'):
        return self.x > knot.x and self.y == knot.y

    def is_n_of(self, knot: 'Knot'):
        return self.x == knot.x and self.y > knot.y

    def is_w_of(self, knot: 'Knot'):
        return self.x < knot.x and self.y == knot.y

    def is_s_of(self, knot: 'Knot'):
        return self.x == knot.x and self.y < knot.y

    def is_ne_of(self, knot: 'Knot'):
        return self.x > knot.x and self.y > knot.y

    def is_nw_of(self, knot: 'Knot'):
        return self.x < knot.x and self.y > knot.y

    def is_sw_of(self, knot: 'Knot'):
        return self.x < knot.x and self.y < knot.y

    def is_se_of(self, knot: 'Knot'):
        return self.x > knot.x and self.y < knot.y

    def follow(self) -> None:
        if self.is_head():
            self.next.follow()
            return
        if self.is_adjacent_or_same():
            return
        if self.prev.is_e_of(self):
            self._move_e()
        elif self.prev.is_ne_of(self):
            self._move_ne()
        elif self.prev.is_n_of(self):
            self._move_n()
        elif self.prev.is_nw_of(self):
            self._move_nw()
        elif self.prev.is_w_of(self):
            self._move_w()
        elif self.prev.is_sw_of(self):
            self._move_sw()
        elif self.prev.is_s_of(self):
            self._move_s()
        elif self.prev.is_se_of(self):
            self._move_se()

        if not self.is_tail():
            self.next.follow()

    def is_diagonal(self):
        if abs(self.x - self.prev.x) == abs(self.y - self.prev.y):
            return True
        return False

    def _move_e(self):
        self._move_e_near_x()

    def _move_e_near_x(self):
        for x in range(self.x + 1, self.prev.x):
            self.add_visited((x, self.prev.y))
        self.x = self.prev.x - 1
        self.y = self.prev.y

    def _move_ene(self):
        self._move_e_near_x()

    def _move_ne(self):
        if self.is_diagonal():
            self._move_ne_exactly()
        elif abs(abs(self.y) - abs(self.prev.y)) == 1:
            self._move_ene()
        else:
            self._move_nne()

    def _move_ne_exactly(self):
        for x, y in zip(range(self.x + 1, self.prev.x),
                        range(self.y + 1, self.prev.y)):
            self.add_visited((x, y))
        self.x = self.prev.x - 1
        self.y = self.prev.y - 1

    def _move_n_near_y(self):
        for y in range(self.y + 1, self.prev.y):
            self.add_visited((self.prev.x, y))
        self.x = self.prev.x
        self.y = self.prev.y - 1

    def _move_nne(self):
        self._move_n_near_y()

    def _move_n(self):
        self._move_n_near_y()

    def _move_nnw(self):
        self._move_n_near_y()

    def _move_nw(self):
        if self.is_diagonal():
            self._move_nw_exactly()
        elif abs(abs(self.x) - abs(self.prev.x)) == 1:
            self._move_nnw()
        else:
            self._move_wnw()

    def _move_nw_exactly(self):
        for x, y in zip(range(self.x - 1, self.prev.x, -1),
                        range(self.y + 1, self.prev.y)):
            self.add_visited((x, y))
        self.x = self.prev.x + 1
        self.y = self.prev.y - 1

    def _move_w_near_x(self):
        for x in range(self.x - 1, self.prev.x, -1):
            self.add_visited((x, self.prev.y))
        self.x = self.prev.x + 1
        self.y = self.prev.y

    def _move_wnw(self):
        self._move_w_near_x()

    def _move_w(self):
        self._move_w_near_x()

    def _move_wsw(self):
        self._move_w_near_x()

    def _move_sw(self):
        if self.is_diagonal():
            self._move_sw_exactly()
        elif abs(abs(self.y) - abs(self.prev.y)) == 1:
            self._move_wsw()
        else:
            self._move_ssw()

    def _move_sw_exactly(self):
        for x, y in zip(range(self.x - 1, self.prev.x, -1),
                        range(self.y - 1, self.prev.y, -1)):
            self.add_visited((x, y))
        self.x = self.prev.x + 1
        self.y = self.prev.y + 1

    def _move_s_near_y(self):
        for y in range(self.y - 1, self.prev.y, -1):
            self.add_visited((self.prev.x, y))
        self.x = self.prev.x
        self.y = self.prev.y + 1

    def _move_ssw(self):
        self._move_s_near_y()

    def _move_s(self):
        self._move_s_near_y()

    def _move_sse(self):
        self._move_s_near_y()

    def _move_se(self):
        if self.is_diagonal():
            self._move_se_exactly()
        elif abs(abs(self.x) - abs(self.prev.x)) == 1:
            self._move_sse()
        else:
            self._move_ese()

    def _move_se_exactly(self):
        for x, y in zip(range(self.x + 1, self.prev.x),
                        range(self.y - 1, self.prev.y, -1)):
            self.add_visited((x, y))
        self.x = self.prev.x - 1
        self.y = self.prev.y + 1

    def _move_ese(self):
        self._move_e_near_x()

    def is_adjacent_or_same(self) -> bool:
        return self.prev.x in range(self.x - 1, self.x + 2) and \
            self.prev.y in range(self.y - 1, self.y + 2)

    def add_visited(self, xy: tuple[int, int]):
        if self.is_tail():
            self.visited.add(xy)


class Solver(AbstractSolver):

    def __init__(self) -> None:
        super().__init__()
        self.head = None
        self.move = None

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        return [Move(x[0], int(x[1])) for x in [a.split() for a in data]]

    def init_rope(self, knot_count: int):
        self.head = Knot(0, 0)
        for _ in range(1, knot_count):
            knot = Knot(0, 0)
            self.get_tail().add_knot(knot)

    def get_tail(self) -> Knot:
        knot = self.head
        while not knot.is_tail():
            knot = knot.next
        return knot

    def solve_part_1(self, moves: Any) -> int:
        self.init_rope(2)
        for move in moves:
            self.head.move(move)

        return len(self.get_tail().visited)

    def solve_part_2(self, moves: Any) -> int:
        self.init_rope(10)
        for move in moves:
            self.move = move
            self.head.move(move)

        return len(self.get_tail().visited)

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
