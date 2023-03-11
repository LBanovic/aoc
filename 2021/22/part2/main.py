import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
from tqdm import tqdm

input_file = Path(sys.argv[1])


def parse():
    steps = []
    for line in input_file.open():
        xyz = list(map(int, re.findall(r'\d+|-\d+', line)))
        on = len(re.findall('on', line)) > 0
        start_xyz = xyz[0], xyz[2], xyz[4]
        end_xyz = xyz[1] + 1, xyz[3] + 1, xyz[5] + 1
        steps.append(RebootStep(tuple(start_xyz), tuple(end_xyz), on))
    return steps


@dataclass(frozen=True)
class RebootStep:
    start_xyz: Tuple[int, int, int]
    end_xyz: Tuple[int, int, int]
    on: bool

    def get_start_end_for_axis(self, axis: int) -> Tuple[int, int]:
        return self.start_xyz[axis], self.end_xyz[axis]


steps = parse()
xs, ys, zs = set(), set(), set()
for step in steps:
    xs.update(step.get_start_end_for_axis(0))
    ys.update(step.get_start_end_for_axis(1))
    zs.update(step.get_start_end_for_axis(2))
xs, ys, zs = tuple(map(sorted, (xs, ys, zs)))

x_inverted = {x: i for i, x in enumerate(xs)}
y_inverted = {y: i for i, y in enumerate(ys)}
z_inverted = {z: i for i, z in enumerate(zs)}

grid = np.zeros((len(x_inverted), len(y_inverted), len(z_inverted)), dtype=bool)

for step in tqdm(steps):
    start_x, end_x = step.get_start_end_for_axis(0)
    start_y, end_y = step.get_start_end_for_axis(1)
    start_z, end_z = step.get_start_end_for_axis(2)

    grid[x_inverted[start_x]:x_inverted[end_x],
         y_inverted[start_y]:y_inverted[end_y],
         z_inverted[start_z]:z_inverted[end_z]] = step.on


on_values = np.column_stack(np.where(grid))

total = 0
for i, j, k in tqdm(on_values):
    total += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j]) * (zs[k + 1] - zs[k])

print(total)
