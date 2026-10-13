import os
import numpy as np
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
    
def day6_part_2_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    # transforming into matrix to retain spaces
    rows = np.array([list(r) for r in data.split('\n')]).T

    # grab operators
    ops = [op for op in rows[:, -1] if op != ' ']
    cleaned_rows = rows[:, :-1]

    empty_row_mask = (cleaned_rows == ' ').all(axis=1)
    empty_row_indices = np.where(empty_row_mask)[0]

    # this will split by completely empty rows (columns from input but we transposed)
    groups = [
            group[~(group == ' ').all(axis=1)]
            for group in np.split(cleaned_rows, empty_row_indices)
        ]
    final_nums = []

    for group in groups:
        final_nums.append(
            [
                int("".join(x for x in row if x != ' '))
                for row in group
            ]
        )

    return final_nums, ops    


def day6_part_2(filename):
    nums, ops = day6_part_2_file_read(filename)
    total_sum = sum(
            [
                reduce(operator.add if ops[idx] == '+' else operator.mul, row) 
                for idx, row in enumerate(nums)
            ]
        )

    print(f"Day 6 part 2 {filename} results: {total_sum}")
    

# day6_part_1("sample.txt")
# day6_part_1("input.txt")

day6_part_2("sample.txt")
day6_part_2("input.txt")
