# https://adventofcode.com/2024/day/5

from collections import defaultdict


def day5_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    parts = data.split("\n\n")

    rules = [line.split("|") for line in parts[0].split("\n")]
    pages = [line.split(",") for line in parts[1].split("\n")]

    return rules, pages


def build_graph(rules):
    graph = defaultdict(list)
    for rule in rules:
        graph[rule[0]].append(rule[1])

    return graph


def day5_part_1(filename):
    rules, pages = day5_file_read(filename)

    # build graph
    graph = build_graph(rules)

    def is_page_valid(page):
        i = 0
        while i < len(page) - 1 and page[i + 1] in graph[page[i]]:
            i += 1

        return i == len(page) - 1

    results = 0
    for page in pages:
        if is_page_valid(page):
            results += int(page[len(page) // 2])

    print(f"Day 5 part 1 {filename} results: {results}")


day5_part_1("sample.txt")
day5_part_1("input.txt")
