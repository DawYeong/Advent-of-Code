# https://adventofcode.com/2024/day/10

from collections import defaultdict
import os

WORKING_DIR = os.path.dirname(__file__)

SEARCH_DIR = {
    (-1, 0),  # UP,
    (1, 0),  # DOWN,
    (0, -1),  # LEFT
    (0, 1),  # RIGHT
}


def day10_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return [[int(x) for x in line] for line in data.split("\n")]


def get_starting_points(graph):
    starting_points = []
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 0:
                starting_points.append((i, j))

    return starting_points


def is_point_valid(bound_x, bound_y, point):
    return 0 <= point[0] < bound_y and 0 <= point[1] < bound_x


def add_tuples(tup1, tup2):
    return tuple(map(lambda x, y: x + y, tup1, tup2))


def dfs(graph, starting_point):
    visited = set()
    work_list = [starting_point]
    bound_y = len(graph)
    bound_x = len(graph[0])
    trail_heads = 0

    while work_list:
        item = work_list.pop()
        if item in visited:
            continue

        visited.add(item)

        if graph[item[0]][item[1]] == 9:
            trail_heads += 1
        else:
            for dir in SEARCH_DIR:
                new_pos = add_tuples(item, dir)
                if is_point_valid(bound_x, bound_y, new_pos) and graph[new_pos[0]][
                    new_pos[1]
                ] == (graph[item[0]][item[1]] + 1):
                    work_list.append(new_pos)

    return trail_heads


def day10_part_1(filename):
    graph = day10_file_read(filename)
    starting_points = get_starting_points(graph)

    results = 0
    for starting_point in starting_points:
        results += dfs(graph, starting_point)

    print(f"Day 10 part 1 {os.path.basename(filename)} results: {results}")


def dfs2(graph, starting_point):
    work_list = [starting_point]
    bound_y = len(graph)
    bound_x = len(graph[0])
    trail_heads = 0

    while work_list:
        item = work_list.pop()

        if graph[item[0]][item[1]] == 9:
            trail_heads += 1
        else:
            for dir in SEARCH_DIR:
                new_pos = add_tuples(item, dir)
                if is_point_valid(bound_x, bound_y, new_pos) and graph[new_pos[0]][
                    new_pos[1]
                ] == (graph[item[0]][item[1]] + 1):
                    work_list.append(new_pos)

    return trail_heads


def day10_part_2(filename):
    graph = day10_file_read(filename)
    starting_points = get_starting_points(graph)

    results = 0
    for starting_point in starting_points:
        results += dfs2(graph, starting_point)

    print(f"Day 10 part 2 {os.path.basename(filename)} results: {results}")


day10_part_1(f"{WORKING_DIR}/sample.txt")
day10_part_1(f"{WORKING_DIR}/input.txt")

day10_part_2(f"{WORKING_DIR}/sample.txt")
day10_part_2(f"{WORKING_DIR}/input.txt")
