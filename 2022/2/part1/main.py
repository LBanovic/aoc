import sys

elf_input = {
    'A': 1,  # rock
    'B': 2,  # paper
    'C': 3   # scissors
}

my_response = {
    'X': 1,  # rock
    'Y': 2,  # paper
    'Z': 3   # scissors
}

with open(sys.argv[1]) as input_data:
    result = 0
    for line in input_data:
        elf_symbol, my_symbol = line.split()
        elf = elf_input[elf_symbol]
        me = my_response[my_symbol]

        result += me
        if elf == me:
            result +=  3
        elif (me - elf) % 3 == 1:
            result += 6

print(result)