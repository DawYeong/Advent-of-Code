import os
from functools import reduce
import operator

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day6_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    processed = [[int(r) if r.isdigit() else r for r in row.split()] for row in data.split('\n')]

    return processed[:-1], processed[-1]

def day6_part_1(filename):
    nums, ops = day6_file_read(filename)
    
    total_sum = sum(
        [
            reduce(operator.add if ops[idx] == '+' else operator.mul, col) 
            for idx, col in enumerate(zip(*nums))
        ]
    )

    print(f"Day 6 part 1 {filename} results: {total_sum}")
    


day6_part_1("sample.txt")
day6_part_1("input.txt")
