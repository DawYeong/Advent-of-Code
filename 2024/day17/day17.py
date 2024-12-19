# https://adventofcode.com/2024/day/17

from dataclasses import dataclass
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


def execute_program(device: Device):
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

    return ",".join(out)


def day17_part_1(filename: str):
    device = day17_file_read(filename)
    results = execute_program(device)

    print(f'Day 17 part 1 {filename} results: {results}')


day17_part_1("sample.txt")
day17_part_1("input.txt")
