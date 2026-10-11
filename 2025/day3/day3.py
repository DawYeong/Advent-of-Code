import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day3_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    rows = [[int(l) for l in row] for row in data.split('\n')]

    return rows


def day3(filename, length, part):
    rows = day3_file_read(filename)
    
    joltage = 0
    for r in rows:
        num = ""
        curr_idx = 0
        for i in range(length-1, -1, -1):
            max_num = max(r[curr_idx:len(r)-i])
            max_num_idx = r[curr_idx:len(r)-i].index(max_num)
            num += str(max_num)
            curr_idx += max_num_idx + 1

        joltage += int(num)

    print(f"Day 3 part {part} {filename} results: {joltage}")


def day3_part_1(filename):
    day3(filename, 2, 1)

def day3_part_2(filename):
    day3(filename, 12, 2)


day3_part_1("sample.txt")
day3_part_1("input.txt")

day3_part_2("sample.txt")
day3_part_2("input.txt")
