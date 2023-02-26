import sys
from pathlib import Path

input_file = Path(sys.argv[1])

count_increased = 0
previous = None
for line in input_file.open():
    current = int(line)
    if previous:
        count_increased += current > previous
    previous = current

print(count_increased)