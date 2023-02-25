import sys

X = 1
last_finished_cycle = 0

max_interesting_cycle = 220
current_interesting_cycle = 20

signal_strengths = []

for line in open(sys.argv[1]):
    if line.startswith('noop'):
        if last_finished_cycle + 1 == current_interesting_cycle:
            signal_strengths.append(current_interesting_cycle * X)
            current_interesting_cycle += 40
        last_finished_cycle += 1
    else:
        value = int(line.split()[1])
        for i in range(2):
            if last_finished_cycle + 1 == current_interesting_cycle:
                signal_strengths.append(current_interesting_cycle * X)
                current_interesting_cycle += 40
            last_finished_cycle += 1

        X += value

print(signal_strengths)
print(sum(signal_strengths))