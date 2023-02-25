import sys


class Monkey:

    def __init__(self, monkeys, worry_levels, worry_update_op, divide_by, targets):
        self.worry_levels = worry_levels
        self.worry_update_op = worry_update_op
        self.divide_by = divide_by
        self.targets = targets

        self.monkeys = monkeys
        self.inspected = 0

    def do_turn(self):
        while len(self.worry_levels):
            worry_level = self.worry_levels.pop(0) % GLOBAL_MODULO
            old = worry_level
            worry_level = eval(self.worry_update_op)
            test = worry_level % self.divide_by == 0
            target = self.targets[int(test)]
            self.monkeys[target].receive(worry_level)
            self.inspected += 1

    def receive(self, worry_level):
        self.worry_levels.append(worry_level)


monkeys = []
current_monkey = 0
monkey_data = {'monkeys': monkeys}
targets = []

for line in open(sys.argv[1]):
    line = line.strip()
    if line:
        if 'Starting items' in line:
            items = list(map(int, line.split(':')[-1].split(',')))
            monkey_data['worry_levels'] = items
        elif 'Operation' in line:
            op_string = line.split('=')[-1]
            operation = op_string
            monkey_data['worry_update_op'] = operation
        elif 'Test' in line:
            test = int(line.split()[-1])
            monkey_data['divide_by'] = test
        elif 'If true' in line:
            targets.append(int(line.split()[-1]))
        elif 'If false' in line:
            targets.insert(0, int(line.split()[-1]))
    else:
        monkey_data['targets'] = targets
        targets = []
        monkey = Monkey(**monkey_data)
        monkeys.append(monkey)
        monkey_data = {'monkeys': monkeys}
        current_monkey += 1

monkey_data['targets'] = targets
targets = []
monkey = Monkey(**monkey_data)
monkeys.append(monkey)
monkey_data = {'monkeys': monkeys}
current_monkey += 1

GLOBAL_MODULO = 1
for monkey in monkeys:
    GLOBAL_MODULO *= monkey.divide_by

round_count = 10000

for i in range(round_count):
    for j, monkey in enumerate(monkeys):
        monkey.do_turn()

monkeys.sort(key=lambda x: x.inspected)
print(monkeys[-2].inspected * monkeys[-1].inspected)