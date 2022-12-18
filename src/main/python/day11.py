#!/usr/bin/env python3
"""
Day 11: Monkey in the Middle

https://adventofcode.com/2022/day/11

I had to get outside help on this one. I thought I could keep worry levels
at reasonable orders of magnitude for part 2 by managing them as sets of
factors (instead of integer values) using prime factorization. However,
I never got it quite right.

Credit for the total modulo idea goes to
https://github.com/Kokopak/advent2022/blob/master/day11/day11.py
"""

import os.path
import re
from typing import Any

from src.main.python.util import AbstractSolver

total_modulo = 1


class Item:
    last_id = -1

    def __init__(self, worry_level):
        Item.last_id += 1
        self.item_id = Item.last_id
        self.worry_level = worry_level

    def __key(self):
        return self.item_id

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Item):
            return self.__key() == o.__key()
        return NotImplemented

    def __repr__(self) -> str:
        return f'item_id={self.item_id}, worry_level={self.worry_level}'


class Operation:

    def __init__(self, expr):
        self.expr = expr

        def execute(self, old):
            replace = self.expr.replace('old', str(old))
            result = eval(replace)
            return result

        setattr(Operation, 'execute', execute)


class Monkey:
    monkeys: list['Monkey']

    def __init__(self, monkey_id):
        self.monkey_id = monkey_id
        self.items = None
        self.operation = None
        self.test_div = 0
        self.test_true = 0
        self.test_false = 0
        self.inspection_count = 0
        self.deleted_items = []

    def __repr__(self) -> str:
        return f'monkey_id={self.monkey_id}, ' \
               f'operation={self.operation}, ' \
               f'test_div={self.test_div}, ' \
               f'test_true={self.test_true}, ' \
               f'test_false={self.test_false}, ' \
               f'inspection_count={self.inspection_count}, ' \
               f'items={self.items}'

    def inspect_items(self, worry_factor: int):
        self.deleted_items.clear()
        for item in self.items:
            self.inspect_item(item, worry_factor)
        for item in self.deleted_items:
            self.items.remove(item)

    def inspect_item(self, item: Item, worry_factor: int):
        item.worry_level = self.operation.execute(item.worry_level)
        assert item.worry_level

        if worry_factor > 1:
            item.worry_level //= worry_factor

        self.inspection_count += 1
        destination_monkey = self.destination_monkey(item)
        self.throw(item, destination_monkey)

        item.worry_level %= total_modulo

    def destination_monkey(self, item: Item) -> 'Monkey':
        if item.worry_level % self.test_div == 0:
            return self.monkeys[self.test_true]
        else:
            return self.monkeys[self.test_false]

    def throw(self, item: Item, monkey: 'Monkey'):
        monkey.items.append(item)
        self.deleted_items.append(item)


class Solver(AbstractSolver):

    def __init__(self) -> None:
        super().__init__()
        self.monkeys = None

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        monkeys = []
        Monkey.monkeys = monkeys
        monkey = None
        for line in data:
            result = self.parse_line(line)
            if result[0] == 'empty':
                monkeys.append(monkey)
            elif result[0] == 'monkey':
                monkey = Monkey(result[1])
            elif result[0] == 'starting':
                monkey.items = result[1]
            elif result[0] == 'operation':
                monkey.operation = result[1]
            elif result[0] == 'test':
                monkey.test_div = result[1]
                global total_modulo
                total_modulo *= int(monkey.test_div)
            elif result[0] == 'true':
                monkey.test_true = result[1]
            elif result[0] == 'false':
                monkey.test_false = result[1]
            else:
                raise RuntimeError(f'Unable to parse line: {line}')

        monkeys.append(monkey)
        return monkeys

    @staticmethod
    def parse_line(line: str) -> tuple:
        pattern = r'^Monkey (\d):'
        m = re.search(pattern, line)
        if m is not None:
            return 'monkey', int(m.group(1))
        pattern = r'\s+Starting items: (.+)'
        m = re.search(pattern, line)
        if m is not None:
            return 'starting', [Item(int(x)) for x in m.group(1).split(', ')]
        pattern = r'\s+Operation: new = (.+)'
        m = re.search(pattern, line)
        if m is not None:
            return 'operation', Operation(m.group(1))
        pattern = r'\s+Test: divisible by (.+)'
        m = re.search(pattern, line)
        if m is not None:
            return 'test', int(m.group(1))
        pattern = r'\s+If true: throw to monkey (.+)'
        m = re.search(pattern, line)
        if m is not None:
            return 'true', int(m.group(1))
        pattern = r'\s+If false: throw to monkey (.+)'
        m = re.search(pattern, line)
        if m is not None:
            return 'false', int(m.group(1))
        pattern = r'^\s*$'
        m = re.search(pattern, line)
        if m is not None:
            return 'empty',

        raise RuntimeError(f'Cannot parse: {line}')

    def evaluate_round(self, worry_factor: int) -> None:
        for monkey in self.monkeys:
            monkey.inspect_items(worry_factor)

    def solve_part_1(self, monkeys: list[Monkey]) -> int:
        # return 0
        self.monkeys = monkeys
        for _ in range(20):
            self.evaluate_round(3)
        counts = sorted([x.inspection_count for x in self.monkeys],
                        reverse=True)
        return counts[0] * counts[1]

    def solve_part_2(self, monkeys: Any) -> int:
        # return 0
        self.monkeys = monkeys
        for _ in range(10000):
            self.evaluate_round(1)
        c = [x.inspection_count for x in self.monkeys]
        counts = sorted(c,
                        reverse=True)
        return counts[0] * counts[1]

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
