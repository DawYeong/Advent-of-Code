# https://adventofcode.com/2024/day/15

from dataclasses import dataclass
from functools import reduce
from typing import List, Set, Tuple
from operator import add
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

DIRECTIONS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


@dataclass
class Graph:
    walls: Set[Tuple[int, int]]
    robot: Tuple[int, int]
    boxes: Set[Tuple[int, int]]

    def __init__(self):
        self.walls = set()
        self.boxes = set()
        self.robot = (-1, -1)


def day15_file_read(filename: str) -> Tuple[Graph, List[str]]:
    with open(filename, "r") as file:
        data = file.read()

    sections = data.split("\n\n")

    # build graph
    graph = Graph()

    lines = [list(line) for line in sections[0].split("\n")]

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                graph.walls.add((i, j))
            elif lines[i][j] == "O":
                graph.boxes.add((i, j))
            elif lines[i][j] == "@":
                # assuming there is a single robot lol
                graph.robot = (i, j)

    # get directions
    directions = [dir for line in sections[1].split("\n") for dir in line]

    return graph, directions


def add_tuples(tuples: List[Tuple[int, int]]) -> Tuple[int, int]:
    return reduce(lambda x, y: tuple(map(add, x, y)), tuples)


def traverse(graph: Graph, directions: List[str]) -> None:
    for dir in directions:
        check_dir = DIRECTIONS[dir]
        next_position = add_tuples([graph.robot, check_dir])

        if next_position in graph.walls:
            # do not move
            continue
        elif next_position in graph.boxes:
            # check to see if we can move boxes
            curr_box_check_pos = next_position
            while curr_box_check_pos in graph.boxes:
                curr_box_check_pos = add_tuples([curr_box_check_pos, check_dir])

            if curr_box_check_pos in graph.walls:
                # do not move anything
                continue
            else:
                # move robot
                graph.robot = next_position
                # move boxes => move first box to curr_box_check_pos
                graph.boxes.remove(next_position)
                graph.boxes.add(curr_box_check_pos)
        else:
            # move robot to next_position
            graph.robot = next_position


def calculate_gps(graph: Graph) -> int:
    gps = 0
    for box in graph.boxes:
        gps += box[0] * 100 + box[1]

    return gps


def day15_part_1(filename):
    graph, directions = day15_file_read(filename)
    traverse(graph, directions)
    results = calculate_gps(graph)

    print(f"Day 15 part 1 {filename} results: {results}")


day15_part_1("small_example.txt")
day15_part_1("sample.txt")
day15_part_1("input.txt")
