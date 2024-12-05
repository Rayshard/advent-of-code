from collections import defaultdict
from io import TextIOWrapper
import sys
from typing import Callable, Mapping
import functools

def cmp(a: int, b: int, graph: Mapping[int, set[int]]) -> int:
    if a == b:
        return 0  # a == b
    
    if a not in graph:
        return ((cmp(b, a, graph) == 1) and -1) or 1
    
    a_greaters = graph[a]
    if b in a_greaters:
        return -1

    if any(cmp(greater, b, graph) == -1 for greater in a_greaters):
        return -1
    else:
        return ((cmp(b, a, graph) == 1) and -1) or 1


def part1(input: TextIOWrapper) -> int:
    result = 0

    # Build Graph
    graph = defaultdict[int, set[int]](set[int])

    for line in input:
        if line == "\n":
            break

        left, right = tuple(int(i) for i in line.split("|"))
        graph[left].add(right)

    # Get correctly ordered updates
    for line in input:
        page_numbers = [int(i) for i in line.split(",")]
        pair_wise = zip(page_numbers[:-1], page_numbers[1:])
        ordered = all(cmp(a, b, graph) == -1 for a, b in pair_wise)

        if ordered:
            result += page_numbers[len(page_numbers) // 2]

    # print(cmp(75, 97, graph))

    # from pprint import pprint
    # pprint(dict(graph))


    # numbers = set(graph.keys()).union(*(s for s in graph.values()))
    # print(sorted(numbers, key=functools.cmp_to_key(lambda a, b: cmp(a, b, graph))))

    return result


def part2(input: TextIOWrapper) -> int:
    return 0


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
