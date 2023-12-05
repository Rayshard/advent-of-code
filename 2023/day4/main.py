from collections import defaultdict
from io import TextIOWrapper


def part1and2(file: TextIOWrapper) -> int:
    part1_result = 0
    total = defaultdict(int)

    for i, line in enumerate(file):
        total[i] += 1

        count = len(set.intersection(*[set(int(number.strip()) for number in cards.split(" ") if number != "") for cards in line.split(": ", 1)[1].split(" | ")]))

        if count != 0:
            part1_result += 2**(count - 1)

            for index in range(1, count + 1):
                total[i + index] += total[i]

    return part1_result, sum(total.values())


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1and2(file))
