import sys
from functools import cache
from pathlib import Path
from typing import Tuple, List

input_file = Path(sys.argv[1])
risk_map = [list(map(int, line.strip())) for line in input_file.open()]

side = len(risk_map)
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
    shortest = set()
    distances = {
        (row, col): sum(sum(risk_line) for risk_line in risk_map)
        for row in range(side) for col in range(side)
    }
    distances[start] = 0
    while len(shortest) < side ** 2:
        candidates = set(distances.keys()) - shortest
        best_candidate = min(candidates, key=lambda k: distances[k])
        shortest.add(best_candidate)
        for row, col in adjacent(best_candidate):
            distances[row, col] = min(distances[row, col], distances[best_candidate] + risk_map[row][col])
    return distances[end]

print(dijkstra(start))