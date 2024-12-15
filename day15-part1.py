import sys

WALL = "#"
ROBOT = "@"
BOX = "O"
EMPTY = "."

DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def find_robot(grid) -> tuple[int, int]:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == ROBOT:
                return r, c
    return -1, -1


def move_box(grid, box, direction) -> bool:
    dr, dc = direction
    br, bc = box
    nr, nc = br + dr, bc + dc

    if grid[nr][nc] == EMPTY:
        grid[nr][nc] = BOX
        return True

    if grid[nr][nc] == WALL:
        return False

    if grid[nr][nc] == BOX:
        return move_box(grid, (nr, nc), direction)

    return False


def move_robot(grid, robot, direction) -> tuple[int, int]:
    dr, dc = DIRECTIONS[direction]
    rr, rc = robot
    nr, nc = rr + dr, rc + dc

    if grid[nr][nc] == EMPTY:
        grid[nr][nc] = ROBOT
        grid[rr][rc] = EMPTY
        return nr, nc

    if grid[nr][nc] == WALL:
        return rr, rc

    if grid[nr][nc] == BOX:
        possible = move_box(grid, (nr, nc), (dr, dc))
        if possible:
            grid[nr][nc] = ROBOT
            grid[rr][rc] = EMPTY
            return nr, nc
        else:
            return rr, rc

    return rr, rc


def gps_sum(grid):
    sum = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == BOX:
                sum += 100 * r + c
    return sum


def print_grid(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            print(grid[r][c], end="")
        print()


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    grid, moves = data.split("\n\n")
    moves = moves.replace("\n", "")
    grid = [list(line) for line in grid.splitlines()]

    robot = find_robot(grid)

    for dir in moves:
        robot = move_robot(grid, robot, dir)

    # print_grid(grid)
    print(gps_sum(grid))


if __name__ == "__main__":
    main()
