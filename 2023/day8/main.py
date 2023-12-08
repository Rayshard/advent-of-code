from io import TextIOWrapper

def part1(file: TextIOWrapper) -> int:
    directions = [0 if c == "L" else 1 for c in file.readline().strip()]

    file.readline()

    network = {line[:3]: (line[7:10], line[12:15]) for line in file}

    pos = "AAA"
    steps = 0
    
    while True:
        for direction in directions:
            pos = network[pos][direction]
            steps += 1

            if pos == "ZZZ":
                return steps

if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
