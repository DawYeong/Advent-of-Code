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
        


day1_part1('sample.txt')
day1_part1('input.txt')
