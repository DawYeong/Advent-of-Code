# https://adventofcode.com/2024/day/7

import os

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


day7_part_1(f"{WORKING_DIR}/sample.txt")
day7_part_1(f"{WORKING_DIR}/input.txt")
