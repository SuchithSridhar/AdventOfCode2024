import sys

with open(sys.argv[1]) as f:
    data = f.read()


def check_update(update, rules_map):
    prev = set()
    for elem in update:
        if (elem in rules_map) and len(rules_map[elem].intersection(prev)) > 0:
            return 0
        prev.add(elem)

    return update[len(update) // 2]


rules, updates = data.split("\n\n")
rules = rules.strip().split("\n")
updates = updates.strip().split("\n")
rules = [list(map(int, rule.split("|"))) for rule in rules]
updates = [list(map(int, update.split(","))) for update in updates]

rules_map: dict[int, set[int]] = {}

for lhs, rhs in rules:
    if lhs in rules_map:
        rules_map[lhs].add(rhs)
    else:
        rules_map[lhs] = {rhs}

sum = 0

for update in updates:
    sum += check_update(update, rules_map)

print(sum)
