from io import TextIOWrapper
import networkx
import math


def parse_graph(file: TextIOWrapper) -> networkx.Graph:
    graph = networkx.Graph()

    for line in file:
        node, *adj = line.strip().split()
        node = node[:-1]

        for a in adj:
            graph.add_edge(node, a)
            graph.add_edge(a, node)

    return graph


def part1(graph: networkx.Graph) -> int:
    graph = graph.copy()
    graph.remove_edges_from(networkx.minimum_edge_cut(graph))

    return math.prod(len(subgraph) for subgraph in networkx.connected_components(graph))


if __name__ == "__main__":
    with open("input.txt") as file:
        graph = parse_graph(file)

    print(part1(graph))
