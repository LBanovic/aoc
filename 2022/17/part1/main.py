import sys
from pathlib import Path
from typing import List, Tuple

from tqdm import tqdm

filename = Path(sys.argv[1])
MAX_ITERATIONS = 2022
WIDTH = 7
N_BLOCKS = 5

BLOCK_POSITIONS = set()

with filename.open() as infile:
    operations = infile.readlines()[0]

current_operation_index = 0


class Rock:

    def __init__(self, block_positions: List[Tuple[int, int]],
                 start_x: int, start_y: int):
        self.block_positions = [(x + start_x, y + start_y) for (x, y) in block_positions]

    def move_right(self) -> bool:
        # TODO check for collision between rocks
        new_positions = [(x + 1, y) for (x, y) in self.block_positions]
        return update_block(self, new_positions)

    def move_left(self) -> bool:
        # TODO check for collision between rocks
        new_positions = [(x - 1, y) for (x, y) in self.block_positions]
        return update_block(self, new_positions)

    def move_down(self) -> bool:
        new_position = [(x, y - 1) for (x, y) in self.block_positions]
        return update_block(self, new_position)

    def __repr__(self):
        return repr(self.block_positions)

    @staticmethod
    def spawn_minus(x: int, y: int) -> 'Rock':
        block_positions = [(0, 0), (1, 0), (2, 0), (3, 0)]
        return Rock(block_positions, x, y)

    @staticmethod
    def spawn_plus(x: int, y: int) -> 'Rock':
        block_position = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        return Rock(block_position, x, y)

    @staticmethod
    def spawn_L(x: int, y: int) -> 'Rock':
        block_position = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        return Rock(block_position, x, y)

    @staticmethod
    def spawn_I(x: int, y: int) -> 'Rock':
        block_position = [(0, 0), (0, 1), (0, 2), (0, 3)]
        return Rock(block_position, x, y)

    @staticmethod
    def spawn_square(x: int, y: int) -> 'Rock':
        block_position = [(0, 0), (0, 1), (1, 0), (1, 1)]
        return Rock(block_position, x, y)


def update_block(block: Rock, new_positions: List[Tuple[int, int]]) -> bool:
    valid = _check_position_valid(new_positions)
    if valid:
        block.block_positions = new_positions
    return valid


def _check_position_valid(block_position: List[Tuple[int, int]]) -> bool:
    for x, y in block_position:
        if not (0 <= x <= WIDTH - 1):
            return False
        if y < 0:
            return False

    if set(block_position) & BLOCK_POSITIONS:
        return False

    return True


def get_max_height() -> int:
    if BLOCK_POSITIONS:
        return max(y for _, y in BLOCK_POSITIONS) + 1
    return 0


for i in tqdm(range(MAX_ITERATIONS)):
    x = 2
    y = get_max_height() + 3

    if i % N_BLOCKS == 0:
        rock = Rock.spawn_minus(x, y)
    elif i % N_BLOCKS == 1:
        rock = Rock.spawn_plus(x, y)
    elif i % N_BLOCKS == 2:
        rock = Rock.spawn_L(x, y)
    elif i % N_BLOCKS == 3:
        rock = Rock.spawn_I(x, y)
    else:
        rock = Rock.spawn_square(x, y)

    while True:
        jet = operations[current_operation_index]
        current_operation_index += 1
        current_operation_index %= len(operations)
        if jet == '>':
            rock.move_right()
        else:
            rock.move_left()
        if not rock.move_down():
            break
    BLOCK_POSITIONS.update(rock.block_positions)

print(get_max_height())
