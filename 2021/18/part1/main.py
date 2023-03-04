import sys
from pathlib import Path
from typing import Union, List, Optional

input_file = Path(sys.argv[1])


class SnailfishNumber:

    def __init__(self, x: 'SnailfishNumber' = None, y: 'SnailfishNumber' = None, value: int = None,
                 parent: 'SnailfishNumber' = None):
        self.left = x
        self.right = y
        self.value = value
        self.parent = parent

    @classmethod
    def from_list(cls, numbers: List[Union[List, int]], parent=None) -> 'SnailfishNumber':
        number = SnailfishNumber()
        number.parent = parent
        x, y = numbers[0], numbers[1]
        if isinstance(x, List):
            number.left = SnailfishNumber.from_list(x, parent=number)
        else:
            number.left = SnailfishNumber(value=x, parent=number)
        if isinstance(y, List):
            number.right = SnailfishNumber.from_list(y, parent=number)
        else:
            number.right = SnailfishNumber(value=y, parent=number)
        return number

    def __add__(self, other: 'SnailfishNumber') -> 'SnailfishNumber':
        number = SnailfishNumber(self, other)
        self.parent = number
        other.parent = number
        number.reduce()
        return number

    def is_regular(self):
        return self.value is not None

    @property
    def magnitude(self):
        if self.is_regular():
            return self.value
        else:
            return self.left.magnitude * 3 + self.right.magnitude * 2

    def reduce(self):
        while True:
            exploded = self.explode()
            if exploded:
                continue
            split = self.split()
            if not (split or exploded):
                break

    def explode(self, depth: int = 0) -> bool:
        if self.is_regular():
            return False

        if depth == 4:
            left_val = self.left.value
            right_val = self.right.value

            left_root = self._find_left_root()
            if left_root is not None:
                left_root._add_rightmost(left_val)

            right_root = self._find_right_root()
            if right_root is not None:
                right_root._add_leftmost(right_val)

            self.left = None
            self.right = None
            self.value = 0

            return True

        return bool(self.left.explode(depth + 1)) or bool(self.right.explode(depth + 1))

    def _find_left_root(self) -> Optional['SnailfishNumber']:
        if self.parent is None:
            return None
        if self.parent.left is self:
            return self.parent._find_left_root()
        return self.parent.left

    def _add_rightmost(self, value: int):
        if self.is_regular():
            self.value += value
        else:
            self.right._add_rightmost(value)

    def _find_right_root(self) -> Optional['SnailfishNumber']:
        if self.parent is None:
            return None
        if self.parent.right is self:
            return self.parent._find_right_root()
        return self.parent.right

    def _add_leftmost(self, value: int):
        if self.is_regular():
            self.value += value
        else:
            self.left._add_leftmost(value)

    def split(self) -> bool:
        if self.is_regular():
            if self.value >= 10:
                left = self.value // 2
                right = self.value - left
                self.value = None
                self.left = SnailfishNumber(value=left, parent=self)
                self.right = SnailfishNumber(value=right, parent=self)
                return True
            else:
                return False
        else:
            return bool(self.left.split()) or bool(self.right.split())

    def __repr__(self):
        if self.is_regular():
            return f'{self.value}'
        else:
            return f'[{self.left},{self.right}]'


numbers = []
for line in input_file.open():
    numbers.append(SnailfishNumber.from_list(eval(line.strip())))

total = None
for number in numbers:
    if total is None:
        total = number
    else:
        total = total + number

print(total.magnitude)