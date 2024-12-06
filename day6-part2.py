import sys


with open(sys.argv[1]) as f:
    data = f.read()


INF = 9999999

GUARD = "^"
OBSTRUCTION = "#"
EMPTY_SPOT = "."

VISITED = "V"
VISITED_UP = "K"
VISITED_DOWN = "J"
VISITED_LEFT = "H"
VISITED_RIGHT = "L"

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

dir_change_map = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
dir_marker_map = {
    UP: VISITED_UP,
    DOWN: VISITED_DOWN,
    LEFT: VISITED_LEFT,
    RIGHT: VISITED_RIGHT,
}

# Rules:
# 1. If something directly infront, turn right
# 2. Otherwise, take step forward.

array = []
guard_x = -1
guard_y = -1

# find starting position of guard
for i, line in enumerate(data.strip().splitlines()):
    index = line.find(GUARD)
    if index != -1:
        guard_y = i
        guard_x = index
    array.append([char for char in line.strip()])


def count_guard_steps(array, guard_x, guard_y):
    guard_direction = UP
    array[guard_y][guard_x] = dir_marker_map[guard_direction]
    ways_visited = [[[] for _ in row] for row in array]
    width = len(array[0])
    height = len(array)
    # this tracks the distinct positions
    guard_steps = 1

    while True:
        next_x = guard_x + guard_direction[0]
        next_y = guard_y + guard_direction[1]

        if next_x < 0 or next_x >= height or next_y < 0 or next_y >= width:
            # we are now out of the map
            break

        if array[next_y][next_x] == "#":
            guard_direction = dir_change_map[guard_direction]
            continue

        if dir_marker_map[guard_direction] in ways_visited[next_y][next_x]:
            # this indicates that we hit a loop!
            return INF

        if array[next_y][next_x] == EMPTY_SPOT:
            guard_steps += 1
            array[next_y][next_x] = VISITED

        # print(f"x: {guard_x} -> {next_x}, y {guard_y} -> {next_y}")
        guard_x = next_x
        guard_y = next_y
        ways_visited[guard_y][guard_x].append(dir_marker_map[guard_direction])

    return guard_steps


# we need to count the number of loops possible
# we can't place a obstacle where the guard current is.

loops = 0

print("ways to try: ", len(array) * len(array[0]))
print("rows to try: ", len(array))

for r in range(len(array)):
    for c in range(len(array[r])):
        if (array[r][c] == OBSTRUCTION) or (r == guard_x and c == guard_y):
            # either case, we can't place something here
            continue

        tmp = array[r][c]
        array[r][c] = OBSTRUCTION
        steps = count_guard_steps(array, guard_x, guard_y)
        array[r][c] = tmp

        if steps == INF:
            loops += 1
    print(f"Completed row {r}: {loops}")

print(loops)
