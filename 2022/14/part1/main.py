import sys

rock_lines = []
for line in open(sys.argv[1]):
    endpoints = line.strip().split('->')
    endpoints = [list(map(int, p.strip().split(','))) for p in endpoints if p.strip()]
    single_rock = []
    for start_point, end_point in zip(endpoints, endpoints[1:]):
        start_point, end_point = min(start_point, end_point), max(start_point, end_point)
        single_rock.append((start_point, end_point))

    rock_lines.append(single_rock)

filled = set()
for rock_line in rock_lines:
    for start_point, end_point in rock_line:
        x1, y1 = start_point
        x2, y2 = end_point
        dx = x2 - x1
        dy = y2 - y1

        for i in range(dx + 1):
            for j in range(dy + 1):
                filled.add((x1 + i, y1 + j))

sand_start_point = (500, 0)
abyss_height = max(p[1] for p in filled)

n_sand = 0
while True:
    sand_point = sand_start_point
    while True:
        x, y = sand_point
        new_points = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
        for p in new_points:
            if p not in filled:
                sand_point = p
                break
        if (x, y) == sand_point or y >= abyss_height:
            break
    if sand_point[1] >= abyss_height:
        break
    filled.add(sand_point)
    n_sand += 1

print(n_sand)