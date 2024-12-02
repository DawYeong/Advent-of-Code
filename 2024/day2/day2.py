# https://adventofcode.com/2024/day/2


def day2_file_read(filename):
    with open(filename, 'r') as file:
        data = file.read().split("\n")

    reports = [[int(el) for el in line.split(' ')] for line in data]

    return reports

def day2_part1(filename):
    reports = day2_file_read(filename)

    def is_report_safe(report):
        prev_dir = None

        for i in range(len(report)-1):
            distance = report[i] - report[i+1]
            
            if not (1 <= abs(distance) <= 3):
                return False
            
            # False: negative, True: positive
            next_dir = distance > 0
            if (prev_dir != None and prev_dir != next_dir):
                return False
            
            prev_dir = next_dir

        return True
    
    safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            safe_reports += 1

    print(f"Day 2 part 1 {filename} results: {safe_reports}")

def day2_part2(filename):
    reports = day2_file_read(filename)

    def is_level_safe(a, b, prev_dir):
        distance = a - b
        print(a, b)

        if not (1 <= abs(distance) <= 3):
            return False, None, 1
        
        next_dir = distance > 0
        if (prev_dir != None and prev_dir != next_dir):
            return False, None, 2
        
        return True, next_dir, 0

    def check_report(report):
        prev_dir = None

        for i in range(len(report)-1):
            distance = report[i] - report[i+1]
            
            if not (1 <= abs(distance) <= 3):
                return i
            
            next_dir = distance > 0
            if (prev_dir != None and prev_dir != next_dir):
                return i
            
            prev_dir = next_dir

        return None

    # brute forcing, couldn't think of a better way to solve this... :(
    # basically if we have a failing report:
    # => remove current, next, and prev elements (each separate reports) and check again
    def is_report_safe(report, fail_count=0):
        if fail_count > 1:
            return False

        fail_index = check_report(report)

        if fail_index != None:
            # something has gone wrong, report element around fail index
            remove_curr = report[0:fail_index] + report[fail_index+1:]
            remove_prev = report[0:fail_index-1] + report[fail_index:]
            remove_next = report[0:fail_index+1] + report[fail_index+2:]
            
            is_remove_curr_safe = is_report_safe(remove_curr, fail_count=fail_count+1)
            is_remove_prev_safe = is_report_safe(remove_prev, fail_count=fail_count+1)
            is_remove_next_safe = is_report_safe(remove_next, fail_count=fail_count+1)

            return is_remove_curr_safe or is_remove_prev_safe or is_remove_next_safe

        return True
    
    safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            safe_reports += 1


    print(f"Day 2 part 2 {filename} results: {safe_reports}")


day2_part1("sample.txt")
day2_part1("input.txt")

day2_part2("sample.txt")
day2_part2("input.txt")
