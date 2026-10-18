from collections import deque
import numpy as np
from scipy.optimize import linprog
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def convert_idx_pos_to_binary(idx_arr):
    num = 0
    for idx in idx_arr:
        num |= (1 << int(idx))

    return num

def build_equation(idx_arr, length):
    arr = [0] * length
    for idx in idx_arr:
        arr[idx] = 1
    return arr



def day10_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    raw_rows = data.split('\n')
    rows = []
    for row in raw_rows:
        cleaned = row.translate(str.maketrans("", "", "[]{}()")).split(' ')
        binary_string = cleaned[0].replace("#", "1").replace(".", "0")[::-1]
        buttons = [[int(x) for x in r.split(',')]for r in cleaned[1:-1]]
        
        rows.append(
            (
                int(binary_string, 2),
                [convert_idx_pos_to_binary(b) for b in buttons],
                [int(x) for x in cleaned[-1].split(',')],
                int("1"*len(binary_string), 2),
                [build_equation(button, len(binary_string)) for button in buttons]
            )
        )

    return rows

def day10_part_1(filename):
    # rows are 3-tuples where pos 1 is the final state, 2 is a list of buttons, 3 is the joltages, 4 is the mask
    rows = day10_file_read(filename)

    ans = 0 
    for row in rows:
        visited = set()
        work = deque([(0, 0)])
        final = 0
        while work:
            state, presses = work.popleft()
            # print(state, presses)
            if state == row[0]:
                final = presses
                break


            for button in row[1]:
                # Bitwise XOR
                next_state = (state ^ button) & row[3]
                if next_state not in visited:
                    visited.add(next_state)
                    work.append((next_state, presses + 1))
        
        ans += final
        
    print(f"Day 10 part 1 {filename} results: {ans}")



def day10_part_2(filename):
    rows = day10_file_read(filename)

    ans = 0
    for row in rows:
        A = np.array(row[4])
        b = np.array(row[2])

        """
        We have X number of equations and N number of constraints, this is linear programming problem

        Given an example like [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

        We have 6 buttons and we want to minimize the number of button presses:
        Min P = b_1 + b_2 + b_3 + b_4 + b_5 + b_6

        We also have constraints given the joltage
        For 1: b_5 + b_6 = 3
        For 2: b_2 + b_6 = 5
        For 3: b_3 + b_4 + b_5 = 4
        For 4: b_1 + b_2 + b_4 = 7

        As well as:
        b >= 0 and b has to be a positive integer

        Transforming this to a matrix it ends up looking like:
        P0 [ 0  0  0  0  1  1 ] = 3
        P1 [ 0  1  0  0  0  1 ] = 5
        P2 [ 0  0  1  1  1  0 ] = 4
        P3 [ 1  1  0  1  0  0 ] = 7
        """
        c = [1] * len(row[4])
        result = linprog(c, A_eq=A.T, b_eq=b, integrality=1)

        ans += int(np.sum(np.round(result.x)))


    print(f"Day 10 part 2 {filename} results: {ans}")
                    


# day10_part_1("sample.txt")
# day10_part_1("input.txt")

day10_part_2("sample.txt")
day10_part_2('input.txt')
