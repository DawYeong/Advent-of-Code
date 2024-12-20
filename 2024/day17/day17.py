# https://adventofcode.com/2024/day/17

import copy
from dataclasses import dataclass
import math
import os
import re

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


@dataclass
class Device:
    registers: list[int]
    program: list[int]


OPCODE_COMBO = {4: 0, 5: 1, 6: 2}


def day17_file_read(filename: str) -> Device:
    with open(filename, "r") as file:
        data = file.readlines()

    lines = [
        [int(num) for num in el]
        for el in list(
            filter(lambda x: len(x) > 0, [re.findall(r"\d+", line) for line in data])
        )
    ]

    return Device(registers=[lines[0][0], lines[1][0], lines[2][0]], program=lines[3])


def execute_program(device: Device) -> list[int]:
    program_counter = 0

    out = []

    while program_counter < len(device.program):
        opcode = device.program[program_counter]
        operand = device.program[program_counter + 1]
        combo = OPCODE_COMBO.get(operand, None)
        combo_value = device.registers[combo] if combo is not None else operand

        match opcode:
            case 0:
                # division
                device.registers[0] = device.registers[0] // pow(2, combo_value)
            case 1:
                # bitwise XOR: B = B ^ literal
                device.registers[1] = device.registers[1] ^ operand
            case 2:
                # mod 8
                device.registers[1] = combo_value % 8
            case 3:
                # jump
                if device.registers[0] != 0:
                    program_counter = operand
                    continue
            case 4:
                # bitwise XOR: B = B ^ C
                device.registers[1] = device.registers[1] ^ device.registers[2]
            case 5:
                # out
                out.append(str(combo_value % 8))
            case 6:
                # division but store in B
                device.registers[1] = device.registers[0] // pow(2, combo_value)
            case 7:
                # division but store in C
                device.registers[2] = device.registers[0] // pow(2, combo_value)

        program_counter += 2

    return out


def day17_part_1(filename: str):
    device = day17_file_read(filename)
    results = execute_program(device)

    print(f"Day 17 part 1 {filename} results: {",".join(results)}")


def octal_to_decimal(octal: str) -> int:
    result = 0
    for i in range(len(octal)):
        result += int(octal[len(octal) - 1 - i]) * pow(8, i)

    return result


def day17_part_2(filename: str):
    device = day17_file_read(filename)

    # TESTING
    # for i in range(8):
    #     for j in range(8):
    #         for k in range(8):
    #             for m in range(8):
    #                 print(f'Start: {i}, {j}, {k}, {m}')
    #                 # device1 = copy.deepcopy(device)
    #                 device.registers[0] = octal_to_decimal(str(i) + str(j) + str(k) + str(m))
    #                 print(execute_program(device))

    results = math.inf

    def backtracking(curr_level: int, curr_value: int):
        nonlocal results

        for i in range(8):
            value = curr_value + i
            device_copy = copy.deepcopy(device)
            device_copy.registers[0] = value
            curr_result = execute_program(device_copy)
            if int(curr_result[0]) == device.program[-curr_level]:
                if curr_level == len(device.program):
                    results = min(results, value)
                else:
                    backtracking(curr_level + 1, value * 8)

    backtracking(1, 0)

    print(f"Day 17 part 2 {filename} results: {results}")


day17_part_1("sample.txt")
day17_part_1("sample2.txt")
day17_part_1("input.txt")

day17_part_2("sample2.txt")
day17_part_2("input.txt")
