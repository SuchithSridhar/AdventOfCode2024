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


def find_most_significant_output_bit(connections):
    return max(map(lambda c: c.out, (
        filter(lambda c: c.out.name[0] == "z", connections)
    )), key=lambda x: x.name)


# this function is heavily inspired by reddit user: u/lscddit
def find_mistakes(connections: set[Connection]) -> set[Connection]:
    mistakes = set()
    msob = find_most_significant_output_bit(connections)
    for conn in connections:
        if (
            conn.out.name[0] == "z" and
            conn.out != msob and
            conn.op != MAP["XOR"]
        ):
            mistakes.add(conn)

        if (
            conn.op == MAP["XOR"] and
            conn.a.name[0] not in "xy" and
            conn.b.name[0] not in "xy" and
            conn.out.name[0] != "z"
        ):
            mistakes.add(conn)

        if (
            conn.op == MAP["AND"] and
            "x00" not in (conn.a.name, conn.b.name)
        ):
            for c2 in connections:
                if conn.out in (c2.a, c2.b) and c2.op != MAP["OR"]:
                    mistakes.add(conn)

        if (conn.op == MAP["XOR"]):
            for c2 in connections:
                if conn.out in (c2.a, c2.b) and c2.op == MAP["OR"]:
                    mistakes.add(conn)

    return mistakes


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    initalizations, connections = data.split("\n\n")

    nodes = {}
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
        conns.add(Connection(nodes[a], MAP[op], nodes[b], nodes[out]))

    mistakes = sorted(map(lambda x: x.out.name, find_mistakes(conns)))
    print(",".join(mistakes))


if __name__ == "__main__":
    main()
