from io import TextIOWrapper
import sys
from typing import Literal

Direction = Literal["U", "D" , "L", "R"]

def part1(input: TextIOWrapper) -> int:
    obstacles = set[tuple[int, int]]()

    lines = list(line.strip() for line in input)
    map_width, map_height = len(lines[0]), len(lines)
    guard_pos : tuple[int, int] | None = None

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            match char:
                case ".":
                    continue
                case "#":
                    obstacles.add((row, col))
                case "^":
                    guard_pos = (row, col)
                    continue
                case char:
                    raise NotImplementedError(char)

    assert guard_pos is not None
    guard_row, guard_col = guard_pos
    guard_dir :Direction= "U"
    tiles_touched = set[tuple[int, int]]()

    while (0 <= guard_row < map_height and 0<= guard_col < map_width):
        tiles_touched.add(guard_pos)

        match guard_dir:
            case "U":
                new_pos = (guard_row - 1, guard_col)
                new_dir = "R"
            case "D":
                new_pos = (guard_row + 1, guard_col)
                new_dir = "L"
            case "L":
                new_pos = (guard_row, guard_col - 1)
                new_dir = "U"
            case "R":
                new_pos = (guard_row, guard_col + 1)
                new_dir = "D"

        if new_pos in obstacles:
            guard_dir = new_dir
        else:
            guard_row, guard_col = guard_pos = new_pos

    return len(tiles_touched)


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
