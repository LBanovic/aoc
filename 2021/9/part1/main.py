import sys
from pathlib import Path
from typing import Tuple

input_file = Path(sys.argv[1])
grid = [list(map(int, line.strip())) for line in input_file.open()]
height = len(grid)
width = len(grid[0])


def testers(x: int, y: int) -> Tuple[int, int]:
    for dy in (-1, 1):
        new_y = y + dy
        if 0 <= new_y < height:
            yield x, new_y
    for dx in (-1, 1):
        new_x = x + dx
        if 0 <= new_x < width:
            yield new_x, y

        for dx in (-1, 0, 1):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height and (dx == 0 or dy == 0):
                yield new_x, new_y


total = 0
for y, row in enumerate(grid):
    for x, val in enumerate(row):
        low_point = all(val < grid[ny][nx] for nx, ny in testers(x, y))
        if low_point:
            total += val + 1

print(total)
