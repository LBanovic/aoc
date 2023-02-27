import sys
from pathlib import Path

input_file = Path(sys.argv[1])
positions = list(map(int, input_file.open().readlines()[0].split(',')))

'''
Median minimizes Manhattan distance, mean minimizes Euclidean distance.
'''


def calc(x, positions):
    total = 0
    for pos in positions:
        diff = abs(pos - x)
        total += (diff + 1) * diff // 2
    return total


start = min(positions)
end = max(positions)

best = min(calc(m, positions) for m in range(start, end + 1))
print(best)
