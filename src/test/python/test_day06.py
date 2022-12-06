#!/usr/bin/env python3
import os.path

from src.main.python.day06 import Solver


day = os.path.basename(__file__)[8:10]


def test_part_1_example():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 7


def test_part_1_example_2():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-2.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 5


def test_part_1_example_3():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-3.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 6


def test_part_1_example_4():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-4.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 10


def test_part_1_example_5():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-5.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 11


def test_part_2_example():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 19


def test_part_2_example_2():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-2.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 23


def test_part_2_example_3():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-3.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 23


def test_part_2_example_4():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-4.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 29


def test_part_2_example_5():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-5.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 26


def test_part_1():
    data_file_path = os.path.join(os.environ.get('RESOURCES_DIR_PATH'),
                                  f'day{day}.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 1093


def test_part_2():
    data_file_path = os.path.join(os.environ.get('RESOURCES_DIR_PATH'),
                                  f'day{day}.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 3534
