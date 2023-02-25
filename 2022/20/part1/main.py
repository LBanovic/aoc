import sys
from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm

input_file = Path(sys.argv[1])

INDICES_AFTER_ZERO = (1000, 2000, 3000)

numbers_ordered_by_file = list(map(int, input_file.open()))
n = len(numbers_ordered_by_file)


@dataclass
class Node:
    number: int
    left: 'Node' = None
    right: 'Node' = None


nodes = [Node(num) for num in numbers_ordered_by_file]
zero_node = [node for node in nodes if node.number == 0][0]

for i, node in enumerate(nodes):
    node.left = nodes[(i - 1) % n]
    node.right = nodes[(i + 1) % n]

m = n - 1
for node in nodes:
    if node.number > 0:
        for _ in range(node.number % m):
            # resolve left and right nodes first
            node.right.left = node.left
            node.left.right = node.right

            # resolve node
            helper = node.right
            node.right = helper.right
            node.left = helper

            # resolve right node
            helper.right.left = node
            helper.right = node

    else:
        for _ in range(-node.number % m):
            # resolve left and right nodes first
            node.left.right = node.right
            node.right.left = node.left

            # resolve node
            helper = node.left
            node.left = helper.left
            node.right = helper

            helper.left.right = node
            helper.left = node

    curr_node = zero_node


curr_node = zero_node
total = 0
for _ in range(3):
    for _ in range(1000):
        curr_node = curr_node.right
    print(curr_node.number)
    total += curr_node.number
print(total)