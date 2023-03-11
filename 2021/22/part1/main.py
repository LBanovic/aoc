import itertools
import re
import sys
from pathlib import Path
from typing import List, Set

input_file = Path(sys.argv[1])


def parse():
    steps = []
    for line in input_file.open():
        xyz = list(map(int, re.findall(r'\d+|-\d+', line)))
        on = len(re.findall('on', line)) > 0
        if all(-50 <= k <= 50 for k in xyz):
            steps.append(RebootStep(xyz[:2], xyz[2:4], xyz[4:], on))
    return steps


class RebootStep:

    def __init__(self, x_range: List[int], y_range: List[int], z_range: List[int], on: bool):
        x_range[1] += 1
        self.x_range = range(*x_range)
        y_range[1] += 1
        self.y_range = range(*y_range)
        z_range[1] += 1
        self.z_range = range(*z_range)
        self.on = on

    def point_set(self):
        return set(itertools.product(self.x_range, self.y_range, self.z_range))

    def execute(self, turned_on: Set):
        if self.on:
            return turned_on | self.point_set()
        else:
            intersection = turned_on & self.point_set()
            return turned_on - intersection


turned_on = set()
steps = parse()
for step in steps:
    turned_on = step.execute(turned_on)

print(len(turned_on))
