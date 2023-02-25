import sys

matrix = []

for line in open(sys.argv[1]):
    matrix.append(list(map(int, line.strip())))

max_score = 0

for i, row in enumerate(matrix[1:-1], start=1):
    for j, el in enumerate(row[1:-1], start=1):
        left_guard = max(reversed(range(j)), key=lambda x: matrix[i][x] >= el)
        right_guard = max(range(j + 1, len(matrix[i])), key=lambda x: matrix[i][x] >= el)
        top_guard = max(reversed(range(i)), key=lambda x: matrix[x][j] >= el)
        bottom_guard = max(range(i + 1, len(matrix)), key=lambda x: matrix[x][j] >= el)

        if matrix[i][left_guard] < el:
            left_guard = 0

        if matrix[i][right_guard] < el:
            right_guard = len(matrix[i]) - 1

        if matrix[top_guard][j] < el:
            top_guard = 0

        if matrix[bottom_guard][j] < el:
            bottom_guard = len(matrix) - 1

        scenic_score = (j - left_guard) * (right_guard - j) * (i - top_guard) * (bottom_guard - i)

        max_score = max(max_score, scenic_score)

print(max_score)
