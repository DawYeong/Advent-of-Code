# https://adventofcode.com/2024/day/12

import os
from collections import defaultdict

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def day12_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return [list(line) for line in data.split("\n")]


def is_in_bounds(graph, pos):
    return 0 <= pos[0] < len(graph) and 0 <= pos[1] < len(graph[0])


def get_regions(graph):
    regions = defaultdict(list)
    visited = set()

    def get_region(start_pos, key):
        work_list = [start_pos]
        region = []
        while work_list:
            item = work_list.pop()

            if item in visited:
                continue

            visited.add(item)
            region.append(item)

            for dir in DIRECTIONS:
                new_pos = (item[0] + dir[0], item[1] + dir[1])
                if (
                    is_in_bounds(graph, new_pos)
                    and graph[new_pos[0]][new_pos[1]] == key
                ):
                    work_list.append(new_pos)

        return region

    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if (i, j) not in visited:
                # traverse and get region
                regions[graph[i][j]].append(get_region((i, j), graph[i][j]))

    return regions


def calculate_region_cost(graph, region, key):
    perimeter = 0
    for pos in region:
        # check directions:
        for dir in DIRECTIONS:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])

            if not is_in_bounds(graph, new_pos) or graph[new_pos[0]][new_pos[1]] != key:
                perimeter += 1

    return perimeter * len(region)


def day12_part_1(filename):
    graph = day12_file_read(filename)

    key_regions_map = get_regions(graph)

    results = 0
    for key, regions in key_regions_map.items():
        for region in regions:
            results += calculate_region_cost(graph, region, key)

    print(f"Day 12 part 1 {filename} results: {results}")


def graph_item(graph, pos):
    if is_in_bounds(graph, pos):
        return graph[pos[0]][pos[1]]
    else:
        return None


def calculate_region_cost_2(graph, region, key):
    visited = set()

    def traverse(visited_key, key_check):
        # to determine a side => we keep moving horizontally/vertically and checking "below" us
        # this is traversing from the neighbor's POV
        work_list = [visited_key]
        dir = DIRECTIONS[visited_key[2]]
        check_dir = tuple([x * -1 for x in DIRECTIONS[visited_key[2]]])
        MOVE_DIRECTIONS = [(dir[1], dir[0]), (check_dir[1], check_dir[0])]

        while work_list:
            item = work_list.pop()

            if item in visited:
                continue

            visited.add(item)

            for move_dir in MOVE_DIRECTIONS:
                new_pos = (item[0] + move_dir[0], item[1] + move_dir[1])
                check_pos = (new_pos[0] + check_dir[0], new_pos[1] + check_dir[1])

                if (
                    graph_item(graph, check_pos) == key_check
                    and graph_item(graph, new_pos) != key_check
                ):
                    new_item = new_pos + (idx,)
                    work_list.append(new_item)

    sides = 0
    for pos in region:
        # check directions:
        for idx, dir in enumerate(DIRECTIONS):
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])

            if not is_in_bounds(graph, new_pos) or graph[new_pos[0]][new_pos[1]] != key:
                visited_key = new_pos + (idx,)

                if visited_key in visited:
                    continue

                # new side
                sides += 1
                traverse(visited_key, key)

    return sides * len(region)


def day12_part_2(filename):
    graph = day12_file_read(filename)

    key_regions_map = get_regions(graph)

    results = 0
    for key, regions in key_regions_map.items():
        for region in regions:
            results += calculate_region_cost_2(graph, region, key)

    print(f"Day 12 part 2 {filename} results: {results}")


day12_part_1("sample.txt")
day12_part_1("input.txt")

day12_part_2("sample.txt")
day12_part_2("input.txt")
