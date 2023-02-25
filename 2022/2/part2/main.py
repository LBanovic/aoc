import sys

elf_input = {
    'A': 1,  # rock
    'B': 2,  # paper
    'C': 3   # scissors
}

outcomes = {
    'X': 0,  # lose
    'Y': 3,  # draw
    'Z': 6   # win
}


with open(sys.argv[1]) as input_data:
    result = 0
    for line in input_data:
        elf_symbol, my_outcome = line.split()
        elf = elf_input[elf_symbol]
        outcome = outcomes[my_outcome]

        shift = (outcome // 3 - 1) % 3
        answer = elf + shift
        answer = answer % 3 if answer > 3 else answer
        result += outcome + answer

print(result)