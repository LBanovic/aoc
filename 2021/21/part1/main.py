import re
import sys
from pathlib import Path

input_file = Path(sys.argv[1])

positions = []
scores = []
for line in input_file.open():
    digits = re.findall(r'\d+', line.strip())
    positions.append(int(digits[1]) - 1)
    scores.append(0)

MAX_POS = 10

max_rolls = 100
available_rolls = list(i + 1 for i in range(100))
current_roll_index = 0

ended = False
while True:
    player_1_roll = 0
    for _ in range(3):
        player_1_roll += available_rolls[current_roll_index % max_rolls]
        current_roll_index += 1
    positions[0] = (positions[0] + player_1_roll) % MAX_POS
    scores[0] += positions[0] + 1
    if scores[0] >= 1000:
        break

    player_2_roll = 0
    for _ in range(3):
        player_2_roll += available_rolls[current_roll_index % max_rolls]
        current_roll_index += 1
    positions[1] = (positions[1] + player_2_roll) % MAX_POS
    scores[1] += positions[1] + 1
    if scores[1] >= 1000:
        break

print(min(scores) * current_roll_index)
