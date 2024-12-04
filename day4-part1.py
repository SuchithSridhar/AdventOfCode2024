import sys

with open(sys.argv[1]) as f:
    data = f.read()

data = data.splitlines()


def search_xmas(data, r, c):
    # search left to right
    count = 0
    rows = len(data)
    cols = len(data[0])

    count += (
        (c + 3 < cols)
        and data[r][c + 1] == "M"
        and data[r][c + 2] == "A"
        and data[r][c + 3] == "S"
    )
    count += (
        (c - 3 >= 0)
        and data[r][c - 1] == "M"
        and data[r][c - 2] == "A"
        and data[r][c - 3] == "S"
    )
    count += (
        (r + 3 < rows)
        and data[r + 1][c] == "M"
        and data[r + 2][c] == "A"
        and data[r + 3][c] == "S"
    )
    count += (
        (r - 3 >= 0)
        and data[r - 1][c] == "M"
        and data[r - 2][c] == "A"
        and data[r - 3][c] == "S"
    )

    count += (
        (c + 3 < cols and r + 3 < rows)
        and data[r + 1][c + 1] == "M"
        and data[r + 2][c + 2] == "A"
        and data[r + 3][c + 3] == "S"
    )
    count += (
        (c - 3 >= 0 and r - 3 >= 0)
        and data[r - 1][c - 1] == "M"
        and data[r - 2][c - 2] == "A"
        and data[r - 3][c - 3] == "S"
    )

    count += (
        (c + 3 < cols and r - 3 >= 0)
        and data[r - 1][c + 1] == "M"
        and data[r - 2][c + 2] == "A"
        and data[r - 3][c + 3] == "S"
    )
    count += (
        (c - 3 >= 0 and r + 3 < rows)
        and data[r + 1][c - 1] == "M"
        and data[r + 2][c - 2] == "A"
        and data[r + 3][c - 3] == "S"
    )

    return count


count = 0
for r in range(len(data)):
    for c in range(len(data[r])):
        if data[r][c] == "X":
            count += search_xmas(data, r, c)

print(count)
