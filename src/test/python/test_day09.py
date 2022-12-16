#!/usr/bin/env python3
import os.path

from src.main.python.day09 import Solver

day = os.path.basename(__file__)[8:10]


def test_part_1_example():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 13


def test_part_1_example_2():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-2.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 36


def test_part_1_example_3():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-3.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 41


def test_part_1_example_lr():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-LR.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 5


def test_part_1_example_lu():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-LU.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_ld():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-LD.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_rl():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-RL.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 5


def test_part_1_example_ru():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-RU.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_rd():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-RD.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_ul():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-UL.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_ur():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-UR.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_ud():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-UD.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 5


def test_part_1_example_dl():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-DL.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_dr():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-DR.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 9


def test_part_1_example_du():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-DU.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 5


def test_part_2_example():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 1


def test_part_2_example_4():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  f'day{day}-example-4.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 36


def test_part_1():
    data_file_path = os.path.join(os.environ.get('RESOURCES_DIR_PATH'),
                                  f'day{day}.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 6271


def test_part_2():
    data_file_path = os.path.join(os.environ.get('RESOURCES_DIR_PATH'),
                                  f'day{day}.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 2458
