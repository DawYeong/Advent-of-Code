import os
from math import ceil, pow

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day2_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    ranges = [(r_s[0], r_s[1]) for r in data.split(',') if (r_s := r.split('-'))]

    return ranges


def day2_part_1(filename):
    data = day2_file_read(filename)
    print(f"DATA: {data}")
    # Process the data for part 1
    ranges = []
    for row in data:
        print(f"row: {row}")
        item_1_len = len(row[0])//2
        min_range = (row[0][:item_1_len] or "0", row[0][item_1_len:], len(row[0]))
        item_2_len = ceil(len(row[1])/2)
        max_range = (row[1][:item_2_len], row[1][item_2_len:] or "0", len(row[1]))
        ranges.append((min_range, max_range))
    
    print(ranges)
    invalid_sum = 0
    for idx, r in enumerate(ranges):
        curr = int(r[0][0]) if r[0][2] % 2 == 0 or r[0][2] == 1 else int(pow(10, len(r[0][0])))
        print(curr, r)
        invalid_in_range = []
        while(True):
            test_num = int(str(curr)*2)
            if test_num > int(data[idx][1]):
                break

            if test_num >= int(data[idx][0]):
                invalid_in_range.append(test_num)
                invalid_sum += test_num
            curr += 1

        print(invalid_in_range)

    
    print(f"Day 2 part 1 {filename} results: {invalid_sum}")
        


# day2_part_1("test.txt")
# day2_part_1("sample.txt")
day2_part_1("input.txt")

