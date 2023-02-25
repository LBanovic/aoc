import sys

matrix = []

for line in open(sys.argv[1]):
    matrix.append(list(map(int, line.strip())))


not_visible = 0

for i, row in enumerate(matrix[1:-1], start=1):
    for j, el in enumerate(row[1:-1], start=1):
        left_guard = max(matrix[i][:j])
        right_guard = max(matrix[i][j+1:])
        top_guard = max([row[j] for row in matrix[:i]])
        bottom_guard = max([row[j] for row in matrix[i+1:]])

        not_visible += el <= left_guard and el <= right_guard and el <= top_guard and el <= bottom_guard

print(len(matrix) * len(matrix[0]) - not_visible)