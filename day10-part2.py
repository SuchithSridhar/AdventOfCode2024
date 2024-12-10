import sys


class Grid:
    def __init__(self, data: str):
        lines = data.strip().splitlines()
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.grid = list(map(lambda x: list(map(int, x)), lines))

    def find_peaks(self, r, c) -> int:
        return self._find_peak_recur(r, c, 0)

    def _find_peak_recur(self, r, c, cur_elem) -> int:
        if self.grid[r][c] == 9:
            return 1

        count = 0

        if r - 1 >= 0 and self.grid[r - 1][c] == cur_elem + 1:
            count += self._find_peak_recur(r - 1, c, cur_elem + 1)

        if r + 1 < self.rows and self.grid[r + 1][c] == cur_elem + 1:
            count += self._find_peak_recur(r + 1, c, cur_elem + 1)

        if c - 1 >= 0 and self.grid[r][c - 1] == cur_elem + 1:
            count += self._find_peak_recur(r, c - 1, cur_elem + 1)

        if c + 1 < self.cols and self.grid[r][c + 1] == cur_elem + 1:
            count += self._find_peak_recur(r, c + 1, cur_elem + 1)

        return count


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    grid = Grid(data)
    count = 0
    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.grid[r][c] == 0:
                count += grid.find_peaks(r, c)

    print(count)


if __name__ == "__main__":
    main()
