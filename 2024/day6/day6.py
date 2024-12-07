# https://adventofcode.com/2024/day/6

from collections import defaultdict
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


def is_obstacle_valid(graph, start_pos):
    curr_pos = start_pos
    dir = 0
    # keeps track of the amount of times element has hit obstacle
    obstacle_counts = defaultdict(int)
    while True:
        next_pos = tuple(map(sum, zip(curr_pos, DIRECTION[dir])))

        if not check_in_bounds(graph, next_pos):
            break

        if graph[next_pos[0]][next_pos[1]] == "#":
            # this is loop detection, if we hit obstacle a certain amount of times, we can say that there is a loop
            if obstacle_counts[next_pos] < 3:
                obstacle_counts[next_pos] += 1
            else:
                return True
            dir = (dir + 1) % 4
        else:
            curr_pos = next_pos

    return False


# given a graph and visited spots => try to place barrier there and simulate
def valid_obstacles(graph, visited, start_pos):
    num_valid = 0
    for i, pos in enumerate(visited):
        # skip start, can't place one here
        if pos == start_pos:
            continue

        graph[pos[0]][pos[1]] = "#"
        # simulate
        if is_obstacle_valid(graph, start_pos):
            num_valid += 1

        graph[pos[0]][pos[1]] = "."

    return num_valid


def day6_part_2(filename):
    graph = day6_file_read(filename)
    start_pos = find_start(graph)
    assert start_pos[0] >= 0 and start_pos[1] >= 0
    visited = traverse(graph, start_pos)
    results = valid_obstacles(graph, visited, start_pos)

    print(f"Day 6 part 2 {os.path.basename(filename)} results: {results}")


day6_part_1(f"{WORKING_DIR}/sample.txt")
day6_part_1(f"{WORKING_DIR}/input.txt")

day6_part_2(f"{WORKING_DIR}/sample.txt")
day6_part_2(f"{WORKING_DIR}/input.txt")
