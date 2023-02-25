import sys


class State:

    def __init__(self, position, height, cost):
        self.position = position
        self.height = height
        self.cost = cost

    def get_next_states(self, map_matrix):
        new_positions = [
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.position[1]),
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1)
        ]

        map_h, map_w = len(map_matrix), len(map_matrix[0])

        for new_position in new_positions:
            x, y = new_position
            if 0 <= x < map_w and 0 <= y < map_h:
                new_height = map_matrix[y][x]
                if new_height != 'A':
                    if abs(ord(new_height) - ord(self.height)) <= 1:
                        yield State(new_position, new_height, self.cost + 1)

    def __repr__(self):
        return f'{self.position} {self.height}'

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return self.position == other.position


def blind_alg(start_state, end_state, map_matrix, expand_func):
    start_state = State(start_state, 'a', 0)
    states = [start_state]

    while states:
        current_state = states.pop(0)
        x, y = current_state.position
        map_matrix[y][x] = 'A'
        if current_state.position == end_state:
            return current_state
        expand_func(states, map_matrix, current_state)
    return None


def bfs(start_state, end_state, map_matrix):
    def expand(states, map_matrix, current_state):
        for next_state in current_state.get_next_states(map_matrix):
            states.append(next_state)

    return blind_alg(start_state, end_state, map_matrix, expand)


def dfs(start_state, end_state, map_matrix):
    def expand(states, visited_states, current_state):
        for next_state in current_state.get_next_states(map_matrix):
            if next_state not in visited_states:
                states.insert(0, next_state)

    return blind_alg(start_state, end_state, map_matrix, expand)


def depth_dfs(start_state, end_state, map_matrix, max_depth):
    def expand(states, visited_states, current_state):
        if current_state < max_depth:
            for next_state in current_state.get_next_states(map_matrix):
                if next_state not in visited_states:
                    states.insert(0, next_state)

    return blind_alg(start_state, end_state, map_matrix, expand)


def filter_condition(p_vertex, current_vertex, unvisited, w, h):
    x2, y2 = p_vertex
    x, y = current_vertex
    valid_vertex = (x2, y2) in unvisited and 0 <= x2 < w and 0 <= y2 < h

    if valid_vertex:
        new_elevation = ord(map_matrix[y2][x2])
        old_elevation = ord(map_matrix[y][x])
        can_cross = valid_vertex and new_elevation - old_elevation <= 1
    else:
        can_cross = False
    return can_cross


def dijkstra(start_state, end_state, map_matrix):
    vertices = []
    h, w = len(map_matrix), len(map_matrix[0])
    for y in range(h):
        for x in range(w):
            vertices.append((x, y))

    unvisited = set(vertices)
    print(len(unvisited))
    distances = {vertex: 0 if vertex == start_state else 2 ** 32 - 1 for vertex in vertices}

    current_vertex = start_state

    while True:
        if current_vertex == end_state:
            return distances[current_vertex]

        x, y = current_vertex
        possible_vertices = (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

        valid_possible_vertices = list(filter(lambda p: filter_condition(p, current_vertex,
                                                                         unvisited, w, h), possible_vertices))

        for p_vertex in valid_possible_vertices:
            distances[p_vertex] = min(distances[current_vertex] + 1, distances[p_vertex])

        unvisited.remove(current_vertex)
        current_vertex = min(filter(lambda x: x in unvisited, distances), key=lambda x: distances[x])



map_matrix = []
for y, line in enumerate(open(sys.argv[1])):
    start_x = line.find('S')
    if start_x >= 0:
        line = line.replace('S', 'a')
        start_state = (start_x, y)

    end_x = line.find('E')
    if end_x >= 0:
        line = line.replace('E', 'z')
        end_state = (end_x, y)

    map_matrix.append(list(line.strip()))

distance = bfs(start_state, end_state, map_matrix)
print(distance)
