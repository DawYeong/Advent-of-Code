# https://adventofcode.com/2024/day/1

from collections import defaultdict


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

    results = 0
    for i in range(len(list1)):
        results += abs(list1[i] - list2[i])

    print(f"Day 1 part 1 {filename} results: {results}")


def day1_part2(filename):
    list1, list2 = day1_file_read(filename)

    # technically can just use Counter, but want to show work
    occurrences = defaultdict(int)
    for el in list1:
        occurrences[el] += 1

    results = 0
    for el in list2:
        results += el * occurrences[el]

    print(f"Day 1 part 2 {filename} results: {results}")


day1_part1("sample.txt")
day1_part1("input.txt")

day1_part2("sample.txt")
day1_part2("input.txt")
