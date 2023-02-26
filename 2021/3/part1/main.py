import sys
from pathlib import Path

input_file = Path(sys.argv[1])
sum_by_element = []
i = 0
for line in input_file.open():
    digits = map(int, line.strip())
    if not sum_by_element:
        sum_by_element = list(digits)
    else:
        sum_by_element = [s + d for s, d in zip(sum_by_element, digits)]
    i += 1

n_rows = i + 1
gamma = []
epsilon = []
for count in sum_by_element:
    is_more_than_half = count > n_rows / 2
    gamma.append(int(is_more_than_half))
    epsilon.append(1 - int(is_more_than_half))

gamma_decimal = 0
epsilon_decimal = 0
for i, (g, e) in enumerate(zip(gamma[::-1], epsilon[::-1])):
    gamma_decimal += 2 ** i * g
    epsilon_decimal += 2 ** i * e

print(gamma_decimal * epsilon_decimal)