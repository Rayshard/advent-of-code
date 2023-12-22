from io import TextIOWrapper


def print_map(garden_plots: set[tuple[int, int]], possible_positions: set[tuple[int, int]], start: tuple[int, int], max_row: int, max_col: int) -> None:
    for row in range(0, max_row + 1):
        line = ""

        for col in range(0, max_col + 1):
            if (row, col) in garden_plots:
                if (row, col) in possible_positions:
                    line += "O"
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

    possible_positions = {start}

    for _ in range(64):
        next_pps = set[tuple[int, int]]()

        while possible_positions:
            (row, col) = possible_positions.pop()
            adj = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
            ]

            for a_row, a_col in adj:
                if a_row < 0 or a_row > max_row or a_col < 0 or a_col > max_col:
                    continue
                elif (a_row, a_col) in garden_plots:
                    next_pps.add((a_row, a_col))

        possible_positions = next_pps

    return len(possible_positions)



if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
