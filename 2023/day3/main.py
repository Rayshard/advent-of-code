from collections import defaultdict
from io import TextIOWrapper


def part1and2(file: TextIOWrapper) -> int:
    next_possible_part_number_id = 0
    part_numbers = {}
    possible_gear_ratios = defaultdict(list)
    last_3_lines = [
        {"numbers": {}, "symbols": dict()},
        {"numbers": {}, "symbols": dict()}
    ]

    for y, line in enumerate(file):
        numbers = dict()
        symbols = dict()
        digits = []

        for x, char in enumerate(line):
            if char.isdigit():
                digits.append((char, (x, y)))
            else:
                if char != "." and char != "\n":
                    symbols[x, y] = char

                if len(digits) != 0:
                    number = int("".join([digit for digit, _ in digits]))

                    for _, pos in digits:
                        numbers[pos] = (number, next_possible_part_number_id)

                    digits = []
                    next_possible_part_number_id += 1

        last_3_lines.append({"numbers": numbers, "symbols": symbols})

        all_numbers = {}
        all_numbers.update(last_3_lines[0]["numbers"])
        all_numbers.update(last_3_lines[1]["numbers"])
        all_numbers.update(last_3_lines[2]["numbers"])

        for l in last_3_lines:
            for (symbol_x, symbol_y), symbol in l["symbols"].items():
                adjacent = [
                    (symbol_x - 1, symbol_y - 1),
                    (symbol_x, symbol_y - 1),
                    (symbol_x + 1, symbol_y - 1),
                    (symbol_x - 1, symbol_y),
                    (symbol_x, symbol_y),
                    (symbol_x + 1, symbol_y),
                    (symbol_x - 1, symbol_y + 1),
                    (symbol_x, symbol_y + 1),
                    (symbol_x + 1, symbol_y + 1),
                ]

                for pos in adjacent:
                    if pos in all_numbers:
                        number, id = all_numbers[pos]
                        if id not in part_numbers:
                            part_numbers[id] = number
                            possible_gear_ratios[(symbol_x, symbol_y)].append(number)

        last_3_lines.pop(0)

    gear_ratios = [numbers[0] * numbers[1] for numbers in possible_gear_ratios.values() if len(numbers) == 2]

    return sum(part_numbers.values()), sum(gear_ratios)


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1and2(file))
