import sys
from collections import deque

"""
Part 2 Change:

Each side is either a verticle or a horizontal side.
IF we have a verticle side, we check above and below the current char
if either of them have a processed verticle side, then
this is the same side. If not, this is a new side.
"""


class Grid:
    def __init__(self, data: str):
        lines = data.strip().splitlines()
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.grid = list(map(list, lines))

    def tally_cost(self, r, c):
        char_upper = self.grid[r][c]
        char_lower = char_upper.lower()

        assert char_upper != char_lower

        a, s = self._apr(r, c, char_upper, char_lower)
        return a * s

    def check_side(self, r, c, ri, ci, chu, chl):
        is_r_edge = r + ri < 0 or r + ri >= self.rows
        is_c_edge = c + ci < 0 or c + ci >= self.cols

        return (
            ci == 0
            and (
                (
                    (0 <= c - 1)  # left cell is a valid index
                    and self.grid[r][c - 1] == chu  # this cell has been processed
                    and (is_r_edge or self.grid[r + ri][c - 1] not in (chl, chu))
                )
                or (
                    (c + 1 < self.cols)  # right cell is valid index
                    and self.grid[r][c + 1] == chu  # this cell has been processed
                    and (is_r_edge or (self.grid[r + ri][c + 1] not in (chl, chu)))
                )
            )
        ) or (
            ri == 0
            and (
                (
                    (0 <= r - 1)  # top cell is a valid index
                    and self.grid[r - 1][c] == chu  # this cell has been processed
                    and (is_c_edge or self.grid[r - 1][c + ci] not in (chl, chu))
                )
                or (
                    (r + 1 < self.cols)  # bottom cell is valid index
                    and self.grid[r + 1][c] == chu  # this cell has been processed
                    and (is_c_edge or (self.grid[r + 1][c + ci] not in (chl, chu)))
                )
            )
        )

    def _apr(self, r: int, c: int, chu: str, chl: str) -> tuple[int, int]:
        area = 0
        sides = 0
        queue = deque([(r, c)])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        assert self.grid[r][c] == chu

        while queue:
            cr, cc = queue.popleft()

            if self.grid[cr][cc] == chl:
                continue

            self.grid[cr][cc] = chl
            area += 1

            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc

                if nr >= self.rows or nr < 0 or nc >= self.cols or nc < 0:
                    if not self.check_side(cr, cc, dr, dc, chu, chl):
                        sides += 1
                    continue

                if self.grid[nr][nc] not in (chu, chl):
                    if not self.check_side(cr, cc, dr, dc, chu, chl):
                        sides += 1
                    continue

                if self.grid[nr][nc] == chl:
                    continue

                if self.grid[nr][nc] == chu:
                    queue.append((nr, nc))

        return area, sides


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    grid = Grid(data)
    count = 0
    for r in range(grid.rows):
        for c in range(grid.cols):
            if "A" <= grid.grid[r][c] <= "Z":
                count += grid.tally_cost(r, c)

    print(count)


if __name__ == "__main__":
    main()
