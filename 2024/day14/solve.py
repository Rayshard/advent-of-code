from dataclasses import dataclass
from io import TextIOWrapper
import math
import sys
from typing import Optional

Vec2 = tuple[int, int]
ClawMachine = tuple[Vec2, Vec2, Vec2]


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def quadrant(self, map_width: int, map_height: int) -> Optional[int]:
        half_width = map_width // 2
        half_height = map_height // 2

        if self.x == half_width or self.y == half_height:
            return None
        elif 0 <= self.x < half_width:
            if 0 <= self.y < half_height:
                return 0
            else:
                return 2
        elif 0 <= self.y < half_height:
            return 1
        else:
            return 3


def parse_robots(input: TextIOWrapper) -> list[Robot]:
    def parse_robot(line: str) -> Robot:
        line = line.strip()
        pos, vel = line.split(" ")

        x, y = pos.removeprefix("p=").split(",")
        vx, vy = vel.removeprefix("v=").split(",")

        return Robot(int(x), int(y), int(vx), int(vy))

    return [parse_robot(line) for line in input]


def simulate(robot: Robot, steps: int, map_width: int, map_height: int) -> Robot:
    robot.x = (robot.x + robot.vx * steps) % map_width
    robot.y = (robot.y + robot.vy * steps) % map_height
    return robot


def part1(input: TextIOWrapper) -> int:
    map_width, map_height = 101, 103
    steps = 100
    robots = (
        simulate(robot, steps, map_width, map_height) for robot in parse_robots(input)
    )
    quadrants = {i: 0 for i in range(4)}

    for robot in robots:
        if (quadrant := robot.quadrant(map_width, map_height)) is None:
            continue

        quadrants[quadrant] += 1

    return math.prod(quadrants.values())


def part2(input: TextIOWrapper) -> int:
    map_width, map_height = 101, 103
    robots = parse_robots(input)
    min_score, min_second = sys.maxsize, -1

    for second in range(map_width * map_height):
        quadrants = {i: 0 for i in range(4)}

        for robot in robots:
            simulate(robot, 1, map_width, map_height)

            if (quadrant := robot.quadrant(map_width, map_height)) is None:
                continue

            quadrants[quadrant] += 1

        score = math.prod(quadrants.values())

        if score < min_score:
            min_score = score
            min_second = second + 1

    return min_second


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
