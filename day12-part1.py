import sys


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

        a, p = self._apr(r, c, char_upper, char_lower)
        print(f"{char_upper}: area:{a}, peri:{p}")
        return a * p

    def _apr(self, r: int, c: int, chu: str, chl: str) -> tuple[int, int]:
        # area and perimeter recursive

        area = 1
        peri = 0

        assert self.grid[r][c] == chu
        self.grid[r][c] = chl

        directions = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

        for nr, nc in directions:
            if nr >= self.rows or nr < 0 or nc >= self.cols or nc < 0:
                peri += 1
                continue

            if self.grid[nr][nc] == chl:
                # already processed this cell, just continue
                continue

            if self.grid[nr][nc] == chu:
                a, p = self._apr(nr, nc, chu, chl)
                area, peri = area + a, peri + p
                continue

            assert self.grid[nr][nc] != chu and self.grid[nr][nc] != chl
            peri += 1

        return area, peri


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
