# https://adventofcode.com/2024/day/19

import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


def day19_file_read(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as file:
        data = file.read()

    sections = data.split("\n\n")

    return sections[0].split(", "), sections[1].split("\n")


def is_towel_valid(towels: list[str], target_towel: str):
    work_list = [""]

    while work_list:
        curr_item = work_list.pop()

        if curr_item == target_towel:
            return True

        left = target_towel[len(curr_item) :]
        for towel in towels:
            if towel == left[: len(towel)]:
                work_list.append(curr_item + towel)

    return False


def day19_part_1(filename: str):
    towels, target_towels = day19_file_read(filename)

    valid_towels = 0
    for target_towel in target_towels:
        if is_towel_valid(towels, target_towel):
            valid_towels += 1

    print(f"Day 19 part 1 {filename} results: {valid_towels}")


day19_part_1("sample.txt")
day19_part_1("input.txt")
