from io import TextIOWrapper
from typing import Callable


def mapping(triples: list[tuple[int, int, int]]) -> Callable[[int], int]:
    def func(num: int) -> int:
        for src_start, dest_start, rng_len in triples:
            if src_start <= num < src_start + rng_len:
                return num - src_start + dest_start

        return num

    return func


def part1(file: TextIOWrapper) -> int:
    seeds = [int(n) for n in file.readline()[7:].split(" ")]
    mappings : dict[str, Callable[[int], int]] = {}

    file.readline()  # skip first whitespace line

    for line in file:
        label = line.split(" ", 1)[0]
        triples = []

        while (line := file.readline()) and line != "\n":
            dest_start, src_start, rng_len = [int(val) for val in line.split(" ")]
            triples.append((src_start, dest_start, rng_len))

        mappings[label] = mapping(triples)

    seeds_to_locations = {}

    for seed in seeds:
        seed_to_soil = mappings["seed-to-soil"](seed)
        soil_to_fertilizer = mappings["soil-to-fertilizer"](seed_to_soil)
        fertilizer_to_water = mappings["fertilizer-to-water"](soil_to_fertilizer)
        water_to_light = mappings["water-to-light"](fertilizer_to_water)
        light_to_temperature = mappings["light-to-temperature"](water_to_light)
        temperature_to_humidity = mappings["temperature-to-humidity"](light_to_temperature)
        humidity_to_location = mappings["humidity-to-location"](temperature_to_humidity)

        seeds_to_locations[seed] = humidity_to_location

    return min(seeds_to_locations.values())


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
