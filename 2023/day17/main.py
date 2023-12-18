from dataclasses import dataclass
from enum import Enum, auto
from io import TextIOWrapper
from typing import Literal, Optional


Map = dict[tuple[int, int], int]


def parse_map(file: TextIOWrapper) -> Map:
    map = Map()

    for row, line in enumerate(file):
        for col, block in enumerate(line.strip()):
            map[(row, col)] = int(block)

    return map


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class Crucible:
    position: tuple[int, int]
    direction: Direction
    remaining_movements_in_direction: int
    heat_loss_total: int

    def move_in_dir(self, map: Map) -> Optional["Crucible"]:
        if self.remaining_movements_in_direction <= 0:
            return None

        match self.direction:
            case Direction.UP:
                new_pos = (self.position[0] - 1, self.position[1])
            case Direction.DOWN:
                new_pos = (self.position[0] + 1, self.position[1])
            case Direction.LEFT:
                new_pos = (self.position[0], self.position[1] - 1)
            case Direction.RIGHT:
                new_pos = (self.position[0], self.position[1] + 1)
            case dir:
                raise RuntimeError(dir)
            
        if new_pos not in map:
            return None

        return Crucible(
            position=new_pos,
            direction=self.direction,
            remaining_movements_in_direction=self.remaining_movements_in_direction - 1,
            heat_loss_total=self.heat_loss_total + map[new_pos]
        )
    
    def get_next_possiblities(self) -> list["Crucible"]:
        match self.direction:
            case Direction.UP | Direction.DOWN:
                return [
                    Crucible(self.position, Direction.LEFT, 3, self.heat_loss_total),
                    Crucible(self.position, Direction.RIGHT, 3, self.heat_loss_total)
                ]
            case Direction.LEFT | Direction.RIGHT:
                return [
                    Crucible(self.position, Direction.UP, 3, self.heat_loss_total),
                    Crucible(self.position, Direction.DOWN, 3, self.heat_loss_total)
                ]
            case dir:
                raise RuntimeError(dir)


def part1(map: Map) -> int:
    end = max(map)

    crucibles = {
        Crucible((0, 0), Direction.RIGHT, 2, 0),
        Crucible((0, 0), Direction.DOWN, 2, 0),
    }

    seen : dict[tuple[tuple[int, int], Direction, int], int] = {}
    minimum_heat_loss = None

    while crucibles:
        new_crucibles = set[Crucible]()

        for crucible in crucibles:
            if minimum_heat_loss is not None and crucible.heat_loss_total > minimum_heat_loss:
                continue

            if crucible.position not in map:
                continue

            if (seen_heat_loss := seen.get((crucible.position, crucible.direction, crucible.remaining_movements_in_direction))) is not None:
                if crucible.heat_loss_total >= seen_heat_loss:
                    continue

            seen[(crucible.position, crucible.direction, crucible.remaining_movements_in_direction)] = crucible.heat_loss_total

            if crucible.position == end and (minimum_heat_loss is None or crucible.heat_loss_total < minimum_heat_loss):
                minimum_heat_loss = crucible.heat_loss_total

            if (new_crucible := crucible.move_in_dir(map)) is None:
                continue

            new_crucibles.add(new_crucible)
            new_crucibles.update(new_crucible.get_next_possiblities())

        crucibles = new_crucibles

    return minimum_heat_loss


if __name__ == "__main__":
    with open("input.txt") as file:
        map = parse_map(file)

    print(part1(map))

