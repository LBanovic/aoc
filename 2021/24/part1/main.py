import itertools
import sys
from pathlib import Path

input_file = Path(sys.argv[1])

read_ops = []
read_args = []

X = [12, 12, 15, -8, -4, 15, 14, 14, -13, -3, -7, 10, -6, -8]
Y = [1, 1, 16, 5, 9, 3, 2, 15, 5, 11, 7, 1, 10, 3]


def check(digits):
    z = 0
    result = [0] * 14
    digit_index = 0

    for i in range(14):
        x, y = X[i], Y[i]

        if x >= 0:
            z = z * 26 + digits[digit_index] + y
            result[i] = digits[digit_index]
            digit_index += 1

        else:
            result[i] = (z % 26) + x
            z //= 26
            if result[i] not in range(1, 10):
                return None
    return result


input_space = itertools.product(reversed(range(1, 10)), repeat=7)

for digits in input_space:
    result = check(digits)
    if result:
        print(''.join(str(i) for i in result))
        break
