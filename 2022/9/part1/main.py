import sys

head_position = [0, 0]
tail_position = [0, 0]

visited = {tuple(tail_position)}


def update_tail():
    dx = head_position[0] - tail_position[0]
    dy = head_position[1] - tail_position[1]

    if abs(dx) > 1:
        tail_position[0] = head_position[0] - (1 if dx > 0 else -1)
        tail_position[1] = head_position[1]
    if abs(dy) > 1:
        tail_position[1] = head_position[1] - (1 if dy > 0 else -1)
        tail_position[0] = head_position[0]

    visited.add(tuple(tail_position))


for line in open(sys.argv[1]):
    direction, amount = line.split()
    amount = int(amount)

    if direction == 'R':
        for i in range(amount):
            head_position[0] += 1
            update_tail()
    if direction == 'L':
        for i in range(amount):
            head_position[0] -= 1
            update_tail()
    if direction == 'U':
        for i in range(amount):
            head_position[1] += 1
            update_tail()
    if direction == 'D':
        for i in range(amount):
            head_position[1] -= 1
            update_tail()

print(len(visited))