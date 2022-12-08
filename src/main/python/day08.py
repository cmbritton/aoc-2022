#!/usr/bin/env python3
"""
Day 8: Treetop Tree House

https://adventofcode.com/2022/day/8
"""
import os.path
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Tree:
    height: int


class Grove:
    trees: list[list[Tree]]

    def __init__(self, data: list[str]):
        self.trees = Grove.build(data)

    def is_visible_from_left(self, row: int, col: int) -> bool:
        result = True
        for c in range(col):
            if self.trees[row][c].height >= self.trees[row][col].height:
                result = False
                break
        return result

    def is_visible_from_right(self, row: int, col: int) -> bool:
        result = True
        for c in range(col + 1, len(self.trees[row])):
            if self.trees[row][c].height >= self.trees[row][col].height:
                result = False
                break
        return result

    def is_visible_from_top(self, row: int, col: int) -> bool:
        result = True
        for r in range(row):
            if self.trees[r][col].height >= self.trees[row][col].height:
                result = False
                break
        return result

    def is_visible_from_bottom(self, row: int, col: int) -> bool:
        result = True
        for r in range(row + 1, len(self.trees)):
            if self.trees[r][col].height >= self.trees[row][col].height:
                result = False
                break
        return result

    def is_tree_visible(self, row: int, col: int) -> bool:
        return self.is_visible_from_top(row, col) or \
            self.is_visible_from_right(row, col) or \
            self.is_visible_from_bottom(row, col) or \
            self.is_visible_from_left(row, col)

    def viewing_distance_left(self, row: int, col: int) -> int:
        result = 0
        for c in range(col - 1, -1, -1):
            result += 1
            if self.trees[row][c].height >= self.trees[row][col].height:
                break
        return result if result > 0 else 1

    def viewing_distance_right(self, row: int, col: int) -> int:
        result = 0
        for c in range(col + 1, len(self.trees[row])):
            result += 1
            if self.trees[row][c].height >= self.trees[row][col].height:
                break
        return result if result > 0 else 1

    def viewing_distance_up(self, row: int, col: int) -> int:
        result = 0
        for r in range(row - 1, -1, -1):
            result += 1
            if self.trees[r][col].height >= self.trees[row][col].height:
                break
        return result if result > 0 else 1

    def viewing_distance_down(self, row: int, col: int) -> int:
        result = 0
        for r in range(row + 1, len(self.trees)):
            result += 1
            if self.trees[r][col].height >= self.trees[row][col].height:
                break
        return result if result > 0 else 1

    def get_scenic_score(self, row: int, col: int) -> int:
        return self.viewing_distance_up(row, col) * \
            self.viewing_distance_right(row, col) * \
            self.viewing_distance_down(row, col) * \
            self.viewing_distance_left(row, col)

    def high_scenic_score(self) -> int:
        result = 0
        for row in range(len(self.trees)):
            for col in range(len(self.trees[row])):
                result = max(result, self.get_scenic_score(row, col))
        return result

    @staticmethod
    def build(data: list[str]) -> list[list[Tree]]:
        trees = []
        for line in data:
            tree_row = []
            for height in list(line):
                tree_row.append(Tree(int(height)))
            trees.append(tree_row)
        return trees


class Solver(AbstractSolver):

    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        return Grove(self.get_data(self.get_day(), data_file_path))

    def solve_part_1(self, grove: Grove) -> int:
        answer = 0
        for row in range(len(grove.trees)):
            for col in range(len(grove.trees[row])):
                if grove.is_tree_visible(row, col):
                    answer += 1
        return answer

    def solve_part_2(self, grove: Grove) -> int:
        answer = 0
        for row in range(len(grove.trees)):
            for col in range(len(grove.trees[row])):
                answer = max(answer, grove.get_scenic_score(row, col))
        return answer

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
