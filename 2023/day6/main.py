from io import TextIOWrapper
import math

# Solve (time-hold) * hold > distance
#    -> h*h - t*h + d < 0
def ways_to_win(time: int, distance: int) -> int:
    determinant = math.sqrt(time * time - 4*distance)
    min_hold_time = math.floor((time - determinant) / 2 + 1)
    max_hold_time = math.ceil((time + determinant) / 2 - 1)

    return max_hold_time - min_hold_time + 1

def part1(file: TextIOWrapper) -> int:
    times = (int(time) for time in file.readline().split()[1:])
    distances = (int(distance) for distance in file.readline().split()[1:])
    races = zip(times, distances)

    ways_to_win_per_race = (ways_to_win(time, distance) for time, distance in races)
    return math.prod(ways_to_win_per_race)

def part2(file: TextIOWrapper) -> int:
    time = int("".join(file.readline().split()[1:]))
    distance = int("".join(file.readline().split()[1:]))
    return ways_to_win(time, distance)

if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

    with open("input.txt") as file:
        print(part2(file))
