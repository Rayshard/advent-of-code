from collections import defaultdict
from io import TextIOWrapper
from dataclasses import dataclass, field
from queue import Queue
from typing import Literal

from pprint import pprint

Pulse = Literal[0] | Literal[1]

@dataclass
class Module:
    targets: list[str]

@dataclass
class Broadcaster(Module):
    pass

@dataclass
class FlipFlop(Module):
    state: bool = False

@dataclass
class Conjunction(Module):
    inputs: defaultdict[str, Pulse] = field(default_factory=lambda: defaultdict(int))


def parse_configuration(file: TextIOWrapper) -> dict[str, Module]:
    config = dict[str, Module]()

    for line in file:
        module_name, targets = line.strip().split(" -> ")
        targets = targets.split(", ")

        match module_name:
            case "broadcaster":
                module = Broadcaster(targets)
            case other if other.startswith("%"):
                module_name = module_name[1:]
                module = FlipFlop(targets)
            case other if other.startswith("&"):
                module_name = module_name[1:]
                module = Conjunction(targets)
            case other:
                raise RuntimeError(other)

        config[module_name] = module

    for name, module in config.items():
        for target in module.targets:
            target_module = config.get(target)
            if target_module is not None and isinstance(target_module, Conjunction):
                target_module.inputs[name] = 0

    return config

def run_configuration(config: dict[str, Module]) -> tuple[int, int, defaultdict[str, tuple[int, int]]]:
    queue = Queue[tuple[str, Pulse, str]]()
    queue.put(("button", 0, "broadcaster"))

    def step() -> None:
        source, pulse, module = queue.get()

        match config.get(module), pulse:
            case Broadcaster(targets), pulse:
                pass
            case FlipFlop(targets, _), 1:
                targets = []
            case FlipFlop(targets, state=False), 0:
                config[module].state = True
                pulse = 1
            case FlipFlop(targets, state=True), 0:
                config[module].state = False
                pulse = 0
            case Conjunction(targets, _), pulse:
                config[module].inputs[source] = pulse
                pulse = 0 if all(bool(value) for value in config[module].inputs.values()) else 1
            case None, _:
                return
            case m, p:
                raise NotImplementedError(m, p)

        for target in targets:
            queue.put((module, pulse, target))

    pulsed_modules = defaultdict[str, tuple[int, int]](lambda: (0, 0))
    low_pulses, high_pulses = 0, 0
    while not queue.empty():
        peek_source, peek_pulse, peek_module = queue.queue[0]
        pulsed_module_ls, pulsed_module_hs = pulsed_modules[peek_module]

        if peek_pulse == 0:
            low_pulses += 1
            pulsed_modules[peek_module] = (pulsed_module_ls + 1, pulsed_module_hs)
        elif peek_pulse == 1:
            high_pulses += 1

            pulsed_modules[peek_module] = (pulsed_module_ls, pulsed_module_hs + 1)
        else:
            raise RuntimeError(f"Unknown pulse: {peek_pulse}")

        #print(f"============ Step {(low_pulses + high_pulses)}: ({queue.queue[0]}) ============")
        step()

        #pprint((config, list(queue.queue)))

    return low_pulses, high_pulses, pulsed_modules


def part1(file: TextIOWrapper) -> int:
    config = parse_configuration(file)
    low_pulses, high_pulses = 0, 0
    p = dict()

    for i in range(1000000):
        ls, hs, pms = run_configuration(config)
        low_pulses += ls
        high_pulses += hs
        p.update(pms)
        print(i)

    print(pms["rx"])
    print(low_pulses, high_pulses)
    return low_pulses * high_pulses


def part2(file: TextIOWrapper) -> int:
    config = parse_configuration(file)
    presses = 0
    module_high_periods = dict[str, int]()

    rx_sources = {name for name, module in config.items() if "rx" in module.targets}
    assert len(rx_sources) == 1
    rx_source = rx_sources.pop()

    print(config[rx_source].inputs)

    seen = dict[str, int]()

    for _ in range(10000):
        presses += 1
        _, _, pms = run_configuration(config)

        for input in config[rx_source].inputs:
            if pms.get(input, (0, 0))[1] == 1:
                if input not in seen:
                    seen[input] = presses
                else:
                    assert presses % seen[input] == 0

    print(seen)

if __name__ == "__main__":
    # with open("input.txt") as file:
    #     print(part1(file))

    with open("input.txt") as file:
        print(part2(file))
