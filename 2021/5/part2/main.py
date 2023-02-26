import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Optional, Set

input_file = Path(sys.argv[1])


@dataclass
class Line:
    start: Tuple[int, int]
    end: Tuple[int, int]

    def __post_init__(self):
        if self.start[0] == self.end[0]:
            start, end = min(self.start[1], self.end[1]), max(self.start[1], self.end[1])
            self.points = set((self.start[0], p) for p in range(start, end + 1))
        elif self.start[1] == self.end[1]:
            start, end = min(self.start[0], self.end[0]), max(self.start[0], self.end[0])
            self.points = set((p, self.start[1]) for p in range(start, end + 1))
        else:
            dx = 1 if self.end[0] - self.start[0] > 0 else -1
            dy = 1 if self.end[1] - self.start[1] > 0 else -1
            self.points = set()
            x, y = self.start
            while True:
                self.points.add((x, y))
                if (x, y) == self.end:
                    break
                x += dx
                y += dy

    def __repr__(self):
        return f'{self.start} {self.end} {self.points}'

    def overlap(self, other: 'Line') -> Optional[Set[Tuple[int, int]]]:
        if self != other:
            intersection = self.points.intersection(other.points)
            return intersection


lines = []
for line in input_file.open():
    startstr, endstr = line.strip().split('->')
    start = tuple(map(int, startstr.strip().split(',')))
    end = tuple(map(int, endstr.strip().split(',')))
    lines.append(Line(start, end))

overlaps = set()
for i, line1 in enumerate(lines):
    for line2 in lines[i + 1:]:
        overlap = line1.overlap(line2)
        if overlap:
            overlaps.update(overlap)
print(len(overlaps))
