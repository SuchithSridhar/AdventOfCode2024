import sys
import heapq

START_CHAR = "S"
END_CHAR = "E"
WALL = "#"
EMPTY = "."

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

STEP_WEIGHT = 1
TURN_WEIGHT = 1000


class Grid:
    def __init__(self, data):
        self.grid = data.splitlines()
        self.cols = len(self.grid[0])
        self.rows = len(self.grid)

        start_row = self.rows - 2
        start_col = 1
        end_row = 1
        end_col = self.cols - 2

        self.start = (start_row, start_col, EAST)
        self.end = (end_row, end_col)

        assert (
            self.grid[start_row][start_col] == START_CHAR
        ), "Assumption about starting position violated"
        assert (
            self.grid[end_row][end_col] == END_CHAR
        ), "Assumption about ending pointion violated"


def find_shortest_path(grid):
    # simple implementation of Dijkstra's algorithm
    # using direction as a part of the state

    pq: list[tuple[int, int, int, int]] = []
    heapq.heappush(pq, (0, *grid.start))

    distances = {
        (r, c, d): float("inf")
        for r in range(grid.rows)
        for c in range(grid.cols)
        for d in range(len(DIRECTIONS))
    }
    distances[grid.start] = 0

    visited = set()

    while pq:
        cdist, crow, ccol, cdir = heapq.heappop(pq)
        cur = (crow, ccol, cdir)
        if cur in visited:
            continue
        visited.add(cur)

        for dir in [-1, 0, 1]:
            if dir == 0:
                dr, dc = DIRECTIONS[(cdir + dir) % len(DIRECTIONS)]
                next = (crow + dr, ccol + dc, cdir)
                weight = STEP_WEIGHT
            else:
                next = crow, ccol, (cdir + dir) % len(DIRECTIONS)
                weight = TURN_WEIGHT

            if grid.grid[next[0]][next[1]] == WALL:
                continue

            dist = cdist + weight
            if dist < distances[next]:
                distances[next] = dist
                heapq.heappush(pq, (dist, *next))

    return min(
        distances[(grid.end[0], grid.end[1], NORTH)],
        distances[(grid.end[0], grid.end[1], SOUTH)],
        distances[(grid.end[0], grid.end[1], EAST)],
        distances[(grid.end[0], grid.end[1], WEST)],
    )


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    grid = Grid(data)
    print(find_shortest_path(grid))


if __name__ == "__main__":
    main()
