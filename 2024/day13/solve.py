from io import TextIOWrapper
import sys
import string
from typing import Optional

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


def solve(button_a: Vec2, button_b: Vec2, prize: Vec2, error) -> Optional[int]:
    Ax, Ay = button_a
    Bx, By = button_b
    Px, Py = prize

    b: float = (Px - Py * (Ax / Ay)) / (Bx - By * (Ax / Ay))
    a: float = (Px / Ax) - ((Bx * b) / Ax)

    a_rounded, b_rounded = round(a), round(b)

    if abs(a - a_rounded) <= error and abs(b - b_rounded) <= error:
        a, b = a_rounded, b_rounded

        if a >= 0 and b >= 0:
            return a * 3 + b

    return None


def part1(input: TextIOWrapper) -> int:
    return sum(
        tokens
        for button_a, button_b, prize in parse_claw_machines(input)
        if (tokens := solve(button_a, button_b, prize, error=1e-9)) is not None
    )


def part2(input: TextIOWrapper) -> int:
    add = 10000000000000

    return sum(
        tokens
        for button_a, button_b, (Px, Py) in parse_claw_machines(input)
        if (tokens := solve(button_a, button_b, (Px + add, Py + add), error=1e-3))
        is not None
    )


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
