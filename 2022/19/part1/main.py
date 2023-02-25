import math
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Dict, Generator

input_file = Path(sys.argv[1])


class Robot(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


class Resource(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


@dataclass(frozen=True)
class Blueprint:
    id: int
    costs: Tuple[Tuple[int]]
    max_spend: Tuple[int]

    resources: Tuple[int] = (0, 0, 0, 0)
    robots: Tuple[int] = (1, 0, 0, 0)

    def gather_resources(self, step=1) -> Tuple[int]:
        return tuple(res + rob * step for res, rob in zip(self.resources, self.robots))

    def make_robot(self, robot: Robot) -> Tuple[int]:
        robots = tuple(robot_ + int(i == robot.value) for i, robot_ in enumerate(self.robots))
        return robots

    def can_skip_robot(self, robot: Robot) -> bool:
        if robot == Robot.geode:
            return False

        if self.robots[robot.value] >= self.max_spend[robot.value]:
            return True

        return False

    def get_resource(self, resource: Resource) -> int:
        return self.resources[resource.value]

    def get_robot(self, robot: Robot) -> int:
        return self.robots[robot.value]

    def get_cost_for_robot(self, robot: Robot) -> Generator:
        for i, cost in enumerate(self.costs[robot.value]):
            if cost != 0:
                yield Resource(i), cost


def get_resource_cost_for_robot(costs: Tuple[Tuple[int]], robot: Robot, resource: Resource) -> int:
    return costs[robot.value][resource.value]


TOTAL_MINUTES = 24


def parse_input() -> List[Blueprint]:
    number_regex = re.compile(r'\d+')
    resources_paid = [('ore',), ('ore',), ('ore', 'clay'), ('ore', 'obsidian')]
    number_indices = [(1, 2), (2, 3), (3, 5), (5, 7)]
    blueprints = []
    with input_file.open() as blueprint_file:
        for line in blueprint_file:
            line_numbers = list(map(int, number_regex.findall(line)))
            id = line_numbers[0]

            robot_costs = []

            for robot, resources, (start, end) in zip(Robot, resources_paid, number_indices):
                value_list = [0] * 4
                for resource, value in zip(resources, line_numbers[start:end]):
                    value_list[Resource[resource].value] = value
                robot_costs.append(tuple(value_list))
            robot_costs = tuple(robot_costs)

            max_spend_resource = [0] * 4

            for resource in Resource:
                resource_cost_for_robot = [get_resource_cost_for_robot(robot_costs, robot, resource) for robot in Robot]
                max_spend_resource[resource.value] = max(resource_cost_for_robot)

            max_spend_resource = tuple(max_spend_resource)
            blueprints.append(Blueprint(id, robot_costs, max_spend_resource))
    return blueprints


def dfs(blueprint: Blueprint, time: int, cache: Dict) -> int:
    if time == 0:
        return blueprint.get_resource(Resource.geode)

    key = (blueprint, time)
    if key in cache:
        return cache[key]
    # do nothing or build robot

    # do nothing
    highest_value = blueprint.get_resource(Resource.geode) + blueprint.get_robot(Robot.geode) * time
    for robot in Robot:
        if blueprint.can_skip_robot(robot):  # if we already have more than we can spend, don't make more robots
            continue

        wait = 0
        for resource, amount in blueprint.get_cost_for_robot(robot):
            n_robots = blueprint.robots[resource.value]
            n_resource = blueprint.resources[resource.value]
            if n_robots == 0:
                break
            wait = max(wait, math.ceil((amount - n_resource) / n_robots))
        else:
            remaining_time = time - wait - 1
            if remaining_time <= 0:
                continue
            new_resources = blueprint.gather_resources(step=wait + 1)
            robot_costs = blueprint.costs[robot.value]
            robots = blueprint.make_robot(robot)
            paid_resources = tuple(r - int(val <= r) * val for r, val in zip(new_resources, robot_costs))
            clipped_resources = tuple((min(r, max_spend * remaining_time) if i < 3 else r) for i, (r, max_spend)
                                      in enumerate(zip(paid_resources, blueprint.max_spend)))

            new_blueprint = Blueprint(blueprint.id, blueprint.costs, blueprint.max_spend,
                                      resources=clipped_resources, robots=robots)

            highest_value = max(highest_value, dfs(new_blueprint, remaining_time, cache))

    cache[key] = highest_value
    return highest_value


blueprints = parse_input()

total = 0
for blueprint in blueprints:
    cache = {}
    max_geode = dfs(blueprint, TOTAL_MINUTES, cache)
    total += blueprint.id * max_geode

print(total)
