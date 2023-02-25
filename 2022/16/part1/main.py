import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, FrozenSet

input_file = Path(sys.argv[1])
TOTAL_MINUTES = 30

valves_by_name = {}


@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    leads_to: Tuple[str]

    def __repr__(self) -> str:
        return f'{self.name}' \
            # f', {self.flow_rate} -> {", ".join(self.leads_to)}'


def get_valve_by_name(valves: List[Valve], name: str) -> Valve:
    for valve in valves:
        if valve.name == name:
            return valve


re_upper_letter = re.compile(r'[A-Z]{2}')
re_flow_rate = re.compile(r'\d+')

valves = []

with input_file.open('r') as f:
    for line in f:
        all_valves = re_upper_letter.findall(line)
        flow_rate = int(re_flow_rate.findall(line)[0])
        curr_valve = all_valves[0]
        leads_to = tuple(all_valves[1:])
        valves.append(Valve(curr_valve, flow_rate, leads_to))

starting_valve = get_valve_by_name(valves, 'AA')

# BFS - ignore nodes with 0 flow_rate
distances = {}
for valve in valves:
    if valve != starting_valve and valve.flow_rate == 0:
        continue
    distances[valve] = {}
    visited = {valve}
    queue = deque([(0, valve)])
    while queue:
        distance, new_valve = queue.popleft()
        for neighbor_name in new_valve.leads_to:
            neighbor = get_valve_by_name(valves, neighbor_name)
            if neighbor in visited:
                continue
            visited.add(neighbor)
            if neighbor.flow_rate > 0:
                distances[valve][neighbor] = distance + 1
            queue.append((distance + 1, neighbor))


# dfs over compressed graph
def dfs(time: int, valve: Valve, open_valves: FrozenSet):
    maxval = 0
    for neighbor in distances[valve]:
        if neighbor in open_valves:
            continue
        remaining_time = time - distances[valve][neighbor] - 1
        if remaining_time <= 0:
            continue
        maxval = max(maxval, dfs(remaining_time, neighbor,
                                 open_valves.copy() | {neighbor}) + neighbor.flow_rate * remaining_time)

    return maxval


print(dfs(TOTAL_MINUTES, starting_valve, frozenset()))
