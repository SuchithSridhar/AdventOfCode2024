import sys

# +ve x is to the right of the matrix ->
# +ve y is going down the matrix V


def vec_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def vec_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def vec_sub_till_end(a, b, rows, cols):
    new = vec_sub(a, b)
    nodes = set()
    while vec_in_graph(new, rows, cols):
        nodes.add(new)
        new = vec_sub(new, b)
    return nodes


def vec_add_till_end(a, b, rows, cols):
    new = vec_add(a, b)
    nodes = set()
    while vec_in_graph(new, rows, cols):
        nodes.add(new)
        new = vec_add(new, b)
    return nodes


def vec_in_graph(a, rows, cols):
    return a[0] >= 0 and a[1] >= 0 and a[0] < rows and a[1] < cols


with open(sys.argv[1]) as f:
    data = f.read()

data = list(map(list, data.strip().splitlines()))

# Search for the nodes
nodes = {}
for r in range(len(data)):
    for c in range(len(data[r])):
        if data[r][c] != ".":
            if data[r][c] in nodes:
                nodes[data[r][c]].append((r, c))
            else:
                nodes[data[r][c]] = [(r, c)]

rows = len(data)
cols = len(data[0])

# Each pair has two antinodes
antinodes = set()
for _, antenas in nodes.items():
    for i in range(len(antenas)):
        for j in range(i + 1, len(antenas)):
            a, b = antenas[i], antenas[j]
            if a == b:
                continue
            antinodes.add(a)
            antinodes.add(b)
            vec = vec_sub(b, a)
            an1 = vec_sub_till_end(a, vec, rows, cols)
            an2 = vec_add_till_end(b, vec, rows, cols)
            antinodes = antinodes.union(an1.union(an2))

print(len(antinodes))
