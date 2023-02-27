import sys
from pathlib import Path
from typing import Tuple, Set

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


def find_basin(x: int, y: int) -> Set[Tuple[int, int]]:
    queue = [(x, y)]
    basin = {(x, y)}
    while queue:
        x, y = queue.pop(0)
        for nx, ny in testers(x, y):
            if grid[y][x] <= grid[ny][nx] < 9:
                if (nx, ny) not in basin:
                    basin.add((nx, ny))
                    queue.append((nx, ny))
    return basin


basin_lens = []

for y, row in enumerate(grid):
    for x, val in enumerate(row):
        low_point = all(val < grid[ny][nx] for nx, ny in testers(x, y))
        if low_point:
            basin_lens.append(len(find_basin(x, y)))

total = 1
for blen in sorted(basin_lens)[-3:]:
    print(blen)
    total *= blen
print(total)
