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


def find_lor(rows_or_cols: list[str]) -> Optional[int]:
    for i in range(len(rows_or_cols) - 1):
        left = rows_or_cols[i]
        right = rows_or_cols[i + 1]

        if left == right:
            offset = 1

            while True:
                if (left_pos := i - offset) == -1 or (right_pos := i + 1 + offset) == len(rows_or_cols):
                    return i + 1
                
                rows_or_col_1 = rows_or_cols[left_pos]
                rows_or_col_2 = rows_or_cols[right_pos]

                if rows_or_col_1 != rows_or_col_2:
                    break

                offset += 1

    return None


def part1(patterns: list[tuple[list[str], list[str]]]) -> int:
    result = 0

    for i, (rows, cols) in enumerate(patterns):
        if (vertical_lor := find_lor(cols)) is not None:
            result += vertical_lor
        elif (horizontal_lor := find_lor(rows)) is not None:
            result += horizontal_lor * 100
        else:
            raise RuntimeError(f"No LOR found for pattern #{i}")

    return result

if __name__ == "__main__":
    with open("input.txt") as file:
        patterns = parse_patterns(file)

    print(part1(patterns))
