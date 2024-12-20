from io import TextIOWrapper
import sys


def parse_input(input: TextIOWrapper) -> tuple[set[str], list[str]]:
    patterns = set(input.readline().strip().split(", "))
    input.readline()
    designs = [line.strip() for line in input.readlines()]

    return patterns, designs


def num_ways_to_make_design(
    patterns: set[str], design: str, cache: dict[str, int]
) -> int:
    if design in cache:
        return cache[design]

    count = 0

    for size in reversed(range(len(design))):
        if design[: size + 1] not in patterns:
            continue

        remaining = design[size + 1 :]

        if not remaining:
            count += 1
        else:
            count += num_ways_to_make_design(patterns, remaining, cache)

    cache[design] = count
    return count


def can_make_design(patterns: set[str], design: str, cache: dict[str, int]) -> bool:
    # This is less efficient than stopping once a design is determined
    # can be made but hey
    return num_ways_to_make_design(patterns, design, cache) != 0


def part1(input: TextIOWrapper) -> int:
    patterns, designs = parse_input(input)
    cache = dict[str, int]()

    return sum(can_make_design(patterns, design, cache) for design in designs)


def part2(input: TextIOWrapper) -> int:
    patterns, designs = parse_input(input)
    cache = dict[str, int]()

    return sum(num_ways_to_make_design(patterns, design, cache) for design in designs)


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
