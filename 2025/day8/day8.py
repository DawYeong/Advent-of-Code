from collections import defaultdict
from itertools import combinations
import math
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


def day8_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    coords = [tuple(int(x) for x in row.split(',')) for row in data.split('\n')]

    return coords

def calculate_distance(a, b):
    # assuming a and b are same length
    x = 0

    for i in range(len(a)):
        x += (a[i] - b[i]) ** 2

    return x ** 0.5


def day8_part_1(filename, connections):
    coords = day8_file_read(filename)

    pairs = list(combinations(range(0,len(coords)), 2))
    distances = []
    for i, j in pairs:  
        dist = calculate_distance(coords[i], coords[j])
        distances.append((dist, i, j))


    sorted_distances = sorted(distances, key=lambda x: x[0])
    trimmed_distances = sorted_distances[:connections]

    connection_dict = defaultdict(set)
    for item in trimmed_distances:
        connection_dict[item[1]].add(item[2])
        connection_dict[item[2]].add(item[1])

    nodes = connection_dict.keys()


    graphs = []
    visited = set()
    for node in nodes:
        if node not in visited:
            current_graph = set()
            work = [node]
            while work:
                item = work.pop(0)
                current_graph.add(item)
                visited.add(item)
                for child in connection_dict[item]:
                    if child not in visited:
                        visited.add(child)
                        current_graph.add(child)
                        work.append(child)

            graphs.append(current_graph)

    three_largest = math.prod(sorted([len(g) for g in graphs], reverse=True)[:3])

    print(f"Day 8 part 1 {filename} results: {three_largest}")

def day8_part_2(filename):
    coords = day8_file_read(filename)

    nodes = set(range(0, len(coords)))
    pairs = list(combinations(nodes, 2))
    distances = []
    for i, j in pairs:  
        dist = calculate_distance(coords[i], coords[j])
        distances.append((dist, i, j))


    sorted_distances = sorted(distances, key=lambda x: x[0])
    make_sets = list({i} for i in nodes)

    def find_set(u):
        for idx, s in enumerate(make_sets):
            if u in s:
                return s, idx

    # kruskals algorithm -> we will build the MST using the shortest edges
    # essentially we are connecting shortest length connections until the graph is connected, noting the final connection
    ans = 0
    for edge in sorted_distances:
        _, u, v = edge
        set_u, idx_u = find_set(u)
        set_v, idx_v = find_set(v)
        if set_u != set_v:
            # nodes in different sets merge them
            make_sets[idx_u] = set_u | set_v
            del make_sets[idx_v]

            if len(make_sets) == 1:
                # only one set that means we found the last pair, note the pairs
                ans = coords[u][0] * coords[v][0]
                break

    print(f"Day 8 part 2 {filename} results: {ans}")


# day8_part_1("sample.txt", 10)
# day8_part_1("input.txt", 1000)

day8_part_2("sample.txt")
day8_part_2("input.txt")
