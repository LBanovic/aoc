import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('year', help='AOC Year')
parser.add_argument('task', help='AOC Task')
parser.add_argument('part', help='part of task')
parser.add_argument('input_file', help='name of input file .txt')
parser.add_argument('--runner_file', help='name of file to run .py', default='main.py', required=False)


args = parser.parse_args()

if __name__ == '__main__':
    directory = Path(args.year) / args.task / f'part{args.part}'
    runner_file = directory / args.runner_file
    input_file = directory / args.input_file
    subprocess.run(f'python {runner_file} {input_file}', shell=True)
