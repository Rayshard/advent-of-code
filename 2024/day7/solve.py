from io import TextIOWrapper
import sys
from typing import Callable


def parse_line(line: str) -> tuple[int, list[int]]:
    left, right = line.split(": ")
    return int(left), [int(num) for num in right.split()]


def solve_all(
    equation: list[int],
    upper_limit: int,
    operators: list[Callable[[int, int], int]],
) -> list[int]:
    solutions = [equation[0]]

    for num in equation[1:]:
        new_solutions = []

        for prev in solutions:
            new_solutions += [
                result
                for operator in operators
                if (result := operator(prev, num)) <= upper_limit
            ]

        solutions = new_solutions

    return solutions


def part1(input: TextIOWrapper) -> int:
    result = 0

    for line in input:
        expected, equation = parse_line(line)

        solutions = solve_all(
            equation,
            expected,
            operators=[
                lambda a, b: a + b,
                lambda a, b: a * b,
            ],
        )

        if expected in solutions:
            result += expected

    return result


def part2(input: TextIOWrapper) -> int:
    result = 0

    for line in input:
        expected, equation = parse_line(line)

        solutions = solve_all(
            equation,
            expected,
            operators=[
                lambda a, b: a + b,
                lambda a, b: a * b,
                lambda a, b: int(str(a) + str(b)),
            ],
        )

        if expected in solutions:
            result += expected

    return result


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
