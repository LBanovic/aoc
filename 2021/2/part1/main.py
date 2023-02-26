import sys
from pathlib import Path

input_file = Path(sys.argv[1])
forward = 0
depth = 0

for line in input_file.open():
    val = int(line.split()[1])
    if line.startswith('forward'):
        forward += val
    elif line.startswith('up'):
        depth -= val
    else:
        depth += val

print(forward * depth)