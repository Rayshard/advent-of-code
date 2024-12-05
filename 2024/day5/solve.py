from collections import defaultdict
from io import TextIOWrapper
import sys
from typing import Mapping


def cmp(a: int, b: int, graph: Mapping[int, set[int]]) -> int:
    if a == b:
        return 0  # a == b

    if a not in graph:
        return 1  # b > a

    a_greaters = graph[a]
    if b in a_greaters:
        return -1

    if any(cmp(greater, b, graph) == -1 for greater in a_greaters):
        return -1  # a < b
    else:
        return 1  # b > a


def part1(input: TextIOWrapper) -> int:
    result = 0

    # Build graph
    graph = defaultdict[int, set[int]](set[int])

    for line in input:
        if line == "\n":
            break

        left, right = tuple(int(i) for i in line.split("|"))
        graph[left].add(right)

    # Get correctly ordered updates
    for line in input:
        page_numbers = [int(i) for i in line.split(",")]

        # Build graph that only includes starting nodes from the page
        page_numbers_set = set(page_numbers)
        relevant_graph = {
            num: greaters for num, greaters in graph.items() if num in page_numbers_set
        }

        # Compare pairwise
        pair_wise = zip(page_numbers[:-1], page_numbers[1:])

        if all(cmp(a, b, relevant_graph) == -1 for a, b in pair_wise):
            result += page_numbers[len(page_numbers) // 2]

    return result


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
