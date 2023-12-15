from io import TextIOWrapper
from typing import Optional


def part1(file: TextIOWrapper) -> int:
    result = 0

    def hash(s: str) -> int:
        current_value = 0

        for c in s:
            current_value += ord(c)
            current_value *= 17
            current_value %= 256

        return current_value

    for step in file.readline().strip().split(","):
        result += hash(step)

    return result


def part2(file: TextIOWrapper) -> int:
    boxes = [list[tuple[str, int]]() for _ in range(256)]

    def hash(s: str) -> tuple[str, int, Optional[int]]:
        current_value = 0
        label = ""

        for i, c in enumerate(s):
            if c == "=":
                return label, current_value, int(s[i + 1:])
            elif c == "-":
                return label, current_value, None

            current_value += ord(c)
            current_value *= 17
            current_value %= 256
            label += c

        raise RuntimeError(f"Did not find = or - in string: {s}")

    for step in file.readline().strip().split(","):
        label, box_id, focal_length = hash(step)

        found = False
        box = boxes[box_id]

        for i, (item_label, item_focal_length) in enumerate(box):
            if item_label == label:
                found = True
                break
        
        if focal_length is not None:
            if found:
                box[i] = (label, focal_length)
            else:
                box.append((label, focal_length))
        elif found:
            box.remove((item_label, item_focal_length))

    result = 0

    for i, box in enumerate(boxes):
        for j, (_, focal_length) in enumerate(box):
            result += (i + 1) * (j + 1) * focal_length
    
    return result



if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

    with open("input.txt") as file:
        print(part2(file))
