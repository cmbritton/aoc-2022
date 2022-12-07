#!/usr/bin/env python3
"""
Day X: Something

https://adventofcode.com/2022/day/7
"""
import os.path
from dataclasses import dataclass
from typing import Any

from src.main.python.util import AbstractSolver


@dataclass
class Node:
    is_dir: bool
    size_bytes: int
    name: str
    parent: 'Node'
    children: list['Node']

    # def __init__(self) -> None:
    #     self.is_dir = False
    #     self.size_bytes = 0
    #     self.name = ''
    #     self.parent = None
    #     self.children = []

    def is_root(self):
        return self.name == '/'

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def has_child(self, name):
        return self.get_child(name) is not None

    def size_bytes_recursive(self):
        if self.is_dir:
            total = sum([n.size_bytes for n in self.children if not n.is_dir])
            d = [n.size_bytes_recursive() for n in self.children if
                 n.is_dir]
            return sum([n.size_bytes_recursive() for n in self.children if
                        n.is_dir]) + total
        else:
            return self.size_bytes

    def get_directories_recursive(self):
        dirs = []
        for c in self.children:
            if c.is_dir:
                dirs.append(c)
                dirs.extend(c.get_directories_recursive())
        return dirs

    def print(self, indent: int = 0):
        print(f'{" " * 4 * indent}{self.size_bytes}\t{self.name}')
        [x.print(indent + 1) for x in self.children if x.is_dir]
        [x.print(indent + 1) for x in self.children if not x.is_dir]


@dataclass
class Tree:
    root: Node


@dataclass
class Command:
    cmd: str
    arg: str
    output: list[str]

    def is_cd(self):
        return self.cmd == 'cd'

    def is_ls(self):
        return self.cmd == 'ls'


class Solver(AbstractSolver):
    def __init__(self) -> None:
        super().__init__()
        # noinspection PyTypeChecker
        self.root = Node(True, 0, '/', None, [])
        self.cwd = self.root

    def init_data(self, data_file_path: str = None) -> Any:
        data = self.get_data(self.get_day(), data_file_path)
        commands = []
        command = None
        for line in data:
            fields = line.split()
            if fields[0] == '$':
                if command:
                    commands.append(command)
                cmd = fields[1]
                arg = None
                if len(fields) > 2:
                    arg = fields[2]
                command = Command(cmd, arg, [])
            else:
                command.output.append(line)
        commands.append(command)

        return commands

    def build_tree(self, commands):
        for command in commands:
            if command.is_cd():
                if command.arg == '/':
                    self.cwd = self.root
                    continue
                elif command.arg == '..':
                    if not self.cwd.is_root():
                        self.cwd = self.cwd.parent
                    continue
                else:
                    node = self.cwd.get_child(command.arg)
                    if not node:
                        node = Node(True, 0, command.arg, self.cwd, [])
                        self.cwd.children.append(node)
                    self.cwd = node
            elif command.is_ls():
                for line in command.output:
                    fields = line.split()
                    is_dir = fields[0] == 'dir'
                    size_bytes = int(fields[0]) if fields[0] != 'dir' else 0
                    if not self.cwd.has_child(fields[1]):
                        node = Node(is_dir, size_bytes, fields[1], self.cwd,
                                    [])
                        self.cwd.children.append(node)
            else:
                raise RuntimeError(f'Unknown command: {command.cmd}')

    def solve_part_1(self, data: Any) -> int:
        self.build_tree(data)
        answer = 0
        for d in self.root.get_directories_recursive():
            x = d.size_bytes_recursive()
            answer += x if x <= 100000 else 0
        return answer

    def solve_part_2(self, data: Any) -> int:
        self.build_tree(data)
        answer = 0
        total_bytes = 70000000
        bytes_free = total_bytes - self.root.size_bytes_recursive()
        needed_bytes = 30000000
        min_bytes_to_free = needed_bytes - bytes_free

        target_dir = self.root
        possible_dirs = filter(
            lambda x: x.size_bytes_recursive() >= min_bytes_to_free,
            self.root.get_directories_recursive())

        return min([x.size_bytes_recursive() for x in possible_dirs])

    def get_day(self) -> str:
        return os.path.basename(__file__)[3:5]


def main() -> None:
    solver = Solver()
    solver.run()


if __name__ == "__main__":
    main()
