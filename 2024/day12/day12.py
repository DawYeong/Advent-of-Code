# https://adventofcode.com/2024/day/12

from collections import defaultdict


DIRECTIONS = {(-1, 0), (1, 0), (0, -1), (0, 1)}


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


day12_part_1("sample.txt")
day12_part_1("input.txt")
