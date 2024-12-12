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

    def tally_cost(self, r, c):
        char_upper = self.grid[r][c]
        char_lower = char_upper.lower()

        assert char_upper != char_lower

        a, s = self._apr(r, c, char_upper, char_lower)
        print(f"{char_upper}: a={a} s={s}")
        return a * s

    def check_side(self, r, c, ri, ci, chu, chl):
        is_r_edge = r + ri < 0 or r + ri >= self.rows
        is_c_edge = c + ci < 0 or c + ci >= self.cols

        return (
            ci == 0
            and (
                (
                    (0 <= c - 1)  # left cell is a valid index
                    and self.grid[r][c - 1] == chl  # this cell has been processed
                    and (is_r_edge or self.grid[r + ri][c - 1] not in (chl, chu))
                )
                or (
                    (c + 1 < self.cols)  # right cell is valid index
                    and self.grid[r][c + 1] == chl  # this cell has been processed
                    and (is_r_edge or (self.grid[r + ri][c + 1] not in (chl, chu)))
                )
            )
        ) or (
            ri == 0
            and (
                (
                    (0 <= r - 1)  # top cell is a valid index
                    and self.grid[r - 1][c] == chl  # this cell has been processed
                    and (is_c_edge or self.grid[r - 1][c + ci] not in (chl, chu))
                )
                or (
                    (r + 1 < self.cols)  # bottom cell is valid index
                    and self.grid[r + 1][c] == chl  # this cell has been processed
                    and (is_c_edge or (self.grid[r + 1][c + ci] not in (chl, chu)))
                )
            )
        )

    def _apr(self, r: int, c: int, chu: str, chl: str) -> tuple[int, int]:
        # area and perimeter recursive

        area = 1
        sides = 0

        assert self.grid[r][c] == chu
        self.grid[r][c] = chl

        directions = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

        for nr, nc in directions:
            if nr >= self.rows or nr < 0 or nc >= self.cols or nc < 0:
                if not self.check_side(r, c, nr - r, nc - c, chu, chl):
                    print(f"{chu} ({r}, {c}): has side on {nr}, {nc}")
                    sides += 1
                continue

            if self.grid[nr][nc] not in (chu, chl) and not self.check_side(
                r, c, nr - r, nc - c, chu, chl
            ):
                print(f"{chu} ({r}, {c}): has side on {nr}, {nc}")
                sides += 1

        for nr, nc in directions:
            if nr >= self.rows or nr < 0 or nc >= self.cols or nc < 0:
                continue

            if self.grid[nr][nc] == chl:
                # already processed this cell, just continue
                continue

            if self.grid[nr][nc] == chu:
                a, s = self._apr(nr, nc, chu, chl)
                area, sides = area + a, sides + s
                continue

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
