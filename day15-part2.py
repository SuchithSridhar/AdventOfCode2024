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
    WALL: [WALL, WALL],
    BOX: [BOX_LEFT, BOX_RIGHT],
    EMPTY: [EMPTY, EMPTY],
    ROBOT: [ROBOT, EMPTY],
}


def find_robot(grid) -> tuple[int, int]:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == ROBOT:
                return r, c
    return -1, -1


def build_grid(data: str) -> list[list[str]]:
    grid = []
    for line in data.strip().splitlines():
        row = []
        for char in line:
            row.extend(SWITCH_MAP[char])
        grid.append(row)
    return grid


def move_box_horizontal(grid, box, direction) -> bool:
    dr, dc = direction
    br, bc = box

    assert dr == 0

    nr, nc = br, bc + 2 * dc  # because box is 2-wide
    if grid[nr][nc] == EMPTY:  # [].
        grid[nr][nc] = grid[nr][nc - dc]  # []]
        grid[nr][nc - dc] = grid[nr][bc]  # [[]
        grid[br][bc] = EMPTY  # .[]
        return True

    if grid[nr][nc] == WALL:
        return False

    if grid[nr][nc] in BIG_BOX:
        if move_box_horizontal(grid, (nr, nc), direction):
            grid[nr][nc] = grid[nr][nc - dc]  # []]
            grid[nr][nc - dc] = grid[nr][bc]  # [[]
            grid[br][bc] = EMPTY  # .[]
        else:
            return False

    return True


def move_box_vertical(grid, box_left, direction) -> bool:
    dr, dc = direction
    br, bc = box_left

    assert dc == 0

    can_move = True
    items = [(br, bc), (br, bc + 1)]  # add box left and box right to list
    index = 0

    while index < len(items):
        # look ahead and append to items
        ir, ic = items[index]

        c = grid[ir + dr][ic]
        if c == BOX_LEFT:
            left = (ir + dr, ic)
            right = (ir + dr, ic + 1)
            if left not in items:
                items.append(left)
            if right not in items:
                items.append(right)

        elif c == BOX_RIGHT:
            left = (ir + dr, ic - 1)
            right = (ir + dr, ic)
            if left not in items:
                items.append(left)
            if right not in items:
                items.append(right)

        elif c == WALL:
            can_move = False
            break

        index += 1

    if not can_move:
        return False

    # need to move all the boxes
    for br, bc in reversed(items):
        grid[br + dr][bc] = grid[br][bc]
        grid[br][bc] = EMPTY

    return True


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
        possible = move_box_horizontal(grid, (nr, nc), (dr, dc))
        if possible:
            grid[nr][nc] = ROBOT
            grid[rr][rc] = EMPTY
            return nr, nc
        else:
            return rr, rc

    if grid[nr][nc] == BOX_LEFT and dc == 0:
        possible = move_box_vertical(grid, (nr, nc), (dr, dc))
        if possible:
            grid[nr][nc] = ROBOT
            grid[rr][rc] = EMPTY
            return nr, nc
        else:
            return rr, rc
    if grid[nr][nc] == BOX_RIGHT and dc == 0:
        possible = move_box_vertical(grid, (nr, nc - 1), (dr, dc))
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
            if grid[r][c] == BOX_LEFT:
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
    grid = build_grid(grid)

    robot = find_robot(grid)

    for i, dir in enumerate(moves):
        robot = move_robot(grid, robot, dir)

    # print_grid(grid)
    print(gps_sum(grid))


if __name__ == "__main__":
    main()
