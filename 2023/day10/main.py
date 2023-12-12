from collections import defaultdict
from enum import IntEnum
from io import TextIOWrapper


class Direction(IntEnum):
    NORTH = 0b1000
    SOUTH = 0b0100
    EAST = 0b0010
    WEST = 0b0001

    NORTHEAST = 0b1010
    NORTHSOUTH = 0b1100
    NORTHWEST = 0b1001

    SOUTHEAST = 0b0110
    SOUTHWEST = 0b0101
    


SYMBOL_TO_PIPE_DIRS = {
    "|": Direction.NORTH | Direction.SOUTH,
    "-": Direction.EAST | Direction.WEST,
    "L": Direction.NORTH | Direction.EAST,
    "J": Direction.NORTH | Direction.WEST,
    "7": Direction.SOUTH | Direction.WEST,
    "F": Direction.SOUTH | Direction.EAST,
    ".": 0b0000,
}

PIPE_DIRS_TO_SYMBOLS = {dirs: symbol for symbol, dirs in SYMBOL_TO_PIPE_DIRS.items()}

Coord = tuple[int, int]
Map = dict[Coord, int]

def parse_map(file: TextIOWrapper) -> tuple[Map, Coord]:
    result = {}
    start = None
    rows, cols = 0, 0

    for row, line in enumerate(file):
        for col, symbol in enumerate(line.strip()):
            cols += 1
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


def longest_loop(map: Map, start: Coord) -> list[Coord]:
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

    return result[:-1]


def calculate_start(loop: list[Coord]) -> int:
    start = loop[0]
    adj_1 = (loop[-1][0] - start[0], loop[-1][1] - start[1])
    adj_2 = (loop[1][0] - start[0], loop[1][1] - start[1])

    match adj_1, adj_2:
        case (1, 0), (0, 1):
            return SYMBOL_TO_PIPE_DIRS["F"]
        case (1, 0), (-1, 0):
            return SYMBOL_TO_PIPE_DIRS["-"]
        case (1, 0), (0, -1):
            return SYMBOL_TO_PIPE_DIRS["L"]
        case (0, 1), (-1, 0):
            return SYMBOL_TO_PIPE_DIRS["7"]
        case (0, 1), (0, -1):
            return SYMBOL_TO_PIPE_DIRS["|"]
        case (0, 1), (1, 0):
            return SYMBOL_TO_PIPE_DIRS["F"]
        case (-1, 0), (0, -1):
            return SYMBOL_TO_PIPE_DIRS["J"]
        case (-1, 0), (1, 0):
            return SYMBOL_TO_PIPE_DIRS["-"]
        case (-1, 0), (0, 1):
            return SYMBOL_TO_PIPE_DIRS["7"]
        case (0, -1), (1, 0):
            return SYMBOL_TO_PIPE_DIRS["L"]
        case (0, -1), (0, 1):
            return SYMBOL_TO_PIPE_DIRS["|"]
        case (0, -1), (-1, 0):
            return SYMBOL_TO_PIPE_DIRS["J"]
        case adj:
            raise NotImplementedError(adj)


def get_loop_positive_tiles(loop: list[Coord], map: Map) -> set[Coord]:
    min_pipe = min(loop)
    min_pipe_index = loop.index(min_pipe)

    pos_dir = Direction.SOUTHEAST
    pos_coords = set[Coord]()
    last_pipe_value = map[min_pipe]

    for pipe in loop[min_pipe_index + 1:] + loop[:min_pipe_index]:
        match pos_dir:
            case Direction.NORTH:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_dir = Direction.NORTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.SOUTH:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_dir = Direction.SOUTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["-"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.EAST:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.EAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.WEST:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.WEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["|"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.SOUTHEAST:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.EAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_dir = Direction.SOUTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.EAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_dir = Direction.SOUTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.SOUTHWEST:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_dir = Direction.SOUTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.WEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.WEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_dir = Direction.SOUTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.NORTHEAST:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_dir = Direction.NORTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.EAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_dir = Direction.NORTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.EAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["7"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.SOUTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["L"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case Direction.NORTHWEST:
                if last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.WEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_dir = Direction.NORTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["F"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["L"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["|"]:
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.WEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["J"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.NORTHWEST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["-"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_dir = Direction.NORTH
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["F"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] - 1))
                    pos_coords.add((pipe[0] + 1, pipe[1]))
                    pos_dir = Direction.NORTHEAST
                elif last_pipe_value == SYMBOL_TO_PIPE_DIRS["J"] and map[pipe] == SYMBOL_TO_PIPE_DIRS["7"]:
                    pos_coords.add((pipe[0], pipe[1] + 1))
                    pos_coords.add((pipe[0] - 1, pipe[1]))
                    pos_dir = Direction.SOUTHWEST
                else:
                    raise NotImplementedError((PIPE_DIRS_TO_SYMBOLS[last_pipe_value], PIPE_DIRS_TO_SYMBOLS[map[pipe]]))
            case dir:
                raise NotImplementedError(dir)
            
        last_pipe_value = map[pipe]

    return pos_coords

def get_loop_num_enclosed_tiles(loop: list[Coord], map: Map) -> set[Coord]:
    pos_coords = {coord for coord in get_loop_positive_tiles(loop, map) if coord in map and coord not in loop}
    enclosed_tiles = set(pos_coords)
    loop = set(loop)

    while len(pos_coords) != 0:
        to_check = {pos_coords.pop()}

        while len(to_check) != 0:
            col, row = to_check.pop()
            adj = [
                (col - 1, row),
                (col + 1, row),
                (col, row - 1),
                (col, row + 1),
            ]

            for a in adj:
                if a in loop:
                    continue
                elif a not in map:
                    assert False
                elif a not in enclosed_tiles:
                    to_check.add(a)
                    enclosed_tiles.add(a)

    return len(enclosed_tiles)

def part1and2(file: TextIOWrapper) -> int:
    map, start = parse_map(file)
    loop = longest_loop(map, start)
    map[start] = calculate_start(loop)

    return len(loop) // 2, get_loop_num_enclosed_tiles(loop, map)

if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1and2(file))
