import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day3_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    rows = [[int(l) for l in row] for row in data.split('\n')]

    return rows


def day3_part_1(filename):
    rows = day3_file_read(filename)

    joltage = 0
    for r in rows:
        limit = max(r)
        limit_idx = r.index(limit)

        first_digit = 0
        second_digit = 0
        if limit_idx == len(r) - 1:
            # max is at the end, find find the first digit
            second_digit = limit
            first_digit = max(r[:len(r)-1])
        else:
            # max is at some beginning, find the max else where
            first_digit = limit
            second_digit = max(r[limit_idx+1:])

        joltage += int(str(first_digit) + str(second_digit))

    print(f"Day 3 part 1 {filename} results: {joltage}")

day3_part_1("sample.txt")
day3_part_1("input.txt")

