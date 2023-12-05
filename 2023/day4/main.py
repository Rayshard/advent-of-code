from collections import defaultdict
from io import TextIOWrapper


def part1(file: TextIOWrapper) -> int:
    result = 0

    for line in file:
        count = len(set.intersection(*[set(int(number.strip()) for number in cards.split(" ") if number != "") for cards in line.split(": ", 1)[1].split(" | ")]))

        if count != 0:
            result += 2**(count - 1)

    return result


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
