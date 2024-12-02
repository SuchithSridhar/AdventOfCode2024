import sys

with open(sys.argv[1]) as f:
    data = f.read()


def is_safe(level: list[int]):
    increasing = level[2] - level[1]

    if increasing == 0:
        return False

    increasing = increasing > 0

    for i in range(len(level) - 1):
        diff = level[i + 1] - level[i]
        if (diff > 0) != increasing:
            return False
        diff = abs(diff)
        if diff < 1 or diff > 3:
            return False

    return True


print(sum([is_safe(list(map(int, level.split()))) for level in data.splitlines()]))
