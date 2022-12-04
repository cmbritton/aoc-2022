import time
from abc import abstractmethod, ABC
from typing import Any


class Timer:
    """
    Track the elapsed time to solve various parts of the puzzle.
    """

    def __init__(self) -> None:
        """
        Create a new Timer and start it.
        """
        self.start_time = time.perf_counter()
        self.end_time = None

    def stop(self) -> None:
        """
        Stop the Timer.
        """
        self.end_time = time.perf_counter()

    def elapsed_time(self) -> str:
        """
        Format a string that represents the elapsed time.

        Scale the elapsed time value to seconds, milliseconds, microseconds,
        or nanoseconds based on the magnitude of the value.

        Returns:
            The string representation of the elapsed time for this Timer.
        """
        if self.end_time is None:
            self.stop()
        t = self.end_time - self.start_time
        unit = 'seconds'
        if t < 1:
            t = t * 1000
            unit = 'milliseconds'
        if t < 1:
            t = t * 1000
            unit = 'microseconds'
        if t < 1:
            t = t * 1000
            unit = 'nanoseconds'

        return f'{t:.2f} {unit}'


class AbstractSolver(ABC):
    def __init__(self) -> None:
        self.data = None

    @abstractmethod
    def init_data(self) -> list[Any]:
        pass

    @abstractmethod
    def solve_part_1(self, data: list[Any]) -> int:
        pass

    @abstractmethod
    def solve_part_2(self, data: list[Any]) -> int:
        pass

    def part_1(self) -> None:
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = self.solve_part_1(data)
        solver_timer.stop()

        self.print_info(part='Part 1', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)

    def part_2(self) -> None:
        init_timer = Timer()
        data = self.init_data()
        init_timer.stop()

        solver_timer = Timer()
        answer = self.solve_part_2(data)
        solver_timer.stop()

        self.print_info(part='Part 2', init_timer=init_timer,
                        solver_timer=solver_timer, answer=answer)

    def run(self) -> None:
        self.part_1()
        self.part_2()

    @staticmethod
    def print_info(part: str, init_timer: Timer,
                   solver_timer: Timer, answer: int) -> None:
        print(f'{part}\n'
              f'\tElapsed Time\n'
              f'\t\t  Init: {init_timer.elapsed_time()}\n'
              f'\t\t   Run: {solver_timer.elapsed_time()}\n'
              f'\t\tAnswer: {answer}')

    @staticmethod
    def get_data(day: str) -> list[str]:
        with open(f'../resources/day{day}.data', 'r') as data_file:
            return data_file.read().splitlines()
