import sys
from copy import deepcopy
from pathlib import Path

input_file = Path(sys.argv[1])

cucumber_grid = [list(line.strip()) for line in input_file.open()]

height = len(cucumber_grid)
width = len(cucumber_grid[0])

n_steps = 0
while True:
    new_grid = deepcopy(cucumber_grid)
    changed = False

    for i, row in enumerate(cucumber_grid):
        for j, element in enumerate(row):
            if element == '>':
                next_i, next_j = i, (j + 1) % width
                if cucumber_grid[next_i][next_j] == '.':
                    new_grid[next_i][next_j] = cucumber_grid[i][j]
                    new_grid[i][j] = '.'
                    changed = True

    cucumber_grid = deepcopy(new_grid)
    for i, row in enumerate(cucumber_grid):
        for j, element in enumerate(row):
            if element == 'v':
                next_i, next_j = (i + 1) % height, j
                if cucumber_grid[next_i][next_j] == '.':
                    new_grid[next_i][next_j] = cucumber_grid[i][j]
                    new_grid[i][j] = '.'
                    changed = True
    n_steps += 1
    if not changed:
        break

    cucumber_grid = new_grid

print(n_steps)
