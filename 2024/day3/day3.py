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


def day3_part_2(filename):
    data = day3_file_read(filename)

    mul_reg = r"mul\(\d+,\d+\)"
    do_reg = r"do\(\)"
    dont_reg = r"don't\(\)"

    # combine regex
    match_reg = "|".join([mul_reg, do_reg, dont_reg])
    tokens = re.findall(match_reg, data)

    enabled = True
    results = 0
    for token in tokens:
        # not Python 3.10, currently using 3.7.7 no switch statement
        if re.match(do_reg, token):
            enabled = True
        elif re.match(dont_reg, token):
            enabled = False
        elif enabled:
            results += calculate(token)

    print(f"Day 3 part 2 {filename} results: {results}")


day3_part_1("sample.txt")
day3_part_1("input.txt")

day3_part_2("sample2.txt")
day3_part_2("input.txt")
