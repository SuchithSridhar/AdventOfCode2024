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


class State:
    def __init__(self, row, col, direction):
        self.r = row
        self.c = col
        self.d = direction

    @property
    def pos(self):
        return (self.r, self.c)

    @property
    def all(self):
        return (self.r, self.c, self.d)

    def next(self):
        dr, dc = DIRECTIONS[self.d]
        return State(self.r + dr, self.c + dc, self.d)

    def __hash__(self):
        return hash(self.all)

    def __eq__(self, other):
        return isinstance(other, State) and self.__hash__() == other.__hash__()


class Grid:
    def __init__(self, data):
        self.grid = data.splitlines()
        self.cols = len(self.grid[0])
        self.rows = len(self.grid)

        start_row = self.rows - 2
        start_col = 1
        end_row = 1
        end_col = self.cols - 2

        self.start = State(start_row, start_col, EAST)
        self.end = (end_row, end_col)

        assert (
            self.grid[start_row][start_col] == START_CHAR
        ), "Assumption about starting position violated"
        assert (
            self.grid[end_row][end_col] == END_CHAR
        ), "Assumption about ending pointion violated"


def find_shortest_path(grid):

    pq: list[tuple[int, State]] = []
    heapq.heappush(pq, (0, grid.start))

    distances = {
        State(r, c, d): float("inf")
        for r in range(grid.rows)
        for c in range(grid.cols)
        for d in range(len(DIRECTIONS))
    }
    visited = set()

    while pq:
        cur_dist, cur = heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)

        for dir in [-1, 0, 1]:
            if dir == 0:
                next = cur.next()
                weight = STEP_WEIGHT
            else:
                next = State(cur.r, cur.c, (cur.d + dir) % len(DIRECTIONS))
                weight = TURN_WEIGHT

            dist = cur_dist + weight
            if dist < distances[next]:
                distances[next] = dist
                heapq.heappush(pq, (dist, next))

    return min(
        distances[State(grid.end[0], grid.end[1], NORTH)],
        distances[State(grid.end[0], grid.end[1], SOUTH)],
        distances[State(grid.end[0], grid.end[1], EAST)],
        distances[State(grid.end[0], grid.end[1], WEST)],
    )


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    grid = Grid(data)
    print(find_shortest_path(grid))


if __name__ == "__main__":
    main()
