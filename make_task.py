import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('year', help='AOC Year')
parser.add_argument('task', help='AOC Task')

args = parser.parse_args()

parts = ['part1', 'part2']
files = ['main.py']

if __name__ == '__main__':
    root_dir = Path(args.year) / args.task
    for part in parts:
        partdir = root_dir / part
        partdir.mkdir(exist_ok=True, parents=True)
        for f in files:
            filepath = partdir / f
            filepath.touch()
            if f == 'main.py':
                filepath.open('w').writelines(['import sys\n',
                                               'from pathlib import Path\n\n',
                                               'input_file = Path(sys.argv[1])'])
