import sys
import re


class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.height = HEIGHT
        self.width = WIDTH

    def get_quad(self):
        # 1 | 2
        # 3 | 4
        hw = self.width // 2
        hh = self.height // 2

        if self.x < hw and self.y < hh:
            return 1
        elif self.x < hw and self.y > hh:
            return 2
        elif self.x > hw and self.y < hh:
            return 3
        elif self.x > hw and self.y > hh:
            return 4
        else:
            return 0

    def move(self, seconds):
        self.x = (self.x + self.vx * seconds) % self.width
        self.y = (self.y + self.vy * seconds) % self.height

    def __repr__(self):
        return f"(p={self.x},{self.y} v={self.vx},{self.vy})"


HEIGHT = 103
WIDTH = 101
SECONDS = 100


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    robots = list(
        Robot(*map(int, rbt))
        for rbt in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", data)
    )

    r_count = {x: 0 for x in range(0, 5)}
    for r in robots:
        r.move(SECONDS)
        r_count[r.get_quad()] += 1

    print(r_count[1] * r_count[2] * r_count[3] * r_count[4])


if __name__ == "__main__":
    main()
