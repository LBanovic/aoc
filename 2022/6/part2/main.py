import sys

for line in open(sys.argv[1]):
    for i in range(14, len(line)):
        if len(set(line[i - 14:i])) == 14:
            print(i)
            break
