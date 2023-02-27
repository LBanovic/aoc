import sys
from pathlib import Path
from typing import FrozenSet, Dict, List, Callable

input_file = Path(sys.argv[1])
valid_lens = (2, 3, 4, 7)
len_digits = (1, 7, 4, 8)
count = 0


def get_digit_for_val(mapping: Dict[FrozenSet, int], t: int) -> FrozenSet:
    return [mapping for mapping, val in mapping.items() if val == t][0]


def find_key_for_condition(digits: List[FrozenSet], *conditions: Callable) -> FrozenSet:
    keys = [digit for digit in digits if all(condition(digit) for condition in conditions)]
    assert len(keys) == 1
    return keys[0]


def condition_len(target: int) -> Callable:
    return lambda digit: len(digit) == target


def condition_subset(value: int, reverse=False) -> Callable:
    target = get_digit_for_val(mapping, value)
    return lambda digit: digit.issubset(target) if not reverse else target.issubset(digit)


def condition_is_not_equal(*vals):
    vals = [get_digit_for_val(mapping, val) for val in vals]
    return lambda digit: digit not in vals


outputs = []
for line in input_file.open():
    digits = line.strip().split('|')[0]
    target = line.strip().split('|')[1]
    mapping = {}
    digits = list(frozenset(digit) for digit in digits.strip().split())
    for digit in digits:
        if len(digit) in valid_lens:
            mapping[digit] = len_digits[valid_lens.index(len(digit))]

    key = find_key_for_condition(digits, condition_subset(4, reverse=True), condition_len(6))
    mapping[key] = 9

    key = find_key_for_condition(digits, condition_len(6), condition_subset(1, reverse=True), condition_is_not_equal(9))
    mapping[key] = 0

    key = find_key_for_condition(digits, condition_len(6), condition_is_not_equal(0, 9))
    mapping[key] = 6

    key = find_key_for_condition(digits, condition_len(5), condition_subset(1, reverse=True))
    mapping[key] = 3

    key = find_key_for_condition(digits, condition_len(5),condition_subset(6))
    mapping[key] = 5

    key = find_key_for_condition(digits, condition_len(5), condition_is_not_equal(5, 3))
    mapping[key] = 2

    target_str = ''
    for t in target.strip().split():
        target_str += str(mapping[frozenset(t)])
    outputs.append(int(target_str))

print(sum(outputs))
