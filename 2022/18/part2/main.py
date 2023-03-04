import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Set, List

input_file = Path(sys.argv[1])


@dataclass
class Cube:
    x: int
    y: int
    z: int
    sides: List[int] = field(default_factory=lambda: [1] * 6)  # left, right, bottom, top, back, front

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def move(self, dx: int, dy: int, dz: int) -> 'Cube':
        x = self.x + dx
        y = self.y + dy
        z = self.z + dz
        return Cube(x, y, z)


def update_cubes(cube1: Cube, cube2: Cube, diff: int, ind1: int, ind2: int) -> None:
    if diff < 0:
        cube1.sides[ind1] = 0
        cube2.sides[ind2] = 0
    elif diff > 0:
        cube1.sides[ind2] = 0
        cube2.sides[ind1] = 0


def cube_bounding_box(cubes: Set[Cube]):
    min_x, min_y, min_z = min(cube.x for cube in cubes), min(cube.y for cube in cubes), min(cube.z for cube in cubes)
    max_x, max_y, max_z = max(cube.x for cube in cubes), max(cube.y for cube in cubes), max(cube.z for cube in cubes)

    cube_start = Cube(min_x - 1, min_y - 1, min_z - 1)
    cube_end = Cube(max_x + 1, max_y + 1, max_z + 1)
    return cube_start, cube_end


def find_overlaps(cubes1, cubes2):
    for cube1 in cubes1:
        for cube2 in cubes2:
            xdiff = cube1.left - cube2.left
            ydiff = cube1.right - cube2.right
            zdiff = cube1.z - cube2.z

            if sum(abs(diff) for diff in (xdiff, ydiff, zdiff)) == 1:
                update_cubes(cube1, cube2, xdiff, 0, 1)
                update_cubes(cube1, cube2, ydiff, 2, 3)
                update_cubes(cube1, cube2, zdiff, 4, 5)


cubes = []
with input_file.open() as filein:
    for line in filein:
        position = map(int, line.split(','))
        cube = Cube(*position)
        cubes.append(cube)

droplet = set(cubes)
cube_start, cube_end = cube_bounding_box(droplet)

air = {cube_start}
queue = deque([cube_start])

updates = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1)
]

while queue:
    current_cube = queue.popleft()
    for dx, dy, dz in updates:
        new_cube = current_cube.move(dx, dy, dz)
        if not (cube_start.x <= new_cube.x <= cube_end.x and cube_start.y <= new_cube.y <= cube_end.y
                and cube_start.z <= new_cube.z <= cube_end.z):
            continue
        if new_cube in droplet or new_cube in air:
            continue

        air.add(new_cube)
        queue.append(new_cube)

find_overlaps(droplet, air)

total_exposed_surface_air_block = sum(sum(cube.sides) for cube in air)
print(6 * len(air) - total_exposed_surface_air_block)
