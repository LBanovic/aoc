import sys
from pathlib import Path
from typing import Tuple, List

input_file = Path(sys.argv[1])
risk_map = [list(map(int, line.strip())) for line in input_file.open()]
side = len(risk_map)

for line in risk_map:
    for i in range(1, 5):
        line.extend([line[j] + i for j in range(side)])

for i in range(1, 5):
    for j in range(side):
        risk_map.append([el + i for el in risk_map[j]])

side = len(risk_map)
for row in range(side):
    for col in range(side):
        while risk_map[row][col] > 9:
            risk_map[row][col] -= 9

start = (0, 0)
end = side - 1, side - 1


def adjacent(point: Tuple[int, int]) -> List[Tuple[int, int]]:
    row, col = point
    for dr in (-1, 1):
        next_row = row + dr
        if 0 <= next_row < side:
            yield next_row, col
    for dc in (-1, 1):
        next_col = col + dc
        if 0 <= next_col < side:
            yield row, next_col


def dijkstra(start: Tuple[int, int]) -> int:
    maxval = sum(sum(risk_line) for risk_line in risk_map)
    shortest = set()
    distances = {start: 0}
    candidates = {start}
    while len(shortest) < side ** 2:
        best_candidate = min(candidates, key=lambda k: distances[k])
        shortest.add(best_candidate)
        candidates.remove(best_candidate)
        for row, col in adjacent(best_candidate):
            distances[row, col] = min(distances.get((row, col), maxval), distances[best_candidate] + risk_map[row][col])
            if (row, col) not in shortest:
                candidates.add((row, col))
    return distances[end]

print(dijkstra(start))
