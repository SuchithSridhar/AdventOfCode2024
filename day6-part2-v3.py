import sys
import bisect

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

GUARD = "^"
EMPTY = "."
OBSTR = "#"

INF = 999999

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
DIR_COUNT = len(DIRECTIONS)


class Grid:
    def __init__(self, data: str):
        lines = data.strip().splitlines()
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.grid = list(map(list, lines))
        self.guard = (-1, -1)
        self.dir = 0
        self.find_guard_build_table()

    def find_guard_build_table(self):
        # self.row_obs[r] = [c1, c2, ... ,cn]
        # stores an array of column positions which contain
        # an obsticle in row r.
        self.row_obs = [[-1] for _ in range(self.rows)]
        self.col_obs = [[-1] for _ in range(self.cols)]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == OBSTR:
                    self.row_obs[row].append(col)
                    self.col_obs[col].append(row)

                elif self.grid[row][col] == GUARD:
                    self.guard = (row, col)
                    self.grid[row][col] = EMPTY

        for i in range(max(self.rows, self.cols)):
            if i < self.rows:
                self.row_obs[i].append(INF)
            if i < self.cols:
                self.col_obs[i].append(INF)

    def encode(self, row: int, col: int, direction: int):
        return (row * self.cols + col) * DIR_COUNT + direction

    def decode(self, hash) -> tuple[int, int, int]:
        direction = hash % DIR_COUNT
        cell_index = hash // DIR_COUNT
        col = cell_index % self.cols
        row = cell_index // self.cols
        return row, col, direction

    def next_pos(self, r, c, dir) -> tuple[int, int, int]:
        if DIRECTIONS[dir] == DOWN:
            obs_idx = bisect.bisect_left(self.col_obs[c], r)
            return self.col_obs[c][obs_idx], c, (dir + 1) % 4
        elif DIRECTIONS[dir] == UP:
            obs_idx = bisect.bisect_left(self.col_obs[c], r) - 1
            return self.col_obs[c][obs_idx], c, (dir + 1) % 4
        elif DIRECTIONS[dir] == RIGHT:
            obs_idx = bisect.bisect_left(self.row_obs[r], c)
            return r, self.row_obs[r][obs_idx], (dir + 1) % 4
        else:
            obs_idx = bisect.bisect_left(self.row_obs[r], c) - 1
            return r, self.row_obs[r][obs_idx], (dir + 1) % 4

    def get_path(self):

        pos = self.guard
        dir = self.dir

        path_set = {pos[0] * self.cols + pos[1]}
        path_list = [self.encode(pos[0], pos[1], dir)]

        while True:
            nr = pos[0] + DIRECTIONS[dir][0]
            nc = pos[1] + DIRECTIONS[dir][1]

            if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                break

            if self.grid[nr][nc] == OBSTR:
                dir = (dir + 1) % DIR_COUNT
                continue

            pos = (nr, nc)
            if (pos[0] * self.cols + pos[1]) not in path_set:
                path_set.add(pos[0] * self.cols + pos[1])
                path_list.append(self.encode(nr, nc, dir))

        return path_list

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


def main():

    with open(sys.argv[1]) as f:
        data = f.read()

    grid = Grid(data)
    path = grid.get_path()
    count = 0
    for i in range(len(path) - 1, 0, -1):
        r1, c1, _ = grid.decode(path[i])
        gr, gc, dir = grid.decode(path[i - 1])

        grid.grid[r1][c1] = OBSTR
        loop = grid.is_loop((gr, gc), dir)
        grid.grid[r1][c1] = EMPTY

        if loop:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
