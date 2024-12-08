from collections import defaultdict
from io import TextIOWrapper
import sys
from typing import Mapping


Vec2 = tuple[int, int]


def find_antinodes(map: Mapping[str, set[Vec2]], map_size: int) -> set[Vec2]:
    pairs = set[tuple[Vec2, Vec2]]()
    antinodes = set[tuple[Vec2]]()

    for antenna in map.values():
        for antenna1 in antenna:
            row1, col1 = antenna1

            for antenna2 in antenna:
                row2, col2 = antenna2

                if antenna1 == antenna2:
                    continue
                elif (antenna1, antenna2) in pairs or (antenna2, antenna1) in pairs:
                    continue

                row_diff, col_diff = row2 - row1, col2 - col1
                antinode1 = (row1 - row_diff, col1 - col_diff)
                antinode2 = (row2 + row_diff, col2 + col_diff)

                if (0 <= antinode1[0] < map_size) and (0 <= antinode1[1] < map_size):
                    antinodes.add(antinode1)

                if (0 <= antinode2[0] < map_size) and (0 <= antinode2[1] < map_size):
                    antinodes.add(antinode2)

                pairs.add((antenna1, antenna2))

    return antinodes


def part1(input: TextIOWrapper) -> int:
    map = defaultdict[str, set[Vec2]](set[Vec2])
    map_size = 0

    for row, line in enumerate(input):
        line = line.strip()
        map_size = max(map_size, len(line))

        for col, char in enumerate(line):
            if char == ".":
                continue

            map[char].add((row, col))

    return len(find_antinodes(map, map_size))


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
