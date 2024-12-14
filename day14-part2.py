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
        return (
            (self.x + self.vx * seconds) % self.width,
            (self.y + self.vy * seconds) % self.height,
        )

    def __repr__(self):
        return f"(p={self.x},{self.y} v={self.vx},{self.vy})"


def print_robots(robot_pos, height, width, seconds):
    xy = set(robot_pos)

    # Making an assumption that no two robots will
    # be in the same position when tree exists.
    if len(xy) != len(robot_pos):
        return

    print("=" * width, " ->", seconds)
    for y in range(height):
        for x in range(width):
            if (x, y) in xy:
                print("#", end="")
            else:
                print(".", end="")
        print("")
    print("=" * width)


HEIGHT = 103
WIDTH = 101


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    robots = list(
        Robot(*map(int, rbt))
        for rbt in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", data)
    )

    for s in range(HEIGHT * WIDTH):
        positions = [r.move(s) for r in robots]
        print_robots(positions, HEIGHT, WIDTH, s)


if __name__ == "__main__":
    main()
