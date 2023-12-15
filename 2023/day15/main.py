from io import TextIOWrapper


def hash(s: str) -> int:
    current_value = 0

    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value

def part1(file: TextIOWrapper) -> int:
    result = 0

    for step in file.readline().strip().split(","):
        result += hash(step)

    return result



if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
