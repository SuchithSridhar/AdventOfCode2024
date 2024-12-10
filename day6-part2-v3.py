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
            return self.col_obs[c][obs_idx] - 1, c, (dir + 1) % 4
        elif DIRECTIONS[dir] == UP:
            obs_idx = bisect.bisect_left(self.col_obs[c], r) - 1
            return self.col_obs[c][obs_idx] + 1, c, (dir + 1) % 4
        elif DIRECTIONS[dir] == RIGHT:
            obs_idx = bisect.bisect_left(self.row_obs[r], c)
            return r, self.row_obs[r][obs_idx] - 1, (dir + 1) % 4
        else:
            obs_idx = bisect.bisect_left(self.row_obs[r], c) - 1
            return r, self.row_obs[r][obs_idx] + 1, (dir + 1) % 4

    def insert_obs(self, r, c):
        idx_r = bisect.bisect_left(self.row_obs[r], c)
        idx_c = bisect.bisect_left(self.col_obs[c], r)
        self.row_obs[r].insert(idx_r, c)
        self.col_obs[c].insert(idx_c, r)
        return idx_r, idx_c

    def remove_obs(self, r, c, idx_r, idx_c):
        self.row_obs[r].pop(idx_r)
        self.col_obs[c].pop(idx_c)

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
            if (nr * self.cols + nc) not in path_set:
                path_set.add(nr * self.cols + nc)
                path_list.append(self.encode(nr, nc, dir))

        return path_list

    def is_loop(self, gr, gc, gd):

        state_set: set[int] = set()
        pr, pc, pd = gr, gc, gd
        state_set.add(self.encode(pr, pc, pd))

        while True:
            nr, nc, nd = self.next_pos(pr, pc, pd)

            if nr <= 0 or nr >= self.rows - 1 or nc <= 0 or nc >= self.cols - 1:
                break

            if self.encode(nr, nc, nd) in state_set:
                # this indicates that we hit a loop!
                return True

            pr, pc, pd = nr, nc, nd
            state_set.add(self.encode(pr, pc, pd))

        return False


def main():

    with open(sys.argv[1]) as f:
        data = f.read()

    grid = Grid(data)
    path = grid.get_path()
    count = 0

    for i in range(len(path) - 1, 0, -1):
        r, c, _ = grid.decode(path[i])
        gr, gc, gd = grid.decode(path[i - 1])

        idx_r, idx_c = grid.insert_obs(r, c)
        grid.grid[r][c] = OBSTR
        loop = grid.is_loop(gr, gc, gd)
        grid.grid[r][c] = EMPTY
        grid.remove_obs(r, c, idx_r, idx_c)

        if loop:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
