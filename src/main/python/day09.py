#!/usr/bin/env python3
"""
Day 9: Rope Bridge

https://adventofcode.com/2022/day/9
"""
import os.path
from typing import Any

from src.main.python.util import AbstractSolver


step = 0


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
            solver.plot_points()

    def _move_down(self, count: int):
        for y in range(self.y - 1, self.y - count - 1, -1):
            self.y -= 1
            self.follow()
            solver.plot_points()

    def _move_right(self, count: int):
        for x in range(self.x + 1, self.x + count + 1):
            self.x += 1
            self.follow()
            solver.plot_points()

    def _move_left(self, count: int):
        for x in range(self.x - 1, self.x - count - 1, -1):
            self.x -= 1
            self.follow()
            solver.plot_points()

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
            # print(f'({self.x:>3}, {self.y:>3})')
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
        # if self.is_head() and self.next.is_tail() or \
        #         self.is_tail() and self.prev.is_head():
        #     return False
        if abs(self.x - self.prev.x) == abs(self.y - self.prev.y):
            return True
        return False

    def _move_e(self):
        for x in range(self.x + 1, self.prev.x):
            self.add_visited((x, self.prev.y))
        self.x = self.prev.x - 1
        self.y = self.prev.y
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_e')

    def _move_ene(self):
        for x in range(self.x + 1, self.prev.x):
            self.add_visited((x, self.prev.y))
        self.x = self.prev.x - 1
        self.y = self.prev.y
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_ene')

    def _move_ne(self):
        if self.is_diagonal():
            self._move_ne_exactly()
        elif abs(abs(self.y) - abs(self.prev.y)) == 1:
            self._move_ene()
        else:
            self._move_nne()

    def _move_ne_exactly(self):
        for x, y in zip(range(self.x + 1, self.prev.x), range(self.y + 1, self.prev.y)):
            self.add_visited((x, y))
        self.x = self.prev.x - 1
        self.y = self.prev.y - 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_ne_exactly')

    def _move_nne(self):
        for y in range(self.y + 1, self.prev.y):
            self.add_visited((self.prev.x, y))
        self.x = self.prev.x
        self.y = self.prev.y - 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_nne')

    def _move_n(self):
        for y in range(self.y + 1, self.prev.y):
            self.add_visited((self.x, y))
        self.x = self.prev.x
        self.y = self.prev.y - 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_n')

    def _move_nnw(self):
        for y in range(self.y + 1, self.prev.y):
            self.add_visited((self.prev.x, y))
        self.x = self.prev.x
        self.y = self.prev.y - 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_nnw')

    def _move_nw(self):
        if self.is_diagonal():
            self._move_nw_exactly()
        elif abs(abs(self.x) - abs(self.prev.x)) == 1:
            self._move_nnw()
        else:
            self._move_wnw()

    def _move_nw_exactly(self):
        for x, y in zip(range(self.x - 1, self.prev.x, -1), range(self.y + 1, self.prev.y)):
            self.add_visited((x, y))
        self.x = self.prev.x + 1
        self.y = self.prev.y - 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_nw_exactly')

    def _move_wnw(self):
        for x in range(self.x - 1, self.prev.x, -1):
            self.add_visited((x, self.prev.y))
        self.x = self.prev.x + 1
        self.y = self.prev.y
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_wnw')

    def _move_w(self):
        for x in range(self.x - 1, self.prev.x, -1):
            self.add_visited((x, self.y))
        self.x = self.prev.x + 1
        self.y = self.prev.y
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_w')

    def _move_wsw(self):
        # if self.id == 9:
        #     print(f'self: {self.x, self.y}, prev: {self.prev.x, self.prev.y}')
        for x in range(self.x - 1, self.prev.x, -1):
            self.add_visited((x, self.prev.y))
            # if self.id == 9:
            #     print(f'\tloop adds {(x, self.prev.y)}')
        self.x = self.prev.x + 1
        self.y = self.prev.y
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_wsw')
        self.add_visited((self.x, self.y))

    def _move_sw(self):
        if self.is_diagonal():
            self._move_sw_exactly()
        elif abs(abs(self.y) - abs(self.prev.y)) == 1:
            self._move_wsw()
        else:
            self._move_ssw()

    def _move_sw_exactly(self):
        for x, y in zip(range(self.x - 1, self.prev.x, -1), range(self.y - 1, self.prev.y, -1)):
            self.add_visited((x, y))
        self.x = self.prev.x + 1
        self.y = self.prev.y + 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_sw_exactly')

    def _move_ssw(self):
        for y in range(self.y - 1, self.prev.y, -1):
            self.add_visited((self.prev.x, y))
        self.x = self.prev.x
        self.y = self.prev.y + 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_ssw')

    def _move_s(self):
        for y in range(self.y - 1, self.prev.y, - 1):
            self.add_visited((self.x, y))
        self.x = self.prev.x
        self.y = self.prev.y + 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_s')

    def _move_sse(self):
        for y in range(self.y - 1, self.prev.y, -1):
            self.add_visited((self.prev.x, y))
        self.x = self.prev.x
        self.y = self.prev.y + 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_sse')

    def _move_se(self):
        if self.is_diagonal():
            self._move_se_exactly()
        elif abs(abs(self.x) - abs(self.prev.x)) == 1:
            self._move_sse()
        else:
            self._move_ese()

    def _move_se_exactly(self):
        for x, y in zip(range(self.x + 1, self.prev.x), range(self.y - 1, self.prev.y, -1)):
            self.add_visited((x, y))
        self.x = self.prev.x - 1
        self.y = self.prev.y + 1
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_se_exactly')

    def _move_ese(self):
        for x in range(self.x + 1, self.prev.x):
            self.add_visited((x, self.prev.y))
        self.x = self.prev.x - 1
        self.y = self.prev.y
        if self.id == 9 and (self.x, self.y) not in self.visited:
            print(f'missed visit {(self.x, self.y)} in _move_ese')

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

    def get_points(self):
        points = []
        knot = self.head
        while knot is not None:
            points.append((knot.x, knot.y))
            knot = knot.next
        return points

    def plot_points(self):
        global step
        if step < 408 or step > 0:
            return
        print(f'Move {self.move}')

        for y in range(20, -21, -1):
            for x in range(-20, 21):
                c = '\t'
                # if x == 0 and y == 0:
                #     c = '+ '
                # elif x == 0:
                #     c = '| '
                # elif y == 0:
                #     c = '- '
                # else:
                #     c = '. '
                knot = self.head
                while knot is not None:
                    if (x, y) == (0, 0):
                        c = '(0, 0)'
                    elif (x, y) == (knot.x, knot.y):
                        c = f'id={knot.id} {(knot.x, knot.y)}\t'
                        # if knot.is_head():
                        #     c = 'H '
                        # elif knot.is_tail():
                        #     c = 'T '
                        # else:
                        #     c = f'{str(knot.id)} '
                        break
                    # elif (x, y) in tail.visited:
                    #     c = '# '
                    knot = knot.next
                print(c, end='')
            print('')
        print('')
        pass

    def plot_rope(self):
        self.plot_points()
        print('')

    def print_rope(self):
        knot = self.head
        while knot is not None:
            print(f'{knot}, ', end='')
            knot = knot.next
        print('')

    def solve_part_1(self, moves: Any) -> int:
        # return 0
        global solver
        solver = self
        self.init_rope(2)
        for move in moves:
            self.head.move(move)

        return len(self.get_tail().visited)

    # 2448 is too low
    # 2504 is wrong
    # 2505 is wrong
    # 2506 is wrong
    # 2510 is wrong
    # 2520 is too high
    # 2531 is wrong
    # 2557 is too high
    def solve_part_2(self, moves: Any) -> int:
        global solver, step
        solver = self
        Knot.last_id = 0
        self.init_rope(10)
        for move in moves:
            self.move = move
            step += 1
            # print(move)
            self.head.move(move)
            self.head.follow()
            # self.plot_rope()
            # self.print_rope()
            # print(self.get_tail().visited)

        return len(self.get_tail().visited)

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


solver = None


def main() -> None:
    global solver
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
