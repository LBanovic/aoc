import sys
from pathlib import Path

input_file = Path(sys.argv[1])

opening = ('(', '[', '{', '<')
closing = (')', ']', '}', '>')
scores = (1, 2, 3, 4)

score_list = []
for line in input_file.open():
    stack = []
    for ch in line:
        if ch in opening:
            stack.insert(0, ch)
        elif ch in closing:
            closing_index = closing.index(ch)
            if not stack:
                break
            pair = stack.pop(0)
            if opening.index(pair) != closing_index:
                break
    else:
        score_sum = 0
        for val in stack:
            assert val in opening
            score = scores[opening.index(val)]
            score_sum = score_sum * 5 + score
        score_list.append(score_sum)

middle = len(score_list) // 2
print(sorted(score_list)[middle])
