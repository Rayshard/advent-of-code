from collections import defaultdict
from enum import IntEnum
from io import TextIOWrapper


class Direction(IntEnum):
    NORTH = 0b1000
    SOUTH = 0b0100
    EAST = 0b0010
    WEST = 0b0001


SYMBOL_TO_PIPE_DIRS = {
    "|": Direction.NORTH | Direction.SOUTH,
    "-": Direction.EAST | Direction.WEST,
    "L": Direction.NORTH | Direction.EAST,
    "J": Direction.NORTH | Direction.WEST,
    "7": Direction.SOUTH | Direction.WEST,
    "F": Direction.SOUTH | Direction.EAST,
    ".": 0b0000,
}

Coord = tuple[int, int]
Map = dict[Coord, int]

def parse_map(file: TextIOWrapper) -> tuple[Map, Coord]:
    result = {}
    start = None

    for row, line in enumerate(file):
        for col, symbol in enumerate(line.strip()):
            if symbol == "S":
                start = (col, row)
            else:
                result[(col, row)] = SYMBOL_TO_PIPE_DIRS[symbol]

    assert start is not None
    return result, start

def connecting_pipes(position: Coord, map: Map, start: Coord) -> list[Coord]:
    col, row = position
    
    if position ==  start:
        return [
            (col, row - 1),
            (col, row + 1),
            (col + 1, row),
            (col - 1, row)
        ]

    pipe = map[position]
    connecting = []
    
    if ((pipe & Direction.NORTH) and (north := map.get((col, row - 1))) is not None and (north & Direction.SOUTH)) or start == (col, row - 1):
        connecting.append((col, row - 1))

    if ((pipe & Direction.SOUTH)and (south := map.get((col, row + 1))) is not None and (south & Direction.NORTH)) or start == (col, row + 1):
        connecting.append((col, row + 1))

    if ((pipe & Direction.EAST) and (east := map.get((col + 1, row))) is not None and (east & Direction.WEST)) or start == (col + 1, row):
        connecting.append((col + 1, row))

    if ((pipe & Direction.WEST) and (west := map.get((col - 1, row))) is not None and (west & Direction.EAST)) or start == (col - 1, row):
        connecting.append((col - 1, row))

    return connecting


def longest_loop(map: Map, start: Coord) -> list[list[Coord]]:
    result = None
    paths = [[start]]
    
    while paths:
        new_paths = []

        for path in paths:
            last = path[-1]
            seen = set(path)

            for connecting in connecting_pipes(last, map, start):
                if connecting == start and len(path) > 2:
                    loop = path + [connecting]
                    
                    if result is None or len(loop) > len(result):
                        result = loop
                    
                    continue
                
                if connecting in seen:
                    continue

                new_paths.append(path + [connecting])

        paths = new_paths

    return result


def part1(file: TextIOWrapper) -> int:
    map, start = parse_map(file)
    return (len(longest_loop(map, start))) // 2

if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
