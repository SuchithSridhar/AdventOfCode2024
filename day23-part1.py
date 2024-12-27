from collections import deque
import sys


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def add_neighbour(self, n):
        self.neighbours.add(n)


def add_edge(a: Node, b: Node):
    a.add_neighbour(b)
    b.add_neighbour(a)


def find_triple_cycle(node: Node):
    cycles = set()
    for first in node.neighbours:
        for second in first.neighbours:
            if second == node:
                continue
            if node in second.neighbours:
                cycles.add(tuple(sorted([node.name, first.name, second.name])))
    return cycles


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    computers = {}
    t_computers = set()

    for connection in data.splitlines():
        left, right = connection.split("-")
        if left not in computers:
            computers[left] = Node(left)
        if right not in computers:
            computers[right] = Node(right)

        if left.startswith("t"):
            t_computers.add(left)
        if right.startswith("t"):
            t_computers.add(right)

        left_node, right_node = computers[left], computers[right]
        add_edge(left_node, right_node)

    cycles = set()
    for t_comp in t_computers:
        cycles.update(find_triple_cycle(computers[t_comp]))

    print(len(cycles))


if __name__ == "__main__":
    main()
