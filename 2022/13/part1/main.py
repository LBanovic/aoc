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


# for i, pair in enumerate(pairs_of_packets):
#     val = compare_pair(*pair)

valid_pairs = [i + 1 for i, pair in enumerate(pairs_of_packets) if compare_pair(*pair) > 0]

print(sum(valid_pairs))
