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

    def find_edge(self, r, c, dr, dc, chu, chl):
        edge_set = {(r, c, dr, dc)}
        if dr == 0:
            # vertical edge

            # going upward
            rup = r - 1
            while rup >= 0 and self.grid[rup][c] in (chu, chl):
                edge_set.add((rup, c, dr, dc))
                rup -= 1

            # goind downward
            rdw = r + 1
            while rdw < self.rows and self.grid[rdw][c] in (chu, chl):
                edge_set.add((rdw, c, dr, dc))
                rdw += 1

        else:
            # horizontal edge
            assert dc == 0

            # going left
            cup = c - 1
            while cup >= 0 and self.grid[r][cup] in (chu, chl):
                edge_set.add((r, cup, dr, dc))
                cup -= 1

            # goind right
            cdw = c + 1
            while cdw < self.cols and self.grid[r][cdw] in (chu, chl):
                edge_set.add((r, cdw, dr, dc))
                cdw += 1

        return edge_set

    def is_side_counted(self, r, c, dr, dc, counted_sides):
        return (r, c, dr, dc) in counted_sides

    def _apr(self, r: int, c: int, chu: str, chl: str) -> tuple[int, int]:
        area = 0
        sides = 0
        queue = deque([(r, c)])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        assert self.grid[r][c] == chu

        # (r, c, dr, dr)
        counted_sides = set()

        while queue:
            cr, cc = queue.popleft()

            if self.grid[cr][cc] == chl:
                continue

            self.grid[cr][cc] = chl
            area += 1

            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc

                if nr >= self.rows or nr < 0 or nc >= self.cols or nc < 0:
                    if not self.is_side_counted(cr, cc, dr, dc, counted_sides):
                        counted_sides.update(self.find_edge(cr, cc, dr, dc, chu, chl))
                        sides += 1
                    continue

                if self.grid[nr][nc] == chl:
                    continue

                if self.grid[nr][nc] == chu:
                    queue.append((nr, nc))

                if not self.is_side_counted(cr, cc, dr, dc, counted_sides):
                    counted_sides.update(self.find_edge(cr, cc, dr, dc, chu, chl))
                    sides += 1

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
