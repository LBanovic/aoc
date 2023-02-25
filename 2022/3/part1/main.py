import sys

characters = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]

priority_map = dict(zip(characters, range(1, 53)))

priority_sum = 0

for line in open(sys.argv[1]):
    half_point = len(line) // 2
    first_half = set(line[:half_point])
    second_half = set(line[half_point:])

    intersected_char = (first_half & second_half).pop()
    priority_sum += priority_map[intersected_char]

print(priority_sum)