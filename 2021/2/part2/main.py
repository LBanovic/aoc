import sys
from pathlib import Path

input_file = Path(sys.argv[1])
forward = 0
depth = 0
aim = 0

for line in input_file.open():
    val = int(line.split()[1])
    if line.startswith('forward'):
        forward += val
        depth += val * aim
    elif line.startswith('up'):
        aim -= val
    else:
        aim += val

print(forward * depth)