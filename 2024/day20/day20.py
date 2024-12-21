# https://adventofcode.com/2024/day/20

from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import add
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


DIRECTIONS = {(0, 1), (0, -1), (1, 0), (-1, 0)}


@dataclass
class Graph:
    walls: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]
    standard_time: int
    bound_row: int
    bound_col: int


def day20_file_read(filename: str) -> Graph:
    with open(filename, "r") as file:
        data = file.read()

    lines = [list(line) for line in data.split("\n")]

    walls = set()
    start = None
    end = None
    standard_time = 0
    bound_row = len(lines)
    bound_col = len(lines[0])

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                walls.add((i, j))
                continue

            if lines[i][j] == "S":
                start = (i, j)
                continue
            elif lines[i][j] == "E":
                end = (i, j)

            standard_time += 1

    assert start
    assert end

    return Graph(
        walls=walls,
        start=start,
        end=end,
        standard_time=standard_time,
        bound_row=bound_row,
        bound_col=bound_col,
    )


def add_tuples(tuples: list[tuple[int, int]]) -> tuple[int, int]:
    return reduce(lambda x, y: tuple(map(add, x, y)), tuples)


def traverse(graph: Graph) -> dict[tuple[int, int], int]:
    work_list = [(graph.start, 0)]

    time_map = dict()
    visited = set()

    while work_list:
        curr_pos, curr_time = work_list.pop()

        if curr_pos in visited:
            continue

        visited.add(curr_pos)
        time_map[curr_pos] = curr_time
        new_time = curr_time + 1

        for dir in DIRECTIONS:
            new_pos = add_tuples([curr_pos, dir])

            # no point of checking if new_pos is in bounds because of how the maze is set up
            if new_pos not in graph.walls:
                work_list.append((new_pos, new_time))

    return time_map


def get_manhattan_dist_map(
    positions: list[tuple[int, int]]
) -> dict[tuple[int, int], list[tuple[tuple[int, int], int]]]:
    manhattan_dist_map = defaultdict(list)

    for i in range(len(positions) - 1):
        for j in range(i, len(positions)):
            dist = abs(positions[i][0] - positions[j][0]) + abs(
                positions[i][1] - positions[j][1]
            )
            manhattan_dist_map[positions[i]].append((positions[j], dist))
            manhattan_dist_map[positions[j]].append((positions[i], dist))

    return manhattan_dist_map


def calculate_cheat(
    time_map: dict[tuple[int, int], int],
    dist_map: dict[tuple[int, int], list[tuple[tuple[int, int], int]]],
    min_time_save: int,
    max_cheat_time: int = 2,
):
    time_save_map = defaultdict(int)
    for pos, time in time_map.items():
        pos_in_distance = [el for el in dist_map[pos] if el[1] <= max_cheat_time]
        for new_pos, cheat_time in pos_in_distance:
            time_save = time_map[new_pos] - time - cheat_time
            if time_save >= min_time_save:
                time_save_map[time_save] += 1

    return time_save_map


def day20(filename: str, min_time_save: int = 1):
    graph = day20_file_read(filename)
    time_map = traverse(graph)
    manhattan_dist_map = get_manhattan_dist_map(list(time_map.keys()))
    time_save_map_1 = calculate_cheat(time_map, manhattan_dist_map, min_time_save)
    results_1 = sum(time_save_map_1.values())

    print(f"Day 20 part 1 {filename} results: {results_1}")

    time_save_map_2 = calculate_cheat(time_map, manhattan_dist_map, min_time_save, 20)
    results_2 = sum(time_save_map_2.values())
    print(f"Day 20 part 2 {filename} results: {results_2}")


day20("sample.txt", 50)
day20("input.txt", 100)
