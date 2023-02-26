import sys
from pathlib import Path
from typing import List, Callable

input_file = Path(sys.argv[1])
input_numbers = [list(map(int, line.strip())) for line in input_file.open()]


def find_extreme_at_pos(num_list: List[List[int]], position: int, comparison: Callable) -> int:
    if len(num_list) == 1:
        return binary_2_decimal(num_list[0])

    val = sum(n[position] for n in num_list)
    most_often_digit = 1 if comparison(val, len(num_list) / 2) else 0
    return find_extreme_at_pos([n for n in num_list if n[position] == most_often_digit], position + 1, comparison)


def binary_2_decimal(binary: List[int]) -> int:
    val = 0
    for i, b in enumerate(binary[::-1]):
        val += 2 ** i * b
    return val


oxy = find_extreme_at_pos(input_numbers, 0, lambda x, y: x >= y)
co2 = find_extreme_at_pos(input_numbers, 0, lambda x, y: x < y)
print(oxy * co2)
