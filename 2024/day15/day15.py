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


def day15_file_read_part_1(filename: str) -> Tuple[Graph, List[str]]:
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
    graph, directions = day15_file_read_part_1(filename)
    traverse(graph, directions)
    results = calculate_gps(graph)

    print(f"Day 15 part 1 {filename} results: {results}")


# practically the same as part 1 but with some minor changes
def day15_file_read_part_2(filename: str) -> Tuple[Graph, List[str]]:
    with open(filename, "r") as file:
        data = file.read()

    sections = data.split("\n\n")

    # build graph
    graph = Graph()

    lines = [list(line) for line in sections[0].split("\n")]

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            # only store left half of box
            new_x_pos = j * 2
            if lines[i][j] == "#":
                graph.walls.add((i, new_x_pos))
            elif lines[i][j] == "O":
                graph.boxes.add((i, new_x_pos))
            elif lines[i][j] == "@":
                # assuming there is a single robot lol
                graph.robot = (i, new_x_pos)

    # get directions
    directions = [dir for line in sections[1].split("\n") for dir in line]

    return graph, directions


# doing this for box sizes of 2, can extend to general case, but I am lazy :>
def check_pos_hit_object(objects: List[Tuple[int, int]], position: Tuple[int, int]):
    hit_boxes = set()
    for obj in objects:
        for i in range(2):
            obj_pos = (obj[0], obj[1] + i)
            if position == obj_pos:
                hit_boxes.add(obj)
                break

    return hit_boxes


# kinda convoluted, this is the consequence of only storing one half of a box
def traverse_2(graph: Graph, directions: List[str]) -> None:
    for dir in directions:
        check_dir = DIRECTIONS[dir]
        next_position = add_tuples([graph.robot, check_dir])

        if len(check_pos_hit_object(graph.walls, next_position)):
            # do not move
            continue
        elif len(check_pos_hit_object(graph.boxes, next_position)):
            # check to see if we can move boxes
            check_positions = set()
            check_positions.add(next_position)
            checked_positions = set()
            is_wall_hit = False
            boxes = set()

            while len(check_positions):
                new_check_positions = set()
                for check_pos in check_positions:
                    if len(check_pos_hit_object(graph.walls, check_pos)):
                        is_wall_hit = True
                        new_check_positions = set()
                        break

                    # this is prevent checking the same spot again
                    # this is the consequence of storing positions of the first half of box
                    checked_positions.add(check_pos)
                    hit_boxes = check_pos_hit_object(graph.boxes, check_pos)
                    boxes = boxes.union(hit_boxes)
                    for hit_box in hit_boxes:
                        # since a box is 2 spaces, we have to check both spaces if a box is moved
                        new_check_positions.add(add_tuples([hit_box, check_dir]))
                        new_check_positions.add(
                            add_tuples([hit_box, check_dir, (0, 1)])
                        )

                check_positions = new_check_positions - checked_positions

            if is_wall_hit:
                # do not move anything
                continue
            else:
                # move robot
                graph.robot = next_position

                # have to shift everything down by one...
                # remove everything first to prevent accidentally removing a box permanently
                for box in boxes:
                    graph.boxes.remove(box)
                for box in boxes:
                    new_box_location = add_tuples([box, check_dir])
                    graph.boxes.add(new_box_location)
        else:
            # move robot to next_position
            graph.robot = next_position


def day15_part_2(filename):
    graph, directions = day15_file_read_part_2(filename)
    traverse_2(graph, directions)
    results = calculate_gps(graph)

    print(f"Day 15 part 2 {filename} results: {results}")


day15_part_1("small_example.txt")
day15_part_1("sample.txt")
day15_part_1("input.txt")

day15_part_2("sample.txt")
day15_part_2("input.txt")
