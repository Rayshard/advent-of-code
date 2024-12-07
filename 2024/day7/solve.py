from io import TextIOWrapper
import sys


def part1(input: TextIOWrapper) -> int:
    result = 0

    for line in input:
        left, right = line.split(": ")
        expected = int(left)
        nums = [int(num) for num in right.split()]

        level = [nums[0]]

        for num in nums[1:]:
            new_level = []

            for prev in level:
                if (sum := prev + num) <= expected:
                    new_level.append(sum)

                if (product := prev * num) <= expected:
                    new_level.append(product)

            level = new_level

        if expected in level:
            result += expected

    return result


def part2(input: TextIOWrapper) -> int:
    result = 0

    for line in input:
        left, right = line.split(": ")
        expected = int(left)
        nums = [int(num) for num in right.split()]

        level = [nums[0]]

        for num in nums[1:]:
            new_level = []

            for prev in level:
                if (sum := prev + num) <= expected:
                    new_level.append(sum)

                if (product := prev * num) <= expected:
                    new_level.append(product)

                if (concat := int(str(prev) + str(num))) <= expected:
                    new_level.append(concat)

            level = new_level

        if expected in level:
            result += expected

    return result


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
