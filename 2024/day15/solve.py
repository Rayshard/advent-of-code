from dataclasses import dataclass
from io import TextIOWrapper
import math
import sys
from typing import Optional

Vec2 = tuple[int, int]

MOVEMENTS_TO_VEC2 = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse_map(input: TextIOWrapper) -> tuple[dict[Vec2, str], str, Vec2]:
    map = dict[Vec2, str]()
    robot: Vec2 = (0, 0)

    for row, line in enumerate(input):
        line = line.strip()

        if not line:
            break

        for col, char in enumerate(line):
            if char == ".":
                continue
            elif char == "@":
                robot = (row, col)
                continue

            map[(row, col)] = char

    movements = "".join(line.strip() for line in input)
    return map, movements, robot


def resize_map(original: dict[Vec2, str]) -> dict[Vec2, str]:
    return original


def move_robot_part_1(robot: Vec2, map: dict[Vec2, str], direction: Vec2) -> Vec2:
    robot_row, robot_col = robot
    dir_y, dir_x = direction
    target = (robot_row + dir_y, robot_col + dir_x)

    match map.get(target):
        case None:
            return target
        case "#":
            return robot
        case "O":
            current = target

            while True:
                current = (current[0] + dir_y, current[1] + dir_x)

                match map.get(current):
                    case None:
                        map[current] = "O"
                        del map[target]
                        return target
                    case "#":
                        return robot
                    case "O":
                        continue
                    case char:
                        raise NotImplementedError(char)
        case char:
            raise NotImplementedError(char)
        

def move_robot_part_2(robot: Vec2, map: dict[Vec2, str], direction: Vec2) -> Vec2:
    robot_row, robot_col = robot
    dir_y, dir_x = direction
    target = (robot_row + dir_y, robot_col + dir_x)

    match map.get(target):
        case None:
            return target
        case "#":
            return robot
        case "[" | "]":
            current = target

            while True:
                current = (current[0] + dir_y, current[1] + dir_x)

                match map.get(current):
                    case None:
                        map[current] = "O"
                        del map[target]
                        return target
                    case "#":
                        return robot
                    case "O":
                        continue
                    case char:
                        raise NotImplementedError(char)
        case char:
            raise NotImplementedError(char)


def part1(input: TextIOWrapper) -> int:
    map, movements, robot = parse_map(input)

    for movement in movements:
        robot = move_robot_part_1(robot, map, MOVEMENTS_TO_VEC2[movement])

    return sum((100 * row + col) for (row, col), char in map.items() if char == "O")


def part2(input: TextIOWrapper) -> int:
    map, movements, robot = parse_map(input)
    map = resize_map(map)

    for movement in movements:
        robot = move_robot_part_2(robot, map, MOVEMENTS_TO_VEC2[movement])

    return sum((100 * row + col) for (row, col), char in map.items() if char == "[")


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
