import sys
from collections import deque
from itertools import product


class PadSolver:

    def __init__(self, pad):
        self.map = {}
        self.pad = pad
        self.positions = {}
        self.set_positions()
        self.precompute_paths()

    def set_positions(self):
        for r in range(len(self.pad)):
            for c in range(len(self.pad[r])):
                if self.pad[r][c] is not None:
                    self.positions[self.pad[r][c]] = (r, c)

    def precompute_paths(self):
        # key_start, location_start
        # key_end, location_end
        for ks, ls in self.positions.items():
            for ke, le in self.positions.items():
                if (ks == ke):
                    self.map[(ks, ke)] = ["A"]
                else:
                    self.map[(ks, ke)] = self._find_path_bfs(ls, le)

    def _find_path_bfs(self, loc_start: tuple[int, int], loc_end: tuple[int, int]):
        q = deque([(*loc_start, "")])
        ways = []
        best = 10000
        while q:
            r, c, seq = q.popleft()
            if (r, c) == loc_end and len(seq) <= best:
                ways.append(seq + "A")
                best = len(seq)
            elif (r, c) == loc_end and len(seq) > best:
                break

            for nr, nc, cr in [(r-1, c, "^"), (r+1, c, "v"), (r, c-1, "<"), (r, c+1, ">")]:
                if 0 <= nr < len(self.pad) and 0 <= nc < len(self.pad[nr]) and self.pad[nr][nc] != None:
                    q.append((nr, nc, seq + cr))

        return ways


def old_solve(keypad: PadSolver, string: str):
    state = 'A'
    seqs = [""]
    for letter in string:
        ways = keypad.map[state, letter]
        new = []
        for way in ways:
            new.extend([seq + way for seq in seqs])
        state = letter
        seqs = new

    return seqs


def solve(keypad: PadSolver, string: str):
    options = map(lambda pair: keypad.map[pair[0], pair[1]], zip("A" + string, string))
    return map("".join, product(*options))


NUMPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"]
]

DIRPAD = [
    [None, "^", "A"],
    ["<", "v", ">"]
]


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    numpad = PadSolver(NUMPAD)
    dirpad = PadSolver(DIRPAD)

    arrangement = [numpad, dirpad, dirpad]
    required_nums = data.splitlines()

    sum = 0
    min_len = 0
    for string in required_nums:
        seqs = [string]
        for bot in arrangement:
            new = []
            for seq in seqs:
                new.extend(solve(bot, seq))
            min_len = min(map(len, new))
            seqs = filter(lambda x: len(x) == min_len, new)

        num = int(string[:-1])
        complx = min_len * num
        print(f"{string}: {complx}")
        sum += complx
    print("Total:", sum)


if __name__ == "__main__":
    main()
