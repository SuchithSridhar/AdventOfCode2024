import sys


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def add_neighbour(self, n):
        self.neighbours.add(n)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class Clique:
    def __init__(self):
        self.nodes = set()

    def __hash__(self):
        return hash(tuple(sorted([x.name for x in self.nodes])))


def add_edge(a: Node, b: Node):
    a.add_neighbour(b)
    b.add_neighbour(a)


# Code taken directly from:
# https://www.geeksforgeeks.org/maximal-clique-problem-recursive-solution/
# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
# R holds current clique
# P holds possible nodes for clique
# X already processed nodes
def bron_kerbosch(R, P, X):
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(
            R | {v},
            P & v.neighbours,
            X & v.neighbours,
        )
        X.add(v)


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    computers = {}

    for connection in data.splitlines():
        left, right = connection.split("-")
        if left not in computers:
            computers[left] = Node(left)
        if right not in computers:
            computers[right] = Node(right)
        add_edge(computers[left], computers[right])

    max_set = max(bron_kerbosch(set(), set(computers.values()), set()), key=len)
    print(",".join(sorted(map(lambda x: x.name, list(max_set)))))


if __name__ == "__main__":
    main()
