from collections import defaultdict
from io import TextIOWrapper


def part1and2(file: TextIOWrapper) -> int:
    result_1 = 0
    result_2 = 0

    for line in file:
        current_row = [int(number) for number in line.split()]
        prev_value = current_row[0]
        next_value = current_row[-1]
        part2_sign = -1

        while True:
            next_row = []
            all_zeros = True

            for i in range(len(current_row) - 1):
                sum = current_row[i + 1] - current_row[i]
                all_zeros = all_zeros and sum == 0
                next_row.append(sum)

            current_row = next_row
            prev_value += current_row[0] * part2_sign
            next_value += current_row[-1]
            part2_sign = -part2_sign

            if all_zeros:
                break

        result_2 += prev_value
        result_1 += next_value

    return result_1, result_2


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1and2(file))
