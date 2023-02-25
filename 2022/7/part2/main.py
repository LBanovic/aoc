import sys


class Directory:

    def __init__(self, name, super_dir):
        self.name = name
        self.super_dir = super_dir if super_dir is not None else self
        self.dirs = []
        self.files = set()

    @property
    def size(self):
        return sum([d.size for d in self.dirs]) + sum(size for size, name in self.files)


dirs = {}
current_dir = None

listing_dir = False

for line in open(sys.argv[1]):
    if line.startswith('$ cd'):
        listing_dir = False
        new_dir = line.split()[2]
        if new_dir == '..':
            new_dir = current_dir.super_dir.name
        elif new_dir != '/':
            new_dir = f'{current_dir.name}-{new_dir}'

        if new_dir not in dirs:
            dirs[new_dir] = Directory(new_dir, current_dir)
        current_dir = dirs[new_dir]

    elif line.startswith('$ ls'):
        listing_dir = True
        continue

    if listing_dir:
        type_, name = line.split()
        if type_ == 'dir':
            name = f'{current_dir.name}-{name}'
            if name not in dirs:
                dirs[name] = Directory(name, current_dir)
            current_dir.dirs.append(dirs[name])
        else:
            size = int(type_)
            current_dir.files.add((size, name))

MAX_SPACE = 70_000_000
TARGET_UNUSED = 30_000_000
sizes = [d.size for d in dirs.values()]
free_space = MAX_SPACE - dirs['/'].size

potential_candidates = [size for size in sizes if size + free_space >= TARGET_UNUSED]
print(min(potential_candidates))