from collections import defaultdict
from dataclasses import dataclass, field
from io import TextIOWrapper
import sys
import time
import string
from typing import Optional


Vec2 = tuple[int, int]


@dataclass
class Region:
    tiles: set[Vec2] = field(default_factory=set[Vec2])
    perimeter: list[Vec2] = field(default_factory=list[Vec2])

    def calculate_num_sides(self) -> int:
        not_seen_perimeter_tiles = defaultdict[Vec2, int](int)
        num_sides = 0

        def mark_tile_seen(tile: Vec2) -> None:
            if not_seen_perimeter_tiles.get(tile) == 1:
                not_seen_perimeter_tiles.pop(tile)
            else:
                not_seen_perimeter_tiles[tile] -= 1

        def pop_unseen_tile() -> Vec2:
            tile, count = not_seen_perimeter_tiles.popitem()

            if count != 1:
                not_seen_perimeter_tiles[tile] = count - 1

            return tile

        for tile in self.perimeter:
            not_seen_perimeter_tiles[tile] += 1

        # print(not_seen_perimeter_tiles)
        # print("Sum", sum(not_seen_perimeter_tiles.values()))

        while not_seen_perimeter_tiles:
            tile = pop_unseen_tile()
            tile_row, tile_col = tile
            direction = None

            if ((tile_row - 1, tile_col) in not_seen_perimeter_tiles) or (
                (tile_row + 1, tile_col) in not_seen_perimeter_tiles
            ):
                direction = "vertical"
            elif ((tile_row, tile_col - 1) in not_seen_perimeter_tiles) or (
                tile_row,
                tile_col + 1,
            ) in not_seen_perimeter_tiles:
                direction = "horizontal"

            if direction == "vertical":
                tile_in_side = (tile_row - 1, tile_col)

                while tile_in_side in not_seen_perimeter_tiles:
                    mark_tile_seen(tile_in_side)
                    tile_in_side_row, tile_in_side_col = tile_in_side
                    tile_in_side = (tile_in_side_row - 1, tile_in_side_col)

                tile_in_side = (tile_row + 1, tile_col)

                while tile_in_side in not_seen_perimeter_tiles:
                    mark_tile_seen(tile_in_side)
                    tile_in_side_row, tile_in_side_col = tile_in_side
                    tile_in_side = (tile_in_side_row + 1, tile_in_side_col)
            elif direction == "horizontal":
                tile_in_side = (tile_row, tile_col - 1)

                while tile_in_side in not_seen_perimeter_tiles:
                    mark_tile_seen(tile_in_side)
                    tile_in_side_row, tile_in_side_col = tile_in_side
                    tile_in_side = (tile_in_side_row, tile_in_side_col - 1)

                tile_in_side = (tile_row, tile_col + 1)

                while tile_in_side in not_seen_perimeter_tiles:
                    mark_tile_seen(tile_in_side)
                    tile_in_side_row, tile_in_side_col = tile_in_side
                    tile_in_side = (tile_in_side_row, tile_in_side_col + 1)

            num_sides += 1

        return num_sides


def parse_map(input: TextIOWrapper) -> dict[Vec2, int]:
    map = dict[Vec2, int]()

    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char in string.whitespace:
                continue

            map[(row, col)] = ord(char)

    return map


def get_regions(map: dict[Vec2, int]) -> list[Region]:
    regions = list[Region]()
    not_seen = set(map.keys())

    while not_seen:
        region = Region()
        next = {not_seen.pop()}

        while next:
            tile = next.pop()
            tile_value = map[tile]
            row, col = tile

            adj = {
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            }

            for coord in adj:
                if map.get(coord) != tile_value:
                    region.perimeter.append(coord)
                elif coord not in not_seen:
                    continue
                else:
                    next.add(coord)

            not_seen.discard(tile)
            region.tiles.add(tile)

        regions.append(region)

    return regions


def part1(input: TextIOWrapper) -> int:
    map = parse_map(input)
    regions = get_regions(map)

    return sum((len(region.tiles) * len(region.perimeter)) for region in regions)


def part2(input: TextIOWrapper) -> int:
    map = parse_map(input)
    regions = get_regions(map)

    return sum((len(region.tiles) * region.calculate_num_sides()) for region in regions)


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
