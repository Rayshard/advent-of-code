from io import TextIOWrapper
import sys


def part1(input: TextIOWrapper) -> int:
    left, right = list[int](), list[int]()

    for line in input:
        l, r = line.split()
        left.append(int(l.strip()))
        right.append(int(r.strip()))

    left = sorted(left)
    right = sorted(right)

    return sum(abs(l - r) for l, r in zip(left, right))


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))
