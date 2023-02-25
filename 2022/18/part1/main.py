import sys
from dataclasses import dataclass
from pathlib import Path

input_file = Path(sys.argv[1])


@dataclass
class Cube:
    x: int
    y: int
    z: int

    def __post_init__(self):
        self.sides = [1] * 6  # left, right, bottom, top, back, front

def update_cubes(cube1: Cube, cube2: Cube, diff: int, ind1: int, ind2: int) -> None:
    if diff < 0:
        cube1.sides[ind1] = 0
        cube2.sides[ind2] = 0
    elif diff > 0:
        cube1.sides[ind2] = 0
        cube2.sides[ind1] = 0


cubes = []

with input_file.open() as filein:
    for line in filein:
        position = map(int, line.split(','))
        cube = Cube(*position)
        cubes.append(cube)

for i, cube1 in enumerate(cubes):
    for j, cube2 in enumerate(cubes[i + 1:]):
        xdiff = cube1.x - cube2.x
        ydiff = cube1.y - cube2.y
        zdiff = cube1.z - cube2.z

        if sum(abs(diff) for diff in (xdiff, ydiff, zdiff)) == 1:
            update_cubes(cube1, cube2, xdiff, 0, 1)
            update_cubes(cube1, cube2, ydiff, 2, 3)
            update_cubes(cube1, cube2, zdiff, 4, 5)

print(sum(sum(cube.sides) for cube in cubes))