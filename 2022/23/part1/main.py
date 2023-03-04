import sys
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple, List, Callable

from tqdm import tqdm

input_file = Path(sys.argv[1])


class Direction(Enum):
    North = (0, -1)
    NorthWest = (-1, -1)
    NorthEast = (1, -1)
    South = (0, 1)
    SouthWest = (-1, 1)
    SouthEast = (1, 1)
    West = (-1, 0)
    East = (1, 0)

    @classmethod
    def all(cls) -> Tuple['Direction']:
        return tuple(Direction)

    def __repr__(self):
        return self.name


@dataclass
class DirectionChecker:
    directions: Tuple
    operation: Callable

    def check_direction(self, elf: 'Elf'):
        doesnt_exist_around = all(self._check_not_exists_in_direction(elf, direction) for direction in self.directions)
        if doesnt_exist_around:
            return self.operation(elf)
        return None

    @staticmethod
    def _check_not_exists_in_direction(elf, direction: Direction) -> bool:
        dx, dy = direction.value
        next_position = (elf.left + dx, elf.right + dy)
        for elf_ in elves:
            if (elf_.x, elf_.y) == next_position:
                return False
        return True

    @classmethod
    def all(cls):
        return cls(tuple(Direction), operation=lambda elf: (elf.left, elf.right))


@dataclass
class Elf:
    x: int
    y: int

    def propose_move(self, checkers: List[DirectionChecker]) -> Tuple[int, int]:
        around = DirectionChecker.all().check_direction(self)
        if around:
            return around

        for checker in checkers:
            new_pos = checker.check_direction(self)
            if new_pos:
                return new_pos

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


elves = []
for y, line in enumerate(input_file.open()):
    for x, ch in enumerate(line):
        if ch == '#':
            elves.append(Elf(x, y))


def print_elves():
    start_x, end_x = min(elf.x for elf in elves), max(elf.x for elf in elves) + 1
    start_y, end_y = min(elf.y for elf in elves), max(elf.y for elf in elves) + 1
    print(f'W: {end_x - start_x} H: {end_y - start_y}')
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            for elf in elves:
                if (elf.x, elf.y) == (x, y):
                    print('#', end='')
                    break
            else:
                print('.', end='')
        print()
    print()


checkers = [
    DirectionChecker(
        directions=(Direction.North, Direction.NorthEast, Direction.NorthWest),
        operation=lambda elf: (elf.left, elf.right - 1)
    ),
    DirectionChecker(
        directions=(Direction.South, Direction.SouthEast, Direction.SouthWest),
        operation=lambda elf: (elf.left, elf.right + 1)
    ),
    DirectionChecker(
        directions=(Direction.West, Direction.SouthWest, Direction.NorthWest),
        operation=lambda elf: (elf.left - 1, elf.right)
    ),
    DirectionChecker(
        directions=(Direction.East, Direction.SouthEast, Direction.NorthEast),
        operation=lambda elf: (elf.left + 1, elf.right)
    )
]

N_STEPS = 10
for i in tqdm(range(N_STEPS)):
    move_checker = Counter()
    proposed = []
    for elf in elves:
        move = elf.propose_move(checkers)
        move_checker[move] += 1
        proposed.append(move)

    valid_moves = set(move for move, count in move_checker.items() if count == 1)
    for elf, move in zip(elves, proposed):
        if move in valid_moves:
            x, y = elf.x, elf.y
            elf.move(*move)
    checkers = checkers[1:] + checkers[:1]

start_x, end_x = min(elf.x for elf in elves), max(elf.x for elf in elves) + 1
start_y, end_y = min(elf.y for elf in elves), max(elf.y for elf in elves) + 1
print((end_x - start_x) * (end_y - start_y) - len(elves))
