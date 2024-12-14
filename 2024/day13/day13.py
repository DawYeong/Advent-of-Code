# https://adventofcode.com/2024/day/13

from dataclasses import dataclass
import re
import os
from typing import Tuple, List

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


OFFSET = 10000000000000


@dataclass
class Machine:
    prize: Tuple[int, int]
    buttons: List[Tuple[int, int]]


def day13_file_read(filename, part_2=False):
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

        machines.append(
            Machine(
                prize=(
                    value_list[2][0] + (OFFSET if part_2 else 0),
                    value_list[2][1] + (OFFSET if part_2 else 0),
                ),
                buttons=value_list[:2],
            )
        )

    return machines


def calculate_min_tokens(machine: Machine):
    """
    Linear optimization problem:

    min 3*A + B
    constraints:
    But.X * A + But.X * B = Prize.X
    But.Y * A + But.Y * B = Prize.Y

    Find point of intersection
    """
    det = (
        machine.buttons[0][0] * machine.buttons[1][1]
        - machine.buttons[1][0] * machine.buttons[0][1]
    )
    if det == 0:
        return None

    A = (
        machine.prize[0] * machine.buttons[1][1]
        - machine.prize[1] * machine.buttons[1][0]
    ) / det

    B = (
        machine.prize[1] * machine.buttons[0][0]
        - machine.prize[0] * machine.buttons[0][1]
    ) / det

    # a point is valid only if it has integers
    if int(A) == A and int(B) == B:
        return int(A) * 3 + int(B) * 1
    else:
        return None


def day13_part_1(filename):
    machines = day13_file_read(filename)

    results = 0
    for machine in machines:
        tokens = calculate_min_tokens(machine)
        if tokens:
            results += tokens

    print(f"Day 13 part 1 {filename} results: {results}")


def day13_part_2(filename):
    machines = day13_file_read(filename, True)

    results = 0
    for machine in machines:
        tokens = calculate_min_tokens(machine)
        if tokens:
            results += tokens

    print(f"Day 13 part 2 {filename} results: {results}")


day13_part_1("sample.txt")
day13_part_1("input.txt")

day13_part_2("sample.txt")
day13_part_2("input.txt")
