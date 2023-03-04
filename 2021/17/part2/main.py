import re
import sys
from pathlib import Path
from typing import Optional

from tqdm import tqdm
import numba

input_file = Path(sys.argv[1])

numbers = re.findall(r'-*\d+', input_file.open().readlines()[0])
numbers = list(map(int, numbers))
x_range = tuple(numbers[:2])
y_range = tuple(numbers[2:])


@numba.jit(nopython=True)
def sign(x: int):
    return int(x > 0) - int(x < 0)


@numba.jit(nopython=True)
def test_velocity(min_x, max_x, min_y, max_y, vx: int, vy: int, timesteps=1000) -> Optional[int]:
    x, y = 0, 0
    max_h = 0
    for t in range(timesteps):
        x += vx
        y += vy
        if min_x <= x <= max_x and min_y <= y <= max_y:
            return max_h

        max_h = max(y, max_h)

        vy -= 1
        vx -= sign(vx)
    return None


max_h = 0
count = 0
for vx in tqdm(range(2000)):
    for vy in range(-1200, 1200):
        h = test_velocity(x_range[0], x_range[1], y_range[0], y_range[1], vx, vy, timesteps=1000)
        if h is not None:
            count += 1
            max_h = max(max_h, h)
print(count)
