from collections import defaultdict
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day11_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    rows = [row.replace(':', '').split(' ') for row in data.split('\n')]

    graph = defaultdict(list)
    for row in rows:
        graph[row[0]].extend(row[1:])

    return graph


def get_all_paths_from_source(graph, source, destination):
    result = []

    def dfs(node, path):
        if node == destination:
            result.append(list(path))
            return
        for child in graph[node]:
            path.append(child)
            dfs(child, path)
            path.pop()

    dfs(source, [source])
    return result

def day11_part_1(filename):
    graph = day11_file_read(filename)

    all_paths = get_all_paths_from_source(graph, "you", "out")

    print(f"Day 11 part 1 {filename} results: {len(all_paths)}")


day11_part_1("sample.txt")
day11_part_1("input.txt")
