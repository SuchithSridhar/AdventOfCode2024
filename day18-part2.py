import sys
from collections import deque

SIZE = 71

EMPTY = 0
WALL = 1


def min_steps(grid, start, end):
    # just a simple BFS
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = len(grid), len(grid[0])

    r, c = start
    queue = deque([(*start, 0)])
    visited = set([start])

    while queue:
        r, c, steps = queue.popleft()
        if (r, c) == end:
            return steps

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == EMPTY
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append((nr, nc, steps + 1))

    return -1


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    start = (0, 0)
    end = (SIZE - 1, SIZE - 1)
    grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    locs = [tuple(map(int, line.split(","))) for line in data.splitlines()]

    for c, r in locs:
        grid[r][c] = WALL
        if min_steps(grid, start, end) == -1:
            print(f"{c},{r}")
            break


if __name__ == "__main__":
    main()
