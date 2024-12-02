import sys

with open(sys.argv[1]) as f:
    data = f.read()


def is_safe(level: list[int], recur=False):
    # just remove first and second element and check
    if not recur and (is_safe(level[1:], True) or is_safe(level[:1] + level[2:], True)):
        return True

    increasing = level[1] - level[0]

    if increasing == 0:
        return False

    increasing = increasing > 0

    for i in range(len(level) - 1):
        diff = level[i + 1] - level[i]
        if (diff > 0) != increasing:
            if recur:
                return False
            else:
                return is_safe(level[:i] + level[i + 1 :], True) or is_safe(
                    level[: i + 1] + level[i + 2 :], True
                )
        diff = abs(diff)
        if diff < 1 or diff > 3:
            if recur:
                return False
            else:
                return is_safe(level[:i] + level[i + 1 :], True) or is_safe(
                    level[: i + 1] + level[i + 2 :], True
                )

    return True


print(sum([is_safe(list(map(int, level.split()))) for level in data.splitlines()]))
