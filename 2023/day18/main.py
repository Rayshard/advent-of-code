from io import TextIOWrapper


Coord = tuple[int, int]


def part1(file: TextIOWrapper) -> int:
    position: Coord = (0, 0)
    trench: set[Coord] = {position}
    min_row, min_col, max_row, max_col = 0, 0, 0, 0

    for line in file:
        dir, amt, color = line.strip().split()
        amt = int(amt)
        color = color[2:-1]

        match dir:
            case "R":
                offset = (0, 1)
            case "L":
                offset = (0, -1)
            case "U":
                offset = (-1, 0)
            case "D":
                offset = (1, 0)
            case dir:
                raise NotImplementedError(dir)

        for _ in range(amt):
            row, col = (position[0] + offset[0], position[1] + offset[1])
            position = (row, col)
            trench.add(position)

            if row < min_row:
                min_row = row
            if row > max_row:
                max_row = row
            if col < min_col:
                min_col = col
            if col > max_col:
                max_col = col

    # Flood fill
    exterior_seen = set[Coord]()
    interior_seen = set[Coord](trench)

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if (row, col) in exterior_seen or (row, col) in interior_seen:
                continue

            to_visit: set[Coord] = {(row, col)}
            seen = set[Coord]()
            touched_exterior = False

            while to_visit:
                coord = to_visit.pop()
                coord_row, coord_col = coord

                if coord in trench:
                    continue

                seen.add(coord)

                if (
                    coord_row < min_row
                    or coord_row > max_row
                    or coord_col < min_col
                    or coord_col > max_col
                ):
                    touched_exterior = True
                    continue

                adj = [
                    (coord[0] - 1, coord[1]),
                    (coord[0] + 1, coord[1]),
                    (coord[0], coord[1] - 1),
                    (coord[0], coord[1] + 1),
                ]

                to_visit.update(a for a in adj if a not in seen)

            if touched_exterior:
                exterior_seen.update(seen)
            else:
                interior_seen.update(seen)

    return len(interior_seen)


def part2(file: TextIOWrapper) -> int:
    position: Coord = (0, 0)
    trench: set[Coord] = {position}
    min_row, min_col, max_row, max_col = 0, 0, 0, 0

    for line in file:
        color = line.strip().split()[2]
        amt = int(color[2:7], base=16)
        dir = int(color[-2])

        print(amt, dir)
        


if __name__ == "__main__":
    # with open("input.txt") as file:
    #     print(part1(file))

    with open("input.txt") as file:
        print(part2(file))
