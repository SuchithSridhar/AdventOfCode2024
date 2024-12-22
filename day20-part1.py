from collections import deque
import sys

START = "S"
END = "E"
WALL = "#"
EMPTY = "."
MIN_SAVE = 100


def find_start_end(grid):
    start, end = (-1, -1), (-1, -1)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == START:
                start = (r, c)
            elif grid[r][c] == END:
                end = (r, c)
    return start, end


def find_path(grid, start, end):
    # assuming boundary checking not necessary since surrounded by walls

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    queue = deque([(start)])
    previous: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

    def build_path():
        path = []
        prev = end
        while prev is not None:
            path.append(prev)
            prev = previous[prev]
        path.reverse()
        return path

    while queue:
        cr, cc = queue.popleft()
        if (cr, cc) == end:
            return build_path()
        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc
            if grid[nr][nc] != WALL and (nr, nc) not in previous:
                previous[(nr, nc)] = (cr, cc)
                queue.append((nr, nc))

    return []


def cheat_options(grid, path: list[tuple[int, int]]):
    # assumption: looking at cheats of length 2
    # this ensure that we don't see original path more than once
    # for every point in the path, i'm going to walk in all
    # possible direction to see if it speeds me up.

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    options = []

    # need to be at least 4 to save any time
    for i, (pr, pc) in enumerate(path[:-3]):
        for dr, dc in directions:
            nr, nc = pr + dr, pc + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != WALL:
                continue

            for drn, dcn in directions:
                nrn, ncn = nr + drn, nc + dcn
                if (pr, pc) == (nrn, ncn):
                    continue
                try:
                    index = path.index((nrn, ncn), i)
                    options.append(index - i - 2)
                except ValueError:
                    continue

    return options


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
    start, end = find_start_end(grid)
    path = find_path(grid, start, end)
    options = cheat_options(grid, path)
    print(len(list(filter(lambda x: x >= MIN_SAVE, options))))


if __name__ == "__main__":
    main()
