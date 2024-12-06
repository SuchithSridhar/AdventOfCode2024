import sys


with open(sys.argv[1]) as f:
    data = f.read()


GUARD = "^"
OBSTRUCTION = "#"
EMPTY_SPOT = "."
VISITED = "X"

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

dir_change_map = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

# Rules:
# 1. If something directly infront, turn right
# 2. Otherwise, take step forward.

array = []
guard_x = -1
guard_y = -1
guard_direction = UP

# this tracks the distinct positions
guard_steps = 1

# find starting position of guard
for i, line in enumerate(data.strip().splitlines()):
    index = line.find(GUARD)
    if index != -1:
        guard_y = i
        guard_x = index
    array.append([char for char in line.strip()])

width = len(array[0])
height = len(array)

# we replace the spot with an empty spot since we're tracking the number.
array[guard_y][guard_x] = VISITED

while True:
    next_x = guard_x + guard_direction[0]
    next_y = guard_y + guard_direction[1]

    if next_x < 0 or next_x >= height or next_y < 0 or next_y >= width:
        # we are now out of the map
        break

    if array[next_y][next_x] == "#":
        guard_direction = dir_change_map[guard_direction]
        continue

    if array[next_y][next_x] == EMPTY_SPOT:
        guard_steps += 1
        array[next_y][next_x] = VISITED

    guard_x = next_x
    guard_y = next_y

print(guard_steps)
