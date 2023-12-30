from dataclasses import dataclass
from io import TextIOWrapper
from typing import Literal, Optional, Union


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

    return sum(sum(pr.values()) for pr in accepted)


def part2(file: TextIOWrapper) -> int:
    @dataclass(frozen=True)
    class Part:
        x: tuple[int, int] = (1, 4000)
        m: tuple[int, int] = (1, 4000)
        a: tuple[int, int] = (1, 4000)
        s: tuple[int, int] = (1, 4000)

        @property
        def x_count(self) -> int:
            return self.x[1] - self.x[0] + 1

        @property
        def m_count(self) -> int:
            return self.m[1] - self.m[0] + 1

        @property
        def a_count(self) -> int:
            return self.a[1] - self.a[0] + 1

        @property
        def s_count(self) -> int:
            return self.s[1] - self.s[0] + 1

        @property
        def combinations(self) -> int:
            return self.x_count * self.m_count * self.a_count * self.s_count

        def sub_part(self, rating_name: str, filter: tuple[Literal["<", ">"], int]) -> Union[tuple["Part", "Part"], "Part", None]:
            match rating_name, filter[0], filter[1]:
                case "x" , "<", filter_value if self.x[0] < filter_value:
                    cut = min(self.x[1], filter_value - 1)

                    if cut == self.x[1]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(x=(self.x[0], cut), m=self.m, a=self.a, s=self.s), Part(x=(cut + 1, self.x[1]), m=self.m, a=self.a, s=self.s)
                case "x" , ">", filter_value if self.x[1] > filter_value:
                    cut = max(self.x[0], filter_value)

                    if cut == self.x[0]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(x=(cut + 1, self.x[1]), m=self.m, a=self.a, s=self.s), Part(x=(self.x[0], cut), m=self.m, a=self.a, s=self.s)
                case "m" , "<", filter_value if self.m[0] < filter_value:
                    cut = min(self.m[1], filter_value - 1)

                    if cut == self.m[1]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(m=(self.m[0], cut), x=self.x, a=self.a, s=self.s), Part(m=(cut + 1, self.m[1]), x=self.x, a=self.a, s=self.s)
                case "m" , ">", filter_value if self.m[1] > filter_value:
                    cut = max(self.m[0], filter_value)

                    if cut == self.m[0]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(m=(cut + 1, self.m[1]), x=self.x, a=self.a, s=self.s), Part(m=(self.m[0], cut), x=self.x, a=self.a, s=self.s)
                case "a" , "<", filter_value if self.a[0] < filter_value:
                    cut = min(self.a[1], filter_value - 1)

                    if cut == self.a[1]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(a=(self.a[0], cut), m=self.m, x=self.x, s=self.s), Part(a=(cut + 1, self.a[1]), m=self.m, x=self.x, s=self.s)
                case "a" , ">", filter_value if self.a[1] > filter_value:
                    cut = max(self.a[0], filter_value)

                    if cut == self.a[0]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(a=(cut + 1, self.a[1]), m=self.m, x=self.x, s=self.s), Part(a=(self.a[0], cut), m=self.m, x=self.x, s=self.s)
                case "s" , "<", filter_value if self.s[0] < filter_value:
                    cut = min(self.s[1], filter_value - 1)

                    if cut == self.s[1]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(s=(self.s[0], cut), m=self.m, a=self.a, x=self.x), Part(s=(cut + 1, self.s[1]), m=self.m, a=self.a, x=self.x)
                case "s" , ">", filter_value if self.s[1] > filter_value:
                    cut = max(self.s[0], filter_value)

                    if cut == self.s[0]:
                        return Part(x=self.x, m=self.m, a=self.a, s=self.s)
                    else:
                        return Part(s=(cut + 1, self.s[1]), m=self.m, a=self.a, x=self.x), Part(s=(self.s[0], cut), m=self.m, a=self.a, x=self.x)

            return None


    workflows = parse_workflows(file)
    accepted = set[Part]()
    parts : list[tuple[Part, str]] = [(Part(), "in")]

    while parts:
        part, workflow = parts.pop()

        for rule in workflows[workflow].rules:
            match rule:
                case rating_name, operation, value, dest:
                    match part.sub_part(rating_name, (operation, value)):
                        case None:
                            pass
                        case valid_part, invalid_part:
                            if dest == "A":
                                accepted.add(valid_part)
                            elif dest == "R":
                                pass
                            else:
                                parts.append((valid_part, dest))

                            part = invalid_part
                        case sub_part:
                            parts.append((sub_part, dest))
                            break
                case "A":
                    accepted.add(part)
                    break
                case "R":
                    break
                case dest:
                    parts.append((part, dest))
                    break

    return sum(part.combinations for part in accepted)


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

    with open("input.txt") as file:
        print(part2(file))

