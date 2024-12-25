import sys


PRUNE_DIVISOR = 16777216


def next_secret_num(num):
    step_1 = num * 64
    num = (num ^ step_1) % PRUNE_DIVISOR

    step_2 = num // 32
    num = (num ^ step_2) % PRUNE_DIVISOR

    step_3 = num * 2048
    num = (num ^ step_3) % PRUNE_DIVISOR

    return num


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    nums = map(int, data.splitlines())
    for _ in range(2000):
        nums = map(next_secret_num, nums)

    print(sum(nums))


if __name__ == "__main__":
    main()
