import sys
from collections import deque
from pathlib import Path
from typing import List, Set

input_file = Path(sys.argv[1])

connections = {}
for line in input_file.open():
    start, end = line.strip().split('-')
    connections.setdefault(start, []).append(end)
    connections.setdefault(end, []).append(start)

start_cave = 'start'
end_cave = 'end'


def get_connections(cave: str, visited_small_cave: Set[str]) -> List[str]:
    return [next_cave for next_cave in connections[cave] if
            next_cave not in visited_small_cave]


queue = deque([((start_cave,), set())])
paths = set()
while queue:
    caves, small_caves_visited = queue.popleft()
    if caves[0] == start_cave and caves[-1] == end_cave:
        paths.add(caves)
        continue

    if caves[-1].islower():
        small_caves_visited.add(caves[-1])

    for cave in get_connections(caves[-1], small_caves_visited):
        next_caves = (*caves, cave)
        queue.append((next_caves, small_caves_visited.copy()))

print(len(paths))
