import sys


def parse_locks_and_keys(items: list[str]) -> tuple[set, set]:
    locks = set()
    keys = set()
    is_key = False

    for item in items:
        item = item.strip().splitlines()
        cols = len(item[0])
        is_key = item[0][0] == "."
        heights = [0] * cols
        for row in item[1:-1]:
            heights = [
                heights[i] + (0 if row[i] == "." else 1)
                for i in range(len(heights))
            ]

        if is_key:
            keys.add(tuple(heights))
        else:
            locks.add(tuple(heights))

    return locks, keys


def does_key_overlap_lock(key: tuple[int], lock: tuple[int]) -> bool:
    assert len(key) == len(lock)

    HEIGHT = 5
    for k, l in zip(key, lock):
        if k + l > HEIGHT:
            return True

    return False


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    items = data.split("\n\n")
    locks, keys = parse_locks_and_keys(items)

    valid_pairs = 0

    for lock in locks:
        for key in keys:
            if not does_key_overlap_lock(key, lock):
                valid_pairs += 1

    print(valid_pairs)

if __name__ == "__main__":
    main()
