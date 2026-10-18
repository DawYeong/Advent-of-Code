from collections import deque
import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def convert_idx_pos_to_binary(idx_arr):
    num = 0
    for idx in idx_arr:
        num |= (1 << int(idx))

    return num


def day10_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    raw_rows = data.split('\n')
    rows = []
    for row in raw_rows:
        cleaned = row.translate(str.maketrans("", "", "[]{}()")).split(' ')
        binary_string = cleaned[0].replace("#", "1").replace(".", "0")[::-1]
        
        rows.append(
            (
                int(binary_string, 2),
                [convert_idx_pos_to_binary(r.split(',')) for r in cleaned[1:-1]],
                [int(x) for x in cleaned[-1].split(',')],
                int("1"*len(binary_string), 2)
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
        

day10_part_1("sample.txt")
day10_part_1("input.txt")
