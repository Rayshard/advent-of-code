from typing import Literal


def part1(lines: list[str], bag: dict[Literal["red", "green", "blue"], int]) -> int:
    result = 0

    for line in lines:
        game, draws = line.strip().split(": ", 1)
        game = int(game[5:])

        playable = True

        for draw in draws.split("; "):
            for set in draw.split(", "):
                count, color = set.split(" " , 1)
                count = int(count)

                if count > bag[color]:
                    playable = False
                    break

            if not playable:
                break

        if playable:
            result += game

    return result


def part2(lines: list[str]) -> int:
    result = 0

    for line in lines:
        game, draws = line.strip().split(": ", 1)
        game = int(game[5:])

        min_bag = { "red": 0, "green": 0, "blue": 0}

        for draw in draws.split("; "):
            for set in draw.split(", "):
                count, color = set.split(" " , 1)
                count = int(count)

                if count > min_bag[color]:
                    min_bag[color] = count

        result += min_bag["red"] * min_bag["green"] * min_bag["blue"]

    return result

if __name__ == "__main__":
    with open("input.txt") as file:
        lines =  file.readlines()
        print(part1(lines, {"red": 12, "green": 13, "blue": 14}))
        print(part2(lines))
