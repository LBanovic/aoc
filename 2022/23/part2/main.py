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
        return elf.neighbours[direction] is None

    @classmethod
    def all(cls):
        return cls(tuple(Direction), operation=lambda elf: (elf.x, elf.y))


@dataclass
class Elf:
    x: int
    y: int

    def check_for_neighbours(self):
        self.neighbours = {}
        for direction in Direction:
            elf_key = (self.x + direction.value[0], self.y + direction.value[1])
            self.neighbours[direction] = elves.get(elf_key, None)

    def propose_move(self, checkers: List[DirectionChecker]) -> Tuple[int, int]:
        around = DirectionChecker.all().check_direction(self)
        if around:
            return around

        for checker in checkers:
            new_pos = checker.check_direction(self)
            if new_pos:
                return new_pos
        return self.x, self.y

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


elves = {}
for y, line in enumerate(input_file.open()):
    for x, ch in enumerate(line):
        if ch == '#':
            elves[x, y] = Elf(x, y)

checkers = [
    DirectionChecker(
        directions=(Direction.North, Direction.NorthEast, Direction.NorthWest),
        operation=lambda elf: (elf.x, elf.y - 1)
    ),
    DirectionChecker(
        directions=(Direction.South, Direction.SouthEast, Direction.SouthWest),
        operation=lambda elf: (elf.x, elf.y + 1)
    ),
    DirectionChecker(
        directions=(Direction.West, Direction.SouthWest, Direction.NorthWest),
        operation=lambda elf: (elf.x - 1, elf.y)
    ),
    DirectionChecker(
        directions=(Direction.East, Direction.SouthEast, Direction.NorthEast),
        operation=lambda elf: (elf.x + 1, elf.y)
    )
]

i = 1
while True:
    move_counter = 0
    move_checker = Counter()
    for elf in elves.values():
        elf.check_for_neighbours()

    proposed = []
    for elf in elves.values():
        move = elf.propose_move(checkers)
        move_checker[move] += 1
        proposed.append(move)

    valid_moves = set(move for move, count in move_checker.items() if count == 1)
    for elf, move in zip(elves.values(), proposed):
        if move in valid_moves and move != (elf.x, elf.y):
            x, y = elf.x, elf.y
            elf.move(*move)
            move_counter += 1
    checkers = checkers[1:] + checkers[:1]
    if move_counter == 0:
        break
    i += 1
    elves = {(elf.x, elf.y): elf for elf in elves.values()}

print(i)
