from collections import defaultdict
from io import TextIOWrapper
import sys
from typing import Mapping


Vec2 = tuple[int, int]


def parse_map(input: TextIOWrapper) -> tuple[Mapping[str, set[Vec2]], int]:
    map = defaultdict[str, set[Vec2]](set[Vec2])
    map_size = 0

    for row, line in enumerate(input):
        line = line.strip()
        map_size = max(map_size, len(line))

        for col, char in enumerate(line):
            if char == ".":
                continue

            map[char].add((row, col))

    return map, map_size


def find_antinodes(
    map: Mapping[str, set[Vec2]], map_size: int, max_reps: int = 1
) -> set[Vec2]:
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

                for i in range(1, max_reps + 1):
                    antinode = (row1 - row_diff * i, col1 - col_diff * i)

                    if (0 <= antinode[0] < map_size) and (0 <= antinode[1] < map_size):
                        antinodes.add(antinode)
                    else:
                        break

                for i in range(1, max_reps + 1):
                    antinode = (row2 + row_diff * i, col2 + col_diff * i)

                    if (0 <= antinode[0] < map_size) and (0 <= antinode[1] < map_size):
                        antinodes.add(antinode)
                    else:
                        break

                pairs.add((antenna1, antenna2))

    return antinodes


def part1(input: TextIOWrapper) -> int:
    map, map_size = parse_map(input)
    return len(find_antinodes(map, map_size))


def part2(input: TextIOWrapper) -> int:
    map, map_size = parse_map(input)
    antinodes = find_antinodes(map, map_size, max_reps=map_size * map_size)
    return len(antinodes.union(*map.values()))


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
