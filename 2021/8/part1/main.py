import sys
from pathlib import Path

input_file = Path(sys.argv[1])
valid_lens = (2, 3, 4, 7)
count = 0
for line in input_file.open():
    digits = line.strip().split('|')[-1]
    for digit in digits.strip().split():
        if len(digit) in valid_lens:
            count += len(digit) in valid_lens
print(count)
