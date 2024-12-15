# https://adventofcode.com/2024/day/14

from dataclasses import dataclass
from functools import reduce
import re
import os
from typing import Tuple, List

import matplotlib

matplotlib.use("WebAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


@dataclass
class Robot:
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int

    def __init__(self, elements: List[int]):
        assert len(elements) == 4
        self.pos_x = elements[0]
        self.pos_y = elements[1]
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
                (robot.pos_x + robot.vel_x * time) % max_x,
                (robot.pos_y + robot.vel_y * time) % max_y,
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


def move_robots(robots: List[Robot], max_x: int, max_y: int, sec: int):
    for robot in robots:
        robot.pos_x = (robot.pos_x + robot.vel_x * sec) % max_x
        robot.pos_y = (robot.pos_y + robot.vel_y * sec) % max_y


def get_x_and_y(robots: List[Robot]) -> Tuple[List[int], List[int]]:
    return ([robot.pos_x for robot in robots], [robot.pos_y for robot in robots])


def animate(i, robots, max_x, max_y):
    plt.cla()
    move_robots(robots, max_x, max_y, 1)
    x, y = get_x_and_y(robots)
    plt.title(f"Frame: {i}")
    plt.scatter(x, y)


#######################################################
# from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


#######################################################


def crt(congruences: List[Tuple[int, int]]):
    M = reduce(lambda x, y: x * y, [c[1] for c in congruences])

    result = 0
    for i in range(len(congruences)):
        m_i = M // congruences[i][1]
        x_i = modinv(m_i, congruences[i][1])
        result += (congruences[i][0] * m_i * x_i) % M

    return result


def day14_part_2():
    # initial rendering to check where cycles begin and end
    # robots, max_x, max_y = day14_file_read("input.txt")
    # move_robots(robots, max_x, max_y, 72)
    # x, y = get_x_and_y(robots)
    # plt.title("Frame: 0")
    # plt.scatter(x, y)
    # fig = plt.figure()
    # ani = animation.FuncAnimation(
    #     fig,
    #     animate,
    #     interval=700,
    #     fargs=(robots, max_x, max_y),
    #     frames=102,
    #     repeat=False,
    # )
    # plt.show()

    # from manual rendering
    # (start_cycle, cycle_length)
    # (72, 103), (2, 101)

    # We need to use Chinese Remainder theorem to figure out when these cycles intersect
    results = crt([(72, 103), (2, 101)])

    print(f"Day 14 part 2 input.txt results: {results}")


day14_part_1("sample.txt")
day14_part_1("input.txt")

day14_part_2()
