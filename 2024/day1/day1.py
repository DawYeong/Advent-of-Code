# https://adventofcode.com/2024/day/1


def day1_file_read(filename):
    with open(filename, "r") as file:
        data = file.read().split("\n")

    list1 = []
    list2 = []
    for line in data:
        elements = line.replace("  ", ",").split(",")
        list1.append(int(elements[0]))
        list2.append(int(elements[1]))

    return list1, list2


def day1_part1(filename):
    list1, list2 = day1_file_read(filename)
    assert len(list1) == len(list2)

    list1.sort()
    list2.sort()

    result = 0
    for i in range(len(list1)):
        result += abs(list1[i] - list2[i])

    print(f"Day 1 part 1 {filename} results: {result}")


day1_part1("sample.txt")
day1_part1("input.txt")
