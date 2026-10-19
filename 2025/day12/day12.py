import numpy as np
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day12_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    rows = data.split('\n\n')

    packages = []
    areas = []
    for row in rows[:-1]:
        r = row.split('\n')[1:]
        matrix = np.zeros((len(r), len(r[0])), dtype=int)
        area = 0
        for i in range(len(r)):
            for j in range(len(r[0])):
                if r[i][j] == "#":
                    matrix[i][j] = 1
                    area += 1

        packages.append((matrix, area))


    for row in rows[-1].split('\n'):
        parsed = row.replace(":", "").split(' ')
        dimensions = tuple(int(x) for x in parsed[0].split('x'))
        areas.append((dimensions, [int(x) for x in parsed[1:]]))

    return packages, areas

def day12_part_1(filename):
    # either bin-packing algorithm or this cheese
    packages, areas = day12_file_read(filename)
    ans = 0
    for area in areas:
        a = area[0][0] * area[0][1]
        package_areas = 0
        for idx, p in enumerate(area[1]):
            package_areas += p * packages[idx][1]

        if a >= package_areas:
            ans += 1

    print(ans)


day12_part_1("sample.txt")
day12_part_1("input.txt")

