from enum import Enum, auto
from io import TextIOWrapper


def parse_map(file: TextIOWrapper) -> dict[tuple[int, int], str]:
    map = dict[tuple[int, int], str]()

    for row, line in enumerate(file):
        for col, tile in enumerate(line.strip()):
            map[(row, col)] = tile

    return map


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


Beam = tuple[tuple[int, int], Direction]


def move_beam(beam: Beam, map: dict[tuple[int, int], str]) -> list[Beam]:
    beam_pos, beam_direction = beam
    beam_row, beam_col = beam_pos

    match map[beam_pos], beam_direction:
        case ".", Direction.NORTH:
            return [((beam_row - 1, beam_col), Direction.NORTH)]
        case ".", Direction.SOUTH:
            return [((beam_row + 1, beam_col), Direction.SOUTH)]
        case ".", Direction.EAST:
            return [((beam_row, beam_col + 1), Direction.EAST)]
        case ".", Direction.WEST:
            return [((beam_row, beam_col - 1), Direction.WEST)]
        case "/", Direction.NORTH:
            return [((beam_row, beam_col + 1), Direction.EAST)]
        case "/", Direction.SOUTH:
            return [((beam_row, beam_col - 1), Direction.WEST)]
        case "/", Direction.EAST:
            return [((beam_row - 1, beam_col), Direction.NORTH)]
        case "/", Direction.WEST:
            return [((beam_row + 1, beam_col), Direction.SOUTH)]
        case "\\", Direction.NORTH:
            return [((beam_row, beam_col - 1), Direction.WEST)]
        case "\\", Direction.SOUTH:
            return [((beam_row, beam_col + 1), Direction.EAST)]
        case "\\", Direction.EAST:
            return [((beam_row + 1, beam_col), Direction.SOUTH)]
        case "\\", Direction.WEST:
            return [((beam_row - 1, beam_col), Direction.NORTH)]
        case "|", Direction.NORTH:
            return [((beam_row - 1, beam_col), Direction.NORTH)]
        case "|", Direction.SOUTH:
            return [((beam_row + 1, beam_col), Direction.SOUTH)]
        case "|", Direction.EAST:
            return [
                ((beam_row - 1, beam_col), Direction.NORTH),
                ((beam_row + 1, beam_col), Direction.SOUTH),
            ]
        case "|", Direction.WEST:
            return [
                ((beam_row - 1, beam_col), Direction.NORTH),
                ((beam_row + 1, beam_col), Direction.SOUTH),
            ]
        case "-", Direction.NORTH:
            return [
                ((beam_row, beam_col + 1), Direction.EAST),
                ((beam_row, beam_col - 1), Direction.WEST),
            ]
        case "-", Direction.SOUTH:
            return [
                ((beam_row, beam_col + 1), Direction.EAST),
                ((beam_row, beam_col - 1), Direction.WEST),
            ]
        case "-", Direction.EAST:
            return [((beam_row, beam_col + 1), Direction.EAST)]
        case "-", Direction.WEST:
            return [((beam_row, beam_col - 1), Direction.WEST)]
        case tile, dir:
            raise RuntimeError((tile, dir))


def part1(file: TextIOWrapper) -> int:
    map = parse_map(file)

    beams = {((0, 0), Direction.EAST)}
    seen = {(0, 0)}
    energized_tiles = set[tuple[int, int]]()

    while beams:
        beam = beams.pop()
        beam_pos, _ = beam

        energized_tiles.add(beam_pos)

        if beam not in seen:
            seen.add(beam)
            
            for new_beam in move_beam(beam, map):
                new_beam_pos, _ = new_beam
                if new_beam_pos in map:
                    beams.add(new_beam)
                    

    return len(energized_tiles)


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

