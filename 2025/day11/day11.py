from collections import defaultdict
from functools import lru_cache
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


def get_all_paths_from_source_part_1(graph, source, destination):
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

def get_all_paths_from_source_part_2(graph, source, destination):
    @lru_cache(maxsize=None)
    def dfs(node, seen_fft, seen_dac):
        if node == destination:
            if seen_fft and seen_dac:
                return 1
            return 0

        total = 0
        for child in graph[node]:
            next_fft = seen_fft | (child == 'fft')
            next_dac = seen_dac | (child == 'dac')
            total += dfs(child, next_fft, next_dac)

        return total

    return dfs(source, False, False)



def day11_part_1(filename):
    graph = day11_file_read(filename)

    all_paths = get_all_paths_from_source_part_1(graph, "you", "out")

    print(f"Day 11 part 1 {filename} results: {len(all_paths)}")


def day11_part_2(filename):
    graph = day11_file_read(filename)
    
    total = get_all_paths_from_source_part_2(graph, "svr", "out")

    print(f"Day 11 part 2 {filename} results: {total}")


# day11_part_1("sample.txt")
# day11_part_1("input.txt")

day11_part_2("sample2.txt")
day11_part_2("input.txt")
