# https://adventofcode.com/2024/day/18

from functools import reduce
from operator import add
import os
import time

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

DIRECTION = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def day18_file_read(filename: str) -> list[tuple[int, int]]:
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    return [tuple(int(val) for val in line.split(",")) for line in lines]


def add_tuples(tuples: list[tuple[int, int]]) -> tuple[int, int]:
    return reduce(lambda x, y: tuple(map(add, x, y)), tuples)


def is_pos_in_bounds(grid_size: int, pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] <= grid_size and 0 <= pos[1] <= grid_size


def traverse(
    bytes: list[tuple[int, int]], grid_size: int, simulation_duration: int
) -> int:
    simulated_bytes = set(bytes[:simulation_duration])
    work_list = [((0, 0), 0)]
    visited = set()

    # bfs
    while work_list:
        curr_pos, steps = work_list.pop(0)

        if curr_pos == (grid_size, grid_size):
            return steps

        if curr_pos in visited:
            continue

        visited.add(curr_pos)

        for dir in DIRECTION:
            new_pos = add_tuples([curr_pos, dir])

            if is_pos_in_bounds(grid_size, new_pos) and new_pos not in simulated_bytes:
                work_list.append((new_pos, steps + 1))

    return -1


def day18_part_1(filename: str, grid_size: int = 70, simulation_duration: int = 1024):
    bytes = day18_file_read(filename)
    results = traverse(bytes, grid_size, simulation_duration)

    print(f"Day 18 part 1 {filename} results: {results}")


# brute force...
def find_first_blocked_byte(
    bytes: list[tuple[int, int]], grid_size: int
) -> tuple[int, int] | None:
    for i in range(len(bytes)):
        # progress logging
        # if i % 50 == 0:
        #     print(f"{i}/{len(bytes)}")

        if (min_steps := traverse(bytes, grid_size, i + 1)) == -1:
            return bytes[i]

    return None


def day18_part_2(filename: str, grid_size: int = 70):
    start = time.time()
    bytes = day18_file_read(filename)
    first_blocked_byte = [str(el) for el in find_first_blocked_byte(bytes, grid_size)]

    print(
        f"Day 18 part 2 {filename} results: {",".join(first_blocked_byte)}, {time.time() - start}s"
    )


day18_part_1("sample.txt", 6, 12)
day18_part_1("input.txt")

day18_part_2("sample.txt", 6)
day18_part_2("input.txt")
