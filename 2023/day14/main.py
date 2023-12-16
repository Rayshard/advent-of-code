from io import TextIOWrapper


def parse_map(file: TextIOWrapper) -> tuple[dict[tuple[int, int], str], str, tuple[int, int]]:
    map = dict[tuple[int, int], str]()
    map_as_str = ""

    for row, line in enumerate(file):
        line = line.strip()
        map_as_str += line

        for col, char in enumerate(line):
            map[(row, col)] = char

    max_row, max_col = max(map)
    return map, map_as_str, (max_row + 1, max_col + 1)


def map_to_str(map: dict[tuple[int, int], str], num_rows: int, num_cols: int) -> str:
    result = ""
    
    for row in range(num_rows):
        for col in range(num_cols):
            result += map[(row, col)]

    return result


def tilt_north(map: dict[tuple[int, int], str], num_rows: int, num_cols: int) -> int:
    for col in range(num_cols):
        next_open_slots = list[int]()

        for row in range(num_rows):
            c = map[(row, col)]

            if c == ".":
                next_open_slots.append(row)
            elif c == "O":
                if len(next_open_slots) != 0:
                    next_open_slot = next_open_slots.pop(0)
                    map[(next_open_slot, col)] = "O"
                    map[(row, col)] = "."
                    next_open_slots.append(row)
            elif c == "#":
                next_open_slots = []


def tilt_west(map: dict[tuple[int, int], str], num_rows: int, num_cols: int):
    for row in range(num_rows):
        next_open_slots = list[int]()

        for col in range(num_cols):
            match map[(row, col)]:
                case ".":
                    next_open_slots.append(col)
                case "O" if len(next_open_slots) != 0:
                    next_open_slot = next_open_slots.pop(0)
                    map[(row, next_open_slot)] = "O"
                    map[(row, col)] = "."
                    next_open_slots.append(col)
                case "#":
                    next_open_slots = []
                case "O":
                    pass
                case c:
                    raise RuntimeError(c)
                

def tilt_south(map: dict[tuple[int, int], str], num_rows: int, num_cols: int):
    for col in range(num_cols - 1, -1, -1):
        next_open_slots = list[int]()

        for row in range(num_rows - 1, -1, -1):
            match map[(row, col)]:
                case ".":
                    next_open_slots.append(row)
                case "O" if len(next_open_slots) != 0:
                    next_open_slot = next_open_slots.pop(0)
                    map[(next_open_slot, col)] = "O"
                    map[(row, col)] = "."
                    next_open_slots.append(row)
                case "#":
                    next_open_slots = []
                case "O":
                    pass
                case c:
                    raise RuntimeError(c)


def tilt_east(map: dict[tuple[int, int], str], num_rows: int, num_cols: int):
    for row in range(num_rows - 1, -1, -1):
        next_open_slots = list[int]()

        for col in range(num_cols - 1, -1, -1):
            match map[(row, col)]:
                case ".":
                    next_open_slots.append(col)
                case "O" if len(next_open_slots) != 0:
                    next_open_slot = next_open_slots.pop(0)
                    map[(row, next_open_slot)] = "O"
                    map[(row, col)] = "."
                    next_open_slots.append(col)
                case "#":
                    next_open_slots = []
                case "O":
                    pass
                case c:
                    raise RuntimeError(c)


def get_north_support(map: dict[tuple[int, int], str], num_rows: int, num_cols: int) -> int:
    result = 0
    
    for row in range(num_rows):
        for col in range(num_cols):
            if map[(row, col)] == "O":
                result += num_rows - row

    return result


def execute_cycle(map: dict[tuple[int, int], str], num_rows: int, num_cols: int, maps: set[str]) -> bool:
    seen = False

    tilt_north(map, num_rows, num_cols)
    if (map_as_str := map_to_str(map, num_rows, num_cols)) not in maps:
        maps.add(map_as_str)
    else:
        seen = True

    tilt_west(map, num_rows, num_cols)
    if (map_as_str := map_to_str(map, num_rows, num_cols)) not in maps:
        maps.add(map_as_str)
    else:
        seen = True

    tilt_south(map, num_rows, num_cols)
    if (map_as_str := map_to_str(map, num_rows, num_cols)) not in maps:
        maps.add(map_as_str)
    else:
        seen = True

    tilt_east(map, num_rows, num_cols)
    if (map_as_str := map_to_str(map, num_rows, num_cols)) not in maps:
        maps.add(map_as_str)
    else:
        seen = True
    
    return seen


def part1(file: TextIOWrapper) -> int:
    map, _, (num_rows, num_cols) = parse_map(file)
    tilt_north(map, num_rows, num_cols)

    return get_north_support(map, num_rows, num_cols)


def part2(file: TextIOWrapper) -> int:
    map, map_as_str, (num_rows, num_cols) = parse_map(file)
    maps = {map_as_str}

    for cycle in range(1_000_000_000):
        if execute_cycle(map, num_rows, num_cols, maps):
            for _ in range(1_000_000_000 % cycle + 2):
                execute_cycle(map, num_rows, num_cols, maps)

            break

    return get_north_support(map, num_rows, num_cols)


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

    with open("input.txt") as file:
        print(part2(file))
