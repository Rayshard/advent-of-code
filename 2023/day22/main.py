from collections import defaultdict
from io import TextIOWrapper
from pprint import pprint as print, pformat as format


Coord = tuple[int, int, int]
Coord2D = tuple[int, int]


class Block:
    def __init__(self, start: Coord, end: Coord) -> None:
        (x1, y1, z1) = self.start = start
        (x2, y2, z2) = self.end = end

        assert x1 >= x2
        assert y1 >= y2
        assert z1 >= z2

    @property
    def min_z(self) -> int:
        self.start[2]

    @property
    def max_z(self) -> int:
        self.end[2]

    def __repr__(self) -> str:
        return format((self.start, self.end))


class Space:
    def __init__(self) -> None:
        self.blocks = defaultdict[int, dict[int, Block]](dict[int, Block])
        self.__max_z = 0
        self.__next_block_id = 0

    @property
    def max_z(self) -> int:
        return self.__max_z

    def add_block(self, block: Block) -> None:
        for z in range(block.min_z, block.max_z + 1):
            self.blocks[z][self.__next_block_id] = block

        self.__next_block_id += 1
        self.__max_z = max(self.__max_z, block.max_z)

    def __repr__(self) -> str:
        return format(self.blocks)


def parse_space(file: TextIOWrapper) -> Space:
    space = Space()

    for line in file:
        start, end = [tuple(map(int, item.split(","))) for item in line.strip().split("~")]
        space.add_block(Block(start, end))

    return space


def part1(file: TextIOWrapper) -> int:
    space = parse_space(file)
    print(space)

    iterations = 0
    while True:
        print((iterations := iterations + 1))
        new_space = Space()

        for block in space.blocks[1].values():
            new_space.add_block(block)

        changed = False
        handled = set[int]()

        for z in range(2, space.max_z + 1):
            current_plane = space.blocks[z]
            blocks_beneath = new_space.blocks[z - 1].values()

            for block_id, block in current_plane.items():
                if block_id in handled:
                    continue
                else:
                    handled.add(block_id)

                if block.bottom.intersection(plane_beneath):
                    new_space.add_block(block)
                else:
                    new_space.add_block(Block({(x, y, z - 1) for (x, y, z) in block.bricks}))
                    changed = True

        space = new_space

        if not changed:
            break

    handled = set(space.blocks[space.max_z].keys())
    can_disintegrate = len(space.blocks[space.max_z].keys())

    supports = defaultdict[int, set[int]](set[int])
    supported = defaultdict[int, set[int]](set[int])

    for z in range(1, space.max_z):
        current_plane = space.blocks[z]
        blocks_above = new_space.blocks[z + 1]

        for block_id, block in current_plane.items():
            if block_id in handled:
                continue
            else:
                handled.add(block_id)

            for block_above_id, block_above in blocks_above.items():
                if block.top.intersection(block_above.bottom):
                    supports[block_id].add(block_above_id)
                    supported[block_above_id].add(block_id)

    for block_id, supported_block_ids in supports.items():
        can_be_disintergrated = True

        for supported_block_id in supported_block_ids:
            if len(supported[supported_block_id]) < 2:
                can_be_disintergrated = False
                break

        if can_be_disintergrated:
            can_disintegrate += 1

    return can_disintegrate


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
