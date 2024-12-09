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


# rewrite file_read ... data structure is not great, hard to work with
def part_2_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    blocks = [int(el) for el in data]

    filesystem = []
    for idx, block in enumerate(blocks):
        key = None if idx % 2 else idx // 2

        filesystem.append([key, block])

    return filesystem


def part_2_transform(filesystem):
    return [[*value, key] for key, value in filesystem.items()]


def day_9_part_2(filename):
    file_system = part_2_file_read(filename)

    current_block = len(file_system)
    while current_block > 0:
        current_block -= 1
        block = file_system[current_block]

        if block[0] is None:
            # empty block move to next block
            continue

        # find empty block of suitable size
        for i in range(current_block):
            check_block = file_system[i]
            if check_block[0] is not None or check_block[1] < block[1]:
                continue

            # remove from file_system
            if block[1] == check_block[1]:
                # replace block
                file_system[i][0] = block[0]
                file_system[current_block][0] = None
            else:
                file_system[i][1] -= block[1]
                # slot block
                file_system.insert(i, block.copy())
                file_system[current_block + 1][0] = None
            break

    results = 0
    counter = 0
    for block in file_system:
        key = block[0]
        length = block[1]
        if key is None:
            counter += length
        else:
            for _ in range(length):
                results += counter * key
                counter += 1

    print(f"Day 9 part 2 {os.path.basename(filename)} results: {results}")


day9_part_1(f"{WORKING_DIR}/sample.txt")
day9_part_1(f"{WORKING_DIR}/input.txt")

day_9_part_2(f"{WORKING_DIR}/sample.txt")
day_9_part_2(f"{WORKING_DIR}/input.txt")
