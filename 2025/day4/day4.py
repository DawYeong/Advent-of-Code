import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


check_locs = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
    (-1, -1)
]

def day4_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    raw = data.split('\n')
    paper_roll_locs = set()

    for row in range(len(raw)):
        for col in range(len(raw[0])):
            if raw[row][col] == '@':
                paper_roll_locs.add((row, col))


    return paper_roll_locs, len(raw), len(raw[0])

def day4_part_1(filename):
    paper_rolls, max_row, max_col = day4_file_read(filename)
    can_access = 0
    for roll in paper_rolls:
        num_in_range = 0
        for check in check_locs:
            loc_check = tuple(x + y for x, y in zip(roll, check))

            if loc_check[0] < 0 or loc_check[1] < 0 or loc_check[0] == max_row or loc_check[1] == max_col:
                # out of bounds
                continue

            if loc_check in paper_rolls:
                num_in_range += 1
            
            if num_in_range == 4:
                # no need to process other directions
                break

        if num_in_range != 4:
            can_access += 1

    print(f'Day 4 part 1 {filename} results: {can_access}')
            

def day4_part_2(filename):
    paper_rolls, max_row, max_col = day4_file_read(filename)

    removed = 0
    while paper_rolls:
        remove = set()
        for roll in paper_rolls:
            num_in_range = 0
            for check in check_locs:
                loc_check = tuple(x + y for x, y in zip(roll, check))

                if loc_check[0] < 0 or loc_check[1] < 0 or loc_check[0] == max_row or loc_check[1] == max_col:
                    # out of bounds
                    continue

                if loc_check in paper_rolls:
                    num_in_range += 1
                
                if num_in_range == 4:
                    # no need to process other directions
                    break

            if num_in_range != 4:
                # remove paper roll
                remove.add(roll)

        if not remove:
            break

        paper_rolls = paper_rolls.difference(remove)
        removed += len(remove)

    print(f'Day 4 part 2 {filename} results: {removed}')

# day4_part_1("sample.txt")
# day4_part_1("input.txt")

day4_part_2("sample.txt")
day4_part_2("input.txt")
