from io import TextIOWrapper
import sys

Vec2 = tuple[int, int]
Map = dict[Vec2, int]
Trail = list[Vec2]

UDLR = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def parse_map(input: TextIOWrapper) -> tuple[Map, set[Vec2]]:
    map = Map()
    trailheads = set[Vec2]()

    for row, line in enumerate(input):
        for col, char in enumerate(line.strip()):
            if char == ".":
                continue

            coord, height = (row, col), int(char)
            map[coord] = height

            if height == 0:
                trailheads.add(coord)

    return map, trailheads


def get_reachable_ends(map: Map, start: Vec2) -> set[Vec2]:
    def helper(tail: Vec2) -> set[Vec2]:
        ends = list[Vec2]()
        tail_height = map[tail]

        if tail_height == 9:
            ends.append(tail)
        else:
            for row, col in UDLR:
                adj: Vec2 = (tail[0] + row, tail[1] + col)

                if (adj_height := map.get(adj)) is None:
                    continue
                elif adj_height != (tail_height + 1):
                    continue

                ends.extend(helper(adj))

        return set(ends)

    return helper(start)


def part1(input: TextIOWrapper) -> int:
    map, trailheads = parse_map(input)
    return sum(len(get_reachable_ends(map, trailhead)) for trailhead in trailheads)


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
