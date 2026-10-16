from itertools import combinations
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


def day9_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    coords = [tuple(int(x) for x in row.split(',')) for row in data.split("\n")]

    return coords

def day9_part_1(filename):
    coords = day9_file_read(filename)
    pairs = combinations(coords, 2)

    max_area = 0
    for a, b in pairs:
        # calculate area
        area = ((abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1))
        if area > max_area:
            max_area = area

    print(f"Day 9 part 1 {filename} results: {max_area}")


day9_part_1("sample.txt")
day9_part_1("input.txt")
