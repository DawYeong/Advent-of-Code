# https://adventofcode.com/2024/day/7

import os
import time

WORKING_DIR = os.path.dirname(__file__)


def day7_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")
    raw_calibrations = [line.split(": ") for line in lines]
    calibrations = [
        (int(rc[0]), [int(x) for x in rc[1].split(" ")]) for rc in raw_calibrations
    ]

    return calibrations


def traverse(calibration):
    expected, nums = calibration

    n = len(nums)
    # tuple: curr_result, idx, op
    work_list = [(0, 0, 0)]

    while work_list:
        item = work_list.pop(0)

        next_value = (
            item[0] + nums[item[1]] if item[2] == 0 else item[0] * nums[item[1]]
        )

        if item[1] != n - 1:
            # branch
            work_list.append((next_value, item[1] + 1, 0))
            work_list.append((next_value, item[1] + 1, 1))
        else:
            # check
            if next_value == expected:
                return True

    return False


def day7_part_1(filename):
    calibrations = day7_file_read(filename)

    results = 0
    for calibration in calibrations:
        if traverse(calibration):
            results += calibration[0]

    print(f"Day 7 part 1 {os.path.basename(filename)} results: {results}")


# Much slower as we are adding a lot more paths (exponentially)
def traverse_2(calibration):
    expected, nums = calibration

    n = len(nums)
    # tuple: curr_result, idx, op
    work_list = [(0, 0, 0)]

    while work_list:
        item = work_list.pop(0)

        if item[2] == 0:  # add
            next_value = item[0] + nums[item[1]]
        elif item[2] == 1:  # mul
            next_value = item[0] * nums[item[1]]
        else:  # concat
            next_value = int(str(item[0]) + str(nums[item[1]]))

        if item[1] != n - 1:
            # branch
            work_list.append((next_value, item[1] + 1, 0))
            work_list.append((next_value, item[1] + 1, 1))
            work_list.append((next_value, item[1] + 1, 2))
        else:
            # check
            if next_value == expected:
                return True

    return False


def day7_part_2(filename):
    start_time = time.time()
    calibrations = day7_file_read(filename)

    results = 0
    incorrect_calibrations = []
    for calibration in calibrations:
        if traverse(calibration):
            results += calibration[0]
        else:
            incorrect_calibrations.append(calibration)

    # Slight performance improvement, ~30s improvement on my machine
    # Only traversing || on incorrect calibrations instead of the entire set
    for calibration in incorrect_calibrations:
        if traverse_2(calibration):
            results += calibration[0]

    # for calibration in calibrations:
    #     if traverse_2(calibration):
    #         results += calibration[0]

    print(f"Day 7 part 2 {os.path.basename(filename)} results: {results}")
    print(f"Took {time.time() - start_time}s")


day7_part_1(f"{WORKING_DIR}/sample.txt")
day7_part_1(f"{WORKING_DIR}/input.txt")

day7_part_2(f"{WORKING_DIR}/sample.txt")
day7_part_2(f"{WORKING_DIR}/input.txt")
