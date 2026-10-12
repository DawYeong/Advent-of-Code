import os

if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))


def day5_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read()

    raw_fresh, raw_ingredients = data.split("\n\n")

    ranges = {tuple(int(x) for x in row.split('-')) for row in raw_fresh.split("\n")}
    ingredients = {int(r) for r in raw_ingredients.split("\n")}

    return ranges, ingredients

def day5_part_1(filename):
    ranges, ingredients = day5_file_read(filename)

    fresh = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                fresh += 1
                break


    print(f"Day 5 part 1 {filename} results: {fresh}")


def day5_part_2(filename):
    ranges, _ = day5_file_read(filename)

    # merge the ranges
    sorted_ranges = sorted(ranges, key=lambda item: item[0])

    pointer = 1
    curr_range = 0

    merged_ranges = [sorted_ranges[0]]

    while pointer < len(sorted_ranges):

        # If the pointer range start is smaller than the merged range end, that means the ranges intersect and we will grab the maxes
        # We can guarantee that the mins can remain because the ranges are pre sorted
        if sorted_ranges[pointer][0] <= merged_ranges[curr_range][1]:
            # merge ranges and move on
            merged_ranges[curr_range] = (merged_ranges[curr_range][0] ,max(merged_ranges[curr_range][1], sorted_ranges[pointer][1]))
        else:
            # range is beyond the current merged range, we have to start a new merged range
            merged_ranges.append(sorted_ranges[pointer])
            curr_range += 1

        pointer += 1

    num_of_fresh_id = 0
    # get the total sum
    for mr in merged_ranges:
        num_of_fresh_id += (mr[1] - mr[0] + 1)

    print(f"Day 5 part 2 {filename} results: {num_of_fresh_id}")
        

# day5_part_1("sample.txt")
# day5_part_1("input.txt")

day5_part_2("sample.txt")
day5_part_2("input.txt")
