#!/usr/bin/env python3
import os.path

from src.main.python.day05 import Solver


def test_part_1_example():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  'day05-example.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 'CMZ'


def test_part_2_example():
    data_file_path = os.path.join(os.environ.get('TEST_RESOURCES_DIR_PATH'),
                                  'day05-example.data')
    solver = Solver()
    answer = solver.part_2(data_file_path)
    assert answer == 'MCD'


def test_part_1():
    data_file_path = os.path.join(os.environ.get('RESOURCES_DIR_PATH'),
                                  'day05.data')
    solver = Solver()
    answer = solver.part_1(data_file_path)
    assert answer == 'TBVFVDZPN'
