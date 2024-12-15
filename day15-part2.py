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

BOX_LEFT = "["
BOX_RIGHT = "]"
BIG_BOX = BOX_LEFT + BOX_RIGHT

SWITCH_MAP = {
    WALL: WALL + WALL,
    BOX: BIG_BOX,
    EMPTY: EMPTY + EMPTY,
    ROBOT: ROBOT + EMPTY,
}


def find_robot(grid) -> tuple[int, int]:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == ROBOT:
                return r, c
    return -1, -1


def build_grid(data: str) -> list[list[str]]:
    return [[SWITCH_MAP[char] for char in line] for line in data.strip().splitlines()]


def move_box(grid, box, direction) -> bool:
    dr, dc = direction
    br, bc = box

    if dr == 0:
        # horizontal move
        nr, nc = br, bc + 2 * dc  # because box is 2-wide
        if grid[nr][nc] == EMPTY:  # [].
            grid[nr][nc] = grid[nr][nc - dc]  # []]
            grid[nr][nc - dc] = grid[nr][bc]  # [[]
            grid[br][bc] = EMPTY  # .[]
            return True

        if grid[nr][nc] == WALL:
            return False

        if grid[nr][nc] in BIG_BOX:
            if move_box(grid, (nr, nc), direction):
                grid[nr][nc] = grid[nr][nc - dc]  # []]
                grid[nr][nc - dc] = grid[nr][bc]  # [[]
                grid[br][bc] = EMPTY  # .[]
            else:
                return False

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

    if grid[nr][nc] in BIG_BOX and dr == 0:
        # we are moving horizontally
        possible = move_box(grid, (nr, nc), (dr, dc))
        if possible:
            grid[nr][nc] = ROBOT
            grid[rr][rc] = EMPTY
            return nr, nc
        else:
            return rr, rc

    if grid[nr][nc] in BIG_BOX and dc == 0:
        # we are move vertically
        pass
    # TODO: Handle vertical box movement.
    # remember that a single box may push two boxes now.
    # .....#...
    # ..[][][].
    # ...[][]..
    # ....[]...
    # becuase of such cases, we can't split them into recursive calls perse.
    # may be possible if move_box tells you if the move is possible but doesn't
    # actually move the box. Then if all boxes are moveable, then we have a
    # different function to move all the boxes.

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
    grid = build_grid(data)

    robot = find_robot(grid)

    for dir in moves:
        robot = move_robot(grid, robot, dir)

    # print_grid(grid)
    print(gps_sum(grid))


if __name__ == "__main__":
    main()
