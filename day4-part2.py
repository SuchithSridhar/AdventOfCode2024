import sys

with open(sys.argv[1]) as f:
    data = f.read()

data = data.splitlines()


def a(data, r, c):
    if 0 <= r < len(data) and 0 <= c < len(data[r]):
        return data[r][c]
    return ""


def search_xmas(d, r, c):
    l = a(d, r - 1, c - 1) + a(d, r, c) + a(d, r + 1, c + 1)
    r = a(d, r + 1, c - 1) + a(d, r, c) + a(d, r - 1, c + 1)

    return (l == "MAS" or l == "SAM") and (r == "MAS" or r == "SAM")


count = 0
for r in range(len(data)):
    for c in range(len(data[r])):
        if data[r][c] == "A":
            count += search_xmas(data, r, c)

print(count)
