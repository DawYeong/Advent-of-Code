# https://adventofcode.com/2024/day/2


def day2_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read().split("\n")

    reports = [[int(el) for el in line.split(' ')] for line in data]

    return reports

def day2_part1(filename):
    reports = day2_file_read(filename)

    def is_report_safe(report):
        prevDir = None

        for i in range(len(report)-1):
            distance = report[i] - report[i+1]
            
            if not (1 <= abs(distance) <= 3):
                return False
            
            # False: negative, True: positive
            nextDir = distance > 0
            if (prevDir != None and prevDir != nextDir):
                return False
            
            prevDir = nextDir

        return True
    
    safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            safe_reports += 1

    print(f"Day 2 part 1 {filename} results: {safe_reports}")


day2_part1("sample.txt")
day2_part1("input.txt")
