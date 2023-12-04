from io import TextIOWrapper


def part1(file: TextIOWrapper) -> int:
    next_possible_part_number_id = 0
    part_numbers = {}
    last_3_lines = [
        {"numbers": {}, "symbols": set()},
        {"numbers": {}, "symbols": set()}
    ]

    for y, line in enumerate(file):
        numbers = dict()
        symbols =set()
        digits = []

        for x, char in enumerate(line):
            if char.isdigit():
                digits.append((char, (x, y)))
            else:
                if char != "." and char != "\n":
                    symbols.add((x, y))

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
            for symbol_x, symbol_y in l["symbols"]:
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

        last_3_lines.pop(0)

    return sum(part_numbers.values())


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
