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


def day7_part_1(filename):
    start, splitters = day7_file_read(filename)

    new_beams = {start}
    splitters_hit = set()
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

        new_beams = new_beam_set

    print(f"Day 7 part 1 {filename} results: {len(splitters_hit)}")


day7_part_1("sample.txt")
day7_part_1("input.txt")
