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
        else:
            start, end = min(self.start[0], self.end[0]), max(self.start[0], self.end[0])
            self.points = set((p, self.start[1]) for p in range(start, end + 1))

    def overlap(self, other: 'Line') -> Optional[Set[Tuple[int, int]]]:
        if self != other:
            intersection = self.points.intersection(other.points)
            return intersection


lines = []
for line in input_file.open():
    startstr, endstr = line.strip().split('->')
    start = tuple(map(int, startstr.strip().split(',')))
    end = tuple(map(int, endstr.strip().split(',')))
    if start[0] == end[0] or start[1] == end[1]:
        lines.append(Line(start, end))

overlaps = set()
for i, line1 in enumerate(lines):
    for line2 in lines[i + 1:]:
        overlap = line1.overlap(line2)
        if overlap:
            overlaps.update(overlap)
print(len(overlaps))
