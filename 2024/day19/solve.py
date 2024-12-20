from io import TextIOWrapper
import sys


def parse_input(input: TextIOWrapper) -> tuple[set[str], list[str]]:
    patterns = set(input.readline().split(", "))
    input.readline()
    designs = [line.strip() for line in input.readlines()]

    return patterns, designs


def can_make_design(patterns: set[str], design: str) -> bool:
    for size in reversed(range(len(design))):
        if design[:size + 1] not in patterns:
            continue

        remaining = design[size + 1:]

        if not remaining or can_make_design(patterns, remaining):
            return True

    return False



def part1(input: TextIOWrapper) -> int:
    patterns, designs = parse_input(input)
    return sum(can_make_design(patterns, design) for design in designs)


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
