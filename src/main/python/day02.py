#!/usr/bin/env python3
"""
Day 2: Rock Paper Scissors.

https://adventofcode.com/2022/day/2
"""
import os
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Shape:
    value: str

    def is_rock(self) -> bool:
        return self.value == 'A'

    def is_paper(self) -> bool:
        return self.value == 'B'

    def is_scissors(self) -> bool:
        return self.value == 'C'

    def score(self) -> int:
        return ord(self.value) - ord('A') + 1

    def defeats(self) -> 'Shape':
        if self.is_rock():
            return Shape('C')
        elif self.is_paper():
            return Shape('A')
        elif self.is_scissors():
            return Shape('B')
        else:
            raise RuntimeError(f'Unknown shape: {self.value}')

    def loses(self) -> 'Shape':
        if self.is_rock():
            return Shape('B')
        elif self.is_paper():
            return Shape('C')
        elif self.is_scissors():
            return Shape('A')
        else:
            raise RuntimeError(f'Unknown shape: {self.value}')


@dataclass
class Turn:
    your_shape: Shape
    my_shape: Shape

    def i_win(self):
        return self.my_shape.is_rock() and self.your_shape.is_scissors() or \
            self.my_shape.is_paper() and self.your_shape.is_rock() or \
            self.my_shape.is_scissors() and self.your_shape.is_paper()

    def u_win(self):
        return self.your_shape.is_rock() and self.my_shape.is_scissors() or \
            self.your_shape.is_paper() and self.my_shape.is_rock() or \
            self.your_shape.is_scissors() and self.my_shape.is_paper()

    def is_draw(self):
        return not self.i_win() and not self.u_win()

    def i_should_win(self):
        return self.my_shape.value == 'Z'

    def u_should_win(self):
        return self.my_shape.value == 'X'

    def we_should_draw(self):
        return self.my_shape.value == 'Y'

    def your_outcome_score(self):
        if self.u_win():
            return 6
        elif self.i_win():
            return 0
        else:
            return 3

    def my_outcome_score(self):
        if self.i_win():
            return 6
        elif self.u_win():
            return 0
        else:
            return 3

    def your_score(self) -> int:
        return self.your_shape.score() + self.your_outcome_score()

    def my_score(self) -> int:
        return self.my_shape.score() + self.my_outcome_score()

    def score(self) -> tuple[int, int]:
        return self.your_score(), self.my_score()


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self) -> list[Any]:
        data = []
        day = os.path.basename(__file__)[3:5]
        for line in self.get_data(day):
            (your_choice, my_choice) = tuple(line.split())
            data.append(Turn(your_shape=Shape(your_choice),
                             my_shape=Shape(my_choice)))

        return data

    @staticmethod
    def decode_shapes(data: list[Turn]) -> list[Turn]:
        turns = []
        for turn in data:
            new_my_shape = Shape(chr(ord(turn.my_shape.value) - 23))
            turns.append(Turn(turn.your_shape, new_my_shape))
        return turns

    @staticmethod
    def decode_outcomes(data: list[Turn]) -> list[Turn]:
        turns = []
        for turn in data:
            if turn.i_should_win():
                new_my_shape = turn.your_shape.loses()
            elif turn.u_should_win():
                new_my_shape = turn.your_shape.defeats()
            elif turn.we_should_draw():
                new_my_shape = Shape(turn.your_shape.value)
            else:
                raise RuntimeError(f'Unknown shape: {turn.my_shape.value}')
            turns.append(Turn(turn.your_shape, new_my_shape))
        return turns

    @staticmethod
    def play(turns: list[Turn]) -> int:
        your_total = 0
        my_total = 0
        for turn in turns:
            score = turn.score()
            your_total += score[0]
            my_total += score[1]
        return my_total

    def solve_part_1(self, data: list[Any]) -> int:
        return self.play(self.decode_shapes(data))

    def solve_part_2(self, data: list[Any]) -> int:
        return self.play(self.decode_outcomes(data))


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
