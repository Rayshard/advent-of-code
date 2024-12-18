from collections import defaultdict
from dataclasses import dataclass, field
from io import TextIOWrapper
import sys
import string
import math

Vec2 = tuple[int, int]
ClawMachine = tuple[Vec2, Vec2, Vec2]


def parse_claw_machines(input: TextIOWrapper) -> list[ClawMachine]:
    def get_numbers(line: str) -> Vec2:
        a, b = "".join(
            char for char in line if (char in string.digits or char == ",")
        ).split(",")
        return int(a), int(b)

    claw_machines = list[ClawMachine]()

    while True:
        eq1 = get_numbers(input.readline())
        eq2 = get_numbers(input.readline())
        prize = get_numbers(input.readline())

        claw_machines.append((eq1, eq2, prize))

        if not input.readline():
            break

    return claw_machines


def part1(input: TextIOWrapper) -> int:
    claw_machines = parse_claw_machines(input)
    result = 0

    for button_a, button_b, prize in claw_machines:
        Ax, Ay = button_a
        Bx, By = button_b
        Px, Py = prize

        b: float = (Px - (Py * Ax) / Ay) / (Bx - (By * Ax) / Ay)
        a: float = (Px - (Bx * b)) / Ax

        a_rounded, b_rounded = round(a), round(b)

        if math.isclose(a, a_rounded) and math.isclose(b, b_rounded):
            a, b = a_rounded, b_rounded

            if (0 <= a <= 100) and (0 <= b <= 100):
                result += a * 3 + b

    return result


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
