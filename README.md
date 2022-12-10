# [Advent of Code 2022](https://adventofcode.com/2022)

My solutions to Advent of Code (AoC) 2022 puzzles.

Some programmers aim to solve each puzzle in as few lines of code as possible.
Others create really cool animations of puzzle solutions. There are some
extremely skilled people in both camps.

I try to write understandable, maintainable, and extendable object-oriented
code.

## Development Environment

Here's what I use.

### Platform-Independent

* [IntelliJ IDEA](https://www.jetbrains.com/idea/)
* [Python](https://www.python.org/)
* [pipenv](https://pipenv.pypa.io/en/latest/)

### Platform-Specific

* [Windows 10 Pro](https://www.microsoft.com/en-us/software-download/windows10)
* [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) running
  an [Ubuntu 20.04 LTS](https://ubuntu.com/) distribution.

## Setup
Edit the `.env` file to match your environment. Then, run:

    pipenv install

## Run a Daily Puzzle

Run a single puzzle with:

    pipenv run day08.py

## Running Unit Tests

    pipenv run test

## Code Evolution

The logic for each solution is in the `dayxx.init_data`, `dayxx.solve_part_1`,
and `dayxx.solve_part_2` methods. Everything else is common code for reading
puzzle data, testing, outputting results, etc.

Most puzzle solutions follow a pattern you can discern from the commit
messages.

Any commit whose message begins with `WIP` is a work-in-progress checkpoint.
That version may not even work.

Commit messages that look like `Day 8 part 1 works` indicate the revision
that first achieved the correct answer. It might be sloppy. It might be slow.

Messages that contain the word `cleanup` indicate a revision where I removed
commented out lines of code, print statements, etc.

Messages with the word `refactor` mark a revision where I refactored the
original solution to improve readability, performance, or use some language
feature that I was not familiar with enough to use in my initial solution. 

## Results

No answers here! Just elapsed times for each puzzle solution.

|Puzzle|Part 1 Elapsed Time|Part 2 Elapsed Time|
|---|--:|--:|
|[Day 1: Calorie Counting](https://adventofcode.com/2022/1)|1.52 milliseconds|1.01 milliseconds|
|[Day 2: Rock Paper Scissors](https://adventofcode.com/2022/2)|17.54 milliseconds|9.60 milliseconds|
|[Day 3: Rucksack Reorganization](https://adventofcode.com/2022/3)|1.06 milliseconds|695.10 microseconds|
|[Day 4: Camp Cleanup](https://adventofcode.com/2022/4)|3.36 milliseconds|2.18 milliseconds|
|[Day 5: Supply Stacks](https://adventofcode.com/2022/5)|1.65 milliseconds|902.90 microseconds|
|[Day 6: Tuning Trouble](https://adventofcode.com/2022/6)|327.80 microseconds|1.43 milliseconds|
|[Day 7: No Space Left On Device](https://adventofcode.com/2022/7)|1.82 milliseconds|2.13 milliseconds|
|[Day 8: Treetop Tree House](https://adventofcode.com/2022/8)|36.40 milliseconds|31.27 milliseconds|
|[Day 9: Rope Bridge](https://adventofcode.com/2022/9)|36.41 milliseconds|Unsolved|
|[Day 10: Cathode-Ray Tube](https://adventofcode.com/2022/10)|366.30 microseconds|371.90 microseconds|
|Day 11: Unavailable|Unsolved|Unsolved|
|Day 12: Unavailable|Unsolved|Unsolved|
|Day 13: Unavailable|Unsolved|Unsolved|
|Day 14: Unavailable|Unsolved|Unsolved|
|Day 15: Unavailable|Unsolved|Unsolved|
|Day 16: Unavailable|Unsolved|Unsolved|
|Day 17: Unavailable|Unsolved|Unsolved|
|Day 18: Unavailable|Unsolved|Unsolved|
|Day 19: Unavailable|Unsolved|Unsolved|
|Day 20: Unavailable|Unsolved|Unsolved|
|Day 21: Unavailable|Unsolved|Unsolved|
|Day 22: Unavailable|Unsolved|Unsolved|
|Day 23: Unavailable|Unsolved|Unsolved|
|Day 24: Unavailable|Unsolved|Unsolved|
|Day 25: Unavailable|Unsolved|Unsolved|
