# https://adventofcode.com/2024/day/14

from dataclasses import dataclass
from functools import reduce
import re
import os
from typing import Tuple, List

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


@dataclass
class Robot:
    start_x: int
    start_y: int
    vel_x: int
    vel_y: int

    def __init__(self, elements: List[int]):
        assert len(elements) == 4
        self.start_x = elements[0]
        self.start_y = elements[1]
        self.vel_x = elements[2]
        self.vel_y = elements[3]


def day14_file_read(filename: str) -> Tuple[Robot, int, int]:
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")
    reg = r"[p|v]="

    robots = []

    max_x = 0
    max_y = 0

    for line in lines:
        elements = [int(el) for el in re.split(",| ", re.sub(reg, "", line).strip())]
        robots.append(Robot(elements))
        max_x = max(max_x, elements[0])
        max_y = max(max_y, elements[1])

    return robots, max_x + 1, max_y + 1


def simulate_robots(
    robots: List[Robot], max_x: int, max_y: int, time: int
) -> List[Tuple[int, int]]:
    final_positions = []
    for robot in robots:
        final_positions.append(
            (
                (robot.start_x + robot.vel_x * time) % max_x,
                (robot.start_y + robot.vel_y * time) % max_y,
            )
        )

    return final_positions


def compute_safety_factor(
    robot_pos: List[Tuple[int, int]], max_x: int, max_y: int
) -> int:
    quadrant = [0, 0, 0, 0]
    mid_x = max_x // 2
    mid_y = max_y // 2

    for pos in robot_pos:
        if pos[0] == mid_x or pos[1] == mid_y:
            continue

        if pos[0] > mid_x and pos[1] > mid_y:
            # quadrant 1
            quadrant[0] += 1
        elif pos[0] > mid_x and pos[1] < mid_y:
            # quadrant 4
            quadrant[3] += 1
        elif pos[0] < mid_x and pos[1] > mid_y:
            # quadrant 2
            quadrant[1] += 1
        elif pos[0] < mid_x and pos[1] < mid_y:
            # quadrant 3
            quadrant[2] += 1

    return reduce(lambda x, y: x * y, quadrant)


def day14_part_1(filename: str):
    robots, max_x, max_y = day14_file_read(filename)

    final_robot_positions = simulate_robots(robots, max_x, max_y, 100)
    results = compute_safety_factor(final_robot_positions, max_x, max_y)

    print(f"Day 14 part 1 {filename} results: {results}")


day14_part_1("sample.txt")
day14_part_1("input.txt")
