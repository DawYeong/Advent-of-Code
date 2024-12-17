# https://adventofcode.com/2024/day/16

from collections import defaultdict
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
    queue = [(0, graph.start, 0, None)]
    visited = {}
    min_score = math.inf
    predecessors = defaultdict(set)
    end_predecessors = set()

    while queue:
        curr_score, pos, curr_dir, prev = heappop(queue)

        # if we have already seen this path => don't compute unless it is less
        if (pos, curr_dir) in visited and visited[(pos, curr_dir)] < curr_score:
            continue

        visited[((pos, curr_dir))] = curr_score
        if prev != None:
            predecessors[(pos, curr_dir)].add(prev)

        for i in range(len(DIRECTIONS)):
            # don't traverse backwards
            if i == (curr_dir + 2) % 4:
                continue

            new_pos = add_tuples([pos, DIRECTIONS[i]])

            if new_pos in graph.positions:
                if curr_dir % 4 != i % 4:
                    # turn, but don't move!
                    heappush(queue, (curr_score + 1000, pos, i, (pos, curr_dir)))
                else:
                    if new_pos == graph.end:
                        if min_score > curr_score + 1:
                            min_score = curr_score + 1
                            end_predecessors.add((pos, curr_dir))
                        continue

                    heappush(queue, (curr_score + 1, new_pos, i, (pos, curr_dir)))

    seats = {graph.end}
    visited_nodes = set()
    pos_list = list(end_predecessors)

    # traverse backwards from end to start to get the nodes on the "best" path
    while pos_list:
        pos = pos_list.pop()

        if pos in visited_nodes:
            continue

        visited_nodes.add(pos)
        seats.add(pos[0])

        pos_list.extend(list(predecessors[pos]))

    return min_score, len(seats)


def day16(filename: str):
    graph = day16_file_read(filename)
    min_score, tiles = traverse(graph)

    print(f"Day 16 part 1 {filename} results: {min_score}")
    print(f"Day 16 part 2 {filename} results: {tiles}")


day16("sample1.txt")
day16("sample2.txt")
day16("input.txt")
