# https://adventofcode.com/2024/day/9

from collections import defaultdict
import os

WORKING_DIR = os.path.dirname(__file__)


def day9_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    count = 0
    filesystem = defaultdict(list)
    for i in range(len(data)):
        if i % 2 == 0:
            # file block
            filesystem[count].append(int(data[i]))
        else:
            # space
            filesystem[count].append(int(data[i]))
            count += 1

    filesystem[count].append(0)

    return filesystem


def day9_part_1(filename):
    filesystem = day9_file_read(filename)
    lp = 0
    rp = len(filesystem) - 1

    space_reallocation = [(0, filesystem[0][0])]
    space_left = filesystem[0][1]
    space_required = filesystem[rp][0]
    while lp < rp:
        if space_left < space_required:
            space_required -= space_left
            space_reallocation.append((rp, space_left))
            filesystem[rp][0] -= space_left
            lp += 1
            space_left = filesystem[lp][1]
            space_reallocation.append((lp, filesystem[lp][0]))
        elif space_left > space_required:
            space_left -= space_required
            space_reallocation.append((rp, space_required))
            rp -= 1
            space_required = filesystem[rp][0]
        else:
            space_reallocation.append((rp, space_required))
            rp -= 1
            lp += 1
            space_reallocation.append((lp, filesystem[lp][0]))
            space_left = filesystem[lp][1]
            space_required = filesystem[rp][0]

    results = 0
    idx = 0
    for reallocation in space_reallocation:
        for _ in range(reallocation[1]):
            results += idx * reallocation[0]
            idx += 1

    print(f"Day 9 part 1 {os.path.basename(filename)} results: {results}")


day9_part_1(f"{WORKING_DIR}/sample.txt")
day9_part_1(f"{WORKING_DIR}/input.txt")
