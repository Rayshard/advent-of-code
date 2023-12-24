from collections import defaultdict
from io import TextIOWrapper


def print_map(garden_plots: set[tuple[int, int]], possible_positions: dict[tuple[int, int], int], start: tuple[int, int], max_row: int, max_col: int) -> None:
    for row in range(0, max_row + 1):
        line = ""

        for col in range(0, max_col + 1):
            if (row, col) in garden_plots:
                if (row, col) in possible_positions:
                    assert possible_positions[(row, col)] > 0
                    line += str(possible_positions[(row, col)])
                elif (row, col) == start:
                    line += "S"
                else:
                    line += "."
            else:
                line += "#"

        print(line)


def part1(file: TextIOWrapper) -> int:
    garden_plots = set[tuple[int, int]]()
    start = None
    max_row, max_col = 0, 0

    for row, line in enumerate(file):
        for col, tile in enumerate(line.strip()):
            pos = (row, col)
            if tile == ".":
                garden_plots.add(pos)
            elif tile == "S":
                garden_plots.add(pos)
                start = pos

        max_row, max_col = row, col

    max_row_plus_1, max_col_plus_1 = max_row + 1, max_col + 1
    possible_positions = {start: 1}

    for _ in range(10):
        next_pps = defaultdict[tuple[int, int], int](int)
        next_pps.update(possible_positions)

        for (row, col), count in possible_positions.items():
            assert count != 0
            adj = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
            ]

            for a_row, a_col in adj:
                a_row_modded, a_col_modded = a_row % max_row_plus_1, a_col % max_col_plus_1
                if a_row < 0 or a_row > max_row or a_col < 0 or a_col > max_col:
                    next_pps[(a_row_modded, a_col_modded)] += 1
                elif (a_row, a_col) in garden_plots:
                    next_pps[(a_row_modded, a_col_modded)] = 1

            next_pps[(row, col)] -= 1
            if next_pps[(row, col)] == 0:
                next_pps.pop((row, col))

        possible_positions = next_pps
        print_map(garden_plots, possible_positions, start, max_row, max_col)
        print()

    return sum(possible_positions.values())



if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
