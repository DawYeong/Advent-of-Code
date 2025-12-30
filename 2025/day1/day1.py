import os


if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

def day1_file_read(filename):
    with open(filename, "r") as file:
        data = file.read()

    rotations = [line for line in data.split('\n')]
    return rotations

def day1_part1(filename):
    curr_point = 50
    rotations = day1_file_read(filename)
    pwd = 0
    
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == "L":
            curr_point -= distance
        else:
            curr_point += distance

        curr_point %= 100

        if curr_point == 0: pwd += 1

    print(f"Day 1 part 1 {filename} results: {pwd}")
        


def day1_part2(filename):
    curr_point = 50
    rotations = day1_file_read(filename)
    pwd = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        temp_point = curr_point
        if direction == "L":
            curr_point -= distance
        else:
            curr_point += distance

        if curr_point == 0: 
            pwd += 1
        else:
            cycles = abs(int(curr_point / 100))
            
            if curr_point < 0:
                cycles += 1 if temp_point != 0 else 0
            
            pwd += cycles

        curr_point %= 100

    print(f"Day 1 part 2 {filename} results: {pwd}")

day1_part1('sample.txt')
day1_part1('input.txt')

day1_part2('sample.txt')
day1_part2('input.txt')
