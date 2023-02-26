import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

input_file = Path(sys.argv[1])


@dataclass
class Board:
    numbers: List[List[int]]

    def __post_init__(self):
        self.hit: List[List[bool]] = [
            [False for _ in row] for row in self.numbers
        ]
        self.board_sum = sum(sum(num) for num in self.numbers)

    def is_win(self) -> bool:
        dim = len(self.hit)
        for i in range(dim):
            if sum(self.hit[i]) == dim:
                return True
            elif sum(row[i] for row in self.hit) == dim:
                return True
        return False

    def sum_unmarked(self) -> int:
        return self.board_sum

    def mark_num(self, target: int) -> None:
        for j, row in enumerate(self.numbers):
            for i, number in enumerate(row):
                if number == target:
                    self.hit[j][i] = True
                    self.board_sum -= number
                    return


boards = []
numbers = []
for i, line in enumerate(input_file.open()):
    if i == 0:
        rng = map(int, line.strip().split(','))
    elif i % 6 == 1:
        if numbers:
            board = Board(numbers)
            boards.append(board)
            numbers = []
    else:
        numbers.append(list(map(int, line.strip().split())))

boards.append(Board(numbers))


def process_num(num):
    for board in boards:
        board.mark_num(num)
    for board in boards:
        if board.is_win():
            if len(boards) > 1:
                boards.remove(board)
            else:
                print(num)
                print(board.sum_unmarked())
                return board.sum_unmarked() * num


for num in rng:
    res = process_num(num)
    if res:
        break
print(res)
