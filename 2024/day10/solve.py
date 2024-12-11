from io import TextIOWrapper
import sys

Vec2 = tuple[int, int]
Map = dict[Vec2, int]

UDLR = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT


def parse_map(input: TextIOWrapper) -> tuple[Map, set[Vec2]]:
    map = Map()
    trailheads = set[Vec2]()

    for row, line in enumerate(input):
        for col, char in enumerate(line.strip()):
            coord, height = (row, col), int(char)
            map[coord] = height

            if height == 0:
                trailheads.add(coord)

    return map, trailheads


def get_trail_ends(map: Map, start: Vec2) -> list[Vec2]:
    def helper(tail: Vec2) -> list[Vec2]:
        if (tail_height := map[tail]) == 9:
            return [tail]

        ends = list[Vec2]()

        for row, col in UDLR:
            adj: Vec2 = (tail[0] + row, tail[1] + col)

            if (adj_height := map.get(adj)) is None:
                continue
            elif adj_height != (tail_height + 1):
                continue

            ends += helper(adj)

        return ends

    return helper(start)


def part1(input: TextIOWrapper) -> int:
    map, trailheads = parse_map(input)
    unique_ends = (set(get_trail_ends(map, trailhead)) for trailhead in trailheads)
    return sum(len(re) for re in unique_ends)


def part2(input: TextIOWrapper) -> int:
    map, trailheads = parse_map(input)
    trail_ends = (get_trail_ends(map, trailhead) for trailhead in trailheads)
    return sum(len(te) for te in trail_ends)


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
