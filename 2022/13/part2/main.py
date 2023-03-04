import sys

pairs_of_packets = []

pair = []
for line in open(sys.argv[1]):
    if line.strip():
        pair.append(eval(line.strip()))
    else:
        pairs_of_packets.append(pair)
        pair = []

pairs_of_packets.append(pair)


def compare_pair(x, y):
    if isinstance(x, int) and isinstance(y, int):
        comparison = 0 if x == y else (-1 if x > y else 1)
        return comparison

    if isinstance(x, list) and isinstance(y, list):
        for xel, yel in zip(x, y):
            comparison = compare_pair(xel, yel)
            if comparison != 0:
                return comparison
        comparison = 0 if len(x) == len(y) else (-1 if len(x) > len(y) else 1)
        return comparison

    x = x if isinstance(x, list) else [x]
    y = y if isinstance(y, list) else [y]

    return compare_pair(x, y)


class Comparator:

    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return -compare_pair(self.x, other.left) == 0

    def __lt__(self, other):
        # -compare cause the assumption is the other is greater
        return -compare_pair(self.x, other.left) < 0

    def __gt__(self, other):
        return -compare_pair(self.x, other.left) > 0


divider_packets = [[2]], [[6]]

packets = [*divider_packets]
for pair in pairs_of_packets:
    packets.extend(pair)

packets.sort(key=Comparator)
indices = [packets.index(d) + 1 for d in divider_packets]

print(indices[0] * indices[1])

