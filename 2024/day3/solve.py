from io import TextIOWrapper
import re
import sys

PATTERN = re.compile("mul\\(([0-9]+),([0-9]+)\\)")

def part1(input: TextIOWrapper) -> int:
    memory = "".join(line for line in input)
    result = 0

    for i in range(len(memory)):
        if not (match := PATTERN.match(memory, i)):
            continue

        left, right = match.groups()

        result += int(left) * int(right)
        i = match.end()

    return result

def part2(input: TextIOWrapper) -> int:
    memory = "".join(line for line in input)
    result = 0
    enabled = True

    for i in range(len(memory)):
        if (match := PATTERN.match(memory, i)):
            if enabled:
                left, right = match.groups()
                result += int(left) * int(right)

            i = match.end()
        elif memory.startswith("do()", i):
            enabled = True
            i += 4
        elif memory.startswith("don't()", i):
            enabled = False
            i += 7

    return result


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
