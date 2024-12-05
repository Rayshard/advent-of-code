from collections import defaultdict
import functools
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


def build_graph(input: TextIOWrapper) -> Mapping[int, set[int]]:
    graph = defaultdict[int, set[int]](set[int])

    for line in input:
        if line == "\n":
            break

        left, right = tuple(int(i) for i in line.split("|"))
        graph[left].add(right)

    return graph


def get_page_graph(
    page: list[int], graph: Mapping[int, set[int]]
) -> Mapping[int, set[int]]:
    """Returns a graph that only includes starting nodes from the page"""
    page_set = set(page)
    return {num: greaters for num, greaters in graph.items() if num in page_set}


def get_pages(input: TextIOWrapper) -> tuple[list[int], list[int]]:
    graph = build_graph(input)
    ordered = list[int]()
    reordered = list[int]()

    for line in input:
        page = [int(i) for i in line.split(",")]
        page_graph = get_page_graph(page, graph)

        # Compare pairwise
        pair_wise = zip(page[:-1], page[1:])

        if all(cmp(a, b, page_graph) == -1 for a, b in pair_wise):
            ordered.append(page)
        else:
            page = sorted(
                page, key=functools.cmp_to_key(lambda a, b: cmp(a, b, page_graph))
            )
            reordered.append(page)

    return ordered, reordered


def order_page(page: list[int], graph: Mapping[int, set[int]]) -> list[int]:
    page_graph = get_page_graph(page, graph)
    return sorted(page, key=functools.cmp_to_key(lambda a, b: cmp(a, b, page_graph)))


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        ordered_pages, reordered_pages = get_pages(file)

        print(sum(page[len(page) // 2] for page in ordered_pages))
        print(sum(page[len(page) // 2] for page in reordered_pages))
