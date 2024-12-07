# https://adventofcode.com/2024/day/6

import os

WORKING_DIR = os.path.dirname(__file__)

DIRECTION = [
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
]


def day6_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    return [list(line) for line in lines]


def find_start(graph):
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == "^":
                return (i, j)

    return (-1, -1)


def check_in_bounds(graph, pos):
    return 0 <= pos[0] < len(graph) and 0 <= pos[1] < len(graph[0])


def traverse(graph, start_pos):
    visited = set()
    curr_pos = start_pos
    dir = 0
    while True:
        visited.add(curr_pos)
        next_pos = tuple(map(sum, zip(curr_pos, DIRECTION[dir])))

        if not check_in_bounds(graph, next_pos):
            break

        if graph[next_pos[0]][next_pos[1]] == "#":
            dir = (dir + 1) % 4
        else:
            curr_pos = next_pos

    return visited


def day6_part_1(filename):
    graph = day6_file_read(filename)

    start_pos = find_start(graph)
    assert start_pos[0] >= 0 and start_pos[1] >= 0

    results = len(traverse(graph, start_pos))

    print(f"Day 6 part 1 {os.path.basename(filename)} results: {results}")


day6_part_1(f"{WORKING_DIR}/sample.txt")
day6_part_1(f"{WORKING_DIR}/input.txt")
