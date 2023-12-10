from io import TextIOWrapper
import signal
import sys
from typing import Literal


def part1(directions: list[Literal[0, 1]], network: dict[str, tuple[str, str]]) -> int:
    pos = "AAA"
    steps = 0
    
    while True:
        for direction in directions:
            pos = network[pos][direction]
            steps += 1

            if pos == "ZZZ":
                return steps

def part2(directions: list[Literal[0, 1]], network: dict[str, tuple[str, str]]) -> int:
    starts = [node for node in network.keys() if node.endswith("A")]
    node_to_terminal = dict[tuple[str, int], tuple[str, int]]() # (node, dir_index) -> (terminal, steps_to_next_terminal)
    
    def to_terminal(start: str, dir_index: int) -> tuple[str, int]:
        pos = network[start][directions[dir_index]]
        dir_index += 1
        steps = 1
        
        while pos[2] != "Z":
            while dir_index != len(directions):
                direction = directions[dir_index]
                pos = network[pos][direction]
                steps += 1
                dir_index += 1

                if pos[2] == "Z":
                    break

            dir_index = 0

        return pos, steps

    current = {node: 0 for node in starts}

    def signal_handler(sig, frame):
        print(current)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        if all(node[2] == "Z" for node in current) and len(set(current.values())) == 1:
            break

        min_node = min(current, key=current.get)
        min_steps = current.pop(min_node)
        min_dir_index = min_steps % len(directions)

        if (min_node, min_dir_index) not in node_to_terminal:
            node_to_terminal[(min_node, min_dir_index)] = to_terminal(min_node, min_dir_index)

        terminal, num_steps = node_to_terminal[(min_node, min_dir_index)]
        current[terminal] = min_steps + num_steps

    return current.popitem()[1]


if __name__ == "__main__":
    with open("input.txt") as file:
        directions = [0 if c == "L" else 1 for c in file.readline().strip()]
        file.readline()
        network = {line[:3]: (line[7:10], line[12:15]) for line in file}
    
    #print(part1(directions, network))
    print(part2(directions, network))
