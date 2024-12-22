import sys

START = "S"
END = "E"
WALL = "#"
EMPTY = "."
MIN_SAVE = 100
MAX_CHEAT_LENGTH = 2


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == START:
                return (r, c)
    return (-1, -1)


def find_path(grid, start):
    # assuming boundary checking not necessary since surrounded by walls
    # assuming unique path from start to end

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    cr, cc = start
    path = [start]

    while grid[cr][cc] != END:
        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc
            if grid[nr][nc] != WALL and (nr, nc) not in path:
                path.append((nr, nc))
                cr, cc = nr, nc
                break

    return path


def cheat_options(
    path: list[tuple[int, int]], min_time_save: int, max_cheat_length: int
):
    # basically look from every point in the path to every other point in the
    # ptah to see if we can make it there in length steps. If we can, then this
    # is a valid cheat
    mcl = max_cheat_length
    mts = min_time_save
    count = 0

    for i in range(len(path)):
        for j in range(i + mts, len(path)):
            start, end = path[i], path[j]
            dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
            if dist <= mcl and j - i - dist >= min_time_save:
                count += 1

    return count


def grid_print(grid, path):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if (r, c) not in path:
                print(grid[r][c], end="")
            else:
                print("+", end="")
        print()


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    grid = [list(line) for line in data.splitlines()]
    start = find_start(grid)
    path = find_path(grid, start)
    # grid_print(grid, path)
    opt_count = cheat_options(path, MIN_SAVE, MAX_CHEAT_LENGTH)
    print(opt_count)


if __name__ == "__main__":
    main()
