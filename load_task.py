import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('year', help='AOC Year')
parser.add_argument('task', help='AOC Task')
parser.add_argument('output_file', help='AOC File Name', choices=('test.txt', 'input.txt', 'task.txt'))
parser.add_argument('--part', help='Part of AOC Task', type=int, default=1)

args = parser.parse_args()

parts = ['part1', 'part2']

if __name__ == '__main__':
    root_dir = Path(args.year) / args.task
    data = []
    print('Press CTRL-D (Linux) or CTRL-Z (Windows) to finish input.\n')
    while True:
        try:
            data.append(input())
        except EOFError:
            break
    if args.output_file == 'task.txt':
        parts = parts[args.part - 1: args.part]

    for part in parts:
        filename = root_dir / part / args.output_file
        if not filename.exists():
            with filename.open('w') as outfile:
                outfile.write('\n'.join(data))