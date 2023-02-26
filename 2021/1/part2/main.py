import sys
from pathlib import Path

input_file = Path(sys.argv[1])

count_increased = 0
previous = None
current = []
for i, line in enumerate(input_file.open()):
    if len(current) == 3:
        if previous:
            count_increased += sum(current) > previous
        previous = sum(current)
        current = current[1:]
    current.append(int(line))
count_increased += sum(current) > previous

print(count_increased)