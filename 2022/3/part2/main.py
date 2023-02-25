import sys

characters = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]

priority_map = dict(zip(characters, range(1, 53)))

priority_sum = 0

lines = []

for line in open(sys.argv[1]):
    lines.append(set(line.strip()))
    if len(lines) == 3:
        repeated = (lines[0] & lines[1] & lines[2]).pop()
        priority_sum += priority_map[repeated]
        lines = []

print(priority_sum)