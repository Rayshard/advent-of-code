from io import TextIOWrapper
from typing import Callable


def mapping(triples: list[tuple[int, int, int]]) -> Callable[[int], int]:
    def func(num: int) -> int:
        for src_start, dest_start, rng_len in triples:
            if src_start <= num < src_start + rng_len:
                return num - src_start + dest_start

        return num

    return func


def range_mapping(triples: list[tuple[int, int, int]]) -> Callable[[tuple[int, int]], list[tuple[int, int]]]:
    def func(seed_rngs: list[tuple[int, int]]) -> list[tuple[int, int]]:
        input_ranges = seed_rngs
        output_ranges = []

        for src_start, dest_start, rng_len in triples:
            src_stop = src_start + rng_len - 1
            dest_stop = dest_start + rng_len - 1
            new_ranges = []

            for input_range_start, input_range_stop in input_ranges:
                if src_start <= input_range_start <= src_stop:
                    output_range_start = input_range_start - src_start + dest_start

                    if src_start <= input_range_stop <= src_stop:
                        output_range_stop = input_range_stop - src_start + dest_start
                        output_ranges.append((output_range_start, output_range_stop))
                    else:
                        output_ranges.append((output_range_start, dest_stop))
                        new_ranges.append((src_stop + 1, input_range_stop))
                elif src_start <= input_range_stop <= src_stop:
                    new_ranges.append((input_range_start, src_start - 1))

                    output_range_stop = input_range_stop - src_start + dest_start
                    output_ranges.append((dest_start, output_range_stop))
                elif input_range_start > src_stop or input_range_stop < src_start:
                    new_ranges.append((input_range_start, input_range_stop))
                else:
                    new_ranges.append((input_range_start, src_start - 1))
                    new_ranges.append((src_stop + 1, input_range_stop))
                    output_ranges.append((dest_start, dest_stop))

            input_ranges = new_ranges

        return input_ranges + output_ranges

    return func


def part1and2(file: TextIOWrapper) -> int:
    seeds = [int(n) for n in file.readline()[7:].split(" ")]
    point_mappings : dict[str, Callable[[int], int]] = {}
    range_mappings : dict[str, Callable[[tuple[int, int]], list[tuple[int, int]]]] = {}

    file.readline()  # skip first whitespace line

    for line in file:
        label = line.split(" ", 1)[0]
        triples = []

        while (line := file.readline()) and line != "\n":
            dest_start, src_start, rng_len = [int(val) for val in line.split(" ")]
            triples.append((src_start, dest_start, rng_len))

        point_mappings[label] = mapping(triples)
        range_mappings[label] = range_mapping(triples)

    # part 1
    part1_min_location = None

    for seed in seeds:
        seed_to_soil = point_mappings["seed-to-soil"](seed)
        soil_to_fertilizer = point_mappings["soil-to-fertilizer"](seed_to_soil)
        fertilizer_to_water = point_mappings["fertilizer-to-water"](soil_to_fertilizer)
        water_to_light = point_mappings["water-to-light"](fertilizer_to_water)
        light_to_temperature = point_mappings["light-to-temperature"](water_to_light)
        temperature_to_humidity = point_mappings["temperature-to-humidity"](light_to_temperature)
        humidity_to_location = point_mappings["humidity-to-location"](temperature_to_humidity)

        if part1_min_location is None or humidity_to_location < part1_min_location:
            part1_min_location = humidity_to_location

    # part 2
    part2_min_location = None

    for i in range(0, len(seeds), 2):
        seed_rng = (seeds[i], seeds[i] + seeds[i + 1] - 1)
        seed_to_soil = range_mappings["seed-to-soil"]([seed_rng])
        soil_to_fertilizer = range_mappings["soil-to-fertilizer"](seed_to_soil)
        fertilizer_to_water = range_mappings["fertilizer-to-water"](soil_to_fertilizer)
        water_to_light = range_mappings["water-to-light"](fertilizer_to_water)
        light_to_temperature = range_mappings["light-to-temperature"](water_to_light)
        temperature_to_humidity = range_mappings["temperature-to-humidity"](light_to_temperature)
        humidity_to_location = range_mappings["humidity-to-location"](temperature_to_humidity)

        minimum_humidity_to_location = min(start for start, _ in humidity_to_location)
        if part2_min_location is None or minimum_humidity_to_location < part2_min_location:
            part2_min_location = minimum_humidity_to_location

    # result
    return part1_min_location, part2_min_location


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1and2(file))
