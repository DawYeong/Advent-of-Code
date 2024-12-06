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


def is_page_valid(page, graph):
    i = 0
    while i < len(page) - 1 and page[i + 1] in graph[page[i]]:
        i += 1

    return i == len(page) - 1


def day5_part_1(filename):
    rules, pages = day5_file_read(filename)

    # build graph
    graph = build_graph(rules)

    results = 0
    for page in pages:
        if is_page_valid(page, graph):
            results += int(page[len(page) // 2])

    print(f"Day 5 part 1 {filename} results: {results}")


def dfs(graph, reverse_graph, nodes):
    # this is assuming the graph is a tree, if it is a forest, different story
    source_nodes = [node for node in nodes if len(reverse_graph[node]) == 0]
    visited = set()
    post_visit = {}
    clock = 0

    def explore(start_node):
        nonlocal clock, visited, post_visit
        visited.add(start_node)
        clock += 1
        for node in graph[start_node]:
            if node not in visited:
                explore(node)

        post_visit[start_node] = clock
        clock += 1

    for source_node in source_nodes:
        explore(source_node)

    return post_visit


def get_middle_from_ordered_page(page, post_visit):
    sorted_page = sorted(page, key=(lambda x: post_visit[x]), reverse=True)

    return int(sorted_page[len(sorted_page) // 2])


def build_sub_graph(graph, page):
    sub_graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for node, children in graph.items():
        if node not in page:
            continue

        filtered_children = []
        for child in children:
            if child not in page:
                continue
            filtered_children.append(child)
            reverse_graph[child].append(node)

        sub_graph[node] = filtered_children

    return sub_graph, reverse_graph


def day5_part_2(filename):
    rules, pages = day5_file_read(filename)
    # main graph is not a DAG... => some sort of sort on sub graph?
    graph = build_graph(rules)

    results = 0
    for page in pages:
        if not is_page_valid(page, graph):
            # graph from input is actually cyclical
            # subgraph containing only page nodes should be a DAG, if it isn't then this problem is impossible
            sub_graph, reverse_graph = build_sub_graph(graph, page)
            # performs dfs and returns a list of post_visit => topological sort is descending order of post_visit
            post_visit = dfs(sub_graph, reverse_graph, page)
            results += get_middle_from_ordered_page(page, post_visit)

    print(f"Day 5 part 2 {filename} results: {results}")


day5_part_1("sample.txt")
day5_part_1("input.txt")

day5_part_2("sample.txt")
day5_part_2("input.txt")
