import sys
from collections import deque

SIZE = 71
TIME_STEPS = 1024

EMPTY = 0
WALL = 1
SEEN = 2


def min_steps(grid, start, end):
    # just a simple BFS
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = len(grid), len(grid[0])

    r, c = start
    queue = deque([(*start, 0)])
    grid[r][c] = SEEN

    while queue:
        r, c, steps = queue.popleft()
        if (r, c) == end:
            return steps

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == EMPTY:
                grid[nr][nc] = SEEN
                queue.append((nr, nc, steps + 1))

    return -1


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    start = (0, 0)
    end = (SIZE - 1, SIZE - 1)
    grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    locs = [tuple(map(int, line.split(","))) for line in data.splitlines()]

    for i in range(TIME_STEPS):
        c, r = locs[i]
        grid[r][c] = WALL

    print(min_steps(grid, start, end))


if __name__ == "__main__":
    main()
