#!/usr/bin/env python3
"""
Day 2: Rock Paper Scissors.

https://adventofcode.com/2022/day/2
"""
from dataclasses import dataclass

from src.main.python.util import Timer


@dataclass
class Shape:
    """
    A shape (rock, paper, or scissors) in the "Rock, Paper, Scissors" game.

    Attributes:
        value: The value for the shape. A = rock, B = paper, C = scissors.
    """
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
    """
    Represents one round (or turn) of the game.

    Attributes:
        your_shape: The opponent's chosen shape for this round.
        my_shape: My chosen shape for this round.
    """
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


@dataclass
class Solver:
    """
    The main code to solve the puzzle and display the results.
    """
    def __init__(self):
        self.data = None

    @staticmethod
    def init_data() -> list[Turn]:
        """
        Read the puzzle data.

        Returns:
            A list of Turns.
        """
        turns = []
        with open('../resources/day02.data', 'r') as data_file:
            lines = data_file.read().splitlines()
        for line in lines:
            (your_choice, my_choice) = tuple(line.split())
            turns.append(Turn(your_shape=Shape(your_choice),
                              my_shape=Shape(my_choice)))

        return turns

    @staticmethod
    def decode_shapes(data: list[Turn]) -> list[Turn]:
        """
        Create a new list of Turns assuming that the encoded strategy guide
        provides shapes to play on each turn.

        X means rock, Y means paper, and Z means scissors.

        Parameters:
            data: The strategy guide that specifies which shape I should
            play in each round.

        Returns:
            A new list of Turns with the shape I should play substituted for
            the encoded values in the strategy guide.
        """
        turns = []
        for turn in data:
            new_my_shape = Shape(chr(ord(turn.my_shape.value) - 23))
            turns.append(Turn(turn.your_shape, new_my_shape))
        return turns

    @staticmethod
    def decode_outcomes(data: list[Turn]) -> list[Turn]:
        """
        Create a new list of Turns assuming that the encoded strategy guide
        provides the desired outcome for each turn.

        X means I should lose, Y means draw, and Z means I should win.

        Parameters:
            data: The strategy guide that specifies which shape I should
            play in each round.

        Returns:
            A new list of Turns with the shape I should play to achieve
            the outcome specified by the encoded values in the strategy guide.
        """
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
        """
        Play the game according to specified list of Turns.

        Evaluate each turn. Determine the winning player and the score
        for both players.

        Parameters:
            turns: The list Turns to evaluate.
        """
        your_total = 0
        my_total = 0
        for turn in turns:
            score = turn.score()
            your_total += score[0]
            my_total += score[1]
        return my_total

    @staticmethod
    def print_info(part: str, init_timer: Timer,
                   solver_timer: Timer, answer: int) -> None:
        """
        Print the answer and elapsed time information for this puzzle.

        Parameters:
            part: Description of puzzle. 'Part 1' or 'Part 2'.
            init_timer: Elapsed time for initialization.
            solver_timer: Elapsed time to solve the puzzle.
            answer: The puzzle answer.
        """
        print(f'{part}\n'
              f'\tElapsed Time\n'
              f'\t\t  Init: {init_timer.elapsed_time()}\n'
              f'\t\t   Run: {solver_timer.elapsed_time()}\n'
              f'\t\tAnswer: {answer}')

    def part_1(self) -> None:
        """
        Play the game assuming X means rock, Y means paper, and Z means
        scissors.

        Read the puzzle data, play the game, and print the results.
        """
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = self.play(self.decode_shapes(data))
        solver_timer.stop()

        self.print_info(part='Part 1', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)

    def part_2(self) -> None:
        """
        Play the game assuming X means I should lose a round, Y means the
        round should be a draw, and Z I should win a round.
        scissors.

        Read the puzzle data, play the game, and print the results.
        """
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = self.play(self.decode_outcomes(data))
        solver_timer.stop()
        self.print_info(part='Part 2', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)

    def run(self) -> None:
        """
        Run the puzzle solver.
        """
        self.part_1()
        self.part_2()


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
