import sys
from pathlib import Path
from typing import Dict

from tqdm import tqdm

input_file = Path(sys.argv[1])

symbols = ('.', '#')

characters = None
image = {}
for y, line in enumerate(input_file.open()):
    if line.strip():
        if characters is None:
            characters = [symbols.index(ch) for ch in line.strip()]
        else:
            for x, ch in enumerate(line.strip()):
                image[x, y - 2] = symbols.index(ch)


def adjacent(image: Dict, x: int, y: int) -> str:
    return ''.join([str(image.get((x + dx, y + dy), default_value)) for dy in range(-1, 2) for dx in range(-1, 2)])


default_value = 0

STEPS = 50
for _ in tqdm(range(STEPS)):
    new_image = image.copy()

    start_x = min(image, key=lambda tup: tup[0])[0] - 2
    start_y = min(image, key=lambda tup: tup[1])[1] - 2

    end_x = max(image, key=lambda tup: tup[0])[0] + 2
    end_y = max(image, key=lambda tup: tup[1])[1] + 2

    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            code = adjacent(image, x, y)
            index = int(code, 2)
            new_image[x, y] = characters[index]
    image = new_image

    '''
    Everything is easy except you have to figure out the oscillation.
    
    If characters[0] == 1, that means that after one step all unseen pixels are turned on after one step.
    Because the picture is infinite, it means that there will be infinitely many pixels lit after one step.
    
    Since we know that for this input file, the result must be finite (due to it being AOC :)), we can assume that
    the next step will turn the unseen pixels off. This means unseen pixels will oscillate and is the reason behind
    this if-statement.
    '''
    if characters[0] == 1:
        default_value = 1 - default_value

print(sum(image.values()))
