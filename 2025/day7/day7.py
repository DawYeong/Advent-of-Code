from bisect import bisect_right
from collections import defaultdict
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


def day7_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    rows = data.split('\n')
    splitters = defaultdict(list)

    start = None
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            if rows[i][j] == "S":
                start = (i, j)
            elif rows[i][j] == "^":
                splitters[j].append(i)

    return start, splitters

# for the current beams, is how many splitters will it hit -> determine the splits -> those will be the new beams to keep track
# to determine the current beams hit something -> given the row and col is there something in the same col below? -> closest splitter in row

def dp(graph, start):
    # dp values here represents the number of paths from start to a particular node
    # we process downwards with dp[start] = 1
    # we need to process nodes in appropriate order so topo sort helps here
    
    indegree = defaultdict(int)

    for v in graph.values():
        for n in v:
            indegree[n] += 1

    work = [start]
    dp_values = defaultdict(int)

    dp_values[start] = 1
    while work:
        item = work.pop(0)
        
        for child in graph[item]:
            dp_values[child] += dp_values[item]

            indegree[child] -= 1

            if indegree[child] == 0:
                work.append(child)
    
    return dp_values



def day7_process(filename):
    start, splitters = day7_file_read(filename)
    
    new_beams = {start}
    splitters_hit = set()
    graph = defaultdict(set)
    while new_beams:
        # process each beam
        new_beam_set = set()
        for beam in new_beams:
            # figure out if it hits a splitter
            possible_splitters = splitters[beam[1]]
            # figure out the closest splitter
            if not possible_splitters:
                continue

            closest_splitter_row = bisect_right(possible_splitters, beam[0])
            if closest_splitter_row == len(possible_splitters):
                continue

            # it found a splitter, split
            splitters_hit.add((possible_splitters[closest_splitter_row], beam[1]))
            new_beam_set.add((possible_splitters[closest_splitter_row], beam[1]-1)) # left
            new_beam_set.add((possible_splitters[closest_splitter_row], beam[1]+1)) # right

            # building graph
            graph[beam].update({(possible_splitters[closest_splitter_row], beam[1]-1), (possible_splitters[closest_splitter_row], beam[1]+1)})

        new_beams = new_beam_set

    dp_values = dp(graph, start)

    leaf_nodes = set([node for node, values in graph.items() if not values])

    # gather leaf nodes
    paths = 0
    for node in leaf_nodes:
        paths += dp_values[node]

    print(f"Day 7 part 1 {filename} results: {len(splitters_hit)}")
    print(f"Day 7 part 2 {filename} results: {paths}")


day7_process("sample.txt")
day7_process("input.txt")
