import sys
from math import floor, log10, pow
from functools import cache


@cache
def run_rule(num: int) -> list[int]:
    if num == 0:
        return [1]

    num_digits = floor(log10(num)) + 1
    if num_digits % 2 == 0:
        divisor = int(pow(10, num_digits // 2))
        return [num // divisor, num % divisor]

    return [num * 2024]


@cache
def split_num(num, iters) -> int:
    if iters == 0:
        return 1

    return sum(split_num(n, iters - 1) for n in run_rule(num))


ITERATIONS = 75


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    nums = list(map(int, data.strip().split(" ")))
    print(sum(split_num(n, ITERATIONS) for n in nums))


if __name__ == "__main__":
    main()
