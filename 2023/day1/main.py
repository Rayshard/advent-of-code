def part1(lines : list[str]) -> int:
    sum = 0

    for line in lines:
        first_digit, last_digit = None, None

        for char in line:
            if char.isdigit():
                last_digit = char

                if first_digit is None:
                    first_digit = last_digit

        assert first_digit is not None
        assert last_digit is not None
        sum += int(first_digit + last_digit)

    return  sum

def part2(lines : list[str]) -> int:
    sum = 0

    words_to_digits = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    for line in lines:
        first_digit, last_digit = None, None

        while len(line) != 0:
            digit = None

            if line[0].isdigit():
                digit = line[0]
            else:
                for word, value in words_to_digits.items():
                    if line.startswith(word):
                        digit = value
                        break

            line = line[1:]

            if digit is None:
                continue

            last_digit = digit

            if first_digit is None:
                first_digit = last_digit

        assert first_digit is not None
        assert last_digit is not None
        sum += int(first_digit + last_digit)

    return sum

if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()

        print(part1(lines))
        print(part2(lines))
