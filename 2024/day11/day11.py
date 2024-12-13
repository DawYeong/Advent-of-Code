# https://adventofcode.com/2024/day/11


def day11_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    return data.split(" ")


def blink_stone(stone, blinks):
    blink = 0
    stones = [stone]
    while blink < blinks:
        blink += 1

        new_stones = []
        for s in stones:
            if s == "0":
                new_stones.append("1")
            elif len(s) % 2 == 0:
                # split stone
                new_stones.append(str(s[0 : len(s) // 2]))
                new_stones.append(str(int(s[len(s) // 2 :])))
            else:
                new_stones.append(str(int(s) * 2024))

        stones = new_stones

    return len(stones)


def day11_part_1(filename):
    initial_stones = day11_file_read(filename)

    results = 0

    for stone in initial_stones:
        results += blink_stone(stone, 25)

    print(f"Day 11 part 1 {filename} results: {results}")


day11_part_1("sample.txt")
day11_part_1("input.txt")
