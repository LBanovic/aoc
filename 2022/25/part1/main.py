import sys
from pathlib import Path

input_file = Path(sys.argv[1])

snafu_2_digits = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

digits_2_snafu = dict(zip(snafu_2_digits.values(), snafu_2_digits.keys()))


def snafu_2_num(snafu_str: str) -> int:
    total = 0
    for i, digit in enumerate(reversed(snafu_str)):
        total += 5 ** i * snafu_2_digits[digit]
    return total


def num_2_snafu(num: int) -> str:
    snafu = []
    while num:
        digit = num % 5
        num //= 5
        if digit <= 2:
            snafu.append(str(digit))
        else:
            snafu.append(digits_2_snafu[digit - 5])
            num += 1

    return ''.join(reversed(snafu))


total = 0
for line in input_file.open():
    total += snafu_2_num(line.strip())
print(num_2_snafu(total))
