import sys

line_count = 0
for line in open(sys.argv[1]):
    sector1, sector2 = line.split(',')
    s1_start, s1_end = map(int, sector1.split('-'))
    s2_start, s2_end = map(int, sector2.split('-'))
    sector1_range = set(range(s1_start, s1_end + 1))
    sector2_range = set(range(s2_start, s2_end + 1))

    smaller_set = sector1_range if len(sector1_range) <= len(sector2_range) else sector2_range
    larger_set = sector1_range if len(sector1_range) > len(sector2_range) else sector2_range

    line_count += int((smaller_set & larger_set) == smaller_set)

print(line_count)