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
        rules[source.strip()] = source[0] + target + source[1]

base_template = template
N_STEPS = 10
for i in range(N_STEPS):
    counter = Counter(template)
    new_template = []
    for j in range(len(template)):
        if j + 2 > len(template):
            break
        code = template[j:j+2]
        replacement = rules[code]
        if j == 0:
            new_template.append(replacement)  # apply the whole replacement
        else:
            new_template.append(replacement[1:])  # don't put the first letter because it's the last letter of previous replacement
    template = ''.join(new_template)

counter = Counter(template)
print(max(counter.values()) - min(counter.values()))

