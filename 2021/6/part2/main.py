import sys
from collections import Counter
from pathlib import Path

input_file = Path(sys.argv[1])
current_timers = list(map(int, input_file.open().readlines()[0].strip().split(',')))

steps = 256

lanternfish = {
    i: sum(a == i for a in current_timers) for i in range(9)
}


for step in range(steps):
    new_lanternfish = {}
    for timer, count in lanternfish.items():
        if timer == 0:
            new_lanternfish[6] = new_lanternfish.get(6, 0) + count
            new_lanternfish[8] = new_lanternfish.get(8, 0) + count
        else:
            new_lanternfish[timer - 1] = new_lanternfish.get(timer - 1, 0) + count
    lanternfish = new_lanternfish

print(sum(lanternfish.values()))
