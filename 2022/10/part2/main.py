import sys

X = 1
last_finished_cycle = 0

cursor_position = 0

sprite_start = 0
sprite_width = 3

for line in open(sys.argv[1]):
    if line.startswith('noop'):
        if X - 1 <= last_finished_cycle % 40 <= X + 1:
            print('##', end='')
        else:
            print('..', end='')
        last_finished_cycle += 1
        if last_finished_cycle % 40 == 0:
            print()
    else:
        value = int(line.split()[1])
        for i in range(2):
            if X - 1 <= last_finished_cycle % 40 <= X + 1:
                print('##', end='')
            else:
                print('..', end='')
            last_finished_cycle += 1
            if last_finished_cycle % 40 == 0:
                print()

        X += value