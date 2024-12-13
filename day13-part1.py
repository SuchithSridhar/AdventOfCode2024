import sys
import re

EPSILON = 10e-4


class Machine:
    def __init__(self, ax, ay, bx, by, px, py):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py

    def tokens_to_win(self):
        B = (self.py * self.ax - self.ay * self.px) / (
            self.by * self.ax - self.bx * self.ay
        )
        A = (self.px - B * self.bx) / self.ax
        if abs(A - int(A)) < EPSILON and abs(B - int(B)) < EPSILON:
            return 3 * A + 1 * B

        return 0


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    print(
        sum(
            Machine(*map(int, m)).tokens_to_win()
            for m in re.findall(
                r"X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
                data,
            )
        )
    )


if __name__ == "__main__":
    main()
