from io import TextIOWrapper
import sys
from typing import Iterable


def is_report_safe(report: Iterable[int]) -> bool:
    direction = 0  # decreasing = -1, neutral = 0, increasing = 1
    last_level = next(report)
    safe = True

    for cur_level in report:
        diff = cur_level - last_level
        abs_diff = abs(diff)
        monotonic = (
            direction == 0
            or (diff <= 0 and direction == -1)
            or (diff >= 0 and direction == 1)
        )
        last_level = cur_level

        if abs_diff < 1 or abs_diff > 3 or not monotonic:
            safe = False
            break
        elif diff < 0:
            direction = -1
        elif diff > 0:
            direction = 1

    return safe


def part1(input: TextIOWrapper) -> int:
    return sum(is_report_safe(int(level) for level in line.split()) for line in input)


def part2(input: TextIOWrapper) -> int:
    safe_reports = 0

    for line in input:
        original_report = [int(level) for level in line.split()]

        if is_report_safe(iter(original_report)):
            safe_reports += 1
            continue
        
        for i in range(len(line)):
            report = iter(original_report[0:i] + original_report[i+1:])

            if is_report_safe(report):
                safe_reports += 1
                break

    return safe_reports


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
