# https://adventofcode.com/2024/day/3

from functools import reduce
from operator import mul
import re


def day3_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    # print(data)

    return data


def calculate(str):
    # assume str is of form mul(d+,d+) => will error out anyways
    nums = [int(num) for num in str[4:-1].split(",")]
    return reduce(mul, nums)


def day3_part_1(filename):
    match_reg = r"mul\(\d+,\d+\)"
    data = day3_file_read(filename)

    expressions = re.findall(match_reg, data)

    results = 0
    for exp in expressions:
        results += calculate(exp)

    print(f"Day 3 part 1 {filename} results: {results}")


day3_part_1("sample.txt")
day3_part_1("input.txt")
