import sys
totals_per_elf = []

with open(sys.argv[1]) as input_data:
    elf_total = 0
    for line in input_data:
        line = line.strip()
        if line:
            elf_total += int(line)
        else:
            totals_per_elf.append(elf_total)
            elf_total = 0
totals_per_elf.append(elf_total)
print(max(totals_per_elf))