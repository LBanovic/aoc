import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Set

input_file = Path(sys.argv[1])


@dataclass
class Instruction:
    x: int = None
    y: int = None

    def __post_init__(self):
        if self.x is None:
            self.x = max(point[0] for point in points)
        if self.y is None:
            self.y = max(point[1] for point in points)

    def fold_over(self, points: Set[Tuple[int]]) -> Set[Tuple[int]]:
        new_points = set()
        for point in points:
            if point[0] > self.x:
                point = self.x - (point[0] - self.x), point[1]
                # TODO calculation of reflection
            if point[1] > self.y:
                point = point[0], self.y - (point[1] - self.y)
                # TODO calculation of reflection
            new_points.add(point)
        return new_points


now_instruction = None
points = set()
instructions = []
with input_file.open() as infile:
    for line in infile:
        if not line.strip():
            now_instruction = True
        elif not now_instruction:
            point = tuple(map(int, line.strip().split(',')))
            points.add(point)
        else:
            split_line = line.strip().split('=')
            indict = {split_line[0][-1]: int(split_line[1])}
            instructions.append(Instruction(**indict))

points = instructions[0].fold_over(points)
print(len(points))