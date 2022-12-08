#!/usr/bin/env python3
"""
Day X: Something

https://adventofcode.com/2022/day/8
"""
import os.path
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Tree:
    height: int
    visible: bool
    scenic_score: int


class Grove:
    trees: list[list[Tree]]

    def __init__(self):
        self.trees = []

    def print_visible_tree(self):
        for r in range(len(self.trees)):
            for c in range(len(self.trees[0])):
                print(self.trees[r][c], end='')
                if self.trees[r][c].visible:
                    print('  ', end='')
                else:
                    print(' ', end='')
            print('')


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        grove = Grove()
        for line in data:
            tree_row = []
            for height in list(line):
                tree_row.append(Tree(int(height), True, 0))
            grove.trees.append(tree_row)

        return grove

    def is_visible_from_left(self, grove: Grove, row: int, col: int) -> bool:
        result = True
        for c in range(col):
            if grove.trees[row][c].height >= grove.trees[row][col].height:
                result = False
                break
        return result

    def is_visible_from_right(self, grove: Grove, row: int, col: int) -> bool:
        result = True
        for c in range(col + 1, len(grove.trees[row])):
            if grove.trees[row][c].height >= grove.trees[row][col].height:
                result = False
                break
        return result

    def is_visible_from_top(self, grove: Grove, row: int, col: int) -> bool:
        result = True
        for r in range(row):
            if grove.trees[r][col].height >= grove.trees[row][col].height:
                result = False
                break
        return result

    def is_visible_from_bottom(self, grove: Grove, row: int, col: int) -> bool:
        result = True
        for r in range(row + 1, len(grove.trees)):
            if grove.trees[r][col].height >= grove.trees[row][col].height:
                result = False
                break
        return result

    def is_tree_visible(self, grove: Grove, row: int, col: int) -> bool:
        return self.is_visible_from_top(grove, row, col) or \
            self.is_visible_from_right(grove, row, col) or \
            self.is_visible_from_bottom(grove, row, col) or \
            self.is_visible_from_left(grove, row, col)

    def visible_tree_count(self, grove: Grove):
        result = 0
        for row in range(len(grove.trees)):
            for col in range(len(grove.trees[row])):
                if grove.trees[row][col].visible:
                    result += 1
        return result

    def viewing_distance_left(self, grove: Grove, row: int, col: int) -> int:
        result = 0
        for c in range(col - 1, -1, -1):
            result += 1
            if grove.trees[row][c].height >= grove.trees[row][col].height:
                break
        # print(f'row={row}, col={col}, viewing_distance_left={result}')
        return result

    def viewing_distance_right(self, grove: Grove, row: int, col: int) -> int:
        result = 0
        for c in range(col + 1, len(grove.trees[row])):
            result += 1
            if grove.trees[row][c].height >= grove.trees[row][col].height:
                break
        # print(f'row={row}, col={col}, viewing_distance_right={result}')
        return result

    def viewing_distance_up(self, grove: Grove, row: int, col: int) -> int:
        result = 0
        for r in range(row - 1, -1, -1):
            result += 1
            if grove.trees[r][col].height >= grove.trees[row][col].height:
                break
        # print(f'row={row}, col={col}, viewing_distance_up={result}')
        return result

    def viewing_distance_down(self, grove: Grove, row: int, col: int) -> int:
        result = 0
        for r in range(row + 1, len(grove.trees)):
            result += 1
            if grove.trees[r][col].height >= grove.trees[row][col].height:
                break
        # print(f'row={row}, col={col}, viewing_distance_down={result}')
        return result

    def high_scenic_score(self, grove: Grove) -> int:
        result = 0
        for row in range(len(grove.trees)):
            for col in range(len(grove.trees[row])):
                if grove.trees[row][col].scenic_score > result:
                    result = grove.trees[row][col].scenic_score
        return result

    def solve_part_1(self, grove: Any) -> int:
        for row in range(len(grove.trees)):
            for col in range(len(grove.trees[row])):
                grove.trees[row][col].visible = self.is_tree_visible(grove,
                                                                     row, col)
        return self.visible_tree_count(grove)

    def solve_part_2(self, grove: Any) -> int:
        for row in range(len(grove.trees)):
            for col in range(len(grove.trees[row])):
                up = self.viewing_distance_up(grove, row, col)
                if up == 0:
                    up = 1
                right = self.viewing_distance_right(grove, row, col)
                if right == 0:
                    right = 1
                down = self.viewing_distance_down(grove, row, col)
                if down == 0:
                    down = 1
                left = self.viewing_distance_left(grove, row, col)
                if left == 0:
                    left = 1
                grove.trees[row][col].scenic_score = up * right * down * left
        # grove.print_visible_tree()
        return self.high_scenic_score(grove)

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
