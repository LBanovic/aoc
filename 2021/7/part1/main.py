import sys
from pathlib import Path

input_file = Path(sys.argv[1])
positions = list(map(int, input_file.open().readlines()[0].split(',')))

'''
Median minimizes Manhattan distance, mean minimizes Euclidean distance.
'''


def calc(x, positions):
    return sum(abs(x - pos) for pos in positions)


positions = sorted(positions)
mid = len(positions) // 2
x_med = (positions[mid-1] + positions[mid]) // 2 if len(positions) % 2 == 0 else positions[mid]
print(calc(x_med, positions))