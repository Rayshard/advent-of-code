from dataclasses import dataclass
from io import TextIOWrapper
import re
from itertools import combinations
from typing import Optional

@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @property
    def slope_2D(self) -> float:
        return self.vy / self.vx

    def y_at_x(self, x: float) -> float:
        return self.slope_2D * (x - self.x) + self.y

    def __repr__(self) -> str:
        return f"{self.x}, {self.y}, {self.z} @ {self.vx}, {self.vy}, {self.vz}"


def calculate_x_intersection(hailstone_a: Hailstone, hailstone_b: Hailstone) -> Optional[float]:
    if hailstone_a.slope_2D == hailstone_b.slope_2D:
        return None

    return (hailstone_b.y - hailstone_a.y + hailstone_a.slope_2D * hailstone_a.x - hailstone_b.slope_2D * hailstone_b.x) / (hailstone_a.slope_2D - hailstone_b.slope_2D)


def cross_inside_test_area(hailstone_a: Hailstone, hailstone_b: Hailstone, test_area_boundary: tuple[int, int]) -> bool:
    if (x_int := calculate_x_intersection(hailstone_a, hailstone_b)) is None:
        return False

    t_a = (x_int - hailstone_a.x) / hailstone_a.vx
    t_b = (x_int - hailstone_b.x) / hailstone_b.vx

    if t_a < 0 or t_b < 0:
        return False

    y_int = hailstone_a.y_at_x(x_int)

    test_area_min, test_area_max = test_area_boundary
    return (test_area_min <= x_int <= test_area_max) and (test_area_min <= y_int <= test_area_max)

def part1(file: TextIOWrapper) -> int:
    hailstones = list[Hailstone]()
    test_area_boundary = (7, 27)

    for line in file:
        x, y, z, vx, vy, vz = (int(i) for i in re.split(r",?\s+@?\s*", line.strip()))
        hailstones.append(Hailstone(x, y, z, vx, vy, vz))

    return sum(cross_inside_test_area(hailstone_a, hailstone_b, test_area_boundary) for hailstone_a, hailstone_b in combinations(hailstones, 2))


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))
