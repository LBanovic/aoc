import sys
from dataclasses import dataclass, InitVar
from pathlib import Path
from typing import Callable, Tuple, Dict

input_file = Path(sys.argv[1])


@dataclass
class Monkey:
    name: str
    needed_monkeys: Tuple[str, str]
    operation: InitVar[str]

    def __post_init__(self, operation: str):
        self._call = self._parse_op(operation)

    def __call__(self):
        return self._call()

    def _parse_op(self, operation_or_value: str) -> Callable:
        if not self.needed_monkeys:
            return lambda: int(operation_or_value)
        m1, m2 = self.needed_monkeys
        if operation_or_value == '+':
            return lambda: monkeys[m1]() + monkeys[m2]()
        if operation_or_value == '-':
            return lambda: monkeys[m1]() - monkeys[m2]()
        if operation_or_value == '*':
            return lambda: monkeys[m1]() * monkeys[m2]()
        if operation_or_value == '/':
            return lambda: monkeys[m1]() / monkeys[m2]()
        else:
            raise ValueError('Not supported op.')


monkeys: Dict[str, Monkey] = {}
for line in input_file.open():
    name, operation = line.split(':')
    operation = operation.strip()
    op_elements = operation.split(' ')
    if len(op_elements) == 1:
        needed_monkeys = tuple()
    else:
        needed_monkeys = op_elements[0], op_elements[2]
        operation = op_elements[1]
    monkeys[name] = Monkey(name, needed_monkeys, operation)

print(monkeys['root']())