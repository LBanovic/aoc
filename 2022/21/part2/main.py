import sys
from dataclasses import dataclass, InitVar
from pathlib import Path
from typing import Callable, Tuple, Dict

input_file = Path(sys.argv[1])


class Monkey:
    def __init__(self, name: str, needed_monkeys: Tuple[str, str], operation: str):
        self.name = name
        self.needed_monkeys = needed_monkeys
        self.operation = operation
        self._call = self._parse_op(operation)
        self.starting_monkey = None

    def __call__(self):
        return self._call()

    def _parse_op(self, operation_or_value: str) -> Callable:
        if not self.needed_monkeys:
            return lambda: int(operation_or_value)
        m1, m2 = self.needed_monkeys
        if self.name == 'root':
            return lambda: monkeys[m1]() == monkeys[m2]()
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


class Human(Monkey):
    def __init__(self, name: str, needed_monkeys: Tuple[str, str], operation: str):
        super().__init__(name, needed_monkeys, operation)
        self.end_result = None
        self.yell = None

    def __call__(self):
        if not self.yell:
            raise ValueError('I dont know yet')
        return self.yell

    def figure_out_end_result(self):
        m1, m2 = monkeys['root'].needed_monkeys
        try:
            x = monkeys[m1]()
            self.starting_monkey = m2
        except ValueError:
            x = monkeys[m2]()
            self.starting_monkey = m1
        self.end_result = x

    def traverse_backwards_from_root(self):
        current_value = self.end_result
        current_monkey = self.starting_monkey
        while True:
            if current_monkey == 'humn':
                self.yell = current_value
                break
            m1, m2 = monkeys[current_monkey].needed_monkeys
            try:
                value = monkeys[m1]()
                current_value = invert_op_for_first_arg(current_value, value, monkeys[current_monkey].operation)
                current_monkey = m2
            except ValueError:
                value = monkeys[m2]()
                current_value = invert_op_for_second_arg(current_value, value, monkeys[current_monkey].operation)
                current_monkey = m1


def invert_op_for_first_arg(result: float, first_arg: float, operation: str) -> float:
    if operation == '+':
        return result - first_arg
    if operation == '-':
        return first_arg - result
    if operation == '*':
        return result / first_arg
    if operation == '/':
        return first_arg / result


def invert_op_for_second_arg(result: float, second_arg: float, operation: str) -> float:
    if operation == '+':
        return result - second_arg
    if operation == '-':
        return second_arg + result
    if operation == '*':
        return result / second_arg
    if operation == '/':
        return second_arg * result


monkeys = {}
for line in input_file.open():
    name, operation = line.split(':')
    operation = operation.strip()
    op_elements = operation.split(' ')
    if len(op_elements) == 1:
        needed_monkeys = tuple()
    else:
        needed_monkeys = op_elements[0], op_elements[2]
        operation = op_elements[1]
    if name == 'humn':
        monkeys[name] = Human(name, needed_monkeys, operation)
    else:
        monkeys[name] = Monkey(name, needed_monkeys, operation)

human = monkeys['humn']
human.figure_out_end_result()
human.traverse_backwards_from_root()
print(human.yell)