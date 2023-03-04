import sys
from pathlib import Path

input_file = Path(sys.argv[1])

opening = ('(', '[', '{', '<')
closing = (')', ']', '}', '>')
scores = (3, 57, 1197, 25137)

score_sum = 0
for line in input_file.open():
    stack = []
    for ch in line:
        if ch in opening:
            stack.insert(0, ch)
        elif ch in closing:
            closing_index = closing.index(ch)
            if not stack:
                score_sum += scores[closing_index]
                break
            pair = stack.pop(0)
            if opening.index(pair) != closing_index:
                score_sum += scores[closing_index]
                break

print(score_sum)
