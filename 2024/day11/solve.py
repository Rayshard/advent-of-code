from io import TextIOWrapper
import sys


def run_25(stones: list[int]) -> list[int]:
    new_stones = list[int]()

    for _ in range(25):
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(digits := str(stone)) % 2 == 0:
                half = len(digits) // 2
                left = int(digits[:half])
                right = int(digits[half:])

                new_stones += [left, right]
            else:
                new_stones.append(stone * 2024)

        stones = new_stones
        new_stones = list[int]()

    return stones

def part1(input: TextIOWrapper) -> int:
    stones = [int(stone) for stone in input.readline().strip().split()]
    after_25 = run_25(stones)

    # for stone in stones:

    return len(stones)


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
