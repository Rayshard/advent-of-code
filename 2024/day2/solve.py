from collections import defaultdict
from io import TextIOWrapper
import sys


def part1(input: TextIOWrapper) -> int:
    safe_levels = 0

    for line in input:
        report = (int(level) for level in line.split())
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

        if safe:
            safe_levels += 1

    return safe_levels


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
