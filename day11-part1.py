import sys
from itertools import chain


def run_rule(num: int) -> list[int]:
    if num == 0:
        return [1]

    snum = str(num)
    if len(snum) % 2 == 0:
        x = len(snum) // 2
        return [int(snum[:x]), int(snum[x:])]

    return [num * 2024]


ITERATIONS = 25


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    nums = list(map(int, data.strip().split(" ")))
    for _ in range(ITERATIONS):
        nums = list(chain.from_iterable(map(run_rule, nums)))

    print(len(nums))


if __name__ == "__main__":
    main()
