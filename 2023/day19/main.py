from dataclasses import dataclass
from io import TextIOWrapper
from typing import Literal


WorkflowRule = tuple[str, Literal["<", ">"], int, str] | str


@dataclass(frozen=True)
class Workflow:
    name: str
    rules: list[WorkflowRule]


def parse_workflows(file: TextIOWrapper) -> dict[str, Workflow]:
    workflows = dict[str, Workflow]()

    for line in file:
        if not (line := line.strip()):
            break

        name, rules_raw = line.strip()[:-1].split("{")
        rules_raw = rules_raw.split(",")
        rules = list[tuple[str, WorkflowRule]]()

        for raw_rule in rules_raw:
            match raw_rule.split(":"):
                case [dest]:
                    rule = dest
                case [expr, dest] if ">" in expr:
                    rating_name, value = expr.split(">")
                    rule = (rating_name, ">", int(value), dest)
                case [expr, dest] if "<" in expr:
                    rating_name, value = expr.split("<")
                    rule = (rating_name, "<", int(value), dest)
                case raw_rule:
                    raise RuntimeError(f"Invalid rule: {raw_rule}")

            rules.append(rule)

        workflows[name] = Workflow(name, rules)

    return workflows

def part1(file: TextIOWrapper) -> int:
    workflows = parse_workflows(file)
    accepted = list[dict[str, int]]()

    for line in file:
        part_ratings = {name: int(value) for name, value in (item.split("=") for item in line.strip()[1:-1].split(","))}
        current_workflow = workflows["in"]

        while True:
            for rule in current_workflow.rules:
                match rule:
                    case rating_name, operation, value, dest if (rating_value := part_ratings.get(rating_name)) is not None:
                        match = False

                        match operation:
                            case "<":
                                match = rating_value < value
                            case ">":
                                match = rating_value > value
                            case _:
                                raise RuntimeError(operation)

                        if match:
                            break
                    case dest:
                        break

            match dest:
                case "A":
                    accepted.append(part_ratings)
                    break
                case "R":
                    break
                case dest:
                    current_workflow = workflows[dest]

    for pr in accepted:
        print(pr)

    return sum(sum(pr.values()) for pr in accepted)


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

