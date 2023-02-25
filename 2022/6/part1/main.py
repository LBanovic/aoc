import sys

for line in open(sys.argv[1]):
    for i in range(4, len(line)):
        if len(set(line[i-4:i])) == 4:
            print(i)
            break