from collections import defaultdict
from io import TextIOWrapper
import sys
from typing import Mapping


def parse_stones(input: TextIOWrapper) -> list[int]:
    return [int(stone) for stone in input.readline().strip().split()]


def handle_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(digits := str(stone)) % 2 == 0:
        half = len(digits) // 2
        left = int(digits[:half])
        right = int(digits[half:])

        return [left, right]
    else:
        return [stone * 2024]


def run(stones: list[int], num_iterations: int) -> Mapping[int, int]:
    cache = dict[int, list[int]]()
    prev_iteration = defaultdict[int, int](int)

    for stone in stones:
        prev_iteration[stone] += 1

    for _ in range(num_iterations):
        cur_iteration = defaultdict[int, int](int)

        for stone, count in prev_iteration.items():
            if stone not in cache:
                cache[stone] = handle_stone(stone)

            for stone_child in cache[stone]:
                cur_iteration[stone_child] += count

        prev_iteration = cur_iteration

    return prev_iteration


def part1(input: TextIOWrapper) -> int:
    stones = parse_stones(input)
    return sum(run(stones, 25).values())


def part2(input: TextIOWrapper) -> int:
    stones = parse_stones(input)
    return sum(run(stones, 75).values())


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
