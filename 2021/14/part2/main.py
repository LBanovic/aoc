import sys
from collections import Counter
from pathlib import Path

input_file = Path(sys.argv[1])
rules = {}
for i, line in enumerate(input_file.open()):
    if i == 0:
        template = line.strip()
    if i > 1:
        source, target = line.strip().split('->')
        source, target = source.strip(), target.strip()
        rules[source.strip()] = (source[0] + target), (target + source[1])

template_counter = Counter()
for j in range(len(template)):
    if j + 2 > len(template):
        break
    template_counter[template[j:j + 2]] += 1

character_counter = Counter(template)
N_STEPS = 40
for _ in range(N_STEPS):
    new_counter = template_counter.copy()
    for code, count in template_counter.items():
        part1, part2 = rules[code]
        new_counter[code] -= count
        new_counter[part1] += count
        new_counter[part2] += count
        character_counter[part1[-1]] += count
    template_counter = new_counter

print(max(character_counter.values()) - min(character_counter.values()))
