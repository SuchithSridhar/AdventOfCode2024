import sys
from collections import deque


PRUNE_DIVISOR = 16777216


def next_secret_num(num):
    step_1 = num * 64
    num = (num ^ step_1) % PRUNE_DIVISOR

    step_2 = num // 32
    num = (num ^ step_2) % PRUNE_DIVISOR

    step_3 = num * 2048
    num = (num ^ step_3) % PRUNE_DIVISOR

    return num


def update_change_map(num, change_map):
    # this stores the previous 4 price changes at all times
    queue = deque()
    length = 4

    # each buyer can only see a sequence once, the first time.
    seen = set()
    current = num
    next = None

    for _ in range(length):
        next = next_secret_num(current)
        change = (next % 10) - (current % 10)
        queue.append(change)
        current = next

    key = tuple(queue)
    change_map[key] = change_map.get(key, 0) + current % 10
    seen.add(key)

    for _ in range(2000 - length):
        next = next_secret_num(current)
        change = (next % 10) - (current % 10)
        current = next
        queue.popleft()
        queue.append(change)
        key = tuple(queue)
        if key not in seen:
            change_map[key] = change_map.get(key, 0) + current % 10
            seen.add(key)


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    nums = map(int, data.splitlines())
    change_map = {}
    for num in nums:
        update_change_map(num, change_map)

    print(max(change_map.values()))


if __name__ == "__main__":
    main()
