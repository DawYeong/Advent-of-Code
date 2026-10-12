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
        

day5_part_1("sample.txt")
day5_part_1("input.txt")

