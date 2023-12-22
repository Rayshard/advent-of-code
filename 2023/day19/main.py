from io import TextIOWrapper
from typing import Callable

import re


WorkflowRule = tuple[Callable[[], bool], str]
Workflow = tuple[str, dict[str, WorkflowRule]]

def part1(file: TextIOWrapper) -> int:
    workflows = dict[str, Workflow]()

    for line in file:
        if not (line := line.strip()):
            break

        name, rules_raw = line.strip()[:-1].split("{")
        rules_raw = rules_raw.split(",")
        rules = dict[str, WorkflowRule]()

        for raw_rule in rules_raw:
            match raw_rule.split(":"):
                case [dest]:
                    rules[None] = (lambda _: True, dest)
                case [expr, dest] if ">" in expr:
                    part, value = expr.split(">")
                    rules[part] = (lambda x: print(x, ">", value) or x > int(value), dest)
                case [expr, dest] if "<" in expr:
                    part, value = expr.split("<")
                    rules[part] = (lambda x: print(x, "<", value) or x < int(value), dest)
                case raw_rule:
                    raise RuntimeError(f"Invalid rule: {raw_rule}")

        workflows[name] = (name, rules)

    accepteds = 0

    for line in file:
        part_ratings = [tuple(item.split("=")) for item in line.strip()[1:-1].split(",")]
        current_workflow = workflows["in"]

        while True:
            dest = current_workflow[1][None][1]
            current_workflow_name, current_workflow_rules = current_workflow

            for rating_id, rating_value in part_ratings:
                print(current_workflow_name, rating_id, rating_value)
                rating_value = int(rating_value)

                if rating_id in current_workflow_rules:
                    if current_workflow_rules[rating_id][0](rating_value):
                        dest = current_workflow_rules[rating_id][1]
                        print(current_workflow_name, rating_id, rating_value, "Passed")
                        break
                    else:
                        print(current_workflow_name, rating_id, rating_value, "Failed")


            match dest:
                case "A":
                    accepteds += 1
                    break
                case "R":
                    break
                case dest:
                    current_workflow = workflows[dest]

    return accepteds


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

