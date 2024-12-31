import sys
import re
from typing import Callable


MAP = {
    "AND": lambda x, y: x and y,
    "OR": lambda x, y: x or y,
    "XOR": lambda x, y: (x and not y) or (not x and y)
}

Func = Callable[[bool, bool], bool]


class Node:
    def __init__(self, name: str, state: bool | None = None):
        self.name = name
        self.state = state

    def __repr__(self) -> str:
        sm = {True: "1", False: "0", None: " "}
        return f"{self.name}[{sm[self.state]}]"

    def __str__(self) -> str:
        sm = {True: "1", False: "0", None: " "}
        return f"{self.name}[{sm[self.state]}]"


class Connection:
    def __init__(self, a: Node, op: Func, b: Node, out: Node):
        self.a = a
        self.b = b
        self.op = op
        self.out = out
        self.evaluated = self.out.state is not None

    def can_eval(self):
        return None not in (self.a.state, self.b.state)

    def eval(self):
        assert self.a.state is not None
        assert self.b.state is not None
        self.out.state = self.op(self.a.state, self.b.state)
        self.evaluated = True

    def __repr__(self) -> str:
        op = next((k for k, v in MAP.items() if v == self.op), None)
        return f"{self.a.name} {op} {self.b.name} -> {self.out.name}"


def complete_circuit(uninit_nodes: set[Node], conns: set[Connection]):
    while uninit_nodes:
        # look through connections to see if two inputs are in init_nodes
        eval = False
        for conn in conns:
            if not conn.evaluated and conn.can_eval():
                eval = True
                conn.eval()
                uninit_nodes.remove(conn.out)

        if not eval:
            print("some uninit nodes exist")
            break


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    initalizations, connections = data.split("\n\n")

    nodes = {}
    uninitialized_nodes = set()
    conns = set()

    for n in initalizations.strip().split("\n"):
        name, value = n.split(": ")
        nodes[name] = (Node(name, bool(int(value))))

    pattern = r"([a-z0-9]+)\s+(AND|XOR|OR)\s+([a-z0-9]+)\s+->\s+([a-z0-9]+)"

    for c in connections.strip().split("\n"):
        match = re.match(pattern, c)
        assert match is not None
        a, op, b, out = match[1], match[2], match[3], match[4]
        for x in a, b, out:
            if x not in nodes:
                nodes[x] = Node(x)
                uninitialized_nodes.add(nodes[x])
        conns.add(Connection(nodes[a], MAP[op], nodes[b], nodes[out]))

    complete_circuit(uninitialized_nodes, conns)
    sm = {True: "1", False: "0", None: " "}

    filtered_nodes = filter(lambda x: x.name[0] == "z", nodes.values())
    sorted_nodes = sorted(filtered_nodes, key=lambda x: x.name, reverse=True)
    state_values = map(lambda x: sm[x.state], sorted_nodes)
    binary_string = "".join(state_values)
    result = int(binary_string, base=2)

    print(result)


if __name__ == "__main__":
    main()
