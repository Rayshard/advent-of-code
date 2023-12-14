from collections import defaultdict
from io import TextIOWrapper
from typing import Optional


def parse_patterns(file: TextIOWrapper) -> list[tuple[list[str], list[str]]]:
    patterns = list[tuple[list[str], list[str]]]()
    
    current_rows = list[str]()
    current_cols = defaultdict[int, str](str)
    
    for line in file:
        if (line := line.strip()):
            current_rows.append(line)

            for i, c in enumerate(line):
                current_cols[i] += c
        else:
            patterns.append((current_rows, [col for _, col in sorted(current_cols.items())]))
            
            current_rows = list[str]()
            current_cols = defaultdict[int, str](str)

    patterns.append((current_rows, [col for _, col in sorted(current_cols.items())]))
    return patterns


def num_differences(str1: str, str2: str) -> int:
    assert len(str1) == len(str2)
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))


def find_lor(rows_or_cols: list[str]) -> Optional[int]:
    for i in range(len(rows_or_cols) - 1):
        left = rows_or_cols[i]
        right = rows_or_cols[i + 1]

        if left == right:
            offset = 1

            while True:
                if (left_pos := i - offset) == -1 or (right_pos := i + 1 + offset) == len(rows_or_cols):
                    return i + 1
                
                left = rows_or_cols[left_pos]
                right = rows_or_cols[right_pos]

                if left != right:
                    break

                offset += 1

    return None


def find_lor_with_smudge(rows_or_cols: list[str], exclude_possibility: int = -1) -> Optional[int]:
    for i in range(len(rows_or_cols) - 1):
        left = rows_or_cols[i]
        right = rows_or_cols[i + 1]
        smudge_found = num_differences(left, right) == 1

        if left == right or smudge_found:
            offset = 1

            while True:
                if (left_pos := i - offset) == -1 or (right_pos := i + 1 + offset) == len(rows_or_cols):
                    if (lor := i + 1) == exclude_possibility:
                        break
                    else:
                        return lor
                
                left = rows_or_cols[left_pos]
                right = rows_or_cols[right_pos]

                if left != right:
                    if not smudge_found and num_differences(left, right) == 1:
                        smudge_found = True
                    else:
                        break

                offset += 1

    return None


def part1and2(patterns: list[tuple[list[str], list[str]]]) -> int:
    result1, result2 = 0, 0

    for i, (rows, cols) in enumerate(patterns):
        if (vertical_lor := find_lor(cols)) is not None:
            result1 += vertical_lor

            if (vertical_lor_ws := find_lor_with_smudge(cols, vertical_lor)) is not None:
                result2 += vertical_lor_ws
            elif (horizontal_lor_ws := find_lor_with_smudge(rows)) is not None:
                result2 += horizontal_lor_ws * 100
            else:
                raise RuntimeError(f"No LOR found for smudged pattern #{i}")
        elif (horizontal_lor := find_lor(rows)) is not None:
            result1 += horizontal_lor * 100

            if (vertical_lor_ws := find_lor_with_smudge(cols)) is not None:
                result2 += vertical_lor_ws
            elif (horizontal_lor_ws := find_lor_with_smudge(rows, horizontal_lor)) is not None:
                result2 += horizontal_lor_ws * 100
            else:
                raise RuntimeError(f"No LOR found for smudged pattern #{i}")
        else:
            raise RuntimeError(f"No LOR found for pattern #{i}")

    return result1, result2

if __name__ == "__main__":
    with open("input.txt") as file:
        patterns = parse_patterns(file)

    print(part1and2(patterns))
