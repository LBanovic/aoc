import math
import sys
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Tuple, Generator

input_file = Path(sys.argv[1])

in_lines = list(line.strip() for line in input_file.open())

width = len(in_lines[0].strip()) - 2
height = len(in_lines) - 2


class BlizzardDirection(Enum):
    Left = "<"
    Right = ">"
    Up = "^"
    Down = "v"


blizzard_direction_increment = {
    BlizzardDirection.Left: (-1, 0),
    BlizzardDirection.Right: (1, 0),
    BlizzardDirection.Up: (0, -1),
    BlizzardDirection.Down: (0, 1)
}

blizzards = {
    BlizzardDirection.Left: set(),
    BlizzardDirection.Right: set(),
    BlizzardDirection.Up: set(),
    BlizzardDirection.Down: set()
}


def check_collision(location: Tuple[int, int], blizzard_direction, time: int) -> bool:
    nx, ny = location
    dx, dy = blizzard_direction_increment[blizzard_direction]
    x, y = (nx - dx * time) % width, (ny - dy * time) % height
    return (x, y) in blizzards[blizzard_direction]


def get_next_states(x, y, time: int) -> Generator:
    potential_positions = ((x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx == 0 or dy == 0)
    for position in potential_positions:
        nx, ny = position
        if position not in (start_loc, end_loc):
            if nx >= width or nx < 0 or ny >= height or ny < 0:
                continue
            collision = False
            for blizzard_direction in BlizzardDirection:
                collision = check_collision(position, blizzard_direction, time)
                if collision:
                    break

            if collision:
                continue
        yield position


def bfs(start_loc: Tuple[int, int], end_loc: Tuple[int, int], time: int, width: int, height: int) -> int:
    seen = set()
    queue = deque([(start_loc, time)])
    lcm = width * height // math.gcd(width, height)
    while queue:
        state, time = queue.popleft()
        time += 1
        for next_state in get_next_states(*state, time):
            if next_state == end_loc:
                return time
            key = next_state, time % lcm
            if key in seen:
                continue
            seen.add(key)
            queue.append((next_state, time))


for y, line in enumerate(input_file.open()):
    for x, ch in enumerate(line):
        try:
            direction = BlizzardDirection(ch)
            blizzards[direction].add((x - 1, y - 1))
        except ValueError:
            pass

start_loc = (0, -1)
end_loc = (width - 1, height)

objectives = ((start_loc, end_loc), (end_loc, start_loc), (start_loc, end_loc))
total = 0
for s, e in objectives:
    n = bfs(s, e, total, width, height) - total
    total += n

print(total)
