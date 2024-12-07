import sys

# The original implementation takes 36s to find all the different positions.
# This newer implementation only checks positions on the path, runs in 5s.
"""
$ time python day6-part2.py input/day6-input.txt
1309
34.23s user 0.00s system 99% cpu 34.310 total

$ time python day6-part2-improved.py input/day6-input.txt
1309
5.71s user 0.02s system 99% cpu 5.739 total
"""

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

GUARD = "^"
EMPTY = "."
OBSTR = "#"

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
DIR_COUNT = len(DIRECTIONS)


class Grid:
    def __init__(self, data: str):
        lines = data.strip().splitlines()
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.grid = list(map(list, lines))
        self.guard = self.find_guard()
        self.dir = 0

    def find_guard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == GUARD:
                    return (row, col)

        return (-1, -1)

    def encode(self, row: int, col: int, direction: int):
        return (row * self.cols + col) * DIR_COUNT + direction

    def decode(self, hash) -> tuple[int, int, int]:
        direction = hash % DIR_COUNT
        cell_index = hash // DIR_COUNT
        col = cell_index % self.cols
        row = cell_index // self.cols
        return row, col, direction

    def get_path(self):
        path = [self.encode(self.guard[0], self.guard[1], self.dir)]

        init_pos = self.guard
        init_dir = self.dir

        while True:
            nr = self.guard[0] + DIRECTIONS[self.dir][0]
            nc = self.guard[1] + DIRECTIONS[self.dir][1]

            if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                break

            if self.grid[nr][nc] == OBSTR:
                self.dir = (self.dir + 1) % DIR_COUNT
                continue

            self.guard = (nr, nc)
            path.append(self.encode(nr, nc, self.dir))

        self.guard = init_pos
        self.dir = init_dir

        return path

    def is_loop(self, guard_pos, guard_dir):
        state_set: set[int] = set()
        pos = guard_pos
        dir = guard_dir
        state_set.add(self.encode(pos[0], pos[1], dir))

        while True:
            nr = pos[0] + DIRECTIONS[dir][0]
            nc = pos[1] + DIRECTIONS[dir][1]

            if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                break

            if self.grid[nr][nc] == OBSTR:
                dir = (dir + 1) % DIR_COUNT
                continue

            if self.encode(nr, nc, dir) in state_set:
                # this indicates that we hit a loop!
                return True

            pos = (nr, nc)
            state_set.add(self.encode(nr, nc, dir))

        return False


with open(sys.argv[1]) as f:
    data = f.read()

grid = Grid(data)
path = grid.get_path()

count = 0
hashset = set()
for i in range(len(path) - 1, 0, -1):
    r1, c1, _ = grid.decode(path[i])
    hash = r1 * grid.cols + c1

    # if either guard position or we've already added this position
    if grid.guard == (r1, c1) or hash in hashset:
        continue

    grid.grid[r1][c1] = OBSTR
    loop = grid.is_loop(grid.guard, grid.dir)
    grid.grid[r1][c1] = EMPTY

    if loop:
        hashset.add(hash)
        count += 1

print(count)
