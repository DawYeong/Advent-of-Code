# https://adventofcode.com/2024/day/8

from collections import defaultdict
import os

WORKING_DIR = os.path.dirname(__file__)


def day8_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return [list(line) for line in data.split("\n")]


def get_frequencies(graph):
    frequencies = defaultdict(list)

    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] != ".":
                frequencies[graph[i][j]].append((i, j))

    return frequencies


def add_tuples(tup1, tup2):
    return tuple(map(lambda x, y: x + y, tup1, tup2))


def sub_tuples(tup1, tup2):
    return tuple(map(lambda x, y: x - y, tup1, tup2))


def compute_antinodes(pos1, pos2):
    slope = (pos1[0] - pos2[0], pos1[1] - pos2[1])
    antinodes = []

    # using Python 3.7.7, walrus operator introduced in 3.8...
    antinode1 = add_tuples(pos1, slope)
    if antinode1 != pos2:
        antinodes.append(antinode1)
    else:
        antinodes.append(sub_tuples(pos1, slope))

    antinode2 = add_tuples(pos2, slope)
    if antinode2 != pos1:
        antinodes.append(antinode2)
    else:
        antinodes.append(sub_tuples(pos2, slope))

    return antinodes


def check_pos_in_bounds(bound_y, bound_x, pos):
    return 0 <= pos[0] < bound_y and 0 <= pos[1] < bound_x


def get_antinodes(bound_y, bound_x, frequencies):
    antinode_positions = set()
    for positions in frequencies.values():
        if len(positions) < 2:
            continue

        for i in range(len(positions) - 1):
            for j in range(i + 1, len(positions)):
                antinodes = compute_antinodes(positions[i], positions[j])

                for antinode in antinodes:
                    if check_pos_in_bounds(bound_y, bound_x, antinode):
                        antinode_positions.add(antinode)

    return antinode_positions


def day8_part_1(filename):
    graph = day8_file_read(filename)
    frequencies = get_frequencies(graph)

    antinodes = get_antinodes(len(graph), len(graph[0]), frequencies)
    results = len(antinodes)

    print(f"Day 8 part 1 {os.path.basename(filename)} results: {results}")


# add every point on the line (including pos1, pos2) instead of just 2
def compute_antinodes_2(bound_y, bound_x, pos1, pos2):
    slope = (pos1[0] - pos2[0], pos1[1] - pos2[1])
    antinodes = [pos1]

    dir = 0
    curr_pos = pos1
    while dir != 2:
        antinode_pos = (
            add_tuples(curr_pos, slope) if dir == 0 else sub_tuples(curr_pos, slope)
        )

        if not check_pos_in_bounds(bound_y, bound_x, antinode_pos):
            dir += 1
            curr_pos = pos1
            continue

        antinodes.append(antinode_pos)
        curr_pos = antinode_pos

    return antinodes


def get_antinodes_2(bound_y, bound_x, frequencies):
    antinode_positions = set()
    for positions in frequencies.values():
        if len(positions) < 2:
            continue

        for i in range(len(positions) - 1):
            for j in range(i + 1, len(positions)):
                antinodes = compute_antinodes_2(
                    bound_y, bound_x, positions[i], positions[j]
                )
                antinode_positions.update(antinodes)

    return antinode_positions


def day8_part_2(filename):
    graph = day8_file_read(filename)
    frequencies = get_frequencies(graph)

    antinodes = get_antinodes_2(len(graph), len(graph[0]), frequencies)
    results = len(antinodes)

    print(f"Day 8 part 2 {os.path.basename(filename)} results: {results}")


day8_part_1(f"{WORKING_DIR}/sample.txt")
day8_part_1(f"{WORKING_DIR}/input.txt")

day8_part_2(f"{WORKING_DIR}/sample.txt")
day8_part_2(f"{WORKING_DIR}/input.txt")
