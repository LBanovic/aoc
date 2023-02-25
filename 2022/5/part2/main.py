import sys

stacks = []

finished_starting_configuration = False

for line in open(sys.argv[1]):
    if not line.strip():
        finished_starting_configuration = True
        continue

    if not finished_starting_configuration:
        elements_at_height = [line[i:i + 3] for i in range(0, len(line), 4)]
        for i, element in enumerate(elements_at_height):
            if i >= len(stacks):
                stacks.append([])
            stack = stacks[i]
            if element.strip():
                stack.insert(0, element[1:-1])
    else:
        line_split = line.split()
        amount = int(line_split[1])
        source = int(line_split[3]) - 1
        destination = int(line_split[5]) - 1

        destination_length = len(stacks[destination])
        for k in range(amount):
            stacks[destination].insert(destination_length, stacks[source].pop())

print(''.join(stack[-1] for stack in stacks))
