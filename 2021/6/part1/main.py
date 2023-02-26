import sys
from pathlib import Path

input_file = Path(sys.argv[1])
current_timers = list(map(int, input_file.open().readlines()[0].strip().split(',')))

steps = 80
for _ in range(steps):
    new_timers = []
    for timer in current_timers:
        if timer == 0:
            new_timers.append(6)
            new_timers.append(8)
        else:
            new_timers.append(timer - 1)
    current_timers = new_timers

print(len(new_timers))
