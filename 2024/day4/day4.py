# https://adventofcode.com/2024/day/4

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


def day4_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return [list(line) for line in data.split("\n")]


def day4_part_1(filename):
    grid = day4_file_read(filename)
    n = len(grid)
    m = len(grid[0])

    def check_direction(r, c, y, x):
        target_x = c + x * (len(TARGET_WORD) - 1)
        target_y = r + y * (len(TARGET_WORD) - 1)

        if target_x < 0 or target_x >= m or target_y < 0 or target_y >= n:
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


day4_part_1("sample.txt")
day4_part_1("input.txt")
