import sys

input_file = sys.argv[1]

y_target = 10 if 'test' in input_file else 2_000_000

sensors = []
beacons = set()


def parse_loc(string):
    sx_loc = string.find('x=') + 2, string.find(',')
    sy_loc = string.find('y=') + 2

    sx, sy = int(string[sx_loc[0]:sx_loc[1]]), int(string[sy_loc:])
    return sx, sy


for line in open(input_file):
    data = line.strip().split(':')
    sensor_data = parse_loc(data[0])
    beacon_data = parse_loc(data[1])
    if beacon_data[1] == y_target:
        beacons.add(beacon_data)
    distance = abs(beacon_data[0] - sensor_data[0]) + abs(beacon_data[1] - sensor_data[1])
    sensors.append((sensor_data, distance))

# distance <= |x_sensor - x_target| + |y_sensor - y_target|
# distance - |y_sensor - y_target| <= |x_sensor - x_target|
# |x_sensor - x_target| => distance - |y_sensor - y_target|
# distance - |y_sensor - y_target| => x_target - x_sensor => -distance + |y_sensor - y_target|
# distance - |y_sensor - y_target| + x_sensor => x_target => -distance + |y_sensor - y_target| + x_sensor

xs = set()


def cannot_contain_for_sensor(sensor, y_target):
    (x_sensor, y_sensor), distance = sensor
    top_limit = distance - abs(y_sensor - y_target) + x_sensor
    bottom_limit = -distance + abs(y_sensor - y_target) + x_sensor
    return range(bottom_limit, top_limit)


for sensor in sensors:
    xs.update(cannot_contain_for_sensor(sensor, y_target))

# xs -= len(beacons)
print(len(xs))
