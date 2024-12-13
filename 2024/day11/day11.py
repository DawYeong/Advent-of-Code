# https://adventofcode.com/2024/day/11


def day11_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return data.split(" ")


def rule(stone):
    if stone == "0":
        return ["1"]
    elif len(stone) % 2 == 0:
        # split stone
        return [str(stone[0 : len(stone) // 2]), str(int(stone[len(stone) // 2 :]))]
    else:
        return [str(int(stone) * 2024)]


def calculate_num_stones(initial_stones, num_blinks):
    cache = {}

    def blink_stone(stone, blinks_left):
        # no blinks left => no stone change
        if blinks_left == 0:
            return 1

        # found in cache => don't recompute
        if (stone, blinks_left) in cache:
            return cache[(stone, blinks_left)]

        num_stones = 0
        # traverse new stones
        new_stones = rule(stone)
        for s in new_stones:
            num_stones += blink_stone(s, blinks_left - 1)

        # save results in cache
        cache[(stone, blinks_left)] = num_stones

        return num_stones

    results = 0
    for stone in initial_stones:
        results += blink_stone(stone, num_blinks)

    return results


def day11_part_1(filename):
    initial_stones = day11_file_read(filename)

    results = calculate_num_stones(initial_stones, 25)

    print(f"Day 11 part 1 {filename} results: {results}")


def day11_part_2(filename):
    initial_stones = day11_file_read(filename)

    results = calculate_num_stones(initial_stones, 75)

    print(f"Day 11 part 2 {filename} results: {results}")


day11_part_1("sample.txt")
day11_part_1("input.txt")

day11_part_2("sample.txt")
day11_part_2("input.txt")
