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


def day9_part_2(filename):
    coords = day9_file_read(filename)
    pairs = list(combinations(coords, 2))

    vertical_lines = set()
    horizontal_lines = set()
    for i in range(len(coords)):
        a = coords[i%len(coords)]
        b = coords[(i+1)%len(coords)]

        if a[0] == b[0]:
            vertical_lines.add(tuple(sorted([a, b], key=lambda x: x[1])))

        if a[1] == b[1]:
            horizontal_lines.add(tuple(sorted([a, b], key=lambda x: x[0])))


    max_area = 0
    for a, b in pairs:
        is_valid = True

        rect_min_x, rect_max_x = min(a[0], b[0]), max(a[0], b[0])
        rect_min_y, rect_max_y = min(a[1], b[1]), max(a[1], b[1])
        mid_x = (rect_min_x + rect_max_x) / 2.0
        mid_y = (rect_min_y + rect_max_y) / 2.0

        # ray cast in center first to avoid edge checking
        vert_matches = [
            line for line in vertical_lines
            if line[0][1] <= mid_y < line[1][1] and mid_x <= line[0][0]
        ]

        if len(vert_matches) % 2 == 0:
            is_valid = False

        # Then start checking how many lines we are hitting given the bounds
        if is_valid:
            for line in vertical_lines:
                wall_x = line[0][0]
                # If wall is inside the X bounds
                if rect_min_x < wall_x < rect_max_x:
                    # If wall's Y range overlaps the rectangle's Y range
                    if not (line[1][1] <= rect_min_y or line[0][1] >= rect_max_y):
                        is_valid = False
                        break

            for line in horizontal_lines:
                wall_y = line[0][1]
                # If wall is inside the Y bounds
                if rect_min_y < wall_y < rect_max_y:
                    # If wall's X range overlaps the rectangle's X range
                    if not (line[1][0] <= rect_min_x or line[0][0] >= rect_max_x):
                        is_valid = False
                        break

        if is_valid:
            area = ((abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1))
            if area > max_area:
                max_area = area


    print(f"Day 9 part 2 {filename} results: {max_area}")



# day9_part_1("sample.txt")
# day9_part_1("input.txt")

day9_part_2("sample.txt")
day9_part_2("input.txt")
