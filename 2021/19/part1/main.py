import itertools
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

s = np.sin
c = np.cos

input_file = Path(sys.argv[1])


def R_x(angle):
    angle = np.deg2rad(angle)
    return np.array([
        [1, 0, 0],
        [0, c(angle), -s(angle)],
        [0, s(angle), c(angle)]
    ])


def R_y(angle):
    angle = np.deg2rad(angle)
    return np.array([
        [c(angle), 0, s(angle)],
        [0, 1, 0],
        [-s(angle), 0, c(angle)]
    ])


def R_z(angle):
    angle = np.deg2rad(angle)
    return np.array([
        [c(angle), -s(angle), 0],
        [s(angle), c(angle), 0],
        [0, 0, 1]
    ])


rotations = []
for a_x, a_y, a_z in itertools.product(range(0, 360, 90), repeat=3):
    R = R_x(a_x) @ R_y(a_y) @ R_z(a_z)
    R = R.astype(int)
    for other_R in rotations:
        if np.all(R == other_R):
            break
    else:
        rotations.append(R)


@dataclass(frozen=True)
class Sensor:
    id: int
    beacons: np.ndarray

    def apply(self, R: np.ndarray) -> 'Sensor':
        beacons = R @ self.beacons.T
        return Sensor(self.id, beacons.T)

    def check_overlap(self, other: 'Sensor'):
        for rotation in rotations:
            target = other.apply(rotation)
            targets = {}
            for beacon in self.beacons:
                x1, y1, z1 = beacon
                for target_beacon in target.beacons:
                    x2, y2, z2 = target_beacon
                    difference = (x1 - x2, y1 - y2, z1 - z2)
                    targets.setdefault(difference, set()).add((tuple(beacon), tuple(target_beacon)))

            for sensor_location, overlapped in targets.items():
                if len(overlapped) == 12:
                    return sensor_location, rotation

    def tuple_beacons(self):
        return tuple(
            tuple(row) for row in self.beacons
        )


def parse_file() -> List[Sensor]:
    sensors = []
    with input_file.open() as infile:
        for line in infile:
            if line.startswith('---'):
                beacons = []
                sensor_id = int(re.findall(r'\d+', line)[0])
                continue
            elif stripped := line.strip():
                beacon = tuple(map(int, stripped.split(',')))
                beacons.append(beacon)
            else:
                beacons = np.array(beacons)
                sensors.append(Sensor(sensor_id, beacons))

    beacons = np.array(beacons)
    sensors.append(Sensor(sensor_id, beacons))

    return sensors


sensors = parse_file()

sensor_locations = {}

for i, sensor1 in enumerate(sensors):
    for j, sensor2 in enumerate(sensors):
        if i != j:
            location = sensor1.check_overlap(sensor2)
            if location:
                sensor_locations[(i, j)] = location

while len(sensor_locations) < len(sensors) ** 2 - len(sensors):
    for i, sensor in enumerate(sensors):
        for j, sensor2 in enumerate(sensors):
            if i != j and (i, j) not in sensor_locations:
                sensors_left = set(end for start, end in sensor_locations.keys() if start == i)
                sensors_right = set(start for start, end in sensor_locations.keys() if end == j)

                intersection = sensors_left & sensors_right
                if intersection:
                    m = intersection.pop()
                    L1, R1 = sensor_locations[i, m]
                    L2, R2 = sensor_locations[m, j]
                    l_relative = tuple(R1 @ L2 + L1)
                    sensor_locations[i, j] = (l_relative, R1 @ R2)

clean_dict = {key: value for key, value in sensor_locations.items() if key[0] == 0}

seen_beacons = set()

for sensor in sensors:
    if sensor.id == 0:
        seen_beacons.update(sensor.tuple_beacons())
    else:
        L, R = sensor_locations[0, sensor.id]
        new_beacons = R @ sensor.beacons.T
        new_beacons = new_beacons.T + L
        target = Sensor(sensor.id, new_beacons)
        seen_beacons.update(target.tuple_beacons())

print(len(seen_beacons))