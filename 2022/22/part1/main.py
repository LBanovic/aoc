import re
import sys
from enum import Enum
from pathlib import Path
from typing import Tuple, Dict, Optional

from tqdm import tqdm

input_file = Path(sys.argv[1])


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def change(self, rotation: str) -> 'Direction':
        curr_val = self.value
        direction = 1 if rotation == 'R' else -1
        return Direction((curr_val + direction) % len(Direction))


class Cell:

    def __init__(self, location: Tuple[int, int], mark: str):
        self.location = location
        self.mark = mark
        self.is_wall = mark == '#'
        self.is_valid = mark != ' '
        self.neighbours: Dict[Direction, Optional['Cell']] = {
            Direction.RIGHT: None,
            Direction.LEFT: None,
            Direction.UP: None,
            Direction.DOWN: None
        }

    def set_neighbour(self, direction: Direction, cell: 'Cell') -> None:
        self.neighbours[direction] = cell

    def move(self, direction: Direction) -> Optional['Cell']:
        neighbour = self.neighbours[direction]
        return neighbour

    def __repr__(self):
        return f'{self.location}: {self.mark}'


grid = {}
locating_grid = True
with input_file.open() as txt:
    for y, line in enumerate(txt):
        locating_grid = locating_grid and bool(line.strip())
        if locating_grid:
            for x, ch in enumerate(line):
                if ch in ('.', '#'):
                    grid[(x, y)] = Cell((x, y), ch)
        elif line.strip():
            instructions = re.findall(r'(R|L|\d+)', line)

max_x = max(grid.keys(), key=lambda t: t[0])[0]
max_y = max(grid.keys(), key=lambda t: t[1])[1]

modulo_x = max_x + 1
modulo_y = max_y + 1


for (x, y), cell in tqdm(grid.items(), total=len(grid)):
    right_neighbour = ((x + 1) % modulo_x, y)
    while right_neighbour not in grid:
        new_x, new_y = right_neighbour
        right_neighbour = ((new_x + 1) % modulo_x, new_y)
    cell.set_neighbour(Direction.RIGHT, grid[right_neighbour])

    left_neighbour = ((x - 1) % modulo_x, y)
    while left_neighbour not in grid:
        new_x, new_y = left_neighbour
        left_neighbour = ((new_x - 1) % modulo_x, new_y)
    cell.set_neighbour(Direction.LEFT, grid[left_neighbour])

    up_neighbour = (x, (y - 1) % modulo_y)
    while up_neighbour not in grid:
        new_x, new_y = up_neighbour
        up_neighbour = (new_x, (new_y - 1) % modulo_y)
    cell.set_neighbour(Direction.UP, grid[up_neighbour])

    down_neighbour = (x, (y + 1) % modulo_y)
    while down_neighbour not in grid:
        new_x, new_y = down_neighbour
        down_neighbour = (new_x, (new_y + 1) % modulo_y)
    cell.set_neighbour(Direction.DOWN, grid[down_neighbour])

current_direction = Direction.RIGHT
current_cell = grid[min(grid.keys(), key=lambda t: (t[1], t[0]))]
for instruction in instructions:
    x, y = current_cell.location
    if instruction in ('R', 'L'):
        current_direction = current_direction.change(instruction)
    else:
        move = int(instruction)
        for _ in range(move):
            next_cell = current_cell.move(current_direction)
            if next_cell.is_wall:
                break
            current_cell = next_cell


x, y = current_cell.location
print((y + 1) * 1000 + (x + 1) * 4 + current_direction.value)
