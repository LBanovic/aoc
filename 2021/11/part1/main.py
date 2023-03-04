import sys
from pathlib import Path

input_file = Path(sys.argv[1])
grid = list(list(map(int, line.strip())) for line in input_file.open())
width = len(grid[0])
height = len(grid)


def next(i, j):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < height and 0 <= nj < width:
                yield ni, nj


def flash(i, j):
    if grid[i][j] > 9 and (i, j) not in flashed:
        flashed.add((i, j))
        for ni, nj in next(i, j):
            grid[ni][nj] += 1
            if (ni, nj) not in flashed:
                flash(ni, nj)


N_STEPS = 100
n_flashes = 0
for step in range(N_STEPS):
    for i in range(height):
        for j in range(width):
            grid[i][j] += 1

    flashed = set()
    for i in range(height):
        for j in range(width):
            flash(i, j)

    for i in range(height):
        for j in range(width):
            if (i, j) in flashed:
                grid[i][j] = 0

    n_flashes += len(flashed)
print(n_flashes)
