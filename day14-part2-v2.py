import sys
import re
import statistics as stats


class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.height = HEIGHT
        self.width = WIDTH

    def move(self, seconds):
        return (
            (self.x + self.vx * seconds) % self.width,
            (self.y + self.vy * seconds) % self.height,
        )


HEIGHT = 103
WIDTH = 101


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    robots = list(
        Robot(*map(int, rbt))
        for rbt in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", data)
    )

    # Thanks to r/i_have_no_biscuits for this solution based on statistics
    # https://www.reddit.com/r/adventofcode/comments/1hdvhvu/comment/m1zws1g/

    min_x, min_xvar, min_y, min_yvar = 0, 10000, 0, 10000

    for t in range(max(WIDTH, HEIGHT)):
        all_x, all_y = zip(*[r.move(t) for r in robots])
        x_var = stats.variance(all_x)
        y_var = stats.variance(all_y)

        if x_var < min_xvar:
            min_x, min_xvar = t, x_var

        if y_var < min_yvar:
            min_y, min_yvar = t, y_var

    k = (pow(WIDTH, -1, HEIGHT) * (min_y - min_x)) % HEIGHT
    min_xy = min_x + (k * WIDTH)

    print(min_xy)


"""
The premise of this approach is that we have minimum variance
in x and y when the tree is formed. However, x and y are independent
variance, so if we find the minimum variance in x and the minimum
variance in y we should be able to calculate when these two occur together.

Since x = (x + vx * s) % W, we know that there are at most W possible variances
for the x variable. Similarly, we have H possible variances for the Y variable.

For whatever time t with both lowest x variance and y variance:
t = min_x (mod W) = min_x + k*W
t = min_y (mod H)

that is, t = min_x + k*W

min_x + k*W = min_y (mod H)
k*W = min_y - min_x
k = (min_y - min_x) * W^-1

Note that we need W^-1 in field H.
The python function pow(value, pow, field) is used to accomodate this.

Then, once we have k, we can just plug k into the original t equation.
"""


if __name__ == "__main__":
    main()
