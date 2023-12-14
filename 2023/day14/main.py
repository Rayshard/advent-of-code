from collections import defaultdict
from io import TextIOWrapper
from typing import Optional


def parse_map(file: TextIOWrapper) -> tuple[list[str], list[str]]:
    map = tuple[list[str], list[str]]()
    
    rows = list[str]()
    cols = defaultdict[int, str](str)
    
    for line in file:
        line = line.strip()
        rows.append(line)

        for i, c in enumerate(line):
            cols[i] += c

    return rows, [col for _, col in sorted(cols.items())]


def part1(map: tuple[list[str], list[str]]) -> int:
    result = 0
    num_rows = len(map[0])

    for col in map[1]:
        next_open_slots = []

        for i, c in enumerate(col):
            if c == ".":
                next_open_slots.append(num_rows - i)
            elif c == "O":
                if next_open_slots:
                    result += next_open_slots[0]
                    next_open_slots = next_open_slots[1:] + [num_rows - i]
                else:
                    result += num_rows - i
            elif c == "#":
                next_open_slots = []

    return result

if __name__ == "__main__":
    with open("input.txt") as file:
        map = parse_map(file)

    print(part1(map))