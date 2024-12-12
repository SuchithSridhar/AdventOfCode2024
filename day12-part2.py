import sys

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
        self.sides_set = set()

    def tally_cost(self, r, c):
        char_upper = self.grid[r][c]
        char_lower = char_upper.lower()

        assert char_upper != char_lower

        self.sides_set = set()
        self.chu = char_upper
        self.chl = char_lower
        self.chr = (self.chu, self.chl)

        a, s = self._apr(r, c)
        return a * s

    def is_edge(self, r, c, dr, dc):
        nr, nc = r + dr, c + dc
        return (
            nr < 0
            or nr >= self.rows
            or nc < 0
            or nc >= self.cols
            or self.grid[nr][nc] not in self.chr
        )

    def explore_side(self, r, c, dr, dc):
        self.sides_set.add((r, c, dr, dc))

        # 0 <= nr < self.rows
        # and 0 <= nc < self.cols
        # and self.grid[nr][nc] in (chu, chl)

        if dr == 0:
            # vertical side
            # look one spot up
            nr, nc = r - 1, c
            if (
                0 <= nr
                and self.grid[nr][nc] in self.chr
                and (nr, nc, dr, dc) not in self.sides_set
                and self.is_edge(nr, nc, dr, dc)
            ):
                self.explore_side(nr, nc, dr, dc)

            # look down
            nr, nc = r + 1, c
            if (
                nr < self.rows
                and self.grid[nr][nc] in self.chr
                and (nr, nc, dr, dc) not in self.sides_set
                and self.is_edge(nr, nc, dr, dc)
            ):
                self.explore_side(nr, nc, dr, dc)

        if dc == 0:
            # horizontal side
            # look one spot left
            nr, nc = r, c - 1
            if (
                0 <= nc
                and self.grid[nr][nc] in self.chr
                and (nr, nc, dr, dc) not in self.sides_set
                and self.is_edge(nr, nc, dr, dc)
            ):
                self.explore_side(nr, nc, dr, dc)

            # look down
            nr, nc = r, c + 1
            if (
                nc < self.rows
                and self.grid[nr][nc] in self.chr
                and (nr, nc, dr, dc) not in self.sides_set
                and self.is_edge(nr, nc, dr, dc)
            ):
                self.explore_side(nr, nc, dr, dc)

    def _apr(self, r: int, c: int) -> tuple[int, int]:
        area = 1
        sides = 0

        assert self.grid[r][c] == self.chu
        self.grid[r][c] = self.chl

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if nr >= self.rows or nr < 0 or nc >= self.cols or nc < 0:
                if (r, c, dr, dc) not in self.sides_set:
                    sides += 1
                    self.explore_side(r, c, dr, dc)
                continue

            if self.grid[nr][nc] == self.chl:
                # already processed this cell, just continue
                continue

            if self.grid[nr][nc] == self.chu:
                a, s = self._apr(nr, nc)
                area, sides = area + a, sides + s
                continue

            assert self.grid[nr][nc] not in self.chr
            if (r, c, dr, dc) not in self.sides_set:
                sides += 1
                self.explore_side(r, c, dr, dc)

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
