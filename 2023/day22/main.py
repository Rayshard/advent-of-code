from collections import defaultdict
from io import TextIOWrapper


Coord = tuple[int, int, int]
Block = list[Coord]


def parse_space(file: TextIOWrapper) -> tuple[set[Coord], list[Block]]:
    space = set[Coord]()
    blocks = list[Block]()

    for line in file:
        (x1, y1, z1), (x2, y2, z2) = [tuple(map(int, item.split(","))) for item in line.strip().split("~")]

        bricks = list[Coord]()

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    bricks.append((x, y, z))

        space.update(bricks)
        blocks.append(bricks)

    return space, blocks


def simulate(space: set[Coord], blocks: list[Block]) -> tuple[set[Coord], list[Block], set[int]]:
    fallen_blocks = set[int]()


    while True:
        old_space = space.copy()

        for i in range(len(blocks)):
            block = blocks[i]
            space.difference_update(block)
            done = False

            while not done:
                new_block = list[Coord]()
                fell = True
                for x, y, z in block:
                    new_coord = (x, y, z - 1)

                    if z == 1 or new_coord in space:
                        done = True
                        new_block = block
                        fell = False
                        break
                    else:
                        new_block.append(new_coord)

                if fell:
                    fallen_blocks.add(i)

                block = new_block

            space.update(block)
            blocks[i] = block

        if old_space == space:
            break

    return space, blocks, fallen_blocks


def find_disintegratable_blocks(blocks: list[Block]) -> set[int]:
    brick_to_blocks = dict[Coord, int]()

    for block, bricks in enumerate(blocks):
        for brick in bricks:
            brick_to_blocks[brick] = block


    block_to_supporting = defaultdict[int, set[int]](set[int])
    block_to_supported_by = defaultdict[int, set[int]](set[int])

    for brick, block in brick_to_blocks.items():
        x, y, z = brick
        above = (x, y, z + 1)

        if above in brick_to_blocks:
            supported = brick_to_blocks[above]

            if supported != block:
                block_to_supporting[block].add(supported)
                block_to_supported_by[supported].add(block)

    disintegratable_blocks = set(range(len(blocks)))

    for supporters in block_to_supported_by.values():
        if len(supporters) == 1:
            disintegratable_blocks.difference_update(supporters)

    return disintegratable_blocks


def solve(file: TextIOWrapper) -> int:
    space, blocks = parse_space(file)
    space, blocks, _ = simulate(space, blocks)
    disintegratable_blocks = find_disintegratable_blocks(blocks)
    non_disintegratable_blocks = set(range(len(blocks))) - disintegratable_blocks

    part_2_result = 0

    for ndb in non_disintegratable_blocks:
        _, _, fallen = simulate(space.difference(blocks[ndb]), blocks[:ndb] + blocks[ndb+1:])
        part_2_result += len(fallen)

    return len(disintegratable_blocks), part_2_result


if __name__ == "__main__":
    with open("input.txt") as file:
        print(solve(file))
