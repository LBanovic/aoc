import sys

positions = [list((0, 0)) for _ in range(10)]

visited = {tuple(positions[-1])}


def update_rest():
    for head_position, tail_position in zip(positions, positions[1:]):
        dx = head_position[0] - tail_position[0]
        dy = head_position[1] - tail_position[1]

        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1

        if abs(dx) > 1 and dy == 0:
            tail_position[0] = tail_position[0] + sx
        elif abs(dy) > 1 and dx == 0:
            tail_position[1] = tail_position[1] + sy
        elif abs(dx) > 1 or abs(dy) > 1:
            tail_position[0] += sx
            tail_position[1] += sy

    visited.add(tuple(positions[-1]))


for line in open(sys.argv[1]):
    direction, amount = line.split()
    amount = int(amount)

    if direction == 'R':
        for i in range(amount):
            positions[0][0] += 1
            update_rest()
    if direction == 'L':
        for i in range(amount):
            positions[0][0] -= 1
            update_rest()
    if direction == 'U':
        for i in range(amount):
            positions[0][1] += 1
            update_rest()
    if direction == 'D':
        for i in range(amount):
            positions[0][1] -= 1
            update_rest()

print(len(visited))
