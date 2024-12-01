from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from io import TextIOWrapper


class Tile(Enum):
    Path = auto()
    Forest = auto()
    NSlope = auto()
    SSlope = auto()
    ESlope = auto()
    WSlope = auto()


Coord = tuple[int, int]
Map = dict[Coord, Tile]
Hike = tuple[Coord, set[Coord]]


def print_map(map: Map) -> None:
    max_row, max_col = max(map)

    for row in range(max_row + 1):
        line = ""

        for col in range(max_col + 1):
            match map[(row, col)]:
                case Tile.Forest:
                    line += "#"
                case Tile.Path:
                    line += "."
                case Tile.NSlope:
                    line += "^"
                case Tile.SSlope:
                    line += "v"
                case Tile.ESlope:
                    line += ">"
                case Tile.WSlope:
                    line += "<"
                case tile:
                    raise RuntimeError(f"Unknown tile: {tile}")

        print(line)


def parse_map(file: TextIOWrapper) -> Map:
    map = Map()

    for row, line in enumerate(file):
        for col, tile in enumerate(line.strip()):
            match tile:
                case ".":
                    map[(row, col)] = Tile.Path
                case "#":
                    map[(row, col)] = Tile.Forest
                case "^":
                    map[(row, col)] = Tile.NSlope
                case "v":
                    map[(row, col)] = Tile.SSlope
                case "<":
                    map[(row, col)] = Tile.WSlope
                case ">":
                    map[(row, col)] = Tile.ESlope
                case tile:
                    raise RuntimeError(f"Unknown tile: {tile}")

    return map


def part1(map: Map) -> int:
    max_row, max_col = max(map)

    for col in range(max_col + 1):
        if map[(0, col)] == Tile.Path:
            start = (0, col)

        if map[(max_row, col)] == Tile.Path:
            end = (max_row, col)

    hikes = [(start, set[Coord]())]
    longest_hike = 0

    while hikes:
        new_hikes = list[Hike]()

        for current_position, visited in hikes:
            if current_position == end:
                print(f"Hike ended in {len(visited)} steps")
                longest_hike = max(longest_hike, len(visited))
                continue

            visited.add(current_position)
            next_tiles = set[Coord]()

            match map[current_position]:
                case Tile.Forest:
                    raise RuntimeError("Hike is on forest")
                case Tile.Path:
                    next_tiles.update(
                        [
                            (current_position[0] - 1, current_position[1]),
                            (current_position[0] + 1, current_position[1]),
                            (current_position[0], current_position[1] - 1),
                            (current_position[0], current_position[1] + 1),
                        ]
                    )
                case Tile.NSlope:
                    next_tiles.add((current_position[0] - 1, current_position[1]))
                case Tile.SSlope:
                    next_tiles.add((current_position[0] + 1, current_position[1]))
                case Tile.ESlope:
                    next_tiles.add((current_position[0], current_position[1] + 1))
                case Tile.WSlope:
                    next_tiles.add((current_position[0], current_position[1] - 1))
                case tile:
                    raise RuntimeError(f"Unknown tile: {tile}")

            for row, col in next_tiles:
                if (row, col) in visited:
                    continue
                elif not (0 <= row <= max_row) or not (0 <= col <= max_col):
                    continue
                elif map[(row, col)] == Tile.Forest:
                    continue

                new_hikes.append(((row, col), set(visited)))

        hikes = new_hikes

    return longest_hike


def part2(map: Map) -> int:
    max_row, max_col = max(map)

    for col in range(max_col + 1):
        if map[(0, col)] == Tile.Path:
            start = (0, col)

        if map[(max_row, col)] == Tile.Path:
            end = (max_row, col)

    hikes = [(start, set[Coord]())]
    longest_hike = 0

    while hikes:
        new_hikes = list[Hike]()

        for current_position, visited in hikes:
            if current_position == end:
                print(f"Hike ended in {len(visited)} steps")
                longest_hike = max(longest_hike, len(visited))
                continue

            visited.add(current_position)

            next_tiles = [
                (current_position[0] - 1, current_position[1]),
                (current_position[0] + 1, current_position[1]),
                (current_position[0], current_position[1] - 1),
                (current_position[0], current_position[1] + 1)
            ]

            for row, col in next_tiles:
                if (row, col) in visited:
                    continue
                elif not (0 <= row <= max_row) or not (0 <= col <= max_col):
                    continue
                elif map[(row, col)] == Tile.Forest:
                    continue

                new_hikes.append(((row, col), set(visited)))

        hikes = new_hikes

    return longest_hike


def part2(map: Map) -> int:
    max_row, max_col = max(map)

    for col in range(max_col + 1):
        if map[(0, col)] == Tile.Path:
            start = (0, col)

        if map[(max_row, col)] == Tile.Path:
            end = (max_row, col)

    hikes = dict[Coord, set[Coord]]()
    hikes[start] = set[Coord]()
    longest_hike = 0

    while hikes:
        current_position, visited = hikes.popitem()

        if current_position == end:
            print(f"Hike ended in {len(visited)} steps")
            longest_hike = max(longest_hike, len(visited))
            continue

        visited.add(current_position)

        next_tiles = [
            (current_position[0] - 1, current_position[1]),
            (current_position[0] + 1, current_position[1]),
            (current_position[0], current_position[1] - 1),
            (current_position[0], current_position[1] + 1)
        ]

        for row, col in next_tiles:
            if (row, col) in visited:
                continue
            elif not (0 <= row <= max_row) or not (0 <= col <= max_col):
                continue
            elif map[(row, col)] == Tile.Forest:
                continue
            elif (row, col) in hikes and len(hikes[(row, col)]) < len(visited):
                continue

            hikes[(row, col)] = set(visited)

    return longest_hike

if __name__ == "__main__":
    with open("input.txt") as file:
        map = parse_map(file)

    # print(part1(map))
    print(part2(map))
