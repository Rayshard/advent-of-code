from io import TextIOWrapper
import sys


def get_char(map: list[str], row: int, col: int) -> str | None:
    if row < 0 or row >= len(map):
        return None

    line = map[row]

    if col < 0 or col >= len(line):
        return None

    return line[col]


def get_num_xmas(origin: tuple[int, int], map: list[str]) -> int:
    origin_row, origin_col = origin
    count = 0

    spans = [
        [(0, -1), (0, -2), (0, -3)],  # west
        [(0, 1), (0, 2), (0, 3)],  # east
        [(-1, 0), (-2, 0), (-3, 0)],  # north
        [(1, 0), (2, 0), (3, 0)],  # south
        [(-1, -1), (-2, -2), (-3, -3)],  # northwest
        [(-1, 1), (-2, 2), (-3, 3)],  # northeast
        [(1, -1), (2, -2), (3, -3)],  # southwest
        [(1, 1), (2, 2), (3, 3)],  # southeast
    ]

    for (m_row, m_col), (a_row, a_col), (s_row, s_col) in spans:
        M, A, S = (
            get_char(map, origin_row + m_row, origin_col + m_col),
            get_char(map, origin_row + a_row, origin_col + a_col),
            get_char(map, origin_row + s_row, origin_col + s_col),
        )

        if (M, A, S) == ("M", "A", "S"):
            count += 1

    return count


def is_x_mas(origin: tuple[int, int], map: list[str]) -> bool:
    origin_row, origin_col = origin

    possibilities = {
        ("M", "M", "S", "S"),
        ("M", "S", "M", "S"),
        ("S", "S", "M", "M"),
        ("S", "M", "S", "M"),
    }

    chars = (
        get_char(map, origin_row - 1, origin_col - 1),  # top-left
        get_char(map, origin_row - 1, origin_col + 1),  # top-right
        get_char(map, origin_row + 1, origin_col - 1),  # bottom-left
        get_char(map, origin_row + 1, origin_col + 1),  # bottom-right
    )

    return chars in possibilities


def part1(input: TextIOWrapper) -> int:
    possible_origins = list[tuple[int, int]]()
    map = list[str]()

    # Build the map
    for row, line in enumerate(input):
        map.append(line)

        for col, char in enumerate(line):
            if char == "X":
                possible_origins.append((row, col))

    return sum(
        get_num_xmas(possible_origin, map) for possible_origin in possible_origins
    )


def part2(input: TextIOWrapper) -> int:
    possible_origins = list[tuple[int, int]]()
    map = list[str]()

    # Build the map
    for row, line in enumerate(input):
        map.append(line)

        for col, char in enumerate(line):
            if char == "A":
                possible_origins.append((row, col))

    return sum(
        is_x_mas(possible_origin, map) for possible_origin in possible_origins
    )


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
