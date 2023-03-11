import itertools
import re
import sys
from functools import cache
from pathlib import Path

input_file = Path(sys.argv[1])

positions = []
for line in input_file.open():
    digits = re.findall(r'\d+', line.strip())
    positions.append(int(digits[1]) - 1)

MAX_SCORE = 21

roll = [sum(combination) for combination in itertools.product(range(1, 4), repeat=3)]


@cache
def dfs(position1: int, position2: int, score1: int = 0, score2: int = 0):
    win_counts = [0, 0]
    for dp in roll:
        position1_new = position1 + dp
        position1_new = position1_new % 10
        score1_new = score1 + position1_new + 1
        if score1_new >= MAX_SCORE:
            win_counts[0] += 1
        else:
            p2_wins, p1_wins = dfs(position2, position1_new, score2, score1_new)
            win_counts[0] += p1_wins
            win_counts[1] += p2_wins
    return win_counts


win_counts = dfs(positions[0], positions[1])
print(max(win_counts))
