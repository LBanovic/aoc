import sys
from dataclasses import dataclass

MIN = 0
MAX = 4000000
X_MULTIPLIER = 4000000

input_file = sys.argv[1]

sensors = []


@dataclass
class Sensor:
    x: int
    y: int
    r: int = None

    def distance_from(self, other: 'Sensor') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def set_radius(self, beacon: 'Sensor'):
        self.r = self.distance_from(beacon)

    def __eq__(self, o: 'Sensor') -> bool:
        return self.x == o.x and self.y == o.y


def parse_loc(string):
    sx_loc = string.find('x=') + 2, string.find(',')
    sy_loc = string.find('y=') + 2

    sx, sy = int(string[sx_loc[0]:sx_loc[1]]), int(string[sy_loc:])
    return Sensor(sx, sy)


for line in open(input_file):
    data = line.strip().split(':')
    sensor = parse_loc(data[0])
    beacon = parse_loc(data[1])
    sensor.set_radius(beacon)
    sensors.append(sensor)

candidates = []


def check_distance(s1, s2):
    return s1.r + s2.r + 1 <= s1.distance_from(s2) <= s1.r + s2.r + 2


def are_intersecting(s1, s2):
    return s1.distance_from(s2) < s1.r + s2.r


def find_slope_and_intercept_of_edge(edge):
    p1, p2 = edge
    x1, y1 = p1
    x2, y2 = p2

    slope = (y2 - y1) // (x2 - x1)
    intercept = y1 - slope * x1
    return slope, intercept


for i, s1 in enumerate(sensors):
    for j, s2 in enumerate(sensors[i + 1:]):
        if check_distance(s1, s2):
            candidates.append((s1, s2))

for i, candidate in enumerate(candidates):
    s1, s2 = candidate
    for candidate in candidates[i + 1:]:
        s3, s4 = candidate
        if s1 in (s3, s4) or s2 in (s3, s4):
            continue
        if are_intersecting(s1, s3) and are_intersecting(s2, s4) and are_intersecting(s1, s4) and are_intersecting(s2,
                                                                                                                   s3):
            # found sensors that have a one 1x1 cell gap between them
            sensors = s1, s2, s3, s4
            break

# now we act like sensors are squares rotated by 90°
# visual: https://www.desmos.com/calculator/xa9ei93g9n
# the goal is to find the integer coordinates of the gap
# here, it is modeled as a problem of finding line intersections

top_left_point = Sensor(MIN, MAX)
top_right_point = Sensor(MAX, MAX)
bottom_left_point = Sensor(MIN, MIN)
bottom_right_point = Sensor(MAX, MIN)

top_left_sensor = min(sensors, key=lambda sensor: sensor.distance_from(top_left_point))
top_right_sensor = min(sensors, key=lambda sensor: sensor.distance_from(top_right_point))

top_left_sensor_bottom_right_edge = ((top_left_sensor.x + top_left_sensor.r, top_left_sensor.y),
                                     (top_left_sensor.x, top_left_sensor.y - top_left_sensor.r))
line1 = find_slope_and_intercept_of_edge(top_left_sensor_bottom_right_edge)

top_right_sensor_bottom_left_edge = ((top_right_sensor.x - top_right_sensor.r, top_right_sensor.y),
                                     (top_right_sensor.x, top_right_sensor.y - top_right_sensor.r))
line2 = find_slope_and_intercept_of_edge(top_right_sensor_bottom_left_edge)

# line1: a1*x + b1
# line2: a2*x + b2
# we need to pull line1 down by 1 to get it out of the top left square, so subtract 1
# analogous for line2

a1, b1 = line1
b1 -= 1

a2, b2 = line2
b2 -= 1

# a1*x + b1 = a2*x + b2
# x = (b2 - b1) / (a1 - a2)

target_x = (b2 - b1) // (a1 - a2)
target_y = a1 * target_x + b1

import ipdb; ipdb.set_trace()

print(a1, b1, a2, b2)
print(target_x, target_y)
print(target_x * X_MULTIPLIER + target_y)
