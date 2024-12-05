import sys

with open(sys.argv[1]) as f:
    data = f.read()


def is_update_broken(update, rules_map):
    prev = set()
    for i, elem in enumerate(update):
        if elem in rules_map:
            inter = rules_map[elem].intersection(prev)
            if len(inter) > 0:
                return i, inter.pop()
        prev.add(elem)

    return -1, -1


def fix_update(update, bidx, belem):
    eidx = update.index(belem)
    update[bidx], update[eidx] = update[eidx], update[bidx]


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
    was_broken = False
    idx, elem = is_update_broken(update, rules_map)
    while idx != -1:
        was_broken = True
        fix_update(update, idx, elem)
        idx, elem = is_update_broken(update, rules_map)

    if was_broken:
        sum += update[len(update) // 2]

print(sum)
