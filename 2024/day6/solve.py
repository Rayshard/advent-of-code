from io import TextIOWrapper
import sys
from typing import Literal

Direction = Literal["U", "D", "L", "R"]
Vec2 = tuple[int, int]
TerminationReason = Literal["OFF_MAP", "LOOP"]


def read_map(input: TextIOWrapper) -> tuple[Vec2, set[Vec2], Vec2]:
    obstacles = set[Vec2]()

    lines = list(line.strip() for line in input)
    map_size = len(lines[0]), len(lines)
    guard_pos: Vec2 | None = None

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
    return map_size, obstacles, guard_pos


def simulate(
    map_size: Vec2, obstacles: set[Vec2], guard_pos: Vec2
) -> tuple[set[tuple[Vec2, Direction]], TerminationReason]:
    map_width, map_height = map_size
    guard_row, guard_col = guard_pos
    guard_dir: Direction = "U"
    tiles_touched = set[tuple[Vec2, Direction]]()

    termination_reason: TerminationReason = "OFF_MAP"

    while 0 <= guard_row < map_height and 0 <= guard_col < map_width:
        if (pair := (guard_pos, guard_dir)) in tiles_touched:
            termination_reason = "LOOP"
            break

        tiles_touched.add(pair)

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

    return tiles_touched, termination_reason


def part1(input: TextIOWrapper) -> int:
    (map_width, map_height), obstacles, guard_pos = read_map(input)
    tiles_touched, _ = simulate((map_width, map_height), obstacles, guard_pos)

    return len(set(tile_pos for tile_pos, _ in tiles_touched))


def part2(input: TextIOWrapper) -> int:
    (map_width, map_height), obstacles, guard_pos = read_map(input)

    # Run simulation with no additional obstacles to narrow down how many
    # new obstacles we need to test for
    tiles_touched, _ = simulate((map_width, map_height), obstacles, guard_pos)
    additional_obstacles = {tile_pos for tile_pos, dir in tiles_touched}

    # Don't wanna place an obstacle on the starting pos
    additional_obstacles.remove(guard_pos)

    # Simulate with each additional obstacle and check for a loop
    loops = 0

    for additional_obstacle in additional_obstacles:
        _, termination_reason = simulate(
            (map_width, map_height), obstacles | {additional_obstacle}, guard_pos
        )

        if termination_reason == "LOOP":
            loops += 1

    return loops


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
