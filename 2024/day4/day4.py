# https://adventofcode.com/2024/day/4

from collections import defaultdict

DIRECTIONS = {
    (1, 0),  # N
    (0, 1),  # E
    (-1, 0),  # S
    (0, -1),  # W
    (1, 1),  # NE
    (-1, -1),  # SW
    (-1, 1),  # SE
    (1, -1),  # NW
}

TARGET_WORD = "XMAS"

X_CHECK = {"M", "S"}


def day4_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return [list(line) for line in data.split("\n")]


def is_coord_valid(y, x, n, m):
    return 0 <= y < n and 0 <= x < m


def day4_part_1(filename):
    grid = day4_file_read(filename)
    n = len(grid)
    m = len(grid[0])

    def check_direction(r, c, y, x):
        target_x = c + x * (len(TARGET_WORD) - 1)
        target_y = r + y * (len(TARGET_WORD) - 1)

        if not is_coord_valid(target_y, target_x, n, m):
            return False

        for i in range(len(TARGET_WORD)):
            if grid[r + y * i][c + x * i] != TARGET_WORD[i]:
                return False

        return True

    def traverse(r, c):
        occurrences = 0
        for y, x in DIRECTIONS:
            # check if XMAS would even be in bounds
            if check_direction(r, c, y, x):
                occurrences += 1

        return occurrences

    results = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "X":
                # begin traversal
                results += traverse(i, j)

    print(f"Day 4 part 1 {filename} results: {results}")


def day4_part_2(filename):
    grid = day4_file_read(filename)
    n = len(grid)
    m = len(grid[0])

    def check_x(r, c):
        # check the four corners => opposite corners have to be M S
        corners = [
            (r + 1, c - 1, 0),
            (r - 1, c + 1, 0),
            (r + 1, c + 1, 1),
            (r - 1, c - 1, 1),
        ]
        direction_pair = defaultdict(set)

        for new_y, new_x, key in corners:
            if not is_coord_valid(new_y, new_x, n, m):
                return False

            direction_pair[key].add(grid[new_y][new_x])

        for pair in direction_pair.values():
            if pair != X_CHECK:
                return False

        return True

    results = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "A" and check_x(i, j):
                results += 1

    print(f"Day 4 part 2 {filename} results: {results}")


day4_part_1("sample.txt")
day4_part_1("input.txt")

day4_part_2("sample.txt")
day4_part_2("input.txt")
