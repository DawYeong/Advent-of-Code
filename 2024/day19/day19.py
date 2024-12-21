# https://adventofcode.com/2024/day/19

import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


def day19_file_read(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as file:
        data = file.read()

    sections = data.split("\n\n")

    return sections[0].split(", "), sections[1].split("\n")


def day19(filename: str):
    towels, target_towels = day19_file_read(filename)
    valid_towels = 0
    arrangements = 0
    cache = dict()

    def towel_arrangements(towels: list[str], curr_towel: str) -> int:
        if not curr_towel:
            return 1

        if curr_towel in cache:
            return cache[curr_towel]

        count = 0
        for towel in towels:
            if curr_towel.startswith(towel):
                count += towel_arrangements(towels, curr_towel[len(towel) :])

        cache[curr_towel] = count

        return count

    for target_towel in target_towels:
        if count := towel_arrangements(towels, target_towel):
            valid_towels += 1
            arrangements += count

    print(f"Day 19 part 1 {filename} results: {valid_towels}")
    print(f"Day 19 part 2 {filename} results: {arrangements}")


day19("sample.txt")
day19("test.txt")
day19("input.txt")
