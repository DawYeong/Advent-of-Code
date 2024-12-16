# https://adventofcode.com/2024/day/16

from dataclasses import dataclass
from functools import reduce
from heapq import *
import math
from operator import add
import os
from typing import List, Set, Tuple

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


@dataclass
class Graph:
    positions: Set[Tuple[int, int]]
    end: Tuple[int, int]
    start: Tuple[int, int]

    def __init__(self):
        self.positions = set()
        self.end = (-1, -1)
        self.start = (-1, -1)


def day16_file_read(filename: str) -> Graph:
    with open(filename, "r") as file:
        data = file.read()

    lines = [list(line) for line in data.split("\n")]

    graph = Graph()

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == ".":
                graph.positions.add((i, j))
            elif lines[i][j] == "E":
                graph.end = (i, j)
                graph.positions.add((i, j))
            elif lines[i][j] == "S":
                graph.start = (i, j)
                graph.positions.add((i, j))

    return graph


def add_tuples(tuples: List[Tuple[int, int]]) -> Tuple[int, int]:
    return reduce(lambda x, y: tuple(map(add, x, y)), tuples)


def traverse(graph: Graph) -> int:
    queue = [(0, graph.start, 0)]
    visited = {}
    min_score = math.inf

    while queue:
        # print(queue)
        curr_score, pos, curr_dir = heappop(queue)

        # if we have already seen this path => don't compute unless it is less
        if (pos, curr_dir) in visited and visited[(pos, curr_dir)] < curr_score:
            continue

        visited[((pos, curr_dir))] = curr_score

        for i in range(len(DIRECTIONS)):
            # don't traverse backwards
            if i == (curr_dir + 2) % 4:
                continue

            new_pos = add_tuples([pos, DIRECTIONS[i]])

            if new_pos in graph.positions:
                if curr_dir % 4 != i % 4:
                    # turn, but don't move!
                    heappush(queue, (curr_score + 1000, pos, i))
                else:
                    if new_pos == graph.end:
                        min_score = min(min_score, curr_score + 1)
                        continue

                    heappush(queue, (curr_score + 1, new_pos, i))

    return min_score


def day16_part_1(filename: str):
    graph = day16_file_read(filename)
    results = traverse(graph)

    print(f"Day 16 part 1 {filename} results: {results}")


day16_part_1("sample1.txt")
day16_part_1("sample2.txt")
day16_part_1("input.txt")
