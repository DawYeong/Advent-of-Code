# https://adventofcode.com/2024/day/13

from collections import defaultdict
from dataclasses import dataclass
import math
import re
import os
from typing import Tuple, List

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

COSTS = [3, 1]


@dataclass
class Machine:
    prize: Tuple[int, int]
    buttons: List[Tuple[int, int]]


def day13_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    sections = [section.split("\n") for section in data.split("\n\n")]

    button_reg = r"Button [A|B]:|\s[X|Y]\+"
    prize_reg = r"Prize:|\s[X|Y]="

    machines = []
    for section in sections:
        value_list = []
        for i in range(3):
            reg = button_reg if i < 2 else prize_reg
            filtered_section = re.sub(reg, "", section[i])
            value_list.append(tuple([int(el) for el in filtered_section.split(",")]))

        machines.append(Machine(prize=value_list[2], buttons=value_list[:2]))

    return machines


def is_key_valid(key, prize):
    return 0 <= key[0] <= prize[0] and 0 <= key[1] <= prize[1]


def calculate_min_tokens(machine: Machine):
    cache = defaultdict(lambda: math.inf)

    work_list = [(0, 0, 0, 0, 0)]

    while work_list:
        item = work_list.pop()
        key = (item[0], item[1])

        if not is_key_valid(key, machine.prize) or item[2] > 100 or item[3] > 100:
            continue

        if cache[key] <= item[4]:
            continue

        cache[key] = item[4]

        # press buttons
        for i in range(len(COSTS)):
            machine_button = machine.buttons[i]
            new_item = (
                item[0] + machine_button[0],
                item[1] + machine_button[1],
                item[2] + 1 if i % 2 == 0 else 0,
                item[3] + 1 if i % 2 else 0,
                item[4] + COSTS[i],
            )

            work_list.append(new_item)

    return cache[machine.prize]


def day13_part_1(filename):
    machines = day13_file_read(filename)

    results = 0
    for machine in machines:
        tokens = calculate_min_tokens(machine)
        if tokens != math.inf:
            results += tokens

    print(f"Day 13 part 1 {filename} results: {results}")


day13_part_1("sample.txt")
day13_part_1("input.txt")
