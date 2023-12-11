from collections import defaultdict
from io import TextIOWrapper

Coord = tuple[int, int]

def parse_map(file: TextIOWrapper, expansion_factor: int) -> set[Coord]:
    galaxies = set[Coord]()
    empty_columns = defaultdict(lambda: True)
    line_padding = 0

    for row, line in enumerate(file):
        empty_line = True

        for col, symbol in enumerate(line.strip()):
            if symbol == "#":
                empty_line = False
                empty_columns[col] = False
                galaxies.add((row + line_padding, col))
            else:
                empty_columns[col] = empty_columns[col] and True
            
        if empty_line:
            line_padding += expansion_factor - 1

    empty_columns = {col for col, empty in empty_columns.items() if empty}

    column_expanded_galaxies = set[Coord]()
    for galaxy_row, galaxy_col in galaxies:
        new_galaxy_col = galaxy_col
        
        for col in empty_columns:
            if col < galaxy_col:
                new_galaxy_col += expansion_factor - 1

        column_expanded_galaxies.add((galaxy_row, new_galaxy_col))

    return column_expanded_galaxies


def calculate(file, expansion_factor: int) -> int:
    galaxies = parse_map(file, expansion_factor)
    distances = dict[tuple[Coord, Coord], int]()
    
    for galaxy_a in galaxies:
        for galaxy_b in galaxies:
            if (galaxy_a, galaxy_b) not in distances and (galaxy_b, galaxy_a) not in distances:
                galaxy_a_row, galaxy_a_col = galaxy_a
                galaxy_b_row, galaxy_b_col = galaxy_b

                distances[(galaxy_a, galaxy_b)] = abs(galaxy_a_row - galaxy_b_row) + abs(galaxy_a_col - galaxy_b_col)

    return sum(distances.values())

if __name__ == "__main__":
    with open("input.txt") as file:
        print(calculate(file, expansion_factor=2))

    with open("input.txt") as file:
        print(calculate(file, expansion_factor=1000000))